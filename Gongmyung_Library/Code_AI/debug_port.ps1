param(
    [int]$Port = 3001
)

Write-Host "🔍 Searching for the cause of port $Port conflict..." -ForegroundColor Cyan

# 1. Find the PID holding the port
$netstat = netstat -ano | findstr ":$Port"
if (-not $netstat) {
    Write-Host "✅ Port $Port is clean! No conflict found." -ForegroundColor Green
    exit
}

Write-Host "⚠️  Port $Port is currently in use!" -ForegroundColor Yellow
$netstat | ForEach-Object { Write-Host "   $_" }

# Extract PIDs
$pids = $netstat | ForEach-Object { 
    $_ -match "\s+(\d+)$" > $null
    $matches[1] 
} | Select-Object -Unique

# 2. Identify the Process
foreach ($id in $pids) {
    if ($id -eq 0) { continue }
    try {
        $proc = Get-Process -Id $id -ErrorAction Stop
        Write-Host "   [PID: $id] is held by: " -NoNewline
        Write-Host "$($proc.ProcessName)" -ForegroundColor Red -NoNewline
        Write-Host " (Path: $($proc.Path))"
        
        # Optional: Suggest killing it
        Write-Host "   👉 To fix this, run: Stop-Process -Id $id -Force" -ForegroundColor Gray
    }
    catch {
        Write-Host "   [PID: $id] exists but access is denied or it's a system process." -ForegroundColor DarkGray
    }
}

Write-Host "`n💡 Reason: The process listed above is holding the door handle (Port $Port)." -ForegroundColor Cyan
