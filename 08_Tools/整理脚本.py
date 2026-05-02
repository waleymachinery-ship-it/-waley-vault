# -*- coding: utf-8 -*-
import sys
import os
import shutil
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 源文件夹
source = r"D:\桌面文件"

# 目标文件夹
target_base = r"D:\桌面文件\伟力机械知识库"

# 文件类型映射
file_types = {
    "图纸": [".dwg", ".dxf", ".step", ".stp", ".stl", ".prt", ".igs", ".iges", 
             ".gxw", ".prx", ".sldprt", ".x_t", ".x_b", ".3dm", ".obj", ".fbx"],
    "合同": ["contract", "合同"],
    "报价": ["quotation", "报价", "quote", "报价单", "rfq", "quot"],
    "PDF": [".pdf"],
    "Word": [".doc", ".docx"],
    "Excel": [".xls", ".xlsx"],
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "视频": [".mp4", ".mov", ".avi", ".mkv"],
    "压缩": [".zip", ".rar", ".7z"],
}

def get_category(filename):
    """根据文件名或扩展名判断类别"""
    fname = filename.lower()
    ext = Path(filename).suffix.lower()
    
    # 先检查文件名关键词
    for cat, keywords in file_types.items():
        if cat in ["合同", "报价"]:
            for kw in keywords:
                if kw in fname:
                    return cat
    
    # 再按扩展名分类
    if ext in [".dwg", ".dxf", ".step", ".stp", ".stl", ".prt", ".igs", ".iges", 
               ".gxw", ".prx", ".sldprt", ".x_t", ".x_b", ".3dm"]:
        return "图纸"
    elif ext in [".pdf"]:
        return "PDF"
    elif ext in [".doc", ".docx"]:
        return "Word"
    elif ext in [".xls", ".xlsx"]:
        return "Excel"
    elif ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        return "图片"
    elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
        return "视频"
    elif ext in [".zip", ".rar", ".7z"]:
        return "压缩"
    
    return "其他"

def organize_files():
    """整理文件"""
    stats = {}
    
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        
        # 跳过文件夹
        if os.path.isdir(src_path):
            # 如果是知识库文件夹，跳过
            if "知识库" in item:
                print(f"[SKIP] 文件夹: {item}")
            else:
                print(f"[FOLDER] 发现文件夹: {item} (待处理)")
            continue
        
        # 获取文件分类
        category = get_category(item)
        
        # 创建目标文件夹
        target_folder = os.path.join(target_base, category)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        
        # 移动文件
        dst_path = os.path.join(target_folder, item)
        
        # 如果目标文件已存在，加编号
        if os.path.exists(dst_path):
            name, ext = os.path.splitext(item)
            dst_path = os.path.join(target_folder, f"{name}_copy{ext}")
        
        try:
            shutil.move(src_path, dst_path)
            print(f"[OK] {item} -> {category}/")
            stats[category] = stats.get(category, 0) + 1
        except Exception as e:
            print(f"[X] 移动失败 {item}: {e}")
    
    print("\n=== 整理完成 ===")
    for cat, count in stats.items():
        print(f"{cat}: {count} 个文件")

if __name__ == "__main__":
    organize_files()
