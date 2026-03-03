"""Health endpoint."""

from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.database import SessionLocal

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    db_ok = False
    redis_ok = False

    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    finally:
        db.close()

    try:
        import redis

        client = redis.from_url(settings.redis_url)
        redis_ok = bool(client.ping())
    except Exception:
        redis_ok = False

    return {"status": "ok" if db_ok else "degraded", "db": db_ok, "redis": redis_ok}
