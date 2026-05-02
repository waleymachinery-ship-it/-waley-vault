import json
from pathlib import Path

path = Path(r"D:\桌面文件\伟力机械知识库\memory\signal_detection_log.json")
if path.exists():
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"信号数: {len(data.get('signals', []))}")
    print(f"最后检查: {data.get('last_check_time', 'N/A')}")
    if data.get('signals'):
        s = data['signals'][-1]
        print(f"最新信号: {s.get('create_time')}")
        print(f"信号内容: {s.get('signals')}")
        print(f"文本预览: {s.get('text_preview', '')[:100]}")
else:
    print("文件不存在")
