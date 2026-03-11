"""Client for subscription service checks."""

import os

import requests

from .circuit import CircuitBreaker

SUBSCRIPTION_URL = os.getenv("SUBSCRIPTION_SERVICE_URL", "http://subscription-service:8002")
breaker = CircuitBreaker(failure_threshold=2, recovery_timeout_s=10)


def is_active_subscription(user_id: str) -> bool:
    def _call() -> bool:
        r = requests.get(f"{SUBSCRIPTION_URL}/subscriptions/{user_id}/active", timeout=1.5)
        r.raise_for_status()
        return bool(r.json().get("active", False))

    return breaker.call(_call)
