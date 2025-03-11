import datetime
import threading
from typing import Any, Dict
from app.conversation import ConversationGraph

class SessionManager:
    """
    Manages user sessions in a thread-safe manner.
    Resets sessions after 30 minutes of inactivity.
    """
    def __init__(self) -> None:
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Retrieves or initializes a session.
        Resets the session if inactive for over 30 minutes.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "message_count": 0,
                    "conversation_graph": ConversationGraph(),
                    "last_activity": now
                }
            else:
                session = self.sessions[session_id]
                if now - session.get("last_activity", now) > datetime.timedelta(minutes=30):
                    self.sessions[session_id] = {
                        "message_count": 0,
                        "conversation_graph": ConversationGraph(),
                        "last_activity": now
                    }
                else:
                    session["last_activity"] = now
            return self.sessions[session_id]
