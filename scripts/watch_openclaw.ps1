# OpenClaw Gateway watchdog
# Check if port 18789 is listening, if not restart

$PORT = 18789
$CHECK_INTERVAL = 300  # 5 minutes

while ($true) {
    $listening = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue
    if ($listening.State -eq "Listen") {
        Write-Host (Get-Date -Format "yyyy-MM-dd HH:mm:ss") "- OpenClaw Gateway OK"
    } else {
        Write-Host (Get-Date -Format "yyyy-MM-dd HH:mm:ss") "- OpenClaw Gateway DOWN, restarting..."
        Start-Process -FilePath "openclaw" -ArgumentList "gateway --port $PORT" -WindowStyle Hidden
    }
    Start-Sleep -Seconds $CHECK_INTERVAL
}
