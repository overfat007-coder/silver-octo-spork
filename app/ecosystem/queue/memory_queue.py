"""FIFO in-memory queue backend for background jobs and local workers."""

from collections import deque


class MemoryQueue:
    """Simple FIFO queue."""

    def __init__(self) -> None:
        self._queue: deque[str] = deque()

    def put(self, item: str) -> None:
        self._queue.append(item)

    def get(self) -> str | None:
        return self._queue.popleft() if self._queue else None
