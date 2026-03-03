"""Event log helper for auditing mobile module actions."""

from dataclasses import dataclass, field


@dataclass
class EventLog:
    events: list[dict] = field(default_factory=list)

    def add(self, kind: str, payload: dict) -> None:
        self.events.append({"kind": kind, "payload": payload})
