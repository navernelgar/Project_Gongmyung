$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Starting Gongmyung AI Body System (Background Mode)..." -ForegroundColor Cyan

# Start Main Core (Hidden)
Write-Host "Launching Main Core (main.py)..."
Start-Process pythonw -ArgumentList "main.py" -WorkingDirectory $ScriptDir

# Wait a moment for the core to initialize
Start-Sleep -Seconds 2

# Start Dashboard (GUI only, no console)
Write-Host "Launching Dashboard (Gongmyung_Dashboard.py)..."
Start-Process pythonw -ArgumentList "Gongmyung_Dashboard.py" -WorkingDirectory $ScriptDir

Write-Host "System Started in Background." -ForegroundColor Green
