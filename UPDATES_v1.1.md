# Warp 清理工具 v1.1 更新说明

## 🆕 新增功能

### 1. 动态用户SID检测
- ✅ 自动获取当前用户的SID，不再使用硬编码
- ✅ 支持不同Windows用户环境
- ✅ 更好的跨用户兼容性

### 2. 机器码重置功能 🔑
- ✅ 重置Warp的ExperimentId（机器码）
- ✅ 支持自动生成新的UUID格式机器码
- ✅ 支持用户自定义机器码
- ✅ 实时显示当前机器码状态
- ✅ UUID格式验证

### 3. Tab界面重构
- ✅ 清理工具Tab - 原有的清理功能
- ✅ 机器码Tab - 新的机器码管理功能  
- ✅ 信息Tab - 系统信息和开发者信息

### 4. 用户体验优化
- ✅ 更清晰的操作提示
- ✅ 智能路径检测和验证
- ✅ 更好的错误处理
- ✅ 实时状态反馈

## 🔧 技术改进

### 路径自动检测
```python
# 动态获取用户SID
def get_current_user_sid():
    # 使用wmic和whoami命令获取当前用户SID
    
# 动态构建路径
registry_path = f"HKEY_USERS\\{user_sid}\\Software\\Warp.dev\\Warp"
data_directory = os.path.join(home_dir, "AppData", "Local", "warp")
```

### 机器码管理
```python
# 重置ExperimentId
def reset_experiment_id(self, custom_id=None):
    # 生成新UUID或使用自定义ID
    # 写入注册表
    
# 获取当前机器码
def get_current_experiment_id(self):
    # 从注册表读取当前ExperimentId
```

## 📊 功能对比

| 功能 | v1.0 | v1.1 |
|------|------|------|
| 注册表清理 | ✅ | ✅ |
| 数据目录清理 | ✅ | ✅ |
| 硬编码路径 | ❌ | ✅ (已移除) |
| 动态SID检测 | ❌ | ✅ |
| 机器码重置 | ❌ | ✅ |
| Tab界面 | ❌ | ✅ |
| 自定义机器码 | ❌ | ✅ |
| 实时状态显示 | ❌ | ✅ |

## 🎯 使用场景

### 机器码重置适用于：
- 需要让Warp识别为新设备
- 重置设备标识
- 解决某些授权或配置问题
- 测试多设备场景

### 注意事项：
- ⚠️ 机器码重置会让Warp认为这是一个新设备
- ⚠️ 可能影响某些基于设备识别的功能
- ⚠️ 建议在重置前了解相关影响

## 📚 链接信息

- **GitHub仓库**: https://github.com/hj01857655/warp-dev-cleanup-tool
- **QQ群**: 1048579623 (WARP Tools Community)
- **Telegram频道**: https://t.me/warp5215  
- **Telegram聊天**: https://t.me/warp1215

## 👨‍💻 作者

hj01857655

---
感谢使用 Warp 清理工具！如有问题请加入社区交流。