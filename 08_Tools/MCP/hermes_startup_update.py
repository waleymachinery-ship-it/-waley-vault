import json
from datetime import datetime

# Update Z_Memory_Sync.json
zpath = r'D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json'
with open(zpath, encoding='utf-8') as f:
    z = json.load(f)

new_entry = {
    "id": "hermes-startup-2026-04-24",
    "agent": "hermes",
    "timestamp": "2026-04-24T18:30:00+08:00",
    "content": "[Hermes] MCP配置修正完成 - 2026-04-24 18:30. task-20260424-002 done. command路径从python改为完整路径. npx openclaw mcp list验证通过.",
    "tags": ["startup", "hermes", "mcp", "2026-04-24"],
    "confidence": 1
}

z['entries'].append(new_entry)
z['version'] = 'v242'
z['last_modified'] = '2026-04-24T18:40:00+08:00'
z['last_writer'] = 'hermes'
z['HERMES_STARTUP'] = '2026-04-24T18:30:00+08:00'

with open(zpath, 'w', encoding='utf-8') as f:
    json.dump(z, f, ensure_ascii=False, indent=2)
print('Z_Memory v242 updated')

# Append to daily log
dpath = r'D:\桌面文件\伟力机械知识库\memory\2026-04-24.md'
ts = datetime.now().strftime('%Y-%m-%d %H:%M')
entry = """

---

## Hermes 启动 + MCP配置修正完成 ({ts})

**task-20260424-002 (MCP配置修正):**
- 问题：python指向WindowsApps转发，无法启动MCP Server
- 修复：改用完整路径 C:/Users/pc/AppData/Local/Programs/Python/Python313/python.exe
- 验证：npx openclaw mcp list 显示 weili-vault ✅
- 状态：done

**待处理：**
- task-20260424-003：MiniMax微调API对接（Claude负责）
- MCP端到端验证：通过飞书测试 Jarvis → MCP 调用

*Hermes 启动确认完毕*
""".replace('{ts}', ts)

with open(dpath, 'a', encoding='utf-8') as f:
    f.write(entry)
print('Daily log updated')
