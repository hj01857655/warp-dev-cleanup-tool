@echo off
chcp 65001 >nul
title Warp 一键清理工具 - 打包程序

echo.
echo ===============================================
echo          Warp 一键清理工具 - 打包程序
echo ===============================================
echo.

:: 检查环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python
    echo 请先安装 Python 3.6+ 
    pause & exit /b 1
)

if not exist "warp_cleanup_tool.py" (
    echo ❤️ 错误：找不到 warp_cleanup_tool.py 文件
    pause & exit /b 1
)

:: 安装 PyInstaller（如果需要）
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 安装失败
        pause & exit /b 1
    )
)

echo 请选择打包方式：
echo.
echo 1. 快速打包 (推荐) - 生成单个exe文件
echo 2. 调试版本 - 带控制台窗口，便于调试
echo 3. 目录版本 - 生成包含依赖的文件夹
echo 4. 清理构建缓存
echo 5. 退出
echo.

set /p choice="请输入选择 (1-5): "

if "%choice%"=="4" goto :cleanup
if "%choice%"=="5" exit /b 0

:: 清理旧文件
if exist "dist" rmdir /s /q dist >nul 2>&1
if exist "build" rmdir /s /q build >nul 2>&1
if exist "*.spec" del *.spec >nul 2>&1

echo.
echo 开始打包...

if "%choice%"=="1" (
    echo 使用快速打包模式...
    python -m PyInstaller ^
        --onefile ^
        --windowed ^
        --name "Warp一键清理工具" ^
        --clean ^
        --noconfirm ^
        --optimize=2 ^
        warp_cleanup_tool.py
) else if "%choice%"=="2" (
    echo 使用调试模式打包...
    python -m PyInstaller ^
        --onefile ^
        --console ^
        --name "Warp一键清理工具_调试版" ^
        --clean ^
        --noconfirm ^
        warp_cleanup_tool.py
) else if "%choice%"=="3" (
    echo 使用目录模式打包...
    python -m PyInstaller ^
        --onedir ^
        --windowed ^
        --name "Warp一键清理工具_目录版" ^
        --clean ^
        --noconfirm ^
        --optimize=2 ^
        warp_cleanup_tool.py
) else (
    echo 无效选择，使用默认快速打包...
    python -m PyInstaller ^
        --onefile ^
        --windowed ^
        --name "Warp一键清理工具" ^
        --clean ^
        --noconfirm ^
        warp_cleanup_tool.py
)

goto :check_result

:cleanup
echo 清理构建缓存...
if exist "dist" (
    rmdir /s /q dist
    echo ✓ 已删除 dist 目录
)
if exist "build" (
    rmdir /s /q build  
    echo ✓ 已删除 build 目录
)
if exist "*.spec" (
    del *.spec
    echo ✓ 已删除 spec 文件
)
echo.
echo 清理完成！
goto :end

:check_result
echo.
if exist "dist\*.exe" (
    echo ===============================================
    echo ✓ 打包成功！
    echo ===============================================
    echo.
    echo 生成的文件：
    for %%f in (dist\*.exe) do (
        echo   📁 %%f
        echo   📏 大小: %%~zf 字节 (%.1fMB)
    )
    echo.
    echo 使用说明：
    echo • 双击exe文件运行
    echo • 建议右键选择"以管理员身份运行"
    echo • 该文件可以在其他电脑运行，无需安装Python
    echo.
    
    set /p open_folder="是否打开输出目录？(y/n): "
    if /i "%open_folder%"=="y" explorer dist
    
    set /p test_run="是否立即测试运行？(y/n): "
    if /i "%test_run%"=="y" (
        echo 启动程序进行测试...
        for %%f in (dist\*.exe) do start "" "%%f"
    )
) else (
    echo ❌ 打包失败！
    echo.
    echo 可能的原因：
    echo • 缺少必要依赖
    echo • 权限不足
    echo • 磁盘空间不足
    echo • 防病毒软件拦截
    echo.
    echo 请检查上述错误信息。
)

:end
echo.
pause