"""Friend graph service."""

from app.mobile.common.store import InMemoryStore


class FriendService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def add_friend(self, left: str, right: str) -> None:
        self.store.friends.setdefault(left, set()).add(right)
        self.store.friends.setdefault(right, set()).add(left)

    def list_friends(self, user_id: str) -> list[str]:
        return sorted(self.store.friends.get(user_id, set()))
