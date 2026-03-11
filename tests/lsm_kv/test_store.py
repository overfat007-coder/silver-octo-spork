from tools.lsm_kv.store import LSMKVStore


def test_put_get_delete_persistence(tmp_path) -> None:
    store = LSMKVStore(data_dir=str(tmp_path), memtable_limit=2, compact_every=10)
    store.put("a", "1")
    store.put("b", "2")  # force flush
    assert store.get("a") == "1"
    store.delete("a")
    assert store.get("a") is None
    store.close()

    reopened = LSMKVStore(data_dir=str(tmp_path), memtable_limit=2, compact_every=10)
    assert reopened.get("a") is None
    assert reopened.get("b") == "2"
    reopened.close()


def test_manual_compaction_gc_tombstones(tmp_path) -> None:
    store = LSMKVStore(data_dir=str(tmp_path), memtable_limit=2, compact_every=10)
    store.put("k", "v1")
    store.put("x", "1")  # flush #1
    store.put("k", "v2")
    store.delete("x")  # flush #2
    store.put("z", "3")
    store.put("w", "4")  # flush #3

    assert store.stats()["sstable_count"] >= 3
    store.manual_compact()
    assert store.stats()["sstable_count"] == 1
    assert store.get("k") == "v2"
    assert store.get("x") is None
    store.close()
