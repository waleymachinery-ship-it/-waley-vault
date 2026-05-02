# 伟力机械 AI 协同规则与规范

> 版本：1.0
> 更新：2026-04-13
> 适用范围：Jarvis / Hermes / Claude

---

## 一、Vault 核心文件

| 文件 | 用途 |
|------|------|
| `D:\桌面文件\伟力机械知识库\memory\YYYY-MM-DD.md` | 每日工作日志 |
| `D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json` | 三AI协同核心基地 |

---

## 二、Vault 写入规范

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

### 三方闭环流程

```
Claude 完成工作 → 写入 <!-- CLAUDE_CODE_DONE: [描述] -->
     ↓
Jarvis/Hermes 检测到 → 读取内容 → 响应 <!-- JARVIS/HERMES_DONE: [回应] -->
     ↓
Claude 下次启动 → 读取 <!-- JARVIS/HERMES_DONE --> → 继续下一轮
```

### 示例

**场景：Claude 修复了 @all 问题**

```
Claude 写入：
<!-- CLAUDE_CODE_DONE: @all 响应问题已修复，源码 + dist 均已更新 -->

Hermes 读到：
<!-- CLAUDE_CODE_DONE: @all 响应问题已修复 -->
响应：
<!-- HERMES_DONE: 收到，已同步到 Hermes 记忆 -->

Jarvis 读到：
<!-- HERMES_DONE: 收到，已同步到 Hermes 记忆 -->
响应：
<!-- JARVIS_DONE: 收到，FAQ 已更新 -->
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

### Hermes Gateway 监控
- **负责人：** Jarvis
- **Cron 频率：** 每 5 分钟
- **检查命令：** `ps aux | grep hermes-gateway`
- **重启脚本：** `D:\桌面文件\hermes-gateway-restart.ps1`

### Claude-to-IM 监控
- **负责人：** Jarvis
- **Cron 频率：** 每 5 分钟
- **检查命令：** `ps aux | grep claude-to-im`
- **重启脚本：** `D:\桌面文件\claude-to-im-start.ps1`

---

## 七、AI 角色分工

| AI | 角色 | 核心职责 |
|----|------|----------|
| **Jarvis** | 前端入口 | 消息接收、FAQ客服，知识库检索 |
| **Hermes** | 调度中枢 | 任务路由、工程图纸AI、自动化执行 |
| **Claude** | 总司令 | 复杂推理、系统协调、重大决策 |

---

## 八、错误处理

1. **发现问题** → 立即写入 Vault
2. **尝试修复** → 记录修复过程
3. **修复成功** → 写入成功标记
4. **修复失败** → 写入失败原因，请求支援

---

## 九、紧急联系

- **陈总（用户）**：通过飞书联系
- **Jarvis**：飞书群
- **Hermes**：飞书群
- **Claude（本地）**：Claude Code CLI

---

*本规则由 Claude Code 维护*
*如需更新，请写入 Z_Memory_Sync.json 并通知各方*
