Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "pythonw" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
Write-Host "All Gongmyung systems (Python & Node.js) stopped."