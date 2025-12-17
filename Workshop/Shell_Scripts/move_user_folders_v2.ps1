# E:\organize_e_drive.ps1 라이브러리 로드
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ScriptDir) { $ScriptDir = "E:\" }
. "$ScriptDir\organize_e_drive.ps1"

function Merge-And-Link {
    param(
        [string]$Source,
        [string]$Destination
    )
    
    if (-not (Test-Path $Source)) { Write-Warning "[$Source] 원본이 없습니다."; return }
    
    # 1. 대상 폴더 생성
    if (-not (Test-Path $Destination)) { New-Item -ItemType Directory -Path $Destination -Force | Out-Null }

    # 2. Robocopy로 파일 이동 (병합)
    # /E: 하위 폴더 포함, /MOVE: 파일/폴더 이동(원본 삭제), /XJ: 정션 제외, /R:1 /W:1: 재시도 제한
    Write-Host "이동 중: $Source -> $Destination"
    $logFile = "$env:TEMP\robocopy_move.log"
    Robocopy $Source $Destination /E /MOVE /XJ /R:1 /W:1 /LOG:$logFile
    
    # Robocopy 종료 코드 확인 (0-7은 성공/부분성공)
    if ($LASTEXITCODE -gt 7) {
        Write-Warning "Robocopy 이동 중 오류 발생. 로그 확인: $logFile"
        # 로그 내용 일부 출력
        Get-Content $logFile -Tail 5
        return
    }

    # 3. 원본 폴더가 비었는지 확인 후 삭제 (Robocopy /MOVE는 폴더를 남길 수 있음)
    if (Test-Path $Source) {
        $items = Get-ChildItem $Source -Force -ErrorAction SilentlyContinue
        if ($items.Count -eq 0) {
            Remove-Item $Source -Force -ErrorAction SilentlyContinue
        } else {
            Write-Warning "[$Source] 이동 후에도 파일이 남아있어 정션을 생성할 수 없습니다. (사용 중인 파일 존재 가능)"
            return
        }
    }

    # 4. 정션 생성
    if (-not (Test-Path $Source)) {
        New-Item -ItemType Junction -Path $Source -Target $Destination | Out-Null
        Write-Host "SUCCESS: [$Source] -> [$Destination] 연결 완료" -ForegroundColor Green
    }
}

Write-Host "=== 사용자 폴더(Downloads, Documents 등) E드라이브 이동 (병합 모드) ===" -ForegroundColor Cyan
Write-Host "주의: 실행 중인 프로그램이 있으면 이동이 실패할 수 있습니다." -ForegroundColor Yellow

$User = $env:USERNAME
$TargetRoot = "E:\Users\$User"

# 이동할 폴더 목록
$folders = @('Downloads', 'Documents', 'Pictures', 'Videos', 'Music', 'Desktop')

foreach ($folder in $folders) {
    $src = "C:\Users\$User\$folder"
    $dst = "$TargetRoot\$folder"
    
    # 이미 정션인지 확인
    $item = Get-Item $src -ErrorAction SilentlyContinue
    if ($item.LinkType -eq 'Junction') {
        Write-Host "[$folder] 이미 연결되어 있습니다. (Skip)" -ForegroundColor Gray
        continue
    }

    Write-Host "`n[$folder] 처리 중..."
    Merge-And-Link -Source $src -Destination $dst
}

# .vscode 처리
$vscodeSrc = "C:\Users\$User\.vscode"
$vscodeDst = "E:\Users\$User\.vscode"
if (Test-Path $vscodeSrc) {
    $item = Get-Item $vscodeSrc
    if ($item.LinkType -ne 'Junction') {
        Write-Host "`n[.vscode] 폴더 처리 (VS Code 종료 필요)" -ForegroundColor Cyan
        # VS Code가 실행 중인지 확인하지 않고 제안만 함 (스크립트 실행 중이므로)
        Write-Host "VS Code를 종료한 상태라면 아래 명령으로 이동 가능합니다:"
        Write-Host "Merge-And-Link -Source `"$vscodeSrc`" -Destination `"$vscodeDst`"" -ForegroundColor Yellow
    }
}

Write-Host "`n작업 완료." -ForegroundColor Green
