"""Push routes."""

from fastapi import APIRouter

from app.mobile.common.store import InMemoryStore
from app.mobile.push.service import PushService

router = APIRouter(prefix="/mobile/push", tags=["mobile-push"])
_store = InMemoryStore()
_service = PushService(_store)


@router.post("/send/{user_id}")
def send_push(user_id: str, payload: dict) -> dict:
    return _service.send(user_id, payload["title"], payload["body"])
