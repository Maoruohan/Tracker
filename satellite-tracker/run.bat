@echo off
echo ========================================
echo   🛰️  Satellite Tracker
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装！
    echo 请访问 https://python.org 下载安装
    pause
    exit /b
)

echo ✅ Python 已安装
echo.

REM 检查依赖是否安装
echo 📦 检查依赖...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装依赖...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo.
echo 🚀 启动卫星跟踪器...
python run.py

pause
