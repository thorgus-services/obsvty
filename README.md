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

## 🔍 Why Obsvty?

Most observability tools stop at the question:  
> _“Where is the error?”_

But engineers need to know:  
> _“Which commit caused this? Which line of code should I review? What is the practical fix suggestion?”_

**Obsvty bridges this gap** by correlating:
- **Traces/logs (OTLP)** ↔ **Commits/PRs** ↔ **LLM Suggestions**

### Example of generated insight:
```markdown
🔍 Detected insight:
- Metric: average latency of /checkout rose from 120ms → 480ms
- Commit: d34db33f (added synchronous card validation)
- Suggestion (LLM): “Move validation to an async queue. See example in docs/async-payment.md”
- Alert sent to #eng-alerts (Slack)
```

This is **smart observability** — not just data, but **action**.

---

## 🧱 Project Status (MVP v0.1 – “Insight Loop”)

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

### Main interfaces (in `obsvty/ports/`):
```python
class GitProvider(ABC): ...
class LLMEngine(ABC): ...
class AlertPlugin(ABC): ...
class DocGenerator(ABC): ...
```

Want to add support for GitLab? Confluence? A new local model? Just implement the interface.

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

## 🚀 How to Run Locally (coming soon)

```bash
git clone https://github.com/thorgus-services/obsvty.git
cd obsvty
docker-compose up
```

> ⚠️ **Still under construction!** We are in phase **M0/M1**. The runnable version will be released in the coming weeks.

---

## 🔧 Initial OTLP/gRPC Setup (TDD)

This project follows Hexagonal Architecture and TDD for the initial OTLP/gRPC setup.

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- Docker (optional)

### One-time setup
```bash
# Install dependencies
poetry install

# Generate OTLP proto stubs
invoke generate_protos

# Run lint, typecheck and tests
invoke dev

# Optional: Vulnerability scan
invoke safety_check
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
- Ports (in `src/obsvty/ports/`): `TraceIngestionPort`, `TraceBatchIngestionPort`, `TraceStoragePort`
- Use Cases (in `src/obsvty/use_cases/`): `ProcessTraceUseCase`
- Composition Root: `src/obsvty/main.py` with `build_use_cases(storage)`

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

## 🤝 Want to Contribute?

Obsvty is born as a project from the community, for the community.

### You can:
- 🧪 Test the MVP as soon as it's released
- 🧩 Write a plugin (e.g.: GitLab, Jira, Confluence)
- 🧠 Suggest improvements for trace compression or anomaly detection
- 📝 Improve documentation or write tutorials

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) to get started.

---

## 📜 License

Apache License 2.0 — see [LICENSE](./LICENSE).

---

## 📣 Contact Us

- Open an [Issue](https://github.com/thorgus-services/obsvty/issues)
- [Contact me directly](https://www.linkedin.com/in/fernandojr-dev/)

---

> **Obsvty**: because understanding the *why* is as important as seeing the *what*.