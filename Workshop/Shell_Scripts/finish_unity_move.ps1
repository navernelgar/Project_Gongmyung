# 관리자 권한 확인
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit
}

$Source = "C:\Program Files\Unity Hub"
$Dest = "E:\Apps\Unity Hub"

Write-Host "=== Unity Hub 이동 마무리 (원본 삭제 및 연결) ===" -ForegroundColor Cyan

# 1. 데이터 검증
$countSource = (Get-ChildItem $Source -Recurse -Force -ErrorAction SilentlyContinue).Count
$countDest = (Get-ChildItem $Dest -Recurse -Force -ErrorAction SilentlyContinue).Count

Write-Host "원본 파일 수: $countSource"
Write-Host "대상 파일 수: $countDest"

if ($countDest -eq 0) {
    Write-Error "E드라이브에 파일이 없습니다. 작업을 중단합니다."
    exit
}

# 2. 원본 삭제 시도
Write-Host "`nC드라이브 원본 폴더 삭제 시도..." -ForegroundColor Yellow
try {
    Remove-Item $Source -Recurse -Force -ErrorAction Stop
    Write-Host " -> 삭제 성공!" -ForegroundColor Green
} catch {
    Write-Warning " -> 삭제 실패: $($_.Exception.Message)"
    Write-Warning " -> 여전히 파일이 사용 중입니다. 컴퓨터를 재부팅해야만 해결됩니다."
    Write-Host "`n아무 키나 누르면 종료합니다."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# 3. 정션 생성
Write-Host "`n정션(연결) 생성 중..."
New-Item -ItemType Junction -Path $Source -Target $Dest | Out-Null
Write-Host "SUCCESS: 모든 작업이 완료되었습니다!" -ForegroundColor Green

Write-Host "`n아무 키나 누르면 종료합니다."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
