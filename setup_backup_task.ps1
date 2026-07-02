# setup_backup_task.ps1 — JJA Website Backup Scheduler
# ======================================================
# Run this ONCE (as Administrator) to register the daily backup in Windows Task Scheduler.
# After that, Windows will run the backup automatically every night at midnight — even if
# Cowork or Claude is not open, and (S4U) even if nobody is logged in.
#
# HOW TO RUN:
#   powershell -ExecutionPolicy Bypass -File C:\Website\setup_backup_task.ps1
#   (from an Administrator command prompt)
#
# Fixed 2026-07-02: a comment after a backtick broke the settings block, LogonType
# "InteractiveToken" is not valid in Windows PowerShell 5 (must be "Interactive"/"S4U"),
# success message printed even on failure, and the Python probe could pick the
# Microsoft Store stub (which silently does nothing under the scheduler).
#
# To verify:  schtasks /query /tn "JJA Website Backup" /v /fo LIST
# To remove:  Unregister-ScheduledTask -TaskName "JJA Website Backup" -Confirm:$false

$TaskName   = "JJA Website Backup"
$ScriptPath = "C:\Website\backup_website.py"
$PythonExe  = ""

# Auto-detect a REAL Python (verified by actually running --version).
# The WindowsApps "python.exe" alias is excluded — it can be a Store stub that
# exits without doing anything when the scheduler invokes it.
$candidates = @(
    "C:\Python313\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Python39\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
    "C:\Windows\py.exe"
)

foreach ($candidate in $candidates) {
    if (Test-Path $candidate) {
        $ver = & $candidate --version 2>&1
        if ("$ver" -match "Python 3") { $PythonExe = $candidate; break }
    }
}

if ($PythonExe -eq "") {
    # Last resort: anything named python/py on PATH that is NOT the WindowsApps alias
    foreach ($name in @("py", "python")) {
        $found = Get-Command $name -ErrorAction SilentlyContinue
        if ($found -and $found.Source -notlike "*WindowsApps*") {
            $ver = & $found.Source --version 2>&1
            if ("$ver" -match "Python 3") { $PythonExe = $found.Source; break }
        }
    }
}

if ($PythonExe -eq "") {
    # Truly last resort: accept the WindowsApps one ONLY if it really runs Python
    $found = Get-Command python -ErrorAction SilentlyContinue
    if ($found) {
        $ver = & $found.Source --version 2>&1
        if ("$ver" -match "Python 3") { $PythonExe = $found.Source }
    }
}

if ($PythonExe -eq "") {
    Write-Host ""
    Write-Host "ERROR: no working Python 3 found on this computer." -ForegroundColor Red
    Write-Host "Install Python from https://www.python.org/downloads/ (check 'Add to PATH') and re-run." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Using Python: $PythonExe  ($(& $PythonExe --version 2>&1))" -ForegroundColor Cyan

try {
    # Remove existing task if it exists (clean re-register)
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

    # Build the scheduled task.
    # -StartWhenAvailable  → runs at next opportunity if the PC was off/asleep at midnight.
    # LogonType S4U        → runs whether or not anyone is logged in (no password stored).
    $Action   = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$ScriptPath`"" -ErrorAction Stop
    $Trigger  = New-ScheduledTaskTrigger -Daily -At "12:00AM" -ErrorAction Stop
    $Settings = New-ScheduledTaskSettingsSet `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
        -StartWhenAvailable `
        -ErrorAction Stop

    $Principal = New-ScheduledTaskPrincipal `
        -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType S4U `
        -RunLevel Highest `
        -ErrorAction Stop

    Register-ScheduledTask `
        -TaskName  $TaskName `
        -Action    $Action `
        -Trigger   $Trigger `
        -Settings  $Settings `
        -Principal $Principal `
        -Force `
        -ErrorAction Stop | Out-Null

    $info = Get-ScheduledTaskInfo -TaskName $TaskName -ErrorAction Stop
    Write-Host ""
    Write-Host "Task registered successfully." -ForegroundColor Green
    Write-Host ("Next run: {0}" -f $info.NextRunTime) -ForegroundColor Green
    Write-Host "Backups save to C:\AI Backup (Google Drive synced)." -ForegroundColor Green
    Write-Host "Log: C:\AI Backup\backup_log.txt" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To test it right now:  Start-ScheduledTask -TaskName 'JJA Website Backup'" -ForegroundColor Yellow
}
catch {
    Write-Host ""
    Write-Host "FAILED to register the task:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to close"
