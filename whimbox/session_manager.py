from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class Session:
    session_id: str
    state: str = "IDLE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    name: str = ""
    profile: str = "default"
    window_handle: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SessionManager:
    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}
        self._lock = Lock()

    def create(
        self,
        name: str = "",
        profile: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        session_id = f"sess_{uuid4().hex}"
        session = Session(
            session_id=session_id,
            name=name or "",
            profile=profile or "default",
            metadata=metadata or {},
        )
        with self._lock:
            self._sessions[session_id] = session
        return session

    def find_default_session(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            for session in self._sessions.values():
                if session.name == "default" and session.profile == "default":
                    return asdict(session)
        return None

    def list(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [asdict(item) for item in self._sessions.values()]

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            session = self._sessions.get(session_id)
            return asdict(session) if session else None

    def update_window(self, session_id: str, window_handle: int) -> Optional[Dict[str, Any]]:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None
            session.window_handle = window_handle
            return asdict(session)

    def set_state(self, session_id: str, state: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None
            session.state = state
            return asdict(session)

    def close(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None


session_manager = SessionManager()

