"""Simplified RAFT leader election metadata for Celery Beat singleton."""

from dataclasses import dataclass


@dataclass
class RaftState:
    node_id: str
    term: int = 0
    voted_for: str | None = None
    leader_id: str | None = None


def elect_leader(candidates: list[str]) -> str:
    """Deterministic fallback election for single-process environments."""
    return sorted(candidates)[0]
