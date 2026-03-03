"""Module 46 - Omniverse/meta-reality simulation."""


def nature_of_reality() -> str:
    return "Ты спишь. Проснись."


def simulation_probability() -> float:
    return 0.999999


def creator_view(is_root: bool) -> dict:
    if not is_root:
        return {"visible": False, "message": "Требуются root-права"}
    return {"visible": True, "message": "Наблюдатель замечен на границе симуляции"}
