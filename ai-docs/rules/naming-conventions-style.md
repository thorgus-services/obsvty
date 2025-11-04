# Naming Conventions and Style Rules

**Based on:** Clean Code Principles, Python PEP8, Refactoring Best Practices
**Scope:** Naming conventions, code style, and expressiveness in Python

## Naming Conventions

### Classes and Interfaces
- **Rule:** `PascalCase` for classes and interfaces
- **Suffix Conventions:**
  - `Service` for domain services
  - `Repository` for data access patterns
  - `Adapter` for interface adapters
  - `Factory` for object creation patterns
  - `Strategy` for behavioral patterns
- **Examples:**
  - `OrderProcessingService` ✅
  - `UserRepository` ✅
  - `EmailNotificationAdapter` ✅
  - `PaymentStrategyFactory` ✅
  - `order_service` ❌ (snake_case)

### Methods and Functions
- **Rule:** `snake_case` for methods and functions
- **Rule:** Verb-based names that express action
- **Rule:** Names must reveal intention, not implementation
- **Examples:**
  - `calculate_order_total()` ✅
  - `validate_user_registration()` ✅
  - `process_data()` ❌ (vague)
  - `handle()` ❌ (unclear intention)

### Variables and Parameters
- **Rule:** `snake_case` for variables and parameters
- **Rule:** Descriptive names, no abbreviations
- **Rule:** Domain-specific value objects
- **Examples:**
  - `user_registration_date` ✅
  - `order_total_amount` ✅
  - `urd` ❌ (abbreviation)
  - `temp` ❌ (non-descriptive)
  - `Money` ✅ (value object)
  - `EmailAddress` ✅ (value object)

### Modules and Packages
- **Rule:** `snake_case` for module names
- **Rule:** Hierarchical structure reflecting responsibility
- **Rule:** No generic names like "utils" or "helpers"
- **Examples:**
  - `payment_processing.py` ✅
  - `user_authentication.py` ✅
  - `utils.py` ❌ (generic)
  - `helpers.py` ❌ (generic)

## Code Expressiveness Rules

### Method Length and Complexity
- **Rule:** Methods must be under 5 lines (Fowler's Rule of Five)
- **Rule:** Extract complex logic into well-named functions
- **Validation:** Automatic method length detection
- **Example:**
  ```python
  # ❌ Too long and complex
  def process_order(order):
      # 20 lines of validation, calculation, notification
      pass
  
  # ✅ Extracted into clear functions
  def process_order(order):
      validate_order(order)
      calculate_totals(order)
      notify_user(order)
  ```

### Comment Philosophy
- **Rule:** Comments only for "why", not "what" or "how"
- **Rule:** Code should be self-documenting through names
- **Rule:** Remove comments that become obsolete
- **Examples:**
  ```python
  # ❌ Bad comment (explains what)
  # Check if user is active
  if user.status == 'active':
  
  # ✅ Self-documenting code
  if user.is_active():
  
  # ✅ Good comment (explains why)
  # Using legacy API due to backward compatibility requirements
  result = legacy_api.call()
  ```

### Boolean Naming
- **Rule:** Boolean variables/methods should read like questions
- **Rule:** Prefix with "is", "has", "can", "should"
- **Examples:**
  - `is_active` ✅
  - `has_permission` ✅
  - `can_edit` ✅
  - `should_retry` ✅
  - `active` ❌ (not question-form)

## Python Specific Conventions

### Type Hints
- **Rule:** Type hints mandatory for public APIs
- **Rule:** Use Python 3.9+ style type annotations
- **Rule:** Generic types with `from typing import`
- **Examples:**
  ```python
  from typing import List, Dict, Optional
  
  def process_users(users: List[User]) -> Dict[str, int]:
      """Process list of users and return statistics."""
      return {"count": len(users)}
  ```

### Imports Organization
- **Rule:** Group imports: standard library, third-party, local
- **Rule:** Use `isort` for consistent import sorting
- **Rule:** Absolute imports preferred over relative
- **Example:**
  ```python
  # Standard library
  import os
  from typing import List, Dict
  
  # Third-party
  from sqlalchemy import create_engine
  import requests
  
  # Local modules
  from domain.models import User, Order
  from adapters.repository import UserRepository
  ```

### String Formatting
- **Rule:** Prefer f-strings over format() or % formatting
- **Rule:** Use descriptive variable names in f-strings
- **Examples:**
  ```python
  name = "John"
  age = 30
  
  # ✅ Good
  message = f"User {name} is {age} years old"
  
  # ❌ Avoid
  message = "User %s is %d years old" % (name, age)
  ```

## Validation Rules for Trae IDE

1. **Naming Consistency:** Automatic case style validation
2. **Method Length:** Flag methods > 5 lines for refactoring
3. **Comment Quality:** Detect explanatory vs. redundant comments
4. **Type Hint Coverage:** Check for missing type hints in public APIs
5. **Import Organization:** Validate import grouping and order
6. **Expressiveness:** Suggest better names for vague identifiers

## Examples from Study Materials

### Good Examples (From Cosmic Python)
```python
# domain/models.py
class Order:
    def __init__(self, order_id: str, items: List[OrderItem]):
        self.order_id = order_id
        self._items = items
    
    def calculate_total(self) -> Money:
        return sum(item.price for item in self._items)

# service_layer/services.py
def create_order(uow: UnitOfWork, order_data: OrderData) -> Order:
    """Create new order with validation and persistence."""
    validate_order_data(order_data)
    order = create_order_from_data(order_data)
    persist_order(uow, order)
    return order
```

### Bad Examples (To Avoid)
```python
# ❌ Vague naming
def process(data):
    # What kind of processing?
    pass

# ❌ Long method
def handle_user_request(request):
    # 15+ lines of validation, processing, response
    # Should be split into smaller functions
    pass

# ❌ Non-descriptive variables
def calc(x, y):
    # What are x and y?
    return x * y
```

## References

- PEP8: Python Style Guide
- Clean Code: Naming and Expressiveness
- Refactoring: Extract Method and Rename patterns
- Study files: `/refactoring-improving-the-design-of-existing-code-book/README.md`