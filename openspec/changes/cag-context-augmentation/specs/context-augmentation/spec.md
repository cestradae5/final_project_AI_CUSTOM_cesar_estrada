# Context Augmentation Specification

## Purpose

The context augmentation module applies user-stored context to modify assistant answers. It processes context items and incorporates them into the base answer using rule-based transformations.

## Requirements

### Requirement: No Context Returns Base Answer

The system MUST return the base_answer unchanged when context_items is empty, None, or contains no recognized keys.

#### Scenario: Empty context list

- GIVEN user_id="user1", question="What is CAG?", base_answer="CAG is Context-Augmented Generation."
- WHEN apply_context(user_id, question, base_answer, context_items=[]) is called
- THEN the result equals base_answer exactly

#### Scenario: None context items

- GIVEN user_id="user3", question="What is Python?", base_answer="Python is a programming language."
- WHEN apply_context(user_id, question, base_answer, context_items=None) is called
- THEN the result is not None
- AND the result equals base_answer

### Requirement: Audience Context Modification

The system MUST incorporate audience-level context into the answer. When context contains {"key": "audience", "value": "explicar como principiante"}, the modified answer MUST contain the word "principiante".

#### Scenario: Audience context modifies answer

- GIVEN user_id="luis", question="Que es CAG?", base_answer="CAG es un sistema avanzado."
- WHEN apply_context(user_id, question, base_answer, [{"key": "audience", "value": "explicar como principiante"}]) is called
- THEN the result contains "principiante" (case-insensitive)

### Requirement: Multiple Context Items

The system MUST process all context items when multiple are provided. The result MUST differ from the base_answer when context is present.

#### Scenario: Multiple context items processed

- GIVEN user_id="student1", question="Explica REST", base_answer="REST es un estilo arquitectonico."
- WHEN apply_context(user_id, question, base_answer, [{"key": "audience", "value": "principiante"}, {"key": "language", "value": "español"}, {"key": "include_examples", "value": "si"}]) is called
- THEN the result is not None
- AND the result differs from base_answer

### Requirement: Unknown Keys Ignored Gracefully

The system MUST NOT raise exceptions or fail when context_items contains unknown keys. Unknown keys MUST be ignored without affecting the output.

#### Scenario: Unknown keys do not break processing

- GIVEN user_id="user2", question="What is REST?", base_answer="REST is an architectural style."
- WHEN apply_context(user_id, question, base_answer, [{"key": "unknown_key_xyz", "value": "some value"}, {"key": "another_unknown", "value": "another value"}]) is called
- THEN the result is not None
- AND no exception is raised

### Requirement: Integration with Assistant

The system MUST integrate with assistant.answer_question() such that:
1. User context is retrieved via context_store.list_for_user(user_id)
2. Context is passed to cag.apply_context()
3. The response includes context_used as a list of context keys that were applied

#### Scenario: Ask endpoint uses context

- GIVEN user "luis" has saved context {"key": "audience", "value": "explicar como principiante"}
- WHEN POST /api/ask with {"user_id": "luis", "question": "Que es CAG?"}
- THEN response status is 200
- AND response["answer"] contains "principiante" (case-insensitive)
- AND response["context_used"] contains "audience"

## Acceptance Criteria

| Criterion | Test Coverage |
|-----------|---------------|
| Empty context returns base | test_no_context_returns_base_answer |
| Audience context applied | test_audience_context_modifies_answer, test_ask_uses_context_to_influence_later_response |
| Multiple context items | test_multiple_context_items |
| Unknown keys ignored | test_unknown_context_keys_ignored |
| None handled gracefully | test_none_context_items |
| Integration complete | test_ask_uses_context_to_influence_later_response |

## Test Mapping

| Requirement | Unit Tests | Validation Tests |
|-------------|-----------|------------------|
| No Context Returns Base Answer | test_no_context_returns_base_answer, test_none_context_items | N/A |
| Audience Context Modification | test_audience_context_modifies_answer | test_ask_uses_context_to_influence_later_response |
| Multiple Context Items | test_multiple_context_items | N/A |
| Unknown Keys Ignored Gracefully | test_unknown_context_keys_ignored | N/A |
| Integration with Assistant | N/A | test_ask_uses_context_to_influence_later_response |
