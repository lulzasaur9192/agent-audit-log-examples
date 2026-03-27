"""
Verify Audit Chain Integrity

Validate that an agent's audit log has not been tampered with
by verifying the HMAC chain. Each entry's HMAC depends on the
previous entry, so any modification or deletion is detectable.

Usage:
    python verify_chain.py

Get your API key at:
    https://rapidapi.com/lulzasaur9192/api/agent-audit-log
"""

import requests
import sys

API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "agent-audit-log.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
}


def verify_chain(agent_id):
    """
    Verify the HMAC chain integrity for an agent's audit log.

    The API checks that every log entry's HMAC correctly
    references the previous entry. Returns verification status
    and details about any broken links.

    Args:
        agent_id: Agent whose audit chain to verify.

    Returns:
        Dict with verification result, chain length, and any errors.
    """
    response = requests.post(
        f"{BASE_URL}/v1/verify",
        headers={**HEADERS, "Content-Type": "application/json"},
        json={"agent_id": agent_id},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_chain_summary(agent_id):
    """
    Get a summary of the agent's audit chain.

    Args:
        agent_id: Agent to summarize.

    Returns:
        Dict with chain stats (length, first/last entry, etc.).
    """
    response = requests.get(
        f"{BASE_URL}/v1/chain/{agent_id}/summary",
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main():
    print("=== Audit Chain Verification ===\n")

    agents = ["demo-agent-001", "demo-agent-002", "production-agent"]

    for agent_id in agents:
        print(f"Verifying chain for: {agent_id}")

        try:
            result = verify_chain(agent_id)

            valid = result.get("valid", False)
            chain_length = result.get("chain_length", 0)
            errors = result.get("errors", [])

            if valid:
                print(f"  VALID — {chain_length} entries, no tampering detected")
            else:
                print(f"  INVALID — {chain_length} entries, {len(errors)} error(s):")
                for err in errors:
                    print(f"    - Entry {err.get('position')}: {err.get('message')}")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("  No audit log found for this agent.")
            else:
                print(f"  Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"  Request failed: {e}")
            sys.exit(1)

        print()


if __name__ == "__main__":
    main()
