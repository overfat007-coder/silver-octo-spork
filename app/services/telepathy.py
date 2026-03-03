"""Module 40 - Telepathic task network simulation."""


def thought_embedding(task_id: int) -> list[float]:
    return [((task_id * (i + 7)) % 101) / 101 for i in range(32)]


def decode_thought(embedding: list[float]) -> str:
    strength = sum(embedding) / max(1, len(embedding))
    if strength > 0.6:
        return "Я думаю, что меня должны выполнить сегодня"
    return "Я в медитативном режиме"


def censor_thought(text: str) -> dict:
    banned = ["удали все", "саботаж", "хаос"]
    blocked = any(b in text.lower() for b in banned)
    return {"blocked": blocked, "text": "[REDACTED]" if blocked else text}
