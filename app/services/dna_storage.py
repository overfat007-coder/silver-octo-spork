"""Module 25 - DNA archive simulation."""

import json

MAP = {"00": "A", "01": "T", "10": "G", "11": "C"}
RMAP = {v: k for k, v in MAP.items()}


def json_to_dna(payload: dict) -> str:
    bits = "".join(f"{b:08b}" for b in json.dumps(payload, ensure_ascii=False).encode())
    if len(bits) % 2:
        bits += "0"
    return "".join(MAP[bits[i:i+2]] for i in range(0, len(bits), 2))


def dna_to_json(seq: str) -> dict:
    bits = "".join(RMAP.get(ch, "00") for ch in seq)
    by = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits) - 7, 8))
    try:
        return json.loads(by.decode(errors="ignore") or "{}")
    except Exception:
        return {}


class DNASynthesizer:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    def write(self, key: str, dna: str) -> dict:
        self.storage[key] = dna
        return {"key": key, "nucleotides": len(dna), "cost_usd": round(len(dna) * 0.001, 3)}

    def read(self, key: str) -> str:
        return self.storage.get(key, "")
