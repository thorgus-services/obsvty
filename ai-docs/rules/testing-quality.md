# Testing and Quality Rule

**Based on:** TDD, Clean Architecture, SOLID Principles, Quality Metrics
**Scope:** Test strategies, quality gates, and continuous validation

## Test Pyramid Strategy

### Unit Tests (Foundation)
- **Coverage:** 70-80% of test suite
- **Scope:** Single class/function in isolation
- **Speed:** Fast execution (<100ms per test)
- **Purpose:** Verify internal logic and behavior

### Integration Tests (Middle Layer)
- **Coverage:** 15-20% of test suite  
- **Scope:** Component interactions
- **Speed:** Medium execution (seconds)
- **Purpose:** Verify integration points

### End-to-End Tests (Top Layer)
- **Coverage:** 5-10% of test suite
- **Scope:** Full system workflows
- **Speed:** Slow execution (minutes)
- **Purpose:** Verify user journeys

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle
1. **Red:** Write failing test for desired feature
2. **Green:** Write minimal code to pass test
3. **Refactor:** Improve code while keeping tests green

### TDD Benefits
- **Design Feedback:** Tests drive better design
- **Safety Net:** Confidence to refactor
- **Documentation:** Living specification
- **Quality:** Built-in quality assurance

### Example TDD Flow
```python
# 1. Red: Write failing test
def test_addition():
    assert add(2, 3) == 5

# 2. Green: Minimal implementation
def add(a, b):
    return a + b

# 3. Refactor: Improve if needed
# (No refactoring needed for simple addition)
```

## Unit Testing Principles

### FIRST Principles
- **Fast:** Tests run quickly
- **Isolated:** Tests don't depend on each other
- **Repeatable:** Same results every time
- **Self-Validating:** Pass/fail without manual interpretation
- **Timely:** Written before or with production code

### Test Structure (Arrange-Act-Assert)
```python
def test_user_creation():
    # Arrange: Setup test data
    user_data = {"name": "John", "email": "john@example.com"}
    
    # Act: Execute the behavior
    user = create_user(user_data)
    
    # Assert: Verify outcomes
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.is_active is True
```

### Mocking and Isolation
- **Rule:** Mock external dependencies
- **Benefit:** Fast, reliable tests
- **Tools:** unittest.mock, pytest-mock
- **Example:**
  ```python
  def test_order_processing(mocker):
      # Mock external service
      mock_email = mocker.patch('services.email.send_confirmation')
      
      # Test order processing
      process_order(test_order)
      
      # Verify email was sent
      mock_email.assert_called_once()
  ```

## Integration Testing

### Testing Real Integrations
- **Database:** Test with real database (test instance)
- **APIs:** Test with real HTTP calls (test environment)
- **Message Queues:** Test with real queues (test instance)

### Test Containers Strategy
- **Approach:** Use Docker containers for dependencies
- **Benefits:** Real integration testing
- **Tools:** testcontainers-python
- **Example:**
  ```python
  def test_database_integration():
      with PostgresContainer() as postgres:
          # Connect to real test database
          db = connect(postgres.get_connection_url())
          
          # Test database operations
          result = db.query("SELECT 1")
          assert result == 1
  ```

## Quality Metrics and Gates

### Code Coverage
- **Minimum:** 80% line coverage
- **Goal:** 90%+ line coverage
- **Critical Paths:** 100% coverage for business logic
- **Tools:** coverage.py, pytest-cov

### Static Analysis
- **Type Checking:** mypy with strict mode
- **Linting:** flake8, pylint, black
- **Security:** bandit, safety
- **Complexity:** radon (cyclomatic complexity)

### Complexity Metrics
- **Cyclomatic Complexity:** < 10 per function
- **Cognitive Complexity:** < 15 per function
- **Maintainability Index:** > 85
- **Technical Debt Ratio:** < 5%

## Test Organization and Structure

### Project Structure
```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── module.py
│       └── submodule/
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_module.py
    │   └── test_submodule/
    ├── integration/
    │   ├── test_database.py
    │   └── test_api.py
    └── e2e/
        └── test_user_journeys.py
```

### Test Naming Conventions
- **Unit Tests:** test_<method>_<scenario>_<expected>
- **Integration Tests:** test_<component>_integration_<scenario>
- **E2E Tests:** test_<user_journey>_workflow

### Example Test Names
```python
def test_create_user_valid_data_returns_user()
def test_user_repository_integration_save_and_retrieve()
def test_user_registration_workflow_completes()
```

## Continuous Testing

### Pre-commit Hooks
- **Run:** Unit tests, linting, type checking
- **Goal:** Prevent broken code from being committed
- **Tools:** pre-commit framework

### CI/CD Pipeline
- **On Push:** Run full test suite
- **Quality Gates:** Block deployment on test failures
- **Metrics:** Track coverage and quality trends

### Test Parallelization
- **Strategy:** Run tests in parallel
- **Benefit:** Faster feedback
- **Tools:** pytest-xdist

## Property-Based Testing

### Hypothesis Testing
- **Approach:** Generate test cases automatically
- **Benefit:** Find edge cases
- **Tool:** hypothesis
- **Example:**
  ```python
  from hypothesis import given, strategies as st
  
  @given(st.integers(), st.integers())
  def test_addition_commutative(a, b):
      assert add(a, b) == add(b, a)
  ```

## Mutation Testing

### Stryker-like Testing
- **Approach:** Introduce mutations to verify test quality
- **Benefit:** Measure test effectiveness
- **Tool:** mutmut (Python)
- **Goal:** High mutation score (>80%)

## Test Data Management

### Factory Pattern
- **Approach:** Use factories for test data
- **Benefit:** Consistent, maintainable test data
- **Tools:** factory_boy
- **Example:**
  ```python
  class UserFactory(factory.Factory):
      class Meta:
          model = User
      
      name = "Test User"
      email = factory.Sequence(lambda n: f"user{n}@test.com")
  
  # Usage
  user = UserFactory()
  admin_user = UserFactory(is_admin=True)
  ```

### Fixtures (pytest)
- **Approach:** Reusable test setup
- **Benefit:** Clean, modular test setup
- **Example:**
  ```python
  @pytest.fixture
  def test_user():
      return User(name="Test", email="test@example.com")
  
  def test_something(test_user):
      # test_user is available here
      assert test_user.name == "Test"
  ```

## Validation Rules for Trae IDE

1. **Test Coverage:** Enforce minimum 80% coverage
2. **Test Organization:** Follow pyramid structure
3. **Test Naming:** Use descriptive naming conventions
4. **Test Isolation:** Mock external dependencies
5. **Test Data:** Use factories/fixtures for consistency
6. **Quality Gates:** Block on test failures and low coverage
7. **Continuous Testing:** Integrate with CI/CD pipeline

## Examples from Study Materials

### Good Test Example (From Cosmic Python)
```python
def test_allocating_to_a_batch_reduces_available_quantity():
    # Arrange
    batch = Batch("batch-001", "SMALL-TABLE", 20, datetime.now())
    line = OrderLine("order-123", "SMALL-TABLE", 2)
    
    # Act
    batch.allocate(line)
    
    # Assert
    assert batch.available_quantity == 18
```

### Integration Test Example
```python
def test_repository_can_save_a_batch(session):
    # Arrange
    batch = Batch("batch-001", "RUSTY-SOAPDISH", 100, None)
    
    # Act
    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()
    
    # Assert
    rows = session.execute(
        "SELECT reference, sku, _purchased_quantity FROM batches"
    )
    assert list(rows) == [("batch-001", "RUSTY-SOAPDISH", 100)]
```

## References

- Test-Driven Development (TDD)
- Clean Architecture Testing Strategies
- SOLID Principles for Testable Code
- Study files: `/cosmic-python-book/README.md`
- Quality Metrics and Best Practices