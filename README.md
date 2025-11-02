# 🕵️‍♂️ Obsvty — Observability with Code Context

> **Ferramentas de observabilidade te dizem _o que quebrou_.  
> Obsvty te mostra _por que quebrou_ e _como consertar_ — com base no seu código.**

**Obsvty** é uma plataforma **open-source** que conecta dados de observabilidade (logs, métricas, traces) com mudanças no código e modelos de linguagem (LLMs) para gerar **insights acionáveis, contextualizados e seguros**.

Tudo isso com:
- 🧩 **Arquitetura modular** — use qualquer LLM, versionador ou destino de alerta.
- 🔒 **Privacy-first** — dados sensíveis nunca saem do seu ambiente.
- 📦 **Auto-documentação técnica** — sua doc se atualiza conforme seu código e infra mudam.
- 🌱 **Fácil de rodar e contribuir** — `docker-compose up` e pronto.

---

## 🔍 Por que Obsvty?

A maioria das ferramentas de observabilidade para na pergunta:  
> _“Onde está o erro?”_

Mas engenheiros precisam saber:  
> _“Qual commit causou isso? Qual linha de código devo revisar? Qual é a sugestão prática de correção?”_

**Obsvty preenche essa lacuna** ao correlacionar:
- **Traces/logs (OTLP)** ↔ **Commits/PRs** ↔ **Sugestões de LLMs**

### Exemplo de insight gerado:
```markdown
🔍 Insight detectado:
- Métrica: latência média de /checkout subiu de 120ms → 480ms
- Commit: d34db33f (adicionou validação síncrona de cartão)
- Sugestão (LLM): “Mova a validação para fila assíncrona. Veja exemplo em docs/async-payment.md”
- Alerta enviado para #eng-alerts (Slack)
```

Isso é **observabilidade inteligente** — não só dados, mas **ação**.

---

## 🧱 Status do Projeto (MVP v0.1 – “Insight Loop”)

Estamos construindo o **primeiro fluxo end-to-end funcional**:

```
[OTLP] → [Compressão + Sanitização] → [LLM Modular] → [Alerta + Doc + Chat]
                     ↑
           [GitHub: commit, PR, diff]
```

### ✅ Critérios de sucesso do MVP:
1. Você envia traces/logs via OTLP.
2. Recebe um alerta no Slack com sugestão contextualizada ao commit.
3. Acessa um chat (Streamlit) com todo o contexto: trace + código + recomendação.
4. Confirma que **nenhum dado sensível** foi enviado ao LLM.
5. Tudo isso roda localmente com `docker-compose up`.

---

## 🛠️ Tecnologias & Arquitetura

- **Linguagem**: Python (3.10+)
- **Ingestão**: OTLP gRPC (OpenTelemetry)
- **Storage**: DuckDB (leve, sem dependências externas)
- **LLM**: Qualquer provedor OpenAI-compatible (Ollama, OpenAI, Anthropic, etc.)
- **Frontend**: Streamlit (protótipo rápido e iterável)
- **Extensibilidade**: Interfaces abstratas para plugins (Git, LLM, Alertas, Docs)

### Interfaces principais (em `obsvty/ports/`):
```python
class GitProvider(ABC): ...
class LLMEngine(ABC): ...
class AlertPlugin(ABC): ...
class DocGenerator(ABC): ...
```

Quer adicionar suporte a GitLab? Confluence? Um novo modelo local? Basta implementar a interface.

---

## 🗺️ Roadmap Público

| Fase | Nome | Objetivo |
|------|------|--------|
| **M0** | Bootstrapping | Repo, CI, estrutura modular |
| **M1** | Observability Core | OTLP + compressão + detecção |
| **M2** | AI Brain | LLM seguro + workflow modular |
| **M3** | Context Connect | GitHub + Slack + doc automática |
| **M4** | Insight Chat | UI com chat contextual |
| **M5** | First Release | Lançamento comunitário |

👉 Veja [ROADMAP.md](./ROADMAP.md) para detalhes e como influenciar as próximas features.

---

## 🚀 Como Rodar Localmente (em breve)

```bash
git clone https://github.com/thorgus-services/obsvty.git
cd obsvty
docker-compose up
```

> ⚠️ **Ainda em construção!** Estamos na fase **M0/M1**. A versão executável virá nas próximas semanas.

---

## 🤝 Quer Contribuir?

Obsvty nasce como um projeto da comunidade, para a comunidade.

### Você pode:
- 🧪 Testar o MVP assim que lançado
- 🧩 Escrever um plugin (ex: GitLab, Jira, Confluence)
- 🧠 Sugerir melhorias de compressão de traces ou detecção de anomalias
- 📝 Melhorar a documentação ou escrever tutoriais

Veja [CONTRIBUTING.md](./docs/CONTRIBUTING.md) para começar.

---

## 📜 Licença

Apache License 2.0 — veja [LICENSE](./LICENSE).

---

## 📣 Fale Conosco

- Abra uma [Issue](https://github.com/thorgus-services/obsvty/issues)
- [Me chame diretamente](https://www.linkedin.com/in/fernandojr-dev/)

---

> **Obsvty**: porque entender o *porquê* é tão importante quanto ver o *o quê**.