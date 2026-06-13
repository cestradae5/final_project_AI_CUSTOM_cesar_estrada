# Design: CAG Context Augmentation

## Technical Approach

Implement in-memory context storage with rule-based augmentation to modify RAG answers based on user preferences. The design follows TDD principles with minimal changes to existing code, ensuring all 17 tests pass (11 unit + 3 validation + 3 base).

## Architecture Decisions

### Decision: In-Memory Storage

**Choice**: Dict structure `{user_id: {key: value}}`
**Alternatives considered**: SQLite, file persistence, Redis
**Rationale**: Exam scope requires simplicity; in-memory meets all test requirements without external dependencies

### Decision: Rule-Based Augmentation

**Choice**: String manipulation via known key patterns
**Alternatives considered**: LLM prompting, template engine
**Rationale**: Deterministic behavior for testing; no LLM costs; explicit control over modifications

### Decision: Integration Point

**Choice**: Modify `answer_question()` after base answer construction
**Alternatives considered**: Modify `retrieve_snippets()`, wrap entire assistant
**Rationale**: Clear separation of concerns; RAG retrieval unchanged; context applied as final layer

## Data Flow

```
User Request ──→ answer_question() ──→ retrieve_snippets()
                        │                      │
                        │                      ▼
                        │               Knowledge Base
                        │                      │
                        │                      ▼
                        │               base_answer built
                        │                      │
                        ▼                      │
                 context_store.list()         │
                        │                      │
                        ▼                      ▼
                 apply_context(base_answer, context_items)
                        │
                        ▼
                 Final Response with context_used
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/context_store.py` | Modify | Replace NotImplementedError with dict storage |
| `backend/cag.py` | Modify | Implement rule-based answer modification |
| `backend/assistant.py` | Modify | Add context retrieval and application |

## Interfaces / Contracts

```python
# ContextStore maintains user isolation
class ContextStore:
    def __init__(self):
        self._data = {}  # {user_id: {key: value}}
    
    def save(self, user_id, key, value) -> bool:
        # Initialize user dict if needed
        # Set key=value
        # Return True
    
    def list_for_user(self, user_id) -> list:
        # Return [{"key": k, "value": v}, ...]
        # Empty list if user unknown

# Apply context modifies answer based on rules
def apply_context(user_id, question, base_answer, context_items):
    # Known keys:
    # - "audience" with "principiante" -> append "(adaptado para principiante)"
    # - "language" -> append language marker
    # - "include_examples" == "si" -> append "(con ejemplos incluidos)"
    # Unknown keys: ignore silently
    # None/empty context: return base_answer unchanged
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | ContextStore isolation, user separation, overwrites | Direct class testing, no HTTP |
| Unit | apply_context rule application, edge cases | Function testing with mocked context |
| Integration | HTTP endpoints, status codes, JSON contracts | Full server with threading |
| Validation | End-to-end context influence on answers | Store context then verify answer changes |
| Base | RAG functionality unchanged | Ensure knowledge retrieval still works |

## Migration / Rollout

No migration required. In-memory storage starts fresh on each server restart.

## Open Questions

- [ ] Should context persist across server restarts? (Out of scope per proposal)
- [ ] Context size limits per user? (Not specified in requirements)