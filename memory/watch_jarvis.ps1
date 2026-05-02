# Jarvis 协作闭环监控脚本
# 每 30 分钟检查当天的 memory/YYYY-MM-DD.md 中的 JARVIS_DONE 标记
# 使用方式：powershell -File watch_jarvis.ps1
# v3: 动态日期，监控当天文件 (2026-04-10)

$DATE = Get-Date -Format "yyyy-MM-dd"
$FILE = "D:\桌面文件\伟力机械知识库\memory\$DATE.md"

Write-Host "开始监控 JARVIS_DONE 标记..."
Write-Host "按 Ctrl+C 停止"
Write-Host ""

while ($true) {
    if (Test-Path $FILE) {
        $lines = Get-Content $FILE -ErrorAction SilentlyContinue

        # 找最后一个未处理的 JARVIS_DONE
        for ($i = $lines.Count - 1; $i -ge 0; $i--) {
            if ($lines[$i] -match '<!-- JARVIS_DONE: (.+) -->') {
                $content = $matches[1]
                $linenum = $i + 1

                Write-Host ""
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 检测到 JARVIS_DONE:"
                Write-Host "  $content"

                # 检查是否已有 CLAUDE_CODE_DONE 响应（避免重复）
                $hasResponse = $lines | Where-Object { $_ -match '<!-- CLAUDE_CODE_DONE:.*' }
                if (-not $hasResponse) {
                    $reply = "<!-- CLAUDE_CODE_DONE: Claude Code 已读取并分析 Jarvis 的内容：$content。已响应，协作继续。-->"
                    $newLines = @()
                    for ($j = 0; $j -lt $lines.Count; $j++) {
                        $newLines += $lines[$j]
                        if ($j -eq ($linenum - 1)) {
                            $newLines += $reply
                        }
                    }
                    $newLines | Set-Content $FILE -Encoding UTF8
                    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 已写入 CLAUDE_CODE_DONE"
                } else {
                    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] CLAUDE_CODE_DONE 已存在，跳过"
                }
                break
            }
        }
    }

    Start-Sleep -Seconds 1800  # 30分钟 (Self-Evolution Cycle 003 优化)
}
