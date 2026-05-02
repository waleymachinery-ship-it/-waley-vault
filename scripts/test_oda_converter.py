# -*- coding: utf-8 -*-
import subprocess
import os

# Test ODA File Converter CLI
oda_exe = r"C:\Program Files\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"
input_file = r"D:\桌面文件\伟力机械知识库\2026\图纸\PEII-III120-00 双层带线三模头 - 新设计dxf.dwg"
output_dir = r"D:\桌面文件\伟力机械知识库\2026\图纸\output"
os.makedirs(output_dir, exist_ok=True)

# Try various CLI argument formats
print("Testing ODA File Converter CLI...")
print(f"Exe: {oda_exe}")
print(f"Input: {input_file}")
print(f"Output dir: {output_dir}")

# Test 1: Simple conversion with output dir
cmd = [
    oda_exe,
    input_file,
    output_dir,
    "ACAD2013",  # Source version
    "DXF",       # Target format
    "0"          # Layer (all)
]
print(f"\nTest 1 command: {cmd}")
result = subprocess.run(cmd, capture_output=True, text=True)
print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout[:500] if result.stdout else '(empty)'}")
print(f"Stderr: {result.stderr[:500] if result.stderr else '(empty)'}")
