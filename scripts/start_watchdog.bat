@echo off
chcp 65001 >nul
REM OpenClaw Watchdog - 确保 Gateway 24/7 运行

echo.
echo ========================================
echo     OpenClaw Watchdog 守护进程
echo ========================================
echo.
echo 监控端口: 18789
echo 检查间隔: 5 分钟
echo.
echo 按 Ctrl+C 停止监控
echo ========================================
echo.

powershell -NoExit -ExecutionPolicy Bypass -File "D:/桌面文件/伟力机械知识库/scripts/watch_openclaw.ps1"
