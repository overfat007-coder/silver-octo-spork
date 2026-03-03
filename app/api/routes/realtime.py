"""WebSocket realtime collaboration endpoints."""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database import SessionLocal
from app.models.task import Task
from app.models.user import User
from app.services.history import add_history
from app.services.realtime import merge_text, room_manager

router = APIRouter(tags=["realtime"])


@router.websocket("/ws/tasks/{task_id}")
async def task_socket(websocket: WebSocket, task_id: int, token: str):
    payload = decode_token(token, "access")
    user_id = int(payload["sub"])
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    await room_manager.connect(task_id, websocket)

    try:
        await room_manager.broadcast(task_id, {"type": "presence", "user": user.username if user else str(user_id)})
        while True:
            data = await websocket.receive_json()
            event = data.get("type")
            if event == "typing":
                await room_manager.broadcast(task_id, {"type": "typing", "user": user.username if user else str(user_id)})
            elif event == "cursor":
                await room_manager.broadcast(task_id, {"type": "cursor", "user": user.username if user else str(user_id), "position": data.get("position")})
            elif event == "update":
                task = db.query(Task).filter(Task.id == task_id).first()
                if not task:
                    continue
                field = data.get("field", "description")
                new_val = str(data.get("value", ""))
                old_val = str(getattr(task, field, ""))
                merged = merge_text(old_val, new_val) if field in {"title", "description"} else new_val
                setattr(task, field, merged)
                db.commit()
                add_history(db, task_id, user_id, field, old_val, merged)
                await room_manager.broadcast(task_id, {"type": "update", "field": field, "value": merged, "user": user.username if user else str(user_id)})
    except WebSocketDisconnect:
        room_manager.disconnect(task_id, websocket)
    finally:
        db.close()
