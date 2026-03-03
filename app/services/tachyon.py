"""Module 32 - Tachyon timeline simulation."""

from datetime import datetime, timedelta


def remind_in_past(created_at: datetime, delta_hours: int = 1) -> dict:
    target = created_at - timedelta(hours=delta_hours)
    allowed = target >= created_at - timedelta(minutes=1)
    return {"target_time": target.isoformat(), "allowed": allowed}


def merge_timelines(a: list[str], b: list[str]) -> list[str]:
    return sorted(set(a + b))
