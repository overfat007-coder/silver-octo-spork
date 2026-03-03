"""Session management for mobile auth."""


class SessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, str] = {}

    def bind(self, session_id: str, user_id: str) -> None:
        self._sessions[session_id] = user_id

    def user_for(self, session_id: str) -> str | None:
        return self._sessions.get(session_id)
