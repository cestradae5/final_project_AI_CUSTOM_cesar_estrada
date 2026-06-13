"""
Unit tests for ContextStore in isolation (TDD red phase).

These tests FAIL with the current stub implementation because:
- save() raises NotImplementedError
- list_for_user() raises NotImplementedError
"""

import unittest

from backend.context_store import ContextStore


class TestContextStoreSave(unittest.TestCase):
    """Test ContextStore.save() behavior."""

    def setUp(self):
        self.store = ContextStore()

    def test_save_returns_true(self):
        """Calling save() should return True to indicate successful storage."""
        result = self.store.save(user_id="user1", key="topic", value="CAG systems")
        self.assertTrue(result)

    def test_save_stores_and_retrieves(self):
        """
        After save(), list_for_user() should return the item as
        {"key": k, "value": v}.
        """
        self.store.save(user_id="alice", key="level", value="intermediate")
        context = self.store.list_for_user(user_id="alice")

        self.assertEqual(len(context), 1)
        self.assertIn({"key": "level", "value": "intermediate"}, context)

    def test_list_for_user_empty(self):
        """Unknown user returns empty list []."""
        context = self.store.list_for_user(user_id="unknown_user")
        self.assertEqual(context, [])

    def test_multiple_keys_for_user(self):
        """Multiple saves all appear in list for that user."""
        user_id = "bob"
        self.store.save(user_id=user_id, key="language", value="español")
        self.store.save(user_id=user_id, key="level", value="avanzado")
        self.store.save(user_id=user_id, key="topic", value="ML")

        context = self.store.list_for_user(user_id=user_id)

        self.assertEqual(len(context), 3)
        self.assertIn({"key": "language", "value": "español"}, context)
        self.assertIn({"key": "level", "value": "avanzado"}, context)
        self.assertIn({"key": "topic", "value": "ML"}, context)

    def test_users_are_isolated(self):
        """user_a's data does not appear in user_b's list."""
        user_a = "alice"
        user_b = "bob"

        self.store.save(user_id=user_a, key="style", value="detailed")
        self.store.save(user_id=user_b, key="style", value="concise")

        context_a = self.store.list_for_user(user_id=user_a)
        context_b = self.store.list_for_user(user_id=user_b)

        self.assertEqual(context_a, [{"key": "style", "value": "detailed"}])
        self.assertEqual(context_b, [{"key": "style", "value": "concise"}])

    def test_save_overwrites_existing_key(self):
        """
        Saving the same key twice for the same user keeps only the latest value.
        """
        user_id = "charlie"
        key = "preference"

        self.store.save(user_id=user_id, key=key, value="old_value")
        self.store.save(user_id=user_id, key=key, value="new_value")

        context = self.store.list_for_user(user_id=user_id)

        self.assertEqual(len(context), 1)
        self.assertIn({"key": key, "value": "new_value"}, context)
        self.assertNotIn({"key": key, "value": "old_value"}, context)


if __name__ == "__main__":
    unittest.main()
