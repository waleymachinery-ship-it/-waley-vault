# Z_Memory_Sync.json 归档脚本
# 伟力机械 AI 系统 - 每月1号自动执行
# 保留近14天，旧的归档到 archives/

$vaultRoot = "D:\桌面文件\伟力机械知识库"
$syncFile = "$vaultRoot\00_Workflow\memory\Z_Memory_Sync.json"
$archiveDir = "$vaultRoot\00_Workflow\memory\archives"

# 创建归档目录
if (-not (Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
}

# 计算14天前的日期
$cutoffDate = (Get-Date).AddDays(-7)
$archiveName = "Z_Memory_Sync_$(Get-Date -Format 'yyyyMM01').json"

# 读取当前文件，获取最后写入时间
$content = Get-Content $syncFile -Raw | ConvertFrom-Json
$lastWriteStr = $content.last_writer -replace '.*(\d{4}-\d{2}-\d{2}).*', '$1'

if ([DateTime]::TryParse($lastWriteStr, [ref]$lastWriteDate)) {
    if ($lastWriteDate -lt $cutoffDate) {
        # 复制到归档目录
        $archivePath = "$archiveDir\$archiveName"
        Copy-Item $syncFile $archivePath -Force
        Write-Host "归档成功: $archivePath"
    } else {
        Write-Host "文件未超过14天，无需归档"
    }
} else {
    Write-Host "无法解析最后写入时间，跳过归档"
}

Write-Host "归档检查完成 - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
