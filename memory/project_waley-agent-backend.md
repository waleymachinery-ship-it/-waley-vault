# Waley Agent Backend 项目详情

> 更新：2026-04-18

## 项目路径
`D:\桌面文件\伟力机械知识库\AI系统\waley-agent-backend`

## 状态
| 项目 | 状态 | 说明 |
|------|------|------|
| 去Manus化 | ✅ 完成 | MiniMax API + JWT 认证 |
| 数据库 | ⚠️ SQLite临时 | MySQL 未安装 |
| 运行地址 | ✅ http://localhost:3000/ | 用户已注册账号 |

## 技术栈
- **后端**: Express + tRPC + Drizzle ORM
- **前端**: React 19 + TypeScript + Wouter + TailwindCSS
- **AI**: MiniMax M2.7 API
- **认证**: JWT + bcryptjs
- **数据库**: SQLite（临时）→ MySQL（待安装）

## 数据库方案

### 当前：SQLite（临时）
- 数据库文件：`waley-agent-backend/waley.db`
- 改动：`server/db.ts` 用 better-sqlite3 替代 mysql2
- 缺点：无法支持并发写入，生产环境需换回MySQL

### 目标：MySQL
- 配置：`mysql://waley:waley123@localhost:3306/waley_agent`
- MySQL 安装后改回

## 改动记录 (2026-04-18)

| 文件 | 改动 |
|------|------|
| `server/db.ts` | mysql2 → better-sqlite3 |
| `server/services/simulatorManager.ts` | 移除 mysql 依赖 |
| `server/services/plcDataSimulator.ts` | mysql2 → drizzle ORM |
| `server/_core/vite.ts` | 修复静态文件路径 `../..` → `..` |

新增依赖：`better-sqlite3`, `@types/better-sqlite3`

## Phase 2 故障报告系统

**状态：** 开发中

**已实现功能：**
- ✅ 7步故障报告表单（客户信息→机器型号→故障类型→描述→时间/处理→照片→确认）
- ✅ 铭牌照片和故障图片上传
- ✅ 报告提交 API（公开接口，无需登录）
- ✅ 报告查询 API（已有报告编号功能）
- ✅ 自动归档到 `D:/桌面文件/伟力机械知识库/故障处理/2026/`
- ⚠️ AI 分析：MiniMax API 网络不通，异步分析失败

**API 接口：**
- `faultReport.submitReport` - 提交故障报告
- `faultReport.getReports` - 获取报告列表
- `faultReport.getReport` - 获取单个报告详情
- `faultReport.updateReport` - 更新报告状态

## 启动指令
```bash
cd "D:\桌面文件\伟力机械知识库\AI系统\waley-agent-backend"
npm run dev
```

## 待办
- [ ] 安装 MySQL
- [ ] 改回 MySQL 数据库
- [ ] 生产环境部署
