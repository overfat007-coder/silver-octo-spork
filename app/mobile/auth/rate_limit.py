"""Rate limit helpers for login attempts."""


class LoginRateLimiter:
    def __init__(self, attempts: int = 5) -> None:
        self.attempts = attempts
        self._counter: dict[str, int] = {}

    def hit(self, key: str) -> bool:
        self._counter[key] = self._counter.get(key, 0) + 1
        return self._counter[key] <= self.attempts
