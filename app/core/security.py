"""Security helpers: password hashing and JWT-like tokens."""

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings


ALGO = "HS256"


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return base64.urlsafe_b64encode(salt + digest).decode()


def verify_password(password: str, hashed: str) -> bool:
    raw = base64.urlsafe_b64decode(hashed.encode())
    salt, digest = raw[:16], raw[16:]
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return hmac.compare_digest(digest, check)


def _b64url(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_token(subject: str, minutes: int, token_type: str) -> str:
    header = {"alg": ALGO, "typ": "JWT"}
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    h = _b64url(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(settings.secret_key.encode(), h + b"." + p, hashlib.sha256).digest()
    s = _b64url(sig)
    return b".".join([h, p, s]).decode()


def decode_token(token: str, expected_type: str) -> dict:
    try:
        h, p, s = token.split(".")
        signing_input = f"{h}.{p}".encode()
        expected = _b64url(hmac.new(settings.secret_key.encode(), signing_input, hashlib.sha256).digest())
        if not hmac.compare_digest(expected, s.encode()):
            raise ValueError("Invalid signature")
        payload = json.loads(_b64url_decode(p).decode())
        if payload.get("type") != expected_type:
            raise ValueError("Invalid token type")
        if int(datetime.now(timezone.utc).timestamp()) > payload.get("exp", 0):
            raise ValueError("Token expired")
        return payload
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc


def create_access_token(user_id: int) -> str:
    return create_token(str(user_id), settings.access_token_minutes, "access")


def create_refresh_token(user_id: int) -> str:
    return create_token(str(user_id), settings.refresh_token_days * 24 * 60, "refresh")
