[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$D82Receipt = 'artifacts/tests/c11d_d8/d8_2/d8_2_validation_receipt.json'
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Get-Location).Path
}
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot 'tools/c11d/d8') -PathType Container)) {
    throw "ProjectRoot does not look like ChallengeEngineV01_STATELESS: $ProjectRoot"
}

$EvidenceRel = 'artifacts/tests/c11d_d8/d8_3'
$EvidenceRoot = Join-Path $ProjectRoot $EvidenceRel
$ScopePath = Join-Path $ProjectRoot 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'
$D82Rel = $D82Receipt.Replace('\','/').TrimStart('./').Replace('/','\')
$D82Path = Join-Path $ProjectRoot $D82Rel
$ScopeHelper = Join-Path $ProjectRoot 'tools/c11d/d8/d8_media_scope.ps1'

function Write-Utf8NoBom([string]$Path, [string]$Text) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllText($Path, $Text, $enc)
}
function CanonicalJson($Value) {
    return ($Value | ConvertTo-Json -Depth 50 -Compress)
}
function Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Rel([string]$FullPath) {
    $r = (Resolve-Path -LiteralPath $FullPath).Path
    if ($r.StartsWith($ProjectRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $r.Substring($ProjectRoot.Length).TrimStart('\','/').Replace('\','/')
    }
    throw "Path escapes ProjectRoot: $r"
}
function IsUnderEvidence([string]$RelativePath) {
    $p = $RelativePath.Replace('\','/').TrimStart('./')
    return ($p -eq $EvidenceRel -or $p.StartsWith($EvidenceRel + '/'))
}
function Snapshot-Files {
    $items = @()
    foreach ($f in @(Get-ChildItem -LiteralPath $ProjectRoot -File -Recurse -Force)) {
        $r = Rel $f.FullName
        if (IsUnderEvidence $r) { continue }
        $items += [ordered]@{
            path = $r
            bytes = [int64]$f.Length
            last_write_utc_ticks = $f.LastWriteTimeUtc.Ticks
            sha256 = (Sha256 $f.FullName)
        }
    }
    return @($items | Sort-Object path)
}
function Compare-Snapshot($Before, $After) {
    $b = @{}
    foreach ($x in @($Before)) { $b[$x.path] = $x }
    $a = @{}
    foreach ($x in @($After)) { $a[$x.path] = $x }
    $added = @(); $removed = @(); $changed = @()
    foreach ($k in @($a.Keys)) {
        if (-not $b.ContainsKey($k)) { $added += $a[$k] }
        elseif (($a[$k].bytes -ne $b[$k].bytes) -or ($a[$k].last_write_utc_ticks -ne $b[$k].last_write_utc_ticks) -or ($a[$k].sha256 -ne $b[$k].sha256)) {
            $changed += [ordered]@{path=$k;before=$b[$k];after=$a[$k]}
        }
    }
    foreach ($k in @($b.Keys)) {
        if (-not $a.ContainsKey($k)) { $removed += $b[$k] }
    }
    return [ordered]@{
        pass = ($added.Count -eq 0 -and $removed.Count -eq 0 -and $changed.Count -eq 0)
        added = @($added | Sort-Object path)
        removed = @($removed | Sort-Object path)
        changed = @($changed | Sort-Object path)
    }
}

if (-not (Test-Path -LiteralPath $ScopePath -PathType Leaf)) { throw "Canonical D8 media scope missing: $ScopePath" }
if (-not (Test-Path -LiteralPath $D82Path -PathType Leaf)) { throw "D8.2 receipt missing: $D82Receipt" }
if (-not (Test-Path -LiteralPath $ScopeHelper -PathType Leaf)) { throw "Canonical D8 scope helper missing: $ScopeHelper" }

. $ScopeHelper
$d82 = Get-Content -LiteralPath $D82Path -Raw -Encoding UTF8 | ConvertFrom-Json
$scope = Get-Content -LiteralPath $ScopePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($d82.status -notin @('PASS','PASS_NO_MEDIA')) { throw "D8.2 is not closed successfully: $($d82.status)" }
if ($scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY') { throw "Unsupported audio QA scope mode: $($scope.scope_mode)" }

if (-not (Test-Path -LiteralPath $EvidenceRoot -PathType Container)) {
    New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null
}

$before = Snapshot-Files
$targets = @(Resolve-D8MediaScope $ProjectRoot)
$audioTargets = @($targets | Where-Object { $_.extension.ToLowerInvariant() -in @('.mp4','.mov','.mkv','.webm','.avi','.wmv','.mxf','.gif','.wav','.mp3','.m4a','.aac','.flac','.ogg','.opus','.aiff') })

$report = [ordered]@{
    contract = 'C11-D-D8.3-AUDIO-QA-REPORT-V1'
    phase = 'D8.3'
    status = if ($audioTargets.Count -eq 0) { 'PASS_NO_MEDIA' } else { 'BLOCKED' }
    scope = [ordered]@{
        declaration_path = 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'
        scope_mode = $scope.scope_mode
        registered_target_count = $targets.Count
        audio_target_count = $audioTargets.Count
        audio_targets = @($audioTargets | ForEach-Object { [ordered]@{path=$_.path;bytes=$_.bytes;extension=$_.extension.ToLowerInvariant()} })
    }
    qa_mode = 'READ_ONLY'
    ffmpeg_invoked = $false
    media_modified_by_runner = $false
    audio_quality_evaluation_performed = ($audioTargets.Count -gt 0)
    release_authority = 'NONE'
    production_execution = $false
    renderer_execution = $false
    governance = [ordered]@{
        d4_8 = 'BLOCKED'
        runtime_authority = 'NONE'
        master_seed = 'NOT_ADOPTED'
        cross_domain_seed_sharing = 'FORBIDDEN'
    }
    reason = if ($audioTargets.Count -eq 0) { $null } else { 'D8_3_AUDIO_EXECUTION_REQUIRES_EXPLICITLY_REGISTERED_MEDIA_AND_IMPLEMENTED_AUDIO_QA' }
}

Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_3_audio_qa_report.json') (CanonicalJson $report)
$after = Snapshot-Files
$mutation = Compare-Snapshot $before $after
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_3_mutation_guard.json') (CanonicalJson ([ordered]@{
    contract='C11-D-D8.3-MUTATION-GUARD-V1'
    scope='all files outside artifacts/tests/c11d_d8/d8_3/'
    result=$mutation
}))

$final = if ($mutation.pass) { $report.status } else { 'FAIL' }
$receipt = [ordered]@{
    contract='C11-D-D8.3-VALIDATION-RECEIPT-V1'
    phase='D8.3'
    status=$final
    next=if ($final -in @('PASS','PASS_NO_MEDIA')) { 'D8.4' } else { 'D8.3_REPAIR' }
    scope_sha256=(Sha256 $ScopePath)
    d82_receipt_sha256=(Sha256 $D82Path)
    audio_report_sha256=(Sha256 (Join-Path $EvidenceRoot 'd8_3_audio_qa_report.json'))
    mutation_guard_pass=$mutation.pass
    governance=$report.governance
}
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_3_validation_receipt.json') (CanonicalJson $receipt)

if (-not $mutation.pass) {
    Write-Host "D8.3 FAIL | evidence=$EvidenceRel | reasons=MUTATION_GUARD"
    exit 1
}
Write-Host "D8.3 $final | evidence=$EvidenceRel | scope_candidates=$($targets.Count) | audio_targets=$($audioTargets.Count)"
if ($final -in @('PASS','PASS_NO_MEDIA')) { exit 0 } else { exit 1 }
