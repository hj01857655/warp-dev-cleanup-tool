@echo off
chcp 65001 >nul
title Start Warp Cleanup Tool

echo.
echo ===============================================
echo         Warp Cleanup Tool - GUI Version
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    echo.
    echo Please install Python or run install_dependencies.bat
    pause
    exit /b 1
)

:: Check if PyQt5 is installed
python -c "import PyQt5.QtWidgets" >nul 2>&1
if errorlevel 1 (
    echo Error: PyQt5 not found
    echo.
    echo Please run install_dependencies.bat first
    pause
    exit /b 1
)

:: Check if main program exists
if not exist "warp_cleanup_tool.py" (
    echo Error: warp_cleanup_tool.py not found
    echo.
    echo Please ensure the file is in the same directory
    pause
    exit /b 1
)

echo Starting GUI cleanup tool...
echo.
echo Tips:
echo - Run as administrator for best results
echo - Backup important data before cleanup
echo.

:: Start GUI program
python warp_cleanup_tool.py

echo.
echo Program exited.
pause