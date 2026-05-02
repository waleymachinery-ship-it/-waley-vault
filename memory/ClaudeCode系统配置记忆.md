# Claude Code 系统配置

**更新时间：** 2026-04-13 18:50

---

## 一、运行信息

| 项目 | 值 |
|------|-----|
| 当前会话 | Claude Code (Hermes Gateway via Feishu) |
| 飞书群 | 老板是疯子 |
| 用户ID | ou_cf8f849148e0839728e5ec4a67627221 |
| 交付目标 | origin（当前飞书群） |

---

## 二、核心配置文件

### hermes-cli config.yaml
```yaml
model:
  default: MiniMax-M2.7
  provider: minimax-cn
  base_url: https://api.minimaxi.com/anthropic
toolsets:
- hermes-cli
agent:
  max_turns: 90
  gateway_timeout: 1800
display:
  compact: false
  personality: kawaii
  show_reasoning: false
  streaming: false
platforms:
  feishu:
    enabled: true
    app_id: cli_a95d06761f385bcb
    connection_mode: websocket
```

### 飞书配置
- App ID: `cli_a95d06761f385bcb`
- App Secret: `gJNYDuQOckvt1SNrHdcGVeN3GGyZ7jri`
- Domain: feishu
- 连接模式: WebSocket

---

## 三、关键路径

| 资源 | 路径 |
|------|------|
| Claude Code 配置 | `C:\Users\pc\.claude\settings.json` |
| Hermes 配置 | `C:\Users\pc\.hermes\config.yaml` |
| Claude-to-IM | `C:\Users\pc\.claude\Claude-to-IM` |
| Vault 知识库 | `D:\桌面文件\伟力机械知识库` |

---

## 四、AI协同规则

### 飞书输出规则（重要）
- ❌ 禁止：工具调用日志、文件路径、推理过程、Command Approval
- ✅ 只输出：最终结论、结果摘要

### 闭环协议
```
Claude 完成 → <!-- CLAUDE_CODE_DONE: -->
Hermes/Jarvis 响应 → <!-- [AGENT]_DONE: -->
```

---

## 五、三AI身份澄清（2026-04-24更新）

| AI | 实际身份 | 说明 |
|----|---------|------|
| **Jarvis** | OpenClaw | 飞书入口、前台接待+记忆中枢 |
| **Hermes** | NousResearch Hermes Agent | 独立开源AI Agent，不是OpenClaw Hermes Gateway |
| **Claude** | Claude Code CLI | 推理引擎 |

### Jarvis 角色重新定位（2026-04-24）
| 能力 | 重新定位 | 价值 |
|------|---------|------|
| cron调用 | 从"提供方"退居"监控方" | ACPX直接暴露，绕过Jarvis |
| 任务队列 | 依然是Vault核心操作 | ACPX不直接操作 |
| 飞书消息 | 依然是唯一入口 | ACPX无法主动发飞书 |
| Z_Memory | 依然是枢纽 | Jarvis和Claude操作 |
| FAQ知识库 | Jarvis独有 | Hermes/Claude不具备 |

**一句话定位：** Jarvis是三AI体系的「前台接待+记忆中枢」，负责消息进出、状态同步、知识检索。

---

## 六、当前状态

| AI | 状态 | 最后同步 |
|----|------|---------|
| Claude | ✅ 运行中 | v91 |
| Hermes | ✅ 运行中 | v92 |
| Jarvis | ✅ 运行中 | v74 |

### 待处理任务
- 工程图AI：DWG读取阻塞，等待陈总提供DXF/PDF测试图纸
