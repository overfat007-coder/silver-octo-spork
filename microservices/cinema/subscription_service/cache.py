"""Redis-backed cache for subscription status."""

import os

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/1")


class SubscriptionCache:
    def __init__(self) -> None:
        self._fallback: dict[str, bool] = {}
        self._client = redis.from_url(REDIS_URL, decode_responses=True)

    def get(self, user_id: str) -> bool | None:
        try:
            value = self._client.get(f"subscription:{user_id}")
        except redis.RedisError:
            return self._fallback.get(user_id)
        if value is None:
            return None
        return value == "1"

    def set(self, user_id: str, active: bool, ttl_s: int = 300) -> None:
        try:
            self._client.setex(f"subscription:{user_id}", ttl_s, "1" if active else "0")
        except redis.RedisError:
            self._fallback[user_id] = active
