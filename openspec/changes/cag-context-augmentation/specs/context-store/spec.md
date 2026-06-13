# Context Store Specification

## Purpose

The context store provides user-isolated persistent storage for context key-value pairs. Each user's context is stored independently and invisible to other users.

## Requirements

### Requirement: Save Context Item

The system MUST accept a user_id, key, and value and store them persistently. The save() method MUST return True on success.

#### Scenario: Save returns True

- GIVEN a ContextStore instance
- WHEN save(user_id="user1", key="topic", value="CAG systems") is called
- THEN the method returns True

#### Scenario: Saved item is retrievable

- GIVEN a ContextStore instance
- WHEN save(user_id="alice", key="level", value="intermediate") is called
- AND list_for_user(user_id="alice") is called
- THEN the result contains exactly [{"key": "level", "value": "intermediate"}]

### Requirement: Retrieve User Context

The system MUST return a list of {"key": k, "value": v} dictionaries for a given user_id.

#### Scenario: Empty user returns empty list

- GIVEN a ContextStore instance with no data
- WHEN list_for_user(user_id="unknown_user") is called
- THEN the result is an empty list []

#### Scenario: Multiple keys for user

- GIVEN a ContextStore with saved items for user "bob"
- WHEN save(user_id="bob", key="language", value="español") is called
- AND save(user_id="bob", key="level", value="avanzado") is called
- AND save(user_id="bob", key="topic", value="ML") is called
- AND list_for_user(user_id="bob") is called
- THEN the result contains all 3 items as [{"key": "language", "value": "español"}, {"key": "level", "value": "avanzado"}, {"key": "topic", "value": "ML"}]

### Requirement: User Isolation

The system MUST isolate user data such that user_a's context is invisible to user_b.

#### Scenario: User data is isolated

- GIVEN a ContextStore instance
- WHEN save(user_id="alice", key="style", value="detailed") is called
- AND save(user_id="bob", key="style", value="concise") is called
- AND list_for_user(user_id="alice") is called
- THEN the result is [{"key": "style", "value": "detailed"}]
- AND list_for_user(user_id="bob") returns [{"key": "style", "value": "concise"}]

### Requirement: Overwrite Existing Key

The system MUST overwrite existing values when the same user_id and key combination is saved again. Only the latest value MUST be retained.

#### Scenario: Save overwrites existing key

- GIVEN a ContextStore instance
- WHEN save(user_id="charlie", key="preference", value="old_value") is called
- AND save(user_id="charlie", key="preference", value="new_value") is called
- AND list_for_user(user_id="charlie") is called
- THEN the result contains exactly [{"key": "preference", "value": "new_value"}]
- AND "old_value" does not appear in the result

## Acceptance Criteria

| Criterion | Test Coverage |
|-----------|---------------|
| save() returns True | test_save_returns_true |
| save() persists items | test_save_stores_and_retrieves |
| Unknown user returns [] | test_list_for_user_empty |
| Multiple keys per user | test_multiple_keys_for_user |
| User isolation | test_users_are_isolated |
| Key overwrite behavior | test_save_overwrites_existing_key |

## Test Mapping

| Requirement | Unit Tests | Validation Tests |
|-------------|-----------|------------------|
| Save Context Item | test_save_returns_true, test_save_stores_and_retrieves | test_saves_context_for_user |
| Retrieve User Context | test_list_for_user_empty, test_multiple_keys_for_user | test_retrieves_context_for_user |
| User Isolation | test_users_are_isolated | N/A |
| Overwrite Existing Key | test_save_overwrites_existing_key | N/A |
