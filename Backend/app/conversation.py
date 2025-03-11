import datetime
import threading

class ConversationGraph:
    """
    A thread-safe graph to manage conversation context.
    Stores messages with roles and timestamps.
    """
    def __init__(self) -> None:
        self.nodes = []
        self.lock = threading.Lock()

    def add_message(self, message: str, role: str) -> None:
        """
        Adds a new message with its role and timestamp.
        """
        with self.lock:
            self.nodes.append({
                "message": message,
                "role": role,
                "timestamp": datetime.datetime.now(datetime.timezone.utc)
            })

    def get_relevant_context(self, query: str, top_n: int = 3) -> str:
        """
        Returns the last top_n messages as context for the current query.
        """
        with self.lock:
            relevant_nodes = self.nodes[-top_n:]
            return "\n".join([f"{node['role']}: {node['message']}" for node in relevant_nodes])