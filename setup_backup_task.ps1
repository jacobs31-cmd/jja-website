# setup_backup_task.ps1 — JJA Website Backup Scheduler
# ======================================================
# Run this ONCE (as Administrator) to register the daily backup in Windows Task Scheduler.
# After that, Windows will run the backup automatically every night at midnight — even if
# Cowork or Claude is not open.
#
# HOW TO RUN:
#   1. Right-click this file → "Run with PowerShell"
#      (If Windows asks, choose "Run as Administrator")
#   2. You should see "Task registered successfully." in the window.
#   3. Done — backups will now run every night at 12:00 AM.
#
# To verify the task was created, open Task Scheduler and look for "JJA Website Backup".
# To remove the task, run:  Unregister-ScheduledTask -TaskName "JJA Website Backup" -Confirm:$false

$TaskName   = "JJA Website Backup"
$ScriptPath = "C:\Website\backup_website.py"
$PythonExe  = ""

# Auto-detect Python installation
$candidates = @(
    "C:\Python313\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Python39\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
)

foreach ($candidate in $candidates) {
    if (Test-Path $candidate) {
        $PythonExe = $candidate
        break
    }
}

if ($PythonExe -eq "") {
    # Try PATH as a last resort
    $found = Get-Command python -ErrorAction SilentlyContinue
    if ($found) {
        $PythonExe = $found.Source
    }
}

if ($PythonExe -eq "") {
    Write-Host ""
    Write-Host "ERROR: Python not found on this computer." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/ and re-run this script." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Using Python: $PythonExe" -ForegroundColor Cyan

# Remove existing task if it exists (clean re-register)
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# Build the scheduled task
$Action   = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$ScriptPath`""
$Trigger  = New-ScheduledTaskTrigger -Daily -At "12:00AM"
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -StartWhenAvailable `          # runs at next opportunity if the PC was off at midnight
    -RunOnlyIfNetworkAvailable:$false

$Principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType InteractiveToken `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName  $TaskName `
    -Action    $Action `
    -Trigger   $Trigger `
    -Settings  $Settings `
    -Principal $Principal `
    -Force

Write-Host ""
Write-Host "Task registered successfully." -ForegroundColor Green
Write-Host "The backup will run every night at 12:00 AM and save to Google Drive." -ForegroundColor Green
Write-Host "A log of each backup is saved to: C:\Website\backup_log.txt" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to close"
