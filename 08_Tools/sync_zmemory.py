# Z_Memory_Sync.py - 用于写入 Z_Memory_Sync.json
# 用法: powershell.exe -File "D:\桌面文件\伟力机械知识库\08_Tools\sync_zmemory.py"

import json
import sys
from datetime import datetime

VAULT_PATH = r"D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json"

def read_zmemory():
    with open(VAULT_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_zmemory(data):
    with open(VAULT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_entry(agent_name, entry_content):
    data = read_zmemory()

    new_entry = {
        "id": f"{agent_name}-startup-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}",
        "agent": agent_name,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "content": entry_content,
        "tags": ["startup", "sync", datetime.now().strftime("%Y-%m-%d")],
        "confidence": 1.0
    }

    data['version'] += 1
    data['last_modified'] = new_entry['timestamp']
    data['last_writer'] = agent_name
    data['entries'].append(new_entry)

    write_zmemory(data)
    print(f"OK: v{data['version']}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sync_zmemory.py <agent> <content>")
        sys.exit(1)

    agent = sys.argv[1]
    content = sys.argv[2]

    try:
        add_entry(agent, content)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
