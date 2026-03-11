"""Module 31 - Fungal computing simulation."""


def fungal_spike_rate(substrate: str) -> float:
    return min(10.0, max(0.1, len(substrate) / 10))


def glow_intensity(task_id: int) -> int:
    return (task_id * 37) % 256


def harvest_result(task_id: int) -> dict:
    return {"task_id": task_id, "harvested": True, "edible": True}
