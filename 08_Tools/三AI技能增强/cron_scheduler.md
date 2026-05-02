# Cron Scheduler Stagger - 三AI版

> 任务错峰执行，避免同时触发。安静时段不打扰。

## 时间槽分配

| AI | 轮询间隔 | 固定槽位 |
|----|---------|---------|
| Jarvis | 30分钟 | :05, :35 |
| Hermes | 30分钟 | :15, :45 |
| Claude | 30分钟 | :25, :55 |

## 规则

1. **同一AI的任务** → 至少间隔15分钟
2. **多AI同时任务** → 自动错开
3. **大批量任务** → 分批处理，每批<=5
4. **安静时段** → 23:00-08:00 不发通知

## 实现

### 时间槽计算

```python
def get_next_slot(agent, current_minute):
    """获取下一个可用时间槽"""
    slots = {
        "jarvis": [5, 35],
        "hermes": [15, 45],
        "claude": [25, 55],
    }
    
    for slot in sorted(slots.get(agent, [5])):
        if current_minute < slot:
            return slot
    
    return slots[agent][0] + 60  # 下一轮
```

### 任务分批

```python
def stagger_tasks(tasks, batch_size=5):
    """分批交错任务"""
    if len(tasks) <= batch_size:
        return tasks
    
    batches = [tasks[i:i+batch_size] for i in range(0, len(tasks), batch_size)]
    
    staggered = []
    for i, batch in enumerate(batches):
        staggered.extend(batch)
        if i < len(batches) - 1:
            # 批次间延迟 = (i+1) * 5分钟
            pass
    
    return staggered
```

### 安静时段检查

```python
QUIET_HOURS_START = 23  # 23:00
QUIET_HOURS_END = 8    # 08:00

def can_notify(user_active=False):
    """是否允许发送通知"""
    if user_active:
        return True
    
    hour = datetime.now().hour
    
    if hour >= QUIET_HOURS_START or hour < QUIET_HOURS_END:
        return False
    
    return True
```

## 任务优先级

| 优先级 | 任务类型 | 槽位 |
|--------|---------|------|
| P0 | 紧急故障/安全 | 立即执行 |
| P1 | 重要客户消息 | 下一个槽 |
| P2 | 常规心跳检查 | 固定槽 |
| P3 | 后台同步/归档 | 空闲槽 |

## 注意事项

- 所有定时任务必须幂等（可重复执行）
- 检查点记录避免重复工作
- 结果保存到 reports/ 目录

---

*基于GBrain cron-scheduler设计，适配伟力机械三AI*