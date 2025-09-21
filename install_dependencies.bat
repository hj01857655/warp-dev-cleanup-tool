@echo off
chcp 65001 >nul
title 安装 Warp 清理工具依赖

echo.
echo ===============================================
echo    Warp 清理工具 - 依赖安装脚本
echo ===============================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python
    echo.
    echo 请先安装 Python 3.6 或更高版本：
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ 检测到 Python：
python --version

echo.
echo 正在安装 PyQt5...
echo.

:: 首先尝试从默认源安装
echo 尝试方法 1：从默认源安装...
pip install PyQt5

:: 检查安装是否成功
python -c "import PyQt5; print('PyQt5 安装成功！')" 2>nul
if not errorlevel 1 (
    goto :success
)

echo.
echo 默认源安装失败，尝试从清华镜像源安装...
pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple/

:: 再次检查安装是否成功
python -c "import PyQt5; print('PyQt5 安装成功！')" 2>nul
if not errorlevel 1 (
    goto :success
)

echo.
echo 清华镜像源安装失败，尝试从豆瓣镜像源安装...
pip install PyQt5 -i https://pypi.douban.com/simple/

:: 最后检查安装是否成功
python -c "import PyQt5; print('PyQt5 安装成功！')" 2>nul
if not errorlevel 1 (
    goto :success
)

echo.
echo ❌ 所有安装尝试都失败了
echo.
echo 请尝试手动安装：
echo 1. 更新 pip：pip install --upgrade pip
echo 2. 安装 PyQt5：pip install PyQt5
echo 3. 或者使用 Anaconda：conda install pyqt
echo.
pause
exit /b 1

:success
echo.
echo ===============================================
echo ✓ 安装完成！
echo ===============================================
echo.
echo PyQt5 已成功安装。现在可以运行 GUI 版本的清理工具：
echo.
echo 运行方式：
echo   python warp_cleanup_gui.py
echo.
echo 或者双击 warp_cleanup_gui.py 文件
echo.
echo 建议以管理员身份运行以获得最佳效果。
echo.
pause