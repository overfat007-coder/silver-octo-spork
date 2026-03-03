"""Simple in-memory rate limiter for login endpoint."""

from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

_ATTEMPTS: dict[str, deque[datetime]] = defaultdict(deque)
_LIMIT = 5
_WINDOW = timedelta(minutes=1)


def check_login_rate_limit(ip: str) -> None:
    now = datetime.now(timezone.utc)
    attempts = _ATTEMPTS[ip]
    while attempts and now - attempts[0] > _WINDOW:
        attempts.popleft()
    if len(attempts) >= _LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts")
    attempts.append(now)
