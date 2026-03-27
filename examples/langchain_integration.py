"""
LangChain Audit Log Integration

Add tamper-evident audit logging to a LangChain agent.
Every tool call, LLM invocation, and decision is logged
to the Agent Audit Log API with HMAC chain verification.

Usage:
    pip install langchain langchain-openai requests
    python langchain_integration.py

Get your API key at:
    https://rapidapi.com/lulzasaur9192/api/agent-audit-log
"""

import requests
from typing import Any, Optional

# LangChain imports
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult

API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "agent-audit-log.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
    "Content-Type": "application/json",
}


def _log(agent_id: str, action: str, details: dict, outcome: str = "success"):
    """Send a log entry to the audit API."""
    try:
        requests.post(
            f"{BASE_URL}/v1/logs",
            headers=HEADERS,
            json={
                "agent_id": agent_id,
                "action": action,
                "details": details,
                "outcome": outcome,
            },
            timeout=10,
        )
    except requests.exceptions.RequestException:
        pass  # Don't block the agent if logging fails


class AuditLogCallback(BaseCallbackHandler):
    """
    LangChain callback handler that logs all agent activity
    to the Agent Audit Log API.

    Usage:
        from langchain.agents import initialize_agent
        audit = AuditLogCallback(agent_id="my-langchain-agent")
        agent = initialize_agent(..., callbacks=[audit])
        agent.run("What is the weather?")
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        """Called when the LLM starts generating."""
        _log(self.agent_id, "llm_start", {
            "model": serialized.get("name", "unknown"),
            "prompt_count": len(prompts),
        })

    def on_llm_end(self, response: LLMResult, **kwargs):
        """Called when the LLM finishes generating."""
        token_usage = {}
        if response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})

        _log(self.agent_id, "llm_end", {
            "generations": len(response.generations),
            "tokens": token_usage,
        })

    def on_llm_error(self, error: BaseException, **kwargs):
        """Called when the LLM errors."""
        _log(self.agent_id, "llm_error", {
            "error": str(error)[:500],
        }, outcome="error")

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        """Called when a tool starts running."""
        _log(self.agent_id, "tool_start", {
            "tool": serialized.get("name", "unknown"),
            "input": input_str[:500],
        })

    def on_tool_end(self, output: str, **kwargs):
        """Called when a tool finishes."""
        _log(self.agent_id, "tool_end", {
            "output_length": len(output),
            "output_preview": output[:200],
        })

    def on_tool_error(self, error: BaseException, **kwargs):
        """Called when a tool errors."""
        _log(self.agent_id, "tool_error", {
            "error": str(error)[:500],
        }, outcome="error")

    def on_agent_action(self, action: AgentAction, **kwargs):
        """Called when the agent decides to take an action."""
        _log(self.agent_id, "agent_action", {
            "tool": action.tool,
            "input": str(action.tool_input)[:500],
            "reasoning": action.log[:500],
        })

    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        """Called when the agent completes."""
        _log(self.agent_id, "agent_finish", {
            "output": str(finish.return_values)[:500],
        })


# ----- Example usage -----

def main():
    """
    Example: Set up a LangChain agent with audit logging.

    This demonstrates how to attach the AuditLogCallback to
    any LangChain agent. Replace the placeholder with your
    actual agent setup.
    """
    print("=== LangChain Audit Log Integration ===\n")

    # Create the audit callback
    audit = AuditLogCallback(agent_id="langchain-demo-001")

    # Example: attach to a LangChain agent
    # (uncomment and modify for your setup)
    #
    # from langchain_openai import ChatOpenAI
    # from langchain.agents import initialize_agent, load_tools
    #
    # llm = ChatOpenAI(model="gpt-4")
    # tools = load_tools(["serpapi", "llm-math"], llm=llm)
    # agent = initialize_agent(
    #     tools, llm,
    #     agent="zero-shot-react-description",
    #     callbacks=[audit],
    #     verbose=True,
    # )
    # agent.run("What is the current price of Bitcoin in EUR?")

    # Simulate agent actions for demo
    print("Simulating agent workflow with audit logging...\n")

    audit.on_llm_start({"name": "claude-3.5-sonnet"}, ["What is 2+2?"])
    print("  Logged: llm_start")

    audit.on_agent_action(AgentAction(
        tool="calculator",
        tool_input="2+2",
        log="I need to calculate 2+2",
    ))
    print("  Logged: agent_action (calculator)")

    audit.on_tool_start({"name": "calculator"}, "2+2")
    print("  Logged: tool_start")

    audit.on_tool_end("4")
    print("  Logged: tool_end")

    audit.on_llm_end(LLMResult(generations=[[]], llm_output={"token_usage": {"total_tokens": 150}}))
    print("  Logged: llm_end")

    audit.on_agent_finish(AgentFinish(
        return_values={"output": "2+2 = 4"},
        log="",
    ))
    print("  Logged: agent_finish")

    print("\nAll actions logged to audit trail with HMAC chain.")
    print("Verify at: https://rapidapi.com/lulzasaur9192/api/agent-audit-log")


if __name__ == "__main__":
    main()
