# Brain-First Lookup Protocol - 三AI版

> 每次外部API调用前，必须先查脑

## 核心原则

**脑里有 → 用脑 | 脑里没有 → 才调外部API**

## 标准查询流程（5步）

### Step 1: 关键词搜索
```bash
gbrain search "设备型号"
# 或
weili-vault__search "设备型号"
```

### Step 2: 混合搜索
```bash
gbrain query "这个故障怎么处理"
# 或  
weili-vault__query "这个故障怎么处理"
```

### Step 3: 读取完整页面
```bash
gbrain get people/陈总
# 或
weili-vault__read_vault_file "people/陈总.md"
```

### Step 4: 检查反向链接
```bash
gbrain get_backlinks "people/陈总"
# 或
weili-vault__get_backlinks("people/陈总")
```

### Step 5: 检查时间线
```bash
gbrain timeline "people/陈总" --limit 5
# 或
weili-vault__get_timeline("people/陈总")
```

### 判断逻辑

```
Step 1-2 有 >= 3 条相关结果 → 直接用脑
Step 3-5 有内容 → 用脑 + 补充外部
全空 → 才调外部API
```

## 场景应用

### 场景1: 客户问设备价格

```
1. 查 brain → 产品目录已有
2. 脑里有 → 直接回答
3. 脑里没有 → 调ERP/CRM查
```

### 场景2: 客户问故障处理

```
1. 查 brain → 故障记录库
2. 找到类似案例 → 用历史方案
3. 没有类似 → 调知识库搜索
```

### 场景3: 新建BOM验证

```
1. 查 brain → 历史验证结果
2. 同型号有过 → 复用
3. 没有 → Claude Code执行验证
```

## 维护规则

- 每次回答后 → 更新脑（如果学到新东西）
- 用户直接说的 → 最高优先级写入
- 外部API查到的 → 标注来源

## 反模式（不要做）

- ❌ 直接调API不查脑
- ❌ 脑里有但不用
- ❌ 不标注信息来源
- ❌ 覆盖用户原始说法

---

*基于GBrain brain-ops设计，适配伟力机械三AI*