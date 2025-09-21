#!/usr/bin/env python3
"""
Warp Cleanup Script for Windows
This script removes Warp registry entries and data directories
"""

import os
import shutil
import winreg
import sys
import uuid
from pathlib import Path


def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def delete_registry_key(key_path):
    """Delete a registry key and all its subkeys"""
    try:
        # Split the key path
        parts = key_path.split('\\', 1)
        if len(parts) != 2:
            print(f"Invalid registry path format: {key_path}")
            return False
            
        root_key_name = parts[0]
        subkey_path = parts[1]
        
        # Map root key name to winreg constant
        root_keys = {
            'HKEY_USERS': winreg.HKEY_USERS,
            'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
            'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        }
        
        if root_key_name not in root_keys:
            print(f"Unsupported root key: {root_key_name}")
            return False
            
        root_key = root_keys[root_key_name]
        
        # Try to delete the key recursively
        def delete_key_recursive(key, subkey):
            try:
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS) as handle:
                    # Get all subkeys
                    subkeys = []
                    i = 0
                    while True:
                        try:
                            subkeys.append(winreg.EnumKey(handle, i))
                            i += 1
                        except WindowsError:
                            break
                    
                    # Delete all subkeys first
                    for sk in subkeys:
                        delete_key_recursive(handle, sk)
                    
                # Delete the key itself
                winreg.DeleteKey(key, subkey)
                return True
            except FileNotFoundError:
                print(f"Registry key not found: {key_path}")
                return False
            except PermissionError:
                print(f"Permission denied accessing registry key: {key_path}")
                return False
            except Exception as e:
                print(f"Error deleting registry key {key_path}: {e}")
                return False
        
        success = delete_key_recursive(root_key, subkey_path)
        if success:
            print(f"✓ Successfully deleted registry key: {key_path}")
        return success
        
    except Exception as e:
        print(f"Error processing registry key {key_path}: {e}")
        return False


def delete_directory(dir_path):
    """Delete a directory and all its contents"""
    try:
        path = Path(dir_path)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"✓ Successfully deleted directory: {dir_path}")
                return True
            else:
                print(f"Path exists but is not a directory: {dir_path}")
                return False
        else:
            print(f"Directory not found: {dir_path}")
            return False
    except PermissionError:
        print(f"Permission denied deleting directory: {dir_path}")
        return False
    except Exception as e:
        print(f"Error deleting directory {dir_path}: {e}")
        return False


def reset_experiment_id(registry_key_path, new_id=None):
    """Reset or generate a new ExperimentId in the Warp registry"""
    try:
        # Split the key path
        parts = registry_key_path.split('\\', 1)
        if len(parts) != 2:
            print(f"Invalid registry path format: {registry_key_path}")
            return False
            
        root_key_name = parts[0]
        subkey_path = parts[1]
        
        # Map root key name to winreg constant
        root_keys = {
            'HKEY_USERS': winreg.HKEY_USERS,
            'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
            'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        }
        
        if root_key_name not in root_keys:
            print(f"Unsupported root key: {root_key_name}")
            return False
            
        root_key = root_keys[root_key_name]
        
        # Generate a new UUID if not provided
        if new_id is None:
            new_id = str(uuid.uuid4())
        
        try:
            # Try to open the registry key
            with winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_SET_VALUE) as key:
                # Set the new ExperimentId
                winreg.SetValueEx(key, "ExperimentId", 0, winreg.REG_SZ, new_id)
                print(f"✓ Successfully reset ExperimentId to: {new_id}")
                return True
                
        except FileNotFoundError:
            print(f"Registry key not found: {registry_key_path}")
            print("The Warp registry key doesn't exist, so no ExperimentId to reset.")
            return False
        except PermissionError:
            print(f"Permission denied accessing registry key: {registry_key_path}")
            print("Try running the script as Administrator.")
            return False
            
    except Exception as e:
        print(f"Error resetting ExperimentId: {e}")
        return False


def get_current_experiment_id(registry_key_path):
    """Get the current ExperimentId from the registry"""
    try:
        # Split the key path
        parts = registry_key_path.split('\\', 1)
        if len(parts) != 2:
            return None
            
        root_key_name = parts[0]
        subkey_path = parts[1]
        
        # Map root key name to winreg constant
        root_keys = {
            'HKEY_USERS': winreg.HKEY_USERS,
            'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
            'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        }
        
        if root_key_name not in root_keys:
            return None
            
        root_key = root_keys[root_key_name]
        
        try:
            # Try to open the registry key and read ExperimentId
            with winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, "ExperimentId")
                return value
                
        except FileNotFoundError:
            return None
        except Exception:
            return None
            
    except Exception:
        return None


def show_menu():
    """Display the main menu and get user choice"""
    print("\nWarp Cleanup Tool - Choose an option:")
    print("1. Complete cleanup (Remove all Warp data and registry entries)")
    print("2. Reset machine code only (Reset ExperimentId)")
    print("3. View current ExperimentId")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def complete_cleanup(registry_path, data_directory):
    """Perform complete Warp cleanup"""
    print("\nStarting complete Warp cleanup...")
    
    success_count = 0
    total_operations = 2
    
    # Clean registry
    print(f"\n1. Cleaning registry: {registry_path}")
    if delete_registry_key(registry_path):
        success_count += 1
    
    # Clean data directory
    print(f"\n2. Cleaning data directory: {data_directory}")
    if delete_directory(data_directory):
        success_count += 1
    
    # Summary
    print(f"\n" + "=" * 40)
    print(f"Cleanup completed: {success_count}/{total_operations} operations successful")
    
    if success_count == total_operations:
        print("🎉 Warp has been completely removed from your system!")
    elif success_count > 0:
        print("⚠️  Partial cleanup completed. Some operations failed.")
    else:
        print("❌ Cleanup failed. No changes were made.")


def reset_machine_code_only(registry_path):
    """Reset only the ExperimentId (machine code)"""
    print("\nResetting Warp machine code (ExperimentId)...")
    
    # Show current ExperimentId if exists
    current_id = get_current_experiment_id(registry_path)
    if current_id:
        print(f"Current ExperimentId: {current_id}")
    else:
        print("Current ExperimentId: Not found")
    
    # Ask if user wants to provide custom ID or generate new one
    print("\nChoose an option:")
    print("1. Generate a new random ExperimentId")
    print("2. Provide a custom ExperimentId")
    
    while True:
        sub_choice = input("Enter your choice (1 or 2): ").strip()
        if sub_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    if sub_choice == '1':
        # Generate new random ID
        if reset_experiment_id(registry_path):
            print("🎉 Machine code has been successfully reset!")
        else:
            print("❌ Failed to reset machine code.")
    else:
        # Use custom ID
        custom_id = input("Enter the new ExperimentId (or press Enter for random): ").strip()
        if not custom_id:
            custom_id = None
        
        if reset_experiment_id(registry_path, custom_id):
            print("🎉 Machine code has been successfully reset!")
        else:
            print("❌ Failed to reset machine code.")


def view_current_experiment_id(registry_path):
    """Display the current ExperimentId"""
    print("\nCurrent Warp ExperimentId:")
    current_id = get_current_experiment_id(registry_path)
    if current_id:
        print(f"🔑 ExperimentId: {current_id}")
        print(f"📁 Registry Path: {registry_path}")
    else:
        print("⚠️  ExperimentId not found in registry")
        print("This could mean:")
        print("  - Warp is not installed")
        print("  - The registry path is incorrect")
        print("  - You don't have permission to read the registry")


def main():
    print("Warp Cleanup Script for Windows")
    print("=" * 40)
    
    # Check if running as administrator
    if not is_admin():
        print("⚠️  Warning: This script is not running as Administrator.")
        print("   Some registry operations may fail.")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("Exiting...")
            sys.exit(1)
    
    # Registry path and data directory
    registry_path = "HKEY_USERS\\S-1-5-21-1975947051-2922622289-44519384-1002\\Software\\Warp.dev\\Warp"
    data_directory = "C:\\Users\\12925\\AppData\\Local\\warp"
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            complete_cleanup(registry_path, data_directory)
        elif choice == '2':
            reset_machine_code_only(registry_path)
        elif choice == '3':
            view_current_experiment_id(registry_path)
        elif choice == '4':
            print("Exiting...")
            break
        
        # Ask if user wants to continue
        print("\n" + "-" * 40)
        continue_choice = input("Would you like to perform another operation? (y/n): ").lower().strip()
        if continue_choice != 'y':
            break
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()