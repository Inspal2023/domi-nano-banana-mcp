#!/bin/sh
# 多米nano-banana图像生成MCP服务器启动脚本
# STDIO模式启动脚本 - 适用于本地工具集成

set -e

# 切换到脚本目录
cd "$(dirname "$0")"

# 检查必要的环境变量
if [[ -z "$DOMI_API_TOKEN" ]]; then
    echo "Warning: DOMI_API_TOKEN environment variable not set" >&2
    echo "Please set DOMI_API_TOKEN before starting the server" >&2
    echo "You can also pass api_token parameter to individual tools" >&2
fi

# 创建独立的虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..." >&2
    uv venv
    echo "Installing dependencies..." >&2
    echo "Note: Dependency installation may take several minutes. Please wait..." >&2
    uv sync
fi

# 启动STDIO模式MCP服务器
echo "Starting多米nano-banana图像生成MCP服务器..." >&2
uv run server.py