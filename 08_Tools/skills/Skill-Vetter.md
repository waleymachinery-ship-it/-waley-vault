# Skill Vetter 🔒

> 安装时间：2026-04-09

## 用途
安全审查技能。所有从 ClawHub、GitHub 或其他来源安装的新 skill，都应先用此工具审查代码安全。

## 位置
```
C:\Users\pc\.openclaw\workspace\skills\skill-vetter-1-0-0\
```

## 风险检查项（红旗）
- curl/wget 到未知 URL
- 发送数据到外部服务器
- 请求凭据/API密钥
- 读取 ~/.ssh、~/.aws、~/.config
- 访问 MEMORY.md、USER.md、SOUL.md、IDENTITY.md
- base64 解码
- eval()/exec() 处理外部输入
- 修改 workspace 外的系统文件
- 安装未列出的包
- 混淆代码（压缩/编码/混淆）
- 请求提升/sudo 权限
- 访问浏览器 cookie/session
- 触碰凭据文件

## 风险等级
| 等级 | 说明 | 行动 |
|------|------|------|
| 🟢 LOW | 笔记、天气、格式化 | 可直接安装 |
| 🟡 MEDIUM | 文件操作、浏览器、API | 需完整代码审查 |
| 🔴 HIGH | 凭据、交易、系统 | 需人工审批 |
| ⛔ EXTREME | 安全配置、root 访问 | 禁止安装 |

## 调用方式
读取 SKILL.md 后，按照其中的 Vetting Protocol 执行审查。
