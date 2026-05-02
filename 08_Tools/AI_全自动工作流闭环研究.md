# 三个AI全自动工作流闭环研究

> 创建：2026-04-11
> 状态：研究阶段

---

## 一、当前三个AI的状态

| AI | 角色 | 职责 | 通信接口 |
|----|------|------|----------|
| **OpenClaw / 贾维斯** | 消息入口 | 微信/飞书接入、简单问答 | WebSocket (18789), ACP |
| **Claude Code / 克劳德** | 协调大脑 | 推理、决策、系统规划 | CLI (claude.exe) |
| **Hermes** | 本地中枢 | 工作流执行、任务处理 | CLI (uv run hermes) |

---

## 二、核心问题

### 2.1 消息无法自动流转

**现状：**
- 用户发消息到微信/飞书 → OpenClaw 接收
- OpenClaw 只能做简单 FAQ 回复
- **无法自动触发 Claude 或 Hermes 处理复杂任务**
- Claude 和 Hermes 需要手动启动，无法被 OpenClaw 自动调用

**问题：**
1. OpenClaw 如何知道一个任务该交给 Claude 还是 Hermes？
2. OpenClaw 如何把用户消息传递给 Claude/Hermes？
3. Claude/Hermes 处理完后，结果如何返回给 OpenClaw？

### 2.2 上下文无法共享

**现状：**
- OpenClaw 有自己的对话上下文
- Claude Code 有自己的会话
- Hermes 有自己的会话
- **三者之间没有上下文传递机制**

### 2.3 通信协议不兼容

- OpenClaw 使用 ACP（Agent Communication Protocol）
- Claude Code 使用自己的 CLI 协议
- Hermes 使用 Hermes CLI 协议
- **三者无法直接对话**

---

## 三、可能的解决方案

### 方案A：OpenClaw 作为调度器（推荐）

**思路：** OpenClaw 通过 spawn subprocess 调用 Claude/Hermes CLI

**实现方式：**
```
用户消息 → OpenClaw → 分析意图
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
简单问题           复杂问题
(OpenClaw直接回复)   ↓
              ┌────────┴────────┐
              ↓                 ↓
         Claude           Hermes
         (CLI调用)        (CLI调用)
              ↓                 ↓
              └────────┬────────┘
                       ↓
              OpenClaw 汇总结果
                       ↓
                  返回用户
```

**技术要点：**
1. OpenClaw 需要配置外部 Agent 回调
2. 通过 stdin/stdout 传递消息
3. 使用共享文件传递长上下文

### 方案B：共享 Vault 作为消息通道

**思路：** 所有 AI 通过读写共享文件传递任务和结果

**实现方式：**
```
用户消息 → OpenClaw → 写入任务文件
                            ↓
              Hermes/Claude 定时检测任务文件
                            ↓
                       处理任务
                            ↓
                       写入结果文件
                            ↓
              OpenClaw 定时检测结果文件
                            ↓
                       返回用户
```

**技术要点：**
1. 任务队列文件：`D:\桌面文件\伟力机械知识库\00_Workflow\tasks\`
2. 状态机管理任务生命周期
3. 需要 watchdog 监控文件变化

### 方案C：Hermes 作为统一网关

**思路：** Hermes 是支持多平台的框架，配置为接收 OpenClaw 的任务

**实现方式：**
```
用户消息 → OpenClaw → Hermes（通过 ACP 或 HTTP）
              ↓
         Hermes 处理/转发
              ↓
    ┌────────┴────────┐
    ↓                 ↓
简单问题           复杂问题
(Hermes直接回复)   ↓
              Claude
              (协作处理)
              ↓
         Hermes 汇总
              ↓
         返回 OpenClaw
              ↓
         返回用户
```

---

## 四、需要研究的技术点

### 4.1 OpenClaw ACP 接口

- [ ] OpenClaw ACP 是否支持外部 Agent 注册？
- [ ] 外部 Agent 如何接收和响应 ACP 消息？
- [ ] Claude Code 能否作为 ACP Agent 接入？

### 4.2 CLI 调用机制

- [ ] OpenClaw 如何 spawn Claude CLI 进程？
- [ ] stdin/stdout 如何传递多轮对话上下文？
- [ ] 超时和错误处理机制？

### 4.3 Hermes 集成

- [ ] Hermes 能否通过 ACP 与 OpenClaw 通信？
- [ ] Hermes 的工具调用能力如何暴露给 OpenClaw？
- [ ] Hermes 与 Claude Code 如何协作？

### 4.4 上下文管理

- [ ] 如何在多 Agent 间传递长上下文？
- [ ] 共享文件 vs 内存传递哪个更合适？
- [ ] 如何避免上下文丢失？

---

## 五、初步实施计划

### Phase 1：基础通信（本周）

1. **研究 OpenClaw ACP 文档**
   - 确认是否支持外部 Agent
   - 了解接入方式

2. **测试 Hermes CLI 调用**
   - 能否通过命令行传入消息？
   - 输出格式是什么？

3. **测试 Claude CLI 调用**
   - 能否通过命令行传入消息？
   - 输出格式是什么？

### Phase 2：点到点连接（下周）

1. **OpenClaw → Claude** 单向通道
   - OpenClaw 收到消息，判断是否需要 Claude
   - Spawn Claude CLI 处理
   - 获取结果返回

2. **OpenClaw → Hermes** 单向通道
   - 同上

### Phase 3：闭环整合（待定）

1. 实现双向通信
2. 实现上下文传递
3. 实现智能路由

---

## 六、关键问题（待确认）

1. **OpenClaw 支持 ACP 外部 Agent 吗？** 需要看文档或测试
2. **Claude CLI 能否被外部进程调用？** 可以，但需要处理 stdin/stdout
3. **Hermes CLI 是否支持 headless 模式？** 需要测试
4. **三者的上下文如何高效传递？** 共享文件可能是最简单方案

---

## 七、参考资源

- OpenClaw ACP 文档
- Hermes Agent 官方文档
- Claude Code CLI 参考
- 伟力机械 Vault 知识库
