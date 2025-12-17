$ErrorActionPreference = "Stop"

try {
    $WshShell = New-Object -comObject WScript.Shell
    $ProjectDir = "D:\Project_Gongmyung\Gongmyung_Library\Code_AI\AI_Body_System"
    $BatPath = "$ProjectDir\launcher.bat"
    
    # 아이콘 설정 (shell32.dll의 42번째 아이콘 - 트리 모양 등)
    $IconPath = "C:\Windows\System32\shell32.dll,41" 

    # 1. 바탕화면 바로가기 생성 (Desktop Shortcut)
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $ShortcutPath = "$DesktopPath\Gongmyung_AI.lnk"
    
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $BatPath
    $Shortcut.WorkingDirectory = $ProjectDir
    $Shortcut.WindowStyle = 1 # 1: Normal, 3: Maximize, 7: Minimize
    $Shortcut.IconLocation = $IconPath
    $Shortcut.Description = "Launch Gongmyung AI Body System"
    $Shortcut.Save()
    
    Write-Host "[Success] Desktop shortcut created at: $ShortcutPath"

    # 2. 시작프로그램 바로가기 생성 (Startup Shortcut)
    $StartupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    $StartupShortcutPath = "$StartupPath\Gongmyung_AI.lnk"
    
    $StartupShortcut = $WshShell.CreateShortcut($StartupShortcutPath)
    $StartupShortcut.TargetPath = $BatPath
    $StartupShortcut.WorkingDirectory = $ProjectDir
    $StartupShortcut.WindowStyle = 1
    $StartupShortcut.IconLocation = $IconPath
    $StartupShortcut.Description = "Auto-start Gongmyung AI Body System"
    $StartupShortcut.Save()
    
    Write-Host "[Success] Startup shortcut created at: $StartupShortcutPath"
    Write-Host "`n모든 설정이 완료되었습니다. 이제 바탕화면의 아이콘을 더블 클릭하거나, 재부팅 시 자동으로 실행됩니다."

} catch {
    Write-Error "바로가기 생성 중 오류가 발생했습니다: $_"
}
