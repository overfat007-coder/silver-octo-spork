from app.mobile.common.store import InMemoryStore
from app.mobile.push.service import PushService


def test_push_send() -> None:
    svc = PushService(InMemoryStore())
    out = svc.send("u1", "t", "b")
    assert out["title"] == "t"
