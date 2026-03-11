from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from tools.lsm_kv.bloom import BloomFilter

TOMBSTONE = "__LSM_TOMBSTONE__"


@dataclass
class SSTableMeta:
    path: Path
    index: dict[str, int]
    bloom: BloomFilter


class SSTable:
    @staticmethod
    def write(path: Path, records: dict[str, str]) -> SSTableMeta:
        path.parent.mkdir(parents=True, exist_ok=True)
        bloom = BloomFilter.for_capacity(max(1, len(records)))
        sorted_items = sorted(records.items(), key=lambda kv: kv[0])

        index: dict[str, int] = {}
        with path.open("w", encoding="utf-8") as f:
            for key, value in sorted_items:
                offset = f.tell()
                row = {"key": key, "value": value}
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                index[key] = offset
                bloom.add(key)

        meta = {
            "index": index,
            "bloom": bloom.to_dict(),
        }
        meta_path = path.with_suffix(path.suffix + ".meta")
        meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        return SSTableMeta(path=path, index=index, bloom=bloom)

    @staticmethod
    def load(path: Path) -> SSTableMeta:
        meta_path = path.with_suffix(path.suffix + ".meta")
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return SSTableMeta(
            path=path,
            index={k: int(v) for k, v in data["index"].items()},
            bloom=BloomFilter.from_dict(data["bloom"]),
        )

    @staticmethod
    def get(meta: SSTableMeta, key: str) -> str | None:
        if not meta.bloom.might_contain(key):
            return None
        offset = meta.index.get(key)
        if offset is None:
            return None
        with meta.path.open("r", encoding="utf-8") as f:
            f.seek(offset)
            line = f.readline()
        row = json.loads(line)
        return row["value"]

    @staticmethod
    def iter_records(meta: SSTableMeta) -> dict[str, str]:
        out: dict[str, str] = {}
        with meta.path.open("r", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                out[row["key"]] = row["value"]
        return out
