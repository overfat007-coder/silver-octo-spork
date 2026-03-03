"""Core protocols for ecosystem components."""

from typing import Protocol


class Serializer(Protocol):
    """Encode/decode Python values to a transport format."""

    name: str

    def dumps(self, value: object) -> str: ...

    def loads(self, payload: str) -> object: ...


class KeyValueStore(Protocol):
    """Simple key-value storage contract."""

    def get(self, key: str) -> str | None: ...

    def set(self, key: str, value: str) -> None: ...

    def delete(self, key: str) -> None: ...


class QueueBackend(Protocol):
    """Queue contract for async or background processing."""

    def put(self, item: str) -> None: ...

    def get(self) -> str | None: ...
