#!/usr/bin/env python3
"""
signal_detector.py — 飞书群消息信号检测器
功能：
  - 读取飞书群最近消息
  - 提取实体（公司名/产品名/需求/故障现象）
  - 写入知识库 (signal_detection_log.json)
  - 同步到 Z_Memory_Sync.json

触发方式：每次 Jarvis cron（30分钟一次）调用
用法：python signal_detector.py
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# 尝试导入 requests（用于飞书 API）
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ============== 配置 ==============
VAULT_ROOT = Path(r"D:\桌面文件\伟力机械知识库")
SIGNAL_LOG_PATH = VAULT_ROOT / "memory" / "signal_detection_log.json"
ZMONEY_PATH = VAULT_ROOT / "00_Workflow" / "memory" / "Z_Memory_Sync.json"
FEISHU_APP_ID = "cli_a942303fdef99cd1"
FEISHU_APP_SECRET = "JrhR2ynU6ogqxZOgKNRxZdXz6Xq0Ot5r"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
DEFAULT_CHAT_ID = "oc_2a35b9e85451a57f9c64f93f15912176"

# ============== 飞书 API ==============

_tenant_token = None
_token_expires_at = 0

def get_tenant_token():
    global _tenant_token, _token_expires_at
    if _tenant_token and datetime.now().timestamp() < _token_expires_at - 60:
        return _tenant_token
    
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    data = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    resp = requests.post(url, json=data, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"获取 tenant token 失败: {result}")
    
    _tenant_token = result["tenant_access_token"]
    _token_expires_at = datetime.now().timestamp() + result.get("expire", 7200)
    return _tenant_token

def read_feishu_messages(chat_id: str, limit: int = 20):
    """读取飞书群消息（直接调用API，不需要MCP）"""
    token = get_tenant_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"{FEISHU_API_BASE}/im/v1/messages"
    params = {
        "container_id_type": "chat",
        "container_id": chat_id,
        "page_size": min(limit, 50),
    }
    
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"读取消息失败: {result}")
    
    messages = []
    for item in result.get("data", {}).get("items", []):
        msg_type = item.get("msg_type", "")
        content = item.get("body", {}).get("content", "")
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except:
                pass
        
        messages.append({
            "message_id": item.get("message_id"),
            "msg_type": msg_type,
            "content": content,
            "create_time": item.get("create_time"),
            "sender": item.get("sender", {}),
        })
    return messages

# ============== 实体提取 ==============

# 中空挤出吹塑机相关产品词
PRODUCT_KEYWORDS = [
    "吹塑机", "挤出机", "中空机", "吹瓶机", "注塑机",
    "WLA", "WLB", "WLH", "WLU", "WLZ",
    "30L", "50L", "100L", "200L",
    "PE", "PP", "PVC", "PET",
]

# 故障现象关键词
FAULT_KEYWORDS = [
    "不工作", "故障", "报错", "异常", "坏", "漏", "堵",
    "无法启动", "不上料", "不下料", "温度", "压力",
    "异响", "震动", "卡", "停", "烧", "焦",
]

# 需求意图关键词
INTENT_KEYWORDS = [
    "需要", "想要", "询价", "报价", "多少钱", "价格",
    "规格", "参数", "型号", "选型", "配置",
    "交货", "货期", "交期", "生产", "产能",
    "合作", "代理", "代理", "批发", "采购",
]

def extract_text_from_message(msg: dict) -> str:
    """从消息中提取文本内容"""
    msg_type = msg.get("msg_type", "")
    content = msg.get("content", {})
    
    if msg_type == "text":
        if isinstance(content, dict):
            return content.get("text", "")
        return str(content)
    elif msg_type == "post":
        if isinstance(content, dict):
            texts = []
            for section in content.get("content", []):
                if isinstance(section, list):
                    for item in section:
                        if isinstance(item, dict) and item.get("tag") == "text":
                            texts.append(item.get("text", ""))
            return " ".join(texts)
    return ""

def extract_signals(text: str) -> dict:
    """从文本中提取信号"""
    signals = {
        "products": [],
        "faults": [],
        "intents": [],
        "mentions": [],
    }
    
    if not text:
        return signals
    
    text_lower = text.lower()
    
    # 产品词提取
    for kw in PRODUCT_KEYWORDS:
        if kw.lower() in text_lower:
            signals["products"].append(kw)
    
    # 故障词提取
    for kw in FAULT_KEYWORDS:
        if kw in text:
            signals["faults"].append(kw)
    
    # 意图词提取
    for kw in INTENT_KEYWORDS:
        if kw in text:
            signals["intents"].append(kw)
    
    # @mention 提取（手机号/邮箱/公司名等）
    mention_patterns = [
        r'@[\w\u4e00-\u9fa5]+',  # @人
        r'[\w\.-]+@[\w\.-]+\.\w+',  # 邮箱
        r'1[3-9]\d{9}',  # 手机号
    ]
    for pattern in mention_patterns:
        for m in re.findall(pattern, text):
            signals["mentions"].append(m)
    
    # 去重
    for k in signals:
        signals[k] = list(set(signals[k]))
    
    return signals

def process_messages(messages: list, last_check_time: str = None) -> list:
    """处理消息列表，返回检测到的信号"""
    results = []
    
    for msg in messages:
        create_time = msg.get("create_time", "")
        
        # 如果指定了 last_check_time，跳过更早的消息
        if last_check_time and create_time <= last_check_time:
            continue
        
        text = extract_text_from_message(msg)
        if not text.strip():
            continue
        
        signals = extract_signals(text)
        
        # 只有检测到有效信号才记录
        has_signal = any(signals[k] for k in ["products", "faults", "intents"])
        
        if has_signal:
            results.append({
                "message_id": msg.get("message_id"),
                "create_time": create_time,
                "sender": msg.get("sender", {}),
                "text_preview": text[:200],
                "signals": signals,
            })
    
    return results

# ============== 知识库读写 ==============

def read_signal_log() -> dict:
    """读取信号日志"""
    if not SIGNAL_LOG_PATH.exists():
        return {"last_check_time": None, "signals": []}
    
    try:
        with open(SIGNAL_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"last_check_time": None, "signals": []}

def write_signal_log(data: dict):
    """写入信号日志（原子操作）"""
    temp_path = SIGNAL_LOG_PATH.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if SIGNAL_LOG_PATH.exists():
        os.remove(SIGNAL_LOG_PATH)
    os.replace(temp_path, SIGNAL_LOG_PATH)

def append_z_memory_entry(agent: str, content: str, tags: list = None):
    """追加到 Z_Memory_Sync"""
    data = read_json(ZMONEY_PATH)
    
    entry_id = f"{agent}-signal-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    new_entry = {
        "id": entry_id,
        "agent": agent,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "content": content,
        "tags": tags or ["signal-detection"],
        "confidence": 0.8
    }
    
    data["entries"] = data.get("entries", [])
    data["entries"].append(new_entry)
    data["version"] = data.get("version", "v0")
    if isinstance(data["version"], str) and data["version"].startswith("v"):
        data["version"] = "v" + str(int(data["version"][1:]) + 1)
    else:
        data["version"] = data.get("version", 0) + 1
    data["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    data["last_writer"] = agent
    
    write_json(ZMONEY_PATH, data)
    return entry_id

def read_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: Path, data: dict):
    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if path.exists():
        os.remove(path)
    os.replace(temp_path, path)

# ============== 主逻辑 ==============

def run(chat_id: str = DEFAULT_CHAT_ID, limit: int = 20):
    """运行信号检测"""
    if not HAS_REQUESTS:
        print("ERROR: requests 库未安装，无法调用飞书 API")
        return {"success": False, "error": "requests not available"}
    
    print(f"[signal_detector] 开始检测飞书群消息... chat_id={chat_id}")
    
    # 读取上次检查时间
    signal_log = read_signal_log()
    last_check = signal_log.get("last_check_time")
    print(f"[signal_detector] 上次检查时间: {last_check or '首次运行'}")
    
    # 读取消息
    messages = read_feishu_messages(chat_id, limit=limit)
    print(f"[signal_detector] 获取到 {len(messages)} 条消息")
    
    if not messages:
        return {"success": True, "signals_found": 0}
    
    # 处理消息
    new_signals = process_messages(messages, last_check_time=last_check)
    print(f"[signal_detector] 检测到 {len(new_signals)} 条新信号")
    
    if not new_signals:
        # 更新时间戳但不记录
        signal_log["last_check_time"] = messages[0].get("create_time", "")
        write_signal_log(signal_log)
        return {"success": True, "signals_found": 0}
    
    # 追加到信号日志
    signal_log["signals"] = signal_log.get("signals", [])
    signal_log["signals"].extend(new_signals)
    signal_log["last_check_time"] = messages[0].get("create_time", "")
    write_signal_log(signal_log)
    
    # 同步到 Z_Memory
    signal_summary = f"【信号检测】检测到 {len(new_signals)} 条新信号:\n"
    for s in new_signals:
        signal_summary += f"- [{s['create_time']}] {s['signals']}\n"
    
    append_z_memory_entry("jarvis", signal_summary, tags=["signal-detection", "feishu"])
    
    print(f"[signal_detector] 完成，写入 {len(new_signals)} 条信号到知识库")
    return {"success": True, "signals_found": len(new_signals), "signals": new_signals}

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    chat_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CHAT_ID
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    result = run(chat_id=chat_id, limit=limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
