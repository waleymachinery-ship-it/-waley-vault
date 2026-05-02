# -*- coding: utf-8 -*-
"""
文件夹整理脚本 - 按类型和日期分类
"""
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 源文件夹
source = r"D:\桌面文件"

# 基础分类关键词
type_keywords = {
    "12L": "产品型号/12L",
    "8L": "产品型号/8L", 
    "90": "产品型号/90系列",
    "WLH": "产品型号/WLH",
    "WLU": "产品型号/WLU",
    "PE": "产品型号/PE系列",
    "CPJ": "产品型号/CPJ",
    "EBpro": "软件/威纶通",
    "程序": "程序文件",
    "PLC": "程序文件/PLC",
    "配方": "配方文件",
    "模具": "模具",
    "直压": "产品型号/直压式",
    "合同": "合同",
    "报价": "报价",
    "视频": "视频",
    "PDF": "文档/PDF",
    "图纸": "图纸",
    "项目": "项目",
    "设备": "设备",
    "物料": "物料",
    "生产": "生产",
    "成本": "财务/成本",
    "销售": "销售",
    "PMC": "PMC",
    "外协": "外协",
}

def get_folder_category(folder_name):
    """根据文件夹名判断分类"""
    for keyword, category in type_keywords.items():
        if keyword in folder_name:
            return category
    return "其他"

def get_date_folder(ctime):
    """根据创建日期返回年份文件夹"""
    year = datetime.fromtimestamp(ctime).year
    return str(year)

def organize_folders():
    """整理文件夹"""
    stats = {}
    processed = []
    
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        
        # 只处理文件夹
        if not os.path.isdir(src_path):
            continue
            
        # 跳过特定文件夹
        skip_folders = ["伟力机械知识库", "贾维斯知识库", "MySkills", "视频", "新建文件夹"]
        if item in skip_folders:
            print(f"[SKIP] {item}")
            continue
        
        # 获取文件夹创建日期
        ctime = os.path.getctime(src_path)
        year = get_date_folder(ctime)
        
        # 获取分类
        category = get_folder_category(item)
        
        # 目标路径：年份/分类/文件夹名
        target_folder = os.path.join(source, "伟力机械知识库", year, category, item)
        
        try:
            # 创建目标文件夹
            os.makedirs(os.path.dirname(target_folder), exist_ok=True)
            
            # 移动文件夹
            shutil.move(src_path, target_folder)
            print(f"[OK] {item} -> {year}/{category}/")
            
            key = f"{year}/{category}"
            stats[key] = stats.get(key, 0) + 1
            
        except Exception as e:
            print(f"[X] 移动失败 {item}: {e}")
    
    print("\n=== 文件夹整理完成 ===")
    for key, count in sorted(stats.items()):
        print(f"{key}: {count} 个文件夹")

if __name__ == "__main__":
    organize_folders()
