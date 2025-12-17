# 관리자 권한 확인
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit
}

$Source = "C:\Program Files\Unity Hub"
$Dest = "E:\Apps\Unity Hub"

Write-Host "=== Unity Hub 강제 이동 시작 ===" -ForegroundColor Cyan

# 1. 프로세스 강제 종료
Write-Host "1. 프로세스 종료 중..."
taskkill /F /IM "Unity Hub.exe" 2>$null
taskkill /F /IM "UnityLicensingClient.exe" 2>$null
taskkill /F /IM "Unity.exe" 2>$null
Start-Sleep -Seconds 2

# 2. 대상 폴더 생성
if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }

# 3. Robocopy 이동
Write-Host "2. 파일 이동 중..."
Robocopy $Source $Dest /E /MOVE /XJ /R:3 /W:1 /IS /IT

# 4. 정션 생성
if (Test-Path $Source) {
    if ((Get-ChildItem $Source).Count -eq 0) {
        Remove-Item $Source -Force
        New-Item -ItemType Junction -Path $Source -Target $Dest | Out-Null
        Write-Host "SUCCESS: Unity Hub 이동 및 연결 완료!" -ForegroundColor Green
    } else {
        Write-Warning "실패: 여전히 사용 중인 파일이 있어 원본을 삭제하지 못했습니다."
        Write-Warning "재부팅 후 다시 시도해야 합니다."
    }
} else {
    New-Item -ItemType Junction -Path $Source -Target $Dest | Out-Null
    Write-Host "SUCCESS: Unity Hub 이동 및 연결 완료!" -ForegroundColor Green
}

Write-Host "`n아무 키나 누르면 종료합니다."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
