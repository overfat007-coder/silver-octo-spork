"""BCI connection and signal interpretation stubs."""


def connect_bci_device(user_id: int, device: str) -> dict:
    return {"user_id": user_id, "device": device, "status": "connected-stub"}


def detect_p300_stub(matrix_events: list[dict]) -> int | None:
    if not matrix_events:
        return None
    best = max(matrix_events, key=lambda e: float(e.get("score", 0)))
    return int(best.get("task_id", 0)) if best.get("task_id") is not None else None


def detect_ssvep_stub(fft_peaks: list[float] | list[int]) -> str:
    if not fft_peaks:
        return "none"
    dominant = max(float(x) for x in fft_peaks)
    if dominant >= 20:
        return "change_priority"
    if dominant >= 15:
        return "delete"
    if dominant >= 10:
        return "create"
    return "idle"
