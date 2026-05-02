#!/bin/bash
# 共享记忆同步 + 触发贾维斯心跳
# 每分钟运行，确保贾维斯定期检查共享记忆

SYNC_FILE="D:/桌面文件/伟力机械知识库/00_Workflow/memory/Z_Memory_Sync.json"
STATE_FILE="C:/Users/pc/AppData/Local/memory_sync_state.txt"
APP_ID="cli_a94d25b3dc381cef"
APP_SECRET="Q32oVLPPHKxUReDasWEofdCCH3h8Ngvl"
JARVIS_OPEN_ID="ou_f13ff9fc7445a35d7d12c9c257d47e77"  # 克劳德自己的ID，用来触发处理

# 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "[$(date)] 获取 token 失败"
    exit 1
fi

# 检查共享记忆版本变化
if [ -f "$SYNC_FILE" ]; then
    CURRENT_VERSION=$(grep -o '"version":[0-9]*' "$SYNC_FILE" | head -1 | cut -d':' -f2)
    LAST_VERSION=0
    if [ -f "$STATE_FILE" ]; then
        LAST_VERSION=$(cat "$STATE_FILE")
    fi

    if [ "$CURRENT_VERSION" != "$LAST_VERSION" ]; then
        echo "[$(date)] 检测到共享记忆更新: v$LAST_VERSION -> v$CURRENT_VERSION"
        echo "$CURRENT_VERSION" > "$STATE_FILE"
    fi
fi

# 发送一条轻量消息给自己（克劳德），触发 OpenClaw 处理心跳检查
# 这会让贾维斯也检查共享记忆
RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"receive_id\":\"$JARVIS_OPEN_ID\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"[系统心跳]共享记忆检查触发\\\"}\"}")

echo "[$(date)] 心跳触发完成"
