#!/usr/bin/env python3
"""Minimal unstructured test"""
import os, sys
print("Starting...", flush=True)

try:
    from unstructured.partition.image import partition_image
    print("import ok", flush=True)
except Exception as e:
    print(f"import error: {e}", flush=True)
    sys.exit(1)

# Try with path string first
import tempfile, shutil, numpy as np, cv2

# Copy image to temp
with open(r'D:\桌面文件\伟力机械知识库\AI工程图模型测试\3dx_image2.png', 'rb') as f:
    data = f.read()
arr = np.frombuffer(data, dtype=np.uint8)
img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
tmp = tempfile.mktemp(suffix='.png')
cv2.imwrite(tmp, img)
print(f"Temp file: {tmp}", flush=True)

# Try partition with path string
print("Calling partition_image with path string...", flush=True)
try:
    elements = partition_image(tmp)
    print(f"Success: {len(elements)} elements", flush=True)
    for e in elements[:3]:
        print(f"  {type(e).__name__}: {str(e)[:80]}")
except Exception as e:
    print(f"partition_image error: {e}", flush=True)
    import traceback; traceback.print_exc()

os.remove(tmp)