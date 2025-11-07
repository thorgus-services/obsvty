## Purpose
Establish comprehensive testing strategy covering unit, integration and end-to-end tests with emphasis on TDD practice and refactoring safety net.

## Guidelines
Test-Driven Development cycle is mandatory:
1. Red: Write failing acceptance test against primary port
2. Green: Implement minimal code to pass test (no refactoring yet)
3. Refactor: Improve structure while keeping tests green

Test distribution requirements:
- Unit tests (≥70% of suite): Target Functional Core only
  * Pure functions → no mocks, no setup
  * Must pass in <100ms each
  * Name pattern: `test_<function>_<scenario>_<expectation>`
- Integration tests (≤25%): Test Core + Adapter combinations
  * Use real/fake adapters — no mocks of domain logic
  * Test boundaries between components
- End-to-end tests (≤5%): Full workflow validation
  * Test critical paths only
  * Execute against production-like environment

Acceptance tests must call primary ports directly (bypassing HTTP/CLI):
```python
def test_create_order_with_invalid_email_fails():
    port = InMemoryOrderCommandPort()
    req = CreateOrderRequest(email="invalid", items=[...])
    with pytest.raises(UserValidationError):
        port.create_order(req)
```

Boy Scout Refactoring Checklist (at least one item per PR):
[ ] Reduced function length (e.g., 25 → 18 lines)
[ ] Improved naming (e.g., `data` → `customer_profile`)
[ ] Extracted pure function from shell
[ ] Replaced `if/else` chain with strategy/polymorphism
[ ] Encapsulated data clump into value object
[ ] Added missing test for edge case
[ ] Lowered cyclomatic complexity by ≥1

No refactoring allowed if:
- Critical path has <80% branch coverage
- No characterization test for legacy behavior

## Anti-Patterns
❌ Mocking core logic (e.g., `mock.patch('core.calculate_total')`)
❌ Tests with `time.sleep()` or global state
❌ "# TODO: write test" in merged code
❌ Writing implementation before tests "to explore the problem"
❌ Tests that check implementation details instead of behavior
❌ Acceptance tests that start/stop HTTP servers
❌ "Happy path only" test coverage