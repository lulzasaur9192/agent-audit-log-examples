"""
Export Audit Trail

Export an agent's full audit trail as JSON or CSV for
compliance reviews, incident investigation, or reporting.

Usage:
    python export_audit.py
    python export_audit.py --format csv --output audit_report.csv

Get your API key at:
    https://rapidapi.com/lulzasaur9192/api/agent-audit-log
"""

import requests
import json
import csv
import argparse
import sys

API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "agent-audit-log.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
}


def fetch_all_logs(agent_id, limit=1000):
    """
    Fetch all audit log entries for an agent.

    Args:
        agent_id: Agent to export logs for.
        limit: Max entries to fetch.

    Returns:
        List of log entry dicts.
    """
    logs = []
    offset = 0
    page_size = 100

    while offset < limit:
        response = requests.get(
            f"{BASE_URL}/v1/logs",
            headers=HEADERS,
            params={
                "agent_id": agent_id,
                "limit": min(page_size, limit - offset),
                "offset": offset,
            },
            timeout=30,
        )
        response.raise_for_status()

        page = response.json().get("logs", [])
        if not page:
            break

        logs.extend(page)
        offset += len(page)

        if len(page) < page_size:
            break

    return logs


def export_json(logs, output_file):
    """Export logs as formatted JSON."""
    with open(output_file, "w") as f:
        json.dump(logs, f, indent=2, default=str)
    print(f"Exported {len(logs)} entries to {output_file}")


def export_csv(logs, output_file):
    """Export logs as CSV."""
    if not logs:
        print("No logs to export.")
        return

    fieldnames = ["id", "timestamp", "agent_id", "action", "outcome", "hmac", "details"]

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for log in logs:
            row = {**log}
            if isinstance(row.get("details"), dict):
                row["details"] = json.dumps(row["details"])
            writer.writerow(row)

    print(f"Exported {len(logs)} entries to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Export agent audit trail")
    parser.add_argument("--agent", default="demo-agent-001", help="Agent ID to export")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--limit", type=int, default=1000, help="Max entries to export")
    args = parser.parse_args()

    output_file = args.output or f"audit_{args.agent}.{args.format}"

    print(f"=== Export Audit Trail ===\n")
    print(f"Agent: {args.agent}")
    print(f"Format: {args.format}")
    print(f"Output: {output_file}\n")

    try:
        logs = fetch_all_logs(args.agent, limit=args.limit)
        print(f"Fetched {len(logs)} log entries.\n")

        if args.format == "json":
            export_json(logs, output_file)
        else:
            export_csv(logs, output_file)

    except requests.exceptions.HTTPError as e:
        print(f"API error: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
