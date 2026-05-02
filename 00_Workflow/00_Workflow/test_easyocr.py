#!/usr/bin/env python3
"""Test OCR tools separately"""
import os, sys, json, traceback, shutil, tempfile, numpy as np, cv2

src_dir = r"D:\桌面文件\伟力机械知识库\AI工程图模型测试"
images_src = [
    os.path.join(src_dir, "3dx_image1.jpeg"),
    os.path.join(src_dir, "3dx_image2.png"),
    os.path.join(src_dir, "3dx_image3.png"),
]

# Copy to temp
temp_dir = tempfile.mkdtemp(prefix="ocr_test_")
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
        print(f"  Copied {bn} -> {dst} ({img.shape})")

results = {}

# --- Test EasyOCR only ---
print("\n" + "="*60)
print("Testing EasyOCR only...")
try:
    import easyocr
    os.environ['CUDA_VISIBLE_DEVICES'] = ''  # force CPU
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False, verbose=False)
    easy_results = {}
    for img_path in image_paths:
        bn = os.path.basename(img_path)
        print(f"  Processing: {bn}...")
        text_results = reader.readtext(img_path, detail=1)
        easy_results[bn] = {
            "texts": [(t, float(b)) for b, t, _ in text_results],
            "count": len(text_results)
        }
        print(f"    -> {len(text_results)} text blocks")
    results["easyocr"] = easy_results
    print("  EasyOCR done.")
except Exception as e:
    results["easyocr"] = {"error": str(e), "trace": traceback.format_exc()}
    print(f"  EasyOCR error: {e}")

# Save intermediate
out_path = r"D:\桌面文件\伟力机械知识库\00_Workflow\ocr_raw_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nSaved to {out_path}")
shutil.rmtree(temp_dir, ignore_errors=True)