#!/usr/bin/env python3
"""
Satellite Tracker - Main Entry Point
Run this file to start the application
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

# 检测是否在 macOS 上运行
if sys.platform == 'darwin':
    # macOS: 隐藏终端窗口（使用 .command 文件时）
    # 但如果是直接运行 python，仍然会显示终端
    pass

from src.main import main

if __name__ == "__main__":
    main()
