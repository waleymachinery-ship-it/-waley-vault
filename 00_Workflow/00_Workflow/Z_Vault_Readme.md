# 伟力机械知识库 - 入口

> 本文件是 DeerFlow Agent 的知识库入口
> DeerFlow 容器内路径：`/mnt/obsidian-vault/`
> 最后更新：2026-04-07

## 目录结构

```
伟力机械知识库/
├── 00_Workflow/           # 工作流（生产排程、自动化）
├── 01_Production/         # 生产管理
├── 01_产品线/             # 产品体系
├── 02_Technology/         # 工艺技术
├── 02_知识库/             # 吹塑工艺知识
├── 03_Cost/               # 成本核算
├── 03_经营体系/           # 经营管理
├── 04_Order/              # 订单管理
├── 04_销售体系/           # 销售体系
├── 05_Mold/               # 模具管理
├── 05_战略规划/           # 战略规划
├── 06_Supplier/           # 供应商管理
├── 07_BP_Invest/          # 并购投资
├── 08_Tools/              # 工具（Obsidian等）
├── 2010~2026/             # 年度记录
└── 99_Archive/            # 档案
```

## 关键文件

| 文件 | 路径 | 内容 |
|------|------|------|
| 挤出系统设计核心逻辑 | `02_Technology/` | 螺杆塑化、材料、温度控制、熔体压力 |
| 生产排程V8.0 | `00_Workflow/` | 双模头方案、多单排产、外协管控 |
| 外协管控台账 | `00_Workflow/` | 伟立机械_V8.0_外协管控台账模板.xlsx |
| 吹塑机规格 | `01_产品线/` | 各机型容量范围、层数配置 |

## DeerFlow 使用指南

### 读取知识
- 查工艺 → `02_Technology/` 或 `02_知识库/`
- 查排程 → `00_Workflow/`
- 查成本 → `03_Cost/`
- 查订单 → `04_Order/`
- 查模具 → `05_Mold/`

### 写入知识
- 写新的分析结果 → 相关分类目录
- 命名格式：`YYYY-MM-DD_摘要.md`
- 包含 YAML frontmatter：`created`, `tags`

### 搜索示例
```
glob: /mnt/obsidian-vault/**/挤出*.md
grep: /mnt/obsidian-vault/** 壁厚
read_file: /mnt/obsidian-vault/00_Workflow/README.md
```
