"""Module 57 - Multiverse of versions simulation."""


def universes_for_task(task_id: int) -> list[dict]:
    return [
        {"universe_id": f"u-{task_id}-a", "state": "done"},
        {"universe_id": f"u-{task_id}-b", "state": "todo"},
    ]


def switch_universe(task_id: int, universe_id: str) -> dict:
    return {"task_id": task_id, "active_universe": universe_id}


def merge_universes(left: str, right: str, keep: str) -> dict:
    return {"left": left, "right": right, "kept": keep, "merged": True}
