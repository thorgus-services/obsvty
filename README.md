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

- **Language**: Python (3.10+)
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