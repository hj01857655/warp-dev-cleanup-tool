#!/usr/bin/env python3
"""
将Warp终端恢复到全新安装、用户未登录、无任何个人数据的干净状态 (macOS版本)
注意：不包含备份功能，清理后数据无法恢复，清理后可重复申请账号使用，达到无限白嫖的目的。
"""

import os
import sys
import sqlite3
import shutil
import subprocess
import time
import random
import string
import uuid
import plistlib
from pathlib import Path
from datetime import datetime


class WarpCleaner:
    def __init__(self):
        self.warp_data_dir = Path(os.path.expanduser("~")) / "Library" / "Application Support" / "dev.warp.Warp-Stable"
        self.cleaned_items = []
        self.errors = []
        # macOS 上 Warp 的配置通过 plist 文件和数据目录管理，无需注册表


    def get_all_warp_processes(self):
        """获取所有可能的Warp相关进程 (macOS版本)"""
        warp_keywords = ['/Applications/Warp.app', 'Warp.app', 'WarpTerminal']
        running_processes = []

        try:
            # 使用 ps 命令获取进程信息
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
            for line in lines:
                if line.strip():
                    # ps aux 的格式: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
                    parts = line.split(None, 10)  # 限制分割为11部分，最后一部分是完整的命令
                    if len(parts) >= 11:
                        command = parts[10]  # 命令部分
                        
                        # 排除当前脚本自身
                        if 'cleanwarp.py' in command:
                            continue
                            
                        # 检查命令是否包含warp关键词
                        for keyword in warp_keywords:
                            if keyword.lower() in command.lower():
                                # 提取进程名（通常是路径的最后一部分）
                                process_name = command.split()[0].split('/')[-1]
                                if process_name not in running_processes:
                                    running_processes.append(process_name)
                                break

            return running_processes

        except Exception as e:
            self.log(f"获取详细进程信息失败: {e}", "WARNING")
            return []
        
    def log(self, message, level="INFO"):
        """记录日志信息"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def check_warp_running(self):
        """检查Warp相关进程是否正在运行 (macOS版本)"""
        # macOS 上 Warp 的可能进程名
        warp_processes = ['Warp']
        running_processes = []

        try:
            # 方法1: 使用 pgrep 基础检测，排除当前脚本
            for process_name in warp_processes:
                try:
                    result = subprocess.run(['pgrep', '-f', f'/Applications/{process_name}.app'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        running_processes.append(process_name)
                except Exception:
                    pass

            # 方法2: 使用详细进程检测
            detailed_processes = self.get_all_warp_processes()
            for proc in detailed_processes:
                if proc not in running_processes:
                    running_processes.append(proc)

            if running_processes:
                self.log(f"检测到运行中的Warp相关进程: {', '.join(running_processes)}")
                return running_processes
            return []

        except Exception as e:
            self.log(f"检查进程时出错: {e}", "WARNING")
            return []
    
    def kill_warp_process(self):
        """强制关闭所有Warp相关进程 (macOS版本)"""
        warp_processes = ['Warp', 'warp']
        killed_processes = []

        for process_name in warp_processes:
            try:
                # 使用 pkill 来杀死进程
                result = subprocess.run(['pkill', '-f', process_name], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    killed_processes.append(process_name)
                    
                # 如果普通 kill 失败，尝试强制 kill
                subprocess.run(['pkill', '-9', '-f', process_name], 
                             capture_output=True, text=True)
                             
            except Exception as e:
                self.log(f"尝试关闭 {process_name} 时出错: {e}", "WARNING")

        if killed_processes:
            self.log(f"已强制关闭进程: {', '.join(killed_processes)}")
            time.sleep(3)  # 等待进程完全关闭
            return True
        else:
            # 再次检查是否还有进程运行
            remaining = self.check_warp_running()
            if remaining:
                self.log(f"仍有进程运行: {', '.join(remaining)}", "ERROR")
                return False
            return True
    

    def clean_preferences(self):
        """清理macOS偏好设置和配置文件"""
        success = True

        # 1. 清理macOS偏好设置plist文件
        success &= self.clean_plist_files()

        # 2. 清理其他配置文件
        success &= self.clean_config_files()

        return success

    def clean_plist_files(self):
        """清理Warp相关的plist偏好设置文件"""
        try:
            # macOS 上 Warp 的偏好设置文件路径
            plist_files = [
                "~/Library/Preferences/dev.warp.Warp-Stable.plist",
                "~/Library/Preferences/dev.warp.Warp.plist"
            ]

            deleted_plists = []
            for plist_file in plist_files:
                plist_path = Path(os.path.expanduser(plist_file))
                try:
                    if plist_path.exists():
                        plist_path.unlink()
                        deleted_plists.append(plist_path.name)
                        self.log(f"已删除偏好设置文件: {plist_path.name}")
                except Exception as e:
                    self.log(f"删除 {plist_path.name} 失败: {e}", "WARNING")

            if deleted_plists:
                self.cleaned_items.extend([f"偏好设置文件: {f}" for f in deleted_plists])
            else:
                self.log("未找到Warp偏好设置文件")

            # 刷新 macOS 偏好设置缓存
            try:
                subprocess.run(['killall', 'cfprefsd'], capture_output=True)
                self.log("已刷新偏好设置缓存")
            except Exception as e:
                self.log(f"刷新偏好设置缓存失败: {e}", "WARNING")

            return True

        except Exception as e:
            self.log(f"清理偏好设置失败: {e}", "ERROR")
            self.errors.append(f"偏好设置清理: {e}")
            return False

    def clean_config_files(self):
        """清理其他配置文件"""
        try:
            # 清理可能的其他配置目录
            config_dirs = [
                "~/Library/Caches/dev.warp.Warp-Stable",
                "~/Library/WebKit/dev.warp.Warp-Stable",
                "~/Library/Saved Application State/dev.warp.Warp-Stable.savedState"
            ]

            deleted_configs = []
            for config_dir in config_dirs:
                config_path = Path(os.path.expanduser(config_dir))
                try:
                    if config_path.exists():
                        if config_path.is_file():
                            config_path.unlink()
                        elif config_path.is_dir():
                            shutil.rmtree(config_path)
                        deleted_configs.append(config_path.name)
                        self.log(f"已删除配置: {config_path.name}")
                except Exception as e:
                    self.log(f"删除 {config_path.name} 失败: {e}", "WARNING")

            if deleted_configs:
                self.cleaned_items.extend([f"配置文件/目录: {f}" for f in deleted_configs])

            return True

        except Exception as e:
            self.log(f"清理配置文件失败: {e}", "ERROR")
            self.errors.append(f"配置文件清理: {e}")
            return False
    
    def clean_database(self):
        """清理数据库，保留架构但删除用户数据"""
        db_path = self.warp_data_dir / "warp.sqlite"
        if not db_path.exists():
            self.log("数据库文件不存在")
            return True
            
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 需要清理的用户数据表
            user_tables = [
                'users', 'user_profiles', 'current_user_information',
                'windows', 'tabs', 'terminal_panes', 'pane_nodes', 'pane_leaves',
                'blocks', 'commands', 'ai_queries', 'ai_blocks', 
                'agent_conversations', 'agent_tasks', 'projects',
                'notebooks', 'workflows', 'teams', 'workspaces',
                'object_metadata', 'object_permissions', 'folders',
                'server_experiments', 'active_mcp_servers', 'mcp_environment_variables'
            ]
            
            cleaned_tables = []
            for table in user_tables:
                try:
                    cursor.execute(f"DELETE FROM {table}")
                    rows_deleted = cursor.rowcount
                    if rows_deleted > 0:
                        cleaned_tables.append(f"{table}({rows_deleted}行)")
                except sqlite3.OperationalError:
                    # 表不存在，跳过
                    pass
            
            # 重置app表的active_window_id
            cursor.execute("UPDATE app SET active_window_id = NULL WHERE id = 1")
            
            conn.commit()
            conn.close()
            
            if cleaned_tables:
                self.log(f"已清理数据库表: {', '.join(cleaned_tables)}")
                self.cleaned_items.append("数据库用户数据")
            else:
                self.log("数据库中无用户数据需要清理")
            
            return True
            
        except Exception as e:
            self.log(f"清理数据库失败: {e}", "ERROR")
            self.errors.append(f"数据库清理: {e}")
            return False
    
    def clean_files_and_directories(self):
        """清理文件和目录 (macOS版本)"""
        if not self.warp_data_dir.exists():
            self.log("Warp数据目录不存在")
            return True
            
        # 需要删除的文件和目录 (基于实际的macOS目录结构)
        items_to_delete = [
            # SQLite临时文件
            "warp.sqlite-shm",
            "warp.sqlite-wal", 
            # 缓存和临时文件
            "autoupdate",
            # 代码库索引快照
            "codebase_index_snapshots",
            # MCP 相关目录
            "mcp"
        ]
        
        # 需要清空的文件
        files_to_clear = [
            "warp_network.log",
            "rudder_telemetry_events.json"
        ]
        
        # 需要重新生成的随机文件（删除让系统重新生成）
        random_files_to_delete = []
        for file_path in self.warp_data_dir.iterdir():
            if file_path.is_file() and len(file_path.name) == 16 and file_path.name.isalnum():
                # 删除类似 "4897515f2ff5aca7" 这样的随机文件
                random_files_to_delete.append(file_path.name)
        
        deleted_items = []
        cleared_items = []
        
        # 删除文件和目录
        for item in items_to_delete:
            item_path = self.warp_data_dir / item
            try:
                if item_path.exists():
                    if item_path.is_file():
                        item_path.unlink()
                        deleted_items.append(item)
                    elif item_path.is_dir():
                        shutil.rmtree(item_path)
                        deleted_items.append(f"{item}/")
            except Exception as e:
                self.log(f"删除 {item} 失败: {e}", "WARNING")
                self.errors.append(f"删除{item}: {e}")
        
        # 删除随机文件
        for item in random_files_to_delete:
            item_path = self.warp_data_dir / item
            try:
                if item_path.exists():
                    item_path.unlink()
                    deleted_items.append(f"随机文件: {item}")
            except Exception as e:
                self.log(f"删除随机文件 {item} 失败: {e}", "WARNING")
        
        # 清空文件内容
        for item in files_to_clear:
            item_path = self.warp_data_dir / item
            try:
                if item_path.exists():
                    item_path.write_text("")
                    cleared_items.append(item)
            except Exception as e:
                self.log(f"清空 {item} 失败: {e}", "WARNING")
                self.errors.append(f"清空{item}: {e}")
        
        if deleted_items:
            self.log(f"已删除: {', '.join(deleted_items)}")
            self.cleaned_items.extend(deleted_items)
            
        if cleared_items:
            self.log(f"已清空: {', '.join(cleared_items)}")
            self.cleaned_items.extend([f"{item}(已清空)" for item in cleared_items])
        
        # 重新创建必要的空目录
        essential_dirs = [
            "codebase_index_snapshots"
        ]

        for dir_path in essential_dirs:
            full_path = self.warp_data_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)

        return True
    
    def verify_cleanup(self):
        """验证清理结果 (macOS版本)"""
        self.log("验证清理结果...")
        
        # 检查数据库
        db_path = self.warp_data_dir / "warp.sqlite"
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                
                # 检查关键用户表
                user_tables = ['users', 'current_user_information', 'windows', 'tabs']
                for table in user_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count > 0:
                            self.log(f"警告: {table}表仍有{count}条记录", "WARNING")
                    except sqlite3.OperationalError:
                        pass
                
                conn.close()
            except Exception as e:
                self.log(f"验证数据库时出错: {e}", "WARNING")
        
        # 检查关键文件是否已删除
        sensitive_files = [
            "rudder_telemetry_events.json",
            "mcp",
            "autoupdate"
        ]

        for file_path in sensitive_files:
            full_path = self.warp_data_dir / file_path
            if full_path.exists():
                self.log(f"警告: {file_path} 仍然存在", "WARNING")

        # 检查偏好设置文件
        plist_files = [
            "~/Library/Preferences/dev.warp.Warp-Stable.plist",
            "~/Library/Preferences/dev.warp.Warp.plist"
        ]
        
        for plist_file in plist_files:
            plist_path = Path(os.path.expanduser(plist_file))
            if plist_path.exists():
                self.log(f"警告: 偏好设置文件 {plist_path.name} 仍然存在", "WARNING")

        self.log("[OK] 已清理用户数据，Warp将自动生成新的配置和遥测数据")
        self.log("清理验证完成")
    
    def run(self, force=False):
        """执行完整的清理流程"""
        self.log("开始Warp终端清理流程")
        self.log(f"目标目录: {self.warp_data_dir}")
        
        if not force:
            response = input("确认要清理所有Warp用户数据吗？这将删除登录状态和个人配置 (y/N): ")
            if response.lower() != 'y':
                self.log("用户取消操作")
                return False
        
        # 检查并关闭Warp进程
        running_processes = self.check_warp_running()
        if running_processes:
            self.log("检测到Warp相关进程正在运行，需要先关闭")
            if not force:
                response = input("是否自动关闭Warp进程？ (Y/n): ")
                if response.lower() == 'n':
                    self.log("请手动关闭Warp后重新运行脚本")
                    return False

            if not self.kill_warp_process():
                self.log("无法关闭Warp进程，请手动关闭后重试", "ERROR")
                return False
        else:
            self.log("未检测到Warp进程运行")
        
        # 执行清理
        success = True
        success &= self.clean_database()
        success &= self.clean_files_and_directories()
        success &= self.clean_preferences()  # 替换clean_registry为clean_preferences

        # 验证结果
        self.verify_cleanup()
        
        # 输出总结
        self.log("=" * 50)
        if self.cleaned_items:
            self.log("已清理的项目:")
            for item in self.cleaned_items:
                self.log(f"  [OK] {item}")

        if self.errors:
            self.log("清理过程中的错误:")
            for error in self.errors:
                self.log(f"  [ERROR] {error}")
        
        if success and not self.errors:
            self.log("清理完成！Warp已恢复到全新安装状态", "SUCCESS")
        else:
            self.log("清理完成，但存在一些问题，请检查上述错误", "WARNING")
        
        return success

def main():
    """主函数"""
    print("Warp Terminal 清理工具 (macOS版本)")
    print("=" * 50)
    
    cleaner = WarpCleaner()
    
    # 解析命令行参数
    force = "--force" in sys.argv
    
    try:
        success = cleaner.run(force=force)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"清理过程中发生未预期的错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
