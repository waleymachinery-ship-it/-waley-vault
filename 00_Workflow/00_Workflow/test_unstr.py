#!/usr/bin/env python3
"""Test unstructured OCR only"""
import os, sys, json, traceback, shutil, tempfile, numpy as np, cv2

src_dir = r"D:\桌面文件\伟力机械知识库\AI工程图模型测试"
images_src = [
    os.path.join(src_dir, "3dx_image1.jpeg"),
    os.path.join(src_dir, "3dx_image2.png"),
    os.path.join(src_dir, "3dx_image3.png"),
]

temp_dir = tempfile.mkdtemp(prefix="ocr_unstr_")
image_paths = []
for src in images_src:
    bn = os.path.basename(src)
    dst = os.path.join(temp_dir, bn)
    with open(src, 'rb') as f:
        data = f.read()
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is not None:
        cv2.imwrite(dst, img)
        image_paths.append(dst)
        print(f"  Copied {bn} ({img.shape})")

results = {}

print("="*60)
print("Testing unstructured...")
try:
    from unstructured.partition.image import partition_image
    unstruct_results = {}
    for img_path in image_paths:
        bn = os.path.basename(img_path)
        print(f"  Processing: {bn}...", flush=True)
        try:
            elements = partition_image(img_path)
            text_output = "\n".join([str(el) for el in elements])
            unstruct_results[bn] = {
                "text": text_output[:5000],
                "count": len(elements),
                "types": list(set(type(el).__name__ for el in elements))
            }
            print(f"    -> {len(elements)} elements: {unstruct_results[bn]['types']}")
        except Exception as e:
            unstruct_results[bn] = {"error": str(e), "trace": traceback.format_exc()}
            print(f"    -> ERROR: {e}")
    results["unstructured"] = unstruct_results
    print("  unstructured done.")
except Exception as e:
    results["unstructured"] = {"setup_error": str(e), "trace": traceback.format_exc()}

out_path = r"D:\桌面文件\伟力机械知识库\00_Workflow\ocr_raw_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Saved to {out_path}")
shutil.rmtree(temp_dir, ignore_errors=True)