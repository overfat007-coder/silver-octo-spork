"""FastAPI app for subscription microservice."""

from fastapi import FastAPI

from .cache import SubscriptionCache
from .events import publish_subscription_event

app = FastAPI(title="Subscription Service", version="0.1.0")
cache = SubscriptionCache()
SUBSCRIPTIONS: dict[str, bool] = {"u1": True, "u2": False, "u3": True}


@app.get("/health")
def health() -> dict:
    return {"service": "subscription", "status": "ok"}


@app.get("/subscriptions/{user_id}/active")
def subscription_status(user_id: str) -> dict:
    cached = cache.get(user_id)
    if cached is not None:
        return {"user_id": user_id, "active": cached, "source": "redis"}

    active = SUBSCRIPTIONS.get(user_id, False)
    cache.set(user_id, active)
    return {"user_id": user_id, "active": active, "source": "memory"}


@app.post("/subscriptions/{user_id}")
def set_subscription(user_id: str, payload: dict) -> dict:
    active = bool(payload.get("active", False))
    SUBSCRIPTIONS[user_id] = active
    cache.set(user_id, active)
    published = publish_subscription_event(user_id, active)
    return {"user_id": user_id, "active": active, "event_published": published}
