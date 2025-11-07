## Purpose
Default to immutable, self-validating value objects in the Functional Core using pure Python standard library with no external dependencies.

## Guidelines
All core data classes must be immutable:
- Use `@dataclass(frozen=True)` for all value objects
- Validate invariants in `__post_init__` or dedicated factory methods
- Never expose mutable collections — convert to `tuple`, `frozenset` or return defensive copies

Prefer type-safe structures over primitive types:
- Use `dataclasses` and `typing.NamedTuple` over plain `dict`/`list` for domain models
- Leverage Python's type system for compile-time validation
- Use transformation methods that return new instances instead of mutation

Implementation patterns:
```python
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Tuple, FrozenSet

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str 
    
    def __post_init__(self):
        # Validate invariants
        if self.amount < 0:
            raise ValueError("Money cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be ISO 3-letter code")
    
    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def with_amount(self, new_amount: Decimal) -> "Money":
        """Return new instance with modified amount"""
        return Money(new_amount, self.currency)

@dataclass(frozen=True)
class ShoppingCart:
    items: Tuple[ShoppingItem, ...] = field(default_factory=tuple)
    customer_id: str | None = None
    
    def add_item(self, item: ShoppingItem) -> "ShoppingCart":
        """Return new cart with item added (no mutation)"""
        return ShoppingCart(
            items=(*self.items, item),
            customer_id=self.customer_id
        )
```

## Boundary considerations:
- Use Pydantic models ONLY at system boundaries (API inputs/outputs)
- Convert Pydantic models to immutable value objects immediately after validation
- Never pass Pydantic models into core domain logic

## Testing strategy:
- Test validation logic thoroughly in value object constructors
- Verify immutability by attempting to modify instances
- Test transformation methods produce new instances with expected changes

## Anti-Patterns
❌ `user.email = "new@ex.com"` — direct mutation of object state
❌ `def process(items: list): items.append(...)` — side effect on input parameter
❌ `{ "amount": 100, "currency": "USD" }` — untyped, mutable dictionary without validation
❌ `@dataclass class MutableValue: value: int` — mutable dataclass without `frozen=True`
❌ `def __init__(self, items=[]): self.items = items` — mutable default arguments
❌ `from pydantic import BaseModel` — external dependencies in functional core logic
❌ `cart.items.append(item)` — modifying internal collections directly
❌ Using primitive types where domain concepts exist (string for email, int for money)