# Project: Context-Augmented Generation (CAG) System

**Initialized:** 2026-06-12  
**Mode:** openspec + SDD  
**Status:** TDD Red Phase (tests written, implementation in progress)

## What This Is

A Python HTTP service that answers questions about software engineering topics (courses, CAG, SDD, BDD, TDD) and personalizes responses using **Context-Augmented Generation (CAG)**: storing user context (audience level, language preference, style) and automatically adapting answers to that context.

## Technology Stack

- **Language:** Python 3.14.6 (pure stdlib)
- **Server:** `http.server.ThreadingHTTPServer`
- **Testing:** `unittest` (auto-discovery)
- **Dependencies:** None (pure stdlib only)

## Project Structure

```
final_project_AI_CUSTOM_cesar_estrada/
├── backend/
│   ├── server.py           # HTTP server with GET /health, GET /api/context, POST /api/ask
│   ├── assistant.py        # answer_question(user_id, question) → knowledge base lookup
│   ├── cag.py              # apply_context(user_id, question, base_answer, context_items) → augmented answer
│   ├── context_store.py    # ContextStore: save() and list_for_user() for persistence (STUB)
│   └── knowledge.py        # Domain knowledge lookup
├── tests/
│   ├── base/               # Integration tests (PASSING 3/3)
│   │   └── test_base_api.py
│   ├── validation/         # Contract tests for CAG feature (FAILING 0/3)
│   │   └── test_cag_contract.py
│   └── unit/               # Unit tests (FAILING 3/11 pass)
│       ├── test_unit_cag.py
│       └── test_unit_context_store.py
├── openspec/
│   ├── config.yaml         # SDD testing capabilities & stack detection
│   ├── PROJECT.md          # This file
│   └── [proposals/specs/designs/tasks] (created during SDD phases)
└── [other: data/, docs/, scripts/, frontend/, etc.]
```

## Current Test Status

| Layer | Status | Count |
|-------|--------|-------|
| **base** (integration) | ✅ PASSING | 3/3 |
| **validation** (contract) | ❌ FAILING | 0/3 |
| **unit** (isolated) | ⚠️ MIXED | 3/11 pass, 2 fail, 6 error |

### Base Tests (PASSING)
- `test_health_returns_ok` — GET /health → 200 {"status": "ok"}
- `test_ask_requires_user_and_question` — POST /api/ask without user_id or question → 400
- `test_ask_answers_from_knowledge_base` — POST /api/ask with valid inputs → 200 with answer

### Validation Tests (FAILING)
- `test_saves_context_for_user` — POST /api/context to save → expects 201 (currently 501 NotImplementedError)
- `test_retrieves_context_for_user` — GET /api/context to retrieve → expects 200 (currently 501)
- `test_ask_uses_context_to_influence_later_response` — Integration: save context, ask, check answer reflects context

### Unit Tests (MIXED — TDD Red Phase)
**Passing:**
- `test_no_context_returns_base_answer` — apply_context([]) returns base unchanged
- `test_unknown_context_keys_ignored` — gracefully handles unknown keys
- `test_none_context_items` — handles None or [] without breaking

**Failing:**
- `test_audience_context_modifies_answer` — apply_context() doesn't process audience context
- `test_multiple_context_items` — apply_context() doesn't modify answer with multiple context items

**Erroring (NotImplementedError):**
- `test_save_returns_true` — ContextStore.save() not implemented
- `test_save_stores_and_retrieves` — ContextStore persistence not implemented
- `test_list_for_user_empty` — ContextStore.list_for_user() not implemented
- `test_multiple_keys_for_user` — ContextStore multi-key storage not implemented
- `test_users_are_isolated` — ContextStore user isolation not implemented
- `test_save_overwrites_existing_key` — ContextStore key overwrite not implemented

## Key Design Decisions

### Strict TDD: true
- Tests are written FIRST (red phase)
- Implementation follows test requirements (green phase)
- Refactoring improves code without breaking tests

### Test Layers (Separation of Concerns)
- **base:** Integration—server responds correctly to HTTP
- **validation:** Contracts—CAG context features work end-to-end
- **unit:** Isolated—individual functions work in isolation

### No Frameworks
- Pure stdlib `http.server` for simplicity
- Demonstrates core concepts without framework magic
- Explicit control flow and error handling

### Context Types
- `audience`: user's technical level (principiante, intermedio, avanzado)
- `language`: preferred language (español, english)
- `include_examples`: whether to add code examples
- `style`: concise vs. detailed
- `topic`: current topic of interest

## Next Steps in SDD

1. **explore** — Clarify context incorporation strategies; what does "use context" mean?
2. **propose** — Scope the CAG feature: what gets built, what's deferred?
3. **spec** — Define ContextStore interface and apply_context behavior precisely
4. **design** — Architecture for persistent storage, CAG answer modification algorithm
5. **tasks** — Break into reviewable work units
6. **apply** — Implement ContextStore and apply_context (TDD: red → green → refactor)
7. **verify** — All tests pass; validate CAG feature works end-to-end
8. **archive** — Document what was built; close the SDD cycle

## Strict TDD Rationale

Unittest is the project's test runner (3 passing base tests). TDD discipline enforces:
- Write failing tests FIRST
- Implement ONLY to make tests pass
- Refactor WITHOUT changing tests
- Tests become specification of behavior

This prevents "over-engineering" and keeps focus on user-facing contracts.
