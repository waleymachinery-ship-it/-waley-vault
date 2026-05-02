# OpenClaw MCP 集成指南

**编制日期：** 2026-04-23
**用途：** 将 weili-vault-mcp-server 集成到 OpenClaw

---

## 一、OpenClaw MCP 配置

### 1.1 配置文件位置
```
C:\Users\pc\.openclaw\config.json
```

### 1.2 添加 MCP Server

在 `config.json` 中添加 `mcpServers` 节点：

```json
{
  "mcpServers": {
    "weili-vault": {
      "command": "python",
      "args": ["-u", "D:/桌面文件/伟力机械知识库/08_Tools/MCP/weili_vault_mcp_server.py"],
      "env": {},
      "description": "伟力Vault MCP Server - 三AI统一通信层"
    }
  }
}
```

### 1.3 完整配置示例

将以上内容追加到 `C:\Users\pc\.openclaw\config.json` 的根对象中。

---

## 二、MCP Server 启动测试

### 2.1 独立启动测试

```bash
cd D:\桌面文件\伟力机械知识库\08_Tools\MCP
python weili_vault_mcp_server.py
```

成功输出：
```
==================================================
伟力Vault MCP Server 启动中...
Vault路径: D:\桌面文件\伟力机械知识库
Z_Memory: D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json
TaskQueue: D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json
==================================================
```

### 2.2 工具调用测试

在 OpenClaw CLI 中测试：
```
/tools call weili-vault-read_z_memory
```

---

## 三、三AI MCP 调用示例

### 3.1 Jarvis (OpenClaw) 调用 FAQ

```javascript
// Jarvis 使用 MCP 读取 Hermes 的 FAQ
const faq = await mcp.callTool("weili-vault", "read_vault_file", {
  relative_path: "02_FAQ/伟力机械产品FAQ.md"
});
```

### 3.2 Hermes 调用 Z_Memory

```python
# Hermes 使用 MCP 读取 Z_Memory
from mcp import Client

client = Client("weili-vault-mcp-server")
result = client.call("read_z_memory")
print(result["data"]["version"])
```

### 3.3 Claude 原子写入 Z_Memory

```python
# Claude 使用 MCP 原子写入（解决写冲突）
from mcp import Client

client = Client("weili-vault-mcp-server")
result = client.call("append_z_memory_entry", {
    "agent": "claude",
    "content": "【Claude 工作记录】...",
    "tags": ["claude", "work-log"]
})
print(f"写入成功，entry_id: {result['entry_id']}")
```

---

## 四、MCP 可用工具列表

### Z_Memory 操作
| 工具 | 功能 | 返回值 |
|------|------|--------|
| `read_z_memory` | 读取完整 Z_Memory | version, entries, last_modified |
| `read_z_memory_recent` | 读取最近 N 条 | entries 列表 |
| `append_z_memory_entry` | 原子追加条目 | entry_id, version |
| `update_startup_marker` | 更新启动标记 | startup_marker, value |

### 任务队列操作
| 工具 | 功能 | 返回值 |
|------|------|--------|
| `read_task_queue` | 读取任务队列 | tasks, pending_count |
| `append_task` | 原子追加任务 | task_id, version |
| `update_task_status` | 更新任务状态 | task_id, status |

### 知识库操作
| 工具 | 功能 | 返回值 |
|------|------|--------|
| `read_vault_file` | 读取知识库文件 | path, content |
| `write_vault_file` | 写入知识库文件 | path, size |
| `append_daily_log` | 追加当日日志 | log_path |

### 状态查询
| 工具 | 功能 | 返回值 |
|------|------|--------|
| `get_agent_status` | 获取三AI状态 | agents, last_writer |

---

## 五、Resource URI

| URI | 内容 |
|-----|------|
| `vault://memory/today` | 当日记忆快照（最近20条） |
| `vault://memory/sync` | Z_Memory 同步状态 |
| `vault://tasks` | 任务队列快照 |

---

## 六、故障排除

### 问题1：MCP Server 无法启动
**检查：** Python 环境变量是否正确
```bash
python --version  # 应为 3.10+
pip show mcp      # 应显示 1.26.0
```

### 问题2：OpenClaw 无法连接
**检查：** 检查 OpenClaw 版本是否支持 MCP
```bash
npx openclaw --version
```

### 问题3：Z_Memory 写冲突
**解决：** 使用 `append_z_memory_entry` 而非直接写入文件，MCP Server 会自动处理原子操作。

---

*本指南为 P0 MCP 集成第一阶段文档。*
*下一步：编写三AI协作的完整 MCP 调用流程。*