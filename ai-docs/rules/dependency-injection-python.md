## Purpose
Implement proper dependency injection patterns in Python to maintain clean architecture boundaries and testability.

## Guidelines
Domain layer owns all interfaces:
```python
# domain/notifications.py
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    order_id: str
    message: str


class NotificationService(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> bool:
        pass
```

Infrastructure implements domain interfaces:
```python
# infrastructure/email_notifications.py
from domain.notifications import NotificationService, Notification


class EmailNotificationService(NotificationService):
    def __init__(self, smtp_server: str, port: int = 587):
        self.smtp_server = smtp_server
        self.port = port
    
    def send(self, notification: Notification) -> bool:
        # Implementation details
        return True
```

Composition root must be single entrypoint:
```python
# bootstrap.py
def bootstrap(
    database_url: str = settings.DATABASE_URL,
    smtp_server: str = settings.SMTP_SERVER,
    redis_url: str = settings.REDIS_URL
) -> MessageBus:
    # Create infrastructure dependencies
    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine)
    redis_client = redis.from_url(redis_url)
    
    # Create adapters
    uow = SqlAlchemyUnitOfWork(session_factory)
    notifications = EmailNotificationService(smtp_server)
    event_publisher = RedisEventPublisher(redis_client)
    
    # Wire dependencies
    dependencies = {
        "uow": uow,
        "notifications": notifications,
        "event_publisher": event_publisher
    }
    
    # Inject into handlers
    injected_handlers = {
        command_type: partial(handler, **dependencies)
        for command_type, handler in COMMAND_HANDLERS.items()
    }
    
    return MessageBus(injected_handlers)
```

Adapter pattern implementation:
```python
# infrastructure/pubsub.py
class RedisEventPublisher(EventPublisher):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def publish(self, channel: str, event: DomainEvent):
        self.redis.publish(channel, json.dumps(asdict(event)))
```

Fake adapters required for testing:
```python
# tests/fakes.py
class FakeNotificationService(NotificationService):
    def __init__(self):
        self.sent = []
    
    def send(self, notification: Notification) -> bool:
        self.sent.append(notification)
        return True
```

## DI techniques in Python:
- Use `functools.partial` for simple function injection
- Use handler classes for complex dependencies
- Use parameter objects for related dependencies
- Never use service locator or global state

```python
# GOOD: Handler class with explicit dependencies
class AllocateHandler:
    def __init__(self, uow: UnitOfWork, notifications: NotificationService):
        self.uow = uow
        self.notifications = notifications
    
    def __call__(self, command: AllocateCommand):
        with self.uow:
            batch_ref = allocate(command.order_id, command.sku, command.qty, self.uow)
            self.uow.commit()
            self.notifications.send(
                Notification(command.order_id, f"Allocated to {batch_ref}")
            )
```

## Testing strategy:
- Unit tests use fake dependencies only
- Integration tests use real dependencies with test containers
- Bootstrap must be tested with different configurations

## Anti-Patterns
❌ Service locator pattern (hidden dependencies)
❌ Global state (singletons, module-level variables)
❌ Concrete implementations in domain layer
❌ Hidden dependencies via `mock.patch` as primary testing strategy
❌ Direct instantiation of infrastructure objects outside bootstrap
❌ Using dependency injection frameworks that obscure dependency flow