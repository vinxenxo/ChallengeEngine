$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Native command exit-code contract: initialize the automatic variable for StrictMode.
$global:LASTEXITCODE = 0

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

$OutputRoot = Join-Path $ProjectRoot 'artifacts/qa/physical_smoke/c10c_e2e'
$DefinitionRoot = Join-Path $OutputRoot 'definitions'
$AviRoot = Join-Path $OutputRoot 'avi'
$Mp4Root = Join-Path $OutputRoot 'mp4'
$ManifestPath = Join-Path $OutputRoot 'C10C_PHYSICAL_SMOKE_MANIFEST.json'

New-Item -ItemType Directory -Force -Path $DefinitionRoot, $AviRoot, $Mp4Root | Out-Null

function Invoke-Checked {
    param(
        [Parameter(Mandatory=$true)][string]$Executable,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Write-Host "[C10C] $Label"
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

function Get-FileSha256Hex {
    param([Parameter(Mandatory=$true)][string]$Path)
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Read-AviProbe {
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

function Wait-ForAviReady {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Label,
        [int]$TimeoutSeconds = 60
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
                    $stableSamples += 1
                } else {
                    $stableSamples = 0
                    $lastSize = $size
                }

                # Require two consecutive identical non-zero samples so the
                # subsequent ffprobe does not race Movie Maker finalization.
                if ($stableSamples -ge 2) {
                    return
                }
            }
        }

        Start-Sleep -Milliseconds 500
    }

    throw "${Label}: AVI was not ready within ${TimeoutSeconds}s: $Path"
}

function Assert-AviContract {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Wait-ForAviReady -Path $Path -Label $Label

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "${Label}: AVI does not exist: $Path"
    }

    $item = Get-Item -LiteralPath $Path
    if ($item.Length -le 0) {
        throw "${Label}: AVI is zero bytes: $Path"
    }

    $probe = Read-AviProbe -Path $Path
    $stream = $probe.streams[0]
    $duration = [double]$probe.format.duration

    if ([int]$stream.width -ne 540) { throw "${Label}: expected width 540, got $($stream.width)" }
    if ([int]$stream.height -ne 960) { throw "${Label}: expected height 960, got $($stream.height)" }
    if ([string]$stream.r_frame_rate -ne '30/1') { throw "${Label}: expected 30/1 FPS, got $($stream.r_frame_rate)" }
    if ([int]$stream.nb_frames -ne 60) { throw "${Label}: expected 60 frames, got $($stream.nb_frames)" }
    if ([math]::Abs($duration - 2.0) -gt 0.05) { throw "${Label}: expected ~2.0s duration, got $duration" }

    return [ordered]@{
        path = $Path
        bytes = [int64]$item.Length
        sha256 = Get-FileSha256Hex -Path $Path
        codec = [string]$stream.codec_name
        width = [int]$stream.width
        height = [int]$stream.height
        r_frame_rate = [string]$stream.r_frame_rate
        nb_frames = [int]$stream.nb_frames
        duration_seconds = $duration
    }
}

function Encode-Mp4 {
    param(
        [Parameter(Mandatory=$true)][string]$Avi,
        [Parameter(Mandatory=$true)][string]$Mp4,
        [Parameter(Mandatory=$true)][string]$Label
    )

    Write-Host "[C10C] $Label"
    & ffmpeg -y -v error -i $Avi -an -c:v libx264 -pix_fmt yuv420p -movflags +faststart $Mp4
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
    if (-not (Test-Path -LiteralPath $Mp4)) {
        throw "$Label did not create $Mp4"
    }
    if ((Get-Item -LiteralPath $Mp4).Length -le 0) {
        throw "$Label created a zero-byte MP4"
    }
}

Invoke-Checked 'godot' @('--headless','--path','.', '-s','./tests/C10CPreparePhysicalFixtures.gd') 'Preparing representative generated envelopes'

$Jobs = @(
    [ordered]@{
        Kind = 'visual_loop'
        Subtype = 'fractal'
        Definition = (Join-Path $DefinitionRoot 'c10c_visual_loop_fractal.json')
        Avi = (Join-Path $AviRoot 'c10c_visual_loop_fractal.avi')
        Mp4 = (Join-Path $Mp4Root 'c10c_visual_loop_fractal.mp4')
    },
    [ordered]@{
        Kind = 'visual_drill'
        Subtype = 'tracking'
        Definition = (Join-Path $DefinitionRoot 'c10c_visual_drill_tracking.json')
        Avi = (Join-Path $AviRoot 'c10c_visual_drill_tracking.avi')
        Mp4 = (Join-Path $Mp4Root 'c10c_visual_drill_tracking.mp4')
    }
)

$Artifacts = @()

foreach ($job in $Jobs) {
    if (Test-Path -LiteralPath $job.Avi) { Remove-Item -Force -LiteralPath $job.Avi }
    if (Test-Path -LiteralPath $job.Mp4) { Remove-Item -Force -LiteralPath $job.Mp4 }

    Invoke-Checked 'godot' @(
        '--path','.',
        '--scene','core/presentation/rendering/VisualContentPlayer.tscn',
        "--definition=$($job.Definition.Replace($ProjectRoot + '\','').Replace('\','/'))",
        '--write-movie', $job.Avi,
        '--fixed-fps','30',
        '--quit-after','60',
        '--','--qa-mode'
    ) "Physical Movie Maker export $($job.Kind)/$($job.Subtype)"

    $aviArtifact = Assert-AviContract -Path $job.Avi -Label "$($job.Kind)/$($job.Subtype)"
    Encode-Mp4 -Avi $job.Avi -Mp4 $job.Mp4 -Label "FFmpeg packaging $($job.Kind)/$($job.Subtype)"

    $mp4Hash = Get-FileSha256Hex -Path $job.Mp4
    $mp4Size = (Get-Item -LiteralPath $job.Mp4).Length

    $Artifacts += [ordered]@{
        kind = $job.Kind
        subtype = $job.Subtype
        definition = $job.Definition
        raw_video = $aviArtifact
        final_video = [ordered]@{
            path = $job.Mp4
            bytes = [int64]$mp4Size
            sha256 = $mp4Hash
        }
    }
}

$manifest = [ordered]@{
    test = 'C10-C'
    scope = 'authoring_to_runtime_to_physical_smoke'
    production_manifest = $false
    godot_command_scene = 'core/presentation/rendering/VisualContentPlayer.tscn'
    fixed_fps = 30
    frame_count = 60
    duration_seconds = 2.0
    artifacts = $Artifacts
}

$manifest | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
Write-Host '[C10C] Physical smoke manifest written:' $ManifestPath
Write-Host '[C10C_PHYSICAL_EXPORT_SMOKE] PASS — 2/2'
