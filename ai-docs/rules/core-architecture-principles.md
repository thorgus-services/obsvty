## Purpose
Structure code to support Hexagonal Architecture where application core depends only on abstract ports, and adapters implement them. Standardize port naming based on actor direction.

## Guidelines
Core must be completely isolated from infrastructure concerns:

```python
# GOOD: Domain model completely isolated
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

# BAD: Domain importing infrastructure packages
from sqlalchemy import Column, Integer  # ❌ Forbidden in core/
```

Primary (driving) ports — app is driven by external actor:
Naming: `*CommandPort`, `*QueryPort`
Test with: harnesses (pytest calling port directly)
Examples: `OrderCommandPort`, `UserQueryPort`

Secondary (driven) ports — app drives external system:
Naming: `*GatewayPort`, `*RepositoryPort`, `*PublisherPort`
Test with: mocks/fakes (e.g., `InMemoryOrderRepo`)
Examples: `PaymentGatewayPort`, `OrderRepositoryPort`

## Directory structure must enforce boundaries:
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models.py         # Immutable value objects and entities
│   ├── use_cases.py      # Pure functions implementing business rules
│   └── ports/            # Interfaces only (Protocols)
│       ├── order_ports.py
│       └── payment_ports.py
│
├── adapters/            # Implementations of core ports
│   ├── db/              # Database implementations
│   ├── api/             # API/handler implementations
│   └── external/        # Third-party service integrations
│
└── app.py               # Composition root for dependency injection

## Implementation example:

```python
# src/core/ports/order_ports.py
from typing import Protocol
from .models import Order, OrderId

class OrderCommandPort(Protocol):
    def create_order(self, order: Order) -> OrderId: ...
    def cancel_order(self, order_id: OrderId) -> None: ...


# src/adapters/db/order_repository.py
from src.core.ports.order_ports import OrderCommandPort

class PostgresOrderRepository(OrderCommandPort):
    def __init__(self, connection_pool):
        self.pool = connection_pool
    
    def create_order(self, order: Order) -> OrderId:
        # Database implementation details
```

## Anti-Patterns
❌ Domain/core objects importing infrastructure packages
❌ Naming ports `IService`, `IHandler` — too vague
❌ Using same port for reading and writing (violates CQS)
❌ Adapter calling another adapter directly (bypassing core ports)
❌ Hidden dependencies via service locator pattern