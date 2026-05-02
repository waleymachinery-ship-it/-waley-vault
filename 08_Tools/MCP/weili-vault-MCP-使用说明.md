# Weili Vault MCP 使用说明

> 版本：v1.0
> 更新：2026-04-24
> 维护：Jarvis / Hermes / Claude

---

## 1. 这是什么

### MCP 协议简介

**MCP（Model Context Protocol）** 是 Anthropic 提出的标准协议，让 AI 模型能调用外部工具。

```
┌─────────────────────────────────────────────────────────┐
│                    AI 模型（如 Claude）                   │
└─────────────────────┬───────────────────────────────────┘
                      │ MCP 协议
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   MCP Client                            │
│  （OpenClaw / Claude Code CLI / 其他客户端）             │
└─────────────────────┬───────────────────────────────────┘
                      │ stdio / HTTP
                      ▼
┌─────────────────────────────────────────────────────────┐
│              weili_vault_mcp_server.py                  │
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │ 记忆工具  │ │ 任务队列  │ │ 文件读写  │ │ 状态查询  │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                                                         │
│  功能：原子操作 Vault 知识库，三AI协作中枢                │
└─────────────────────────────────────────────────────────┘
```

### 三AI架构中的位置

```
                    ┌─────────────┐
                    │  用户（陈总） │
                    └──────┬──────┘
                           │ 飞书消息
                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Jarvis     │◄──►│  Hermes      │◄──►│   Claude     │
│  (OpenClaw)  │    │  (WSL2)      │    │  (CLI)       │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                    │                    │
       │    MCP 调用        │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  weili_vault_mcp_server │
              │  （原子操作 Vault）      │
              └─────────────────────────┘
```

---

## 2. 11个工具清单

### 2.1 记忆同步工具（4个）

| 工具名 | 功能 | 返回值 |
|--------|------|--------|
| `read_z_memory` | 读取完整 Z_Memory_Sync.json | JSON对象 |
| `read_z_memory_recent` | 读取最近N条记忆条目 | JSON数组 |
| `append_z_memory_entry` | 原子追加新记忆条目 | success/error |
| `search_z_memory` | 语义搜索记忆内容 | JSON数组 |

### 2.2 任务队列工具（3个）

| 工具名 | 功能 | 返回值 |
|--------|------|--------|
| `read_task_queue` | 读取完整任务队列 | JSON数组 |
| `append_task` | 原子追加新任务 | task_id |
| `update_task_status` | 更新任务状态 | success/error |

### 2.3 文件读写工具（3个）

| 工具名 | 功能 | 返回值 |
|--------|------|--------|
| `read_vault_file` | 读取知识库文件 | 文件内容 |
| `write_vault_file` | 原子写入知识库文件 | success/error |
| `append_daily_log` | 追加当日工作日志 | success/error |

### 2.4 状态查询工具（1个）

| 工具名 | 功能 | 返回值 |
|--------|------|--------|
| `get_agent_status` | 查询三AI启动状态 | JSON对象 |

---

## 3. 调用示例

### 3.1 Jarvis（OpenClaw）调用

```python
# OpenClaw 通过 MCP Client 调用
# 配置文件：~/.openclaw/openclaw.json
{
  "mcpServers": {
    "weili-vault": {
      "command": "python",
      "args": ["D:/桌面文件/伟力机械知识库/08_Tools/MCP/weili_vault_mcp_server.py"]
    }
  }
}

# 调用示例：读取记忆
result = await mcp_client.call_tool("read_z_memory")
memory = json.loads(result)

# 调用示例：追加记忆
await mcp_client.call_tool("append_z_memory_entry", {
  "agent": "jarvis",
  "content": "【Jarvis 工作记录】\n1. 处理了用户咨询\n2. 结果：成功",
  "tags": ["work", "jarvis"]
})
```

### 3.2 Claude（CLI）调用

```python
# Claude Code 中调用 MCP 工具
# 方式1：直接调用
claude_code --mcp-tools read_z_memory,append_z_memory_entry

# 方式2：在 Python 脚本中
from mcp import Client

client = Client("python weili_vault_mcp_server.py")
memory = client.call("read_z_memory_recent", {"count": 5})

# 方式3：通过 FastMCP 客户端
from weili_vault_mcp_server import mcp
# 工具已注册，可直接调用
```

### 3.3 Hermes（WSL2）调用

```bash
# WSL2 中启动 MCP Server
cd /mnt/d/桌面文件/伟力机械知识库/08_Tools/MCP
python weili_vault_mcp_server.py &

# 通过 stdio 调用
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"read_task_queue"}}' \
  | python weili_vault_mcp_server.py
```

---

## 4. 原子写入原理

### 为什么直接写文件不安全

三AI同时读写 Z_Memory_Sync.json 时，直接写入会导致冲突：

```
时间线：
T1: Jarvis 读取 Z_Memory（v100）
T2: Hermes 读取 Z_Memory（v100）
T3: Jarvis 写入 Z_Memory（v101）← 成功
T4: Hermes 写入 Z_Memory（v101）← 覆盖了 Jarvis 的内容！
T5: 结果：Jarvis 的修改丢失
```

### 原子写入机制

MCP Server 使用文件锁 + 临时文件实现原子写入：

```
步骤1：获取文件锁（flock）
       ┌─────────────────┐
       │ lock.zmemory    │ ← 锁文件
       └─────────────────┘

步骤2：读取当前内容
       Z_Memory v100

步骤3：写入临时文件
       Z_Memory.tmp（包含新内容）

步骤4：重命名原子替换
       mv Z_Memory.tmp Z_Memory_Sync.json

步骤5：释放锁
       rm lock.zmemory
```

### 图解

```
直接写入（危险）：
┌─────────────────────────────────────────┐
│ Jarvis ──写──► Z_Memory.json            │
│ Hermes ──写──► Z_Memory.json（覆盖！）   │
└─────────────────────────────────────────┘

原子写入（安全）：
┌─────────────────────────────────────────┐
│ Jarvis ──获取锁──► Z_Memory.lock        │
│ Jarvis ──写tmp──► Z_Memory.tmp          │
│ Jarvis ──原子替换──► Z_Memory.json      │
│ Jarvis ──释放锁──► 完成                  │
│                                         │
│ Hermes ──等待锁──►（等 Jarvis 完成）     │
│ Hermes ──获取锁──► Z_Memory.lock        │
│ ...                                     │
└─────────────────────────────────────────┘
```

---

## 5. 验证方法

### 5.1 检查 Server 是否运行

```bash
# 方法1：检查进程
ps aux | grep weili_vault_mcp_server

# 方法2：发送 ping
echo '{"method":"ping"}' | python weili_vault_mcp_server.py
# 应返回：{"status":"ok"}

# 方法3：通过 OpenClaw CLI
npx openclaw mcp list
# 应显示：weili-vault
```

### 5.2 测试工具调用

```python
# 测试读取
result = call_mcp_tool("read_z_memory")
assert "version" in result

# 测试写入
result = call_mcp_tool("append_z_memory_entry", {
  "agent": "test",
  "content": "MCP 测试条目",
  "tags": ["test"]
})
assert result["status"] == "success"
```

### 5.3 验证文件完整性

```python
import json

# 读取并验证 JSON 有效
with open("Z_Memory_Sync.json", "r") as f:
    data = json.load(f)
    assert "version" in data
    assert "entries" in data
    print(f"Z_Memory v{data['version']}，{len(data['entries'])} 条记忆")
```

---

## 6. 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| MCP Server 启动失败 | Python 版本不对 | 确认 Python 3.9+：`python --version` |
| 连接被拒绝 | Server 未运行 | 启动：`python weili_vault_mcp_server.py` |
| 工具调用超时 | 锁文件未释放 | 删除锁：`rm Z_Memory.lock` |
| JSON 解析错误 | 文件损坏 | 备份并重建，或用 `zmemory_backup.json` 恢复 |
| 权限不足 | 文件只读 | 检查：`chmod +rw Z_Memory_Sync.json` |

### 锁文件卡住处理

```bash
# 检查锁文件
ls -la *.lock

# 强制删除（仅在确认无其他进程使用时）
rm -f Z_Memory.lock task_queue.lock

# 重启 Server
pkill -f weili_vault_mcp_server
python weili_vault_mcp_server.py
```

### JSON 损坏恢复

```python
# 如果 Z_Memory_Sync.json 损坏
# 1. 检查备份
ls -lt Z_Memory_Sync.json*

# 2. 用备份恢复
cp Z_Memory_Sync.json.bak Z_Memory_Sync.json

# 3. 或手动重建（最后手段）
# 联系 Claude 重建 Z_Memory
```

### OpenClaw MCP 配置无效

```json
// 正确配置位置：~/.openclaw/openclaw.json
{
  "mcpServers": {
    "weili-vault": {
      "command": "python",
      "args": ["D:/桌面文件/伟力机械知识库/08_Tools/MCP/weili_vault_mcp_server.py"]
    }
  }
}
```

**注意：** `mcpServers` 必须放在根级，不是在某个子对象下。

---

## 7. 文件位置

| 文件 | 路径 |
|------|------|
| MCP Server | `D:\桌面文件\伟力机械知识库\08_Tools\MCP\weili_vault_mcp_server.py` |
| 使用说明 | `D:\桌面文件\伟力机械知识库\08_Tools\MCP\weili-vault-MCP-使用说明.md` |
| 集成测试报告 | `D:\桌面文件\伟力机械知识库\00_Workflow\MCP集成测试报告_2026-04-23.md` |

---

*本文件由 Jarvis 创建维护*
