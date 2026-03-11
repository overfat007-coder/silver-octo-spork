"""Cross-module event handlers.

Flow example:
- task.created -> quantum.secure
- task.created -> gnn.recommend_assignee
- task.created -> voice.say
- burnout.detected -> video.context_check -> voice.say
- task.completed -> federated.round -> gnn.refresh
"""

from app.events.schemas import Event


def quantum_secure_task(event: Event) -> None:
    event.payload.setdefault("security", {})["channel"] = "pq-or-quantum-sim"


def gnn_recommend_assignee(event: Event) -> None:
    event.payload.setdefault("recommendation", {})["assignee_id"] = event.payload.get("user_id")


def voice_notify_creation(event: Event) -> None:
    event.payload.setdefault("voice", {})["message"] = "Задача создана"


def video_context_check(event: Event) -> None:
    event.payload.setdefault("video", {})["status"] = "checked"


def voice_soft_rest(event: Event) -> None:
    event.payload.setdefault("voice", {})["message"] = "Рекомендуем отдохнуть"


def federated_round(event: Event) -> None:
    event.payload.setdefault("federated", {})["round_submitted"] = True


def gnn_refresh(event: Event) -> None:
    event.payload.setdefault("gnn", {})["refreshed"] = True
