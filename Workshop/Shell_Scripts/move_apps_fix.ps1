# 관리자 권한 확인 및 자동 상승
$currentPrincipal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "관리자 권한이 필요합니다. 새 창에서 권한 상승을 요청합니다..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# --- 관리자 권한 실행 영역 ---
$Host.UI.RawUI.WindowTitle = "앱 이동 및 정션 연결 (관리자)"

# 1. 프로세스 종료 (파일 잠금 해제)
Write-Host "=== 1. 실행 중인 관련 프로세스 종료 ===" -ForegroundColor Cyan
$processes = @('Unity', 'Unity Hub', 'UnityEditor', 'UnityLicensingClient', 'EpicGamesLauncher', 'EpicWebHelper')
foreach ($proc in $processes) {
    $p = Get-Process -Name $proc -ErrorAction SilentlyContinue
    if ($p) {
        Write-Host " - $proc 종료 중..." -ForegroundColor Yellow
        Stop-Process -Name $proc -Force -ErrorAction SilentlyContinue
    }
}
Start-Sleep -Seconds 2 # 프로세스 종료 대기

# 2. 이동 및 연결 함수
function Force-MoveAndLink {
    param(
        [string]$Source,
        [string]$DestParent
    )

    $FolderName = Split-Path $Source -Leaf
    $Target = Join-Path $DestParent $FolderName

    Write-Host "`n[$FolderName] 처리 시작..." -ForegroundColor Cyan

    # 원본이 없으면
    if (-not (Test-Path $Source)) {
        # 이미 정션인지 확인
        if (Test-Path $Source -PathType Container) {
             # 정션도 디렉토리로 인식되므로 LinkType 확인 필요하지만, Test-Path가 False면 아예 없는 것
             # 하지만 정션이 깨져있거나 다른 상황일 수 있음.
             # 여기서는 단순하게 원본 폴더가 없으면 이미 이동된 것으로 간주하고 정션 확인
             Write-Warning "원본 폴더가 없습니다: $Source"
        }
        # 정션 확인 및 생성
        if (-not (Test-Path $Source)) {
             # 원본 경로가 아예 없으면 정션 생성 시도
             New-Item -ItemType Junction -Path $Source -Target $Target -Force | Out-Null
             Write-Host " - 정션 복구 완료: $Source -> $Target" -ForegroundColor Green
             return
        }
    }

    # 원본이 정션인지 확인
    $item = Get-Item $Source -ErrorAction SilentlyContinue
    if ($item.LinkType -eq 'Junction') {
        Write-Host " - 이미 정션으로 연결되어 있습니다. (완료됨)" -ForegroundColor Green
        return
    }

    # 대상 폴더 생성
    if (-not (Test-Path $Target)) {
        New-Item -ItemType Directory -Path $Target -Force | Out-Null
    }

    # Robocopy 이동 (병합 모드)
    Write-Host " - 파일 이동 중 (Robocopy)..."
    $logFile = "$env:TEMP\move_app_debug.log"
    # /MOVE: 이동(원본 삭제), /E: 하위포함, /IS /IT: 같은 파일도 처리(병합 시 유용), /XJ: 정션 제외
    # /R:1 /W:1: 재시도 최소화
    Robocopy $Source $Target /E /MOVE /XJ /R:1 /W:1 /LOG:$logFile

    # 원본 폴더 확인
    if (Test-Path $Source) {
        $remaining = Get-ChildItem $Source -Force -ErrorAction SilentlyContinue
        if ($remaining.Count -eq 0) {
            Write-Host " - 원본 폴더가 비었습니다. 삭제합니다."
            Remove-Item $Source -Force
        } else {
            Write-Warning " - 이동 실패: 원본에 파일이 남아있습니다. (로그 확인: $logFile)"
            Get-Content $logFile -Tail 5
            return # 정션 생성 불가
        }
    }

    # 정션 생성
    if (-not (Test-Path $Source)) {
        New-Item -ItemType Junction -Path $Source -Target $Target | Out-Null
        Write-Host "SUCCESS: $Source -> $Target 연결 성공!" -ForegroundColor Green
    }
}

# 3. 작업 수행
$apps = @(
    @{Src='C:\Program Files\Epic Games'; Dst='E:\Apps'},
    @{Src='C:\Program Files\Unity'; Dst='E:\Apps'},
    @{Src='C:\Program Files\Unity Hub'; Dst='E:\Apps'}
)

foreach ($app in $apps) {
    Force-MoveAndLink -Source $app.Src -DestParent $app.Dst
}

Write-Host "`n모든 작업이 완료되었습니다. 아무 키나 누르면 종료합니다." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
