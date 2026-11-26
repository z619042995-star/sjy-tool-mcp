# -*- coding:utf-8 -*-
""" 
@Project  :PythonProject2
@File     :mcp_client.py
@Author   :sjy
@Date     :2026/11/26 15:15
"""
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import  create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

BASE_DIR = Path(__file__).resolve().parent

# 依次向上查找 .env（001/.env 或项目根目录/.env）
load_dotenv()

client = MultiServerMCPClient(
    {
        "date-tool-stdio": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(BASE_DIR / "mcp_server_stdio.py")],
        },
        # 需要先启动对应服务端再解开注释，一次只留一种
        "date-tool-sse": {"transport": "sse", "url": "http://127.0.0.1:8000/sse"},
        # "date-tool-streamable": {"transport": "streamable_http", "url": "http://127.0.0.1:8001/mcp"},
    }
)
async def main():
    tools = await client.get_tools()
    import os
    model = init_chat_model(
        "qwen-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_provider="openai",
    )
    agent = create_agent(model, tools)
    result = await agent.ainvoke({"messages": [("user", "今天几号?")]})

    for index, message in enumerate(result["messages"]):
        print(f"\n--- [{index}] {type(message).__name__} ---")
        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                print("工具调用:", call["name"], call["args"], "id:", call["id"])
        if message.type == "tool":
            print("工具返回:", message.name, message.tool_call_id, "->", message.content)

    print("\n最终回答:", result["messages"][-1].content)


asyncio.run(main())