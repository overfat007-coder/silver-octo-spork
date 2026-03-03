"""Module 42 - Akashic records simulation."""


def future_tasks() -> list[dict]:
    return [
        {"title": "Запланировать отдых", "confidence": 0.73},
        {"title": "Закрыть старые долги", "confidence": 0.69},
    ]


def past_lives(task_id: int) -> list[dict]:
    return [
        {"task_id": task_id, "era": "2026", "name": "Купить молоко"},
        {"task_id": task_id, "era": "до Big Bang", "name": "Да будет свет"},
    ]


def archetypes() -> list[str]:
    return ["Купить молоко", "Позвонить маме", "Разобрать почту"]


def enlightenment_result() -> dict:
    return {"enlightened": True, "maya_dissolved": True}
