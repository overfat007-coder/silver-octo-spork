from app.mobile.auth.service import AuthService
from app.mobile.common.store import InMemoryStore


def test_auth_register_and_login() -> None:
    svc = AuthService(InMemoryStore())
    svc.register("u1", "a@b.c", "p")
    token = svc.login("a@b.c", "p")
    assert token is not None
    assert svc.verify(token)["sub"] == "u1"
