# Absolute paths
$projectRoot = "D:\Project_Gongmyung"
$nodeExe = "E:\Apps\NodeJS\node.exe"
$pythonExe = "D:\.venv\Scripts\python.exe"
$pythonwExe = "D:\.venv\Scripts\pythonw.exe"
$aiServerScript = "$projectRoot\Gongmyung_Library\Code_AI\AI_Body_System\ai_server.js"
$mainScript = "$projectRoot\Gongmyung_Library\Code_AI\AI_Body_System\main.py"
$dashboardScript = "$projectRoot\Gongmyung_Library\Code_AI\AI_Body_System\Gongmyung_Dashboard.py"

# Stop any existing processes
Stop-Process -Name "node" -ErrorAction SilentlyContinue
Stop-Process -Name "python" -ErrorAction SilentlyContinue
Stop-Process -Name "pythonw" -ErrorAction SilentlyContinue

Write-Host "Starting Node.js AI Server..."
Write-Host "Node Path: $nodeExe"
Write-Host "Script: $aiServerScript"

# Start Node.js server
$nodeProcess = Start-Process -FilePath $nodeExe -ArgumentList $aiServerScript -PassThru -WindowStyle Hidden -WorkingDirectory "$projectRoot\Gongmyung_Library\Code_AI\AI_Body_System"

Write-Host "Waiting for server to initialize..."
Start-Sleep -Seconds 3

Write-Host "Starting Python Core System (Background)..."
# Start Python Core (Hidden)
Start-Process -FilePath $pythonwExe -ArgumentList $mainScript -WindowStyle Hidden -WorkingDirectory "$projectRoot\Gongmyung_Library\Code_AI\AI_Body_System"

Write-Host "Starting Dashboard (GUI)..."
# Start Dashboard (Visible)
Start-Process -FilePath $pythonwExe -ArgumentList $dashboardScript -WorkingDirectory "$projectRoot\Gongmyung_Library\Code_AI\AI_Body_System"

Write-Host "System Launched. Dashboard should appear shortly."
Write-Host "To stop the system, run 'stop_system.ps1' or use the Tray Icon exit."
Start-Sleep -Seconds 2
