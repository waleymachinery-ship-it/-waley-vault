@echo off
chcp 65001 >nul
echo ===== hermes-agent Windows 安装脚本 (分批版) =====
echo.

set HERMES_VENV=C:\hermes-venv
set UV=C:\Users\pc\.local\bin\uv.exe
set PYTHON=%HERMES_VENV%\Scripts\python.exe
set MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple/

REM 验证 uv 是否存在
if not exist "%UV%" (
    echo [错误] uv 未找到：C:\Users\pc\.local\bin\uv.exe
    echo 请先安装 uv：powershell -Command "& C:\Users\pc\uv-install.ps1"
    pause
    exit /b 1
)

REM 验证 python 是否可用
"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 虚拟环境无效，请重新创建：
    echo %UV% venv %HERMES_VENV% --python 3.11.15
    pause
    exit /b 1
)

echo [步骤0] 虚拟环境检查完成
echo Python: %PYTHON%
echo.

REM ============================================================
REM 第一批：核心基础包（8个，体积小，快速安装）
REM ============================================================
echo ===== 第一批安装：核心基础包 =====
echo 包含：openai anthropic python-dotenv fire httpx rich tenacity pyyaml requests
echo.

"%UV%" pip install openai anthropic python-dotenv fire httpx rich tenacity pyyaml requests ^
    -i "%MIRROR%" ^
    --python "%PYTHON%" ^
    --break-system-packages

if errorlevel 1 (
    echo [错误] 第一批安装失败
    pause
    exit /b 1
)

echo.
echo [验证] 第一批包检查...
"%PYTHON%" -c "import openai; import anthropic; import fire; import httpx; import rich; print('核心包 OK')"
echo.

REM ============================================================
REM 第二批：Jinja2 + Pydantic + prompt_toolkit
REM ============================================================
echo ===== 第二批安装：模板和交互式CLI依赖 =====
echo 包含：jinja2 pydantic pydantic-core prompt-toolkit
echo.

"%UV%" pip install jinja2 "pydantic>=2.12.5,<3" "prompt_toolkit>=3.0.52,<4" ^
    -i "%MIRROR%" ^
    --python "%PYTHON%" ^
    --break-system-packages

if errorlevel 1 (
    echo [错误] 第二批安装失败
    pause
    exit /b 1
)

echo.
echo [验证] 第二批包检查...
"%PYTHON%" -c "import jinja2; import pydantic; import prompt_toolkit; print('模板/交互包 OK')"
echo.

REM ============================================================
REM 第三批：工具类包（不需要浏览器的工具集）
REM ============================================================
echo ===== 第三批安装：工具类包 =====
echo 包含：exa-py firecrawl-py parallel-web edge-tts PyJWT
echo.

"%UV%" pip install exa-py firecrawl-py parallel-web edge-tts "PyJWT[crypto]" ^
    -i "%MIRROR%" ^
    --python "%PYTHON%" ^
    --break-system-packages

if errorlevel 1 (
    echo [错误] 第三批安装失败
    pause
    exit /b 1
)

echo.
echo [验证] 第三批包检查...
"%PYTHON%" -c "import exa; import edge_tts; import jwt; print('工具包 OK')"
echo.

REM ============================================================
REM 第四批：hermes-agent 本地包
REM ============================================================
echo ===== 第四批安装：hermes-agent 源码包 =====
echo 包含：hermes-agent 本地安装
echo.

"%UV%" pip install C:\Users\pc\hermes-agent ^
    -i "%MIRROR%" ^
    --python "%PYTHON%" ^
    --no-deps ^
    --break-system-packages

if errorlevel 1 (
    echo [警告] 第四批安装失败，尝试不安装依赖直接安装...
    "%UV%" pip install C:\Users\pc\hermes-agent ^
        -i "%MIRROR%" ^
        --python "%PYTHON%" ^
        --break-system-packages
)

echo.
echo ===== 全部批次安装完成 =====
echo.
echo 下一步验证 hermes-agent 是否能启动：
echo %PYTHON% -m hermes_cli --version
echo.
pause
