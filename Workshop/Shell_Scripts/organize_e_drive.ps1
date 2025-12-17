<#
E 드라이브 재구조화 및 C 드라이브 최적화 지원 스크립트
주의: 실제 이동/삭제 전 -WhatIf, -Confirm 활용. 관리자 권한 필요 작업 있음.
#>

#region 설정 커스터마이즈
$Global:Root = 'E:\'
$Global:Structure = @{
  Dev = 'E:\Dev'
  Apps = 'E:\Apps'
  Data = 'E:\Data'
  Models = 'E:\Models'
  Media = 'E:\Media'
  Archive = 'E:\Archive'
  Temp = 'E:\Temp'
  Logs = 'E:\Logs'
}
#endregion

function New-TargetStructure {
  param()
  foreach ($kv in $Global:Structure.GetEnumerator()) {
    if (-not (Test-Path $kv.Value)) {
      New-Item -ItemType Directory -Path $kv.Value | Out-Null
      Write-Host "[CREATE] $($kv.Value)" -ForegroundColor Green
    } else {
      Write-Host "[EXIST]  $($kv.Value)"
    }
  }
}

function Move-WithJunction {
  param(
    [Parameter(Mandatory)] [string] $Source,
    [Parameter(Mandatory)] [string] $Destination
  )
  if (-not (Test-Path $Source)) { Write-Warning "Source not found: $Source"; return }
  if (-not (Test-Path $Destination)) { New-Item -ItemType Directory -Path $Destination | Out-Null }
  $Name = Split-Path $Source -Leaf
  $Target = Join-Path $Destination $Name
  if (Test-Path $Target) { Write-Warning "Target already exists: $Target"; return }
  Write-Host "Moving $Source -> $Target"
  Move-Item $Source $Target
  New-Item -ItemType Junction -Path $Source -Target $Target | Out-Null
}

function Archive-OldLogs {
  param(
    [string] $LogRoot = 'E:\AI_body_system\logs',
    [int] $Days = 14,
    [string] $ArchiveRoot = 'E:\AI_body_system\logs_archive'
  )
  if (-not (Test-Path $LogRoot)) { return }
  $Cutoff = (Get-Date).AddDays(-$Days)
  Get-ChildItem $LogRoot -File | Where-Object { $_.LastWriteTime -lt $Cutoff } | ForEach-Object {
    if (-not (Test-Path $ArchiveRoot)) { New-Item -ItemType Directory -Path $ArchiveRoot | Out-Null }
    $dest = Join-Path $ArchiveRoot ($_.Name + '.zip')
    Compress-Archive -Path $_.FullName -DestinationPath $dest -Force
    Remove-Item $_.FullName -Force
  }
}

function Compress-Folder {
  param(
    [Parameter(Mandatory)] [string] $Folder,
    [string] $DestinationZip
  )
  if (-not $DestinationZip) { $DestinationZip = "$Folder.zip" }
  if (-not (Test-Path $Folder)) { Write-Warning "Folder not found"; return }
  Compress-Archive -Path (Join-Path $Folder '*') -DestinationPath $DestinationZip -Force
}

function Clean-TempAreas {
  param([switch] $NoConfirm)
  $Targets = @(
    'C:\Windows\Temp',
    "$env:TEMP",
    'C:\Users\Public\Downloads'
  )
  foreach ($t in $Targets) {
    if (Test-Path $t) {
      Write-Host "Cleaning $t"
      Get-ChildItem $t -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
  }
}

function Report-DriveUsage {
  param([string] $Drive = 'E')
  $rootPath = "$Drive" + ':\'
  $items = Get-ChildItem $rootPath -Directory -ErrorAction SilentlyContinue
  $report = foreach ($d in $items) {
    $files = Get-ChildItem $d.FullName -Recurse -File -ErrorAction SilentlyContinue
    $size = ($files | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{Name=$d.Name; GB=[Math]::Round($size/1GB,2)}
  }
  if ($report.Count -eq 0) { Write-Warning "No directories found or access denied: $rootPath"; return }
  $report | Sort-Object -Property GB -Descending | Format-Table -AutoSize
}

function Get-DriveUsage {
  param([string] $Drive = 'E')
  $rootPath = "$Drive" + ':\'
  $items = Get-ChildItem $rootPath -Directory -ErrorAction SilentlyContinue
  $report = foreach ($d in $items) {
    $files = Get-ChildItem $d.FullName -Recurse -File -ErrorAction SilentlyContinue
    $size = ($files | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{Name=$d.Name; Bytes=$size; GB=[Math]::Round($size/1GB,2)}
  }
  return ($report | Sort-Object -Property GB -Descending)
}

function Export-DriveUsage {
  param(
    [string] $Drive = 'E',
    [ValidateSet('Csv','Json')] [string] $Format = 'Csv',
    [string] $OutFile = "E:\drive_usage"
  )
  $data = Get-DriveUsage -Drive $Drive
  if (-not $data -or $data.Count -eq 0) { Write-Warning 'No data to export.'; return }
  switch ($Format) {
    'Csv'  { $path = "$OutFile.csv"; $data | Export-Csv $path -NoTypeInformation; Write-Host "Exported CSV: $path" -ForegroundColor Green }
    'Json' { $path = "$OutFile.json"; $data | ConvertTo-Json -Depth 4 | Out-File $path -Encoding UTF8; Write-Host "Exported JSON: $path" -ForegroundColor Green }
  }
}
function Export-DriveUsageHtml {
  param(
    [string] $Drive = 'E',
    [string] $OutFile = 'E:\drive_usage.html'
  )
  $data = Get-DriveUsage -Drive $Drive
  if (-not $data -or $data.Count -eq 0) { Write-Warning 'No data for HTML export.'; return }
  $rows = $data | ForEach-Object { "<tr><td>$($_.Name)</td><td>$([string]::Format('{0:N2}',$_.GB)) GB</td></tr>" }
  $html = @("<html><head><meta charset='utf-8'><title>Drive $Drive Usage</title><style>body{font-family:Segoe UI,Arial;}table{border-collapse:collapse;}td,th{border:1px solid #ccc;padding:4px 8px;}th{background:#f4f4f4;}</style></head><body>","<h2>Drive $Drive Usage Report</h2>","<table><thead><tr><th>Directory</th><th>Size</th></tr></thead><tbody>",($rows -join "`n"),"</tbody></table>","<p>Generated: $(Get-Date)</p>","</body></html>") -join "`n"
  $html | Out-File $OutFile -Encoding UTF8
  Write-Host "HTML report written: $OutFile" -ForegroundColor Green
}

function Plan-CDriveOptimization {
  @'
권장 C 드라이브 최적화 단계:
1. powercfg /h off (최대 수 GB 절약: 최대 절전 파일 삭제)
2. pagefile.sys 크기 조정 또는 E 드라이브로 이동 (고급 시스템 설정)
3. 대용량 사용자 폴더(Downloads, Videos)를 E:\Users\<계정>\ 로 이동 후 Junction 생성
   예: Move-WithJunction "C:\Users\User\Downloads" "E:\Users\User"
4. DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase (관리자 권한, WinSxS 최소화)
5. 시스템 복원 지점 정리: SystemPropertiesProtection.exe 실행 후 이전 지점 제거
6. temp, 브라우저 캐시 정리 (Clean-TempAreas 함수 활용)
7. Windows 업데이트 잔여 폴더 ($WINDOWS.~BT, $WinREAgent) 검토 후 삭제 (업데이트 완료 확인 필요)
'@
}

function Show-Plan { Plan-CDriveOptimization }

function Move-UserFolder {
  param(
    [Parameter(Mandatory)] [ValidateSet('Downloads','Documents','Pictures','Videos','Music','Desktop')] [string] $FolderName,
    [string] $User = $env:USERNAME,
    [string] $TargetRoot = 'E:\Users'
  )
  $source = "C:\Users\$User\$FolderName"
  if (-not (Test-Path $source)) { Write-Warning "Source user folder not found: $source"; return }
  $destUserRoot = Join-Path $TargetRoot $User
  if (-not (Test-Path $destUserRoot)) { New-Item -ItemType Directory -Path $destUserRoot | Out-Null }
  Move-WithJunction -Source $source -Destination $destUserRoot
}

function Disable-Hibernation {
  if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    Write-Warning 'Run PowerShell as Administrator to disable hibernation.'
    return
  }
  powercfg /h off | Out-Null
  Write-Host 'Hibernation disabled.'
}

function Cleanup-WinSxS {
  if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    Write-Warning 'Administrator required for DISM cleanup.'
    return
  }
  DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase
}

function Set-DevEnvironmentPaths {
  param(
    [string] $DevRoot = 'E:\Dev',
    [switch] $PersistUserEnv
  )
  if (-not (Test-Path $DevRoot)) { New-Item -ItemType Directory -Path $DevRoot | Out-Null }
  $paths = @(
    'E:\Portable_Python',
    'E:\Git\bin',
    'E:\Git\usr\bin',
    "$DevRoot\bin"
  ) | Where-Object { Test-Path $_ }
  $current = [Environment]::GetEnvironmentVariable('Path',[EnvironmentVariableTarget]::Process)
  foreach ($p in $paths) {
    if ($current -notlike "*${p}*") { $current = $current + ';' + $p }
  }
  [Environment]::SetEnvironmentVariable('Path',$current,[EnvironmentVariableTarget]::Process)
  if ($PersistUserEnv) {
    $userPath = [Environment]::GetEnvironmentVariable('Path',[EnvironmentVariableTarget]::User)
    foreach ($p in $paths) {
      if ($userPath -notlike "*${p}*") { $userPath = $userPath + ';' + $p }
    }
    [Environment]::SetEnvironmentVariable('Path',$userPath,[EnvironmentVariableTarget]::User)
    Write-Host 'User PATH updated.'
  }
  Write-Host 'Session PATH updated for development.'
}

function Report-LargestItems {
  param(
    [string] $Root = 'E:\',
    [int] $Top = 15
  )
  $dirs = Get-ChildItem $Root -Directory -ErrorAction SilentlyContinue
  $sizes = foreach ($d in $dirs) {
    $s = (Get-ChildItem $d.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Path=$d.FullName; GB=[Math]::Round($s/1GB,2)}
  }
  if ($sizes.Count -eq 0) { Write-Warning "No directory sizes computed for $Root"; return }
  $sizes | Sort-Object GB -Descending | Select-Object -First $Top | Format-Table -AutoSize
}

function Report-ModelCache {
  param(
    [string] $ModelsRoot = 'E:\models',
    [string] $OllamaRoot = 'E:\ollama_models'
  )
  $entries = @()
  foreach ($path in @($ModelsRoot,$OllamaRoot)) {
    if (-not (Test-Path $path)) { continue }
    $size = (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    $entries += [PSCustomObject]@{Path=$path; GB=[Math]::Round($size/1GB,2)}
  }
  if ($entries.Count -eq 0) { Write-Warning 'No model/cache paths found.'; return }
  $entries | Sort-Object GB -Descending | Format-Table -AutoSize
}
function Report-ModelCacheDetail {
  param(
    [string] $ModelsRoot = 'E:\models',
    [string] $OllamaRoot = 'E:\ollama_models',
    [int] $Top = 20
  )
  $targets = @($ModelsRoot,$OllamaRoot) | Where-Object { Test-Path $_ }
  $rows = foreach ($root in $targets) {
    Get-ChildItem $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
      $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
      [PSCustomObject]@{Root=$root; Name=$_.Name; GB=[Math]::Round($size/1GB,2); Path=$_.FullName}
    }
  }
  if (-not $rows -or $rows.Count -eq 0) { Write-Warning 'No subdirectories found.'; return }
  $rows | Sort-Object GB -Descending | Select-Object -First $Top | Format-Table -AutoSize
}

function Register-LogRotationTask {
  param(
    [string] $TaskName = 'E_LogRotation',
    [string] $ScriptPath = 'E:\organize_e_drive.ps1',
    [int] $Days = 30,
    [string] $LogRoot = 'E:\AI_body_system\logs'
  )
  if (-not (Test-Path $ScriptPath)) { Write-Warning "Script not found: $ScriptPath"; return }
  $action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -WindowStyle Hidden -Command \". '$ScriptPath'; Archive-OldLogs -Days $Days -LogRoot '$LogRoot'\""
  $trigger = New-ScheduledTaskTrigger -Daily -At 3am
  try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Description 'AI_body_system log rotation' -User $env:USERNAME -RunLevel Highest -ErrorAction Stop
    Write-Host "Scheduled Task '$TaskName' registered." -ForegroundColor Green
  } catch {
    Write-Warning "Failed to register task: $($_.Exception.Message)"
  }
}
function Get-CDriveSummary {
  $paths = @('C:\Users','C:\Windows','C:\Program Files','C:\Program Files (x86)','C:\Temp') | Where-Object { Test-Path $_ }
  $summary = foreach ($p in $paths) {
    $size = (Get-ChildItem $p -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Path=$p; GB=[Math]::Round($size/1GB,2)}
  }
  $summary | Sort-Object GB -Descending
}

function Get-CDriveUserCandidates {
  param([string] $User = $env:USERNAME)
  $root = "C:\Users\$User"
  if (-not (Test-Path $root)) { Write-Warning "User path not found: $root"; return }
  Get-ChildItem $root -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; GB=[Math]::Round($size/1GB,2); Path=$_.FullName}
  } | Sort-Object GB -Descending
}

function Suggest-CDriveMoves {
  param([string] $User = $env:USERNAME, [double] $ThresholdGB = 1)
  $list = Get-CDriveUserCandidates -User $User
  if (-not $list) { return }
  $candidates = $list | Where-Object { $_.GB -ge $ThresholdGB -and $_.Name -in @('Downloads','Videos','Pictures','Music','Documents','Desktop') }
  if ($candidates.Count -eq 0) { Write-Host 'No move candidates meet threshold.'; return }
  $candidates | Format-Table -AutoSize
  Write-Host "Use Move-UserFolder -FolderName <Name> to migrate." -ForegroundColor Yellow
}

<# 추가 실행 예시:
Disable-Hibernation
Cleanup-WinSxS
Move-UserFolder -FolderName Downloads -User $env:USERNAME
Set-DevEnvironmentPaths -PersistUserEnv
Report-LargestItems -Root 'E:\'
#>

<# 실행 예시:
New-TargetStructure
Report-DriveUsage -Drive 'E'
Archive-OldLogs -Days 30
Compress-Folder -Folder 'E:\OpenAI-export' -DestinationZip 'E:\Archive\OpenAI-export_Archive.zip'
#>

function New-SampleData {
  param(
    [string] $Target = 'E:\Data\sample',
    [int] $Files = 5,
    [int] $SizeKB = 100
  )
  if (-not (Test-Path $Target)) { New-Item -ItemType Directory -Path $Target | Out-Null }
  for ($i=1; $i -le $Files; $i++) {
    $path = Join-Path $Target "sample_$i.bin"
    $bytes = New-Object byte[] ($SizeKB * 1024)
    (New-Object System.Random).NextBytes($bytes)
    [IO.File]::WriteAllBytes($path,$bytes)
  }
  Write-Host "Sample data created in $Target ($Files files x $SizeKB KB)." -ForegroundColor Cyan
}
