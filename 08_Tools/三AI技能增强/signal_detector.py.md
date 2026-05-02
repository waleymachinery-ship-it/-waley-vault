# Signal Detector - 三AI版

> 每次消息触发，自动捕获实体和想法

## 触发条件

- 每条飞书群消息（不仅是@ Jarvis）
- 消息包含：客户咨询、故障描述、需求变更、决策结论

## 捕获内容

### 实体类型

| 实体类型 | 存储目录 | 触发关键词 |
|---------|---------|-----------|
| 客户/联系人 | `people/` | 人名、称呼 |
| 公司 | `companies/` | "XX公司"、"XX厂" |
| 产品设备 | `products/` | WLA/WLU/WLH、30L-200L |
| 故障问题 | `faults/` | 漏气、异响、不启动 |

### 原创想法

- 用户决策/结论 → `originals/YYYY-MM-DD-{slug}.md`
- 解决方案 → `solutions/YYYY-MM-DD-{slug}.md`

## 实现逻辑

```
消息到达
  ↓
提取产品型号（WLA/WLU/WLH + 容量）
  ↓
提取故障关键词
  ↓
提取客户/公司
  ↓
检查是否已存在
  ↓
不存在且notable → 创建页面
  ↓
记录信号日志
```

## 配置

```python
TRIGGERS = {
    "product_pattern": r"WLA\d+|WLU\d+|WLH\d+|\d+L-\d+",
    "fault_keywords": [
        "漏气", "异响", "不启动", "温度异常", 
        "压力不稳", "产量低", "产品缺陷"
    ],
    "skip_patterns": ["好的", "收到", "谢谢", "ok", "嗯"]
}
```

## 注意事项

- 仅捕获实质性内容，跳过纯确认消息
- 不阻塞主响应，异步处理
- 不向用户汇报"正在捕获"，静默执行

---

*基于GBrain signal-detector设计，适配伟力机械三AI*