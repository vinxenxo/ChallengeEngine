[CmdletBinding()]
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputRoot = ""
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $ProjectRoot 'qa/c11a1_challenge_qa'
} elseif (-not [IO.Path]::IsPathRooted($OutputRoot)) {
    $OutputRoot = Join-Path $ProjectRoot $OutputRoot
}

$ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot)
$OutputRoot = [IO.Path]::GetFullPath($OutputRoot)
$runsRoot = Join-Path $OutputRoot 'runs'
$manifestPath = Join-Path $OutputRoot 'C11A1_CHALLENGE_BULK_MANIFEST.json'

if (-not (Test-Path -LiteralPath $runsRoot -PathType Container)) {
    throw "C11A.1 finalizer: no existe $runsRoot"
}

function Get-CanonicalJson {
    param([object]$Value)
    return ($Value | ConvertTo-Json -Depth 100 -Compress)
}

function Write-JsonUtf8 {
    param([string]$Path, [object]$Value)
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 100), [Text.UTF8Encoding]::new($false))
}

function Get-Sha256 {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Get-TextSha256 {
    param([string]$Path)
    $hash = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [IO.File]::ReadAllBytes($Path)
        return ([BitConverter]::ToString($hash.ComputeHash($bytes)).Replace('-', '')).ToLowerInvariant()
    } finally { $hash.Dispose() }
}

function Get-DeterminismTelemetry {
    param([object]$Telemetry)
    return [ordered]@{
        initial_seed = [int64]$Telemetry.initial_seed
        final_seed = [int64]$Telemetry.final_seed
        seed_used = [int64]$Telemetry.seed_used
        attempts = [int]$Telemetry.attempts
        rng_version = [string]$Telemetry.rng_version
        winning_frame_game = [int]$Telemetry.winning_frame_game
        winning_frame = [int]$Telemetry.winning_frame
        total_frames = [int]$Telemetry.total_frames
        hook_frames = [int]$Telemetry.hook_frames
        game_frames = [int]$Telemetry.game_frames
        reveal_frames = [int]$Telemetry.reveal_frames
        cta_frames = [int]$Telemetry.cta_frames
        minimum_distance = [double]$Telemetry.minimum_distance
        score = [double]$Telemetry.score
        close_calls = [int]$Telemetry.close_calls
        winning_frame_in_valid_window = [bool]$Telemetry.winning_frame_in_valid_window
    }
}

function Read-Run {
    param([string]$RunDir)
    $recordPath = Join-Path $RunDir 'run_record.json'
    if (-not (Test-Path -LiteralPath $recordPath -PathType Leaf)) {
        return [pscustomobject]@{ valid = $false; error = 'run_record.json missing'; run_dir = $RunDir }
    }

    $record = Get-Content -LiteralPath $recordPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($record.status -ne 'COMPLETE') {
        return [pscustomobject]@{ valid = $false; error = "run status=$($record.status)"; run_dir = $RunDir }
    }

    $factoryManifestPath = [string]$record.factory_manifest
    if (-not (Test-Path -LiteralPath $factoryManifestPath -PathType Leaf)) {
        return [pscustomobject]@{ valid = $false; error = 'factory manifest missing'; run_dir = $RunDir }
    }

    $factoryManifest = Get-Content -LiteralPath $factoryManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($factoryManifest.status -ne 'PASS') {
        return [pscustomobject]@{ valid = $false; error = 'factory manifest status != PASS'; run_dir = $RunDir }
    }

    $telemetry = $factoryManifest.telemetry
    if ($null -eq $telemetry) {
        return [pscustomobject]@{ valid = $false; error = 'telemetry missing'; run_dir = $RunDir }
    }

    $framemd5Path = Join-Path $RunDir 'render.framemd5'
    if (-not (Test-Path -LiteralPath $framemd5Path -PathType Leaf)) {
        return [pscustomobject]@{ valid = $false; error = 'framemd5 missing'; run_dir = $RunDir }
    }

    $mp4 = [string]$record.video.mp4
    $avi = [string]$record.video.avi
    if (-not (Test-Path -LiteralPath $mp4 -PathType Leaf)) { return [pscustomobject]@{ valid = $false; error = 'MP4 missing'; run_dir = $RunDir } }
    if (-not (Test-Path -LiteralPath $avi -PathType Leaf)) { return [pscustomobject]@{ valid = $false; error = 'AVI missing'; run_dir = $RunDir } }

    $frameDir = Join-Path $RunDir 'frames'
    $frameCount = @(Get-ChildItem -LiteralPath $frameDir -Filter 'frame_*.png' -ErrorAction SilentlyContinue).Count
    if ($frameCount -lt 5) { return [pscustomobject]@{ valid = $false; error = "review keyframes=$frameCount < 5"; run_dir = $RunDir } }
    if (-not (Test-Path -LiteralPath (Join-Path $RunDir 'contact_sheet.jpg') -PathType Leaf)) { return [pscustomobject]@{ valid = $false; error = 'contact sheet missing'; run_dir = $RunDir } }

    return [pscustomobject]@{
        valid = $true
        run_dir = $RunDir
        record = $record
        factory_manifest = $factoryManifest
        telemetry = $telemetry
        framemd5_path = $framemd5Path
        framemd5_sha256 = Get-Sha256 $framemd5Path
        mp4_sha256 = Get-Sha256 $mp4
        avi_sha256 = Get-Sha256 $avi
        mp4 = $mp4
        avi = $avi
        frame_count = $frameCount
    }
}

$runDirs = @(Get-ChildItem -LiteralPath $runsRoot -Directory | Sort-Object Name)
Write-Host "[C11A1] Finalizing existing Challenge QA artifacts (no re-rendering)." -ForegroundColor Cyan
Write-Host "[C11A1] Runs found: $($runDirs.Count)"

$expectedRuns = 54
if ($runDirs.Count -ne $expectedRuns) {
    throw "C11A.1 finalizer: expected $expectedRuns run directories, found $($runDirs.Count)."
}

$expectedLabels = @('12345_A','54321','314159','7770001','998877','12345_B')
$coverageFailures = @()
foreach ($challengeNumber in 1..9) {
    $challengeId = "CHALLENGE_{0:D3}" -f $challengeNumber
    $challengeDirs = @($runDirs | Where-Object { $_.Name -like ("{0}_seed_*" -f $challengeId.ToLowerInvariant()) })
    if ($challengeDirs.Count -ne 6) {
        $coverageFailures += "$challengeId expected 6 runs, found $($challengeDirs.Count)"
        continue
    }
    foreach ($label in $expectedLabels) {
        $expectedName = "{0}_seed_{1}" -f $challengeId.ToLowerInvariant(), $label
        if (-not ($challengeDirs.Name -contains $expectedName)) {
            $coverageFailures += "missing $expectedName"
        }
    }
}
if ($coverageFailures.Count -gt 0) {
    $coverageFailures | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    throw 'C11A.1 finalizer: matrix coverage gate FAILED.'
}

$items = @()
$technicalFailures = @()

foreach ($runDir in $runDirs) {
    $run = Read-Run -RunDir $runDir.FullName
    if (-not $run.valid) {
        $technicalFailures += [pscustomobject]@{
            run_id = $runDir.Name
            error = $run.error
        }
        continue
    }

    $record = $run.record
    $telemetry = $run.telemetry
    $expected = $record.expected_timeline

    if ([int]$record.test_seed -ne [int64]$telemetry.initial_seed) {
        $technicalFailures += [pscustomobject]@{ run_id=$runDir.Name; error='initial_seed != QA test_seed' }
        continue
    }
    if ([string]$record.rng_version -ne [string]$telemetry.rng_version) {
        $technicalFailures += [pscustomobject]@{ run_id=$runDir.Name; error='rng_version mismatch' }
        continue
    }
    if ([int]$telemetry.total_frames -ne [int]$expected.total_frames) {
        $technicalFailures += [pscustomobject]@{ run_id=$runDir.Name; error='telemetry total_frames != expected timeline' }
        continue
    }
    $sumFrames = [int]$telemetry.hook_frames + [int]$telemetry.game_frames + [int]$telemetry.reveal_frames + [int]$telemetry.cta_frames
    if ([int]$telemetry.total_frames -ne $sumFrames) {
        $technicalFailures += [pscustomobject]@{ run_id=$runDir.Name; error='telemetry timeline sum mismatch' }
        continue
    }
    if (-not [bool]$telemetry.winning_frame_in_valid_window) {
        $technicalFailures += [pscustomobject]@{ run_id=$runDir.Name; error='winning_frame_in_valid_window=false' }
        continue
    }
    if ([int]$telemetry.winning_frame -lt 0 -or [int]$telemetry.winning_frame -ge [int]$telemetry.total_frames) {
        $technicalFailures += [pscustomobject]@{ run_id=$runDir.Name; error='winning_frame outside video' }
        continue
    }

    $artifact = [ordered]@{
        run_id = $runDir.Name
        challenge_id = [string]$record.challenge_id
        mechanic = [string]$record.mechanic
        mechanic_version = $record.mechanic_version
        seed_label = [string]$record.seed_label
        source_seed = [int64]$record.source_seed
        test_seed = [int64]$record.test_seed
        rng_version = [string]$telemetry.rng_version
        attempts = [int]$telemetry.attempts
        retries_used = [Math]::Max(0, ([int]$telemetry.attempts - 1))
        initial_seed = [int64]$telemetry.initial_seed
        final_seed = [int64]$telemetry.final_seed
        seed_used = [int64]$telemetry.seed_used
        winning_frame_game = [int]$telemetry.winning_frame_game
        winning_frame = [int]$telemetry.winning_frame
        winning_frame_in_valid_window = [bool]$telemetry.winning_frame_in_valid_window
        total_frames = [int]$telemetry.total_frames
        hook_frames = [int]$telemetry.hook_frames
        game_frames = [int]$telemetry.game_frames
        reveal_frames = [int]$telemetry.reveal_frames
        cta_frames = [int]$telemetry.cta_frames
        minimum_distance = [double]$telemetry.minimum_distance
        score = [double]$telemetry.score
        close_calls = [int]$telemetry.close_calls
        mp4_sha256 = $run.mp4_sha256
        avi_sha256 = $run.avi_sha256
        framemd5_sha256 = $run.framemd5_sha256
        simulation_pass = $true
    }
    $items += [pscustomobject]$artifact
}

if ($technicalFailures.Count -gt 0) {
    Write-Host "[C11A1] TECHNICAL FAILURES: $($technicalFailures.Count)" -ForegroundColor Red
    foreach ($failure in $technicalFailures) { Write-Host " - $($failure.run_id): $($failure.error)" -ForegroundColor Red }
    throw 'C11A.1 technical gate FAILED.'
}

$byChallenge = @{}
foreach ($item in $items) {
    if (-not $byChallenge.ContainsKey($item.challenge_id)) { $byChallenge[$item.challenge_id] = @() }
    $byChallenge[$item.challenge_id] += $item
}

$abResults = @()
$determinismPass = $true
foreach ($challengeId in ($byChallenge.Keys | Sort-Object)) {
    $runs = @($byChallenge[$challengeId])
    $a = $runs | Where-Object { $_.seed_label -eq '12345_A' }
    $b = $runs | Where-Object { $_.seed_label -eq '12345_B' }
    if ($null -eq $a -or $null -eq $b) {
        $determinismPass = $false
        $abResults += [pscustomobject]@{ challenge_id=$challengeId; pass=$false; error='missing A/B pair' }
        continue
    }

    $telemetryA = $items | Where-Object { $_.run_id -eq $a.run_id } | Select-Object -First 1
    $telemetryB = $items | Where-Object { $_.run_id -eq $b.run_id } | Select-Object -First 1
    $metaA = [ordered]@{
        challenge_id=$a.challenge_id; mechanic=$a.mechanic; mechanic_version=$a.mechanic_version; rng_version=$a.rng_version
        initial_seed=$a.initial_seed; final_seed=$a.final_seed; seed_used=$a.seed_used; attempts=$a.attempts; retries_used=$a.retries_used
        winning_frame_game=$a.winning_frame_game; winning_frame=$a.winning_frame; total_frames=$a.total_frames
        hook_frames=$a.hook_frames; game_frames=$a.game_frames; reveal_frames=$a.reveal_frames; cta_frames=$a.cta_frames
        minimum_distance=$a.minimum_distance; score=$a.score; close_calls=$a.close_calls
        winning_frame_in_valid_window=$a.winning_frame_in_valid_window
    }
    $metaB = [ordered]@{
        challenge_id=$b.challenge_id; mechanic=$b.mechanic; mechanic_version=$b.mechanic_version; rng_version=$b.rng_version
        initial_seed=$b.initial_seed; final_seed=$b.final_seed; seed_used=$b.seed_used; attempts=$b.attempts; retries_used=$b.retries_used
        winning_frame_game=$b.winning_frame_game; winning_frame=$b.winning_frame; total_frames=$b.total_frames
        hook_frames=$b.hook_frames; game_frames=$b.game_frames; reveal_frames=$b.reveal_frames; cta_frames=$b.cta_frames
        minimum_distance=$b.minimum_distance; score=$b.score; close_calls=$b.close_calls
        winning_frame_in_valid_window=$b.winning_frame_in_valid_window
    }

    $authoringPass = (
        $a.challenge_id -eq $b.challenge_id -and
        $a.mechanic -eq $b.mechanic -and
        [string]$a.mechanic_version -eq [string]$b.mechanic_version -and
        $a.rng_version -eq $b.rng_version -and
        $a.test_seed -eq $b.test_seed
    )
    $metadataPass = ((Get-CanonicalJson $metaA) -eq (Get-CanonicalJson $metaB))
    $md5A = Get-Content -LiteralPath (Join-Path (Join-Path $runsRoot $a.run_id) 'render.framemd5') -Raw -Encoding UTF8
    $md5B = Get-Content -LiteralPath (Join-Path (Join-Path $runsRoot $b.run_id) 'render.framemd5') -Raw -Encoding UTF8
    $frameDigestPass = ($md5A -eq $md5B)
    $mp4ContainerEqual = ($a.mp4_sha256 -eq $b.mp4_sha256)
    $pass = $authoringPass -and $metadataPass -and $frameDigestPass

    if (-not $pass) { $determinismPass = $false }
    $abResults += [pscustomobject]@{
        challenge_id = $challengeId
        pass = $pass
        authoring_equivalence = $authoringPass
        simulation_metadata_equivalence = $metadataPass
        frame_digest_equivalence = $frameDigestPass
        mp4_container_sha256_equal = $mp4ContainerEqual
        run_a = $a.run_id
        run_b = $b.run_id
        mp4_sha256_a = $a.mp4_sha256
        mp4_sha256_b = $b.mp4_sha256
    }
}

$challengeSummary = @()
foreach ($challengeId in ($byChallenge.Keys | Sort-Object)) {
    $runs = @($byChallenge[$challengeId])
    $challengeSummary += [pscustomobject]@{
        challenge_id = $challengeId
        executions = $runs.Count
        simulation_pass = ($runs | Where-Object { $_.simulation_pass }).Count -eq 6
        rng_versions = @($runs.rng_version | Sort-Object -Unique)
        mechanics = @($runs.mechanic | Sort-Object -Unique)
        attempts_min = ($runs.attempts | Measure-Object -Minimum).Minimum
        attempts_max = ($runs.attempts | Measure-Object -Maximum).Maximum
        winning_frame_min = ($runs.winning_frame | Measure-Object -Minimum).Minimum
        winning_frame_max = ($runs.winning_frame | Measure-Object -Maximum).Maximum
        final_seed_changed_runs = @($runs | Where-Object { $_.final_seed -ne $_.initial_seed }).Count
    }
}

$manifest = [ordered]@{
    manifest_version = '1.0'
    qa_id = 'C11A.1'
    status = if ($determinismPass) { 'PASS' } else { 'FAIL' }
    frozen_c11a_reference = 'C11-A Visual Seed Qualification certified before this phase'
    no_core_mutation = $true
    matrix = [ordered]@{
        challenges = 9
        seeds_per_challenge = 6
        total_executions = 54
        seed_cases = @('12345_A','54321','314159','7770001','998877','12345_B')
    }
    gates = [ordered]@{
        technical_executions = $items.Count
        technical_pass = ($technicalFailures.Count -eq 0 -and $items.Count -eq 54)
        simulation_pass = ($items | Where-Object { $_.simulation_pass }).Count -eq 54
        determinism_ab_pass = $determinismPass
        mp4_container_hash_is_not_determinism_gate = $true
    }
    challenge_summary = $challengeSummary
    determinism_ab = $abResults
    executions = $items
    finalized_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
}

Write-JsonUtf8 $manifestPath $manifest

if (-not $determinismPass) {
    throw "C11A.1 determinism A/B gate FAILED. Manifest written: $manifestPath"
}

Write-Host "[C11A1] Manifest finalized: technical=$($items.Count)/54, determinism_ab_pass=True" -ForegroundColor Green
Write-Host "[C11A1] Manifest: $manifestPath"
