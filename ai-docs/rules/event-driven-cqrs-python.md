## Purpose
Implement event-driven architecture and CQRS patterns for scalable, maintainable Python systems with eventual consistency.

## Guidelines
Command-Query Separation:
Commands must:
- Use imperative naming (CreateOrder, CancelOrder)
- Modify only one aggregate
- Return no domain data (only success/failure status or IDs)
- Be processed synchronously

Queries must:
- Use noun-based naming (GetOrder, ListOrders)
- Be side-effect free
- Return DTOs or primitive data structures only
- Be optimized for read performance

API endpoints must follow separation:
```python
# POST endpoint (command)
@app.post("/orders")
async def create_order(command: CreateOrderCommand):
    order_id = message_bus.handle(command)
    return {"order_id": order_id}, 201  # No domain data

# GET endpoint (query)
@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> OrderDTO:
    return order_queries.get_order(order_id)  # Read model only
```

Domain events must be immutable:
```python
@dataclass(frozen=True)
class OrderCreated:
    order_id: str
    customer_id: str
    items: Tuple[OrderItem, ...]
    created_at: datetime
    
    def __post_init__(self):
        # Validate invariants
        if not self.items:
            raise ValueError("Order must have at least one item")
```

Message bus implementation:
```python
class MessageBus:
    def __init__(
        self,
        command_handlers: Dict[Type, Callable],
        event_handlers: Dict[Type, List[Callable]],
        uow: UnitOfWork
    ):
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
        self.uow = uow
    
    def handle_command(self, command: Command) -> Any:
        handler = self.command_handlers[type(command)]
        return handler(command)
    
    def handle_events(self, events: List[DomainEvent]) -> None:
        for event in events:
            for handler in self.event_handlers.get(type(event), []):
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Event handler failed for {type(event).__name__}: {e}")
                    # Continue processing other handlers
```

## Read model implementation:
- Read models must be denormalized for query performance
- Update via event handlers after transaction commit
- Multiple read models allowed for different query patterns

```python
def update_order_read_model(event: OrderCreated):
    with read_model_engine.begin() as conn:
        conn.execute(
            "INSERT INTO order_view (order_id, customer_id, total_amount, status) "
            "VALUES (:order_id, :customer_id, :total_amount, :status)",
            {
                "order_id": event.order_id,
                "customer_id": event.customer_id,
                "total_amount": calculate_total(event.items),
                "status": "CREATED"
            }
        )
```

## Transactional boundaries:
```python
with self.uow:
    result = command_handler(command)
    domain_events = self.uow.collect_new_events()
    self.uow.commit()

# Events processed after commit for eventual consistency
for event in domain_events:
    self.message_bus.handle_events([event])
```

## Testing requirements:
- Command handlers tested with unit tests and fake UoW
- Event handlers tested in isolation with fake dependencies
- End-to-end tests verify eventual consistency
- Idempotency tests for all event handlers

## Anti-Patterns
❌ Returning domain entities from queries
❌ Commands that return data (violates CQS)
❌ Synchronous HTTP calls between services (use events instead)
❌ Event handlers with side effects on write model
❌ Fat events containing full entity state
❌ Processing events before transaction commit
❌ Using synchronous event processing for cross-service communication