"""Module 18 - Voice cloning APIs."""

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User
from app.services.voice_clone import create_voice_embedding_stub, emotion_for_priority, synthesize_voice_stub

router = APIRouter(prefix="/voice", tags=["voice-clone"])


@router.post("/clone/{user_id}")
def clone_voice(user_id: int, payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    embedding = create_voice_embedding_stub(str(payload.get("audio_b64", "")).encode())
    return {"user_id": user_id, "requested_by": current_user.id, "embedding": embedding}


@router.get("/say/{user_id}/{task_id}")
def say_voice(user_id: int, task_id: int, priority: int = 3, current_user: User = Depends(get_current_user)) -> dict:
    emotion = emotion_for_priority(priority)
    audio = synthesize_voice_stub(f"Task {task_id} notification", [0.1, 0.2], emotion)
    return {"user_id": user_id, "task_id": task_id, "emotion": emotion, "audio_preview": audio.decode()[:64], "requested_by": current_user.id}


@router.get("/emotions/list")
def list_emotions() -> dict:
    return {"emotions": ["calm", "urgent", "happy", "serious"]}
