$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")

# 1. Start Shortcut (Green/Play Theme)
$StartShortcutPath = "$DesktopPath\[Gongmyung] START.lnk"
$StartTargetPath = "$DesktopPath\Gongmyung_Start.bat"

# Check if bat exists, if not assume standard path
if (-not (Test-Path $StartTargetPath)) {
    $StartTargetPath = "C:\Users\Owner\Desktop\Gongmyung_Start.bat"
}

$Shortcut = $WshShell.CreateShortcut($StartShortcutPath)
$Shortcut.TargetPath = $StartTargetPath
$Shortcut.Description = "Start Gongmyung AI System"
# Icon: imageres.dll index 96 is often a green shield/check, or shell32.dll 296 (Play). 
# Let's use shell32.dll, 137 (Run) or 246 (Green arrow). 
# shell32.dll, 246 is a good "Go" icon.
$Shortcut.IconLocation = "shell32.dll, 246" 
$Shortcut.Save()

# 2. Stop Shortcut (Red/Stop Theme)
$StopShortcutPath = "$DesktopPath\[Gongmyung] STOP.lnk"
$StopTargetPath = "$DesktopPath\Gongmyung_Stop.bat"

if (-not (Test-Path $StopTargetPath)) {
    $StopTargetPath = "C:\Users\Owner\Desktop\Gongmyung_Stop.bat"
}

$Shortcut = $WshShell.CreateShortcut($StopShortcutPath)
$Shortcut.TargetPath = $StopTargetPath
$Shortcut.Description = "Stop Gongmyung AI System"
# Icon: shell32.dll, 27 is the standard Shutdown icon.
$Shortcut.IconLocation = "shell32.dll, 27"
$Shortcut.Save()

Write-Host "Shortcuts created on Desktop:"
Write-Host "1. [Gongmyung] START (Green Arrow Icon)"
Write-Host "2. [Gongmyung] STOP (Red Power Icon)"
