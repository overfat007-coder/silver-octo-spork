"""Module 27 - Emotion and qualia simulation."""

EMOTIONS = ["joy", "sadness", "anger", "fear", "trust", "disgust", "surprise", "anticipation"]


def emotion_from_task(priority: int, overdue: bool) -> str:
    if overdue:
        return "sadness"
    if priority >= 5:
        return "anger"
    if priority <= 1:
        return "trust"
    return "anticipation"


def qualia_vector(seed: int) -> list[float]:
    return [((seed * (i + 3)) % 97) / 97 for i in range(16)]  # compacted preview


def feeling_today() -> dict:
    return {"emotion": "curious", "stability": 0.74}


def convince(action: str, argument: str) -> dict:
    accepted = len(argument) > 10 and "безопас" in argument.lower()
    return {"action": action, "accepted": accepted}
