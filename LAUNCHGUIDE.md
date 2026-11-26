# Date Tool MCP
## Tagline
A lightweight Python MCP server that returns the current date in YYYY-MM-DD format.
## Description
Date Tool MCP is a lightweight Model Context Protocol server built with Python and FastMCP. It exposes a get_today tool that returns the server's current local date in YYYY-MM-DD format. The repository includes equivalent stdio, SSE, and Streamable HTTP server examples, making it useful both as a simple date utility and as a learning project for MCP transport configuration. No API key is required to run the MCP server itself.
## Setup Requirements
- Python 3.10 or later is required.
- Install the Python dependencies with `pip install -r requirements.txt`.
- No environment variables are required to run `server.py`.
- `DASHSCOPE_API_KEY` (optional): Only required when running the included LangChain demo client. Get a key from Alibaba Cloud Model Studio: https://modelstudio.console.alibabacloud.com/
## Category
Productivity
## Features
- Returns the current local date in YYYY-MM-DD format
- Provides a zero-argument get_today MCP tool
- Supports stdio for simple local client integration
- Includes SSE and Streamable HTTP transport examples
- Requires no API key or external service for the MCP server
- Includes a LangChain agent client example
## Getting Started
- "What is today's date?"
- "Please use the date tool to tell me the current date."
- Tool: get_today — Returns the current local date in YYYY-MM-DD format; use it whenever the current date is needed.
## Tags
date, time, datetime, calendar, mcp, python, fastmcp, langchain, stdio, sse, streamable-http
## Documentation URL
https://github.com/z619042995-star/sjy-tool-mcp#readme
