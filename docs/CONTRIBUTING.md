# Contributing to Obsvty

Thank you for your interest in contributing to **Obsvty**! We welcome contributions from the community to help build a smarter, privacy-first observability platform. This guide will help you get started and ensure a smooth contribution process.

---

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [License](#license)

---

## Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md) to foster a welcoming and respectful community.

---

## How to Contribute

### Reporting Bugs
- Use [GitHub Issues](https://github.com/thorgus-services/obsvty/issues) to report bugs.
- Provide clear steps to reproduce, expected behavior, and screenshots/logs if possible.

### Suggesting Enhancements
- Open an issue for feature requests or improvements.
- Describe the motivation, use case, and potential implementation ideas.

### Submitting Pull Requests
1. Fork the repository and create your branch from `main`.
2. Follow the [Development Setup](#development-setup) below.
3. Write clear, concise commit messages.
4. Ensure your code passes all tests and linters.
5. Submit a pull request with a detailed description of your changes.
6. Reference related issues in your PR description.

---

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thorgus-services/obsvty.git
   cd obsvty
   ```
2. **Install dependencies:**
   ```bash
   poetry install
   ```
3. **Run the application:**
   ```bash
   docker-compose up
   ```
4. **Run tests and checks:**
   ```bash
   poetry run invoke test
   poetry run invoke lint
   poetry run invoke typecheck
   ```

---

## Project Structure

Obsvty follows Clean Architecture and Hexagonal Architecture principles. Key directories:
- `src/obsvty/domain/` — Pure business logic
- `src/obsvty/ports/` — Abstract interfaces (contracts)
- `src/obsvty/use_cases/` — Application orchestration
- `src/obsvty/adapters/` — Concrete implementations (DB, messaging, web)
- `tests/` — Unit, integration, and e2e tests
- `docs/` — Documentation and guides

See [README.md](../README.md) for more details.

---

## Coding Standards

- **Python 3.11+**
- Use [Poetry](https://python-poetry.org/) for dependency management.
- Format code with `ruff format`.
- Lint with `ruff check --select ALL`.
- Type-check with `mypy --strict`.
- Follow SOLID and Clean Code principles.
- Write methods ≤ 10 lines; classes ≤ 3 responsibilities.
- No circular dependencies between layers.

---

## Testing

- Write unit tests before implementation (TDD).
- Mock all ports in unit tests.
- Use `pytest` and `pytest-cov` for coverage (≥80%).
- Use `testcontainers` for integration tests.
- Structure tests to mirror source directories.

---

## Documentation

- Update documentation for any user-facing changes.
- Add or update guides in `docs/` as needed.
- Use Markdown for all documentation files.

---

## License

Obsvty is licensed under the [Apache License 2.0](../LICENSE).

---

## Contact

- Open an [Issue](https://github.com/thorgus-services/obsvty/issues) for questions or feedback.
- [Contact the maintainer](https://www.linkedin.com/in/fernandojr-dev/) directly for urgent matters.

---

> **Obsvty**: because understanding the *why* is as important as seeing the *what*.