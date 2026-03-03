"""Module 28 - Chaos evolution stubs."""

import random


def mutate_dna(config: dict) -> dict:
    cfg = dict(config)
    if "timeout" in cfg:
        cfg["timeout"] = max(1, int(cfg["timeout"] * random.uniform(0.8, 1.2)))
    if "retries" in cfg:
        cfg["retries"] = max(0, int(cfg["retries"] + random.choice([-1, 0, 1])))
    return cfg


def crossover(a: dict, b: dict) -> dict:
    keys = set(a) | set(b)
    return {k: (a.get(k) if random.random() < 0.5 else b.get(k)) for k in keys}


def fitness(latency_ms: float, error_rate: float) -> float:
    return max(0.0, 1000 - latency_ms * 2 - error_rate * 500)
