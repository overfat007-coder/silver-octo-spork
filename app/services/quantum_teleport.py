"""Module 23 - Quantum task teleportation simulation."""

import random
import time


def create_epr_pair(server_a: str, server_b: str) -> dict:
    return {"server_a": server_a, "server_b": server_b, "pair_id": f"epr-{int(time.time()*1000)}"}


def encode_task_state(task: dict) -> str:
    return f"{task.get('title','')}|{task.get('description','')}|{task.get('priority',3)}"


def bennett_teleport_sim(task_state: str, decoherence: float = 0.03) -> dict:
    m1, m2 = random.randint(0, 1), random.randint(0, 1)
    failed = random.random() < decoherence
    restored = task_state if not failed else ""
    return {"bell_bits": [m1, m2], "success": not failed, "restored_state": restored}


def degrade_priority(priority: int, wait_seconds: int, t1: int = 3600) -> int:
    decay = wait_seconds // max(t1, 1)
    return max(1, priority - decay)
