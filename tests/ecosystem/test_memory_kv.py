from app.ecosystem.storage.memory_kv import MemoryKV


def test_memory_kv_ops() -> None:
    kv = MemoryKV()
    kv.set("k", "v")
    assert kv.get("k") == "v"
    kv.delete("k")
    assert kv.get("k") is None
