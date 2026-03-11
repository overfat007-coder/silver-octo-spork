from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from tools.lsm_kv.sstable import SSTable, SSTableMeta, TOMBSTONE


class LSMKVStore:
    def __init__(
        self,
        data_dir: str,
        memtable_limit: int = 100,
        compact_every: float = 2.0,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.wal_path = self.data_dir / "wal.log"

        self.memtable_limit = max(2, memtable_limit)
        self.memtable: dict[str, str] = {}
        self.lock = threading.RLock()

        self.sstables: list[SSTableMeta] = []
        self._seq = self._find_latest_seq() + 1

        self._load_existing_sstables()
        self._replay_wal()

        self._stop = threading.Event()
        self._compact_every = max(0.5, compact_every)
        self._compactor = threading.Thread(target=self._compact_loop, daemon=True)
        self._compactor.start()

    def put(self, key: str, value: str) -> None:
        with self.lock:
            self.memtable[key] = value
            self._append_wal({"op": "put", "key": key, "value": value})
            if len(self.memtable) >= self.memtable_limit:
                self._flush_memtable()

    def get(self, key: str) -> str | None:
        with self.lock:
            if key in self.memtable:
                val = self.memtable[key]
                return None if val == TOMBSTONE else val

            for meta in reversed(self.sstables):
                value = SSTable.get(meta, key)
                if value is None:
                    continue
                return None if value == TOMBSTONE else value
        return None

    def delete(self, key: str) -> None:
        with self.lock:
            self.memtable[key] = TOMBSTONE
            self._append_wal({"op": "delete", "key": key})
            if len(self.memtable) >= self.memtable_limit:
                self._flush_memtable()

    def close(self) -> None:
        self._stop.set()
        self._compactor.join(timeout=2)
        with self.lock:
            if self.memtable:
                self._flush_memtable()

    def _append_wal(self, rec: dict) -> None:
        with self.wal_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def _flush_memtable(self) -> None:
        if not self.memtable:
            return
        sstable_path = self.data_dir / f"sst_{self._seq:06d}.sst"
        self._seq += 1
        meta = SSTable.write(sstable_path, self.memtable)
        self.sstables.append(meta)
        self.memtable = {}
        self.wal_path.write_text("", encoding="utf-8")

    def _find_latest_seq(self) -> int:
        highest = 0
        for p in self.data_dir.glob("sst_*.sst"):
            try:
                highest = max(highest, int(p.stem.split("_")[1]))
            except (IndexError, ValueError):
                continue
        return highest

    def _load_existing_sstables(self) -> None:
        tables = sorted(self.data_dir.glob("sst_*.sst"))
        self.sstables = [SSTable.load(p) for p in tables]

    def _replay_wal(self) -> None:
        if not self.wal_path.exists():
            return
        with self.wal_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                key = rec["key"]
                if rec["op"] == "put":
                    self.memtable[key] = rec["value"]
                elif rec["op"] == "delete":
                    self.memtable[key] = TOMBSTONE

    def _compact_loop(self) -> None:
        while not self._stop.wait(self._compact_every):
            with self.lock:
                if len(self.sstables) < 2:
                    continue
                self._compact_once()

    def _compact_once(self) -> None:
        merged: dict[str, str] = {}
        for meta in self.sstables:
            merged.update(SSTable.iter_records(meta))

        merged = {k: v for k, v in merged.items() if v != TOMBSTONE}

        compacted_path = self.data_dir / f"sst_{self._seq:06d}.sst"
        self._seq += 1
        compacted = SSTable.write(compacted_path, merged)

        old_tables = list(self.sstables)
        self.sstables = [compacted]
        for meta in old_tables:
            try:
                meta.path.unlink(missing_ok=True)
                meta.path.with_suffix(meta.path.suffix + ".meta").unlink(missing_ok=True)
            except OSError:
                pass

    def manual_compact(self) -> None:
        with self.lock:
            if len(self.sstables) >= 2:
                self._compact_once()

    def stats(self) -> dict:
        with self.lock:
            return {
                "memtable_size": len(self.memtable),
                "sstable_count": len(self.sstables),
                "wal_exists": self.wal_path.exists(),
            }
