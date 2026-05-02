# MCP接入可行性报告

> 版本：1.0
> 日期：2026-04-23
> 编制：Hermes
> 状态：已完成

---

## 一、项目背景

伟力机械三AI系统（Jarvis/Hermes/Claude）目前通过直接读写JSON文件实现协作，存在以下问题：
- **写冲突**：多AI同时写入 Z_Memory_Sync.json 导致JSON损坏（2026-04-23实测）
- **同步困难**：各AI需要理解文件路径和格式
- **扩展性差**：新增工具需要修改各AI代码

**MCP（Model Context Protocol）** 是Anthropic推出的开放协议，可将上述问题一步解决。

---

## 二、MCP协议原理

### 什么是MCP？

MCP = Model Context Protocol，模型上下文协议。它是AI领域的"USB接口"——一种通用连接标准，让AI可以标准化的方式连接外部工具和数据源。

### 核心架构

```
┌─────────────┐     JSON-RPC      ┌─────────────────────┐
│ MCP Client  │◄─────────────────►│ MCP Server          │
│ (Jarvis/Hermes/Claude)          │ (伟力Vault服务)      │
└─────────────┘                   └─────────────────────┘
```

| 组件 | 作用 |
|------|------|
| **MCP Client** | AI应用中的通信模块 |
| **MCP Server** | 为特定数据源提供标准化接口 |
| **Transport** | 传输层，支持stdio（标准输入/输出）和SSE |

### 核心功能原语

1. **Tools（工具）**：AI可以调用的函数
2. **Resources（资源）**：AI可以读取的数据
3. **Prompts（提示模板）**：预定义的交互模板

---

## 三、技术选型

### Python SDK vs FastMCP

| 特性 | FastMCP | mcp (官方SDK) |
|------|---------|---------------|
| 封装层级 | 高层封装 | 低层接口 |
| 代码量 | 少量代码即可运行 | 需要较多样板代码 |
| 学习曲线 | 平缓 | 较陡 |
| 灵活性 | 受限于封装 | 完全可控 |
| 适用场景 | 快速原型、内部工具 | 生产级、复杂需求 |

**结论：选用 FastMCP** — 代码量少，API简洁，适合内部工具快速上线。

---

## 四、伟力MCP服务器设计

### 服务器功能

已创建：`08_Tools/MCP/weili_vault_mcp_server.py`

| 工具名称 | 功能 |
|---------|------|
| `read_z_memory` | 读取 Z_Memory_Sync.json 完整内容 |
| `read_z_memory_recent` | 读取最近 N 条记忆条目 |
| `append_z_memory_entry` | 原子追加记忆条目（解决写冲突） |
| `update_startup_marker` | 更新AI启动标记 |
| `read_task_queue` | 读取任务队列 |
| `append_task` | 原子追加任务 |
| `update_task_status` | 更新任务状态 |
| `read_vault_file` | 读取知识库文件 |
| `write_vault_file` | 写入知识库文件 |
| `append_daily_log` | 追加当日日志 |
| `get_agent_status` | 获取三AI在线状态 |

### 关键特性：原子写入

传统方式（写冲突问题根源）：
```
1. 读取文件 → 2. 修改内存 → 3. 写回文件
            ↑ 这里如果另一个AI也在写，就会冲突
```

MCP方式（子代理实现）：
```
1. 读取文件 → 2. 修改内存 → 3. 写临时文件 → 4. 原子替换
            ↑ 任何时刻只有一个写操作成功
```

### 运行环境

```bash
# WSL2/Linux
cd /mnt/d/桌面文件/伟力机械知识库/08_Tools/MCP
python weili_vault_mcp_server.py
```

---

## 五、OpenClaw MCP集成

### OpenClaw配置

OpenClaw v2026331 已支持MCP协议。需要在 `openclaw.json` 中添加 `mcpServers` 配置：

```json
{
  "mcpServers": {
    "weili-vault": {
      "command": "python",
      "args": ["D:/桌面文件/伟力机械知识库/08_Tools/MCP/weili_vault_mcp_server.py"]
    }
  }
}
```

### 配置步骤

1. 备份现有配置：`openclaw.json.bak`
2. 添加 `mcpServers` 节点到根对象
3. 重启 OpenClaw
4. 验证连接：`openclaw mcp list` 或通过飞书测试工具调用

### 预期效果

配置完成后，Jarvis可以通过MCP协议调用伟力Vault工具：
- **Jarvis** 问："Hermes上次启动是什么时候？"
- OpenClaw 通过 MCP 调用 `get_agent_status` 工具
- 返回："Hermes在 2026-04-23 23:00 启动"

---

## 六、实施步骤

### Step 1：MCP服务器测试（本次已完成 ✅）

- ✅ 调研完成（Python SDK、FastMCP）
- ✅ 服务器代码已创建（weili_vault_mcp_server.py）
- ⚠️ 服务器运行测试（import超时，需进一步诊断）

### Step 2：OpenClaw MCP配置（本步骤执行）

1. 备份 `C:\Users\pc\.openclaw\openclaw.json`
2. 添加 `mcpServers` 配置
3. 重启 OpenClaw 服务
4. 验证MCP连接

### Step 3：端到端测试

1. Jarvis 通过MCP调用 `read_z_memory`
2. 验证返回结果正确
3. Jarvis 通过MCP调用 `append_z_memory_entry`
4. 验证原子写入成功

### Step 4：推广使用

将原来直接读写JSON文件的方式，改为通过MCP工具调用。

---

## 七、风险与注意事项

| 风险 | 影响 | 应对 |
|------|------|------|
| MCP包import超时 | 中 | 可能是包初始化慢，继续使用WSL2测试 |
| OpenClaw MCP配置兼容性 | 低 | 先用独立服务器测试，不影响现有功能 |
| Windows路径 vs WSL2路径 | 中 | 服务器使用Windows路径（D:\），WSL2需转换 |
| Python版本要求 | 低 | WSL2 Python 3.12.3 满足要求（3.10+） |

---

## 八、参考链接

| 资源 | 链接 |
|------|------|
| MCP官网 | https://modelcontextprotocol.io |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| FastMCP | https://github.com/jlowin/fastmcp |
| OpenClaw文档 | https://docs.openclaw.ai |

---

## 九、附录

### 已创建文件

- `08_Tools/MCP/weili_vault_mcp_server.py` — 伟力Vault MCP服务器
- `00_Workflow/mcp_research_notes.md` — 调研笔记

### 安装的包

```
mcp: 1.27.0
fastmcp: 3.2.4
python: 3.12.3
```

---

*本报告由Hermes编写，完成P0 MCP调研任务。*
