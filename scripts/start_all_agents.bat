@echo off
chcp 65001 >nul
REM 伟力机械 AI 团队 - 一键启动所有AI服务

echo.
echo ========================================
echo     伟力机械 AI 团队 - 启动脚本
echo ========================================
echo.

REM 显示今日记忆
echo [1/2] 读取今日记忆...
powershell -NoProfile -ExecutionPolicy Bypass -File "D:/桌面文件/伟力机械知识库/scripts/read_today_memory.ps1"
echo.

REM 启动 OpenClaw Gateway
echo [2/2] 启动 OpenClaw Gateway...
start "OpenClaw-Gateway" powershell -NoExit -Command "openclaw gateway; Read-Host '按Enter退出'"
echo     OpenClaw Gateway 已在后台窗口启动
echo     Dashboard: http://127.0.0.1:18789/
echo.

echo ========================================
echo     启动完成！
echo     OpenClaw Gateway: ws://127.0.0.1:18789
echo ========================================
echo.
echo 提示：关闭窗口不会停止后台服务
echo      如需停止，请手动结束对应进程
pause
