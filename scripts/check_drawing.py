# -*- coding: utf-8 -*-
import sys
import os

# Try to read the DWG file header to determine if it's really DWG or DXF
file_path = r"D:\桌面文件\伟力机械知识库\2026\图纸\PEII-III120-00 双层带线三模头 - 新设计dxf.dwg"

try:
    with open(file_path, 'rb') as f:
        header = f.read(16)
    
    header_hex = ' '.join(f'{b:02X}' for b in header)
    print(f"Header bytes: {header_hex}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    # DWG files start with "AC" followed by a version number
    # DXF files are text files starting with "SECTION" or "0"
    if header[:2] == b'AC':
        print("Format: DWG (AutoCAD)")
    elif header[:6] == b'SECTION':
        print("Format: DXF (ASCII)")
    elif header[:1] == b'0':
        print("Format: Possibly DXF (ASCII)")
    else:
        print("Format: Unknown")
except Exception as e:
    print(f"Error: {e}")
