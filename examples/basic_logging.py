"""
Basic Agent Audit Logging

Log AI agent actions with HMAC chain verification using
the Agent Audit Log API. Each entry is cryptographically
linked to the previous one for tamper detection.

Usage:
    python basic_logging.py

Get your API key at:
    https://rapidapi.com/lulzasaur9192/api/agent-audit-log
"""

import requests
import json

API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "agent-audit-log.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
    "Content-Type": "application/json",
}


def log_action(agent_id, action, details=None, outcome="success"):
    """
    Log a single agent action to the audit trail.

    Args:
        agent_id: Unique identifier for the agent.
        action: Action type (e.g., "tool_call", "decision", "output").
        details: Dict of action-specific metadata.
        outcome: Result of the action ("success", "failure", "error").

    Returns:
        Log entry dict with id, hmac, timestamp, and chain position.
    """
    payload = {
        "agent_id": agent_id,
        "action": action,
        "details": details or {},
        "outcome": outcome,
    }

    response = requests.post(
        f"{BASE_URL}/v1/logs",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_logs(agent_id, limit=10):
    """
    Retrieve recent audit log entries for an agent.

    Args:
        agent_id: Agent to fetch logs for.
        limit: Max entries to return.

    Returns:
        List of log entry dicts.
    """
    response = requests.get(
        f"{BASE_URL}/v1/logs",
        headers=HEADERS,
        params={"agent_id": agent_id, "limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("logs", [])


def main():
    print("=== Agent Audit Log — Basic Logging ===\n")

    agent_id = "demo-agent-001"

    # Simulate an agent workflow
    actions = [
        {
            "action": "session_start",
            "details": {"model": "claude-3.5-sonnet", "task": "research"},
        },
        {
            "action": "tool_call",
            "details": {"tool": "web_search", "query": "latest AI safety papers"},
        },
        {
            "action": "tool_result",
            "details": {"tool": "web_search", "results_count": 15},
        },
        {
            "action": "decision",
            "details": {"reasoning": "Top 3 results are most relevant", "selected": 3},
        },
        {
            "action": "output",
            "details": {"type": "summary", "length": 450},
        },
        {
            "action": "session_end",
            "details": {"tokens_used": 2340, "duration_seconds": 12},
        },
    ]

    print(f"Logging {len(actions)} actions for {agent_id}...\n")

    for act in actions:
        entry = log_action(agent_id, act["action"], act["details"])
        print(f"  [{entry.get('id', 'ok')}] {act['action']} — HMAC: {entry.get('hmac', 'N/A')[:16]}...")

    # Retrieve the log
    print(f"\nRecent logs for {agent_id}:")
    logs = get_logs(agent_id)
    for log in logs:
        print(f"  {log.get('timestamp', '')} | {log.get('action', '')} | {log.get('outcome', '')}")


if __name__ == "__main__":
    main()
