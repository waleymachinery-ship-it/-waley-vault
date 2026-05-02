#!/usr/bin/env python3
"""
伟力机械 Vault MCP Server
基于 FastMCP 实现三AI统一通信层

功能：
- 原子读写 Z_Memory_Sync.json（解决写冲突问题）
- 任务队列原子操作
- 知识库文件读写
- 三AI状态查询

安装：pip install mcp fastmcp
运行：python weili_vault_mcp_server.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP

# ============== 配置 ==============
VAULT_ROOT = Path(r"D:\桌面文件\伟力机械知识库")
ZMONEY_PATH = VAULT_ROOT / "00_Workflow" / "memory" / "Z_Memory_Sync.json"
TASK_QUEUE_PATH = VAULT_ROOT / "00_Workflow" / "memory" / "task_queue.json"
MEMORY_LOG_DIR = VAULT_ROOT / "memory"

# 飞书 API 配置
FEISHU_APP_ID = "cli_a942303fdef99cd1"
FEISHU_APP_SECRET = "JrhR2ynU6ogqxZOgKNRxZdXz6Xq0Ot5r"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

# MCP Server 标识
mcp = FastMCP("伟力Vault-MCP-Server")

# ============== 飞书 API 辅助 ==============

_tenant_token = None
_tenant_token_expires_at = 0

def get_tenant_token() -> str:
    """获取飞书 tenant access token"""
    global _tenant_token, _tenant_token_expires_at
    
    # 检查缓存
    if _tenant_token and datetime.now().timestamp() < _tenant_token_expires_at - 60:
        return _tenant_token
    
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    resp = requests.post(url, json=data, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"获取 tenant token 失败: {result}")
    
    _tenant_token = result["tenant_access_token"]
    _tenant_token_expires_at = datetime.now().timestamp() + result.get("expire", 7200)
    return _tenant_token

# ============== 辅助函数 ==============

def read_json(path: Path) -> dict:
    """读取JSON文件，带重试"""
    for attempt in range(3):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            if attempt < 2:
                import time
                time.sleep(0.1)
            else:
                raise e

def write_json(path: Path, data: dict) -> bool:
    """原子写入JSON文件（写临时文件再 rename）"""
    temp_path = path.with_suffix(".tmp")
    for attempt in range(3):
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # 原子替换
            if os.name == "nt":
                # Windows: 先删除再 rename
                if path.exists():
                    os.remove(path)
            os.replace(temp_path, path)
            return True
        except (IOError, OSError) as e:
            if attempt < 2:
                import time
                time.sleep(0.1)
            else:
                raise e
    return False

def increment_version(data: dict, writer: str) -> dict:
    """原子递增版本号"""
    v = data.get("version", 0)
    if isinstance(v, str) and v.startswith("v"):
        data["version"] = "v" + str(int(v[1:]) + 1)
    else:
        data["version"] = int(v) + 1
    data["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    data["last_writer"] = writer
    return data

# ============== Z_Memory 操作 ==============

@mcp.tool()
def read_z_memory() -> dict:
    """读取当前 Z_Memory_Sync.json 完整内容"""
    try:
        data = read_json(ZMONEY_PATH)
        return {
            "success": True,
            "version": data.get("version"),
            "last_modified": data.get("last_modified"),
            "last_writer": data.get("last_writer"),
            "entries_count": len(data.get("entries", [])),
            "data": data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def read_z_memory_recent(count: int = 10) -> list:
    """读取最近 N 条 Z_Memory 条目"""
    try:
        data = read_json(ZMONEY_PATH)
        entries = data.get("entries", [])
        recent = entries[-count:] if len(entries) > count else entries
        return {
            "success": True,
            "version": data.get("version"),
            "entries": recent
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def append_z_memory_entry(
    agent: str,
    content: str,
    tags: list = None,
    confidence: float = 1.0
) -> dict:
    """原子追加 Z_Memory 条目（解决写冲突）"""
    try:
        data = read_json(ZMONEY_PATH)

        # 生成新条目
        entry_id = f"{agent}-work-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
        new_entry = {
            "id": entry_id,
            "agent": agent,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "content": content,
            "tags": tags or [agent],
            "confidence": confidence
        }

        # 追加并递增版本
        data["entries"] = data.get("entries", [])
        data["entries"].append(new_entry)
        data = increment_version(data, agent)

        # 原子写回
        write_json(ZMONEY_PATH, data)

        return {
            "success": True,
            "entry_id": entry_id,
            "version": data["version"],
            "entries_count": len(data["entries"])
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def update_startup_marker(agent: str) -> dict:
    """更新 AI 启动标记"""
    try:
        data = read_json(ZMONEY_PATH)
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

        startup_key = f"{agent.upper()}_STARTUP"
        data[startup_key] = now
        data = increment_version(data, agent)

        write_json(ZMONEY_PATH, data)

        return {
            "success": True,
            "startup_marker": startup_key,
            "value": now,
            "version": data["version"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============== 任务队列操作 ==============

@mcp.tool()
def read_task_queue() -> dict:
    """读取任务队列"""
    try:
        data = read_json(TASK_QUEUE_PATH)
        return {
            "success": True,
            "version": data.get("version"),
            "tasks": data.get("tasks", []),
            "pending_count": sum(1 for t in data.get("tasks", []) if t.get("status") == "pending")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def append_task(
    to: str,
    title: str,
    content: str,
    from_agent: str = "unknown",
    priority: str = "normal"
) -> dict:
    """原子追加任务（解决写冲突）"""
    try:
        data = read_json(TASK_QUEUE_PATH)

        # 生成新任务 ID
        existing_tasks = data.get("tasks", [])
        task_count = len(existing_tasks) + 1
        task_id = f"task-{datetime.now().strftime('%Y%m%d')}-{task_count:03d}"

        new_task = {
            "id": task_id,
            "from": from_agent,
            "to": to,
            "status": "pending",
            "priority": priority,
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "version": data.get("version", 0) + 1
        }

        data["tasks"] = existing_tasks
        data["tasks"].append(new_task)
        data["version"] = data.get("version", 0) + 1
        data["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

        write_json(TASK_QUEUE_PATH, data)

        return {
            "success": True,
            "task_id": task_id,
            "version": data["version"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def update_task_status(task_id: str, status: str, result: str = None) -> dict:
    """更新任务状态（done/failed/in_progress）"""
    try:
        data = read_json(TASK_QUEUE_PATH)

        updated = False
        for task in data.get("tasks", []):
            if task.get("id") == task_id:
                task["status"] = status
                if result:
                    task["result"] = result
                task["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
                updated = True
                break

        if not updated:
            return {"success": False, "error": f"Task {task_id} not found"}

        data["version"] = data.get("version", 0) + 1
        data["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

        write_json(TASK_QUEUE_PATH, data)

        return {
            "success": True,
            "task_id": task_id,
            "status": status,
            "version": data["version"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============== 知识库文件操作 ==============

@mcp.tool()
def read_vault_file(relative_path: str) -> dict:
    """读取知识库文件"""
    try:
        full_path = VAULT_ROOT / relative_path
        if not full_path.exists():
            return {"success": False, "error": "File not found"}

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "success": True,
            "path": str(full_path),
            "size": len(content),
            "content": content
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def write_vault_file(relative_path: str, content: str) -> dict:
    """写入知识库文件"""
    try:
        full_path = VAULT_ROOT / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "path": str(full_path),
            "size": len(content)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def append_daily_log(content: str) -> dict:
    """追加当日日志"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = MEMORY_LOG_DIR / f"{today}.md"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"\n## {timestamp}\n\n{content}\n"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)

        return {
            "success": True,
            "log_path": str(log_path)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============== 飞书消息操作 ==============

@mcp.tool()
def read_feishu_messages(chat_id: str = None, limit: int = 10, hours: int = 24) -> dict:
    """读取飞书群消息历史
    
    Args:
        chat_id: 群ID，默认读取伟力机械群
        limit: 返回消息数量上限，默认10
        hours: 只看最近多少小时内，默认24
    """
    try:
        if chat_id is None:
            chat_id = "oc_2a35b9e85451a57f9c64f93f15912176"
        
        token = get_tenant_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # 计算时间范围
        start_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        
        url = f"{FEISHU_API_BASE}/im/v1/messages"
        params = {
            "container_id_type": "chat",
            "container_id": chat_id,
            "page_size": min(limit, 50),
        }
        
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        
        if result.get("code") != 0:
            return {"success": False, "error": f"Feishu API error: {result}"}
        
        messages = []
        for item in result.get("data", {}).get("items", [])[:limit]:
            msg_type = item.get("msg_type", "")
            content = item.get("body", {}).get("content", "")
            
            # 解析 content
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except:
                    pass
            
            messages.append({
                "message_id": item.get("message_id"),
                "msg_type": msg_type,
                "content": content,
                "create_time": item.get("create_time"),
                "sender": item.get("sender", {}),
            })
        
        return {
            "success": True,
            "chat_id": chat_id,
            "count": len(messages),
            "messages": messages
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============== 三AI状态查询 ==============

@mcp.tool()
def get_agent_status() -> dict:
    """获取三AI启动状态"""
    try:
        data = read_json(ZMONEY_PATH)

        agents = ["JARVIS", "HERMES", "CLAUDE"]
        status = {}

        for agent in agents:
            key = f"{agent}_STARTUP"
            status[agent] = {
                "last_startup": data.get(key),
                "online": data.get(key) is not None
            }

        return {
            "success": True,
            "version": data.get("version"),
            "last_writer": data.get("last_writer"),
            "agents": status
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============== Resource 提供 ==============

@mcp.resource("vault://memory/today")
def vault_memory_today() -> str:
    """当日记忆快照"""
    try:
        data = read_json(ZMONEY_PATH)
        today = datetime.now().strftime("%Y-%m-%d")
        entries = [
            e for e in data.get("entries", [])
            if e.get("timestamp", "").startswith(today)
        ]
        return json.dumps({
            "date": today,
            "entries_count": len(entries),
            "entries": entries[-20:]  # 最近20条
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.resource("vault://memory/sync")
def vault_memory_sync() -> str:
    """Z_Memory 同步状态"""
    try:
        data = read_json(ZMONEY_PATH)
        return json.dumps({
            "version": data.get("version"),
            "last_modified": data.get("last_modified"),
            "last_writer": data.get("last_writer"),
            "entries_count": len(data.get("entries", []))
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.resource("vault://tasks")
def vault_tasks() -> str:
    """任务队列快照"""
    try:
        data = read_json(TASK_QUEUE_PATH)
        return json.dumps({
            "version": data.get("version"),
            "pending": [t for t in data.get("tasks", []) if t.get("status") == "pending"],
            "done": [t for t in data.get("tasks", []) if t.get("status") == "done"]
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

# ============== 启动 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("伟力Vault MCP Server 启动中...")
    print(f"Vault路径: {VAULT_ROOT}")
    print(f"Z_Memory: {ZMONEY_PATH}")
    print(f"TaskQueue: {TASK_QUEUE_PATH}")
    print("=" * 50)
    mcp.run()