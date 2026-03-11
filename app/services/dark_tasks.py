"""Module 58 - Dark matter tasks simulation."""


def dark_ratio() -> float:
    return 0.85


def lensing_offset(task_id: int) -> float:
    return (task_id % 7) * 0.13
