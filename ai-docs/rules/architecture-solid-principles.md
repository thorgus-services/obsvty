# Architecture and SOLID Principles Rule

**Based on:** Cosmic Python, Design Principles, Hexagonal Architecture
**Scope:** Python project structure, dependency management, and SOLID compliance

## Project Structure Template

```
project/
├── domain/              # Pure domain model (no external dependencies)
│   ├── model.py        # Entities and value objects
│   ├── events.py       # Domain events
│   └── exceptions.py   # Domain exceptions
├── service_layer/      # Use cases and orchestration
│   ├── services.py     # Service functions
│   └── unit_of_work.py # Unit of Work pattern
├── adapters/           # Concrete implementations
│   ├── repository.py   # Repositories (SQLAlchemy, etc.)
│   └── notifications.py # Notification adapters
├── entrypoints/        # Entry points
│   ├── api.py         # Flask/FastAPI endpoints
│   └── cli.py         # Command line interface
└── bootstrap.py        # Composition Root (Dependency Injection)
```

## SOLID Principles Enforcement

### Single Responsibility Principle (SRP)
- **Rule:** Classes must have maximum 3 cohesive responsibilities
- **Rule:** Methods must be under 5 lines (Fowler's Rule of Five)
- **Validation:** Trae IDE should detect "God Classes" with >3 responsibilities
- **Example:** Split `UserManager` into `UserValidator`, `UserRepository`, `UserNotifier`

### Open Closed Principle (OCP)
- **Rule:** Extend functionality through abstractions, not modification
- **Patterns:** Strategy, Factory, Decorator patterns for variation
- **Validation:** Detect when new features require modifying existing code
- **Example:** Add new payment method via `PaymentStrategy` interface

### Liskov Substitution Principle (LSP)
- **Rule:** Subclasses must be substitutable for base classes
- **Validation:** Contract testing for polymorphic behavior
- **Example:** `DatabaseUserRepository` and `InMemoryUserRepository` both implement `UserRepository`

### Interface Segregation Principle (ISP)
- **Rule:** Multiple client-specific interfaces over one general interface
- **Validation:** Detect "fat interfaces" with unrelated methods
- **Example:** Split `DataService` into `DataReader` and `DataWriter`

### Dependency Inversion Principle (DIP)
- **Rule:** Depend on abstractions, not concrete implementations
- **Rule:** Domain must not know about infrastructure
- **Validation:** Detect concrete dependencies in domain layer
- **Example:** `OrderService` depends on `OrderRepository` interface, not `SqlOrderRepository`

## Package Principles

### Acyclic Dependencies Principle (ADP)
- **Rule:** No dependency cycles between packages/modules
- **Tooling:** ArchUnit or custom cycle detection
- **Validation:** Automatic cycle detection in dependency graph

### Stable Dependencies Principle (SDP)
- **Rule:** Depend in the direction of stability
- **Metric:** Instability (I) = Fan-out / (Fan-in + Fan-out)
- **Target:** I < 0.5 for stable packages

### Stable Abstractions Principle (SAP)
- **Rule:** Stable packages should be abstract
- **Metric:** Abstractness (A) = Abstract elements / Total elements
- **Target:** A ≈ I for main sequence

## Implementation Examples

### Domain Model (Pure)
```python
# domain/model.py
class Order:
    def __init__(self, order_id: str, items: List[OrderItem]):
        self.order_id = order_id
        self._items = items
    
    @property
    def total_amount(self) -> Money:
        return sum(item.price for item in self._items)
```

### Service Layer
```python
# service_layer/services.py
def create_order(
    uow: UnitOfWork,
    order_id: str,
    items: List[OrderItem]
) -> Order:
    with uow:
        order = Order(order_id, items)
        uow.orders.add(order)
        uow.commit()
        uow.publish(OrderCreated(order_id, order.total_amount))
    return order
```

### Dependency Injection
```python
# bootstrap.py
def bootstrap() -> ServiceContainer:
    session = create_session()
    uow = SqlAlchemyUnitOfWork(session)
    order_repo = SqlAlchemyOrderRepository(session)
    
    return {
        'uow': uow,
        'order_repo': order_repo
    }
```

## Validation Rules for Trae IDE

1. **Dependency Direction:** Domain → Interfaces → Infrastructure
2. **No Concrete Dependencies in Domain:** Only abstractions
3. **Cycle Detection:** Automatic package dependency analysis
4. **SRP Compliance:** Method length and class responsibility checks
5. **Interface Cohesion:** ISP validation for interface design

## References

- Cosmic Python: Clean Architecture with Python
- Design Principles: SOLID and Package Principles
- Hexagonal Architecture: Ports and Adapters
- Study files: `/design-principles-and-design-patterns/README.md`