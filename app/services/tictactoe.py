"""Realtime 5x5 tic-tac-toe matchmaking and game engine."""

from __future__ import annotations

import asyncio
import sqlite3
import time
import uuid
from dataclasses import dataclass, field

from typing import Any

WIN_LENGTH = 5
BOARD_SIZE = 5
TURN_TIMEOUT_SECONDS = 30


@dataclass
class PlayerState:
    player_id: str
    symbol: str
    websocket: Any


@dataclass
class RoomState:
    room_id: str
    players: list[PlayerState]
    board: list[list[str]] = field(default_factory=lambda: [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])
    turn_symbol: str = "X"
    move_history: list[dict] = field(default_factory=list)
    game_over: bool = False
    winner: str | None = None
    turn_deadline: float = field(default_factory=lambda: time.time() + TURN_TIMEOUT_SECONDS)


class MoveHistoryStore:
    def __init__(self, path: str = "tictactoe_history.db") -> None:
        self.path = path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS moves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT NOT NULL,
                    player_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    row_idx INTEGER NOT NULL,
                    col_idx INTEGER NOT NULL,
                    ts REAL NOT NULL
                )
                """
            )
            conn.commit()

    def save_move(self, room_id: str, player_id: str, symbol: str, row_idx: int, col_idx: int) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "INSERT INTO moves (room_id, player_id, symbol, row_idx, col_idx, ts) VALUES (?, ?, ?, ?, ?, ?)",
                (room_id, player_id, symbol, row_idx, col_idx, time.time()),
            )
            conn.commit()


class TicTacToeManager:
    def __init__(self) -> None:
        self.waiting_player: PlayerState | None = None
        self.rooms: dict[str, RoomState] = {}
        self.player_room: dict[str, str] = {}
        self.history_store = MoveHistoryStore()

    async def matchmake(self, websocket: WebSocket) -> tuple[str, str, RoomState]:
        await websocket.accept()
        player_id = str(uuid.uuid4())

        if self.waiting_player is None:
            self.waiting_player = PlayerState(player_id=player_id, symbol="X", websocket=websocket)
            return player_id, "X", RoomState(room_id="waiting", players=[self.waiting_player])

        room_id = str(uuid.uuid4())
        p1 = self.waiting_player
        self.waiting_player = None
        p2 = PlayerState(player_id=player_id, symbol="O", websocket=websocket)
        room = RoomState(room_id=room_id, players=[p1, p2])
        self.rooms[room_id] = room
        self.player_room[p1.player_id] = room_id
        self.player_room[p2.player_id] = room_id
        await self.broadcast(room, {"type": "match_found", "room_id": room_id, "turn": room.turn_symbol})
        return player_id, p2.symbol, room

    async def broadcast(self, room: RoomState, payload: dict) -> None:
        for p in room.players:
            await p.websocket.send_json(payload)

    def check_winner(self, board: list[list[str]]) -> str | None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                symbol = board[row][col]
                if not symbol:
                    continue
                if self._wins_from(board, row, col, 0, 1, symbol):
                    return symbol
                if self._wins_from(board, row, col, 1, 0, symbol):
                    return symbol
                if self._wins_from(board, row, col, 1, 1, symbol):
                    return symbol
                if self._wins_from(board, row, col, 1, -1, symbol):
                    return symbol
        return None

    def _wins_from(self, board: list[list[str]], row: int, col: int, dr: int, dc: int, symbol: str) -> bool:
        for step in range(WIN_LENGTH):
            nr = row + dr * step
            nc = col + dc * step
            if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
                return False
            if board[nr][nc] != symbol:
                return False
        return True

    async def apply_move(self, player_id: str, row_idx: int, col_idx: int) -> RoomState:
        room_id = self.player_room[player_id]
        room = self.rooms[room_id]
        player = next(p for p in room.players if p.player_id == player_id)

        if room.game_over:
            raise ValueError("game already finished")
        if player.symbol != room.turn_symbol:
            raise ValueError("not your turn")
        if not (0 <= row_idx < BOARD_SIZE and 0 <= col_idx < BOARD_SIZE):
            raise ValueError("position out of range")
        if room.board[row_idx][col_idx]:
            raise ValueError("cell already occupied")

        room.board[row_idx][col_idx] = player.symbol
        room.move_history.append({"player_id": player_id, "symbol": player.symbol, "row": row_idx, "col": col_idx})
        self.history_store.save_move(room.room_id, player_id, player.symbol, row_idx, col_idx)

        winner = self.check_winner(room.board)
        if winner:
            room.game_over = True
            room.winner = winner
        else:
            room.turn_symbol = "O" if room.turn_symbol == "X" else "X"
            room.turn_deadline = time.time() + TURN_TIMEOUT_SECONDS
        return room

    async def process_timeout(self, room: RoomState) -> bool:
        if room.game_over:
            return False
        if time.time() <= room.turn_deadline:
            return False

        loser = room.turn_symbol
        room.game_over = True
        room.winner = "O" if loser == "X" else "X"
        await self.broadcast(room, {"type": "timeout", "loser": loser, "winner": room.winner})
        return True

    async def cleanup_player(self, player_id: str) -> None:
        room_id = self.player_room.pop(player_id, None)
        if not room_id:
            if self.waiting_player and self.waiting_player.player_id == player_id:
                self.waiting_player = None
            return

        room = self.rooms.get(room_id)
        if not room:
            return
        room.players = [p for p in room.players if p.player_id != player_id]
        if room.players:
            room.game_over = True
            room.winner = room.players[0].symbol
            await self.broadcast(room, {"type": "opponent_left", "winner": room.winner})
        self.rooms.pop(room_id, None)


manager = TicTacToeManager()


async def wait_for_event(websocket: Any) -> dict | None:
    try:
        return await asyncio.wait_for(websocket.receive_json(), timeout=1.0)
    except asyncio.TimeoutError:
        return None
