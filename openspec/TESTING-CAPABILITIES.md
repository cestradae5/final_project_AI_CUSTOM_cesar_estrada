# Testing Capabilities — final_project_AI_CUSTOM_cesar_estrada

**Detected:** 2026-06-12  
**Test Runner:** unittest  
**Framework:** None (pure stdlib)

## Summary

| Capability | Status | Details |
|------------|--------|---------|
| Test Runner | ✅ CONFIGURED | `python -m unittest discover -s {layer} -v` |
| Test Layers | ✅ STRUCTURED | base (passing), validation (failing), unit (red phase) |
| Coverage | ⏸️ OPTIONAL | `coverage.py` not configured; pure stdlib project |
| Linting | ⏸️ OPTIONAL | No linter configured; can add `flake8` or `ruff` if needed |
| Type Checking | ⏸️ OPTIONAL | No type checker; pure stdlib doesn't require `mypy` |
| Formatting | ⏸️ OPTIONAL | No formatter configured; `black` optional |

## Test Runner: unittest

### Command Syntax

```bash
# Run all tests in a layer
python -m unittest discover -s tests/base -v
python -m unittest discover -s tests/validation -v
python -m unittest discover -s tests/unit -v

# Run all tests
python -m unittest discover -s tests -v

# Run specific test class
python -m unittest tests.base.test_base_api.BaseApiTest -v

# Run specific test method
python -m unittest tests.base.test_base_api.BaseApiTest.test_health_returns_ok -v
```

### How unittest Discovers Tests

1. Scans `-s` directory for files matching `test_*.py`
2. Loads `TestCase` subclasses from those files
3. Runs methods starting with `test_`
4. Reports results in verbose (`-v`) format

### Current Test State

**Base (tests/base/)**
```
✅ test_base_api.BaseApiTest.test_health_returns_ok
✅ test_base_api.BaseApiTest.test_ask_requires_user_and_question
✅ test_base_api.BaseApiTest.test_ask_answers_from_knowledge_base
```
- Status: 3/3 PASSING
- Time: ~0.75s
- Key: Integration tests; server must be running and responding correctly

**Validation (tests/validation/)**
```
❌ test_cag_contract.CagContractTest.test_saves_context_for_user (501 → expected 201)
❌ test_cag_contract.CagContractTest.test_retrieves_context_for_user (501 → expected 200)
❌ test_cag_contract.CagContractTest.test_ask_uses_context_to_influence_later_response (answer doesn't contain "principiante")
```
- Status: 0/3 PASSING
- Time: ~0.65s
- Key: Feature tests; CAG context storage and retrieval not implemented

**Unit (tests/unit/)**
```
✅ test_unit_cag.TestApplyContext.test_no_context_returns_base_answer
❌ test_unit_cag.TestApplyContext.test_audience_context_modifies_answer
❌ test_unit_cag.TestApplyContext.test_multiple_context_items
✅ test_unit_cag.TestApplyContext.test_unknown_context_keys_ignored
✅ test_unit_cag.TestApplyContext.test_none_context_items

❌ test_unit_context_store.TestContextStoreSave.test_save_returns_true (ERROR: NotImplementedError)
❌ test_unit_context_store.TestContextStoreSave.test_save_stores_and_retrieves (ERROR: NotImplementedError)
❌ test_unit_context_store.TestContextStoreSave.test_list_for_user_empty (ERROR: NotImplementedError)
❌ test_unit_context_store.TestContextStoreSave.test_multiple_keys_for_user (ERROR: NotImplementedError)
❌ test_unit_context_store.TestContextStoreSave.test_users_are_isolated (ERROR: NotImplementedError)
❌ test_unit_context_store.TestContextStoreSave.test_save_overwrites_existing_key (ERROR: NotImplementedError)
```
- Status: 3/11 PASSING, 2 FAIL, 6 ERROR
- Time: ~0.03s
- Key: TDD red phase; stubs raise NotImplementedError intentionally

## Test Conventions

### File Naming
- Layer tests: `test_{layer}_{feature}.py`
  - `test_base_api.py` — base layer API tests
  - `test_cag_contract.py` — validation layer CAG contract
  - `test_unit_cag.py`, `test_unit_context_store.py` — unit tests

### Class Naming
- `TestClassName(unittest.TestCase)` — describes what's being tested

### Method Naming
- `test_{behavior}_{condition}` — descriptive, states the assertion
  - `test_no_context_returns_base_answer`
  - `test_save_stores_and_retrieves`

### Docstrings
- First line: one-sentence description of behavior
- Optional: paragraph with context or edge case notes
- Example:
  ```python
  def test_audience_context_modifies_answer(self):
      """
      If context has {"key": "audience", "value": "explicar como principiante"},
      the answer should contain "principiante".
      """
  ```

### Fixtures

**Base Layer (Integration):**
```python
@classmethod
def setUpClass(cls):
    # Start server once for entire test class
    cls.server = create_server(port=0)
    cls.port = cls.server.server_address[1]
    cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
    cls.thread.start()

@classmethod
def tearDownClass(cls):
    # Shutdown server once after all tests
    cls.server.shutdown()
    cls.server.server_close()
```

**Unit Layer:**
```python
def setUp(self):
    # Create fresh instance for each test
    self.store = ContextStore()
```

## Strict TDD Workflow

### Red Phase (✍️ Write Test)
1. Write failing test that describes desired behavior
2. Run test → FAIL ❌
3. Test defines the contract

### Green Phase (💻 Implement)
1. Write minimal code to make test pass
2. Run test → PASS ✅
3. No more, no less

### Refactor Phase (🧹 Improve)
1. Clean up code without changing behavior
2. Run tests → PASS ✅
3. Tests confirm refactoring didn't break anything

### Example: ContextStore.save()

**Red:** Write failing test
```python
def test_save_returns_true(self):
    result = self.store.save(user_id="user1", key="topic", value="CAG")
    self.assertTrue(result)
```

**Green:** Implement minimum
```python
def save(self, user_id, key, value):
    # Minimal implementation: return True
    return True
```

**Refactor:** Add storage later as more tests demand it
```python
def __init__(self):
    self._storage = {}  # {user_id: {key: value}}

def save(self, user_id, key, value):
    if user_id not in self._storage:
        self._storage[user_id] = {}
    self._storage[user_id][key] = value
    return True
```

## Coverage (Optional)

To add coverage later:
```bash
pip install coverage
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m coverage html  # generates htmlcov/index.html
```

## Linting (Optional)

To add linting later:
```bash
pip install ruff
ruff check backend/ tests/
ruff format backend/ tests/
```

## Type Checking (Optional)

To add type checking later (even with pure stdlib):
```bash
pip install mypy
mypy backend/ --strict
```

## Pytest Alternative (NOT RECOMMENDED)

This project uses `unittest`, not `pytest`. Reasons:
- `unittest` is stdlib (zero dependencies)
- Project emphasizes pure-stdlib design
- All tests are already written for `unittest`

If pytest is introduced later, would require rewriting test structure (fixtures, assertions, plugins).
