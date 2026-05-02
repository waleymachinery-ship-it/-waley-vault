#!/usr/bin/env python3
import json

# Update task_queue.json
path = r'D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json'
with open(path, encoding='utf-8') as f:
    d = json.load(f)

for t in d['tasks']:
    if t.get('id') == 'task-20260424-002':
        t['status'] = 'done'
        t['result'] = 'MCP配置已修正：command从python改为完整路径C:/Users/pc/AppData/Local/Programs/Python/Python313/python.exe，args路径正确，npx openclaw mcp list验证通过（weili-vault已注册）。问题原因：python指向WindowsApps转发，无法运行MCP服务器。'
        t['updated_at'] = '2026-04-24T18:35:00+08:00'
        print('Updated task-20260424-002')

d['version'] = d.get('version', 45) + 1
d['last_modified'] = '2026-04-24T18:35:00+08:00'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print('task_queue.json updated, version now:', d['version'])