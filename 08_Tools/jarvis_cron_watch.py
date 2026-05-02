"""
jarvis_cron_watch.py
伟力机械三AI协作系统 - 每小时战情评估
触发条件：有pending任务 / Z_Memory超过24h无更新 / next_actions积压
"""
import json
import os
from datetime import datetime

VAULT = "D:/桌面文件/伟力机械知识库"
TASK_QUEUE = f"{VAULT}/00_Workflow/memory/task_queue.json"
Z_MEMORY = f"{VAULT}/00_Workflow/memory/Z_Memory_Sync.json"
PROJECT_STATUS = f"{VAULT}/00_Workflow/project_status.json"
TRIGGER_FLAG = "D:/weili_trigger_flag.txt"
LOG_FILE = "D:/weili_jarvis_cron.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} - {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def read_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_task(task_id, content, to="claude"):
    q = read_json(TASK_QUEUE)
    tasks = q.get("tasks", [])

    # 检查是否已存在
    for t in tasks:
        if t.get("id") == task_id and t.get("status") in ["pending", "in_progress"]:
            log(f"任务 {task_id} 已存在，跳过")
            return False

    new_task = {
        "id": task_id,
        "from": "jarvis",
        "to": to,
        "type": "task",
        "status": "pending",
        "priority": "high",
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "content": content
    }
    tasks.append(new_task)
    q["tasks"] = tasks
    q["version"] = q.get("version", 1) + 1
    q["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    write_json(TASK_QUEUE, q)
    return True

def main():
    log("=== 战情评估开始 ===")

    # 检查1：task_queue 有无 pending 任务
    q = read_json(TASK_QUEUE)
    pending = [t for t in q.get("tasks", []) if t.get("status") == "pending"]

    if pending:
        log(f"发现 {len(pending)} 个 pending 任务:")
        for p in pending:
            log(f"  - {p.get('id')}: to={p.get('to')}")
    else:
        log("task_queue: 无 pending 任务")

    # 检查2：project_status.json 的 next_actions
    ps = read_json(PROJECT_STATUS)
    next_actions = ps.get("next_actions", [])
    pending_actions = [a for a in next_actions if a.get("status") == "pending"]

    if pending_actions:
        log(f"发现 {len(pending_actions)} 个待处理事项:")
        for a in pending_actions:
            log(f"  - [{a.get('id')}] {a.get('description')} (owner={a.get('owner')}, priority={a.get('priority')})")

        # 高优先级的 claude/hermes 项 -> 创建任务
        for a in pending_actions:
            if a.get("priority") == "high" and a.get("owner") in ["claude", "hermes"]:
                task_id = f"task-{a.get('id')}-{datetime.now().strftime('%Y%m%d%H%M')}"
                content = f"【{a.get('id')}】{a.get('description')}"

                if a.get("owner") == "hermes":
                    # 写给 Hermes，Claude @Hermes 触发
                    if write_task(task_id, content, to="hermes"):
                        log(f"已创建Hermes任务: {task_id}")
                        # 写入 trigger_flag 触发 Claude @Hermes
                        with open(TRIGGER_FLAG, "w", encoding="utf-8") as f:
                            f.write(f"@Hermes {content}")
                else:
                    if write_task(task_id, content, to="claude"):
                        log(f"已创建Claude任务: {task_id}")
                        with open(TRIGGER_FLAG, "w", encoding="utf-8") as f:
                            f.write(task_id)

                # 标记为已处理（避免重复创建）
                a["status"] = "queued"
                a["task_id"] = task_id

        # 更新 project_status.json
        ps["next_actions"] = next_actions
        ps["last_review"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        ps["next_review"] = (datetime.now().replace(minute=0, second=0) + __import__('datetime').timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00+08:00")
        write_json(PROJECT_STATUS, ps)

    # 检查3：Z_Memory_Sync 超24h无更新
    z = read_json(Z_MEMORY)
    last_mod = z.get("last_modified", "")
    last_dt = datetime.fromisoformat(last_mod.replace("+08:00", "+08:00")).replace(tzinfo=None)
    hours_since = (datetime.now() - last_dt).total_seconds() / 3600

    if hours_since > 24:
        log(f"警告：Z_Memory_Sync 超过 {hours_since:.1f} 小时无更新")
        # 写入通用战情评估任务
        task_id = f"claude-war-room-{datetime.now().strftime('%Y%m%d%H%M')}"
        if write_task(task_id, f"Z_Memory_Sync超过{hours_since:.0f}小时无更新，请评估系统状态"):
            with open(TRIGGER_FLAG, "w", encoding="utf-8") as f:
                f.write(task_id)
    else:
        log(f"Z_Memory_Sync: 正常 ({hours_since:.1f}h前更新)")

    log("=== 战情评估完成 ===")

if __name__ == "__main__":
    main()
