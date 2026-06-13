"""In-memory context store for user preferences (CAG - Context-Augmented Generation)."""


class ContextStore:
    def __init__(self):
        self._data = {}  # {user_id: {key: value}}

    def save(self, user_id, key, value):
        """Store a key-value preference for a user. Returns True on success."""
        if user_id not in self._data:
            self._data[user_id] = {}
        self._data[user_id][key] = value
        return True

    def list_for_user(self, user_id):
        """Return all context items for a user as a list of {"key": k, "value": v} dicts."""
        return [
            {"key": k, "value": v}
            for k, v in self._data.get(user_id, {}).items()
        ]
