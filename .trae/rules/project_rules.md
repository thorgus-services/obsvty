# Python Backend Development Rules for Trae IDE

**Based on:** Clean Architecture, Hexagonal Architecture, SOLID Principles, TDD, Cosmic Python  
**Scope:** Project structure, development workflow, code quality, and IDE validation for Python backend

---

## 1. Project Structure (Ports & Adapters + Clean Layers)

### Standard Structure
```
backend-project/
├── src/
│   └── project_name/              # PEP 420 package
│       ├── __init__.py            # Public API (`__all__`)
│       ├── __main__.py            # CLI entrypoint (`python -m project_name`)
│       ├── domain/                # Pure business logic (no deps)
│       │   ├── __init__.py
│       │   ├── entities.py
│       │   ├── value_objects.py
│       │   ├── events.py
│       │   └── exceptions.py
│       ├── ports/                 # Abstract interfaces (contracts)
│       │   ├── __init__.py
│       │   ├── repository.py      # e.g., `UserRepository(Protocol)`
│       │   └── messaging.py       # e.g., `MessageBus(Protocol)`
│       ├── use_cases/             # Application logic (orchestration)
│       │   ├── __init__.py
│       │   ├── create_user.py
│       │   └── unit_of_work.py
│       ├── adapters/              # Concrete implementations
│       │   ├── __init__.py
│       │   ├── persistence/       # e.g., SQLAlchemy, Redis
│       │   ├── messaging/         # e.g., Kafka, SMTP
│       │   └── web/               # e.g., FastAPI routes
│       └── main.py                # Composition Root (DI bootstrap)
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   └── use_cases/
│   ├── integration/
│   │   └── adapters/
│   └── e2e/
├── tasks.py                       # invoke commands
├── pyproject.toml                 # Poetry config
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── README.md
└── .pre-commit-config.yaml
```

### Layer Dependency Rules (DIP Enforcement)
- ✅ Allowed: `adapters` → `ports` → `use_cases` → `domain`
- ❌ Forbidden:  
  - `domain` imports anything outside itself  
  - `use_cases` depends on concrete adapters  
  - Circular dependencies between any layers

> **Trae Validation:** Block commits that violate dependency direction.

---

## 2. Dependency & Tooling Configuration

### Use Poetry for Dependency Management
```toml
# pyproject.toml
[tool.poetry]
name = "backend-project"
version = "0.1.0"
description = "Python backend with Hexagonal Architecture"
authors = ["Your Name <you@example.com>"]
packages = [{ include = "project_name", from = "src" }]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.100.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
ruff = "^0.4"
mypy = "^1.9"
invoke = "^2.0"
pytest-cov = "^4.0"
testcontainers = "^4.0"
factory-boy = "^3.3"
```

### Use `ruff` for Linting & Formatting
- Replaces `black`, `flake8`, `isort`
- **Rule:** Format on save with `ruff format`
- **Rule:** Lint with `ruff check --select ALL`

Example `ruff.toml` (optional, but recommended):
```toml
line-length = 88
target-version = "py311"
```

### Use `invoke` for Development Tasks
```python
# tasks.py
from invoke import task

@task
def test(c):
    c.run("pytest --cov=src --cov-fail-under=80")

@task
def lint(c):
    c.run("ruff check src tests")
    c.run("ruff format --check src tests")

@task
def typecheck(c):
    c.run("mypy src")

@task
def up(c):
    c.run("docker-compose up -d")
```

> **Trae Integration:** Suggest `invoke` tasks in terminal autocomplete.

---

## 3. Testing Strategy (Test Pyramid + TDD)

### Test Distribution
| Type        | Coverage | Speed     | Scope                     |
|-------------|----------|-----------|---------------------------|
| Unit        | 70–80%   | <100ms    | Domain + Use Cases (mocked ports) |
| Integration | 15–20%   | Seconds   | Adapters + real dependencies (DB, queues) |
| E2E         | 5–10%    | Minutes   | Full user workflows |

### Test Structure & Naming
- Mirror source: `tests/unit/domain/test_entities.py`
- Unit: `test_<behavior>()`
- Integration: `test_<component>_integration()`
- E2E: `test_<workflow>_workflow()`

### TDD & Isolation
- Write unit tests **before** implementation (Red → Green → Refactor)
- **Mock all ports** in unit tests (using `unittest.mock` or `pytest-mock`)
- Use **testcontainers** for integration tests with real DBs

### Quality Gates
- **80%+ line coverage** (enforced by `pytest-cov`)
- **100% coverage** for critical domain logic
- **mypy --strict** must pass
- **ruff check** must pass
- **No method > 10 lines** (per refactoring rules)

> **Trae Validation:** Fail commits if coverage < 80% or type/lint errors exist.

---

## 4. Code Quality & Refactoring Rules

### SOLID + Clean Code
- **SRP**: Max 3 responsibilities per class; methods ≤ 10 lines
- **OCP**: Extend via interfaces (`ports/`), not modification
- **LSP**: All adapters must satisfy port contracts
- **ISP**: Ports must be role-specific (e.g., `ReadRepository`, `WriteRepository`)
- **DIP**: Inner layers never import outer layers

### Refactoring Triggers
- ❌ Code duplication (refactor at 3rd occurrence)
- ❌ Methods > 10 lines → extract
- ❌ Classes with >3 concerns → split
- ❌ Complex conditionals → use Strategy/Polymorphism

### Naming & Structure
- Modules: 200–500 lines, single responsibility
- Imports: stdlib → third-party → local (alphabetical)
- Public API: Define `__all__` in `src/project_name/__init__.py`

---

## 5. IDE & Trae Validation Rules

| Rule | Validation |
|------|------------|
| **Layer Compliance** | Block `infrastructure` → `domain` imports |
| **Type Safety** | Enforce `mypy --strict` |
| **Test Coverage** | ≥80% line coverage; 100% in `domain/` |
| **Code Style** | Auto-format with `ruff format`; lint with `ruff check` |
| **Test Isolation** | Unit tests must mock all `ports/` |
| **Refactoring Guardrails** | Flag methods >10 lines, classes >3 responsibilities |
| **Duplication** | Detect structural/semantic duplication |
| **Dependency Cycles** | Block circular imports (ADP enforcement) |

---

## 6. References

- **Architecture**:  
  - *Clean Architecture* (R. Martin)  
  - *Cosmic Python* (Harry Percival)  
  - Hexagonal Architecture (Alistair Cockburn)
- **Testing**:  
  - TDD (Kent Beck)  
  - Test Pyramid (Mike Cohn)
- **Quality**:  
  - SOLID Principles  
  - Refactoring (Martin Fowler)