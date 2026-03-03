"""Voice cloning stubs (embedding + synthesis)."""


def create_voice_embedding_stub(audio_bytes: bytes) -> list[float]:
    base = float(len(audio_bytes) % 100) / 100.0
    return [base, 0.42, 0.73, 0.15]


def emotion_for_priority(priority: int) -> str:
    if priority >= 5:
        return "urgent"
    if priority <= 1:
        return "calm"
    return "serious"


def synthesize_voice_stub(text: str, embedding: list[float], emotion: str) -> bytes:
    content = f"emotion={emotion};len={len(text)};embed={','.join(map(str, embedding[:2]))}"
    return content.encode()
