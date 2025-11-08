# 🕵️‍♂️ Obsvty — Observability with Code Context

> **Observability tools tell you _what broke_.  
> Obsvty shows you _why it broke_ and _how to fix it_ — based on your code.**

**Obsvty** is an **open-source** platform that connects observability data (logs, metrics, traces) with code changes and language models (LLMs) to generate **actionable, contextual, and secure insights**.

All this with:
- 🧩 **Modular architecture** — use any LLM, version control, or alert destination.
- 🔒 **Privacy-first** — sensitive data never leaves your environment.
- 📦 **Auto technical documentation** — your docs update as your code and infra change.
- 🌱 **Easy to run and contribute** — `docker-compose up` and you're set.

---

## 📋 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Getting Started](#-getting-started)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 💡 About

Most observability tools stop at the question:  
> _"Where is the error?"_

But engineers need to know:  
> _"Which commit caused this? Which line of code should I review? What is the practical fix suggestion?"_

**Obsvty bridges this gap** by correlating:
- **Traces/logs (OTLP)** ↔ **Commits/PRs** ↔ **LLM Suggestions**

### Example of generated insight:
```markdown
🔍 Detected insight:
- Metric: average latency of /checkout rose from 120ms → 480ms
- Commit: d34db33f (added synchronous card validation)
- Suggestion (LLM): "Move validation to an async queue. See example in docs/async-payment.md"
- Alert sent to #eng-alerts (Slack)
```

This is **smart observability** — not just data, but **action**.

---

## 🚀 Features

- **Contextual Insights**: Connects observability data with code changes and context
- **Privacy-First**: All sensitive data stays within your environment
- **Modular Architecture**: Support for any LLM, version control, or alert system
- **Automatic Documentation**: Docs update as your code and infrastructure change
- **OpenTelemetry Integration**: Native support for OTLP gRPC protocol
- **Extensible Plugin System**: Easy to add support for new services and tools

---

## 🧱 Project Status (MVP v0.1 – "Insight Loop")

We are building the **first functional end-to-end flow**:

```
[OTLP] → [Compression + Sanitization] → [Modular LLM] → [Alert + Doc + Chat]
                     ↑
           [GitHub: commit, PR, diff]
```

### ✅ MVP Success Criteria:
1. You send traces/logs via OTLP.
2. Receive a Slack alert with a commit-contextualized suggestion.
3. Access a chat (Streamlit) with all the context: trace + code + recommendation.
4. Confirm that **no sensitive data** was sent to the LLM.
5. All runs locally with `docker-compose up`.

---

## 🛠️ Technologies & Architecture

- **Language**: Python (3.11+)
- **Ingestion**: OTLP gRPC (OpenTelemetry)
- **Storage**: DuckDB (lightweight, no external dependencies)
- **LLM**: Any OpenAI-compatible provider (Ollama, OpenAI, Anthropic, etc.)
- **Frontend**: Streamlit (fast, iterative prototype)
- **Extensibility**: Abstract interfaces for plugins (Git, LLM, Alerts, Docs)

### Main interfaces (in `src/obsvty/application/ports/`):
```python
class GitProvider(ABC): ...
class LLMEngine(ABC): ...
class AlertPlugin(ABC): ...
class DocGenerator(ABC): ...
```

Want to add support for GitLab? Confluence? A new local model? Just implement the interface.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- Docker (optional)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thorgus-services/obsvty.git
   cd obsvty
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Generate OTLP proto stubs**:
   ```bash
   python generate_protos.py
   ```

---

## 💻 Usage

### Development Workflow
The project uses Tox for standardized development tasks:

```bash
# List all available environments
poetry run tox -l

# Run linting checks
poetry run tox -e lint

# Run type checking
poetry run tox -e type

# Run unit tests
poetry run tox -e unit

# Run security checks
poetry run tox -e security

# Run all checks at once
poetry run tox
```

### Python Toolchain Standards

This project follows standardized Python toolchain configuration for consistent, secure, and maintainable codebases.

#### Dependency Management
- **Poetry** for dependency management with precise version constraints
- Runtime, dev, and test dependencies are properly separated
- `poetry.lock` file ensures deterministic builds

#### Code Quality Tools
- **Ruff** for formatting and linting (replaces Black and Flake8)
  - Enforces consistent import ordering and grouping
  - Disallows unused imports and variables
  - Code formatting with line length of 88 characters
- **Mypy** for type checking with strict mode enabled for core packages
- **Pytest** for testing with coverage requirements (≥80% in core)

#### Security Scanning
- **Safety** for dependency vulnerability scanning
- **Bandit** for security issue detection in Python code

#### Task Automation
- **Tox** for standardized environments (replaces Invoke/tasks.py)
  - `lint` environment: Code quality checks with Ruff
  - `type` environment: Type checking with Mypy  
  - `unit` environment: Unit tests with Pytest
  - `security` environment: Combined Safety and Bandit scanning

#### Validation Pipeline
The CI pipeline includes:
1. Ruff format and lint check
2. Mypy type checking
3. Bandit security scan
4. Safety dependency vulnerability check
5. Pytest with coverage requirements (≥80% in core)
6. Build and package verification with Poetry

### One-time setup
```bash
# Install dependencies
poetry install

# Generate OTLP proto stubs
python generate_protos.py

# Run lint, typecheck and tests
poetry run tox -e lint && poetry run tox -e type && poetry run tox -e unit

# Run all checks at once (lint, type, unit tests)
poetry run tox

# Run security checks
poetry run tox -e security

# Run individual checks
poetry run tox -e lint    # Linting only
poetry run tox -e type    # Type checking only
poetry run tox -e unit    # Unit tests only
```

### Proto generation script
```bash
# Regenerate stubs from a specific ref (branch or tag)
python generate_protos.py --ref main --force
# With network timeout and validation
python generate_protos.py --ref v1.1.0 --timeout 20 --force
```

### Environment configuration
Copy `.env.example` to `.env` and adjust values if needed:
```env
# Main OTLP configuration (new standard)
OTLP_HOST=localhost
OTLP_PORT=4317
OTLP_MAX_MESSAGE_LENGTH=4194304
OTLP_BUFFER_MAX_SIZE=1000

# Backward compatibility (existing implementation)
OTLP_GRPC_HOST=0.0.0.0
OTLP_GRPC_PORT=4317
OTLP_GRPC_MAX_BUFFER_SIZE=10000
OTLP_GRPC_MAX_MESSAGE_LENGTH=4194304
OTLP_GRPC_ENABLE_REFLECTION=false
OTLP_GRPC_ENABLE_LOGS_SERVICE=false

LOG_LEVEL=INFO
```

### Configuration Model
The project uses `OtlpGrpcSettings` Pydantic model for validated configuration management:

- `OTLP_HOST`: Host address for the gRPC server (default: "localhost")
- `OTLP_PORT`: Port number for the gRPC server (default: 4317)
- `OTLP_MAX_MESSAGE_LENGTH`: Maximum message size in bytes (default: 4MB)
- `OTLP_BUFFER_MAX_SIZE`: Maximum size of the trace buffer (default: 1000)

### Running the OTLP Server
To start the OTLP gRPC server:
```bash
python -m obsvty
```

The server will load configuration from environment variables and start on the configured endpoint.

### Connecting OTLP Clients
To connect your own OTLP client to the server, ensure environment variables are set:

```python
import os
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Read from environment variables
host = os.getenv("OTLP_HOST", "localhost")
port = os.getenv("OTLP_PORT", "4317")
endpoint = f"{host}:{port}"

# Create the exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=endpoint,
    insecure=True,  # For development
)
```

For a complete example, see `examples/otlp_client.py`.

### Architecture primitives (Ports & Use Cases)
- Ports (in `src/obsvty/application/ports/`): `TraceIngestionPort`, `TraceBatchIngestionPort`, `TraceStoragePort`
- Services (in `src/obsvty/domain/services/`): `otlp_processing.py` with `process_otlp_data()` function
- Composition Root: `src/obsvty/main.py` with `create_application(buffer_size)` and `main(port, buffer_size)`

Run the package entrypoint:
```bash
python -m obsvty
```

### Tests
Setup validation tests are in `tests/unit/test_setup_validation.py` and include:
- Directory structure validation
- Dependency version pinning check
- Proto/stub generation validation
- Dockerfile presence

Run tests with coverage:
```bash
pytest --cov=src --cov-fail-under=80
```

---

## 🗺️ Public Roadmap

| Phase | Name | Goal |
|-------|------|------|
| **M0** | Bootstrapping | Repo, CI, modular structure |
| **M1** | Observability Core | OTLP + compression + detection |
| **M2** | AI Brain | Secure LLM + modular workflow |
| **M3** | Context Connect | GitHub + Slack + auto doc |
| **M4** | Insight Chat | UI with contextual chat |
| **M5** | First Release | Community launch |

---

## 🧪 How to Run Locally (coming soon)

```bash
git clone https://github.com/thorgus-services/obsvty.git
cd obsvty
docker-compose up
```

> ⚠️ **Still under construction!** We are in phase **M0/M1**. The runnable version will be released in the coming weeks.

---

## 🤝 Contributing

Obsvty is born as a project from the community, for the community.

We welcome contributions from everyone! Check out our [CONTRIBUTING.md](./docs/CONTRIBUTING.md) file for more details on how to get started.

### You can:
- 🧪 Test the MVP as soon as it's released
- 🧩 Write a plugin (e.g.: GitLab, Jira, Confluence)
- 🧠 Suggest improvements for trace compression or anomaly detection
- 📝 Improve documentation or write tutorials

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) to get started.

---

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.

---

## 📣 Contact

- Open an [Issue](https://github.com/thorgus-services/obsvty/issues)
- [Contact me directly](https://www.linkedin.com/in/fernandojr-dev/)

---

> **Obsvty**: because understanding the *why* is as important as seeing the *what*.