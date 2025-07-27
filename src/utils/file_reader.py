from utils import logger
import hashlib


def read_markdown(filepath: str, scope: str = "Context"):
    logger.reading_filepath(scope=scope, type="Markdown", filepath=filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def calculate_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
