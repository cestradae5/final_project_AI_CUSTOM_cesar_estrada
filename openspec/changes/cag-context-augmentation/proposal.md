# Proposal: CAG Context Augmentation

## Intent

Enable persistent user context storage and inject it alongside RAG-sourced knowledge into assistant responses. Users should be able to set preferences (audience level, language, include_examples) that influence how answers are formatted.

## Scope

### In Scope
- ContextStore implementation with user-isolated in-memory dict storage
- apply_context() rule-based answer modification for known context keys
- Integration into assistant.answer_question() flow with context_used tracking
- All 11 unit tests passing green
- All 3 validation tests passing green
- Base tests (3) remain green

### Out of Scope
- File/database persistence (in-memory sufficient for exam)
- LLM prompt injection (rule-based string manipulation only)
- Authentication/authorization
- Context expiration or TTL

## Capabilities

### New Capabilities
- `context-store`: User-isolated context persistence with save/retrieve/list operations
- `context-augmentation`: Rule-based answer modification based on stored context keys

### Modified Capabilities
None (no existing specs to modify)

## Approach

| Component | Strategy |
|-----------|----------|
| Storage | Dict: `{user_id: {key: value}}` |
| Augmentation | Rule-based string modification per context key |
| Integration | `answer_question()` retrieves context, calls `apply_context()`, returns `context_used` |

**Context keys and rules:**
- `audience`: Prefix answer with complexity indicator
- `language`: Append language note
- `include_examples`: Add example prompt when true

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/context_store.py` | Modified | Implement ContextStore class methods |
| `backend/cag.py` | Modified | Implement apply_context() logic |
| `backend/assistant.py` | Modified | Integrate context retrieval + application |
| `tests/unit/` | Validated | 11 tests must pass |
| `tests/validation/` | Validated | 3 tests must pass |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Context key collision | Low | Validate keys against known list |
| User isolation failure | Medium | Unit test coverage for user separation |
| Answer corruption | Low | apply_context returns unmodified if no context |

## Rollback Plan

Revert to stub implementations:
- `context_store.py`: restore `raise NotImplementedError`
- `cag.py`: restore `return base_answer`
- No HTTP endpoint changes needed (already wired)

## Dependencies

None. Pure stdlib implementation.

## Success Criteria

- [ ] `python -m unittest discover -s tests/unit -v` shows 11/11 pass
- [ ] `python -m unittest discover -s tests/validation -v` shows 3/3 pass
- [ ] `python -m unittest discover -s tests/base -v` shows 3/3 pass
- [ ] POST `/api/context` returns 201 with saved context
- [ ] GET `/api/context` returns user's stored context
- [ ] `/api/ask` responses reflect stored context preferences
