# Installation Guide for AI Agents (Cline)

This file tells an AI coding agent (such as Cline) how to install and configure
the **Date Tool MCP** server automatically. No API key is required to run the
MCP server itself.

## Overview

- **Server name:** `date-tool-mcp`
- **Tool provided:** `get_today` — returns the current local date as `YYYY-MM-DD`
- **Transport:** stdio (the client launches the server as a subprocess)
- **Runtime:** Python 3.10+
- **Repository:** https://github.com/z619042995-star/sjy-tool-mcp

## Step 1 — Clone the repository

```bash
git clone https://github.com/z619042995-star/sjy-tool-mcp.git
cd sjy-tool-mcp
```

## Step 2 — Install dependencies

Use the Python interpreter that the MCP client will also use:

```bash
pip install -r requirements.txt
```

This installs `mcp` (FastMCP) and its dependencies. There are no API keys,
environment variables, or external services required for the server.

## Step 3 — Add the MCP server to the client configuration

Use the following stdio configuration. `server.py` is the stdio entry point
that exposes the `get_today` tool.

```json
{
  "mcpServers": {
    "date-tool-mcp": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/sjy-tool-mcp"
    }
  }
}
```

Notes:

- Replace `/absolute/path/to/sjy-tool-mcp` with the absolute path where the
  repository was cloned in Step 1.
- If your environment uses `python3`, replace `"python"` with `"python3"`.
- Prefer an absolute path to the Python executable if `python` is not on PATH.

## Step 4 — Verify

Once configured, the client should list one tool: `get_today`. Calling it must
return the current date, for example `2026-11-26`.

## Optional — Demo client (not required by the MCP server)

`mcp_client.py` is a LangChain agent demo that calls the tool through a
DashScope (`qwen-plus`) model. It is **not** needed for the MCP server. To run
the demo only, set `DASHSCOPE_API_KEY` in a `.env` file at the repository root.
