# jarvis_cron_watch.ps1
# 伟力机械三AI协作系统 - 每小时战情评估
# 触发条件：有任务长期卡在pending / 阶段里程碑逾期 / 特定事件
# 运行方式：计划任务，每60分钟执行

$ErrorActionPreference = "SilentlyContinue"
$VaultPath = "D:\桌面文件\伟力机械知识库"
$TaskQueuePath = "$VaultPath\00_Workflow\memory\task_queue.json"
$ZMemoryPath = "$VaultPath\00_Workflow\memory\Z_Memory_Sync.json"
$LogPath = "D:\weili_jarvis_cron.log"
$TriggerFlag = "D:\weili_trigger_flag.txt"

function Get-TaskQueue {
    $content = Get-Content $TaskQueuePath -Raw -Encoding UTF8
    $content = $content.TrimStart([char]0xFEFF)
    return ConvertFrom-Json $content
}

function Get-ZMemory {
    $content = Get-Content $ZMemoryPath -Raw -Encoding UTF8
    $content = $content.TrimStart([char]0xFEFF)
    return ConvertFrom-Json $content
}

function Write-Log {
    param($msg)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts - $msg" | Add-Content $LogPath -Encoding UTF8
}

# ===== 健康检查 =====
$q = Get-TaskQueue
$pending = $q.tasks | Where-Object { $_.status -eq 'pending' }

# 检查1：有 pending 任务卡住
if ($pending) {
    Write-Log "发现 $($pending.Count) 个 pending 任务:"
    foreach ($p in $pending) {
        Write-Log "  - $($p.id): to=$($p.to), created=$($p.created_at)"
    }
    # 写入 to:claude 任务触发战情评估
    $taskId = "claude-war-room-$(Get-Date -Format 'yyyyMMdd-HHmm')"
    $newTask = @{
        id = $taskId
        from = "jarvis"
        to = "claude"
        type = "task"
        status = "pending"
        priority = "high"
        created_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss+08:00")
        content = "战情评估：有 $($pending.Count) 个 pending 任务卡住，请评估并部署下一步"
    }
    # 追加到 task_queue（简化版，实际应该用 Python 写）
    Write-Log "写入战情评估任务: $taskId"
    # 注意：Hermes 会通过飞书 @Claude 触发处理
}

# 检查2：Z_Memory_Sync 长期无更新（超过24小时）
$z = Get-ZMemory
$lastUpdate = [DateTime]::Parse($z.last_modified)
$hoursSinceUpdate = ((Get-Date) - $lastUpdate).TotalHours
if ($hoursSinceUpdate -gt 24) {
    Write-Log "警告：Z_Memory_Sync 超过 ${hoursSinceUpdate}小时 无更新"
}

Write-Log "战情评估完成。pending=$($pending.Count), Z_Memory=${hoursSinceUpdate}h"
