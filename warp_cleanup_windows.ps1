# Warp Cleanup Script for Windows (PowerShell)
# This script removes Warp registry entries and data directories

# Check if running as Administrator
function Test-IsAdmin {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to remove registry key recursively
function Remove-RegistryKeyRecursive {
    param(
        [Parameter(Mandatory=$true)]
        [string]$KeyPath
    )
    
    try {
        if (Test-Path $KeyPath) {
            Write-Host "Removing registry key: $KeyPath" -ForegroundColor Yellow
            Remove-Item -Path $KeyPath -Recurse -Force -ErrorAction Stop
            Write-Host "✓ Successfully deleted registry key: $KeyPath" -ForegroundColor Green
            return $true
        } else {
            Write-Host "Registry key not found: $KeyPath" -ForegroundColor Yellow
            return $false
        }
    }
    catch [System.UnauthorizedAccessException] {
        Write-Host "❌ Permission denied accessing registry key: $KeyPath" -ForegroundColor Red
        return $false
    }
    catch {
        Write-Host "❌ Error deleting registry key ${KeyPath}: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to remove directory
function Remove-DirectoryRecursive {
    param(
        [Parameter(Mandatory=$true)]
        [string]$DirectoryPath
    )
    
    try {
        if (Test-Path $DirectoryPath -PathType Container) {
            Write-Host "Removing directory: $DirectoryPath" -ForegroundColor Yellow
            Remove-Item -Path $DirectoryPath -Recurse -Force -ErrorAction Stop
            Write-Host "✓ Successfully deleted directory: $DirectoryPath" -ForegroundColor Green
            return $true
        } else {
            Write-Host "Directory not found: $DirectoryPath" -ForegroundColor Yellow
            return $false
        }
    }
    catch [System.UnauthorizedAccessException] {
        Write-Host "❌ Permission denied deleting directory: $DirectoryPath" -ForegroundColor Red
        return $false
    }
    catch {
        Write-Host "❌ Error deleting directory ${DirectoryPath}: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
function Main {
    Write-Host "Warp Cleanup Script for Windows (PowerShell)" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # Check if running as Administrator
    if (-not (Test-IsAdmin)) {
        Write-Host "⚠️  Warning: This script is not running as Administrator." -ForegroundColor Yellow
        Write-Host "   Some registry operations may fail." -ForegroundColor Yellow
        $response = Read-Host "Continue anyway? (y/n)"
        if ($response.ToLower() -ne 'y') {
            Write-Host "Exiting..." -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host "`nStarting Warp cleanup..." -ForegroundColor Green
    
    # Registry path to clean (using PowerShell registry provider syntax)
    $registryPath = "Registry::HKEY_USERS\S-1-5-21-1975947051-2922622289-44519384-1002\Software\Warp.dev\Warp"
    
    # Data directory to clean
    $dataDirectory = "C:\Users\12925\AppData\Local\warp"
    
    $successCount = 0
    $totalOperations = 2
    
    # Clean registry
    Write-Host "`n1. Cleaning registry: $registryPath" -ForegroundColor Cyan
    if (Remove-RegistryKeyRecursive -KeyPath $registryPath) {
        $successCount++
    }
    
    # Clean data directory
    Write-Host "`n2. Cleaning data directory: $dataDirectory" -ForegroundColor Cyan
    if (Remove-DirectoryRecursive -DirectoryPath $dataDirectory) {
        $successCount++
    }
    
    # Summary
    Write-Host ("`n" + "=" * 50) -ForegroundColor Cyan
    Write-Host "Cleanup completed: $successCount/$totalOperations operations successful" -ForegroundColor Cyan
    
    if ($successCount -eq $totalOperations) {
        Write-Host "🎉 Warp has been completely removed from your system!" -ForegroundColor Green
    } elseif ($successCount -gt 0) {
        Write-Host "⚠️  Partial cleanup completed. Some operations failed." -ForegroundColor Yellow
    } else {
        Write-Host "❌ Cleanup failed. No changes were made." -ForegroundColor Red
    }
    
    Read-Host "`nPress Enter to exit"
}

# Set execution policy for this session if needed
try {
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue
} catch {
    # Ignore errors if we can't set execution policy
}

# Run the main function
Main