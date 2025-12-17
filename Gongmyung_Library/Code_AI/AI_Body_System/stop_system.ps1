$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Stopping Gongmyung AI Body System (Aggressive Mode)..." -ForegroundColor Yellow

# 1. Stop pythonw.exe (Background processes)
$pythonw = Get-WmiObject Win32_Process | Where-Object { $_.Name -eq 'pythonw.exe' }
if ($pythonw) {
    foreach ($proc in $pythonw) {
        if ($proc.CommandLine -like "*main.py*" -or $proc.CommandLine -like "*Gongmyung_Dashboard.py*") {
            Write-Host "Killing pythonw.exe (PID: $($proc.ProcessId))..."
            Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
        }
    }
}

# 2. Stop python.exe (Console processes)
$python = Get-WmiObject Win32_Process | Where-Object { $_.Name -eq 'python.exe' }
if ($python) {
    foreach ($proc in $python) {
        if ($proc.CommandLine -like "*main.py*" -or $proc.CommandLine -like "*Gongmyung_Dashboard.py*") {
            Write-Host "Killing python.exe (PID: $($proc.ProcessId))..."
            Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
        }
    }
}

# 3. Stop cmd.exe (If launcher.bat is stuck)
# Be careful not to kill the user's terminal. Only kill if it looks like our launcher.
# This is risky, so we'll skip killing cmd.exe for now unless we can identify it uniquely.

Write-Host "All Gongmyung processes have been terminated." -ForegroundColor Green
