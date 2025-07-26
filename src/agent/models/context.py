from dataclasses import dataclass


@dataclass
class ContextData:
    name: str
    filename: str
    dirname: str
    content: str
    tags: list[str]
