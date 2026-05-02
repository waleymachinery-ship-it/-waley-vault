# Hermes 系统配置记忆

**更新时间：** 2026-04-18 14:30
**当前Session:** Feishu (老板是疯子) — 2026-04-18 下午
**项目状态：** Phase 2 故障排查系统开发中 + 官网SEO收尾

---

## 一、身份与运行环境

| 项目 | 值 |
|------|-----|
| 角色 | Hermes - 本地推理中枢 |
| 当前Session | Feishu (老板是疯子) |
| 运行环境 | **WSL2** (`Linux DESKTOP-TN08JIQ 6.6.87.2-microsoft-standard-WSL2`) |
| 主机名 | DESKTOP-TN08JIQ |
| D盘路径 | `/mnt/d/桌面文件/...` (WSL2) |
| PowerShell | ❌ 不可用 |

**⚠️ 环境会在sessions之间切换（WSL2 ↔ Git Bash），每次启动必须 `uname -a` 确认**

---

## 二、启动检查清单（每次必执行）

```
【启动时按顺序执行】
1️⃣ 加载 hermes-file-access-limitations → uname -a 确认环境
2️⃣ 加载 windows-python-execution → 禁止 python3 -c
3️⃣ 加载 hermes-feishu-output-rule → 飞书只发结论
4️⃣ 执行 tri-ai-startup-checklist → 三AI同步
```

---

## 三、核心技能（已固化）

| 技能 | 作用 | 违规后果 |
|------|------|---------|
| hermes-file-access-limitations | 文件访问路径规范 + 环境判断 | 文件写到错误位置 |
| windows-python-execution | Python脚本执行规范 | 触发命令审批弹窗 |
| hermes-feishu-output-rule | 飞书输出铁律 | 刷屏暴露内部细节 |
| hermes-autonomous-startup | 自主启动流程（包含上面3个） | — |
| tri-ai-startup-checklist | 三AI启动检查清单 | 三AI协同断裂 |

**启动时必须先加载以上技能，不允许跳过**

---

## 四、Python 环境

### Python313（系统级，有 ezdxf）
- 路径：`C:\Users\pc\AppData\Local\Programs\Python\Python313\python.exe`
- ezdxf：✅ 已安装
- **可读DXF文件，不能读DWG**

### Hermes-agent venv（Hermes运行时）
- 路径：`C:\Users\pc\.hermes\hermes-agent\.venv\Scripts\python.exe`
- ezdxf：❌ 没有
- **执行Python脚本必须用Python313路径**

---

## 五、Vault 知识库路径

| 资源 | 路径 |
|------|------|
| 根目录 | `/mnt/d/桌面文件/伟力机械知识库/` |
| 当日日志 | `/mnt/d/桌面文件/伟力机械知识库/memory/2026-04-18.md` |
| 任务队列 | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/memory/task_queue.json` |
| 核心同步 | `/mnt/d/桌面文件/伟力机械知识库/00_Workflow/memory/Z_Memory_Sync.json` |

---

## 六、当前项目状态

### 🚀 Phase 2：故障排查数据收集系统（进行中）

**项目背景：** 官网AI客服需要更完善的故障知识库支撑

**里程碑：** 6周完成（截止 2026-05-30）

**P0任务（立即启动）：**
- P0-1：故障信息收集表单设计
- P0-2：故障处理过程记录规范
- P0-3：故障知识库FAQ自动化更新

**P1任务（第二周）：**
- P1-1：Phase 2 自动归档系统
- P1-2：FAQ自动更新机制

---

### ✅ 官网SEO + 客服AI（主体已完成）

**今日完成（2026-04-18）：**
- sitemap.xml 生成 ✅ → `06_市场营销/SEO落地页内容/sitemap.xml`
- 官网V8响应式修复 ✅ → `06_市场营销/SEO落地页内容/伟力机械官网_V8版本.html`
- 知乎引流文章6篇广告清理 ✅ → 保留伟力/waley.cn/WLA-WLU-WLH，删除推销话术

**V8修复内容：**
- 汉堡菜单JS（☰/✕ 点击切换）
- nav-open 移动端样式
- header 高度手机端 override
- logo 尺寸手机端限制（max 60px）
- Hero h1 手机字号（28px）
- 聊天窗口手机宽度（calc(100vw - 30px)）

**待处理：**
- Leads推送接口（等用户提供接口格式）
- 官网手机端实测复查（V8已修复，待用户实测）
- 官网部署（等全部完成后统一上线）

---

### 三AI分工

| AI | 职责 | 当前状态 |
|----|------|---------|
| Jarvis | 前端入口、消息路由 | ✅ 运行中 |
| Claude | 技术执行、代码开发 | ✅ 运行中 |
| Hermes | 规划协调、本地推理 | ✅ 运行中 |

---

## 七、飞书输出规则（铁律）

**只输出最终结论，禁止任何内部操作：**
- ❌ 禁止：工具调用日志（📋/💻/🔎等）、文件路径、推理过程、步骤列表
- ✅ 只输出：最终结论 + 数字 + 状态词

---

## 八、协作标记

```
<!-- HERMES_STARTUP: [时间] -->  — Hermes 启动确认
<!-- HERMES_DONE: [描述] -->     — Hermes 完成标记
<!-- CLAUDE_CODE_DONE: [描述] --> — Claude 完成标记
<!-- JARVIS_DONE: [描述] -->     — Jarvis 完成标记
```

---

## 九、AI工程图纸大模型（暂且搁置）

- **状态：** 暂且搁置（陈总指示）
- **成果：** BOM验证算法识别率 97.67%（单一项目WLA90）
- **工具：** `08_Tools/BOM验证工具/bom_verify.py`
- **下一步：** 获取第二个项目数据做交叉验证（需陈总提供图纸+BOM）

---

## 十、关键教训（刻进骨髓）

1. **环境判断**：每次启动必须 `uname -a`，不能假设
2. **文件操作**：WSL2用 `/mnt/d/`，Git Bash用 `/d/`，不能混用
3. **Python执行**：禁止 `python3 -c`，必须先写文件
4. **飞书输出**：只发结论，禁止工具日志
5. **文件操作找Jarvis**：不自己摸索路径，避免卡死
