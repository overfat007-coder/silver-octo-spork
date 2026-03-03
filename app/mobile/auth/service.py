"""Authentication business logic."""

from hashlib import sha256

from app.mobile.auth.jwt import decode_token, encode_token
from app.mobile.auth.models import User
from app.mobile.common.store import InMemoryStore


class AuthService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def register(self, user_id: str, email: str, password: str) -> User:
        record = User(user_id=user_id, email=email, password_hash=sha256(password.encode()).hexdigest())
        self.store.users[user_id] = record.__dict__.copy()
        return record

    def login(self, email: str, password: str) -> str | None:
        pwd = sha256(password.encode()).hexdigest()
        for user in self.store.users.values():
            if user["email"] == email and user["password_hash"] == pwd:
                return encode_token({"sub": user["user_id"], "email": email})
        return None

    def verify(self, token: str) -> dict:
        return decode_token(token)
