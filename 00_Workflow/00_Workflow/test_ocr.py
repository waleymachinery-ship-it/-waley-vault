#!/usr/bin/env python3
"""Test OCR tools separately - Part 1: EasyOCR only"""
import os, sys, json, traceback, shutil, tempfile, numpy as np, cv2

src_dir = r"D:\桌面文件\伟力机械知识库\AI工程图模型测试"
images_src = [
    os.path.join(src_dir, "3dx_image1.jpeg"),
    os.path.join(src_dir, "3dx_image2.png"),
    os.path.join(src_dir, "3dx_image3.png"),
]

# Copy to temp
temp_dir = tempfile.mkdtemp(prefix="ocr_easy_")
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

# --- Test EasyOCR ---
print("\n" + "="*60)
print("Testing EasyOCR...")
try:
    import easyocr
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False, verbose=False)
    easy_results = {}
    for img_path in image_paths:
        bn = os.path.basename(img_path)
        print(f"  Processing: {bn}...", flush=True)
        try:
            text_results = reader.readtext(img_path, detail=1)
            items = []
            for item in text_results:
                if len(item) >= 3:
                    box, text, conf = item[0], item[1], item[2]
                    items.append({"text": text, "confidence": float(conf)})
                elif len(item) == 2:
                    text, conf = item
                    items.append({"text": text, "confidence": float(conf) if isinstance(conf, (int,float)) else 0.0})
            easy_results[bn] = {"items": items, "count": len(items)}
            print(f"    -> {len(items)} text blocks")
        except Exception as e:
            easy_results[bn] = {"error": str(e)}
            print(f"    -> ERROR: {e}")
    results["easyocr"] = easy_results
    print("  EasyOCR done.")
except Exception as e:
    results["easyocr"] = {"setup_error": str(e), "trace": traceback.format_exc()}

# Save
out_path = r"D:\桌面文件\伟力机械知识库\00_Workflow\ocr_raw_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Saved to {out_path}")
shutil.rmtree(temp_dir, ignore_errors=True)
print("Temp cleaned")