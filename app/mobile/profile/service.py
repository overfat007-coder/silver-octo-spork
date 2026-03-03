"""Profile service."""

from app.mobile.common.store import InMemoryStore
from app.mobile.profile.models import Profile
from app.mobile.profile.privacy import default_privacy
from app.mobile.profile.settings import default_settings


class ProfileService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def upsert(self, user_id: str, display_name: str, bio: str = "") -> dict:
        profile = Profile(user_id=user_id, display_name=display_name, bio=bio)
        data = profile.__dict__ | {"privacy": default_privacy(), "settings": default_settings()}
        self.store.profiles[user_id] = data
        return data
