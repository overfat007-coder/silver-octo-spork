"""Social routes."""

from fastapi import APIRouter

from app.mobile.common.store import InMemoryStore
from app.mobile.social.service import SocialService

router = APIRouter(prefix="/mobile/social", tags=["mobile-social"])
_store = InMemoryStore()
_service = SocialService(_store)


@router.post("/friends/{left}/{right}")
def add_friend(left: str, right: str) -> dict:
    _service.friends.add_friend(left, right)
    return {"ok": True}
