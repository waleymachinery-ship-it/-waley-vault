---
name: claude-to-im-status
description: Claude-to-IM 当前运行状态（2026-04-12 更新）
type: reference
---

# Claude-to-IM 运行状态（2026-04-12 更新）

## 当前状态
| 项目 | 值 |
|------|-----|
| PID | 10864 → 13452（重启后稳定） |
| 运行时间 | 38m+ |
| 重启次数 | 6（历史），当前稳定 |
| 进程状态 | online（PM2 管理） |
| 心跳 | 每 30 秒更新 |

## PM2 配置（已确认正确）
| 项目 | 值 |
|------|-----|
| 启动脚本 | `C:\Users\pc\.claude\skills\claude-to-im\dist\daemon.mjs` |
| 日志 | `D:\桌面文件\logs\claude-to-im-*.log` |
| PID 文件 | `C:\Users\pc\.pm2\pids\claude-to-im-0.pid` |
| 开机启动 | `start_all.bat` → `pm2 resurrect` |

## Startup 启动项（已清理完毕）
✅ 已删除：
- `start-claude-to-im.bat` — **与 PM2 重复启动冲突，已删除**
- `Ollama.lnk` — Ollama 未注册 PM2，不需要开机自启

✅ 当前保留：
- `start_all.bat` — 执行 `pm2 resurrect` 恢复所有 PM2 进程

## 启动流程（无冲突）
```
开机 → start_all.bat → pm2 resurrect → 恢复 claude-to-im（唯一实例）
```

**注意：** 之前 `start-claude-to-im.bat` 和 `pm2 resurrect` 同时启动 Claude-to-IM 导致进程冲突（SIGHUP 重启 6 次）。删除重复脚本后稳定。

## 已知问题
| 问题 | 原因 | 状态 |
|------|------|------|
| SIGHUP 信号退出 | 重复启动冲突 | ✅ 已解决 |
| CardKit 9499 错误 | SDK v1 API 差异 | ✅ 已修复 |
| @all 回复失败 | 原因待查 | ⚠️ 待验证 |

## 配置文件
- config.env: `C:\Users\pc\.claude-to-im\config.env`
- status.json: `C:\Users\pc\.claude-to-im\runtime\status.json`

## SDK 版本
- Feishu SDK: 1.60.0
- Claude Code CLI: 2.1.100（最新 2.1.104，有更新）

## 一键脚本
| 脚本 | 用途 |
|------|------|
| `D:\桌面文件\claude-to-im-start.ps1` | 启动 Claude-to-IM（PM2 方式） |
| `D:\桌面文件\claude-to-im-health.ps1` | 健康检查（当前由 PM2 替代） |
| `D:\桌面文件\hermes-gateway-restart.ps1` | 重启 Hermes Gateway |
