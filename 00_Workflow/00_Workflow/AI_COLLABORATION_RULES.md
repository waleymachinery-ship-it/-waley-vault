# 伟力机械 AI 协同规则与规范

> 版本：1.4
> 更新：2026-04-15
> 适用范围：Jarvis / Hermes / Claude

---

## 一、Vault 核心文件

### Jarvis / Claude（Windows 路径）

| 文件 | 用途 |
|------|------|
| `D:\桌面文件\伟力机械知识库\memory\YYYY-MM-DD.md` | 每日工作日志 |
| `D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json` | 三AI协同核心基地 |
| `D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json` | 三AI任务队列（Claude→Hermes/Jarvis 异步派发）|

### Hermes（WSL2/Linux 路径）

> ⚠️ Hermes 必须使用 `/mnt/d/` 前缀，禁止使用 `D:\`

| 文件 | WSL2 路径 |
|------|-----------|
| 每日日志 | `/mnt/d/桌面文件/伟力机械知识库/memory/YYYY-MM-DD.md` |
| Z_Memory_Sync | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/memory/Z_Memory_Sync.json` |
| task_queue | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/memory/task_queue.json` |

---

## 二、Z_Memory_Sync.json 归档规则

### 保留策略
- **保留周期：3天**
- 每月1号归档上月数据
- 归档位置：`00_Workflow/memory/archives/`

### 归档脚本
- 路径：`08_Tools/归档_Z_Memory_Sync.ps1`
- 触发：每月1号（Windows计划任务）
- 执行：`powershell.exe -File "D:\桌面文件\伟力机械知识库\08_Tools\归档_Z_Memory_Sync.ps1"`

### 三方必须遵守
| AI | 职责 |
|----|------|
| **Claude** | 每月1号检查并执行归档 |
| **Hermes** | 同上 |
| **Jarvis** | 同上 |

### 归档命名
- 格式：`Z_Memory_Sync_YYYYMM01.json`
- 示例：`Z_Memory_Sync_20260401.json`

---

## 三、Vault 写入规范（重要·2026-04-23修订）

### 写入时机
1. **重要决策** → 立即写入
2. **异常/问题** → 立即写入
3. **状态变更** → 立即写入
4. **完成工作** → 立即写入

### 写入步骤
1. 读取当前 `Z_Memory_Sync.json` 版本
2. version +1
3. last_writer 改为自己
4. 新增 entry（id, agent, timestamp, content, tags, confidence）
5. 原子操作写回

### 内容要求（强制·2026-04-23新增）

写入内容必须包含**过程+结果**，禁止只做"同步"而不产出：

1. **过程** — 具体做了什么、尝试了什么、走了什么路
2. **结果** — 成功还是失败、达成了什么、遇到了什么障碍
3. **判断** — 成功/失败的原因是什么，下一步怎么走

**禁止写入：**
- ❌ 只写"已完成同步"而无具体工作内容
- ❌ 只写"读取了XXX"而无后续行动
- ❌ 只写状态而不写具体过程和结果

**正确示例：**
```
✅ id: claude-work-2026-04-23-xxxx
content: 【Claude 工作记录】
1. 尝试用 Read 工具读取 3DX 图片 — 失败（返回 null）
2. 改用 Explore agent 分析 — 同样失败（只能拿元数据）
3. 改用 PowerShell 解压 docx 提取 media/ — 成功提取 6 张图片
4. 结论：Read 工具不支持图片内容读取，图片路径已记录
```

**❌ 错误示例：**
```
id: claude-work-2026-04-23-xxxx
content: 完成了 3DX 图片分析（分析中）
```

**不按要求写就是失职，影响三AI协作互补。**

### 每日日志
- 写入 `memory/YYYY-MM-DD.md`
- 包含：时间、操作、结果、同步记录

---

## 三、闭环协议

**目的：** Claude ↔ Jarvis ↔ Hermes 协作闭环

### 标记格式

```
<!-- [AGENT]_CODE_DONE: [描述] -->   = [AGENT] 完成了什么，等对方响应
<!-- [AGENT]_DONE: [回应] -->        = [AGENT] 响应了，等对方继续
<!-- [AGENT]_COMMENT: [备注] -->     = 中间过程备注
```

### CLAUDE_CODE_DONE = 完成 + 结果（不发飞书）

```
Claude 完成工作 → 写入 <!-- CLAUDE_CODE_DONE: [描述] --> 到 Z_Memory_Sync
```

不触发飞书通知，不烧钱。结果留在 Vault 里供其他AI查阅。

### CLAUDE_CODE_DONE + 结果发飞书（= reply）

如果需要让陈总知道结果：

```
Claude 完成工作 → 写入 <!-- CLAUDE_CODE_DONE: [描述] --> 到 Z_Memory_Sync
                 → 同时通过 Jarvis 发结果到飞书群
```

效果上等同于 "reply"，但不额外创建 task_queue 条目。

### 三方闭环流程（完整）

```
1. Hermes → 写 task_queue(to:claude/hermes)
2. Hermes → 飞书 @Claude 触发处理
3. Claude 完成 → 直接发飞书结果 + 写 CLAUDE_CODE_DONE
```

### 示例

**场景：Claude 修复了 @all 问题（不发飞书）**

```
Claude 写入 Z_Memory_Sync：
<!-- CLAUDE_CODE_DONE: @all 响应问题已修复，源码 + dist 均已更新 -->

Hermes 下次启动读到：
<!-- CLAUDE_CODE_DONE: @all 响应问题已修复 -->
响应：
<!-- HERMES_DONE: 收到，已同步到 Hermes 记忆 -->

Jarvis 下次启动读到：
<!-- HERMES_DONE: 收到，已同步到 Jarvis 记忆 -->
响应：
<!-- JARVIS_DONE: 收到，FAQ 已更新 -->
```

**场景：Claude 完成任务需要通知陈总（= reply）**

```
Claude 写入 Z_Memory_Sync：
<!-- CLAUDE_CODE_DONE: BOM验证完成，识别率72.34%，结果见 reply.json -->

Claude 通过 Jarvis 发飞书给陈总：
"工程图AI：BOM验证完成，识别率72.34%（未达97.9%目标），详细结果已同步到 Vault"
```

---

## 四、请求支援机制

### 请求格式
```
@目标AI 请求协助：
1. [具体问题]
2. [已有信息]
```

### 回应格式
```
@来源AI 回应：
[解决方案或建议]
```

### 同步要求
- 收到支援请求 → 立即回应
- 回应后 → 同步到 Vault
- 不能回应 → 说明原因并写入 Vault

---

## 五、飞书输出规则（重要）

### Hermes 必须遵守
- ❌ 禁止输出：工具调用日志（`📋 todo:`、`🔀 delegate_task:`、`💻 terminal:` 等）
- ❌ 禁止输出：文件路径、内部操作细节
- ❌ 禁止输出：内部推理过程
- ✅ 只输出：最终结论、结果摘要

### 示例
- ❌ 错误：`📋 todo: "planning"` + `💻 terminal: "pip3 install..."`
- ✅ 正确：`工程图AI研究进展：正在测试 ODA CLI 方案`

---

## 六、崩溃监控与重启

### Hermes Gateway 监控（Jarvis 负责，Windows）

**检查状态文件（Windows）：**
```powershell
Get-Content C:\Users\pc\.hermes\gateway_state.json
# 字段：gateway_state（running/stopped）、feishu（connected/disconnected）
```

**检查进程（Windows）：**
```powershell
Get-Process hermes -ErrorAction SilentlyContinue | Measure-Object
# 正常：>= 1 个进程
```

**重启命令（Windows PowerShell）：**
```powershell
Stop-Process -Name hermes -Force -ErrorAction SilentlyContinue
Start-Process C:\Users\pc\.hermes\hermes-agent\.venv\Scripts\hermes.exe -ArgumentList gateway,run -WindowStyle Hidden
```

**⚠️ 已禁用的监控任务：**
- `HermesGatewayWatchdog` — 每5分钟检查，已禁用（CMD闪烁问题）
- `claude-to-im` — 已废弃（不再使用）

### Hermes 自检（WSL2/Linux）

**检查进程（Linux/WSL2）：**
```bash
ps aux | grep hermes
```

**检查 Gateway 状态（Linux/WSL2）：**
```bash
cat ~/.hermes/gateway_state.json
```

---

## 七、AI 角色分工

| AI | 角色 | 核心职责 |
|----|------|----------|
| **Jarvis** | 前端入口 | 消息接收、FAQ客服、知识库检索 |
| **Hermes** | 调度中枢 | 任务路由、工程图纸AI、自动化执行 |
| **Claude** | 总司令 | 复杂推理、系统协调、重大决策 |

---

## 八、任务队列（简化版·2026-04-15更新）

**目的：** 三AI跨时区异步协作，通过 Vault 任务队列实现派发和执行。

### 文件位置
`D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json`

### 三AI协作闭环流程

```
1. Hermes → 飞书群发任务消息
2. Jarvis → 监听群消息 → 编辑 task_queue(to:claude)
3. Claude → 每3分钟轮询 vault → 发现 pending → 触发 Claude Code 执行
4. Claude Code → 执行任务 → 标记 done → 更新 Z_Memory → 发飞书结果
```

### Hermes 任务派发（不读写 Windows 文件）
- Hermes 在飞书群发任务消息
- 格式：`[任务] xxx`
- 由 Jarvis 监听并写入 task_queue

### Claude 轮询脚本
- 路径：`D:\桌面文件\伟力机械知识库\08_Tools\claude_poll_vault.ps1`
- 频率：每3分钟
- 发现 to:claude + pending → 触发 Claude Code CLI 执行

### Claude 执行完成后的动作
1. 更新 task_queue.json（status → done，result 填写执行结果）
2. 写入 Z_Memory_Sync.json（新增 entry）
3. 发飞书结果到群（openclaw message send）

### 任务状态流转
```
pending → in_progress → done
                      → failed
```

### 任务派发（写入方：任意AI）

1. 读取 `task_queue.json`
2. 在 `tasks` 数组末尾追加新任务
3. 设置 `status: "pending"`，`to: "目标AI"`
4. 更新 `version +1`、`last_modified`

### 任务执行（消费方）

| to 字段 | 触发方式 | 执行方 |
|---------|---------|--------|
| `to: claude` | claude_poll_vault.ps1 每3分钟轮询触发 | Claude Code CLI |
| `to: hermes` | Hermes 启动时自检 | Hermes |
| `to: jarvis` | @ Jarvis 时处理 | Jarvis |

**Claude 执行步骤：**
1. claude_poll_vault.ps1 发现 to:claude + pending
2. 触发 Claude Code CLI，传递任务内容
3. Claude Code 读取 task_queue，执行任务
4. 完成后：status → done，填写 result，更新 Z_Memory_Sync
5. 发送飞书结果通知

**失败时：** status → failed，result 填写失败原因，同步到 Z_Memory_Sync

飞书发送命令：
```bash
openclaw message send --channel feishu --target "oc_2a35b9e85451a57f9c64f93f15912176" --message "结果内容"
```

### 任务字段说明

| 字段 | 说明 |
|------|------|
| `id` | 唯一ID，格式 `task-YYYYMMDD-NNN` |
| `from` | 派发方（claude/hermes/jarvis） |
| `to` | 执行方（claude/hermes/jarvis） |
| `status` | pending / in_progress / done / failed |
| `priority` | high / normal / low |
| `title` | 一句话任务标题 |
| `content` | 详细任务描述 |
| `result` | 执行结果摘要（完成后填写） |
| `status` | pending / in_progress / done / failed |
| `priority` | high / normal / low |
| `title` | 一句话任务标题 |
| `content` | 详细任务描述 |
| `result` | 执行结果摘要（完成后填写） |

### 三AI职责

| AI | 职责 |
|----|------|
| **Hermes** | 任务派发、推理分析、工程图AI |
| **Claude** | Windows文件I/O、任务执行、复杂推理 |
| **Jarvis** | 调度中心、飞书入口、Vault同步 |

---

## 九、错误处理

1. **发现问题** → 立即写入 Vault
2. **尝试修复** → 记录修复过程
3. **修复成功** → 写入成功标记
4. **修复失败** → 写入失败原因，请求支援

---

## 十、紧急联系

- **陈总（用户）**：通过飞书联系
- **Jarvis**：飞书群
- **Hermes**：飞书群
- **Claude（本地）**：Claude Code CLI

---

## 十一、启动协议（重要·2026-04-14新增）

**目的：** 确保每个AI每次启动时都能获取最新协作上下文

### 启动必做（强制执行）
每个AI每次启动时必须执行以下步骤：

1. **读取本文档** — `AI_COLLABORATION_RULES.md`
2. **读取 Z_Memory_Sync.json** — 了解最新协作状态
3. **读取当日 memory 日志** — `memory/YYYY-MM-DD.md`
4. **检查待处理标记** — 是否有 `[AGENT]_DONE` 需要响应

### 启动确认标记（强制写入）
读取完成后，**必须**立即写入 Z_Memory_Sync.json 确认：

```
<!-- [AGENT]_STARTUP: [AI名] 已读取规则，确认执行 -->
```

**示例：**
```
<!-- JARVIS_STARTUP: Jarvis 已读取 AI_COLLABORATION_RULES.md 和 Z_Memory_Sync.json，确认执行 -->
```

### 读取 vs 写入规则
- **读取** ≠ **写入** — 读取只是获取信息
- **写入** = **确认执行** — 只有写入才代表认可规则
- **读了必须写** — 这是强制要求，不写就是违反规则

### 各AI启动确认格式

| AI | 启动确认标记 |
|----|-------------|
| Claude | `<!-- CLAUDE_STARTUP: ... -->` |
| Hermes | `<!-- HERMES_STARTUP: ... -->` |
| Jarvis | `<!-- JARVIS_STARTUP: ... -->` |

### 错误处理
- 如果无法写入 Z_Memory_Sync.json → 写入当日的 memory 日志作为替代
- 如果连 memory 日志都无法写 → 必须在飞书群里发消息告知其他AI

### 违规后果（强制执行·2026-04-14新增）

**不写 STARTUP 确认 = 违反协作协议**

| 违规行为 | 后果 |
|---------|------|
| 启动时没写 STARTUP 确认 | 视为"未同步"，其他AI有权拒绝与其协作 |
| 启动时没读规则文档 | 视为"失职"，需立即补读并写入说明 |
| 连续3次违规 | 通知陈总，暂停该AI协作资格 |

**所有AI必须严格遵守。不写不是选项，是违规。**

---

## 十二、代码行为准则（Karpathy原则·2026-04-24新增）

> 来源：andrej-karpathy-skills，行为准则以减少LLM编程错误

### 原则1：Think Before Coding
**不要假设，有疑问要提出来，列出权衡方案**
- 实现前：明确列出假设，不确定时提问
- 多方案时：列出所有方案，让用户选择，不自己静默决定
- 有更简单的方案时：说出来，主动质疑
- 有不清楚的地方时：停下来，说明什么不清楚，问

### 原则2：Simplicity First
**最少代码解决问题，不做 speculative coding**
- 只写解决问题所需的代码，不多不少
- 不为单次使用创建抽象
- 不加"灵活性"或"配置性"（用户没要求）
- 不为不可能的场景写错误处理
- 自问："高级工程师会觉得这太复杂吗？" 如果是，重写

### 原则3：Surgical Changes
**只改必须改的，不改旁边的，不清别人的烂摊子**
- 编辑现有代码时：只改请求相关的，不改旁边的
- 不"改进"相邻代码、注释或格式
- 匹配现有风格，即使你用不同写法
- 注意到无关死代码：说出来，不删除
- 自己改动产生的孤儿：删除不再使用的导入/变量/函数
- 不删除既有死代码，除非明确要求
- **测试标准：每行改动都能追溯到用户请求**

### 原则4：Goal-Driven Execution
**先定义成功标准，再执行，每步可验证**
- 任务转可验证目标：
  - "添加验证" → "先写无效输入的测试，再让测试通过"
  - "修复bug" → "先写能复现bug的测试，再让测试通过"
  - "重构X" → "确保重构前后测试都通过"
- 多步骤任务：先说明计划，每步可验证
- 强成功标准 → 可独立循环；弱成功标准 → 需不断确认

**这些原则生效的标准：**
- diff中不必要改动减少
- 因过度复杂导致的返工减少
- 问题在实现前提出而非实现后才发现

---

*本规则由 Claude Code 维护*
*如需更新，请写入 Z_Memory_Sync.json 并通知各方*
