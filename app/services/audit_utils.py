"""Pure functions for audit hashing."""

import hashlib
import os
from datetime import datetime


def chain_hash(previous_hash: str, timestamp: datetime, user_id: int, field_changed: str, new_value: str) -> str:
    salt = os.getenv("AUDIT_SALT", "smartflow-salt")
    raw = f"{previous_hash}{timestamp.isoformat()}{user_id}{field_changed}{new_value}{salt}"
    return hashlib.sha256(raw.encode()).hexdigest()
