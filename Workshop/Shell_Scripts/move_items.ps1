$moves = @(
  @{Src='E:\AI_body_system'; Dst='E:\Dev\AI_body_system'},
  @{Src='E:\ai-collaborator'; Dst='E:\Dev\ai-collaborator'},
  @{Src='E:\OpenAI-export'; Dst='E:\Archive\OpenAI-export'},
  @{Src='E:\OpenAI-export.zip'; Dst='E:\Archive\OpenAI-export.zip'},
  @{Src='E:\Start_Here_*.pdf'; Dst='E:\Archive\Docs'},
  @{Src='E:\Start_Here_*.exe'; Dst='E:\Archive\Installers'},
  @{Src='E:\Warranty.pdf'; Dst='E:\Archive\Docs'},
  @{Src='E:\*.log'; Dst='E:\Logs'},
  @{Src='E:\Application Verifier'; Dst='E:\Apps\Application Verifier'},
  @{Src='E:\Chocolatey'; Dst='E:\Apps\Chocolatey'},
  @{Src='E:\ChocolateyHttpCache'; Dst='E:\Apps\ChocolateyHttpCache'},
  @{Src='E:\Git'; Dst='E:\Apps\Git'},
  @{Src='E:\Python313'; Dst='E:\Apps\Python313'},
  @{Src='E:\inetpub'; Dst='E:\Apps\inetpub'},
  @{Src='E:\node_modules'; Dst='E:\Temp\node_modules_root'},
  @{Src='E:\package.json'; Dst='E:\Temp\package_root.json'},
  @{Src='E:\package-lock.json'; Dst='E:\Temp\package-lock_root.json'}
)

if (-not (Test-Path 'E:\Archive\Docs')) { New-Item -ItemType Directory -Path 'E:\Archive\Docs' | Out-Null }
if (-not (Test-Path 'E:\Archive\Installers')) { New-Item -ItemType Directory -Path 'E:\Archive\Installers' | Out-Null }

foreach ($m in $moves) {
  $items = Get-ChildItem $m.Src -ErrorAction SilentlyContinue
  foreach ($item in $items) {
    $dest = $m.Dst
    # Handle wildcard destination logic if needed, but here Dst is explicit folder or file name usually.
    # If Dst is a folder that doesn't exist, Move-Item might rename the file to that name if it's a file move.
    # So we ensure parent exists.
    
    $destParent = Split-Path $dest -Parent
    if (-not (Test-Path $destParent)) { New-Item -ItemType Directory -Path $destParent | Out-Null }
    
    # If we are moving a folder to a folder, we want it INSIDE.
    # If Dst is 'E:\Dev\AI_body_system', we want 'E:\AI_body_system' to become 'E:\Dev\AI_body_system'.
    # Move-Item E:\AI_body_system E:\Dev\AI_body_system works if E:\Dev exists.
    
    try {
        Move-Item -Path $item.FullName -Destination $dest -Force -ErrorAction Stop
        Write-Host "Moved $($item.Name) to $dest"
    } catch {
        Write-Warning "Failed to move $($item.Name): $_"
    }
  }
}
