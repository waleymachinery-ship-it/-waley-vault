#!/bin/bash
# hermes-agent Windows 安装脚本
# 用途：在 Windows (WSL 或 Git Bash) 环境下通过 uv 安装 hermes-agent 依赖
# 依赖：uv 已安装在 C:\Users\pc\.local\bin\uv.exe

set -e

HERMES_VENV="C:/Users/pc/hermes-venv"
UV="C:/Users/pc/.local/bin/uv.exe"
PYTHON="$HERMES_VENV/Scripts/python.exe"
MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple/"

echo "===== hermes-agent Windows 安装脚本 ====="
echo "venv: $HERMES_VENV"
echo "python: $PYTHON"
echo ""

# 检测 venv 是否存在
if [ ! -d "$HERMES_VENV" ]; then
    echo "[步骤0] 创建虚拟环境..."
    "$UV" venv "$HERMES_VENV" --python 3.11.15
else
    echo "[步骤0] 虚拟环境已存在，跳过"
fi

# 第一批：核心依赖（8个包，预期 1-3 分钟）
echo ""
echo "===== 第一批安装（核心包） ====="
"$UV" pip install openai anthropic python-dotenv fire httpx rich tenacity pyyaml requests \
    -i "$MIRROR" \
    --python "$PYTHON" \
    --break-system-packages

echo ""
echo "===== 第一批完成 ====="
echo "验证包是否安装成功..."
"$PYTHON" -c "import openai; import anthropic; import fire; import httpx; import rich; print('核心包 OK')"

echo ""
echo "===== 安装完成 ====="
echo "下一步：验证 hermes-agent 框架是否能启动"
