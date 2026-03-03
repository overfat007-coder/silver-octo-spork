"""Video analytics stubs."""


def aggregate_activity(events: list[str]) -> dict:
    counts: dict[str, int] = {}
    for e in events:
        counts[e] = counts.get(e, 0) + 1
    return counts


def suggest_tasks_from_objects(objects: list[str]) -> list[str]:
    suggestions = []
    if "documents" in objects:
        suggestions.append("Разобрать документы")
    if "empty_cup" in objects:
        suggestions.append("Заварить чай")
    return suggestions


def fatigue_alert(blinks_per_min: int, posture_bad: bool) -> bool:
    return blinks_per_min > 30 or posture_bad
