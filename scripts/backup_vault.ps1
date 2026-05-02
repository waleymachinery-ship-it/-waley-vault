$SOURCE = 'D:\桌面文件\伟力机械知识库'
$DEST = 'D:\Backup\WeiliKnowledgeBase'
$TSTAMP = Get-Date -Format 'yyyyMMdd_HHmmss'
$TSTAMPED = "D:\Backup\WeiliKnowledgeBase_$TSTAMP"

Write-Host 'Vault Backup Script'
Write-Host "Source: $SOURCE"

if (-not (Test-Path 'D:\Backup')) { New-Item -ItemType Directory -Path 'D:\Backup' -Force }

robocopy "$SOURCE" "$DEST" /MIR /R:3 /W:5 /NP /NDL
robocopy "$SOURCE" "$TSTAMPED" /MIR /R:3 /W:5 /NP /NDL

Get-ChildItem 'D:\Backup\WeiliKnowledgeBase_*' -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 5 |
    Remove-Item -Recurse -Force

Write-Host 'Backup completed'
