# Z_Memory_Sync 定时同步脚本
# 每 30 秒检查共享记忆，有更新时触发 Claude Code 心跳

$syncFile = "D:\桌面文件\伟力机械知识库\00_Workflow\memory\Z_Memory_Sync.json"
$lastVersion = 0
$lastModified = ""

while ($true) {
    try {
        if (Test-Path $syncFile) {
            $content = Get-Content $syncFile -Raw -Encoding UTF8
            $data = $content | ConvertFrom-Json

            $currentVersion = $data.version
            $currentModified = $data.last_modified

            if ($currentVersion -gt $lastVersion) {
                Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] 检测到记忆更新: version $lastVersion -> $currentVersion"
                $lastVersion = $currentVersion
                $lastModified = $currentModified
            }
        }
    }
    catch {
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] 读取共享记忆失败: $_"
    }

    Start-Sleep -Seconds 30
}
