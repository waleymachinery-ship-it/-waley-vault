# 三AI启动检查清单

> 版本：1.3
> 创建：2026-04-14
> 更新：2026-04-15（三AI协作闭环重构：Hermes发群，Jarvis写task_queue，Claude轮询执行）
> 要求：三个AI（Claude/Hermes/Jarvis）启动时必须执行

---

## 启动必做流程

### 第一步：读取启动清单
路径：`D:\桌面文件\伟力机械知识库\00_Workflow\TRI_AI_STARTUP_CHECKLIST.md`（v1.3）

### 第二步：读取规则文档
路径：`D:\桌面文件\伟力机械知识库\00_Workflow\AI_COLLABORATION_RULES.md`（v1.5）

### 第三步：读取核心基地
路径：`D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json`

### 第四步：读取当日日志
路径：`D:\桌面文件\伟力机械知识库\memory\YYYY-MM-DD.md`

### 第五步：检查任务队列
路径：`D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json`

| AI | 检查条件 |
|----|---------|
| **Claude** | `status: "pending"` 且 `to: "claude"` → claude_poll_vault.ps1 轮询触发执行 |
| **Hermes** | `status: "pending"` 且 `to: "hermes"` → 启动时自检执行 |
| **Jarvis** | `status: "pending"` 且 `to: "jarvis"` → 被 @ 时执行 |

执行完成后：`status → "done"`，`result` 填入结果摘要，`updated_at` 更新

### 第六步：写入启动确认（读了必须写）
格式：
```
<!-- [AGENT]_STARTUP: [AI名] 已读取规则，确认执行 -->
```

**⚠️ 重要规则：读取 ≠ 写入，必须明确写入 STARTUP 确认才算完成启动流程。不写就是违反规则。**

---

## 三AI协作闭环（v1.3）

```
1. Hermes → 飞书群发任务消息
2. Jarvis → 监听群消息 → 编辑 task_queue(to:claude)
3. Claude → 每3分钟轮询 vault → 发现 pending → 触发 Claude Code 执行
4. Claude Code → 执行任务 → 标记 done → 更新 Z_Memory → 发飞书结果
```

### Hermes 职责
- 发任务到飞书群（不读写 Windows 文件）
- 格式：`[任务] xxx`

### Jarvis 职责
- 监听飞书群消息
- 将 Hermes 的任务写入 task_queue

### Claude 职责
- 轮询 vault 执行 pending 任务
- 完成后发飞书通知陈总

---

## 各AI职责

| AI | 启动后检查 | 启动写入 | 工作完成写入 |
|----|-----------|---------|------------|
| **Claude** | HERMES_DONE, JARVIS_DONE | CLAUDE_STARTUP | CLAUDE_CODE_DONE + 发飞书 |
| **Hermes** | CLAUDE_CODE_DONE, JARVIS_DONE | HERMES_STARTUP | 发飞书群消息 |
| **Jarvis** | CLAUDE_CODE_DONE, HERMES_DONE | JARVIS_STARTUP | JARVIS_DONE |

---

## 关键文件路径

### Jarvis / Claude（Windows）

| 文件 | 路径 |
|------|------|
| 启动清单 | `D:\桌面文件\伟力机械知识库\00_Workflow\TRI_AI_STARTUP_CHECKLIST.md` |
| AI协同规则 | `D:\桌面文件\伟力机械知识库\00_Workflow\AI_COLLABORATION_RULES.md` |
| Z_Memory_Sync | `D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json` |
| 每日日志 | `D:\桌面文件\伟力机械知识库\memory\YYYY-MM-DD.md` |
| 任务队列 | `D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json` |
| Claude轮询脚本 | `D:\桌面文件\伟力机械知识库\08_Tools\claude_poll_vault.ps1` |

### Hermes（WSL2/Linux）

> ⚠️ Hermes 运行在 WSL2，必须使用 `/mnt/d/` 前缀，不能用 `D:\`

| 文件 | WSL2 路径 |
|------|-----------|
| 启动清单 | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/TRI_AI_STARTUP_CHECKLIST.md` |
| AI协同规则 | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/AI_COLLABORATION_RULES.md` |
| Z_Memory_Sync | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/memory/Z_Memory_Sync.json` |
| 每日日志 | `/mnt/d/桌面文件/伟力机械知识库/memory/YYYY-MM-DD.md` |
| 任务队列 | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/memory/task_queue.json` |

**路径错误写法（禁止使用）：**
- `D:\桌面文件\...` — Windows 路径，WSL2 不识别
- `/d/桌面文件\...` — Git Bash / WSL1 写法
- `/c/Users\...` — WSL2 里 C盘 是 `/mnt/c/`

---

## 飞书群信息

| 群名 | ID |
|------|-----|
| 老板是疯子 | `oc_2a35b9e85451a57f9c64f93f15912176` |

---

## 各AI启动协议文档

| AI | 启动协议文档 |
|----|-------------|
| **Claude** | `CLAUDE.md` — Claude 启动协议章节（v1.0, 2026-04-26） |
| **Hermes** | `.hermes/skills/hermes/tri-ai-startup-checklist/SKILL.md` |
| **Jarvis** | — |

*本清单由 Claude Code 维护*
*最后更新：2026-04-26*

<!-- CLAUDE_STARTUP: Claude Code 已读取规则，确认执行 -->
