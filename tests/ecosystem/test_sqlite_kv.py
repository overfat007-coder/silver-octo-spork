from app.ecosystem.storage.sqlite_kv import SqliteKV


def test_sqlite_kv_ops() -> None:
    kv = SqliteKV(":memory:")
    kv.set("k", "v")
    assert kv.get("k") == "v"
    kv.delete("k")
    assert kv.get("k") is None
