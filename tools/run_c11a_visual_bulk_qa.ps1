$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Native command exit-code contract under StrictMode.
$global:LASTEXITCODE = 0

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

$OutputBase = Join-Path $ProjectRoot 'qa/c11a_visual_qa'
$RunsDir = Join-Path $OutputBase 'runs'
$ManifestPath = Join-Path $OutputBase 'C11_VISUAL_BULK_MANIFEST.json'

$ExpectedWidth = 540
$ExpectedHeight = 960
$ExpectedFps = '30/1'
$ExpectedFrames = 60
$ExpectedDuration = 2.0
$FrameIndices = @(0, 15, 30, 45, 59)

New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null

function Invoke-Checked {
    param(
        [Parameter(Mandatory=$true)][string]$Executable,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Write-Host "[C11A] $Label"
    $process = Start-Process -FilePath $Executable -ArgumentList $Arguments -Wait -PassThru -NoNewWindow
    if ($process.ExitCode -ne 0) {
        throw "$Label failed with exit code $($process.ExitCode)"
    }
}

function Get-FileSha256Hex {
    param([Parameter(Mandatory=$true)][string]$Path)
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Wait-ForStableFile {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Label,
        [int]$TimeoutSeconds = 90
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $lastSize = -1L
    $stableSamples = 0

    while ((Get-Date) -lt $deadline) {
        if (Test-Path -LiteralPath $Path) {
            $item = Get-Item -LiteralPath $Path
            $size = [int64]$item.Length

            if ($size -gt 0) {
                if ($size -eq $lastSize) {
                    $stableSamples++
                } else {
                    $stableSamples = 0
                    $lastSize = $size
                }

                if ($stableSamples -ge 2) {
                    return
                }
            }
        }

        Start-Sleep -Milliseconds 500
    }

    throw "$Label was not stable within ${TimeoutSeconds}s: $Path"
}

function Get-VideoProbe {
    param([Parameter(Mandatory=$true)][string]$Path)

    $json = & ffprobe -v error -select_streams v:0 `
        -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames `
        -show_entries format=duration `
        -of json $Path

    if ($LASTEXITCODE -ne 0) {
        throw "ffprobe failed for $Path"
    }

    return ($json -join "`n") | ConvertFrom-Json
}

function Assert-VideoContract {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Wait-ForStableFile -Path $Path -Label $Label

    $probe = Get-VideoProbe -Path $Path
    if ($null -eq $probe.streams -or $probe.streams.Count -lt 1) {
        throw "$Label has no video stream"
    }

    $stream = $probe.streams[0]
    $duration = [double]$probe.format.duration

    if ([int]$stream.width -ne $ExpectedWidth) { throw "$Label width expected $ExpectedWidth, got $($stream.width)" }
    if ([int]$stream.height -ne $ExpectedHeight) { throw "$Label height expected $ExpectedHeight, got $($stream.height)" }
    if ([string]$stream.r_frame_rate -ne $ExpectedFps) { throw "$Label FPS expected $ExpectedFps, got $($stream.r_frame_rate)" }
    if ([int]$stream.nb_frames -ne $ExpectedFrames) { throw "$Label frames expected $ExpectedFrames, got $($stream.nb_frames)" }
    if ([math]::Abs($duration - $ExpectedDuration) -gt 0.05) { throw "$Label duration expected ~$ExpectedDuration, got $duration" }

    return [ordered]@{
        codec = [string]$stream.codec_name
        width = [int]$stream.width
        height = [int]$stream.height
        r_frame_rate = [string]$stream.r_frame_rate
        nb_frames = [int]$stream.nb_frames
        duration_seconds = $duration
    }
}

function Invoke-EnvelopeRender {
    param(
        [Parameter(Mandatory=$true)][string]$RunId,
        [Parameter(Mandatory=$true)][string]$EnvelopeRelativePath,
        [Parameter(Mandatory=$true)][string]$AviPath
    )

    # Deliberately mirrors the already-certified C10 physical runner:
    # graphical Compatibility renderer; NO --headless for Movie Maker.
    Invoke-Checked 'godot' @(
        '--path','.',
        '--scene','core/presentation/rendering/VisualContentPlayer.tscn',
        "--definition=$EnvelopeRelativePath",
        '--write-movie', $AviPath,
        '--fixed-fps','30',
        '--quit-after','60'
    ) "Movie Maker export $RunId"
}

function Convert-Mp4 {
    param(
        [Parameter(Mandatory=$true)][string]$AviPath,
        [Parameter(Mandatory=$true)][string]$Mp4Path,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Invoke-Checked 'ffmpeg' @(
        '-y','-hide_banner','-loglevel','error',
        '-i',$AviPath,
        '-an',
        '-c:v','libx264',
        '-preset','fast',
        '-crf','23',
        '-pix_fmt','yuv420p',
        '-movflags','+faststart',
        $Mp4Path
    ) $Label

    if (-not (Test-Path -LiteralPath $Mp4Path)) {
        throw "$Label did not create $Mp4Path"
    }
}

function Write-FrameMd5 {
    param(
        [Parameter(Mandatory=$true)][string]$Mp4Path,
        [Parameter(Mandatory=$true)][string]$FrameMd5Path,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Invoke-Checked 'ffmpeg' @(
        '-y','-hide_banner','-loglevel','error',
        '-i',$Mp4Path,
        '-map','0:v:0',
        '-an',
        '-f','framemd5',
        $FrameMd5Path
    ) $Label
}

function Get-KeyFrames {
    param(
        [Parameter(Mandatory=$true)][string]$Mp4Path,
        [Parameter(Mandatory=$true)][string]$RunPath,
        [Parameter(Mandatory=$true)][string]$Label
    )

    $selectTerms = $FrameIndices | ForEach-Object { "eq(n\,$($_))" }
    $selectExpr = "select='$(($selectTerms -join '+'))'"
    Invoke-Checked 'ffmpeg' @(
        '-y','-hide_banner','-loglevel','error',
        '-i',$Mp4Path,
        '-vf',$selectExpr,
        '-fps_mode','vfr',
        (Join-Path $RunPath 'frame_%03d.png')
    ) $Label

    $frames = @(Get-ChildItem -LiteralPath $RunPath -Filter 'frame_*.png' | Sort-Object Name)
    if ($frames.Count -ne 5) {
        throw "$Label expected 5 keyframes, got $($frames.Count)"
    }

    return $frames
}

function New-ContactSheet {
    param(
        [Parameter(Mandatory=$true)][string]$RunPath,
        [Parameter(Mandatory=$true)][string]$OutputPath,
        [Parameter(Mandatory=$true)][string]$Label
    )

    $frames = @(Get-ChildItem -LiteralPath $RunPath -Filter 'frame_*.png' | Sort-Object Name)
    if ($frames.Count -ne 5) {
        throw "$Label requires exactly 5 extracted frames"
    }

    Invoke-Checked 'ffmpeg' @(
        '-y','-hide_banner','-loglevel','error',
        '-i',$frames[0].FullName,
        '-i',$frames[1].FullName,
        '-i',$frames[2].FullName,
        '-i',$frames[3].FullName,
        '-i',$frames[4].FullName,
        '-filter_complex','hstack=inputs=5',
        $OutputPath
    ) $Label
}

Write-Host '==================================================='
Write-Host '[C11A] VISUAL SEED QUALIFICATION & BULK RENDER'
Write-Host '==================================================='

# Phase 1 — envelopes.
Invoke-Checked 'godot' @(
    '--headless','--path','.',
    '-s','./tests/C11ABulkEnvelopeGenerator.gd'
) 'Envelope generation 9x6 matrix'

$Runs = @(Get-ChildItem -Path $RunsDir -Directory | Sort-Object Name)
$ExpectedRuns = 54
if ($Runs.Count -ne $ExpectedRuns) {
    throw "Expected $ExpectedRuns run directories, found $($Runs.Count)"
}

$RunDataList = New-Object System.Collections.Generic.List[object]

# Phase 2/3 — physical render + FFmpeg, intentionally serial.
$CurrentRun = 0
foreach ($Run in $Runs) {
    $CurrentRun++
    $runId = $Run.Name
    $runPath = $Run.FullName

    Write-Host "[C11A] Processing $CurrentRun/$ExpectedRuns : $runId"

    $record = [ordered]@{
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
        technical_status = 'FAIL'
        visual_review = 'PENDING'
        error = $null
    }

    try {
        $envelopePath = Join-Path $runPath 'envelope.json'
        $authoringPath = Join-Path $runPath 'authoring.json'
        $aviPath = Join-Path $runPath 'render.avi'
        $mp4Path = Join-Path $runPath 'render.mp4'
        $frameMd5Path = Join-Path $runPath 'render.framemd5'
        $contactSheetPath = Join-Path $runPath 'contact_sheet.jpg'

        foreach ($artifact in @($aviPath,$mp4Path,$frameMd5Path,$contactSheetPath)) {
            if (Test-Path -LiteralPath $artifact) { Remove-Item -Force -LiteralPath $artifact }
        }
        Get-ChildItem -LiteralPath $runPath -Filter 'frame_*.png' -ErrorAction SilentlyContinue | Remove-Item -Force

        if (-not (Test-Path -LiteralPath $envelopePath)) { throw 'Missing envelope.json' }
        if (-not (Test-Path -LiteralPath $authoringPath)) { throw 'Missing authoring.json' }

        $envData = Get-Content -Raw -LiteralPath $envelopePath | ConvertFrom-Json
        $record.route = "$($envData.kind)/$($envData.subtype)"
        $record.seed = [int]$envData.seed
        if ($runId -match '_A$') { $record.seed_role = 'A' }
        elseif ($runId -match '_B$') { $record.seed_role = 'B' }

        $record.authoring_hash = Get-FileSha256Hex -Path $authoringPath
        $record.envelope_hash = Get-FileSha256Hex -Path $envelopePath

        # Use a project-relative definition path, matching the C10 runner contract.
        $envelopeRelative = $envelopePath.Substring($ProjectRoot.Length + 1).Replace('\','/')
        Invoke-EnvelopeRender -RunId $runId -EnvelopeRelativePath $envelopeRelative -AviPath $aviPath
        [void](Assert-VideoContract -Path $aviPath -Label "AVI $runId")
        $record.avi_sha256 = Get-FileSha256Hex -Path $aviPath

        Convert-Mp4 -AviPath $aviPath -Mp4Path $mp4Path -Label "FFmpeg MP4 $runId"
        [void](Assert-VideoContract -Path $mp4Path -Label "MP4 $runId")
        $record.mp4_sha256 = Get-FileSha256Hex -Path $mp4Path

        Write-FrameMd5 -Mp4Path $mp4Path -FrameMd5Path $frameMd5Path -Label "FFmpeg frame digest $runId"
        $record.frame_digest_sha256 = Get-FileSha256Hex -Path $frameMd5Path

        [void](Get-KeyFrames -Mp4Path $mp4Path -RunPath $runPath -Label "Frame extraction $runId")
        New-ContactSheet -RunPath $runPath -OutputPath $contactSheetPath -Label "Contact sheet $runId"

        $record.technical_status = 'PASS'
    }
    catch {
        $record.error = $_.Exception.Message
        Write-Host "[C11A] FAIL $runId : $($record.error)" -ForegroundColor Red
    }

    $RunDataList.Add([pscustomobject]$record)
}

# Phase 4 — determinism gates.
$Determinism = [ordered]@{
    authoring = $true
    envelope = $true
    decoded_frames = $true
    mp4_container = $true
}

$determinismFailures = New-Object System.Collections.Generic.List[string]

foreach ($route in @($RunDataList | Select-Object -ExpandProperty route -Unique | Sort-Object)) {
    $pair = @($RunDataList | Where-Object { $_.route -eq $route -and $_.seed -eq 12345 })
    $runA = @($pair | Where-Object { $_.seed_role -eq 'A' })
    $runB = @($pair | Where-Object { $_.seed_role -eq 'B' })

    if ($runA.Count -ne 1 -or $runB.Count -ne 1) {
        $Determinism.authoring = $false
        $Determinism.envelope = $false
        $Determinism.decoded_frames = $false
        $Determinism.mp4_container = $false
        $determinismFailures.Add("Missing A/B pair for $route")
        continue
    }

    if ($runA[0].technical_status -ne 'PASS' -or $runB[0].technical_status -ne 'PASS') {
        $Determinism.authoring = $false
        $Determinism.envelope = $false
        $Determinism.decoded_frames = $false
        $Determinism.mp4_container = $false
        $determinismFailures.Add("A/B technical failure for $route")
        continue
    }

    if ($runA[0].authoring_hash -ne $runB[0].authoring_hash) {
        $Determinism.authoring = $false
        $determinismFailures.Add("Authoring mismatch for $route")
    }
    if ($runA[0].envelope_hash -ne $runB[0].envelope_hash) {
        $Determinism.envelope = $false
        $determinismFailures.Add("Envelope mismatch for $route")
    }
    if ($runA[0].frame_digest_sha256 -ne $runB[0].frame_digest_sha256) {
        $Determinism.decoded_frames = $false
        $determinismFailures.Add("Decoded-frame digest mismatch for $route")
    }
    if ($runA[0].mp4_sha256 -ne $runB[0].mp4_sha256) {
        $Determinism.mp4_container = $false
        # Container hash is evidence, but is not the definition of visual determinism.
        Write-Host "[C11A] NOTICE: MP4 container hash differs for $route; visual digest matched/checked." -ForegroundColor Yellow
    }
}

$TechnicalPass = @($RunDataList | Where-Object { $_.technical_status -eq 'PASS' }).Count
$TechnicalFail = $ExpectedRuns - $TechnicalPass
$DeterminismAbPass = $Determinism.authoring -and $Determinism.envelope -and $Determinism.decoded_frames

$Manifest = [pscustomobject]@{
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
        technical_pass = $TechnicalPass
        technical_fail = $TechnicalFail
        determinism_ab_pass = $DeterminismAbPass
    }
    determinism = [pscustomobject]@{
        authoring = [bool]$Determinism.authoring
        envelope = [bool]$Determinism.envelope
        decoded_frames = [bool]$Determinism.decoded_frames
        mp4_container = [bool]$Determinism.mp4_container
    }
    determinism_failures = @($determinismFailures)
    runs = @($RunDataList)
}

$Manifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

if ($TechnicalPass -ne $ExpectedRuns -or -not $DeterminismAbPass) {
    Write-Host "[C11A] FAIL — technical=$TechnicalPass/$ExpectedRuns, determinism_ab_pass=$DeterminismAbPass" -ForegroundColor Red
    exit 1
}

Write-Host "[C11A] PASS — 54/54 technical runs and A/B visual determinism verified." -ForegroundColor Green
exit 0
