import config
from dotenv import load_dotenv

load_dotenv()

REPLACEMENT_MODIFIERS: dict[str, str] = {"{{product_name}}": config.PRODUCT_NAME}


def replacement_modifiers(text: str):
    for key, value in REPLACEMENT_MODIFIERS.items():
        text = text.replace(key, value)

    return text


def chunk_text(text: str, max_tokens: int = 1000) -> list[str]:
    import tiktoken

    encoding = tiktoken.get_encoding("cl100k_base")

    chunks = []
    current_chunk = []

    def num_tokens(text: str) -> int:
        return len(encoding.encode(text))

    for paragraph in text.split("\n\n"):
        if not paragraph.strip():
            continue

        paragraph = paragraph.strip()
        paragraph_tokens = num_tokens(paragraph)

        if paragraph_tokens > max_tokens:
            sentences = paragraph.split(". ")
            temp_chunk = ""
            for sentence in sentences:
                sentence = sentence.strip()
                if num_tokens(temp_chunk + sentence) < max_tokens:
                    temp_chunk += sentence + ". "
                else:
                    chunks.append(temp_chunk.strip())
                    temp_chunk = sentence + ". "
            if temp_chunk:
                chunks.append(temp_chunk.strip())
        else:
            current_chunk.append(paragraph)

            combined = "\n\n".join(current_chunk)
            if num_tokens(combined) > max_tokens:
                current_chunk.pop()
                chunks.append("\n\n".join(current_chunk).strip())
                current_chunk = [paragraph]

    if current_chunk:
        chunks.append("\n\n".join(current_chunk).strip())

    return chunks
