from __future__ import annotations

import hashlib
import math


class BloomFilter:
    def __init__(self, size_bits: int = 2048, hash_count: int = 4, bits: int = 0) -> None:
        self.size_bits = max(128, size_bits)
        self.hash_count = max(2, hash_count)
        self.bits = bits

    @classmethod
    def for_capacity(cls, n_items: int, error_rate: float = 0.01) -> "BloomFilter":
        n_items = max(1, n_items)
        error_rate = min(max(error_rate, 1e-6), 0.5)
        m = int(-(n_items * math.log(error_rate)) / (math.log(2) ** 2))
        k = max(2, int((m / n_items) * math.log(2)))
        return cls(size_bits=max(128, m), hash_count=k)

    def _hash_positions(self, key: str) -> list[int]:
        positions = []
        for i in range(self.hash_count):
            h = hashlib.sha256(f"{i}:{key}".encode("utf-8")).digest()
            positions.append(int.from_bytes(h, "big") % self.size_bits)
        return positions

    def add(self, key: str) -> None:
        for p in self._hash_positions(key):
            self.bits |= 1 << p

    def might_contain(self, key: str) -> bool:
        for p in self._hash_positions(key):
            if ((self.bits >> p) & 1) == 0:
                return False
        return True

    def to_dict(self) -> dict:
        return {"size_bits": self.size_bits, "hash_count": self.hash_count, "bits": str(self.bits)}

    @classmethod
    def from_dict(cls, data: dict) -> "BloomFilter":
        return cls(size_bits=int(data["size_bits"]), hash_count=int(data["hash_count"]), bits=int(data["bits"]))
