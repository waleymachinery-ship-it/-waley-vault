---
name: v8_contact_form_feishu_integration
description: V8页面底部联系表单接入MySQL+飞书群通知方案
type: project
---

# V8联系表单 + 飞书群通知方案

## 现状
- 页面底部联系表单（姓名/公司/邮箱/电话/产品/留言）是空壳，无提交处理逻辑
- leads 表仅有：id, phone, name, company, product, source, registeredAt, updatedAt
- 需要：MySQL持久化 + 飞书群实时通知

## 待执行任务
1. leads 表新增字段：email, message
2. 新建 contactRouter，submitContact 接口
3. 接入飞书群机器人 webhook 推送
4. 前端表单绑定 submitContactForm()

## 飞书 webhook URL
> 暂未提供，待用户提供

## 数据库变更
```sql
ALTER TABLE leads ADD COLUMN email VARCHAR(128) AFTER company;
ALTER TABLE leads ADD COLUMN message TEXT AFTER product;
ALTER TABLE leads ADD COLUMN source VARCHAR(64) DEFAULT 'v8_contact_form';
```

## 后端接口
```typescript
// contactRouter.ts
submitContact: publicProcedure
  .input(z.object({
    name: z.string().min(1),
    phone: z.string().regex(/^1[3-9]\d{9}$|^$/),
    email: z.string().email().or(z.literal('')),
    company: z.string(),
    product: z.string(),
    message: z.string().min(1),
  }))
  .mutation(async ({ input }) => {
    // 1. 存入 MySQL leads 表
    // 2. 调用飞书群机器人 webhook
    // 3. 返回成功
  })
```

## 飞书卡片格式
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": { "tag": "plain_text", "content": "📩 新的客户咨询" },
      "template": "red"
    },
    "elements": [
      { "tag": "div", "text": "**姓名：** 张三" },
      { "tag": "div", "text": "**公司：** 深圳XX厂" },
      { "tag": "div", "text": "**电话：** 138xxxx" },
      { "tag": "div", "text": "**邮箱：** zhangsan@company.com" },
      { "tag": "div", "text": "**感兴趣的产品：** WLC 可定制全电动AI智能型" },
      { "tag": "div", "text": "**留言：** 我们需要一台30L的吹塑机..." }
    ]
  }
}
```

## 前端表单处理
```javascript
<form id="contactForm" onsubmit="submitContactForm(event)">

async function submitContactForm(e) {
  e.preventDefault();
  // 收集表单数据 → 调用 /api/trpc/contact.submitContact
}
```
