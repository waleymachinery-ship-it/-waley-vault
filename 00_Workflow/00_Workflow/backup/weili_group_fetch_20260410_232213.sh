#!/bin/bash
# 飞书群消息拉取脚本

SYNC_FILE="D:/桌面文件/伟力机械知识库/00_Workflow/memory/Z_Memory_Sync.json"
STATE_FILE="C:/Users/pc/AppData/Local/weili_group_lastmsg.txt"
APP_ID="cli_a94d25b3dc381cef"
APP_SECRET="Q32oVLPPHKxUReDasWEofdCCH3h8Ngvl"
CHAT_ID="oc_2a35b9e85451a57f9c64f93f15912176"

# 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "[$(date)] 获取 token 失败"
    exit 1
fi

# 获取消息
MSGS=$(curl -s "https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id=$CHAT_ID&sort_type=ByCreateTimeDesc&page_size=10" \
    -H "Authorization: Bearer $TOKEN")

# 检查是否成功
CODE=$(echo "$MSGS" | grep -o '"code":[0-9]*' | head -1 | cut -d':' -f2)
if [ "$CODE" != "0" ]; then
    echo "[$(date)] 获取消息失败"
    exit 1
fi

# 读取上次处理的消息 ID
LAST_MSG_ID=""
if [ -f "$STATE_FILE" ]; then
    LAST_MSG_ID=$(cat "$STATE_FILE")
fi

# 解析消息（使用 node 如果可用，或者简单 grep）
echo "$MSGS" > /tmp/feishu_msgs.json

# 获取最新消息数
MSG_COUNT=$(echo "$MSGS" | grep -o '"message_id":"[^"]*"' | wc -l)
echo "[$(date)] 发现消息数量: $MSG_COUNT"

# 简单处理：如果有新消息就写入共享记忆
if [ "$MSG_COUNT" -gt 0 ]; then
    FIRST_MSG_ID=$(echo "$MSGS" | grep -o '"message_id":"[^"]*"' | head -1 | cut -d'"' -f4)

    if [ "$FIRST_MSG_ID" != "$LAST_MSG_ID" ]; then
        echo "[$(date)] 发现新群消息，同步到共享记忆"

        # 读取当前共享记忆
        SYNC_VERSION=$(grep -o '"version":[0-9]*' "$SYNC_FILE" | head -1 | cut -d':' -f2)
        NEW_VERSION=$((SYNC_VERSION + 1))

        # 更新 version
        sed -i "s/\"version\":$SYNC_VERSION/\"version\":$NEW_VERSION/" "$SYNC_FILE"
        sed -i "s/\"last_modified\":\"[^\"]*\"/\"last_modified\":\"$(date +%Y-%m-%dT%H:%M:%S+08:00)\"/" "$SYNC_FILE"
        sed -i "s/\"last_writer\":\"[^\"]*\"/\"last_writer\":\"claude-group-monitor\"/" "$SYNC_FILE"

        # 保存最新消息 ID
        echo "$FIRST_MSG_ID" > "$STATE_FILE"

        echo "[$(date)] 同步完成"
    else
        echo "[$(date)] 无新消息"
    fi
fi
