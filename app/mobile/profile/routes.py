"""Profile routes."""

from fastapi import APIRouter

from app.mobile.common.store import InMemoryStore
from app.mobile.profile.service import ProfileService

router = APIRouter(prefix="/mobile/profiles", tags=["mobile-profile"])
_store = InMemoryStore()
_service = ProfileService(_store)


@router.put("/{user_id}")
def put_profile(user_id: str, payload: dict) -> dict:
    return _service.upsert(user_id, payload.get("display_name", user_id), payload.get("bio", ""))
