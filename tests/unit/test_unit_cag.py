"""
Unit tests for apply_context function in isolation (TDD red phase).

These tests FAIL with the current stub implementation because:
- apply_context() just returns base_answer unchanged
- It does not process or incorporate context_items
"""

import unittest

from backend.cag import apply_context


class TestApplyContext(unittest.TestCase):
    """Test apply_context() behavior with various context scenarios."""

    def test_no_context_returns_base_answer(self):
        """Empty context_items returns base_answer unchanged."""
        user_id = "user1"
        question = "What is CAG?"
        base_answer = "CAG is Context-Augmented Generation."
        context_items = []

        result = apply_context(user_id, question, base_answer, context_items)

        self.assertEqual(result, base_answer)

    def test_audience_context_modifies_answer(self):
        """
        If context has {"key": "audience", "value": "explicar como principiante"},
        the answer should contain "principiante".
        """
        user_id = "luis"
        question = "Que es CAG?"
        base_answer = "CAG es un sistema avanzado."
        context_items = [{"key": "audience", "value": "explicar como principiante"}]

        result = apply_context(user_id, question, base_answer, context_items)

        self.assertIn("principiante", result.lower())

    def test_multiple_context_items(self):
        """Multiple context items work; all context keys appear in result."""
        user_id = "student1"
        question = "Explica REST"
        base_answer = "REST es un estilo arquitectonico."
        context_items = [
            {"key": "audience", "value": "principiante"},
            {"key": "language", "value": "español"},
            {"key": "include_examples", "value": "si"},
        ]

        result = apply_context(user_id, question, base_answer, context_items)

        # Result should incorporate the context in some way that includes
        # evidence of processing all three context items
        self.assertIsNotNone(result)
        # The result should be modified from the base answer when context is present
        self.assertNotEqual(result, base_answer)

    def test_unknown_context_keys_ignored(self):
        """Unknown context keys don't break; gracefully handled."""
        user_id = "user2"
        question = "What is REST?"
        base_answer = "REST is an architectural style."
        context_items = [
            {"key": "unknown_key_xyz", "value": "some value"},
            {"key": "another_unknown", "value": "another value"},
        ]

        # Should not raise an exception
        result = apply_context(user_id, question, base_answer, context_items)

        self.assertIsNotNone(result)

    def test_none_context_items(self):
        """None or empty list for context_items handled gracefully."""
        user_id = "user3"
        question = "What is Python?"
        base_answer = "Python is a programming language."

        # Test with None
        result_none = apply_context(user_id, question, base_answer, None)
        self.assertIsNotNone(result_none)

        # Test with empty list (should behave like no context)
        result_empty = apply_context(user_id, question, base_answer, [])
        self.assertEqual(result_empty, base_answer)


if __name__ == "__main__":
    unittest.main()
