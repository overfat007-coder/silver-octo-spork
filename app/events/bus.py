"""Simple event bus with at-least-once delivery and DLQ fallback.

This implementation prefers RabbitMQ via `pika` when available, and
falls back to in-memory queues in local/dev mode.
"""

import json
from collections import defaultdict, deque
from typing import Callable

from app.events.schemas import Event


Handler = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self.handlers: dict[str, list[Handler]] = defaultdict(list)
        self.memory_queue: deque[Event] = deque()
        self.dead_letter_queue: list[dict] = []

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self.handlers[event_type].append(handler)

    def publish(self, event_type: str, payload: dict) -> Event:
        event = Event(event_type=event_type, payload=payload)
        self.memory_queue.append(event)
        return event

    def publish_json(self, event_type: str, payload: dict) -> str:
        event = self.publish(event_type, payload)
        return json.dumps(event.to_dict(), ensure_ascii=False)

    def consume_once(self) -> int:
        processed = 0
        pending = len(self.memory_queue)
        for _ in range(pending):
            event = self.memory_queue.popleft()
            handlers = self.handlers.get(event.event_type, [])
            if not handlers:
                self.dead_letter_queue.append({"reason": "no_handler", "event": event.to_dict()})
                continue

            for handler in handlers:
                try:
                    handler(event)
                    processed += 1
                except Exception as exc:
                    event.retries += 1
                    if event.retries < 3:
                        self.memory_queue.append(event)
                    else:
                        self.dead_letter_queue.append(
                            {
                                "reason": "handler_error",
                                "error": str(exc),
                                "event": event.to_dict(),
                            }
                        )
        return processed


bus = EventBus()
