import asyncio

from app.services.tictactoe import BOARD_SIZE, RoomState, TicTacToeManager


def test_winner_detection_on_5x5_row() -> None:
    manager = TicTacToeManager()
    board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for idx in range(BOARD_SIZE):
        board[2][idx] = "X"
    assert manager.check_winner(board) == "X"


def test_timeout_sets_opposite_winner() -> None:
    manager = TicTacToeManager()
    room = RoomState(room_id="r1", players=[])
    room.turn_symbol = "X"
    room.turn_deadline = 0

    called = []

    async def fake_broadcast(_room, payload):
        called.append(payload)

    manager.broadcast = fake_broadcast  # type: ignore[assignment]

    result = asyncio.run(manager.process_timeout(room))
    assert result is True
    assert room.winner == "O"
    assert called[0]["type"] == "timeout"
