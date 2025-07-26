from utils import logger


def read_markdown(filepath: str, scope: str = "Context"):
    logger.reading_filepath(scope=scope, type="Markdown", filepath=filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
