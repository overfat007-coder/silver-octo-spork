"""Social service aggregator."""

from app.mobile.common.store import InMemoryStore
from app.mobile.social.friends import FriendService


class SocialService:
    def __init__(self, store: InMemoryStore) -> None:
        self.friends = FriendService(store)
