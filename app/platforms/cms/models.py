"""CMS domain models."""
from dataclasses import dataclass, field

@dataclass
class ContentType:
    name: str
    fields: dict[str, str]

@dataclass
class ContentEntry:
    entry_id: str
    type_name: str
    data: dict
    version: int = 1
    status: str = "draft"
    history: list[dict] = field(default_factory=list)
