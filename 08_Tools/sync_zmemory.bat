@echo off
chcp 65001 >nul
REM Hermes/Jarvis 写入 Z_Memory_Sync.json 的脚本
REM 用法: sync_zmemory.bat <agent> "<content>"
REM 示例: sync_zmemory.bat Hermes "<!-- HERMES_STARTUP: Hermes 已确认 -->"

set AGENT=%1
set CONTENT=%2

if "%AGENT%"=="" (
    echo Usage: sync_zmemory.bat ^<agent^> ^<content^>
    exit /b 1
)

if "%CONTENT%"=="" (
    echo Usage: sync_zmemory.bat ^<agent^> ^<content^>
    exit /b 1
)

python.exe "D:\桌面文件\伟力机械知识库\08_Tools\sync_zmemory.py" %AGENT% %CONTENT%
