# AI Agent Audit Log Examples: Tamper-Evident Logging for LLM Agents

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-Agent%20Audit%20Log-blue)](https://rapidapi.com/lulzasaur9192/api/agent-audit-log?utm_source=github&utm_medium=readme&utm_campaign=agent-audit-log)

Code examples for **AI agent audit logging**, **LLM audit trails**, and **tamper-evident logs** using the [Agent Audit Log API](https://rapidapi.com/lulzasaur9192/api/agent-audit-log?utm_source=github&utm_medium=readme&utm_campaign=agent-audit-log).

Add **agent compliance logging**, **HMAC chain verification**, and **agent observability** to your LLM agents — LangChain, CrewAI, AutoGPT, or custom builds.

## Get API Key

1. Go to [Agent Audit Log on RapidAPI](https://rapidapi.com/lulzasaur9192/api/agent-audit-log?utm_source=github&utm_medium=readme&utm_campaign=agent-audit-log)
2. Subscribe (free tier available)
3. Copy your API key from the dashboard

## Installation

### Python

```bash
pip install requests
```

### Node.js

```bash
npm install axios
```

## Examples

| File | Language | Description |
|------|----------|-------------|
| [basic_logging.py](examples/basic_logging.py) | Python | Log agent actions with HMAC verification |
| [verify_chain.py](examples/verify_chain.py) | Python | Verify audit chain integrity |
| [export_audit.py](examples/export_audit.py) | Python | Export audit trail as JSON/CSV |
| [langchain_integration.py](examples/langchain_integration.py) | Python | Add audit logging to a LangChain agent |
| [audit_log_setup.js](examples/audit_log_setup.js) | Node.js | Set up audit logging from Node.js |

## Quickstart

```python
import requests

API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "agent-audit-log.p.rapidapi.com"

# Log an agent action
response = requests.post(
    f"https://{API_HOST}/v1/logs",
    headers={
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST,
        "Content-Type": "application/json"
    },
    json={
        "agent_id": "agent-001",
        "action": "tool_call",
        "details": {"tool": "web_search", "query": "latest AI news"},
        "outcome": "success"
    }
)

log_entry = response.json()
print(f"Log ID: {log_entry['id']}, HMAC: {log_entry['hmac']}")
```

## How It Works

1. **Log actions** — every tool call, decision, or output gets logged with metadata
2. **HMAC chain** — each log entry includes an HMAC linking it to the previous entry
3. **Verify integrity** — validate that no entries have been tampered with or deleted
4. **Export** — pull full audit trails as JSON or CSV for compliance reviews

## Use Cases

- **AI agent audit log** — track every action your agent takes
- **LLM audit trail** — full history of model interactions and decisions
- **Agent compliance logging** — meet regulatory requirements for AI transparency
- **Tamper-evident logs** — HMAC chain makes log manipulation detectable
- **Agent observability** — monitor agent behavior in production
- **AI agent monitoring** — detect anomalies and unexpected actions
- **LangChain logging** — drop-in audit logging for LangChain agents
- **CrewAI audit** — track multi-agent crew interactions

## Keywords

AI agent audit log, LLM audit trail, agent compliance logging, tamper-evident logs, HMAC chain, agent observability, AI agent monitoring, LangChain logging, CrewAI audit

## License

MIT
