"""Module 34 - Task reincarnation and karma simulation."""


def karmic_weight(complexity: int, importance: int) -> int:
    return complexity * importance


def reincarnate(title: str, generation: int) -> dict:
    if generation >= 7:
        return {"title": title, "nirvana": True, "new_title": title}
    return {"title": title, "nirvana": False, "new_title": f"{title} (перерождение {generation+1})"}
