$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$global:LASTEXITCODE = 0

$ProjectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)))
Set-Location $ProjectRoot

$OutputBase = Join-Path $ProjectRoot 'artifacts/qa/c11a_visual'
$RunsDir = Join-Path $OutputBase 'runs'
$ManifestPath = Join-Path $OutputBase 'C11_VISUAL_BULK_MANIFEST.json'

$ExpectedRuns = 54
$ExpectedWidth = 540
$ExpectedHeight = 960
$ExpectedFps = '30/1'
$ExpectedFrames = 60
$ExpectedDuration = 2.0

function Get-FileSha256Hex {
    param([Parameter(Mandatory=$true)][string]$Path)
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Invoke-FfprobeJson {
    param([Parameter(Mandatory=$true)][string]$Path)
    $lines = & ffprobe -v error -select_streams v:0 `
        -count_frames `
        -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames `
        -show_entries format=duration `
        -of json -- $Path
    if ($LASTEXITCODE -ne 0) {
        throw "ffprobe failed: $Path"
    }
    return ($lines -join "`n") | ConvertFrom-Json
}

function Test-VideoContract {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $false }
    $probe = Invoke-FfprobeJson -Path $Path
    if ($null -eq $probe.streams -or @($probe.streams).Count -lt 1) { return $false }
    $s = $probe.streams[0]
    $duration = [double]$probe.format.duration
    $frames = [int]$s.nb_read_frames
    return (
        [int]$s.width -eq $ExpectedWidth -and
        [int]$s.height -eq $ExpectedHeight -and
        [string]$s.r_frame_rate -eq $ExpectedFps -and
        $frames -eq $ExpectedFrames -and
        [math]::Abs($duration - $ExpectedDuration) -le 0.05
    )
}

Write-Host '[C11A] Finalizing existing bulk QA artifacts (no re-rendering).'
if (-not (Test-Path -LiteralPath $RunsDir)) {
    throw "Runs directory not found: $RunsDir"
}

$runs = @(Get-ChildItem -LiteralPath $RunsDir -Directory | Sort-Object Name)
if ($runs.Count -ne $ExpectedRuns) {
    throw "Expected $ExpectedRuns run directories, found $($runs.Count)"
}

$records = @()
$technicalFail = 0

foreach ($run in $runs) {
    $runId = $run.Name
    $runPath = $run.FullName
    $authoringPath = Join-Path $runPath 'authoring.json'
    $envelopePath = Join-Path $runPath 'envelope.json'
    $aviPath = Join-Path $runPath 'render.avi'
    $mp4Path = Join-Path $runPath 'render.mp4'
    $frameMd5Path = Join-Path $runPath 'render.framemd5'
    $frames = @(Get-ChildItem -LiteralPath $runPath -Filter 'frame_*.png' -ErrorAction SilentlyContinue | Sort-Object Name)
    $contactSheet = Join-Path $runPath 'contact_sheet.jpg'

    $status = 'PASS'
    try {
        foreach ($p in @($authoringPath, $envelopePath, $aviPath, $mp4Path, $frameMd5Path, $contactSheet)) {
            if (-not (Test-Path -LiteralPath $p)) { throw "Missing artifact: $p" }
        }
        if ($frames.Count -ne 5) { throw "Expected 5 keyframes, found $($frames.Count)" }

        $env = Get-Content -Raw -LiteralPath $envelopePath | ConvertFrom-Json
        $recordRoute = "$($env.kind)/$($env.subtype)"
        if (-not (Test-VideoContract -Path $aviPath)) { throw 'AVI video contract failed' }
        if (-not (Test-VideoContract -Path $mp4Path)) { throw 'MP4 video contract failed' }

        $seedRole = 'NONE'
        if ($runId -match '_A$') { $seedRole = 'A' }
        elseif ($runId -match '_B$') { $seedRole = 'B' }

        $records += [pscustomobject]@{
            run_id = $runId
            route = $recordRoute
            seed = [int]$env.seed
            seed_role = $seedRole
            tier = 2
            authoring_hash = Get-FileSha256Hex -Path $authoringPath
            envelope_hash = Get-FileSha256Hex -Path $envelopePath
            avi_sha256 = Get-FileSha256Hex -Path $aviPath
            mp4_sha256 = Get-FileSha256Hex -Path $mp4Path
            frame_digest_sha256 = Get-FileSha256Hex -Path $frameMd5Path
            technical_status = 'PASS'
            visual_review = 'PENDING'
            'error' = $null
        }
    }
    catch {
        $status = 'FAIL'
        $technicalFail++
        $records += [pscustomobject]@{
            run_id = $runId
            route = $null
            seed = $null
            seed_role = 'NONE'
            tier = 2
            authoring_hash = $null
            envelope_hash = $null
            avi_sha256 = $null
            mp4_sha256 = $null
            frame_digest_sha256 = $null
            technical_status = $status
            visual_review = 'PENDING'
            'error' = $_.Exception.Message
        }
    }
}

$determinismFailures = @()
$authoringPass = $true
$envelopePass = $true
$framePass = $true
$containerPass = $true

foreach ($route in @($records | Where-Object { $_.route } | Select-Object -ExpandProperty route -Unique | Sort-Object)) {
    $a = @($records | Where-Object { $_.route -eq $route -and $_.seed -eq 12345 -and $_.seed_role -eq 'A' })
    $b = @($records | Where-Object { $_.route -eq $route -and $_.seed -eq 12345 -and $_.seed_role -eq 'B' })
    if ($a.Count -ne 1 -or $b.Count -ne 1) {
        $authoringPass = $false; $envelopePass = $false; $framePass = $false; $containerPass = $false
        $determinismFailures += "Missing A/B pair for $route"
        continue
    }
    if ($a[0].technical_status -ne 'PASS' -or $b[0].technical_status -ne 'PASS') {
        $authoringPass = $false; $envelopePass = $false; $framePass = $false; $containerPass = $false
        $determinismFailures += "A/B technical failure for $route"
        continue
    }
    if ($a[0].authoring_hash -ne $b[0].authoring_hash) { $authoringPass = $false; $determinismFailures += "Authoring mismatch for $route" }
    if ($a[0].envelope_hash -ne $b[0].envelope_hash) { $envelopePass = $false; $determinismFailures += "Envelope mismatch for $route" }
    if ($a[0].frame_digest_sha256 -ne $b[0].frame_digest_sha256) { $framePass = $false; $determinismFailures += "Decoded-frame digest mismatch for $route" }
    if ($a[0].mp4_sha256 -ne $b[0].mp4_sha256) { $containerPass = $false }
}

$technicalPass = @($records | Where-Object { $_.technical_status -eq 'PASS' }).Count
$determinismPass = $authoringPass -and $envelopePass -and $framePass

$manifest = [pscustomobject]@{
    qa_batch_id = 'C11A_VISUAL_SEED_QUALIFICATION'
    timestamp_utc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    contract = [pscustomobject]@{
        tier = 2
        duration_seconds = 2.0
        fps = 30
        frame_count = 60
        resolution = [pscustomobject]@{ width = 540; height = 960 }
        route_count = 9
        seed_count = 6
    }
    total_runs = $ExpectedRuns
    summary = [pscustomobject]@{
        technical_pass = $technicalPass
        technical_fail = ($ExpectedRuns - $technicalPass)
        determinism_ab_pass = $determinismPass
    }
    determinism = [pscustomobject]@{
        authoring = $authoringPass
        envelope = $envelopePass
        decoded_frames = $framePass
        mp4_container = $containerPass
    }
    determinism_failures = @($determinismFailures)
    runs = @($records)
}

$manifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host "[C11A] Manifest finalized: technical=$technicalPass/$ExpectedRuns, determinism_ab_pass=$determinismPass"
if ($technicalPass -ne $ExpectedRuns -or -not $determinismPass) {
    exit 1
}
exit 0
