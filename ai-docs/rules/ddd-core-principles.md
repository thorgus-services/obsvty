## Purpose
Establish foundational Domain-Driven Design principles for Python backend systems with strict domain model purity and separation of concerns.

## Guidelines
Domain layer must be completely isolated from infrastructure:
```python
# GOOD: Pure domain model with no external dependencies
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int
    
    def __post_init__(self):
        if self.qty <= 0:
            raise ValueError("Quantity must be positive")


# BAD: Domain importing infrastructure packages
from sqlalchemy import Column, String  # ❌ Forbidden in domain/
```

Business rules must reside in domain objects, not services:
```python
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date] = None):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()
    
    def allocate(self, line: OrderLine) -> bool:
        if self.can_allocate(line):
            self._allocations.add(line)
            return True
        return False
    
    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
```

Domain exceptions must be specific and contextual:
```python
class OutOfStock(DomainException):
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"Out of stock for sku {sku}")


class InvalidOrderState(DomainException):
    def __init__(self, order_id: str, current_state: str, attempted_action: str):
        super().__init__(
            f"Order {order_id} in state {current_state} cannot perform {attempted_action}"
        )
```

## Layered architecture enforcement:
| Layer           | Responsibilities                          | Dependencies Allowed       |
|-----------------|--------------------------------------------|----------------------------|
| domain/         | Entities, value objects, domain services   | None (pure Python)         |
| application/    | Use cases, DTOs, ports (interfaces)        | domain/ only               |
| infrastructure/ | Database, APIs, external services          | domain/, application/      |
| interfaces/     | API endpoints, CLI commands, event handlers| application/, infrastructure|

Dependency flow must be strictly unidirectional: interfaces → infrastructure → application → domain

## Anti-Patterns
❌ Anemic Domain Model (entities with only getters/setters)
❌ Primitive Obsession (using raw strings/ints instead of value objects)
❌ Domain objects with infrastructure concerns (`.save()` methods on entities)
❌ Leaky abstractions (domain objects exposing internal state)
❌ God objects (classes with multiple responsibilities violating SRP)
❌ Circular dependencies between layers