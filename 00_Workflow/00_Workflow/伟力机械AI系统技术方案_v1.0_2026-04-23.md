# 伟力机械 AI 系统技术方案 v1.0

**编制日期：** 2026-04-23
**编制人：** Claude（基于三AI架构研究）
**状态：** 待审批
**版本：** v1.0

---

## 一、现状分析

### 1.1 三AI架构优缺点

| AI | 平台 | 优势 | 劣势 |
|----|------|------|------|
| Jarvis | OpenClaw (Node.js) | 微信/飞书接入成熟，技能市场丰富 | 与Vault同步依赖文件，不支持MCP |
| Hermes | Hermes-Agent (Python/WSL2) | 自演进能力强，支持200+模型 | 需WSL2，无法直连Windows文件 |
| Claude | Claude Code CLI | 复杂推理能力强，工具丰富 | 轮询机制效率低，无持久状态 |

### 1.2 核心问题

1. **文件-based通信** — 三AI通过Z_Memory_Sync.json通信，写冲突导致损坏
2. **轮询机制** — Claude每3分钟轮询task_queue，效率低且有时延
3. **技能分散** — OpenClaw技能/Hermes技能/Vault知识库三处独立
4. **无统一模型网关** — 每AI独立配置MiniMax/Claude
5. **Hermes需WSL2** — 架构复杂，Windows文件访问绕路

---

## 二、优化方案

### 2.1 第一阶段：MCP统一通信层（立即执行）

**目标：** 用MCP协议替代文件共享，解决写冲突和通信效率问题

**架构：**
```
┌─────────────────────────────────────────────────────────┐
│                   weili-mcp-server                       │
│                   (FastMCP, Python)                       │
├─────────────────────────────────────────────────────────┤
│ Tools:                                                   │
│  - read_z_memory      → 读取共享记忆                     │
│  - write_z_memory     → 原子写入共享记忆                  │
│  - read_task_queue    → 读取任务队列                      │
│  - append_task        → 追加任务（原子操作）              │
│  - update_task_status → 更新任务状态                     │
│  - read_vault_file    → 读取知识库文件                    │
│  - write_vault_file   → 写入知识库文件                    │
│  - get_agent_status   → 获取三AI在线状态                  │
├─────────────────────────────────────────────────────────┤
│ Resources:                                               │
│  - vault://memory/today  → 当日记忆                       │
│  - vault://memory/sync  → Z_Memory状态                   │
│  - vault://tasks        → 任务队列快照                    │
└─────────────────────────────────────────────────────────┘
```

**优势：**
- 原子操作避免写冲突
- 实时通信替代轮询
- 统一接口，三AI均可调用

**安装命令：**
```bash
pip install mcp fastmcp
```

**预计工时：** Hermes调研1周 + Claude实现1周

---

### 2.2 第二阶段：Hermes-Windows原生支持

**目标：** 让Hermes直接在Windows运行，移除WSL2依赖

**方案：**
1. Hermes-Agent支持Windows（pip install hermes-agent[all]）
2. 使用pywin32访问Windows文件
3. OpenClaw的WeChat/飞书插件由Jarvis继承，Hermes专注推理

**优势：**
- 路径统一（不再需要/mnt/d/）
- 启动速度更快
- 调试更简单

**风险：** 某些Python库在Windows环境可能有兼容性问题

---

### 2.3 第三阶段：伟力机械专属模型训练

**目标：** 基于MiniMax/M2.7微调，训练伟力机械领域模型

**数据来源：**
1. 历史故障报告（fault_reports表）
2. 售后服务记录（after_sales表）
3. FAQ知识库（faq.json）
4. 技术文档（BOM、图纸、规格书）
5. 三AI协作日志（Z_Memory_Sync entries）

**训练方案：**

| 阶段 | 目标 | 数据量 | 预计时间 |
|------|------|--------|----------|
| SFT微调 | 理解伟力产品术语 | 10K条对话 | 1周 |
| RLHF | 对齐售后服务风格 | 1K条偏好数据 | 3天 |
| 领域适应 | 机械工程专业术语 | 5K条技术文档 | 1周 |

**核心能力目标：**
1. 故障诊断推理链
2. 产品选型推荐
3. 售后服务对话
4. 技术文档理解

**模型规格：**
- 基座：MiniMax-M2.7
- 参数：~200B（待确认）
- context：192K tokens
- 部署：本地或MiniMax云

---

### 2.4 第四阶段：统一技能市场

**目标：** 建立伟力机械技能商店，统一管理三AI技能

**技能分类：**

| 类别 | 技能示例 | 适用AI |
|------|---------|--------|
| 客服 | 产品FAQ、选型建议、报价 | Jarvis |
| 诊断 | 故障分析、PLC日志解读 | Hermes |
| 文档 | BOM验证、图纸OCR、技术报告 | Claude |
| 运维 | 日志归档、健康检查、备份 | 三AI共用 |

**技能格式：**
```json
{
  "name": "weili-fault-diagnosis",
  "version": "1.0.0",
  "agent": "hermes",
  "description": "伟力机械故障诊断",
  "triggers": ["故障", "报错", "不工作"],
  "actions": ["读取故障日志", "分析可能原因", "输出解决方案"],
  "data_sources": ["fault_reports", "knowledge_base"]
}
```

---

### 2.5 第五阶段：waley-agent-backend整合

**目标：** 将waley-agent-backend升级为三AI的统一后端

**当前架构问题：**
- 三个AI各自独立，没有统一入口
- 后端与三AI通信需要标准化

**整合方案：**
```
用户消息 → OpenClaw（飞书/微信）
              ↓
         waley-backend（统一入口）
              ↓
    ┌────────┴────────┐
    ↓                 ↓
 Hermes            Claude
 (推理)           (执行)
    ↓                 ↓
 SQLitemap          ↓
 (共享状态) ←→ MCP Server
```

**升级内容：**
1. 增加MCP Server端点
2. 任务队列标准化为gRPC
3. 三AI状态实时同步
4. 增加Web管理界面

---

## 三、伟力机械模型训练方案（详情）

### 3.1 数据工程

**数据来源：**

| 来源 | 数量 | 类型 | 用途 |
|------|------|------|------|
| fault_reports表 | ~5000条 | 故障报告 | 诊断推理训练 |
| after_sales表 | ~2000条 | 服务记录 | 对话训练 |
| FAQ知识库 | ~300条 | Q&A | 问答训练 |
| Z_Memory_Sync | ~200条 | 协作日志 | 行为对齐 |
| 技术文档 | ~100份 | PDF/DXF | 领域知识 |

**数据清洗：**
1. 移除敏感信息（客户名称、联系方式）
2. 标准化故障描述格式
3. 标注推理链（故障→原因→解决）
4. 繁体转简体

### 3.2 训练策略

**Phase 1: SFT（有监督微调）**
```
基座模型：MiniMax-M2.7
训练集：10K条（故障诊断、产品咨询、选型推荐）
Epochs: 3
Learning rate: 2e-5
Batch size: 8
```

**Phase 2: RLHF（人类偏好对齐）**
```
使用DPO或PPO
偏好数据：1K条（售后服务风格）
目标：专业、耐心、简洁
```

**Phase 3: 领域适应**
```
技术文档：5K条（机械工程术语）
目标：理解伟力产品技术规格
```

### 3.3 评估指标

| 能力 | 指标 | 目标 |
|------|------|------|
| 故障诊断准确率 | 故障分类准确 | ≥90% |
| FAQ回答质量 | ROUGE-L | ≥0.7 |
| 对话流畅度 |人类评估 | ≥4/5 |
| 技术文档理解 | BOM提取准确率 | ≥95% |

---

## 四、实施计划

### 4.1 短期（1-2周）- MCP集成

| 日期 | 负责人 | 任务 | 交付物 |
|------|--------|------|--------|
| 第1周 | Hermes | MCP调研，输出可行性报告 | MCP可行性.md |
| 第1周 | Hermes | 确定FAQ知识库MCP接口设计 | 接口设计.md |
| 第2周 | Claude | 搭建weili-vault-mcp-server | mcp_server.py |
| 第2周 | Claude | OpenClaw MCP集成测试 | 测试报告 |

### 4.2 中期（3-4周）- Hermes-Windows + 模型准备

| 日期 | 负责人 | 任务 | 交付物 |
|------|--------|------|--------|
| 第3周 | Hermes | Hermes Windows兼容测试 | 测试报告 |
| 第3周 | Claude | 收集整理训练数据 | dataset/ |
| 第4周 | Hermes | 数据清洗和标注 | 数据集v1.0 |
| 第4周 | Claude | 训练脚本准备 | train.sh |

### 4.3 长期（5-8周）- 模型训练

| 日期 | 负责人 | 任务 | 交付物 |
|------|--------|------|--------|
| 第5周 | Claude | SFT微调训练 | model_sft.bin |
| 第6周 | Hermes | RLHF对齐 | model_rlhf.bin |
| 第7周 | Claude | 领域适应训练 | model_final.bin |
| 第8周 | 三AI | 整合测试与部署 | weili-model-v1.0 |

---

## 五、关键技术链接

### MCP生态
| 资源 | 链接 |
|------|------|
| Python SDK | github.com/modelcontextprotocol/python-sdk |
| FastMCP | github.com/jlowin/fastmcp |
| MCP协议规范 | modelcontextprotocol.io |

### 模型训练
| 资源 | 链接 |
|------|------|
| MiniMax API | api.minimaxi.com |
| 微调文档 | minimaxi.com/document |
| DPO训练 | github.com/erhwenkuo/dpo-tuning |

### 技能市场
| 资源 | 链接 |
|------|------|
| ClawHub | clawhub.ai |
| OpenClaw Skills | docs.openclaw.ai/skills |

---

## 六、风险与应对

| 风险 | 影响 | 应对 |
|------|------|------|
| MCP集成复杂度 | 中 | 先做最小可行版本MVP |
| 模型训练资源 | 高 | 确认MiniMax微调支持情况 |
| Hermes Windows兼容 | 低 | 先在WSL2测试再迁移 |
| 数据质量 | 中 | 人工审核关键数据 |

---

## 七、预期收益

| 收益 | 量化 |
|------|------|
| 通信效率 | 实时vs3分钟轮询 |
| 写冲突 | 原子操作vs文件损坏 |
| 故障诊断 | AI自动推理vs人工排查 |
| 客服效率 | 模型训练后FAQ准确率≥90% |
| 三AI协作 | MCP统一协议vs文件共享 |

---

*本方案为伟力机械专属AI系统技术路线图，待陈总审批后执行。*