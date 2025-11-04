# Project Structure Rule

**Based on:** Clean Architecture, Hexagonal Architecture, Package Principles
**Scope:** Project organization, module structure, and dependency management

## Core Project Structure

### Standard Python Project Layout
```
project-name/
├── src/                    # Source code (PEP 420)
│   └── project_name/       # Package name (underscore_case)
│       ├── __init__.py    # Package initialization
│       ├── __main__.py    # CLI entry point
│       ├── domain/        # Core business logic
│       │   ├── __init__.py
│       │   ├── entities.py
│       │   ├── value_objects.py
│       │   └── events.py
│       ├── application/    # Use cases and services
│       │   ├── __init__.py
│       │   ├── use_cases/
│       │   └── services/
│       ├── infrastructure/ # External implementations
│       │   ├── __init__.py
│       │   ├── persistence/
│       │   ├── messaging/
│       │   └── web/
│       └── interfaces/     # Entry points (optional)
│           ├── __init__.py
│           ├── cli/
│           └── web/
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── .github/               # GitHub workflows
├── docker/                # Docker configurations
├── requirements/          # Dependency management
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── pyproject.toml         # Modern Python config
├── setup.cfg             # Legacy config (if needed)
├── README.md
├── LICENSE
└── .gitignore
```

### Package Principles Application

#### Acyclic Dependencies Principle (ADP)
- **Rule:** No circular dependencies between packages
- **Detection:** Dependency graphs and import analysis
- **Enforcement:** Layered architecture with clear boundaries

#### Stable Dependencies Principle (SDP)
- **Rule:** Depend in direction of stability
- **Metric:** Instability metric (I = Ce / (Ce + Ca))
- **Goal:** Stable packages (low I) depend on stable packages

#### Stable Abstractions Principle (SAP)
- **Rule:** Stable packages should be abstract
- **Metric:** Abstractness metric (A = Na / Nc)
- **Goal:** Balance between stability and abstractness

## Clean Architecture Layers

### Domain Layer (Most Stable)
- **Location:** `src/project_name/domain/`
- **Dependencies:** None (pure business logic)
- **Contents:** Entities, Value Objects, Domain Events
- **Rules:** No external dependencies, pure Python

### Application Layer
- **Location:** `src/project_name/application/`
- **Dependencies:** Domain layer only
- **Contents:** Use Cases, Application Services
- **Rules:** Business orchestration, transaction boundaries

### Infrastructure Layer
- **Location:** `src/project_name/infrastructure/`
- **Dependencies:** Domain + Application layers
- **Contents:** Database implementations, External services
- **Rules:** Implement interfaces from inner layers

### Interfaces Layer (Optional)
- **Location:** `src/project_name/interfaces/`
- **Dependencies:** All inner layers
- **Contents:** Web controllers, CLI commands
- **Rules:** Thin adapters, no business logic

## Hexagonal Architecture Structure

### Ports and Adapters Pattern
```
project-name/
├── src/
│   └── project_name/
│       ├── domain/          # Core business
│       ├── application/     # Use cases
│       ├── ports/          # Interfaces (abstractions)
│       │   ├── __init__.py
│       │   ├── repository.py
│       │   └── messaging.py
│       └── adapters/       # Implementations
│           ├── __init__.py
│           ├── persistence/ # Database adapters
│           └── web/        # Web adapters
└── tests/
```

### Ports (Interfaces)
- **Definition:** Abstract interfaces for external systems
- **Location:** `ports/` directory
- **Examples:** Repository, MessageBus, EmailService interfaces

### Adapters (Implementations)
- **Definition:** Concrete implementations of ports
- **Location:** `adapters/` directory
- **Examples:** SQLRepository, SMTPEmailService, RedisMessageBus

## Dependency Management

### Modern Python Packaging
- **Tool:** pyproject.toml (PEP 518, PEP 621)
- **Benefits:** Standardized, tool-agnostic configuration
- **Example:**
  ```toml
  [build-system]
  requires = ["setuptools>=61.0", "wheel"]
  build-backend = "setuptools.build_meta"
  
  [project]
  name = "project-name"
  version = "0.1.0"
  description = "Project description"
  
  dependencies = [
      "requests>=2.28.0",
      "pydantic>=1.10.0",
  ]
  
  [project.optional-dependencies]
  dev = ["pytest>=7.0.0", "black", "mypy"]
  test = ["pytest", "pytest-cov"]
  ```

### Dependency Separation
- **Base Dependencies:** Core runtime requirements
- **Development Dependencies:** Testing, linting, formatting
- **Production Dependencies:** Only what's needed for runtime

## Module Organization Rules

### Module Size and Cohesion
- **Rule:** Modules should have single responsibility
- **Guideline:** 200-500 lines per module
- **Cohesion:** High internal cohesion, low external coupling

### Import Organization
- **Standard Order:**
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- **Grouping:** Alphabetical within each group
- **Example:**
  ```python
  # Standard library
  import os
  import sys
  from typing import Optional
  
  # Third-party
  import requests
  from pydantic import BaseModel
  
  # Local application
  from .domain import User
  from .services import UserService
  ```

### Public API Definition
- **Rule:** Explicitly define public API in `__init__.py`
- **Benefit:** Clear boundaries, controlled exposure
- **Example:**
  ```python
  # src/project_name/__init__.py
  from .domain import User, Product, Order
  from .services import UserService, ProductService
  from .ports import Repository, MessageBus
  
  __all__ = [
      'User', 'Product', 'Order',
      'UserService', 'ProductService',
      'Repository', 'MessageBus'
  ]
  ```

## Test Structure Alignment

### Mirror Production Structure
```
tests/
├── unit/
│   ├── domain/
│   │   ├── test_entities.py
│   │   └── test_value_objects.py
│   ├── application/
│   │   ├── test_use_cases.py
│   │   └── test_services.py
│   └── infrastructure/
│       └── test_adapters.py
├── integration/
│   ├── test_database_integration.py
│   └── test_api_integration.py
└── e2e/
    └── test_user_workflows.py
```

### Test Module Naming
- **Pattern:** `test_<module>_<component>.py`
- **Alignment:** Match production module structure
- **Example:** `test_domain_entities.py` for `domain/entities.py`

## Configuration Management

### Environment-based Configuration
- **Approach:** Different configs for dev, test, prod
- **Tools:** python-dotenv, pydantic-settings
- **Structure:**
  ```
  config/
  ├── __init__.py
  ├── base.py
  ├── development.py
  ├── testing.py
  └── production.py
  ```

### Configuration Loading
```python
# config/__init__.py
from .base import Settings

def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        from .production import ProductionSettings
        return ProductionSettings()
    elif env == "testing":
        from .testing import TestingSettings
        return TestingSettings()
    else:
        from .development import DevelopmentSettings
        return DevelopmentSettings()
```

## Documentation Structure

### Comprehensive Documentation
```
docs/
├── api/                    # API documentation
├── architecture/           # Architectural decisions
├── deployment/            # Deployment guides
├── development/           # Development setup
├── examples/              # Code examples
├── images/               # Diagrams and images
├── principles/           # Design principles
└── README.md             # Documentation root
```

### Architectural Decision Records (ADRs)
```
docs/architecture/decisions/
├── 0001-use-clean-architecture.md
├── 0002-hexagonal-ports-adapters.md
├── 0003-dependency-inversion.md
└── 0004-testing-strategy.md
```

## Tooling and Automation

### Development Environment
- **Editor Config:** `.editorconfig` for consistent formatting
- **Pre-commit Hooks:** `.pre-commit-config.yaml`
- **Docker:** `Dockerfile` and `docker-compose.yml`
- **Makefile:** Common development tasks

### CI/CD Configuration
- **GitHub Actions:** `.github/workflows/`
- **GitLab CI:** `.gitlab-ci.yml`
- **Jenkins:** `Jenkinsfile`

## Validation Rules for Trae IDE

1. **Structure Validation:** Verify Clean Architecture layers
2. **Dependency Validation:** Check for circular dependencies
3. **Import Validation:** Validate import order and grouping
4. **Package Validation:** Ensure proper `__init__.py` usage
5. **Test Structure:** Verify test mirroring production structure
6. **Configuration:** Validate environment-based configuration

## Examples from Study Materials

### Good Structure (From Cosmic Python)
```python
# Clean layered structure
src/
└── allocation/
    ├── domain/           # Entities, Value Objects
    ├── service_layer/    # Use Cases, Handlers
    ├── adapters/         # Repository implementations
    └── entrypoints/      # Web, CLI entry points
```

### Hexagonal Structure
```python
# Ports and Adapters
src/
└── ecommerce/
    ├── domain/          # Core business logic
    ├── ports/           # Repository, PaymentService interfaces
    └── adapters/        # SQLRepository, StripePaymentService
```

## References

- Clean Architecture by Robert C. Martin
- Hexagonal Architecture (Ports and Adapters)
- Package Principles (ADP, SDP, SAP)
- PEP 420 (Implicit Namespace Packages)
- Study files: `/the-hexagonal-architecture/README.md`
- Study files: `/cosmic-python-book/README.md`
- Study files: `/design-principles-and-design-patterns/README.md`