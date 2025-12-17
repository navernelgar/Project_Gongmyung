# E:\organize_e_drive.ps1 라이브러리 로드
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ScriptDir) { $ScriptDir = "E:\" }
. "$ScriptDir\organize_e_drive.ps1"

Write-Host "=== 사용자 폴더(Downloads, Documents 등) E드라이브 이동 시작 ===" -ForegroundColor Cyan
Write-Host "주의: 실행 중인 프로그램(브라우저, 탐색기 등)이 해당 폴더를 사용 중이면 이동이 실패할 수 있습니다." -ForegroundColor Yellow

# 이동할 표준 사용자 폴더 목록
$folders = @('Downloads', 'Documents', 'Pictures', 'Videos', 'Music', 'Desktop')

foreach ($folder in $folders) {
    Write-Host "`n[$folder] 이동 시도..."
    try {
        Move-UserFolder -FolderName $folder -ErrorAction Stop
    } catch {
        Write-Warning "$folder 이동 실패: $($_.Exception.Message)"
        Write-Warning " -> 파일이 사용 중일 수 있습니다. 재부팅 직후 다시 시도하는 것이 좋습니다."
    }
}

# 추가 제안: .vscode 폴더
$vscodePath = "C:\Users\$env:USERNAME\.vscode"
if (Test-Path $vscodePath) {
    $size = (Get-ChildItem $vscodePath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1GB
    Write-Host "`n----------------------------------------------------------------"
    Write-Host "[참고] .vscode 폴더 (VS Code 확장 기능 저장소)" -ForegroundColor Cyan
    Write-Host "현재 크기: $([Math]::Round($size, 2)) GB"
    Write-Host "이 폴더는 VS Code가 실행 중일 때는 이동할 수 없습니다."
    Write-Host "VS Code를 완전히 종료한 후, 아래 명령어를 별도로 실행하여 이동하세요:" -ForegroundColor Yellow
    Write-Host "Move-WithJunction -Source `"$vscodePath`" -Destination `"E:\Users\$env:USERNAME\.vscode`"" -ForegroundColor White
    Write-Host "----------------------------------------------------------------"
}

Write-Host "`n작업이 완료되었습니다." -ForegroundColor Green
