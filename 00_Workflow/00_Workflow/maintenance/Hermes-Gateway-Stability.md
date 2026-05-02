# Hermes Gateway 稳定运行指南

> 更新：2026-04-13

---

## 一、检测 Hermes Gateway 是否在运行

### 方法1：检查进程
```bash
ps aux | grep hermes | grep -v grep
```

### 方法2：检查状态文件
```bash
cat ~/.hermes/gateway_state.json
```
期望输出：`{"running": true, "pid": <数字>}`

### 方法3：检查端口（Hermes Gateway 通常监听某个端口）
```bash
# 待确认具体端口
```

---

## 二、重启 Hermes Gateway（如果检测到崩溃）

### 步骤1：清理锁文件和旧 PID
```bash
rm -rf ~/.local/state/hermes/gateway-locks/*
rm -f ~/.hermes/gateway.pid
```

### 步骤2：停止旧进程
```bash
pkill -f hermes  # 或用 pkill hermes
# 或者通过 PID 文件中的旧 PID 停止
```

### 步骤3：启动 Hermes Gateway
```bash
cd $HOME/.hermes/hermes-agent
uv run hermes
```
**注意：** 需要在 Windows 环境下运行，或通过 WSL 调用 Windows 的 `cmd.exe`

### 步骤4：验证启动
```bash
sleep 5
cat ~/.hermes/gateway_state.json
```
确认 `running: true`

---

## 三、完整的一键检查+重启脚本

```bash
#!/bin/bash
# hermes-check.sh - Hermes Gateway 健康检查

HERMES_DIR="$HOME/.hermes/hermes-agent"
STATE_FILE="$HOME/.hermes/gateway_state.json"
LOCK_DIR="$HOME/.local/state/hermes/gateway-locks"
PID_FILE="$HOME/.hermes/gateway.pid"

echo "[$(date)] 检查 Hermes Gateway 状态..."

# 检查进程是否在运行
if pgrep -f hermes > /dev/null 2>&1; then
    echo "[$(date)] Hermes Gateway 运行正常"
    exit 0
fi

echo "[$(date)] Hermes Gateway 未运行，准备重启..."

# 清理锁文件
rm -rf "$LOCK_DIR"/* 2>/dev/null
rm -f "$PID_FILE" 2>/dev/null

# 停止旧进程
pkill -f hermes 2>/dev/null

# 启动 Hermes
cd "$HERMES_DIR"
cmd.exe /c "uv run hermes" &
sleep 5

# 验证
if cat "$STATE_FILE" | grep -q '"running": true'; then
    echo "[$(date)] Hermes Gateway 重启成功"
else
    echo "[$(date)] Hermes Gateway 重启可能失败，请检查"
fi
```

---

## 四、推荐 Cron 任务配置

### Jarvis 应执行的频率
- **每 5 分钟检查一次**（比 30 秒更温和，减少资源占用）

### Cron 表达式
```
*/5 * * * *
```

### 执行内容
调用上面的 `hermes-check.sh` 脚本

---

## 五、已知问题

### 问题1：Hermes Gateway 不稳定原因
- 崩溃原因尚未确定（可能与内存、网络、配置有关）

### 问题2：Hermes 飞书输出刷屏
- 已修复 SOUL.md，添加飞书输出规则
- 禁止输出内部操作细节，只输出最终结果

### 问题3：WSL 调用 Windows 程序
- Hermes 在 WSL 环境下运行
- 需要通过 `cmd.exe` 调用 Windows 程序
- 示例：`cmd.exe /c "uv run hermes"`

---

## 六、启动脚本位置

| 脚本 | 路径 |
|------|------|
| Hermes 启动 | `D:\桌面文件\hermes-start.ps1` |
| Hermes 重启 | `D:\桌面文件\hermes-gateway-restart.ps1` |

---

## 七、关键路径

| 项目 | 路径 |
|------|------|
| Hermes 安装目录 | `C:\Users\pc\.hermes\hermes-agent` |
| 状态文件 | `C:\Users\pc\.hermes\gateway_state.json` |
| PID 文件 | `C:\Users\pc\.hermes\gateway.pid` |
| 锁文件目录 | `C:\Users\pc\.local\state\hermes\gateway-locks\` |
| Vault 知识库 | `D:\桌面文件\伟力机械知识库\` |

⚠️ 注意：`C:\Users\pc\AppData\Local\hermes\` 是错误路径！
