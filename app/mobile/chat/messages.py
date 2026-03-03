"""Message service."""

from app.mobile.common.store import InMemoryStore


class MessageService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def send(self, chat_id: str, sender_id: str, text: str) -> dict:
        message = {"chat_id": chat_id, "sender_id": sender_id, "text": text}
        self.store.chats.setdefault(chat_id, []).append(message)
        return message

    def history(self, chat_id: str) -> list[dict]:
        return list(self.store.chats.get(chat_id, []))
