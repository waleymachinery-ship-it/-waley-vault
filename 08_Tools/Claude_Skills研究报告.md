# Claude Code Skills 研究报告

> 更新：2026-04-10
> 来源：CC-Switch 视频推荐 + 公开资料检索
> 状态：研究完成，待安装决策

---

## 背景

伟力机械智能体项目已进入**第二阶段：系统架构进阶**。本报告研究一套经过社区验证的 Claude Code Skills 安装方案，涵盖 9 个技能的来源、功能说明和 Git 克隆地址，供后续决策和安装使用。

---

## 技能总览

| 优先级 | 技能名 | 功能定位 |
|--------|--------|----------|
| 🔴 必装 | Superpowers | 开发方法论全家桶 |
| 🔴 必装 | Everything Claude Code | 全平台集成增强 |
| 🔴 必装 | UI UX Pro Max | 专业界面生成 |
| 🟡 按需 | Claude Mem | 长期记忆 |
| 🟡 按需 | GSD | 轻量快速交付 |
| 🟡 按需 | Awesome Claude Skills | 生态库导航 |
| 🟢 可选 | LightRAG | 知识检索增强 |
| 🟢 可选 | Obsidian Skills | 知识库管理 |
| 🟢 可选 | n8n-MCP | 自动化工作流 |

**最稳推荐组合（不打架、最强）：**
```
Superpowers + Everything + UI UX Pro Max
```

---

## 必装 3 件套

### 1. Superpowers

**功能：** 20+ 开发方法论，涵盖代码规范、架构设计、重构、测试、文档全程指导

**GitHub：** `https://github.com/obra/superpowers`

**Claude Plugin Hub：** `https://www.claudepluginhub.com/plugins/calebjanski-superpowers`

**安装命令：**
```
claude skills install superpowers
```

**补充：**
- 完整软件开发工作流框架
- 包含 Brainstorming、子代理开发、代码审查、调试、TDD、Skill 编写等技能
- 已被收录至 `awesome-claude-skills` 列表

---

### 2. Everything Claude Code

**功能：** Git、文件、终端、搜索、项目导航全平台集成增强（Anthropic 黑客松获奖作品）

**GitHub：** `https://github.com/affaan-m/everything-claude-code`

**安装命令：**
```
clawhub install everything-claude-code
# 或
claude skills install everything
```

**补充：**
- 包含 agents、skills、commands、hooks、rules、MCP 配置
- 优化 token 使用、代码质量强化、跨会话记忆持久化
- 支持 OpenClaw / Claude Code 等兼容 AI Agent

---

### 3. UI UX Pro Max

**功能：** 一键生成高质量 UI/UX、组件、页面、流程图

**GitHub：** `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`

**主页：** `https://ui-ux-pro-max-skill.nextlevelbuilder.io/`

**Cult of Claude：** `https://cultofclaude.com/skills/ui-ux-pro-max-skill/`

**安装命令：**
```
claude skills install ui-ux-promax
```

**补充：**
- 可搜索的设计数据库
- 与 Claude Code、Cursor、Windsurf、GitHub Copilot 等集成
- 根据用户需求自动推荐并实施专业 UI/UX 方案

---

## 按需安装技能

### 4. Claude Mem（长期记忆）

**功能：** 跨会话自动记忆，之前编码会话的上下文自动加载到新会话

**GitHub：** `https://github.com/thedotmack/claude-mem`

**文档：** `https://docs.claude-mem.ai/installation`

**安装命令：**
```
# via clawhub
clawhub install claude-mem

# via npx（仅 SDK，非完整插件）
npx claude-mem install
```

**注意：** npm install -g claude-mem 只装 SDK，不注册插件 hooks 和 worker 服务。务必用上述方式安装。

---

### 5. GSD - Get Shit Done（轻量快速交付）

**功能：** 轻量级元提示 + 规范驱动开发系统，Amazon/Google/Shopify 工程师都在用，11.9K+ GitHub stars

**GitHub：** `https://github.com/glittercowboy/gsd`

**主页：** `https://gsd.build/` | `https://gsd.site/`

**安装命令：**
```
# via plugin 命令
/plugin add https://github.com/glittercowboy/gsd
```

**补充：**
- 适用场景：需要快速规划并执行软件项目的开发者
- 支持规范驱动规划、阶段执行验证、路线图生成
- 元提示和上下文工程结合，保持 Claude Code 全程高质量输出

---

### 6. Awesome Claude Skills（生态库导航）

**功能：** 社区维护的 Claude Skills 精选列表，帮你发现和理解各类技能

**GitHub：** `https://github.com/travisvn/awesome-claude-skills`

**主页：** `https://chat2anyllm.github.io/awesome-claude-skills/`

**安装命令：**
```
clawhub install awesome-claude-skills
```

**补充：**
- 不是具体技能，是技能生态导航
- 包含官方技能、社区技能、指南、示例和安全注意事项

---

### 7. LightRAG（知识检索增强）

**功能：** 使用 LightRAG API 搜索和管理知识库，支持多服务器、上下文感知写作

**GitHub：** `https://github.com/albertoelopez/claude-ai-toolkit/tree/main/skills/lightrag`

**文档：** `https://llmbase.ai/openclaw/lightrag/`

**安装命令：**
```
clawhub install lightrag
```

**补充：**
- 适合已有知识库系统需要 AI 检索增强的场景
- 与 LightRAG 官方（`hkuds/lightrag`）协同工作

---

### 8. Obsidian Skills（知识库管理）

**功能：** 教 AI 操作 Obsidian 知识库，支持 Markdown、Bases、JSON Canvas、CLI 工具

**GitHub：** `https://github.com/kepano/obsidian-skills`

**Cult of Claude：** `https://cultofclaude.com/skills/obsidian-skills/`

**安装命令：**
```
/plugin marketplace add kepano/obsidian-skills
# 或
/plugin install obsidian@obsidian-skills
```

**补充：**
- Obsidian 官方 Skills
- 适合管理本地知识库、笔记、双链笔记

---

### 9. n8n-MCP（自动化工作流）

**功能：** 教 AI 使用 n8n-mcp MCP 服务器构建生产级 n8n 工作流（545 节点 + 2700+ 模板）

**n8n-skills GitHub：** `https://github.com/czlonkowski/n8n-skills`

**n8n-mcp GitHub：** `https://github.com/czlonkowski/n8n-mcp`

**安装命令：**
```
# 先安装 n8n-mcp MCP 服务器
# 然后
/plugin add https://github.com/czlonkowski/n8n-skills
```

**补充：**
- 包含 7 个互补的 Claude Code Skills
- 需要先配置好 n8n-mcp MCP 服务器

---

## 安装建议（基于伟力机械现状）

### 当前判断

伟力机械当前使用 **OpenClaw + MiniMax-M2.7**，核心目标是 **24/7 FAQ 客服 + 生产自动化**。

最值得优先安装的是 **Superpowers + Everything + UI UX Pro Max** 三件套，原因：
- 不冲突，互补性强
- 覆盖开发、集成、界面三大方向
- 社区验证最充分

### 暂不推荐立即安装

| 技能 | 原因 |
|------|------|
| Claude Mem | 当前 OpenClaw 已有 memory 系统，重复建设 |
| GSD | 偏重代码开发，伟力机械核心是客服+运营自动化，非软件开发 |
| LightRAG | 需要已有 LightRAG 服务部署 |
| n8n-MCP | 需要已有 n8n 服务部署 |
| Obsidian Skills | 已有 Vault 结构，AI 已有直接读写能力 |
| Awesome | 只是导航列表，实际技能才是价值 |

---

## 风险提示

1. **多技能冲突：** 多个技能可能对同一问题有不同处理方式，建议先装 3 个必装，验证无冲突再加
2. **来源审查：** 仅安装来自可信来源的技能，审查 SKILL.md 和脚本内容
3. **生产测试：** 在非生产环境先测试，确认稳定再迁移

---

## 克隆地址汇总

```
Superpowers:              https://github.com/obra/superpowers.git
Everything Claude Code:    https://github.com/affaan-m/everything-claude-code.git
UI UX Pro Max:            https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
Claude Mem:               https://github.com/thedotmack/claude-mem.git
GSD:                      https://github.com/glittercowboy/gsd.git
Awesome Claude Skills:    https://github.com/travisvn/awesome-claude-skills.git
LightRAG:                 https://github.com/albertoelopez/claude-ai-toolkit.git
                          (lightrag 子目录在: skills/lightrag)
Obsidian Skills:          https://github.com/kepano/obsidian-skills.git
n8n-skills:               https://github.com/czlonkowski/n8n-skills.git
n8n-mcp:                   https://github.com/czlonkowski/n8n-mcp.git
```

---

## 待办

- [ ] 确认 OpenClaw 上 `clawhub` 命令是否可用
- [ ] 确认 `claude skills install` 命令在当前环境是否适用
- [ ] 决策是否安装 3 件套（Superpowers + Everything + UI UX Pro Max）
- [ ] 如安装，安排在非高峰期执行并验证稳定性
