@echo off
REM Jarvis 协作闭环检查脚本
REM 检查 memory 目录，发现 CLAUDE_CODE_DONE 标记则执行任务

echo Checking memory for tasks...
powershell -NoProfile -ExecutionPolicy Bypass -File "D:/桌面文件/伟力机械知识库/scripts/check_memory.ps1"
