"""Playful multiverse/time-travel simulation endpoints.

These are deterministic simulations for UX experimentation only.
"""



def schrodinger_task_states(task_id: int) -> list[dict]:
    return [
        {"task_id": task_id, "is_completed": True, "probability": 0.5},
        {"task_id": task_id, "is_completed": False, "probability": 0.5},
    ]


def time_travel_snapshot(user_id: int, timestamp: str) -> dict:
    return {
        "user_id": user_id,
        "requested_timestamp": timestamp,
        "status": "simulated-restore",
        "note": "full millisecond snapshots are not persisted in this prototype",
    }


def generate_precognition(user_id: int) -> list[dict]:
    return [
        {"title": "Проверить почту", "confidence": 0.58, "user_id": user_id},
        {"title": "Синхронизировать командные задачи", "confidence": 0.51, "user_id": user_id},
    ]
