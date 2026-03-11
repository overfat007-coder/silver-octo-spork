"""Event subscriptions registry."""

from app.events.bus import bus
from app.events.handlers import (
    federated_round,
    gnn_recommend_assignee,
    gnn_refresh,
    quantum_secure_task,
    video_context_check,
    voice_notify_creation,
    voice_soft_rest,
)


def register_default_handlers() -> None:
    bus.subscribe("task.created", quantum_secure_task)
    bus.subscribe("task.created", gnn_recommend_assignee)
    bus.subscribe("task.created", voice_notify_creation)

    bus.subscribe("burnout.detected", video_context_check)
    bus.subscribe("burnout.detected", voice_soft_rest)

    bus.subscribe("task.completed", federated_round)
    bus.subscribe("task.completed", gnn_refresh)
