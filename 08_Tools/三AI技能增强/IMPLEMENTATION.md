# 三AI技能增强方案

> 基于GBrain 29 Skills设计，提炼3个最值得落地的技能，适配伟力机械三AI体系
> 版本：v1.0 | 日期：2026-04-25 | 作者：Jarvis

---

## 一、signal-detector（信号捕获）

**核心理念：** 每次消息触发，自动捕获实体（人物/公司/概念）和用户原创想法。

### 当前三AI的问题
- 消息处理后没有自动提取实体
- 用户想法没有沉淀到知识库
- 重要信息靠手动记录

### 落地实现

#### 触发条件
- 每次收到飞书群消息（不仅是@ Jarvis）
- 消息类型：客户咨询、技术问题、需求变更

#### 捕获内容

**实体类型：**
| 实体 | 存储位置 |
|------|---------|
| 客户/联系人 | `D:\桌面文件\伟力机械知识库\people\` |
| 公司 | `D:\桌面文件\伟力机械知识库\companies\` |
| 产品/设备 | `D:\桌面文件\伟力机械知识库\products\` |
| 问题/故障 | `D:\桌面文件\伟力机械知识库\faults\` |

**创意/想法：**
- 用户原创观点 → `originals/YYYY-MM-DD-{slug}.md`
- 解决方案 → `solutions/YYYY-MM-DD-{slug}.md`

#### 实现代码（Jarvis Hook）

```python
# Jarvis消息处理钩子 - signal_detector.py

def extract_entities(message_content):
    """从消息提取实体"""
    entities = []
    
    # 1. 提取产品型号（正则匹配）
    product_patterns = [
        r'WLA\d+[-\w]*',
        r'WLU\d+[-\w]*', 
        r'WLH\d+[-\w]*',
        r'\d+L[-\d]*',  # 30L-200L
    ]
    
    # 2. 提取问题关键词
    fault_keywords = [
        '漏气', '异响', '不启动', '温度异常', 
        '压力不稳', '产量低', '产品缺陷'
    ]
    
    # 3. 提取客户/公司名（飞书昵称 + 历史记录）
    # ...
    
    return entities

def capture_original_thinking(message_content, sender):
    """捕获用户原创想法"""
    # 检测是否包含决策、结论、方案
    # 如果是 → 写入 originals/ 目录
    pass

def on_message(message):
    entities = extract_entities(message.content)
    for entity in entities:
        # 检查是否已存在
        # 如果不存在且notable → 创建页面
        pass
    
    # 捕获原创想法（非闲聊）
    if is_substantial(message):
        capture_original_thinking(message.content, message.sender)
```

### 预期效果
- 每次客户咨询自动提取：设备型号、故障类型、需求
- 用户决策/结论自动沉淀到知识库
- 无需手动记录，客户历史完整保留

---

## 二、brain-ops lookup protocol（脑优先查询）

**核心理念：** 每次执行外部API调用前，必须先查脑。脑里有就不用调用外部API。

### 当前三AI的问题
- 直接调用外部API（搜索、查询）不看知识库
- 重复查询同样的信息
- 知识库和实时信息脱节

### 落地实现

#### 标准流程（5步）

```
1. gbrain search "关键词"        # 关键词搜索
2. gbrain query "自然语言问题"   # 混合搜索  
3. gbrain get <slug>             # 读取完整页面
4. 检查 backlinks               # 谁引用过这个
5. 检查 timeline                # 最近有什么事件

只有4步都为空 → 才调用外部API
```

#### 代码示例

```python
def query_before_external(query, use_external=True):
    """查脑再外部API"""
    
    # Step 1-2: 查脑
    brain_results = gbrain.query(query)
    
    if brain_results and len(brain_results) >= 3:
        # 脑里有足够信息，直接用
        return {"source": "brain", "data": brain_results}
    
    # Step 3-5: 更深入查
    page = gbrain.get(slug)
    backlinks = gbrain.get_backlinks(slug)
    timeline = gbrain.get_timeline(slug, limit=5)
    
    if page or backlinks or timeline:
        return {"source": "brain", "data": {...}}
    
    # 只有全空才调外部API
    if use_external:
        return call_external_api(query)
    
    return {"source": "none", "data": None}
```

#### 应用场景

| 场景 | 当前行为 | 改进后 |
|------|---------|--------|
| 客户问设备价格 | 直接搜 | 先查产品目录库 |
| 客户问故障处理 | 直接搜 | 先查故障记录库 |
| 新建BOM验证 | 直接搜 | 先查历史验证结果 |

### 预期效果
- 减少重复API调用（省成本）
- 知识库利用率提升
- 答案一致性提高

---

## 三、cron-scheduler stagger（错峰调度）

**核心理念：** 任务错开执行，避免同一时刻触发。安静时段不打扰。

### 当前三AI的问题
- 多个任务同时触发（如同时写Z_Memory）
- 深夜仍发送通知
- 无分批处理机制

### 落地实现

#### 时间槽分配

```
分钟槽: 05, 10, 15, 20, 25, 30, 35, 40, 45, 50

Jarvis:  每30分钟心跳 → :05, :35
Hermes:  任务轮询 → :15, :45  
Claude:  Vault检查 → :25, :55

同一AI的任务之间至少错开15分钟
```

#### 代码实现

```python
# task_scheduler.py

SLOTS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

def get_next_slot(agent, current_time):
    """获取下一个可用时间槽"""
    current_minute = current_time.minute
    
    # 每个AI有固定槽位
    agent_slots = {
        "jarvis": [5, 35],   # 每30分钟
        "hermes": [15, 45], # 每30分钟
        "claude": [25, 55], # 每30分钟
    }
    
    slots = agent_slots.get(agent, [5])
    
    # 找下一个可用槽
    for slot in sorted(slots):
        if current_minute < slot:
            return slot
    
    # 下一轮
    return slots[0] + 60

def stagger_tasks(tasks):
    """分批交错任务"""
    if len(tasks) <= 1:
        return tasks
    
    # 大任务拆小
    batch_size = 5
    batches = [tasks[i:i+batch_size] for i in range(0, len(tasks), batch_size)]
    
    # 批次之间加延迟
    staggered = []
    for i, batch in enumerate(batches):
        staggered.extend(batch)
        if i < len(batches) - 1:
            # 批次间延迟 = 批次 index * 5分钟
            delay = (i + 1) * 5 * 60  # 秒
            # 记录延迟任务
            pass
    
    return staggered
```

#### 安静时段

```python
QUIET_HOURS = {
    "start": 23,  # 23:00
    "end": 8,     # 08:00
}

def should_notify(user_active=False):
    """是否发送通知"""
    if user_active:
        return True  # 用户醒着，随时可通知
    
    current_hour = datetime.now().hour
    if QUIET_HOURS["start"] <= current_hour or current_hour < QUIET_HOURS["end"]:
        return False  # 安静时段不通知
    
    return True
```

### 预期效果
- 多AI任务不再同时写Vault
- 深夜不打扰
- 大批量任务自动分批，避免卡顿

---

## 四、实施优先级

| 技能 | 优先级 | 工作量 | 风险 |
|------|--------|--------|------|
| brain-ops lookup | P0 | 低 | 无 |
| cron-scheduler stagger | P1 | 中 | 低 |
| signal-detector | P2 | 高 | 中 |

**建议顺序：**
1. 先落地 brain-ops（低风险，立刻生效）
2. 再落地 cron-scheduler stagger（避免冲突）
3. 最后 signal-detector（需要持续优化）

---

## 五、代码存放位置

```
D:\桌面文件\伟力机械知识库\08_Tools\三AI技能增强\
├── signal_detector.py      # 信号捕获
├── brain_ops.py            # 脑优先查询
├── task_scheduler.py       # 错峰调度
└── IMPLEMENTATION.md       # 本文档
```

---

*最后更新：2026-04-25*