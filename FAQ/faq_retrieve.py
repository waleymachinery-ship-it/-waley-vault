#!/usr/bin/env python3
"""
faq_retrieve.py
FAQ检索工具 - Claude调用专用
用法: python3 faq_retrieve.py "客户消息文本"

返回: 最匹配的FAQ记录（JSON格式）
"""

import json
import sys
import os

# 知识库路径（Windows格式）
KB_DIR = "/root/waley-vault/FAQ"
FAQ_FILE = "/root/waley-vault/FAQ/chat_knowledge_base_v2.json"
INTENT_FILE = "/root/waley-vault/FAQ/intent_detection_rules.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_intent(message: str, intent_rules: dict) -> dict:
    """检测客户消息的意图类型"""
    lower_msg = message.lower()
    
    # intent_detection_rules.json v2.0 结构映射
    intent_type_map = {
        "purchase_signals": "purchase_high",      # 高意向 → 触发Leads
        "purchase_inquiry_signals": "purchase",    # 一般咨询 → 只回复
        "fault_signals": "fault",
        "technical_signals": "technical",
        "maintenance_signals": "maintenance",
        "greeting_signals": "greeting",
        "thanks_signals": "thanks",
        "negative_signals": "negative"
    }
    
    for rule_key, rule_val in intent_rules.items():
        if rule_key in ("version", "created_at", "description"):
            continue
        if not isinstance(rule_val, dict):
            continue
        keywords = rule_val.get("keywords", [])
        threshold = rule_val.get("threshold", 1)
        matches = [kw for kw in keywords if kw.lower() in lower_msg]
        if len(matches) >= threshold:
            return {
                "intent": intent_type_map.get(rule_key, rule_key),
                "action": rule_val.get("action", "route_to_knowledge_base"),
                "matched_keywords": matches
            }
    
    return {"intent": "unknown", "action": "route_to_knowledge_base", "matched_keywords": []}


def calculate_score(message: str, faq: dict) -> int:
    """计算消息与FAQ的匹配分数"""
    lower_msg = message.lower()
    score = 0
    
    # keywords匹配（最高权重）
    for kw in faq.get("keywords", []):
        if kw.lower() in lower_msg:
            score += 10
    
    # question_patterns匹配（高权重）
    for pattern in faq.get("question_patterns", []):
        if pattern.lower() in lower_msg:
            score += 5
    
    return score


def faq_retrieve(message: str, intent_filter: str = None) -> dict:
    """检索最匹配的FAQ"""
    faq_data = load_json(FAQ_FILE)
    intent_rules = load_json(INTENT_FILE)
    
    # 1. 先检测意图
    intent_result = detect_intent(message, intent_rules)
    
    # 2. 如果有intent_filter，按filter过滤
    candidates = faq_data["faq_data"]
    if intent_filter:
        candidates = [f for f in candidates if intent_filter in f.get("intent", [])]
    
    # 3. 计算每个FAQ的匹配分数
    scored = [
        {"faq": f, "score": calculate_score(message, f)}
        for f in candidates
    ]
    
    # 4. 按分数排序，取最高分
    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0] if scored else None
    
    if not best or best["score"] == 0:
        return {
            "matched": False,
            "intent": intent_result,
            "faq": None,
            "suggested_response": faq_data["quick_reply_templates"].get("unknown", "抱歉，我没能理解您的问题。")
        }
    
    return {
        "matched": True,
        "intent": intent_result,
        "faq": {
            "id": best["faq"]["id"],
            "category": best["faq"]["category"],
            "answer": best["faq"]["answer"],
            "response_type": best["faq"]["response_type"],
            "follow_up": best["faq"].get("follow_up"),
            "leads_trigger": best["faq"].get("leads_trigger", False),
            "fault_related": best["faq"].get("fault_related", False)
        },
        "confidence": best["score"]
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 faq_retrieve.py \"客户消息文本\"")
        sys.exit(1)
    
    message = sys.argv[1]
    result = faq_retrieve(message)
    print(json.dumps(result, ensure_ascii=False, indent=2))
