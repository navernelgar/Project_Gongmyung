$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")

# Update Start Shortcut
$StartShortcutPath = "$DesktopPath\[Gongmyung] START.lnk"
$StartTargetPath = "D:\Project_Gongmyung\Desktop_Workspace\Gongmyung_Start.bat"
$Shortcut = $WshShell.CreateShortcut($StartShortcutPath)
$Shortcut.TargetPath = $StartTargetPath
$Shortcut.IconLocation = "shell32.dll, 246" 
$Shortcut.Save()

# Update Stop Shortcut
$StopShortcutPath = "$DesktopPath\[Gongmyung] STOP.lnk"
$StopTargetPath = "D:\Project_Gongmyung\Desktop_Workspace\Gongmyung_Stop.bat"
$Shortcut = $WshShell.CreateShortcut($StopShortcutPath)
$Shortcut.TargetPath = $StopTargetPath
$Shortcut.IconLocation = "shell32.dll, 27"
$Shortcut.Save()
