from utils.file_reader import read_markdown, calculate_hash
from utils.parse import replacement_modifiers, chunk_text
from .models.context import ContextData
from pathlib import Path
from database import mongo_client, chroma_client
import os
import config
import ollama
from watchfiles import awatch, Change


class Doku:
    async def start_monitor(self):
        async for changes in awatch(config.MONITOR_CHANGES_OBSERVER_PATH):
            for change_type, src_path in changes:
                if change_type is Change.modified:
                    path = Path(src_path)
                    path_parts = list(path.parts)

                    # Only markdown
                    if path.suffix != ".md":
                        continue

                    relative_path = None
                    for part in path_parts:
                        if part == "src":
                            index = path_parts.index(part)
                            relative_path = Path(*path_parts[index:])
                            print(relative_path.stem)
                            break

                    if relative_path is None:
                        continue

                    path = Path(relative_path)
                    path_parts = list(path.parent.parts)
                    path_parts.remove("src")

                    context_name = f"{str.join(':', path_parts)}:{path.stem}"
                    context = await mongo_client.find_context(name=context_name)

                    if context is not None:
                        content = replacement_modifiers(read_markdown(filepath=path))
                        content_hash = calculate_hash(content)

                        if content_hash != context["hash"]:
                            chroma_client.contexts.delete(
                                where={"mongo_id": str(context["_id"])}
                            )

                            await mongo_client.contexts.delete_one(
                                {"name": context_name}
                            )

                            await self.load_context()

    async def load_context(self):
        context_dict: dict[str, ContextData] = {}

        for current_path, folders, files in os.walk("src/context"):
            # Files
            for file in files:
                path = Path(os.path.join(current_path, file))

                path_parts = list(path.parent.parts)
                path_parts.remove("src")

                print(path.suffix)

                # Markdown
                if path.suffix == ".md":
                    content = replacement_modifiers(read_markdown(filepath=path))

                    context_name = f"{str.join(':', path_parts)}:{path.stem}"
                    context_dict[context_name] = ContextData(
                        name=context_name,
                        filename=path.name,
                        dirname=str(path.parent),
                        hash=calculate_hash(content),
                        content=content,
                        tags=path_parts,
                    )

        for key, value in context_dict.items():
            find_mongo = await mongo_client.find_context(key)

            if find_mongo is None:
                mongo_id = await mongo_client.save_context(value)

                chunks = chunk_text(text=value.content)

                for idx, chunk in enumerate(chunks):
                    chroma_client.contexts.add(
                        ids=[f"{mongo_id}:{idx}"],
                        documents=[chunk],
                        metadatas={
                            "mongo_id": str(mongo_id),
                            "name": value.name,
                            "chunk_index": idx,
                            "tags": str.join(", ", value.tags),
                        },
                    )

    async def chat(self, content: str):
        personality = await mongo_client.find_context(config.MONGO_NAME_PERSONALITY)

        if personality is None:
            raise ValueError(f"Not found in Mongo {config.MONGO_NAME_PERSONALITY}")

        find_process = chroma_client.contexts.query(query_texts=content, n_results=1)
        context: str = ""

        if len(find_process["documents"]) > 0 and find_process["distances"][0][0] < 95:
            context = await mongo_client.find_context(
                find_process["metadatas"][0][0]["name"]
            )

        for chunk in ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": personality["content"]},
                {
                    "role": "user",
                    "content": f"Este es un contexto que recibes, acorde a la pregunta del usuario, en cuestión: {context['content']}",
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            stream=True,
            options={"temperature": 0.5},
        ):
            print(chunk["message"]["content"], end="", flush=True)
