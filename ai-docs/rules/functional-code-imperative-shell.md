## Purpose
Enforce strict separation between pure functional core logic and imperative shell that handles side effects.

## Guidelines
Core functions must be:
- Pure (no I/O, no mutation of inputs, no time/random)
- Small (≤15 lines; ≤3 parameters)
- Named with clear verb + domain object
- Follow CQS: Queries (`calculate_total`) vs. Commands (`update_status`) — never both

Shell functions must be:
- Thin wrappers (≤25 lines) around core logic
- Responsible for: I/O, error translation, logging, retries
- Contain `try/except` blocks only — extracted into helpers like `execute_with_retry(fn, max_retries=3)`

Core must never contain:
- Database calls, HTTP requests, file operations
- Random number generation, current time usage
- Direct mutation of input parameters
- Global state access or modification

Shell must never contain:
- Business rules or domain logic
- Complex conditional workflows that belong in core
- Data transformation logic that could be pure functions

## Examples
✅ Core (pure):
```python
def calculate_total(order: Order, tax_rates: TaxTable) -> Money:
    subtotal = sum(item.price * item.qty for item in order.items)
    tax = subtotal * tax_rates.rate_for(order.region)
    return subtotal + tax
```

✅ Shell (side-effectful):
```python
def handle_create_order_request(request: OrderRequest) -> Response:
    try:
        order = Order.from_request(request)
        total = calculate_total(order, global_tax_table)
        persisted = order_repository.save(order.with_total(total))
        return Response.json(OrderDTO.from_model(persisted))
    except OrderValidationError as e:
        return Response.error(400, f"Invalid order: {e}")
```

## Exception handling:
- Domain exceptions defined in core (e.g., `OutOfStock`, `InvalidEmail`)
- Shell translates domain exceptions to appropriate response formats
- No exception handling in core functions (let exceptions propagate)

## Anti-Patterns
❌ Core function calling `requests.get()` or database operations
❌ Shell function containing business rules (e.g., "if user is premium, apply 10% off")
❌ Command function returning computed values (e.g., `save_user(user) -> UserDTO`)
❌ Direct mutation of input parameters in core functions
❌ Using global state or singletons in core logic
❌ Implementing retries or circuit breakers in core functions