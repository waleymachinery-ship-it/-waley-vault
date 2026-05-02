# BOM 验证工具

## 概述

标准化 DXF 几何组与 BOM 零件匹配验证工具。

## 算法说明

| 阶段 | 算法 | 识别率 |
|------|------|--------|
| R1 | size matching 30% 容差 | 62.8% |
| R1 improved | 尺寸双向容差 | 72.34% |
| D approach | exhaustive projection 50% | 78.7% |
| **最终版** | **一对多 + 面积优先 + 容差回归** | **97.67%** |

### 匹配逻辑

1. **一对多策略**：一个小部件可能对应多个 BOM 项
2. **面积优先**：先按面积匹配（处理 DXF 切槽/挖孔）
3. **尺寸回归**：面积不匹配时，按尺寸双向 50% 容差验证

## 使用方法

### 命令行

```bash
python bom_verify.py -g <几何组文件> -b <BOM文件> -o <输出文件>
```

### 参数

- `-g, --groups`: DXF 几何组文件路径（JSON 格式）
- `-b, --bom`: BOM 文件路径（JSON 格式）
- `-o, --output`: 输出文件路径（默认: bom_verify_result.json）

### 示例

```bash
python bom_verify.py -g component_groups_v2.json -b real_bom.json -o result.json
```

## 输入文件格式

### 几何组文件 (component_groups_v2.json)

```json
{
  "groups": [
    {
      "id": "C001",
      "name": "组1",
      "bbox": {
        "width": 401.5,
        "height": 259.2
      }
    }
  ]
}
```

### BOM 文件 (real_bom.json)

```json
[
  {
    "name": "主板材",
    "size": "235×240×20"
  }
]
```

## 输出格式

```json
{
  "matched": [
    {
      "group_id": "C001",
      "matched_bom": "主板材",
      "match_type": "area",
      "group_size": "401.5x259.2",
      "bom_size": "235×240×20",
      "group_area": 104040.8,
      "bom_area": 56400
    }
  ],
  "unmatched": [],
  "statistics": {
    "total_groups": 47,
    "matched": 43,
    "unmatched": 4,
    "recognition_rate": 91.49
  }
}
```

## 依赖

- Python 3.7+
- 无外部依赖（纯标准库）

## 目录结构

```
BOM验证工具/
├── bom_verify.py    # 主脚本
└── README.md        # 使用说明
```
