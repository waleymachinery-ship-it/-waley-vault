@echo off
REM 伟力机械 AI 系统启动脚本
REM 启动：Hermes Gateway

echo [伟力机械 AI 系统] 启动中...

REM 启动 Hermes Gateway (NousResearch Hermes Agent)
echo 启动 Hermes Gateway...
cd C:\Users\pc\.hermes\hermes-agent
start /B cmd /c "uv run hermes gateway run"

echo [伟力机械 AI 系统] 启动完成！
pause
