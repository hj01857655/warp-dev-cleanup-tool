#!/bin/bash

# Warp Cleanup Script for macOS
# This script removes Warp data directories and preferences

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Function to check if directory exists and remove it
remove_directory() {
    local dir_path="$1"
    local description="$2"
    
    if [ -d "$dir_path" ]; then
        print_color $YELLOW "Removing $description: $dir_path"
        rm -rf "$dir_path"
        print_color $GREEN "✓ Successfully deleted: $dir_path"
        return 0
    else
        print_color $YELLOW "Directory not found: $dir_path"
        return 1
    fi
}

# Function to check if file exists and remove it
remove_file() {
    local file_path="$1"
    local description="$2"
    
    if [ -f "$file_path" ]; then
        print_color $YELLOW "Removing $description: $file_path"
        rm -f "$file_path"
        print_color $GREEN "✓ Successfully deleted: $file_path"
        return 0
    else
        print_color $YELLOW "File not found: $file_path"
        return 1
    fi
}

# Main function
main() {
    print_color $CYAN "Warp Cleanup Script for macOS"
    print_color $CYAN "=============================="
    
    print_color $GREEN "\nStarting Warp cleanup..."
    
    local success_count=0
    local total_operations=0
    
    # Define paths to clean up
    local home_dir="$HOME"
    
    # Warp data directories and files to clean
    local paths_to_clean=(
        "$home_dir/Library/Application Support/dev.warp.Warp-Stable"
        "$home_dir/Library/Application Support/dev.warp.Warp"
        "$home_dir/Library/Caches/dev.warp.Warp-Stable"
        "$home_dir/Library/Caches/dev.warp.Warp"
        "$home_dir/Library/HTTPStorages/dev.warp.Warp-Stable"
        "$home_dir/Library/HTTPStorages/dev.warp.Warp"
        "$home_dir/Library/Logs/dev.warp.Warp-Stable"
        "$home_dir/Library/Logs/dev.warp.Warp"
        "$home_dir/Library/Preferences/dev.warp.Warp-Stable.plist"
        "$home_dir/Library/Preferences/dev.warp.Warp.plist"
        "$home_dir/Library/Saved Application State/dev.warp.Warp-Stable.savedState"
        "$home_dir/Library/Saved Application State/dev.warp.Warp.savedState"
        "$home_dir/Library/WebKit/dev.warp.Warp-Stable"
        "$home_dir/Library/WebKit/dev.warp.Warp"
        "$home_dir/.warp"
    )
    
    local descriptions=(
        "Warp Application Support (Stable)"
        "Warp Application Support"
        "Warp Cache (Stable)"
        "Warp Cache"
        "Warp HTTP Storage (Stable)"
        "Warp HTTP Storage"
        "Warp Logs (Stable)"
        "Warp Logs"
        "Warp Preferences (Stable)"
        "Warp Preferences"
        "Warp Saved State (Stable)"
        "Warp Saved State"
        "Warp WebKit (Stable)"
        "Warp WebKit"
        "Warp Config Directory"
    )
    
    # Clean up each path
    for i in "${!paths_to_clean[@]}"; do
        local path="${paths_to_clean[$i]}"
        local desc="${descriptions[$i]}"
        total_operations=$((total_operations + 1))
        
        print_color $CYAN "\n$total_operations. Cleaning $desc"
        
        if [ -d "$path" ]; then
            if remove_directory "$path" "$desc"; then
                success_count=$((success_count + 1))
            fi
        elif [ -f "$path" ]; then
            if remove_file "$path" "$desc"; then
                success_count=$((success_count + 1))
            fi
        else
            print_color $YELLOW "Path not found: $path"
        fi
    done
    
    # Kill Warp processes if running
    print_color $CYAN "\n$((total_operations + 1)). Stopping Warp processes"
    total_operations=$((total_operations + 1))
    
    if pkill -f "Warp" 2>/dev/null; then
        print_color $GREEN "✓ Stopped running Warp processes"
        success_count=$((success_count + 1))
    else
        print_color $YELLOW "No running Warp processes found"
    fi
    
    # Clear LaunchServices database to remove Warp from Open With menus
    print_color $CYAN "\n$((total_operations + 1)). Clearing LaunchServices database"
    total_operations=$((total_operations + 1))
    
    if /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user >/dev/null 2>&1; then
        print_color $GREEN "✓ Cleared LaunchServices database"
        success_count=$((success_count + 1))
    else
        print_color $YELLOW "Failed to clear LaunchServices database"
    fi
    
    # Summary
    print_color $CYAN "\n=============================="
    print_color $CYAN "Cleanup completed: $success_count/$total_operations operations successful"
    
    if [ $success_count -eq $total_operations ]; then
        print_color $GREEN "🎉 Warp has been completely removed from your system!"
    elif [ $success_count -gt 0 ]; then
        print_color $YELLOW "⚠️  Partial cleanup completed. Some operations failed."
    else
        print_color $RED "❌ Cleanup failed. No changes were made."
    fi
    
    print_color $CYAN "\nNote: You may need to empty the Trash to completely remove all files."
    print_color $CYAN "If Warp was installed via Homebrew, you may also want to run:"
    print_color $CYAN "  brew uninstall --cask warp"
    
    echo ""
    read -p "Press Enter to exit..."
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_color $RED "❌ This script is designed for macOS only!"
    exit 1
fi

# Run main function
main