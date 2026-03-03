"""Module 30 - Symbiosis simulation."""


def habits(tasks: list[str]) -> list[str]:
    seen = {}
    for t in tasks:
        seen[t] = seen.get(t, 0) + 1
    return [k for k, v in seen.items() if v >= 3]


def dream_digest(tasks: list[str]) -> dict:
    return {"dreamed_about": tasks[:3], "insight": "Сгруппируйте похожие задачи по контексту"}


def empathy_adjust(load: int, mood: str) -> dict:
    reduce = mood in {"sad", "tired"} or load > 8
    return {"reduce_load": reduce, "joke": "Почему таска не закрылась? Ей не хватило commit-а :)" if reduce else ""}
