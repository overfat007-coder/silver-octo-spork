"""Chat routes."""

from fastapi import APIRouter

from app.mobile.chat.service import ChatService
from app.mobile.common.store import InMemoryStore

router = APIRouter(prefix="/mobile/chat", tags=["mobile-chat"])
_store = InMemoryStore()
_service = ChatService(_store)


@router.post("/{chat_id}/messages")
def send_message(chat_id: str, payload: dict) -> dict:
    return _service.messages.send(chat_id, payload["sender_id"], payload["text"])
