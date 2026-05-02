# Hermes Gateway 故障恢复指南

## 问题描述

重启后 Hermes Gateway PID 文件和锁文件残留，导致新进程无法正常启动。

## 快速修复步骤

### Step 1: 清理锁文件
```bash
rm -rf ~/.local/state/hermes/gateway-locks/*
```

### Step 2: 删除旧 PID 文件
```bash
rm -f ~/.hermes/gateway.pid
```

### Step 3: 检查并停止残留进程
```bash
taskkill //PID <旧PID> //F
```

### Step 4: 用 PowerShell 重启 Hermes Gateway
```powershell
cd 'C:\Users\pc\.hermes\hermes-agent'
Start-Process -FilePath 'uv' -ArgumentList 'run','hermes','gateway','run' -WindowStyle Hidden
```

### Step 5: 验证连接状态
```bash
cat ~/.hermes/gateway_state.json
```

---

## 关键文件路径

| 文件 | 路径 |
|------|------|
| Hermes 程序目录 | `C:\Users\pc\.hermes\hermes-agent\` |
| PID 文件 | `~/.hermes/gateway.pid` |
| 锁文件目录 | `~/.local/state/hermes/gateway-locks/` |
| 状态文件 | `~/.hermes/gateway_state.json` |

⚠️ 注意：`C:\Users\pc\AppData\Local\hermes\` 是错误路径！

---

## 一键重启脚本

一键重启脚本已创建：
```
D:\桌面文件\hermes-gateway-restart.ps1
```
直接双击运行即可（2026-04-12 测试通过 ✅）

手动创建文件 `hermes-gateway-restart.ps1` 到桌面：

```powershell
# Hermes Gateway 一键重启脚本
# 路径：D:\桌面文件\hermes-gateway-restart.ps1

Write-Host "🔧 Hermes Gateway 故障恢复中..." -ForegroundColor Yellow

# 1. 清理锁文件
Write-Host "[1/5] 清理锁文件..." -ForegroundColor Cyan
Remove-Item -Path "$env:USERPROFILE\.local\state\hermes\gateway-locks\*" -Force -ErrorAction SilentlyContinue

# 2. 删除旧 PID 文件
Write-Host "[2/5] 删除旧 PID 文件..." -ForegroundColor Cyan
Remove-Item -Path "$env:USERPROFILE\.hermes\gateway.pid" -Force -ErrorAction SilentlyContinue

# 3. 停止残留进程
Write-Host "[3/5] 检查残留进程..." -ForegroundColor Cyan
$oldPid = Get-Content "$env:USERPROFILE\.hermes\gateway.pid" -ErrorAction SilentlyContinue
if ($oldPid) {
    Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue
    Write-Host "  已停止旧进程: $oldPid" -ForegroundColor Gray
}

# 4. 启动 Hermes Gateway
Write-Host "[4/5] 启动 Hermes Gateway..." -ForegroundColor Cyan
Set-Location 'C:\Users\pc\.hermes\hermes-agent'
Start-Process -FilePath 'uv' -ArgumentList 'run','hermes','gateway','run' -WindowStyle Hidden

# 5. 验证
Write-Host "[5/5] 验证连接状态..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
if (Test-Path "$env:USERPROFILE\.hermes\gateway_state.json") {
    $state = Get-Content "$env:USERPROFILE\.hermes\gateway_state.json" -Raw | ConvertFrom-Json
    if ($state.connected) {
        Write-Host "✅ Hermes Gateway 已连接！" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Hermes Gateway 未连接，请检查日志" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️ 状态文件不存在，Gateway 可能未正常启动" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
```

---

## 症状识别

| 症状 | 原因 |
|------|------|
| 新进程无法启动 | PID/锁文件残留 |
| 连接状态显示 false | Gateway 未正常启动 |
| 端口被占用 | 旧进程未完全退出 |

---

## 预防措施

1. 正常关机前先停止 Hermes Gateway
2. 使用本脚本的一键重启功能
3. 定期检查 `gateway_state.json` 连接状态

---

*最后更新：2026-04-12 by Hermes*
