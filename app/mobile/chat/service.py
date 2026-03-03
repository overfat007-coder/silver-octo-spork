"""Chat service."""

from app.mobile.chat.messages import MessageService
from app.mobile.common.store import InMemoryStore


class ChatService:
    def __init__(self, store: InMemoryStore) -> None:
        self.messages = MessageService(store)
