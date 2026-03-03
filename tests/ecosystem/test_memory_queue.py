from app.ecosystem.queue.memory_queue import MemoryQueue


def test_queue_fifo() -> None:
    q = MemoryQueue()
    q.put("a")
    q.put("b")
    assert q.get() == "a"
    assert q.get() == "b"
    assert q.get() is None
