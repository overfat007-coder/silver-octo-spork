"""Module 48 - Meta-task recursion simulation."""

import time


def level_tasks(n: int) -> dict:
    return {"level": n, "tasks": [f"meta-{n}-control", f"meta-{n}-observe"]}


def create_next_level(n: int) -> dict:
    return {"created_level": n + 1, "seed": f"meta-{n+1}"}


def infinite_attempt(timeout_s: int = 10) -> dict:
    started = time.time()
    while time.time() - started < min(timeout_s, 1):
        pass
    return {"status": "timeout", "message": "Вы достигли дна кроличьей норы"}
