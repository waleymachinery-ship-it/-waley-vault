# AI协调架构（2026-04-10 决策）

## 问题
- OpenClaw 和 Hermes 无法有效协作（ACP 适配器调试失败）
- 两个系统各自为战，没有真正的调度闭环

## 解决方案
**Claude Code 作为协调大脑，Hermes/OpenClaw 作为执行器/消息入口**

## 架构图

```
用户消息 → Hermes/Jarvis（消息入口）
              ↓
         写入 Vault / memory
              ↓
         Claude Code 检测到 → 推理判断 → 调度执行
              ↓
         回复用户 / 更新知识库 / 触发脚本
```

## 角色定义

| AI | 角色 | 职责 |
|----|------|------|
| **Claude Code** | 协调大脑 | 推理、决策、调度任务 |
| **Hermes** | 消息入口 + 专业能力 | 接收消息、触发 Vault 写入、提供 skills/toolsets |
| **OpenClaw (Jarvis)** | 消息入口 + 渠道 | 微信/飞书接入、知识库编辑 |
| **Vault (Obsidian)** | 共享知识中枢 | 记忆、任务队列、知识库 |

## 关键原则

1. **Hermes/OpenClaw 只做入口和执行器**
2. **Claude Code 负责推理和调度**
3. **通过 Vault (memory 文件) 实现异步协作**
4. **不再强求 ACP 适配器直连**

## watchdog 脚本

- `watch_jarvis.ps1` - 监控 JARVIS_DONE 标记，30分钟间隔
- `watch_openclaw.ps1` - 监控 OpenClaw Gateway 存活，5分钟间隔

## ⚠️ 坚决执行规则：问题必须写入Vault

> **重要结论、问题发现 必须及时写入 Vault**
> - 现象、涉及组件、分析判断、结论
> - 写入对应日期的 memory 日志（YYYY-MM-DD.md）
> - 相关配置问题同步更新到 AGENTS.md 或 MEMORY.md

### 已记录问题
- 🔴 **2026-04-11**：单独@Hermes不响应（@all正常，私信也正常）

## 待完成

- Hermes/OpenClaw 的"消息写入 Vault"skill/script
- 消息处理结果读取机制
- 单独@Hermes不响应问题排查（@all正常，需查消息路由差异）
