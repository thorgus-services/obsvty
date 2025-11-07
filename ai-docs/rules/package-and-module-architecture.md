## Purpose
Apply package architecture principles for maintainable, scalable Python projects with clear dependency boundaries.

## Guidelines
Package dependency rules:
- Dependencies must flow inward: interfaces → application → domain
- No circular dependencies between packages
- Stable packages (less likely to change) should not depend on unstable packages

Recommended package structure:
src/
├── domain/          # Most stable package
│   ├── models/      # Entities, value objects (immutable)
│   ├── exceptions/  # Domain-specific exceptions
│   └── services/    # Pure domain services (functions preferred)
├── application/     # Use cases, DTOs, ports (interfaces)
│   ├── use_cases/
│   ├── dto/
│   └── ports/
├── infrastructure/  # External integrations
│   ├── database/
│   ├── external_services/
│   └── messaging/
└── interfaces/      # API endpoints, CLI commands, event handlers
    ├── api/
    ├── cli/
    └── consumers/

Evolution strategy:
- Early stage (prototyping): Prioritize CCP (Common Closure Principle)
- Mature stage (production): Prioritize REP/CRP (Reuse/Release and Common Reuse)

## Python-specific implementation:
- Use namespaces over deeply nested packages
- Type hints for package boundaries with TYPE_CHECKING guards
- Lazy imports for optional dependencies:
```python
  def send_email(recipient: str, message: str) -> bool:
      try:
          import smtplib  # Lazy import for optional dependency
          # Implementation
      except ImportError:
          logger.warning("smtplib not available")
          return False
```

## Dependency validation:
- Implement package dependency tests
- Track stability metrics over time:
  * Afferent Coupling (Ca): Number of packages depending on this package
  * Efferent Coupling (Ce): Number of packages this package depends on
  * Instability (I): Ce / (Ca + Ce) - should be low for core packages

## Anti-Patterns
❌ Utility packages: No `utils/`, `helpers/`, or `common/` packages with random utilities
❌ God packages: No package with >20 files without sub-packages
❌ Circular dependencies between packages
❌ Volatility clusters: Unstable classes grouped with stable classes
❌ Deep nesting that makes imports verbose and complex
❌ Concrete implementations in domain layer
❌ Infrastructure concerns leaking into application or domain layers