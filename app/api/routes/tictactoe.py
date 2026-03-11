"""Realtime Tic-Tac-Toe 5x5 routes."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.tictactoe import manager, wait_for_event

router = APIRouter(prefix="/games/tictactoe", tags=["tictactoe"])


@router.websocket("/ws")
async def tictactoe_ws(websocket: WebSocket) -> None:
    player_id, symbol, room = await manager.matchmake(websocket)
    await websocket.send_json({"type": "joined", "player_id": player_id, "symbol": symbol})

    if room.room_id == "waiting":
        await websocket.send_json({"type": "waiting_for_opponent"})

    try:
        while True:
            if room.room_id != "waiting":
                await manager.process_timeout(room)
            event = await wait_for_event(websocket)
            if event is None:
                continue

            if event.get("type") == "move":
                row_idx = int(event.get("row", -1))
                col_idx = int(event.get("col", -1))
                try:
                    room = await manager.apply_move(player_id, row_idx, col_idx)
                    await manager.broadcast(
                        room,
                        {
                            "type": "move",
                            "board": room.board,
                            "turn": room.turn_symbol,
                            "last": {"row": row_idx, "col": col_idx, "symbol": symbol},
                            "winner": room.winner,
                            "game_over": room.game_over,
                        },
                    )
                except ValueError as exc:
                    await websocket.send_json({"type": "error", "detail": str(exc)})

            if room.room_id != "waiting" and room.game_over:
                await manager.broadcast(room, {"type": "game_over", "winner": room.winner, "board": room.board})
                return
    except WebSocketDisconnect:
        await manager.cleanup_player(player_id)
