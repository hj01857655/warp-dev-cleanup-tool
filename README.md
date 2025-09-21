# 🚀 Warp 一键清理工具

<div align="center">

![GitHub release](https://img.shields.io/github/v/release/hj01857655/warp-dev-cleanup-tool)
![GitHub downloads](https://img.shields.io/github/downloads/hj01857655/warp-dev-cleanup-tool/total)
![GitHub stars](https://img.shields.io/github/stars/hj01857655/warp-dev-cleanup-tool)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)

**一键彻底清理 Warp Terminal 的所有数据和配置文件**

[📥 立即下载](https://github.com/hj01857655/warp-dev-cleanup-tool/releases/latest) • [📖 使用文档](#-快速开始) • [💬 加入社区](#-联系方式) • [🐛 问题反馈](https://github.com/hj01857655/warp-dev-cleanup-tool/issues)

</div>

---

> **作者**: hj01857655  
> **版本**: v2.0  
> **支持系统**: Windows

## ✨ 功能特性

- 🎯 **一键清理** - 彻底删除 Warp 所有数据和配置
- 🖥️ **图形界面** - 现代化GUI，操作简单直观
- 🔒 **DPAPI解密** - 支持Windows DPAPI解密，完整清理用户数据
- ⚡ **独立运行** - 无需安装Python或其他依赖
- 🛡️ **权限检测** - 智能检测并提示管理员权限
- 🔄 **重置机器码** - 支持单独重置ExperimentId
- 📊 **清理报告** - 详细显示清理进度和结果

## 📥 快速使用

### 源码运行（推荐）
```bash
# 安装依赖
pip install PyQt5 pywin32

# 运行GUI版本
python warp_cleanup_windows.py
```

## ⚙️ 使用说明

1. **安装依赖**: `pip install PyQt5 pywin32`
2. **运行程序**: `python warp_cleanup_windows.py`
3. **建议以管理员身份运行**获得完整功能

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
- **💬 QQ群**: [WARP Tools Community](https://qm.qq.com/q/ryYTgE8FBC)
- **📢 Telegram频道**: https://t.me/warp5215
- **💬 Telegram聊天**: https://t.me/warp1215

## ⚠️ 重要提示

- 此工具将**完全删除** Warp 的所有数据
- 清理前请**备份重要配置**
- 操作**不可撤销**，请谨慎使用
- Windows用户建议以**管理员身份**运行

---

**🎉 感谢使用！欢迎加入社区交流和反馈问题！**