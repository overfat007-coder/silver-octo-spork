"""Event schemas for cross-module integration bus."""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Event:
    event_type: str
    payload: dict
    event_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    retries: int = 0

    def to_dict(self) -> dict:
        return asdict(self)
