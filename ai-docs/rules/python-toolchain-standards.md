## Purpose
Standardize Python toolchain configuration and workflow for consistent, secure, and maintainable codebases.

## Guidelines
Dependency management with Poetry:
- Define dependencies with precise version constraints
- Separate runtime, dev, and test dependencies
- Use poetry.lock for deterministic builds
- Example pyproject.toml:
```
  [tool.poetry.dependencies]
  python = "^3.13"
  pydantic-settings = "^2.12"
  sqlalchemy = {version = "^2.0", extras = ["asyncio"]}
  
  [tool.poetry.group.dev.dependencies]
  ruff = "^0.14"
  mypy = "^1.18"
  pytest = "^8.4"
```

Code formatting with Ruff:
- No imports inside functions except for optional dependencies
- Enforce consistent import ordering and grouping
- Disallow unused imports and variables
- Example ruff.toml:
```
  select = ["E", "F", "I", "B", "C4", "T20"]
  ignore = ["E501"]
  line-length = 88
  flake8-quotes.inline-quotes = "double"
  
  [lint.per-file-ignores]
  "__init__.py" = ["F401"]  # Allow unused imports in __init__ for namespace exports
```

Type checking with Mypy:
- Strict mode enabled for core packages
- Permissive mode for tests and infrastructure
- Type ignore only with justification comments
- Example mypy.ini:
```
  [mypy]
  strict = true
  warn_unused_configs = true
  disallow_any_generics = true
  check_untyped_defs = true
  
  [mypy-tests.*]
  strict = false
  disallow_untyped_defs = false
```

Security scanning with Bandit and Safety:
- Bandit configuration to check for common security issues:
```
  [bandit]
  skips = ["B101"]  # Skip assert checks in tests
  exclude_dirs = ["tests", "venv"]
```
- Safety checks in CI pipeline before deployment:
```bash
  poetry run safety check --full-report
```

## Testing with Pytest:
- Test structure matching source layout
- Fixtures for test setup/teardown
- Parametrized tests for edge cases
- Example pytest.ini:
```
  [tool:pytest]
  python_files = test_*.py
  testpaths = tests/unit tests/integration
  addopts = -v --cov=src --cov-report=html --strict-markers
  markers =
      unit: Unit tests (no external dependencies)
      integration: Integration tests (with real/fake adapters)
      slow: Tests that take more than 1 second
```

## Task automation with Tox:
- Standardized environments for linting, testing, type checking
- Example tox.ini:
```
  [tox]
  envlist = lint, type, unit
  
  [testenv:lint]
  deps = ruff
  commands = ruff check src tests
  
  [testenv:type]
  deps = mypy
  commands = mypy src
  
  [testenv:unit]
  deps = pytest pytest-cov
  commands = pytest tests/unit
```

## Configuration with Pydantic Settings:
- Single configuration source with validation
- Environment variable overrides
- Different settings for environments:
```python
  from pydantic_settings import BaseSettings
  
  class AppSettings(BaseSettings):
      database_url: str
      debug: bool = False
      redis_url: str = "redis://localhost:6379"
      
      model_config = SettingsConfigDict(env_prefix="APP_")
  
  settings = AppSettings()
```

## Validation pipeline in CI:
1. Ruff format and lint check
2. Mypy type checking
3. Bandit security scan
4. Safety dependency vulnerability check
5. Pytest with coverage requirements (≥80% in core)
6. Build and package verification with Poetry

## Anti-Patterns
❌ Mixing tabs and spaces (enforced by Ruff)
❌ Unversioned dependencies in pyproject.toml
❌ Type ignores without justification comments
❌ Security vulnerabilities with known CVEs
❌ Tests without assertions or with sleep() calls
❌ Configuration values hardcoded in source files
❌ Different formatting rules between developer machines
❌ Manual dependency installation outside Poetry workflow