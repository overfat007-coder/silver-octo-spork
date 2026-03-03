from app.mobile.chat.service import ChatService
from app.mobile.common.store import InMemoryStore


def test_chat_send_and_history() -> None:
    svc = ChatService(InMemoryStore())
    svc.messages.send("c1", "u1", "hello")
    assert svc.messages.history("c1")[0]["text"] == "hello"
