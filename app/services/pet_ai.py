"""Module 33 - Pet behavior interpretation stubs."""


def behavior_to_task(behavior: str) -> str:
    mapping = {
        "empty_bowl": "Купить корм",
        "scratching_door": "Выпустить погулять",
        "looking_at_leash": "Пойти на прогулку",
    }
    return mapping.get(behavior, "Поиграть с питомцем")


def pet_mood_index(events: list[str]) -> int:
    return max(0, min(100, 60 + events.count("play") * 5 - events.count("idle") * 7))
