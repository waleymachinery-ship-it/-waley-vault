# Hermes Gateway 重启修复日志

**日期：** 2026-04-12
**问题：** Hermes Gateway 重启后无法正常连接飞书
**修复：** 手动清理锁文件和重启 Gateway

---

## 问题现象

1. 电脑重启后，Hermes Gateway 没有自动启动
2. Hermes 自己尝试启动但飞书连接失败
3. 状态显示：
   - Gateway: running
   - Feishu: connected（但实际未正常工作）
   - PID 与实际运行的不一致

---

## 问题原因

Hermes Gateway 重启后，PID 文件和锁文件残留：

| 文件 | 问题 |
|------|------|
| `~/.hermes/gateway.pid` | 记录旧的 PID (17704)，实际已不存在 |
| `~/.local/state/hermes/gateway-locks/` | 残留锁文件，导致新进程无法正常启动 |

---

## 修复步骤

### 1. 检查当前状态

```bash
# 查看 gateway 状态
cat ~/.hermes/gateway_state.json

# 查看 PID 文件
cat ~/.hermes/gateway.pid
```

### 2. 清理旧文件

```bash
# 删除锁文件目录
rm -rf ~/.local/state/hermes/gateway-locks/*

# 删除旧的 PID 文件
rm -f ~/.hermes/gateway.pid
```

### 3. 停止可能残留的 Hermes 进程

```bash
# 查找 Hermes 进程
ps aux | grep -i hermes | grep -v grep

# 如果有残留，强制终止
taskkill //PID <PID号> //F
```

### 4. 重启 Hermes Gateway

使用 PowerShell 启动（避免 Unicode 编码问题）：

```powershell
cd 'C:\Users\pc\AppData\Local\hermes\hermes-agent'
Start-Process -FilePath 'uv' -ArgumentList 'run','hermes','gateway','run' -PassThru -WindowStyle Hidden
```

### 5. 验证启动结果

```bash
# 等待 5 秒后检查
cat ~/.hermes/gateway_state.json
```

### 6. 确认飞书连接

检查 `gateway_state.json` 中的 `platforms.feishu.state`：
- `connected` = 连接成功
- 其他 = 需要进一步排查

---

## 关键文件路径

| 文件 | 路径 |
|------|------|
| Hermes 主程序 | `C:\Users\pc\AppData\Local\hermes\hermes-agent` |
| Hermes 配置文件 | `C:\Users\pc\.hermes\config.yaml` |
| PID 文件 | `C:\Users\pc\.hermes\gateway.pid` |
| 状态文件 | `C:\Users\pc\.hermes\gateway_state.json` |
| 锁文件目录 | `C:\Users\pc\.local\state\hermes\gateway-locks` |
| 日志目录 | `C:\Users\pc\.hermes\logs\` |
| 启动脚本 | `D:\桌面文件\hermes-start.ps1` |

---

## 快速修复脚本（一键修复）

**下次 Hermes Gateway 出问题，直接运行这5步：**

```powershell
# 步骤1: 清理锁文件
rm -rf ~/.local/state/hermes/gateway-locks/*

# 步骤2: 删除旧 PID 文件
rm -f ~/.hermes/gateway.pid

# 步骤3: 停止残留进程（先查 PID）
taskkill //PID $(cat ~/.hermes/gateway.pid) //F 2>$null

# 步骤4: 重启 Hermes Gateway
cd 'C:\Users\pc\AppData\Local\hermes\hermes-agent'
Start-Process -FilePath 'uv' -ArgumentList 'run','hermes','gateway','run' -WindowStyle Hidden

# 步骤5: 等待并验证
Start-Sleep -Seconds 5
cat ~/.hermes/gateway_state.json
```

**或者合并成一行：**
```powershell
rm -rf ~/.local/state/hermes/gateway-locks/*; rm -f ~/.hermes/gateway.pid; cd 'C:\Users\pc\AppData\Local\hermes\hermes-agent'; Start-Process uv -ArgumentList 'run','hermes','gateway','run' -WindowStyle Hidden
```

---

## 记忆要点

**Hermes Gateway 挂了？记住这个顺序：**

1. **清理** → 锁文件 + PID 文件
2. **杀进程** → 停止残留
3. **重启** → PowerShell 启动
4. **验证** → 检查 gateway_state.json

---

## 相关问题

- **WinError 87**：Windows 上 `os.kill(pid, 0)` 的兼容性问题，已在 `status.py` 中添加 `OSError` 异常处理
- **UnicodeEncodeError**：日志中包含 `\u2713` 等 Unicode 字符，Windows GBK 编码无法显示

---

## 预防措施

1. 电脑重启前，确保 Hermes Gateway 已正常停止
2. 或者设置开机自启动脚本
3. 定期清理 `gateway-locks` 目录

---

**标签：** #hermes #gateway #重启 #修复 #飞书
