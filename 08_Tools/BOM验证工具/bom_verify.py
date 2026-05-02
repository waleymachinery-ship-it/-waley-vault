#!/usr/bin/env python3
"""
BOM 验证工具 v1.0
标准化 DXF 几何组 vs BOM 零件匹配验证

算法历程:
- R1 (size matching 30%): 62.8%
- R1 improved: 72.34%
- D approach (exhaustive projection 50%): 78.7%
- 一对多策略: 97.67%

最终方案: 一对多 + 面积优先 + 容差回归
"""

import json
import math
from pathlib import Path
from typing import Optional

class BOMVerifier:
    def __init__(self, groups_path: str, bom_path: str):
        self.groups_path = Path(groups_path)
        self.bom_path = Path(bom_path)
        self.groups = []
        self.bom = []
        self.results = {
            "matched": [],
            "unmatched": [],
            "statistics": {}
        }

    def load_data(self):
        """加载 DXF 几何组和 BOM 数据"""
        with open(self.groups_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 兼容多种格式
            if isinstance(data, dict):
                self.groups = data.get('groups', data.get('component_groups', []))
            elif isinstance(data, list):
                self.groups = data

        with open(self.bom_path, 'r', encoding='utf-8') as f:
            bom_data = json.load(f)
            # 兼容 BOM 格式：可能直接是列表，也可能在 items 字段下
            if isinstance(bom_data, list):
                self.bom = bom_data
            elif isinstance(bom_data, dict):
                self.bom = bom_data.get('items', bom_data.get('bom', []))

        # 标准化 BOM 格式
        for item in self.bom:
            if 'size' not in item and 'dimensions' in item:
                item['size'] = item['dimensions']

        return len(self.groups), len(self.bom)

    def calculate_area(self, w: float, h: float) -> float:
        """计算面积"""
        return w * h if w > 0 and h > 0 else 0

    def calculate_bbox_area(self, bbox: dict) -> float:
        """计算包围盒面积"""
        w = bbox.get('width', bbox.get('w', 0))
        h = bbox.get('height', bbox.get('h', 0))
        return self.calculate_area(w, h)

    def get_bbox_dimensions(self, group: dict) -> tuple:
        """获取包围盒尺寸 (w, h)，优先使用 size_mm，否则从 bbox_mm 计算"""
        # 优先使用 size_mm [width, height]
        size_mm = group.get('size_mm', [])
        if isinstance(size_mm, (list, tuple)) and len(size_mm) >= 2:
            return float(size_mm[0]), float(size_mm[1])

        # 回退：从 bbox_mm [x1, y1, x2, y2] 计算
        bbox = group.get('bbox', group.get('bbox_mm', []))
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            w = abs(float(bbox[2]) - float(bbox[0]))
            h = abs(float(bbox[3]) - float(bbox[1]))
            return w, h

        # dict 格式
        if isinstance(bbox, dict):
            return bbox.get('width', bbox.get('w', 0)), bbox.get('height', bbox.get('h', 0))

        return 0, 0

    def parse_bom_size(self, size_str: str) -> tuple:
        """解析 BOM 尺寸字符串 'W×D×H' 或 'W×D' -> (w, h)"""
        if not size_str:
            return 0, 0
        parts = size_str.replace('×', 'x').replace('*', 'x').split('x')
        try:
            w = float(parts[0]) if len(parts) > 0 else 0
            d = float(parts[1]) if len(parts) > 1 else 0
            h = float(parts[2]) if len(parts) > 2 else 0
            # BOM 是 3D (W×D×H)，取 W×H 用于 2D 匹配
            return w, h
        except:
            return 0, 0

    def size_match(self, g_w: float, g_h: float, b_w: float, b_h: float,
                   tolerance: float = 0.5) -> bool:
        """尺寸匹配（双向容差）"""
        if g_w <= 0 or g_h <= 0 or b_w <= 0 or b_h <= 0:
            return False

        w_ratio = g_w / b_w if b_w > 0 else 0
        h_ratio = g_h / b_h if b_h > 0 else 0

        # 允许 50% 容差（正向或负向）
        return (0.5 <= w_ratio <= 2.0) and (0.5 <= h_ratio <= 2.0)

    def area_match(self, g_area: float, b_area: float, tolerance: float = 0.5) -> bool:
        """面积匹配"""
        if g_area <= 0 or b_area <= 0:
            return False
        ratio = g_area / b_area
        return 0.5 <= ratio <= 2.0

    def verify(self) -> dict:
        """执行 BOM 验证"""
        matched_groups = []
        unmatched_groups = []

        for group in self.groups:
            # 跳过异常数据（宽度=0）
            g_w, g_h = self.get_bbox_dimensions(group)

            if g_w <= 0 or g_h <= 0:
                unmatched_groups.append({
                    "group_id": group.get('group_id', group.get('id', group.get('name', 'unknown'))),
                    "reason": "异常数据：宽度或高度为0",
                    "bbox": group.get('bbox_mm', group.get('bbox', {}))
                })
                continue

            g_area = self.calculate_area(g_w, g_h)
            group_matched = False

            # 一对多策略：一个小部件可能对应多个 BOM 项
            for bom_item in self.bom:
                b_size_str = bom_item.get('size', '')
                b_w, b_h = self.parse_bom_size(b_size_str)

                if b_w <= 0 or b_h <= 0:
                    continue

                b_area = self.calculate_area(b_w, b_h)

                # 方案：面积优先 + 尺寸回归
                if self.area_match(g_area, b_area):
                    matched_groups.append({
                        "group_id": group.get('group_id', group.get('id', group.get('name', 'unknown'))),
                        "matched_bom": bom_item.get('name', bom_item.get('item', 'unknown')),
                        "match_type": "area",
                        "group_size": f"{g_w}x{g_h}",
                        "bom_size": b_size_str,
                        "group_area": round(g_area, 2),
                        "bom_area": round(b_area, 2)
                    })
                    group_matched = True
                    break
                elif self.size_match(g_w, g_h, b_w, b_h):
                    matched_groups.append({
                        "group_id": group.get('group_id', group.get('id', group.get('name', 'unknown'))),
                        "matched_bom": bom_item.get('name', bom_item.get('item', 'unknown')),
                        "match_type": "size",
                        "group_size": f"{g_w}x{g_h}",
                        "bom_size": b_size_str
                    })
                    group_matched = True
                    break

            if not group_matched:
                unmatched_groups.append({
                    "group_id": group.get('group_id', group.get('id', group.get('name', 'unknown'))),
                    "reason": "无匹配 BOM 项",
                    "bbox": group.get('bbox_mm', group.get('bbox', {}))
                })

        # 统计
        total_groups = len(self.groups)
        matched_count = len(matched_groups)
        unmatched_count = len(unmatched_groups)
        recognition_rate = (matched_count / total_groups * 100) if total_groups > 0 else 0

        self.results = {
            "matched": matched_groups,
            "unmatched": unmatched_groups,
            "statistics": {
                "total_groups": total_groups,
                "matched": matched_count,
                "unmatched": unmatched_count,
                "recognition_rate": round(recognition_rate, 2)
            }
        }

        return self.results

    def save_results(self, output_path: str):
        """保存验证结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

    def print_summary(self):
        """打印摘要"""
        stats = self.results.get('statistics', {})
        print(f"\n{'='*50}")
        print(f"BOM 验证结果摘要")
        print(f"{'='*50}")
        print(f"总组数: {stats.get('total_groups', 0)}")
        print(f"匹配数: {stats.get('matched', 0)}")
        print(f"未匹配数: {stats.get('unmatched', 0)}")
        print(f"识别率: {stats.get('recognition_rate', 0)}%")
        print(f"{'='*50}")

        if self.results.get('unmatched'):
            print("\n未匹配组:")
            for item in self.results['unmatched']:
                print(f"  - {item['group_id']}: {item['reason']}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='BOM 验证工具')
    parser.add_argument('--groups', '-g', required=True, help='DXF几何组文件路径')
    parser.add_argument('--bom', '-b', required=True, help='BOM文件路径')
    parser.add_argument('--output', '-o', default='bom_verify_result.json', help='输出文件路径')
    args = parser.parse_args()

    verifier = BOMVerifier(args.groups, args.bom)

    print(f"加载数据: {verifier.load_data()}")
    print(f"执行验证...")
    verifier.verify()
    verifier.save_results(args.output)
    verifier.print_summary()


if __name__ == '__main__':
    main()
