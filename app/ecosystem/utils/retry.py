"""Retry utility for transient operation failures."""

import time
from collections.abc import Callable


def retry(operation: Callable[[], object], attempts: int = 3, delay_s: float = 0.01) -> object:
    """Run operation with fixed-delay retries."""
    last_error: Exception | None = None
    for _ in range(max(1, attempts)):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(delay_s)
    assert last_error is not None
    raise last_error
