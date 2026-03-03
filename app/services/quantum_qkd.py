"""BB84 simulation stubs."""

import random


def bb84_simulate(n: int = 64, eve: bool = False) -> dict:
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(["+", "x"]) for _ in range(n)]
    bob_bases = [random.choice(["+", "x"]) for _ in range(n)]

    measured = []
    for i in range(n):
        bit = alice_bits[i]
        if eve and random.random() < 0.5:
            bit = random.randint(0, 1)
        measured.append(bit if alice_bases[i] == bob_bases[i] else random.randint(0, 1))

    sift_idx = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    key_a = [alice_bits[i] for i in sift_idx]
    key_b = [measured[i] for i in sift_idx]
    errors = sum(1 for a, b in zip(key_a, key_b) if a != b)
    qber = (errors / max(1, len(key_a))) * 100
    return {
        "qber": qber,
        "intercept_detected": qber > 11,
        "shared_key_preview": "".join(map(str, key_b[:16])),
        "sifted_len": len(key_b),
    }
