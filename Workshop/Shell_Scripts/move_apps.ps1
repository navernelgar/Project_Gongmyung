function Move-AppWithJunction {
    param(
        [string]$SourcePath,
        [string]$DestPath
    )

    if (-not (Test-Path $SourcePath)) {
        Write-Warning "Source not found: $SourcePath"
        return
    }

    if (-not (Test-Path $DestPath)) {
        New-Item -ItemType Directory -Path $DestPath -Force | Out-Null
    }

    $FolderName = Split-Path $SourcePath -Leaf
    $Target = Join-Path $DestPath $FolderName

    if (Test-Path $Target) {
        Write-Warning "Target already exists: $Target. Skipping move."
    } else {
        Write-Host "Moving $SourcePath to $Target using Robocopy..." -ForegroundColor Cyan
        # Robocopy to move files, preserving attributes and security, /MOVE deletes from source after copy
        # /E :: copy subdirectories, including empty ones.
        # /MOVE :: move files and dirs (delete from source after copying).
        # /XJ :: exclude junction points (to avoid loops, though usually safe for apps).
        # /R:3 /W:5 :: retry 3 times, wait 5 seconds.
        robocopy $SourcePath $Target /E /MOVE /XJ /R:3 /W:5
        
        if ($LASTEXITCODE -ge 8) {
            Write-Error "Robocopy failed with exit code $LASTEXITCODE"
            return
        }
    }

    if (-not (Test-Path $SourcePath)) {
        Write-Host "Creating Junction at $SourcePath -> $Target" -ForegroundColor Green
        New-Item -ItemType Junction -Path $SourcePath -Target $Target | Out-Null
    } else {
        # If source still exists (e.g. some files locked), we can't make junction easily.
        # Check if empty
        if ((Get-ChildItem $SourcePath -Force).Count -eq 0) {
            Remove-Item $SourcePath -Force
            New-Item -ItemType Junction -Path $SourcePath -Target $Target | Out-Null
            Write-Host "Source was empty, removed and Junction created." -ForegroundColor Green
        } else {
            Write-Warning "Source folder $SourcePath is not empty. Some files might be locked. Junction not created."
        }
    }
}

# List of apps to move. Adjust paths based on previous inventory.
# C:\Program Files\Epic Games -> E:\Apps\Epic Games
# C:\Program Files\Unity -> E:\Apps\Unity
# C:\Program Files\Unity Hub -> E:\Apps\Unity Hub

$appsToMove = @(
    @{Src='C:\Program Files\Epic Games'; Dst='E:\Apps'},
    @{Src='C:\Program Files\Unity'; Dst='E:\Apps'},
    @{Src='C:\Program Files\Unity Hub'; Dst='E:\Apps'}
)

foreach ($app in $appsToMove) {
    Move-AppWithJunction -SourcePath $app.Src -DestPath $app.Dst
}
