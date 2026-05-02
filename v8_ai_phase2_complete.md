# V8网站AI助手 Phase 2 完整方案

## 架构变更

**数据库切换：SQLite → MySQL**

| 项目 | 旧方案 | 新方案 |
|------|--------|--------|
| 数据库 | SQLite (waley.db) | MySQL 8.0 (waley_db) |
| 连接方式 | better-sqlite3 | mysql2/promise + drizzle |
| 存储位置 | /www/waley-agent-backend/waley-agent-backend/waley.db | localhost:3306/waley_db |

## MySQL 配置

- root 密码：Waley2026!
- 用户：waley / Waley2026!
- 数据库：waley_db
- 字符集：utf8mb4_unicode_ci

## leads 表结构

```sql
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(16) NOT NULL UNIQUE,
    name VARCHAR(64) NOT NULL,
    company VARCHAR(255),
    product VARCHAR(128),
    source VARCHAR(64) DEFAULT 'v8_ai_assistant',
    registeredAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 后端接口

### leadRouter

**register** - 注册/更新潜客
- 输入：name, phone(1[3-9]\d{9}), company, product, source
- 手机号已存在则更新，否则插入

**verifyPhone** - 验证手机号
- 输入：phone
- 返回：found, name, company, product, registeredAt

## 前端流程



## 测试数据

- 陈思远 / 13882969259 / 伟力机械 / WLC标准型伺服
- 测试用户 / 13912345678 / 测试公司 / WLA大型储料式

## 部署时间

2026-04-29 22:12 GMT+8
