# MCP (Model Context Protocol) 研究笔记

## 1. MCP协议核心概念

### 什么是MCP？
MCP（Model Context Protocol，模型上下文协议）是由Anthropic主导开发的一个开放协议，旨在为AI大模型提供标准化的方式来连接外部数据源、工具和服务。它相当于AI领域的"USB接口"——一种通用的连接标准，让不同的AI模型可以与各种外部资源进行交互。

### 设计思想（图灵社区风格解释）
MCP的诞生源于一个核心问题：当AI助手需要访问你的文件、数据库、API时，如何避免为每个AI平台、每个数据源单独开发适配器？

MCP的解决思路：
- **标准化通信**：定义一套统一的消息格式和交互流程
- **双向通信**：不仅AI可以调用工具，外部系统也可以向AI推送消息
- **可扩展架构**：通过"服务器"（Server）和"客户端"（Client）模式，支持任意数量的数据源

### 核心架构组件

| 组件 | 作用 |
|------|------|
| **MCP Host** | AI应用本身（如Claude Desktop、IDE插件） |
| **MCP Client** | 驻留在Host中，负责与Server通信 |
| **MCP Server** | 轻量级程序，为特定数据源/工具提供标准化接口 |
| **Transport** | 传输层，支持stdio（标准输入/输出）和SSE（Server-Sent Events） |

### 核心功能原语

1. **Tools（工具）**：AI可以调用的函数，如搜索数据库、发送API请求
2. **Resources（资源）**：AI可以读取的数据，如文件内容、配置信息
3. **Prompts（提示模板）**：预定义的交互模板
4. **Sampling（采样）**：允许Server向Client请求LLM采样

### 通信流程
```
┌─────────────┐     JSON-RPC      ┌─────────────┐
│ MCP Client  │◄─────────────────►│ MCP Server   │
│   (Host)    │                   │  (Data/Tool) │
└─────────────┘                   └─────────────┘
```

---

## 2. Python SDK 安装方法

### 安装命令

```bash
# 官方mcp SDK
pip install mcp

# FastMCP (更易用的封装)
pip install fastmcp

# 两者可共存，FastMCP依赖mcp
```

### 主要类和模块

#### mcp 包（官方SDK）

| 模块/类 | 说明 |
|---------|------|
| `mcp.server.lowlevel.Server` | 核心服务器基类 |
| `mcp.server.stdio.stdio_server()` | stdio传输服务器上下文管理器 |
| `mcp.server.sse.SseServerTransport` | SSE传输支持 |
| `mcp.types` | 所有协议类型的Pydantic模型 |

**创建Server的基本模式**：
```python
from mcp.server.lowlevel import Server

server = Server("my-server-name")

@server.list_tools()
async def list_tools():
    return [...]

@server.call_tool()
async def call_tool(name, arguments):
    return {...}
```

#### fastmcp 包（社区封装，更推荐）

| 类/函数 | 说明 |
|---------|------|
| `fastmcp.FastMCP` | 主服务器类，简化了Server的创建 |
| `fastmcp.Context` | 请求上下文对象 |
| `fastmcp.Client` | 客户端类 |
| `fastmcp.server` | 服务器运行模块 |

**创建FastMCP服务器**：
```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(arg1: str) -> str:
    return f"Result: {arg1}"

mcp.run()  # 默认使用stdio传输
```

---

## 3. FastMCP vs python-sdk 对比

| 特性 | **FastMCP** | **mcp (官方SDK)** |
|------|------------|-------------------|
| **封装层级** | 高层封装 | 低层接口 |
| **代码量** | 少量代码即可运行 | 需要较多样板代码 |
| **学习曲线** | 平缓 | 较陡 |
| **灵活性** | 受限于封装 | 完全可控 |
| **适用场景** | 快速原型、内部工具 | 生产级、复杂需求 |
| **维护者** | 社区 (Jeremiah Lowin) | Anthropic官方 |
| **依赖** | 依赖mcp包 | 独立完整 |

### FastMCP优势
- 装饰器驱动的API（`@mcp.tool()`, `@mcp.resource()`）
- 内置依赖注入
- 自动参数验证
- 更好的错误处理

### mcp官方SDK优势
- 完整控制传输层
- 支持自定义中间件
- 更适合构建复杂的生产系统
- 协议级别的细粒度控制

---

## 4. 最简单的MCP Server示例（python-sdk版本）

### 使用mcp官方SDK

```python
#!/usr/bin/env python3
"""最简单的MCP Server - 使用官方python-sdk"""

from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# 创建服务器实例
server = Server("hello-world-server")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """声明可用的工具"""
    return [
        types.Tool(
            name="greet",
            description="向指定名字的人打招呼",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "被打招呼的人名"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """执行工具调用"""
    if name == "greet":
        greeting = f"你好，{arguments['name']}！欢迎使用MCP！"
        return [types.TextContent(type="text", text=greeting)]
    raise ValueError(f"未知工具: {name}")

async def main():
    """启动服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import anyio
    anyio.run(main)
```

**运行方式**：
```bash
python hello_server.py
# 服务器会通过stdio接收JSON-RPC消息
```

---

## 5. MCP Server运行方式

### 5.1 stdio 传输（标准输入/输出）

**原理**：通过进程的标准输入stdin读取JSON-RPC请求，通过标准输出stdout返回响应。

**特点**：
- 简单直接，适合本地进程通信
- Claude Desktop等工具的标准通信方式
- 无需网络配置

**使用示例**：
```python
from mcp.server.stdio import stdio_server

async with stdio_server() as (read_stream, write_stream):
    await server.run(read_stream, write_stream, init_options)
```

**调用方式**：
```bash
python my_server.py
# 或在Claude Desktop配置中指定
```

### 5.2 SSE（Server-Sent Events）传输

**原理**：基于HTTP的长期连接，服务器通过SSE向客户端推送消息，客户端通过POST请求发送消息。

**特点**：
- 支持网络远程调用
- 适合Web应用集成
- 需要HTTP服务器（Starlette + Uvicorn）

**使用示例**：
```python
from starlette.routing import Route, Mount
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
import uvicorn

sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())
    from starlette.responses import Response
    return Response()

async def handle_messages(request):
    return await sse.handle_post_message(request.scope, request.receive, request._send)

starlette_app = Starlette(routes=[
    Route("/sse", handle_sse, methods=["GET"]),
    Mount("/messages/", app=handle_messages),
])

if __name__ == "__main__":
    uvicorn.run(starlette_app, host="127.0.0.1", port=8000)
```

### 5.3 Streamable HTTP（新版HTTP传输）

MCP还支持 `streamable_http` 传输，这是对SSE的改进，支持更高效的流式通信。

---

## 6. 参考链接列表

### 官方资源
- **MCP 规范文档**: https://modelcontextprotocol.io/specification
- **MCP GitHub 仓库**: https://github.com/modelcontextprotocol
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **MCP TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk

### FastMCP
- **FastMCP 官方文档**: https://gofastmcp.com/
- **FastMCP GitHub**: https://github.com/jlowin/fastmcp

### 社区资源
- **MCP Hub (Smithery)**: https://smithery.ai/ - 各类MCP Server索引
- **MCP Gallery**: https://mcplabs.com/ - MCP工具展示

### 相关技术
- **JSON-RPC 2.0 规范**: https://www.jsonrpc.org/specification
- **Server-Sent Events**: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- **Pydantic V2 文档**: https://docs.pydantic.dev/

### 文章与教程
- **Anthropic 官方博客介绍MCP**: https://www.anthropic.com/news/model-context-protocol
- **MCP协议入门教程**: 搜索 "Model Context Protocol tutorial"

---

## 附录：版本信息

```
mcp: 1.27.0
fastmcp: 3.2.4
python: 3.12
```

**调研日期**: 2026-04-23
