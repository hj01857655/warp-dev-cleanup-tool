# 🚀 Warp 一键清理工具

> **作者**: hj01857655  
> **版本**: v1.0  
> **支持系统**: Windows、macOS  

## 📦 文件说明

### 🎯 推荐使用（开箱即用）
- **`dist/WarpCleanupTool-v1.0-windows-x64.exe`** - 打包好的独立程序，双击即可运行

### 📝 源代码版本
- **`warp_cleanup_tool.py`** - GUI图形界面版本（需要Python + PyQt5）
- **`warp_cleanup_windows.py`** - Windows命令行版本
- **`warp_cleanup_windows.ps1`** - PowerShell版本
- **`warp_cleanup_macos.sh`** - macOS版本

### 🛠️ 辅助工具
- **`install_dependencies.bat`** - 自动安装依赖
- **`run_gui.bat`** - 快速启动GUI版本
- **`build.bat`** - 重新打包工具（多种选项）

## 🚀 快速开始

### Windows 用户（推荐）
1. 直接运行：`dist/WarpCleanupTool-v1.0-windows-x64.exe`
2. 建议右键选择"以管理员身份运行"

### 源码运行（需要Python环境）
1. 安装依赖：双击 `install_dependencies.bat`
2. 运行GUI：双击 `run_gui.bat`
3. 或命令行：`python warp_cleanup_tool.py`

### macOS 用户
1. 运行：`chmod +x warp_cleanup_macos.sh && ./warp_cleanup_macos.sh`

## 🧹 清理内容

### Windows
- **注册表**: `HKEY_USERS\...\Software\Warp.dev\Warp`
- **数据目录**: `C:\Users\用户名\AppData\Local\warp`

### macOS
- **偏好设置**: `~/Library/Preferences/dev.warp.Warp*.plist`
- **应用数据**: `~/Library/Application Support/dev.warp.Warp*`
- **缓存日志**: `~/Library/Caches/dev.warp.Warp*` 等

## 📞 联系方式

- **🔗 GitHub**: https://github.com/hj01857655/
- **💬 QQ群**: 1048579623 (WARP Tools Community)
- **🔗 QQ群链接**: https://qm.qq.com/q/fxFiLHX1le
- **📢 Telegram频道**: https://t.me/warp5215
- **💬 Telegram聊天**: https://t.me/warp1215

## ⚠️ 重要提示

- 此工具将**完全删除** Warp 的所有数据
- 清理前请**备份重要配置**
- 操作**不可撤销**，请谨慎使用
- Windows用户建议以**管理员身份**运行

---

**🎉 感谢使用！欢迎加入社区交流和反馈问题！**