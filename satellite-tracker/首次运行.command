#!/bin/bash

echo "========================================"
echo "  🛰️  卫星跟踪器 - 首次运行设置"
echo "========================================"
echo ""

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "📁 当前目录: $DIR"
echo ""

# 给 .command 文件加权限
echo "🔧 正在修复权限..."
chmod +x 卫星跟踪器.command
xattr -d com.apple.quarantine 卫星跟踪器.command 2>/dev/null

echo ""
echo "✅ 修复完成！"
echo ""
echo "📌 现在双击「卫星跟踪器.command」即可运行"
echo ""

read -p "按回车键退出..."
