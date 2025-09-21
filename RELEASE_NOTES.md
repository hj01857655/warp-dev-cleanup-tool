# 🚀 Warp Cleanup Tool v1.0

A comprehensive cleanup tool for Warp Terminal that completely removes all Warp data from your system.

## 📦 Downloads

### Windows
- **[WarpCleanupTool-v1.0-windows-x64.exe](dist/WarpCleanupTool-v1.0-windows-x64.exe)** (37.1 MB)
  - Standalone executable, no installation required
  - Supports Windows 10/11 (64-bit)
  - Run as administrator for best results

### Source Code
- Python GUI version with cross-platform support
- Windows PowerShell script
- macOS shell script

## ✨ Features

- 🖥️ **Modern GUI Interface** - Easy-to-use graphical interface
- 🔐 **Safe Operation** - Confirmation dialogs and admin privilege detection
- 📊 **Real-time Progress** - Live progress bar and detailed logging
- 🎯 **Selective Cleaning** - Choose what to clean (registry/data)
- 🌍 **Cross-platform** - Windows, macOS support
- 🛡️ **Security** - No network access, completely offline

## 🧹 What Gets Cleaned

### Windows
- **Registry**: `HKEY_USERS\...\Software\Warp.dev\Warp`
- **Data Directory**: `%LOCALAPPDATA%\warp`

### macOS
- **Preferences**: `~/Library/Preferences/dev.warp.Warp*.plist`
- **Application Data**: `~/Library/Application Support/dev.warp.Warp*`
- **Cache & Logs**: `~/Library/Caches/dev.warp.Warp*` and more

## 🚨 Important Warnings

- ⚠️ **PERMANENT DELETION** - This tool completely removes ALL Warp data
- 💾 **BACKUP FIRST** - Save important configurations before running
- 🔒 **ADMIN REQUIRED** - Windows registry cleaning requires administrator privileges
- ❌ **NON-REVERSIBLE** - Operation cannot be undone

## 🏃‍♂️ Quick Start

### Windows (Recommended)
1. Download `WarpCleanupTool-v1.0-windows-x64.exe`
2. Right-click → "Run as administrator"
3. Follow the GUI prompts

### Source Code
1. Install Python 3.6+ and PyQt5: `pip install PyQt5`
2. Run: `python warp_cleanup_tool.py`

### macOS
1. Download and run: `./warp_cleanup_macos.sh`

## 📞 Support & Community

- **🔗 GitHub**: https://github.com/hj01857655/
- **💬 QQ Group**: 1048579623 (WARP Tools Community)
- **🔗 QQ Quick Join**: https://qm.qq.com/q/fxFiLHX1le
- **📢 Telegram Channel**: https://t.me/warp5215
- **💬 Telegram Chat**: https://t.me/warp1215

## 🔧 System Requirements

### Windows
- Windows 10/11 (64-bit)
- Administrator privileges (recommended)
- 50MB free disk space

### macOS
- macOS 10.12+
- Terminal access

## 📝 Changelog

### v1.0 (2025-09-20)
- ✅ Initial release
- ✅ GUI version with PyQt5
- ✅ Windows registry and data cleanup
- ✅ macOS comprehensive cleanup
- ✅ Cross-platform source code
- ✅ Standalone Windows executable
- ✅ Multi-language community support

---

**⭐ If this tool helped you, please star the repository and join our community!**