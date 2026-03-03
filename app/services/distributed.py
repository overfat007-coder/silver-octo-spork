"""Distributed systems placeholders: sharding, 2PC and resharding plans."""

import json
from pathlib import Path


def load_shards(path: str = "shards.json") -> dict[str, str]:
    p = Path(path)
    if not p.exists():
        return {"shard_0": "sqlite:///./smartflow.db"}
    return json.loads(p.read_text())


def pick_shard(user_id: int, shards: dict[str, str]) -> str:
    keys = sorted(shards.keys())
    return keys[user_id % len(keys)]


def two_phase_commit_create_task(prepared: list[callable], committers: list[callable], rollbackers: list[callable]) -> bool:
    """Minimal 2PC coordinator skeleton."""
    try:
        for prepare in prepared:
            prepare()
        for commit in committers:
            commit()
        return True
    except Exception:
        for rollback in rollbackers:
            rollback()
        return False


def reshard_plan(users: list[int], old_shard: str, new_shard: str, threshold: int = 1000) -> dict:
    moving = users[: max(1, len(users) // 2)] if len(users) > threshold else []
    return {"from": old_shard, "to": new_shard, "users": moving, "zero_downtime": True}
