from app.mobile.common.store import InMemoryStore
from app.mobile.profile.service import ProfileService


def test_profile_upsert() -> None:
    svc = ProfileService(InMemoryStore())
    result = svc.upsert("u1", "User 1", "bio")
    assert result["display_name"] == "User 1"
    assert result["privacy"]["show_email"] is False
