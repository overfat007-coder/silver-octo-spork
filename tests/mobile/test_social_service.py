from app.mobile.common.store import InMemoryStore
from app.mobile.social.service import SocialService


def test_social_add_friend() -> None:
    svc = SocialService(InMemoryStore())
    svc.friends.add_friend("a", "b")
    assert svc.friends.list_friends("a") == ["b"]
