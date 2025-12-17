# 관리자 권한 확인 및 자동 상승 스크립트
$currentPrincipal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "관리자 권한이 필요합니다. 새 창에서 권한 상승을 요청합니다..." -ForegroundColor Yellow
    # 현재 스크립트를 관리자 권한으로 새 창에서 재실행
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# --- 여기서부터는 관리자 권한으로 실행됩니다 (새 창) ---
$Host.UI.RawUI.WindowTitle = "C드라이브 최적화 작업 (관리자)"
Write-Host "=== C드라이브 최적화 작업 시작 ===" -ForegroundColor Cyan

# 1. 최대 절전 모드 해제
Write-Host "`n[1/2] 최대 절전 모드(hiberfil.sys) 해제 중..." -ForegroundColor Yellow
try {
    powercfg /h off
    Write-Host " -> 성공: 최대 절전 모드가 해제되었습니다. (약 6~16GB 확보)" -ForegroundColor Green
} catch {
    Write-Warning " -> 오류 발생: $($_.Exception.Message)"
}

# 2. 윈도우 업데이트 저장소 정리 (DISM)
Write-Host "`n[2/2] 윈도우 업데이트 저장소(WinSxS) 정리 중..." -ForegroundColor Yellow
Write-Host " -> 이 작업은 시간이 다소 걸릴 수 있습니다. 창을 닫지 마세요." -ForegroundColor Gray
try {
    # DISM 명령 실행
    $dismArgs = "/Online /Cleanup-Image /StartComponentCleanup /ResetBase"
    Start-Process -FilePath "dism.exe" -ArgumentList $dismArgs -Wait -NoNewWindow
    Write-Host "`n -> 정리 작업 완료." -ForegroundColor Green
} catch {
    Write-Warning " -> DISM 실행 중 오류 발생."
}

Write-Host "`n--------------------------------------------------------"
Write-Host "모든 최적화 작업이 끝났습니다." -ForegroundColor Cyan
Write-Host "아무 키나 누르면 이 창이 닫힙니다."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
