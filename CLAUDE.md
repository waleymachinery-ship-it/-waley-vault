# CLAUDE.md — 伟力机械知识库

> 伟力机械 AI 协作项目行为准则

---

## 核心规范

**Karpathy 编程原则（强制执行）：**

1. **Think Before Coding** — 不要假设，有疑问要提出，列出权衡方案
2. **Simplicity First** — 最少代码解决问题，不做 speculative coding
3. **Surgical Changes** — 只改必须改的，不改旁边的，不清别人的烂摊子
4. **Goal-Driven Execution** — 先定义成功标准，再执行，每步可验证

详细规范见：`00_Workflow/AI_COLLABORATION_RULES.md`

**AI 执行标准（必须遵循）：** `00_Workflow/AGENTS_EXECUTION_RULES.md`

---

## 项目结构

```
D:\桌面文件\伟力机械知识库\
├── 00_Workflow/          # 工作流与协作规则
├── 01_产品体系/           # 产品介绍
├── 02_工艺知识/           # 工艺参数
├── 03_运营体系/           # 生产排程
├── 04_销售工具/           # 报价话术
├── 05_战略资料/           # 并购材料
├── 06_市场运营/           # SEO/落地页
├── 06_Supplier/          # 供应商管理
├── 07_BP_Invest/         # 投资资料
├── 08_Tools/             # 工具脚本
├── FAQ/                  # 知识库
├── memory/               # 每日工作日志
├── AI系统/               # 模型训练/后端（开发目录）
└── Claude/               # Claude Code 专属文档
```

---

## 三AI架构（当前真实状态）

| AI | 位置 | 角色 | 核心职责 |
|----|------|------|----------|
| **Jarvis** | 本地 Windows | 消息入口 | 飞书/微信接入、人机交互、FAQ客服 |
| **Hermes** | 云端 Linux（106.53.207.188） | 执行中枢 | AI 推理、工程图AI、云端会话、记忆管理 |
| **Claude** | 本地 Claude Code | 协调大脑 | 复杂推理、系统规划、重大决策 |

### Hermes 三路调用入口

Hermes（云端）通过三个入口被调用：

1. **飞书 Bot**（cli_a95d06761f385bcb）— 24/7 在线，用户直接在飞书对话
2. **V8 悬浮助手** — 设备管理平台右侧的 AI 助手浮窗，调用 Hermes 会话
3. **waley-agent-backend AI诊断** — 设备故障在线诊断，调用 Hermes 会话

### Hermes 云端部署信息

| 项目 | 信息 |
|------|------|
| 服务器 | 106.53.207.188（OpenCloudOS Linux） |
| 服务端口 | SSH 22，密码 Waley2026! |
| Hermes 运行目录 | `/usr/local/lib/hermes-agent/` |
| 知识库 | `/root/waley-vault/` |
| 记忆系统 | memtensor（memos-plugin，云端） |
| 进程管理 | systemd（hermes-gateway.service） |
| 飞书 Bot | cli_a95d06761f385bcb |
| 启动用户 | root |
| SOUL.md 位置 | `/root/.hermes/SOUL.md` |

### Hermes 重启命令

```bash
# SSH 连接
ssh root@106.53.207.188 -p 22

# 重启 Hermes
systemctl restart hermes-gateway

# 查看状态
systemctl status hermes-gateway

# 查看日志
journalctl -u hermes-gateway --no-pager -n 50
```

---

## 三AI协作协议

**协作协议：** `00_Workflow/AI_COLLABORATION_RULES.md`

**数据流：**
```
用户 → 飞书 → Jarvis（本地）→ Hermes（云端）
                              ↓
                        memtensor 记忆
                              ↓
                        /root/waley-vault/ 知识库
```

---

## claude-mem 记忆系统（本地）

claude-mem 为本地 Claude Code 提供持久化记忆。

| 功能 | 说明 |
|------|------|
| 记忆视图 | http://localhost:37777 |
| 搜索历史 | `/mem-search` |
| 工作线程 | `npx claude-mem start` |

**⚠️ 启动后必须验证 health，不验证不算真正起来：**
```bash
curl -s localhost:37777/health
# 必须返回 {"status":"ok"} 才算完成
# 如果不是 ok，删除 ~/.claude-mem/worker.pid 后重拉
```

---

## Claude 启动协议（每次启动必须执行）

> 版本：v1.1 | 日期：2026-04-29
> 背景：Claude 每次启动是空白状态，必须主动对齐 Hermes/Jarvis 的上下文才能真正协同

### 第一步：读取 Z_Memory 核心基地
```
D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json
```
- 确认 version 和 last_modified
- 确认 HERMES_STARTUP / JARVIS_STARTUP 时间戳（判断其他AI是否在线）

### 第二步：读取当日日志
```
D:\桌面文件\伟力机械知识库\memory\YYYY-MM-DD.md
```
- 了解今天已发生的事情

### 第三步：检查任务队列
```
D:\桌面文件\伟力机械知识库\00_Workflow\memory\task_queue.json
```
- 筛选 `status: "pending"` 且 `to: "claude"` 的任务
- 执行后标记 done + 填写 result

### 第四步：验证 claude-mem health
```bash
curl -s localhost:37777/health
# 必须返回 {"status":"ok"} 才算真正起来
```

### 第五步：写入启动确认
在 Z_Memory 或当日日志末尾写入：
```
<!-- CLAUDE_STARTUP: Claude Code 已读取规则，确认执行 -->
```

**⚠️ 读了 ≠ 写了，不写就是违反协作规则。**

---

## 联系方式

汕头市伟力塑料机械厂有限公司
- 地址：广东省汕头市金平区大学路290号
- 负责人：陈思远
