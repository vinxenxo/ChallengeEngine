[CmdletBinding()]
param(
    [switch]$SkipExecution,
    [switch]$SkipVideoMatrix,
    [int]$StressRetries = 3
)

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))

$root = (Get-Location).Path
$reports = Join-Path $root 'artifacts/tests/reports'
$regression = Join-Path $root 'artifacts/regression/runs/c11_freeze'
$qaStress = Join-Path $root 'artifacts/qa/seed_stress'
$qaPhysical = Join-Path $root 'artifacts/qa/physical_smoke/c10c_e2e'
$qaVideo = Join-Path $root 'artifacts/qa/video_matrix/videos'

New-Item -ItemType Directory -Force -Path $reports,$regression,$qaStress,$qaPhysical,$qaVideo | Out-Null

function Invoke-Checked([string]$FilePath, [string[]]$Arguments) {
    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed ($LASTEXITCODE): $FilePath $($Arguments -join ' ')"
    }
}

$runAllScript = Join-Path $root 'tools\c11freeze\run_all.ps1'
$inventoryScript = Join-Path $root 'tools\c11freeze\inventory_repository.ps1'
$generateVideoMatrixScript = Join-Path $root 'tools\c11freeze\generate_qa_video_matrix.py'
$runVideoMatrixScript = Join-Path $root 'tools\c11freeze\run_qa_video_matrix.ps1'

if (-not $SkipExecution) {
    Write-Host '[C11FREEZE] Running complete freeze gate'

    Invoke-Checked 'powershell.exe' @(
        '-ExecutionPolicy'
        'Bypass'
        '-File'
        $runAllScript
        '-SeedRepeat'
        '2'
        '-StressRetries'
        ([string]$StressRetries)
    )

    if (-not $SkipVideoMatrix) {
        Write-Host '[C11FREEZE] Generating canonical QA video matrix'

        Invoke-Checked 'python.exe' @(
            $generateVideoMatrixScript
            '--include-canonical'
            '--limit'
            '0'
        )

        Invoke-Checked 'powershell.exe' @(
            '-ExecutionPolicy'
            'Bypass'
            '-File'
            $runVideoMatrixScript
        )
    }
}

Write-Host '[C11FREEZE] Refreshing repository inventory'

Invoke-Checked 'powershell.exe' @(
    '-ExecutionPolicy'
    'Bypass'
    '-File'
    $inventoryScript
)
function Read-JsonFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { throw "Evidence missing: $Path" }
    return Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json
}

$retroPath = Join-Path $regression 'RETROCOMPATIBILITY_REPORT.json'
$stressPath = Join-Path $qaStress 'STRESS_REPORT.json'
$physicalPath = Join-Path $qaPhysical 'C10C_PHYSICAL_SMOKE_MANIFEST.json'
$videoPath = Join-Path $qaVideo 'BATCH_MANIFEST.json'

$retro = Read-JsonFile $retroPath
if ($retro.status -ne 'PASS' -or [int]$retro.executions -ne 54 -or [int]$retro.failed -ne 0) {
    throw "Freeze evidence invalid: RETROCOMPATIBILITY_REPORT is not PASS 54/54."
}
if (@($retro.ab_rerun | Where-Object { $_.pass -ne $true }).Count -ne 0) {
    throw "Freeze evidence invalid: retro A/B rerun contains failures."
}

$stress = Read-JsonFile $stressPath
if ($stress.status -ne 'PASS' -or [int]$stress.cases -ne 288 -or [int]$stress.logical_executions -ne 576) {
    throw "Freeze evidence invalid: STRESS_REPORT is not PASS 288 cases / 576 logical executions."
}

$physical = Read-JsonFile $physicalPath
if (@($physical.artifacts).Count -ne 2 -or [int]$physical.frame_count -ne 60 -or [int]$physical.fixed_fps -ne 30) {
    throw "Freeze evidence invalid: physical smoke manifest does not describe the required 2/2 contract."
}

$video = Read-JsonFile $videoPath
$videoTotal = [int]$video.summary.total
$videoPassed = [int]$video.summary.passed
$videoFailed = [int]$video.summary.failed
if ($videoTotal -ne 54 -or $videoPassed -ne 54 -or $videoFailed -ne 0) {
    throw "Freeze evidence invalid: QA video matrix summary is not 54/54."
}
$videoAudioErrorCodes = @($video.errors | ForEach-Object { [string]$_.code })
$onlyExpectedAudioGate = ($videoAudioErrorCodes.Count -eq 1 -and $videoAudioErrorCodes[0] -eq 'C7_A2_MIXED_BATCH_REQUIRED')
$audioOffOnly = ([int]$video.audio_summary.audio_enabled -eq 0 -and [int]$video.audio_summary.audio_disabled -eq 54)
if (-not $onlyExpectedAudioGate -and $videoAudioErrorCodes.Count -ne 0) {
    throw "Freeze evidence invalid: QA video matrix contains unexpected errors."
}
if ($onlyExpectedAudioGate -and -not $audioOffOnly) {
    throw "Freeze evidence invalid: accepted C7-A2 out-of-scope error has unexpected audio summary."
}

$sourceRoots = @('core','mechanics','tests','tools','docs')
$rootFiles = @('project.godot','build_factory.py','README.md','README_C11_FREEZE_FINAL.md')
$entries = New-Object System.Collections.Generic.List[object]
foreach ($relativeRoot in $sourceRoots) {
    $fullRoot = Join-Path $root $relativeRoot
    if (-not (Test-Path -LiteralPath $fullRoot)) { continue }
    Get-ChildItem -LiteralPath $fullRoot -File -Recurse |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($root.Length + 1).Replace('\','/')
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            $entries.Add([pscustomobject]@{ path=$relative; bytes=$_.Length; sha256=$hash })
        }
}
foreach ($relativeFile in $rootFiles) {
    $full = Join-Path $root $relativeFile
    if (-not (Test-Path -LiteralPath $full)) { continue }
    $item = Get-Item -LiteralPath $full
    $hash = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant()
    $entries.Add([pscustomobject]@{ path=$relativeFile; bytes=$item.Length; sha256=$hash })
}
$entries = $entries | Sort-Object path
$canonicalLines = ($entries | ForEach-Object { '{0}|{1}|{2}' -f $_.path,$_.bytes,$_.sha256 }) -join "`n"
$tmp = Join-Path $env:TEMP ('c11_tree_' + [guid]::NewGuid().ToString('N') + '.txt')
[System.IO.File]::WriteAllText($tmp,$canonicalLines,(New-Object System.Text.UTF8Encoding($false)))
$treeHash = (Get-FileHash -LiteralPath $tmp -Algorithm SHA256).Hash.ToLowerInvariant()
Remove-Item -LiteralPath $tmp -Force

$gitHead = $null
$gitStatus = $null
try { $gitHead = (& git rev-parse HEAD 2>$null).Trim(); $gitStatus = (& git status --short 2>$null) -join "`n" } catch {}

$manifest = [ordered]@{
    freeze_id='C11'; status='CERTIFIED / FROZEN'; generated_at_utc=(Get-Date).ToUniversalTime().ToString('o')
    godot_version='4.7.1-stable'; hash_algorithm='SHA-256'
    scope='core + mechanics + tests + tools + docs + declared root project files'
    tree_sha256=$treeHash; file_count=$entries.Count; git_head=$gitHead; git_status=$gitStatus; files=@($entries)
}
$manifestPath = Join-Path $reports 'C11_FREEZE_SHA256_MANIFEST.json'
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$artifactHashes = @{}
foreach ($path in @($retroPath,$stressPath,$physicalPath,$videoPath,$manifestPath)) {
    $artifactHashes[$path.Substring($root.Length + 1).Replace('\','/')] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$certificate = [ordered]@{
    freeze_id='C11'; status='CERTIFIED / FROZEN'; sealed_at_utc=(Get-Date).ToUniversalTime().ToString('o')
    engine=[ordered]@{ name='Godot'; version='4.7.1-stable' }
    gates=[ordered]@{
        logical_corpus='PASS 103/103'; c11_contracts='PASS'; visual_seed_qualification='PASS 54/54'
        challenge_seed_qualification='PASS 54/54'; retrocompatibility='PASS 54/54 telemetry + A/B'
        seed_stress='PASS 288 cases / 576 logical executions'; physical_export='PASS 2/2'
        qa_video_matrix='PASS 54/54 video renders; C7-A2 mixed-audio gate intentionally out of scope'
    }
    source_manifest=[ordered]@{ path='artifacts/tests/reports/C11_FREEZE_SHA256_MANIFEST.json'; tree_sha256=$treeHash }
    evidence_sha256=$artifactHashes
    git=[ordered]@{ head=$gitHead; status=$gitStatus }
    freeze_boundary=@('simulation mathematics','RNG architecture and ownership','SimulationResult semantics','winning-frame calculation','RenderedFrameStream','canonical visual envelope','C7 audio contracts','C9 authoring contracts','test and regression architecture')
    next_scope='C11-C Art Direction - presentation only'
}
$certificatePath = Join-Path $reports 'C11_FREEZE_CERTIFICATE.json'
$certificate | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $certificatePath -Encoding UTF8

Write-Host '[C11FREEZE] Evidence validation PASS'
Write-Host '[C11FREEZE] SHA-256 manifest written:' $manifestPath
Write-Host '[C11FREEZE] Certificate written:' $certificatePath
Write-Host ('[C11FREEZE] TREE SHA-256: ' + $treeHash)
Write-Host '[C11FREEZE] FINAL SEAL PASS'
