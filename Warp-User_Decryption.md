# Warp dev.warp.Warp-User 文件解密

## 概述

本文档专门记录了Warp应用程序中`dev.warp.Warp-User`文件的DPAPI解密过程和完整数据结构。

## 文件信息

- **文件路径**: `%LOCALAPPDATA%\warp\Warp\data\dev.warp.Warp-User`
- **加密方式**: Windows DPAPI
- **文件大小**: 1694 字节（加密状态）
- **解密后长度**: 1465 字符

## 解密实现

### 核心解密函数

```python
def decrypt_warp_user_file(file_path):
    """解密Warp用户文件（使用Windows DPAPI）"""
    try:
        import win32crypt
        
        if not os.path.exists(file_path):
            return None
            
        # 读取加密的二进制数据
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        # 使用Windows DPAPI解密
        decrypted_data = win32crypt.CryptUnprotectData(
            encrypted_data, 
            None, None, None, 0
        )[1]
        
        # 转换为字符串
        return decrypted_data.decode('utf-8')
        
    except Exception as e:
        print(f"解密失败: {e}")
        return None
```

## 完整解密结果

### 原始JSON数据结构

```json
{
    "id_token": {
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjUwMDZlMjc5MTVhMTcwYWIyNmIxZWUzYjgxZDExNjU0MmYxMjRmMjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vYXN0cmFsLWZpZWxkLTI5NDYyMSIsImF1ZCI6ImFzdHJhbC1maWVsZC0yOTQ2MjEiLCJhdXRoX3RpbWUiOjE3NTgzOTA2NTAsInVzZXJfaWQiOiJpM01VNkpDbnU4V0k0ZUZISHd5b09sYUtib1AyIiwic3ViIjoiaTNNVTZKQ251OFdJNGVGSEh3eW9PbGFLYm9QMiIsImlhdCI6MTc1ODM5MjExNCwiZXhwIjoxNzU4Mzk1NzE0LCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImN1c3RvbSJ9fQ.hFH8xxFDvPCCduCCaN0yuhHsdOIz17WKPZBMdrK7oVvqKT8yiPG6YbflZ5Pf_3Vd0M0oOzNsw-JLwNNyNAgOssoPpYHaKT77dlDL1ASyvOZ-QrEQV8eJrgfdHARNMzeYoCA7qV3wsjsVvsIWcA5KAL7t7WHy16hyadSUPzFw-CG7qJXj1zI2fMS9cKbKrkNVVWT9nyT9fNfmA2GSwrU6e0mSN6Ze7Bl2ULydpf9qeMaxVbTgVvbI7WdAbBc6XkV_cHt9gOkeL3NPitgQelJ6o0GcK3sSxUtTzb2aCD68S4CdGLeG45WbLDBO-JiR18OppyBI3Nw_AuPFWTd1voASAg",
        "refresh_token": "AMf-vBxo8P_nO4rzIJNaEKlvR69g9SrP1FXd9i6tdHHAl20v8U4v033VWIAL74tGVkOrigpFxmimt2QRqqDJioWC3xulH8IPW9sFLTCcfCZA4-CMFjj--i4g0pAHEhg_zu3kDsL9cYybGcPRCIFkrbnUkk2UUbY45i8CoxEDGY5DGo6cfT6K9D1Wn0relbguDdHQwA-bnKLM",
        "expiration_time": "2025-09-21T03:12:29.948382+08:00"
    },
    "refresh_token": "",
    "local_id": "i3MU6JCnu8WI4eFHHwyoOlaKboP2",
    "email": "",
    "display_name": null,
    "photo_url": null,
    "is_onboarded": false,
    "needs_sso_link": false,
    "anonymous_user_type": "NativeClientAnonymousUserFeatureGated",
    "linked_at": null,
    "personal_object_limits": {
        "env_var_limit": 1,
        "notebook_limit": 1,
        "workflow_limit": 2
    },
    "is_on_work_domain": false
}
```

## 字段说明

### 顶级字段（12个）

| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `id_token` | object | Firebase JWT认证信息 | 包含3个子字段的对象 |
| `refresh_token` | string | 外层刷新令牌（空） | `""` |
| `local_id` | string | Firebase用户UID | `"i3MU6JCnu8WI4eFHHwyoOlaKboP2"` |
| `email` | string | 用户邮箱（匿名为空） | `""` |
| `display_name` | null | 用户显示名称 | `null` |
| `photo_url` | null | 用户头像URL | `null` |
| `is_onboarded` | boolean | 是否完成引导流程 | `false` |
| `needs_sso_link` | boolean | 是否需要SSO链接 | `false` |
| `anonymous_user_type` | string | 匿名用户类型标识 | `"NativeClientAnonymousUserFeatureGated"` |
| `linked_at` | null | 账户链接时间 | `null` |
| `personal_object_limits` | object | 个人功能限制配额 | 包含3个限制字段的对象 |
| `is_on_work_domain` | boolean | 是否为企业域账户 | `false` |

### id_token 对象结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `id_token` | string | Firebase JWT ID令牌 |
| `refresh_token` | string | Firebase JWT刷新令牌 |
| `expiration_time` | string | 令牌过期时间（ISO 8601格式） |

### personal_object_limits 对象结构

| 字段名 | 类型 | 说明 | 值 |
|--------|------|------|-----|
| `env_var_limit` | integer | 环境变量限制 | `1` |
| `notebook_limit` | integer | 笔记本限制 | `1` |
| `workflow_limit` | integer | 工作流限制 | `2` |

## 用户账户分析

基于解密数据的账户信息：

- **账户类型**: 受限匿名用户 (`NativeClientAnonymousUserFeatureGated`)
- **用户标识**: `i3MU6JCnu8WI4eFHHwyoOlaKboP2`
- **认证状态**: 拥有完整JWT令牌（ID + Refresh）
- **激活状态**: 未完成引导流程
- **身份信息**: 匿名用户（无邮箱、显示名、头像）
- **功能限制**: 环境变量1个，笔记本1个，工作流2个

## 依赖要求

- **Python库**: `pywin32`
- **系统**: Windows（DPAPI专属）
- **权限**: 当前用户权限（数据只能由加密用户解密）

---

**文档版本**: v1.0  
**最后更新**: 2024-12-20  
**数据来源**: 实际解密的Warp用户文件