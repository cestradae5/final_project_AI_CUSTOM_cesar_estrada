# Tasks: CAG Context Augmentation

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 80-120 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | single-pr |
| Chain strategy | size-exception |

**Rationale**: Three files modified with minimal logic (~40 lines ContextStore, ~30 lines apply_context, ~15 lines assistant integration). Pure TDD implementation with existing tests. Low complexity, isolated change.

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Complete CAG Context Augmentation | PR 1 | All 3 files + tests included; single atomic feature |

## Phase 1: Foundation (ContextStore Implementation)

- [x] 1.1 Replace `backend/context_store.py` stub with in-memory dict storage: `self._data = {}`
- [x] 1.2 Implement `save(user_id, key, value)` to initialize user dict if needed, set key=value, return True
- [x] 1.3 Implement `list_for_user(user_id)` to return list of `{"key": k, "value": v}` or `[]` for unknown users
- [x] 1.4 Verify: Run `python -m unittest tests.unit.test_unit_context_store` → expect 6/6 green

## Phase 2: Core Logic (Context Augmentation)

- [x] 2.1 Update `backend/cag.py` apply_context to handle None/empty context_items → return base_answer unchanged
- [x] 2.2 Add rule: if context has `{"key": "audience", "value": ...}` with "principiante" → append "(adaptado para principiante)"
- [x] 2.3 Add rule: if context has `{"key": "language", "value": ...}` → append language marker
- [x] 2.4 Add rule: if context has `{"key": "include_examples", "value": "si"}` → append "(con ejemplos incluidos)"
- [x] 2.5 Unknown keys ignored silently (no error, no modification)
- [x] 2.6 Verify: Run `python -m unittest tests.unit.test_unit_cag` → expect 5/5 green

## Phase 3: Integration (Assistant Wiring)

- [x] 3.1 Import `ContextStore` and `apply_context` into `backend/assistant.py`
- [x] 3.2 Create module-level instance: `context_store = ContextStore()`
- [x] 3.3 In `answer_question()`, after building base answer, call `context_store.list_for_user(user_id)`
- [x] 3.4 Apply context: `answer = apply_context(user_id, question, answer, context_items)`
- [x] 3.5 Build context_used list: extract keys from context_items that appear in final answer
- [x] 3.6 Return updated response with modified answer and context_used list
- [x] 3.7 Verify: Run `python -m unittest tests.validation.test_cag_contract` → expect 3/3 green

## Phase 4: Full Verification

- [x] 4.1 Run full test suite: `python -m unittest discover -s tests -p "test_*.py"`
- [x] 4.2 Verify: base tests (3/3 green), unit tests (11/11 green), validation tests (3/3 green)
- [x] 4.3 Verify: Total 17/17 tests pass
- [x] 4.4 Confirm no regressions in existing RAG functionality
