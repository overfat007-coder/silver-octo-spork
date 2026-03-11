"""In-memory real-time collaboration manager with lightweight OT merge."""

from collections import defaultdict
from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class ClientEvent:
    user_id: int
    username: str
    cursor: int | None = None


class TaskRoomManager:
    def __init__(self) -> None:
        self.rooms: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, task_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self.rooms[task_id].append(ws)

    def disconnect(self, task_id: int, ws: WebSocket) -> None:
        self.rooms[task_id] = [c for c in self.rooms[task_id] if c is not ws]

    async def broadcast(self, task_id: int, payload: dict) -> None:
        for client in list(self.rooms[task_id]):
            await client.send_json(payload)


from app.services.text_merge import merge_text

room_manager = TaskRoomManager()
