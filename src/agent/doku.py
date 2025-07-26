from utils.file_reader import read_markdown
from utils.parse import replacement_modifiers
from .models.context import ContextData
from pathlib import Path
from database import mongo_client
import os


class Doku:
    async def load_context(self):
        context_dict: dict[str, ContextData] = {}

        for current_path, folders, files in os.walk("src/context"):
            # Files
            for file in files:
                path = Path(os.path.join(current_path, file))

                path_parts = list(path.parent.parts)
                path_parts.remove("src")

                # Markdown
                if file.endswith(path.suffix):
                    content = replacement_modifiers(read_markdown(filepath=path))

                    context_name = str.join(":", path_parts)
                    context_dict[context_name] = ContextData(
                        name=context_name,
                        filename=path.name,
                        dirname=str(path.parent),
                        content=content,
                        tags=path_parts,
                    )

        for key, value in context_dict.items():
            find = await mongo_client.find_context(key)

            if find is None:
                await mongo_client.save_context(value)
