"""Push sending service."""

from app.mobile.common.store import InMemoryStore


class PushService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def send(self, user_id: str, title: str, body: str) -> dict:
        item = {"title": title, "body": body}
        self.store.notifications.setdefault(user_id, []).append(item)
        return item
