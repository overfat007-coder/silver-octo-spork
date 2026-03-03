"""Voice intent and sentiment stubs."""


def parse_voice_intent(text: str) -> dict:
    t = text.lower()
    if "создай" in t and "задач" in t:
        return {"intent": "create_task", "entities": {"title": text}}
    if "покажи" in t and "задач" in t:
        return {"intent": "list_tasks", "entities": {}}
    if "выполн" in t and any(ch.isdigit() for ch in t):
        digits = "".join(ch for ch in t if ch.isdigit())
        return {"intent": "complete_task", "entities": {"task_id": int(digits)}}
    return {"intent": "unknown", "entities": {}}


def sentiment_from_audio_stub(signal: list[float] | list[int]) -> str:
    if not signal:
        return "neutral"
    avg = sum(float(x) for x in signal) / len(signal)
    if avg > 0.7:
        return "stressed"
    if avg < 0.3:
        return "calm"
    return "focused"
