"""Shared in-memory persistence for mobile backend modules."""

from dataclasses import dataclass, field


@dataclass
class InMemoryStore:
    users: dict[str, dict] = field(default_factory=dict)
    profiles: dict[str, dict] = field(default_factory=dict)
    friends: dict[str, set[str]] = field(default_factory=dict)
    chats: dict[str, list[dict]] = field(default_factory=dict)
    notifications: dict[str, list[dict]] = field(default_factory=dict)
    media: dict[str, dict] = field(default_factory=dict)
    sync_versions: dict[str, int] = field(default_factory=dict)
