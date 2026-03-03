from app.mobile.common.store import InMemoryStore
from app.mobile.sync.service import SyncService


def test_sync_apply_versioning() -> None:
    svc = SyncService(InMemoryStore())
    out = svc.apply("k", {"updated_at": 2}, {"updated_at": 1})
    assert out["version"] == 1
    assert out["data"]["updated_at"] == 2
