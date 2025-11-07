## Purpose
Implement domain entities, value objects, and aggregates following Python-specific DDD practices with immutability and behavior-rich design.

## Guidelines
Entities must:
- Have explicit identity (UUID preferred)
- Encapsulate state-changing behavior
- Implement proper equality based on identity
- Use private attributes with public methods for state changes

Value objects must:
- Be immutable with `@dataclass(frozen=True)`
- Validate invariants in constructor
- Implement structural equality
- Provide transformation methods returning new instances

```python
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
    
    def __post_init__(self):
        object.__setattr__(self, 'amount', self.amount.quantize(Decimal('0.01')))
        if self.amount < 0:
            raise ValueError("Money cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be ISO 3-letter code")
    
    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

Aggregate boundaries must:
- Have exactly one aggregate root
- Enforce all invariants within the boundary
- Allow external references only to the root
- Return only DTOs or primitive types from root methods

```python
class Order(AggregateRoot):
    def __init__(self, order_id: OrderId, lines: List[OrderLine]):
        self._id = order_id
        self._lines = lines
        self._status = OrderStatus.PENDING
        self._events = []
    
    def add_line(self, line: OrderLine) -> None:
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderState(self._id, self._status, "add_line")
        self._lines.append(line)
        self._record_event(OrderLineAdded(self._id, line))
    
    def collect_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
    
    def _record_event(self, event: DomainEvent) -> None:
        self._events.append(event)
```

## Collection handling:
- Never expose mutable collections directly
- Return defensive copies or immutable collections (tuple, frozenset)
- Use private collections with controlled access methods

## Testing requirements:
- Test domain behavior, not implementation details
- 100% testable without infrastructure
- Express tests in business language

```python
def test_order_cannot_be_modified_after_shipment():
    order = OrderFactory.create_with_lines(3)
    order.ship()
    
    with pytest.raises(InvalidOrderState):
        order.add_line(OrderLineFactory())
```

## Anti-Patterns
❌ Public setters on entities (order.status = "shipped")
❌ Mutable value objects without validation
❌ Exposing internal collections (order.lines.append(new_line))
❌ Aggregate roots with public attributes
❌ Domain objects importing infrastructure packages
❌ Using Python properties for complex business logic