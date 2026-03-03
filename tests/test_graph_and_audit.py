from datetime import datetime

from app.services.audit_utils import chain_hash
from app.services.text_merge import merge_text


def test_merge_text_preserves_concurrent_edits() -> None:
    merged = merge_text("alpha", "beta")
    assert "alpha" in merged and "beta" in merged


def test_chain_hash_is_deterministic() -> None:
    ts = datetime(2024, 1, 1, 10, 0, 0)
    h1 = chain_hash("GENESIS", ts, 1, "title", "new")
    h2 = chain_hash("GENESIS", ts, 1, "title", "new")
    assert h1 == h2
