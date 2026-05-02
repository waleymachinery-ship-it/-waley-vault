@echo off
chcp 65001 >nul
echo ========================================
echo      Vault Backup Script
echo ========================================
echo.
echo Backup started

robocopy "D:\桌面文件\伟力机械知识库" "D:\Backup\WeiliKnowledgeBase" /MIR /R:3 /W:5 /NP /NDL

for /f "tokens=2 delims==." %%a in ('wmic os get localdatetime /value') do set DT=%%a
set TSTAMP=%DT:~0,8%_%DT:~8,6%
robocopy "D:\桌面文件\伟力机械知识库" "D:\Backup\WeiliKnowledgeBase_%TSTAMP%" /MIR /R:3 /W:5 /NP /NDL

echo.
echo Cleaning old backups...
for /f "skip=5 delims=" %%i in ('dir /b /ad /o-d "D:\Backup\WeiliKnowledgeBase_*" 2^>nul') do rmdir /s /q "D:\Backup\%%i"

echo.
echo Backup completed
pause
