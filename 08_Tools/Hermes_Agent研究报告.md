# Hermes Agent 研究报告

> 研究日期：2026-04-10
> 信息来源：GitHub API / NousResearch 官方文档
> 仓库：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
> 状态：研究完成，不下载不安装

---

## 一、项目概述

**Hermes Agent** 是由 [Nous Research](https://nousresearch.com) 开发的一款自进化 AI Agent 框架，核心理念是 **"The agent that grows with you"**——一个随着使用不断学习和进化的 AI 伙伴。

| 项目 | 信息 |
|------|------|
| GitHub | `NousResearch/hermes-agent` |
| Stars | **49,231** ⭐ |
| Forks | 6,334 |
| 语言 | Python |
| 版本 | 0.8.0 |
| License | MIT |
| 官方文档 | https://hermes-agent.nousresearch.com/docs/ |
| 主页 | https://hermes-agent.nousresearch.com |

**与 OpenClaw 的关系：** Hermes 是 OpenClaw 的"升级版"或"继承者"，官方提供从 OpenClaw 一键迁移的功能，支持导入 SOUL.md、Memories、Skills、API Keys 等所有配置。

---

## 二、核心定位

Hermes 介于**通用 AI 框架**和**成品应用**之间：
- 不是从零搭建 Agent 的 SDK
- 而是拿起来就能用的完整 AI 助手产品，同时支持深度定制

它的定位更接近一个**自带技能生态的 AI 工作站**，而非单纯的模型封装或工具库。

---

## 三、核心特性

### 3.1 自进化学习循环（Built-in Learning Loop）

这是 Hermes 最大的差异化特点：

| 能力 | 说明 |
|------|------|
| **从经验中创建技能** | 每次完成复杂任务后，Agent 自动总结并生成可复用的 Skill |
| **使用中自我改进** | Skills 在使用过程中持续优化 |
| **知识持久化** | 自动将学到的知识沉淀到知识库 |
| **历史会话搜索** | FTS5 全文搜索 + LLM 摘要，跨会话记忆召回 |
| **用户建模** | 通过 [Honcho](https://github.com/plastic-labs/honcho) 实现用户画像，持续理解用户偏好 |

简单说：**用得越多，它越懂你**。

### 3.2 支持所有主流模型（Model-Agnostic）

| 提供商 | 说明 |
|--------|------|
| Nous Portal | Nous Research 自有模型 |
| OpenRouter | 200+ 模型 |
| z.ai / GLM | 智谱 / GLM 系列 |
| Kimi / Moonshot | 月之暗面模型 |
| **MiniMax** | ✅ 已列出，伟力机械当前使用 |
| OpenAI | GPT 系列 |
| Anthropic | Claude 系列 |
| 自定义端点 | 任何兼容 OpenAI API 格式的 endpoint |

切换模型只需要一个命令 `hermes model`，**无需改动代码**。

### 3.3 完整终端界面（TUI）

- 多行编辑、斜杠命令自动补全
- 对话历史、随时中断并重定向
- 流式工具输出

### 3.4 消息网关（Messaging Gateway）

支持以下平台（从一个网关进程同时接入）：

| 平台 | 能力 |
|------|------|
| Telegram | 文字 + 语音转录 |
| Discord | 文字 + 语音 |
| Slack | 文字 |
| WhatsApp | 文字 |
| Signal | 文字 |
| Email | 邮件收发 |
| Home Assistant | 智能家居控制 |

语音备忘录传输、跨平台对话连续性。

### 3.5 内置 Cron 定时任务

- 用自然语言描述定时任务
- 自动调度并在对应平台推送结果
- 适用场景：每日报告、每周审计、定时备份等

### 3.6 并行子代理（Subagents）

- 派生出隔离的子 Agent 并行执行工作流
- 编写 Python 脚本通过 RPC 调用工具
- 多步骤管道压缩为零上下文成本的调用

### 3.7 研究级功能

- 批量轨迹生成（Batch Trajectory Generation）
- Atropos RL 环境
- 轨迹压缩，用于训练下一代工具调用模型

---

## 四、安装环境需求

### 4.1 操作系统支持

| 系统 | 支持情况 |
|------|----------|
| Linux | ✅ 官方支持 |
| macOS | ✅ 官方支持 |
| **Windows** | ❌ 原生不支持，需通过 WSL2 |
| Android / Termux | ✅ 官方支持（有独立安装指引）|
| WSL2 | ✅ 官方支持 |

### 4.2 Python 版本要求

```
requires-python = ">=3.11"
```

### 4.3 系统依赖

| 依赖 | 说明 |
|------|------|
| curl | 用于执行安装脚本 |
| git | 用于克隆仓库（可选）|
| WSL2（Windows） | 须先安装 WSL2 再运行安装脚本 |

### 4.4 硬件需求

| 场景 | 最低配置 |
|------|----------|
| 轻量使用 | $5 VPS 即可运行 |
| 深度使用 | GPU 集群或 serverless（Daytona / Modal）|
| 空闲时 | Daytona / Modal 提供 serverless 持久化，休眠几乎零成本 |

### 4.5 可选功能对应的额外依赖

| 功能模块 | 安装方式 |
|----------|----------|
| 消息平台（Telegram/Discord/Slack等）| `pip install hermes-agent[messaging]` |
| 定时任务 | `pip install hermes-agent[cron]` |
| 语音合成（Edge TTS） | `pip install hermes-agent[voice]` |
| ElevenLabs TTS | `pip install hermes-agent[tts-premium]` |
| MCP 扩展 | `pip install hermes-agent[mcp]` |
| 服务器部署（Modal）| `pip install hermes-agent[modal]` |
| 服务器部署（Daytona）| `pip install hermes-agent[daytona]` |
| 飞书 | `pip install hermes-agent[feishu]` |
| 钉钉 | `pip install hermes-agent[dingtalk]` |
| **全部扩展** | `pip install hermes-agent[all]` |

> 注：Matrix（加密通讯）因 libolm 兼容问题已从 `[all]` 中排除，需手动单独安装。

### 4.6 核心依赖（Base）

```
openai >= 2.21.0, < 3
anthropic >= 0.39.0, < 1
python-dotenv >= 1.2.1, < 2
fire >= 0.7.1, < 1
httpx >= 0.28.1, < 1
rich >= 14.3.3, < 15
tenacity >= 9.1.4, < 10
pyyaml >= 6.0.2, < 7
requests >= 2.33.0, < 3        # CVE-2026-25645 已修复
jinja2 >= 3.1.5, < 4
pydantic >= 2.12.5, < 3
prompt_toolkit >= 3.0.52, < 4
exa-py >= 2.9.0, < 3          # 网页搜索
firecrawl-py >= 4.16.0, < 5   # 网页爬取
parallel-web >= 0.4.2, < 1
fal-client >= 0.13.1, < 1
edge-tts >= 7.2.7, < 8         # 免费 TTS，无需 API Key
PyJWT[crypto] >= 2.12.0, < 3  # CVE-2026-32597 已修复
```

---

## 五、快速安装

### 5.1 一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装器会自动检测平台（Linux / macOS / WSL2 / Termux）并完成对应配置。

### 5.2 开发者模式安装

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
python -m pytest tests/ -q
```

### 5.3 安装后配置

```bash
source ~/.bashrc          # 重载 shell（或 source ~/.zshrc）
hermes                    # 启动聊天！
hermes model              # 选择 LLM 提供商和模型
hermes tools              # 配置启用的工具
hermes config set         # 设置各项配置
hermes gateway            # 启动消息网关（Telegram、Discord 等）
hermes setup              # 运行完整设置向导
```

---

## 六、OpenClaw 迁移指南

Hermes 官方支持从 OpenClaw 无痛迁移，迁移内容包括：

| 迁移项 | 说明 |
|--------|------|
| SOUL.md | 角色设定文件 |
| Mem / Memories | MEMORY.md 和 USER.md |
| Skills | 用户创建的 Skills |
| Command allowlist | 命令审批规则 |
| Messaging 配置 | 平台配置、允许用户名单 |
| API Keys | 已白名单的密钥 |
| TTS 资源 | 语音文件 |
| AGENTS.md | 工作区指令 |

迁移命令：
```bash
hermes claw migrate              # 交互式完整迁移
hermes claw migrate --dry-run   # 预览迁移内容
hermes claw migrate --preset user-data    # 不迁移密钥
hermes claw migrate --overwrite  # 覆盖已有冲突
```

---

## 七、与伟力机械项目的关联分析

### 7.1 当前状态对比

| 维度 | 伟力机械（OpenClaw） | Hermes Agent |
|------|---------------------|-------------|
| 定位 | AI 助手 + 消息网关 | 自进化的完整 AI Agent |
| 微信接入 | ✅ openclaw-weixin 插件 | ❌ 无微信插件（官方）|
| 自进化能力 | ❌ 无 | ✅ 内置学习循环 |
| 模型支持 | MiniMax 等 | 200+ 模型，含 MiniMax |
| 部署难度 | 低 | 中（需 Python 3.11+）|
| 技能系统 | SKILL.md 生态 | 自带 Skills Hub + 自创建 |
| OpenClaw 迁移 | — | ✅ 官方支持一键迁移 |

### 7.2 关键差异点

**Hermes 的优势：**
- 自进化能力：随着使用越来越懂用户，无需人工维护知识库
- 消息网关更完善：Telegram/Discord/Slack 等开箱即用
- 社区活跃度高（49k stars，6k+ forks）
- 定时任务、并行子 Agent 等企业级功能
- OpenClaw 迁移官方支持

**Hermes 的劣势：**
- 无微信插件（暂不支持）
- 不支持原生 Windows（需要 WSL2）
- Python 3.11+ 强制要求
- 学习曲线比 OpenClaw 高
- 对于"24/7 FAQ 客服"场景过于复杂

### 7.3 评估结论

| 场景 | 建议 |
|------|------|
| 保持当前 OpenClaw 方案 | 继续使用，伟力机械 Phase 1 已验证可行 |
| 未来迁移探索 | 可关注 Hermes 后续微信支持情况 |
| 技能系统升级 | 可研究 Hermes 的 Skills Hub 生态 |
| 不建议现阶段切换 | 微信接入未解决，功能复杂度高于当前需求 |

---

## 八、克隆地址汇总

```
# 仓库克隆
HTTPS:  https://github.com/NousResearch/hermes-agent.git
SSH:    git@github.com:NousResearch/hermes-agent.git
Git:    git://github.com/NousResearch/hermes-agent.git

# 官方文档
文档:   https://hermes-agent.nousresearch.com/docs/
主页:   https://hermes-agent.nousresearch.com

# 社区
Discord: https://discord.gg/NousResearch
Issues: https://github.com/NousResearch/hermes-agent/issues
Discussions: https://github.com/NousResearch/hermes-agent/discussions

# Nous Research
官网:   https://nousresearch.com
Portal: https://portal.nousresearch.com
```

---

## 九、关键文件参考

| 文件 | 说明 |
|------|------|
| README.md | 项目介绍和快速开始 |
| pyproject.toml | 依赖配置，Python >= 3.11 |
| scripts/install.sh | 官方安装脚本 |
| docs/ | 完整官方文档 |

---

## 十、待办事项

- [ ] 持续关注 Hermes 官方是否新增微信（WeChat）插件支持
- [ ] 若未来迁移，确保先在测试环境验证 OpenClaw → Hermes 迁移流程
- [ ] 评估 Hermes Skills Hub 生态是否能为伟力机械知识库体系带来额外价值
