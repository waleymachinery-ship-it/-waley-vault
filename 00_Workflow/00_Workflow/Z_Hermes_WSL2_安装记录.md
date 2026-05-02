# Hermes 安装记录

> 创建时间：2026-04-09
> 更新时间：2026-04-11（最终安装成功）

## 最终安装方式

**Windows 原生安装（非 WSL2）**

### 安装步骤

1. **运行官方安装脚本**（PowerShell）：
```powershell
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

2. **子模块初始化**（如需要）：
```powershell
cd C:\Users\pc\.hermes\hermes-agent
git submodule update --init --recursive
```

3. **配置 MiniMax 模型**：
```powershell
cd C:\Users\pc\.hermes\hermes-agent
uv run hermes model
# 选择：8 More providers → 6 MiniMax China
# 输入 API Key：sk-cp-RWEbmlt5-_Y8a9-6K-dIjLm89_0yO8xSmW8Th1OAa_Zzq_l4Z0-XeZCihi9c4MM3Ab1Dd7ftnldWnJooooFmCaKKnI03dV3wXykdd8_hvE1h_5t1RZA4ujk
# Base URL：https://api.minimaxi.com/anthropic（自动填充）
# 选择模型：MiniMax-M2.7
```

4. **创建 SOUL.md**：`C:\Users\pc\.hermes\SOUL.md`

5. **创建启动脚本**：`D:\桌面文件\hermes-start.ps1`

---

## 启动方式

**方式1：PowerShell**
```powershell
. D:\桌面文件\hermes-start.ps1
```

**方式2：Windows Terminal**（推荐，编码问题更少）
```powershell
. D:\桌面文件\hermes-start.ps1
```

---

## 配置信息

| 项目 | 值 |
|------|-----|
| 安装路径 | `C:\Users\pc\.hermes\hermes-agent` |
| 版本 | v0.8.0 (2026.4.8) |
| 模型 | MiniMax-M2.7 |
| API Endpoint | https://api.minimaxi.com/anthropic |
| SOUL.md | `C:\Users\pc\.hermes\SOUL.md` |

---

## 已知问题

### 编码问题
- PowerShell 默认编码（GBK）无法显示 Hermes TUI 的 Unicode 字符
- 解决：使用 Windows Terminal 或先运行 `chcp 65001`

---

## 相关文档

- `Z_5plus1_System_Architecture.md` - 系统架构文档
- `memory/AI系统/` - AI 系统文档
