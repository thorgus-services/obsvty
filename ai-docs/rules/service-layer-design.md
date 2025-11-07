## Purpose
Structure service layer as the orchestration layer between domain logic and infrastructure concerns with transaction boundaries.

## Guidelines
Service layer responsibilities:
- Transaction management (via Unit of Work)
- Input validation (not business rules)
- Calling domain logic
- Handling domain exceptions
- Publishing domain events

Service functions must be stateless or use explicit state:
```python
# GOOD: Stateful service as class with explicit dependencies
class OrderService:
    def __init__(self, uow: UnitOfWork, notifications: NotificationService):
        self.uow = uow
        self.notifications = notifications
    
    def create_order(self, customer_id: str, items: List[OrderItem]) -> OrderId:
        with self.uow:
            order = Order.create(customer_id, items)
            order_id = self.uow.orders.add(order)
            self.uow.commit()
            self.notifications.send(
                Notification(order_id, "Order created successfully")
            )
            return order_id
```

Function signatures must use primitive types or DTOs:
```python
# GOOD: Service interface uses primitives/DTOs
def allocate(order_id: str, sku: str, qty: int, uow: UnitOfWork) -> str:
    ...

# BAD: Service interface using domain objects directly
def allocate(order: Order, batch: Batch, uow: UnitOfWork):
    ...
```

## Separation of concerns:
| Layer           | Responsibilities                          | Dependencies Allowed       |
|-----------------|--------------------------------------------|----------------------------|
| Domain          | Business rules, entities, value objects    | None (pure Python)         |
| Service Layer   | Use case orchestration, transaction boundaries | Domain only           |
| Infrastructure  | Database, APIs, external services          | Domain, Service Layer      |
| Entry Points    | HTTP handlers, CLI commands, consumers     | Service Layer, Infrastructure|

## Entry points must be "thin":
```python
# GOOD: Thin FastAPI endpoint
@app.post("/orders")
async def create_order_endpoint(request: OrderRequest):
    try:
        order_id = order_service.create_order(
            request.customer_id,
            [OrderItem(item.sku, item.qty) for item in request.items]
        )
        return {"order_id": order_id}, 201
    except OutOfStock as e:
        return {"error": f"Out of stock for sku {e.sku}"}, 400
    except InvalidOrder as e:
        return {"error": str(e)}, 400
```

## Dependency injection:
- Explicit dependency injection required for all services
- Never use global state or service locator
- Composition root handles all wiring

## Testing strategy:
- Service layer tests use fake repositories/UoW
- Tests validate business outcomes, not implementation details
- Edge-to-edge tests for complete workflow validation

## Anti-Patterns
❌ Anemic Domain Model (moving business logic to services)
❌ Fat controllers (entry points containing business logic)
❌ Service locator (hidden dependencies in service layer)
❌ Transactional scripts (services with complex conditional logic)
❌ Services returning domain entities to entry points
❌ Implicit dependencies (get_current_uow() instead of explicit injection)