$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$RepoPath = "D:\Project_Gongmyung"

# 1. Manual Button (수동 실행)
$ShortcutManual = $WshShell.CreateShortcut("$DesktopPath\Gongmyung_Manual.lnk")
$ShortcutManual.TargetPath = "$RepoPath\Run_Manual.bat"
$ShortcutManual.IconLocation = "shell32.dll,70" # Monitor icon
$ShortcutManual.Description = "Run Gongmyung Daemon Manually"
$ShortcutManual.Save()

# 2. Auto Button (자동 등록)
$ShortcutAuto = $WshShell.CreateShortcut("$DesktopPath\Gongmyung_Auto_Register.lnk")
$ShortcutAuto.TargetPath = "$RepoPath\Register_Auto.bat"
$ShortcutAuto.IconLocation = "shell32.dll,239" # Settings/Gear icon
$ShortcutAuto.Description = "Register Gongmyung to Startup"
$ShortcutAuto.Save()

Write-Host "Shortcuts created on Desktop: Gongmyung_Manual.lnk, Gongmyung_Auto_Register.lnk"