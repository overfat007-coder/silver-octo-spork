"""Federated learning simulation with DP + secure aggregation stubs."""

import math
import random


def laplace_noise(scale: float) -> float:
    u = random.random() - 0.5
    return -scale * math.copysign(1.0, u) * math.log(1 - 2 * abs(u))


def local_train_stub(samples: list[dict]) -> dict:
    grad = sum(float(s.get("minutes", 0)) for s in samples) / max(1, len(samples))
    return {"dw": grad / 100.0, "db": 0.01}


def apply_dp(gradients: dict, epsilon: float = 0.1) -> dict:
    scale = 1.0 / max(epsilon, 1e-6)
    return {k: v + laplace_noise(scale) for k, v in gradients.items()}


def secure_aggregate_stub(encrypted_updates: list[dict]) -> dict:
    summed = {"dw": 0.0, "db": 0.0}
    for upd in encrypted_updates:
        summed["dw"] += float(upd.get("dw", 0))
        summed["db"] += float(upd.get("db", 0))
    return summed
