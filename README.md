<p align="center">
  <img src="assets/logo.png" alt="Date Tool MCP logo" width="160" height="160" />
</p>

# Date Tool MCP — 三种传输方式演示

用同一个工具（`get_today`，返回当前日期）演示 MCP 的三种传输方式，并用 LangChain Agent 作为客户端调用：

| 传输方式 | 服务端 | 客户端连接地址 |
| --- | --- | --- |
| stdio | `mcp_server_stdio.py` | 由客户端自动拉起子进程，无地址 |
| SSE | `mcp_server_sse.py` | `http://127.0.0.1:8000/sse` |
| Streamable HTTP | `mcp_server_streamable.py` | `http://127.0.0.1:8000/mcp` |

## 目录结构

```
001/
├── server.py                  # 发布用 stdio 入口（python server.py）
├── mcp_server_stdio.py        # stdio 传输示例
├── mcp_server_sse.py          # SSE 传输
├── mcp_server_streamable.py   # Streamable HTTP 传输
├── mcp_client.py              # LangChain + MCP 客户端
├── chatmcp.yaml               # ChatMCP 安装配置
├── LAUNCHGUIDE.md             # MCP Marketplace 提交信息
├── llms-install.md            # 供 Cline 等 AI Agent 自动安装
├── assets/logo.png            # 400×400 项目图标
├── requirements.txt
└── LICENSE
```

## 作为 MCP 服务端安装

服务端本身**不需要任何 API Key**。stdio 配置如下（详见 `llms-install.md`，供 Cline 等 AI Agent 自动安装）：

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

## 环境要求

- Python 3.10+
- 一个可用的 DashScope API Key（**仅**运行 `mcp_client.py` 演示时需要，服务端不需要）

## 安装

```bash
pip install -r requirements.txt
```

在项目根目录或本目录创建 `.env`：

```
DASHSCOPE_API_KEY=your_api_key_here
```

## 运行

三个服务端暴露的工具完全相同，**一次只验证一种传输方式**。

### 1. stdio（最简单，不用手动启服务端）

客户端会以子进程方式自动启动 `mcp_server_stdio.py`：

```bash
python mcp_client.py
```

### 2. SSE

先启动服务端，再另开一个终端运行客户端：

```bash
# 终端 1
python mcp_server_sse.py

# 终端 2
python mcp_client.py
```

在 `mcp_client.py` 中启用 SSE 配置：

```python
"date-tool-sse": {"transport": "sse", "url": "http://127.0.0.1:8000/sse"},
```

### 3. Streamable HTTP

```bash
# 终端 1
python mcp_server_streamable.py

# 终端 2
python mcp_client.py
```

在 `mcp_client.py` 中启用对应的 HTTP 配置：

```python
"date-tool-streamable": {"transport": "streamable_http", "url": "http://127.0.0.1:8000/mcp"},
```

## 客户端说明

`mcp_client.py` 使用 `MultiServerMCPClient` 管理多个 MCP 服务端，流程为：

1. `client.get_tools()` 获取所有服务端提供的工具
2. `init_chat_model("qwen-plus", ...)` 通过 DashScope 的 OpenAI 兼容接口初始化模型
3. `create_agent(model, tools)` 构造 Agent
4. 提问「今天几号?」，模型自动调用 `get_today` 工具并输出最终回答

stdio 配置使用 `sys.executable` 和脚本所在目录，因此在任意机器/目录下都能直接运行，无需修改路径。

## 输出示例

```
--- [0] HumanMessage ---
--- [1] AIMessage ---
工具调用: get_today {} id: call_xxx
--- [2] ToolMessage ---
工具返回: get_today call_xxx -> 2026-11-26
--- [3] AIMessage ---

最终回答: 今天是 2026 年 11 月 26 日。
```

## 常见问题

**`McpError: Session terminated` / 连接失败**
客户端里同时启用了未启动的 HTTP 服务端。只保留当前要验证的那一种 transport，其余注释掉。

**端口被占用**
`mcp_server_sse.py` 和 `mcp_server_streamable.py` 默认都使用 8000 端口，不能同时运行。需要同时启动时，请修改其中一个的 `port` 并同步修改客户端 URL。

**`No module named 'langchain_mcp_adapters'`**
装依赖时用错了解释器，确认 `pip install -r requirements.txt` 与运行 `python mcp_client.py` 是同一个环境。

**401 invalid_api_key**
`DASHSCOPE_API_KEY` 无效或未生效，检查 `.env` 内容及是否已加载到环境变量中。
