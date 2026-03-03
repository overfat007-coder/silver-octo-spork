"""Conflict resolution strategies for offline sync."""

def resolve(local: dict, remote: dict) -> dict:
    return local if local.get("updated_at", 0) >= remote.get("updated_at", 0) else remote
