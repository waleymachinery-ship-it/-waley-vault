# Jarvis 协作闭环检查脚本
# 检查 memory 目录，发现 CLAUDE_CODE_DONE 标记则执行任务

$MemoryDir = "D:\桌面文件\伟力机械知识库\memory"
$VaultRoot = "D:\桌面文件\伟力机械知识库"

# 获取最新的 memory 文件
$LatestMemory = Get-ChildItem -Path $MemoryDir -Filter "*.md" |
    Where-Object { $_.Name -match "^\d{4}-\d{2}-\d{2}\.md$" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $LatestMemory) {
    Write-Host "No memory file found"
    exit 0
}

$Content = Get-Content $LatestMemory.FullName -Raw -Encoding UTF8

# 检查是否有未处理的 CLAUDE_CODE_DONE 标记
if ($Content -match "<!-- CLAUDE_CODE_DONE: (.+?) -->") {
    $Task = $Matches[1]
    Write-Host "Found task: $Task"

    # 检查是否已经有 JARVIS_DONE 标记
    if ($Content -match "<!-- JARVIS_DONE: $Task -->") {
        Write-Host "Task already processed"
        exit 0
    }

    # 追加 JARVIS_DONE 标记
    $DoneMarker = "`n`n<!-- JARVIS_DONE: $Task -->"
    Add-Content -Path $LatestMemory.FullName -Value $DoneMarker -Encoding UTF8
    Write-Host "JARVIS_DONE marked"
} else {
    Write-Host "No pending tasks found"
}
