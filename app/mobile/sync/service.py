"""Sync service with version increments."""

from app.mobile.common.store import InMemoryStore
from app.mobile.sync.conflict import resolve


class SyncService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def apply(self, key: str, local: dict, remote: dict) -> dict:
        merged = resolve(local, remote)
        self.store.sync_versions[key] = self.store.sync_versions.get(key, 0) + 1
        return {"version": self.store.sync_versions[key], "data": merged}
