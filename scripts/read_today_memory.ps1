# read_today_memory.ps1
# 每次启动时读取当天日记来获取记忆

$memoryPath = "D:\桌面文件\伟力机械知识库\memory"
$today = Get-Date -Format "yyyy-MM-dd"
$todayFile = Join-Path $memoryPath "$today.md"

if (Test-Path $todayFile) {
    Write-Host "========== 读取今日记忆: $today ==========" -ForegroundColor Cyan
    Get-Content $todayFile -Raw -Encoding UTF8
    Write-Host "`n==========================================" -ForegroundColor Cyan
} else {
    Write-Host "========== 今日 ($today) 尚无日记 ==========" -ForegroundColor Yellow
    Write-Host "提示：memory/$today.md 不存在，请开始今天的日志" -ForegroundColor Yellow
}

# 检查是否有 JARVIS_DONE 标记（待处理事项）
if (Test-Path $todayFile) {
    $content = Get-Content $todayFile -Raw -Encoding UTF8
    if ($content -match '<!-- JARVIS_DONE:') {
        Write-Host "`n>>> 发现 JARVIS_DONE 标记，杰维斯有待处理事项 <<<" -ForegroundColor Magenta
    }
}
