# Gongmyung Backup Script
# Creates a backup of the current project to a folder on the Desktop

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$BackupFolder = Join-Path $DesktopPath "Gongmyung_Backup_$(Get-Date -Format 'yyyyMMdd_HHmm')"

Write-Host "📦 Starting Backup to: $BackupFolder" -ForegroundColor Cyan

# Create Backup Directory
New-Item -ItemType Directory -Force -Path $BackupFolder | Out-Null

# Source Directory (Current Project)
$SourceDir = "D:\Project_Gongmyung\Gongmyung_Library\Code_AI"

# Copy Files
Copy-Item -Path "$SourceDir\*" -Destination $BackupFolder -Recurse -Force

Write-Host "✅ Backup Complete!" -ForegroundColor Green
Write-Host "📂 You can find the backup folder on your Desktop." -ForegroundColor Yellow
Invoke-Item $BackupFolder
