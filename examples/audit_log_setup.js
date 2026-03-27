/**
 * Agent Audit Log Setup (Node.js)
 *
 * Set up tamper-evident audit logging for AI agents.
 * Provides a simple client class that wraps the
 * Agent Audit Log API.
 *
 * Usage:
 *   node audit_log_setup.js
 *
 * Get your API key at:
 *   https://rapidapi.com/lulzasaur9192/api/agent-audit-log
 */

const axios = require("axios");

const API_KEY = "YOUR_RAPIDAPI_KEY";
const API_HOST = "agent-audit-log.p.rapidapi.com";
const BASE_URL = `https://${API_HOST}`;

const headers = {
  "X-RapidAPI-Key": API_KEY,
  "X-RapidAPI-Host": API_HOST,
  "Content-Type": "application/json",
};

/**
 * Audit log client for AI agents.
 */
class AuditLogger {
  /**
   * @param {string} agentId - Unique agent identifier.
   */
  constructor(agentId) {
    this.agentId = agentId;
  }

  /**
   * Log an action to the audit trail.
   * @param {string} action - Action type (e.g., "tool_call", "decision").
   * @param {Object} details - Action metadata.
   * @param {string} outcome - Result ("success", "failure", "error").
   * @returns {Promise<Object>} Created log entry.
   */
  async log(action, details = {}, outcome = "success") {
    const response = await axios.post(
      `${BASE_URL}/v1/logs`,
      {
        agent_id: this.agentId,
        action,
        details,
        outcome,
      },
      { headers, timeout: 30000 }
    );
    return response.data;
  }

  /**
   * Get recent log entries.
   * @param {number} limit - Max entries to return.
   * @returns {Promise<Object[]>} Array of log entries.
   */
  async getLogs(limit = 10) {
    const response = await axios.get(`${BASE_URL}/v1/logs`, {
      headers,
      params: { agent_id: this.agentId, limit },
      timeout: 30000,
    });
    return response.data.logs || [];
  }

  /**
   * Verify the HMAC chain integrity.
   * @returns {Promise<Object>} Verification result.
   */
  async verify() {
    const response = await axios.post(
      `${BASE_URL}/v1/verify`,
      { agent_id: this.agentId },
      { headers, timeout: 60000 }
    );
    return response.data;
  }

  /**
   * Convenience: log a tool call.
   * @param {string} tool - Tool name.
   * @param {Object} input - Tool input.
   * @param {Object} output - Tool output.
   * @returns {Promise<Object>}
   */
  async logToolCall(tool, input, output = null) {
    return this.log("tool_call", { tool, input, output });
  }

  /**
   * Convenience: log a decision.
   * @param {string} reasoning - Why the agent made this decision.
   * @param {*} choice - What was decided.
   * @returns {Promise<Object>}
   */
  async logDecision(reasoning, choice) {
    return this.log("decision", { reasoning, choice });
  }
}

async function main() {
  console.log("=== Agent Audit Log Setup (Node.js) ===\n");

  const logger = new AuditLogger("node-agent-001");

  // Log a series of agent actions
  console.log("Logging agent actions...\n");

  await logger.log("session_start", { model: "gpt-4", task: "data analysis" });
  console.log("  Logged: session_start");

  await logger.logToolCall("database_query", { sql: "SELECT * FROM users LIMIT 10" });
  console.log("  Logged: tool_call (database_query)");

  await logger.logDecision("User count is low, should send activation emails", "send_emails");
  console.log("  Logged: decision");

  await logger.logToolCall("send_email", { to: "team@example.com", subject: "Activation report" });
  console.log("  Logged: tool_call (send_email)");

  await logger.log("session_end", { tokens_used: 1500, actions_taken: 4 });
  console.log("  Logged: session_end");

  // Verify the chain
  console.log("\nVerifying audit chain...");
  try {
    const result = await logger.verify();
    if (result.valid) {
      console.log(`  VALID — ${result.chain_length} entries, no tampering`);
    } else {
      console.log(`  INVALID — ${result.errors.length} error(s) found`);
    }
  } catch (err) {
    console.log(`  Verification error: ${err.message}`);
  }

  // Fetch recent logs
  console.log("\nRecent logs:");
  const logs = await logger.getLogs(5);
  for (const log of logs) {
    console.log(`  ${log.timestamp} | ${log.action} | ${log.outcome}`);
  }
}

main().catch((err) => {
  if (err.response && err.response.status === 403) {
    console.error(
      "API key invalid. Get one at https://rapidapi.com/lulzasaur9192/api/agent-audit-log"
    );
  } else {
    console.error(`Error: ${err.message}`);
  }
  process.exit(1);
});
