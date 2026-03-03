from app.events.bus import EventBus


def test_at_least_once_and_dlq() -> None:
    bus = EventBus()
    seen = {"ok": 0}

    def handler(event):
        seen["ok"] += 1

    bus.subscribe("x", handler)
    bus.publish("x", {"a": 1})
    processed = bus.consume_once()
    assert processed == 1
    assert seen["ok"] == 1

    bus.publish("no-handler", {"a": 1})
    bus.consume_once()
    assert len(bus.dead_letter_queue) == 1
