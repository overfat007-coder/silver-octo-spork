"""Minimal circuit breaker implementation."""

import time
from collections.abc import Callable
from dataclasses import dataclass


class CircuitOpenError(RuntimeError):
    """Raised when a protected call is blocked by open circuit."""


@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    recovery_timeout_s: float = 5.0

    def __post_init__(self) -> None:
        self._failures = 0
        self._opened_at: float | None = None

    @property
    def state(self) -> str:
        if self._opened_at is None:
            return "closed"
        if time.time() - self._opened_at >= self.recovery_timeout_s:
            return "half-open"
        return "open"

    def call(self, fn: Callable[[], bool]) -> bool:
        if self.state == "open":
            raise CircuitOpenError("circuit is open")

        try:
            result = fn()
        except Exception as exc:  # noqa: BLE001
            self._failures += 1
            if self._failures >= self.failure_threshold:
                self._opened_at = time.time()
            raise exc

        self._failures = 0
        self._opened_at = None
        return result
