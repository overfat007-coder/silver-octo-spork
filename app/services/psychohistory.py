"""Module 29 - Psychohistory/statistical mechanics simulation."""


def system_state(avg_priority: float, users: int, tasks: int, urgency: float) -> dict:
    p = avg_priority
    v = max(1, users)
    n = max(1, tasks)
    t = max(0.1, urgency)
    r = (p * v) / (n * t)
    if r > 2:
        phase = "solid"
    elif r < 0.5:
        phase = "gas"
    else:
        phase = "liquid"
    return {"phase": phase, "equation_ratio": r}
