## Purpose
Apply SOLID principles effectively in Python OOP codebases with concrete implementation patterns and Python-specific idioms.

## Guidelines
Single Responsibility Principle implementation:
- Functions ≤15 lines, classes ≤5 public methods
- Name classes with single concern (avoid "and", "or", "manager")
- Extract cross-cutting concerns via decorators or composition:
```python
  # GOOD: SRP via composition
  class OrderProcessor:
      def __init__(self, calculator: OrderCalculator, repository: OrderRepository):
          self.calculator = calculator
          self.repository = repository
  
  # GOOD: Decorator for cross-cutting concern
  def log_execution(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
          logger.info(f"Executing {func.__name__}")
          return func(*args, **kwargs)
      return wrapper
```

Open/Closed Principle in Python:
- Prefer composition over inheritance
- Use protocols/ABCs for abstraction boundaries
- Strategy pattern for variant behaviors:
```python
  from typing import Protocol
  
  class TaxStrategy(Protocol):
      def calculate(self, amount: Decimal) -> Decimal: ...
  
  class IcmsStrategy:
      def calculate(self, amount: Decimal) -> Decimal:
          return amount * Decimal("0.17")
  
  class OrderService:
      def __init__(self, tax_strategy: TaxStrategy):
          self.tax_strategy = tax_strategy
```

Liskov Substitution Principle safeguards:
- Never strengthen preconditions in subclasses
- Never weaken postconditions in subclasses
- Avoid isinstance() checks in domain code:
```python
  # BAD: Violates LSP
  if isinstance(payment, CreditCard):
      payment.process_card()
  elif isinstance(payment, Pix):
      payment.process_pix()
  
  # GOOD: Polymorphic interface
  payment.process()  # All implementations honor same contract
```

Interface Segregation in Python:
- Create role-based protocols instead of fat interfaces
- Use structural subtyping (duck typing) with protocols:
```python
  from typing import Protocol
  
  class OrderQueryService(Protocol):
      def get_order(self, order_id: str) -> OrderDTO: ...
  
  class OrderCommandService(Protocol):
      def create_order(self, request: CreateOrderRequest) -> OrderId: ...
  
  # Implementation can satisfy multiple protocols
  class OrderService(OrderQueryService, OrderCommandService):
      ...
```

Dependency Inversion implementation:
- Core owns interfaces (protocols), infrastructure implements them
- Explicit dependency injection via constructor or function parameters
- Composition root in bootstrap module:
```python
  # domain/ports.py
  class NotificationService(Protocol):
      def send(self, message: str) -> bool: ...
  
  # bootstrap.py
  def bootstrap() -> Application:
      email_service = EmailNotificationService(smtp_server=settings.SMTP_SERVER)
      order_service = OrderService(notifications=email_service)
      return Application(order_service=order_service)
```

## Testing strategy for SOLID code:
- Test behavior, not implementation
- Contract tests for all polymorphic implementations
- Test components in isolation with fake dependencies
- No more than 2 test doubles per test

## Anti-Patterns
❌ Classes with >3 reasons to change
❌ isinstance() checks outside composition root
❌ Base classes with empty methods ("I don't need this method" pattern)
❌ Concrete dependencies instantiated inside domain classes
❌ Interfaces with methods that some clients don't use
❌ Type checking for flow control in business logic
❌ "Jack of all trades" utility classes with mixed concerns