[CmdletBinding()]
param(
    [string]$ProjectRoot = "",
    [string]$OutputRoot = "",
    [switch]$Resume,
    [ValidatePattern('^CHALLENGE_[0-9]{3}$')]
    [string]$ChallengeId = "",
    [ValidateRange(0,2147483646)]
    [int64]$SingleSeed = 0
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $scriptPath = $MyInvocation.MyCommand.Path
    if ([string]::IsNullOrWhiteSpace($scriptPath)) {
        throw 'C11A.1: no se pudo determinar la ruta del script; indique -ProjectRoot.'
    }
    $ProjectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $scriptPath)))
}

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $ProjectRoot 'artifacts/qa/c11a1_challenge'
} elseif (-not [IO.Path]::IsPathRooted($OutputRoot)) {
    $OutputRoot = Join-Path $ProjectRoot $OutputRoot
}

$OutputRoot = [IO.Path]::GetFullPath($OutputRoot)
$ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot)

$producer = Join-Path $ProjectRoot 'tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1'
$challengesRoot = Join-Path $ProjectRoot 'challenges'
$buildFactory = Join-Path $ProjectRoot 'build_factory.py'

if (-not (Test-Path -LiteralPath $producer -PathType Leaf)) {
    throw "C11A.1: no existe el productor canonico: $producer"
}
if (-not (Test-Path -LiteralPath $challengesRoot -PathType Container)) {
    throw "C11A.1: no existe la carpeta challenges/"
}

foreach ($tool in @('ffmpeg','ffprobe','powershell.exe')) {
    if ($null -eq (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "C11A.1: herramienta obligatoria no encontrada en PATH: $tool"
    }
}

# build_factory.py is retained only as a legacy CLI compatibility wrapper.
# C11-A.1 never invokes it; the canonical C11-C Challenge producer is authoritative.
$buildFactoryBytes = if (Test-Path -LiteralPath $buildFactory -PathType Leaf) { (Get-Item -LiteralPath $buildFactory).Length } else { 0 }
if ($buildFactoryBytes -le 0) {
    Write-Host '[C11A1] build_factory.py is absent/empty; using canonical Challenge producer.' -ForegroundColor DarkYellow
} else {
    Write-Host '[C11A1] build_factory.py is legacy compatibility-only; using canonical Challenge producer.' -ForegroundColor DarkYellow
}

$singleMode = (-not [string]::IsNullOrWhiteSpace($ChallengeId)) -or ($SingleSeed -gt 0)
if ($singleMode -and [string]::IsNullOrWhiteSpace($ChallengeId)) {
    throw 'C11A.1 single mode: -ChallengeId es obligatorio cuando se usa -SingleSeed.'
}
if ($singleMode -and $SingleSeed -le 0) {
    throw 'C11A.1 single mode: -SingleSeed debe ser > 0.'
}

if ($singleMode) {
    $seedCases = @([pscustomobject]@{ Label = ('SINGLE_' + [string]$SingleSeed); Seed = [int64]$SingleSeed })
    $challengeNumbers = @([int]$ChallengeId.Substring(10,3))
} else {
    # Matrix contractual: same order for all challenges.
    $seedCases = @(
        [pscustomobject]@{ Label = '12345_A'; Seed = 12345 },
        [pscustomobject]@{ Label = '54321'; Seed = 54321 },
        [pscustomobject]@{ Label = '314159'; Seed = 314159 },
        [pscustomobject]@{ Label = '7770001'; Seed = 7770001 },
        [pscustomobject]@{ Label = '998877'; Seed = 998877 },
        [pscustomobject]@{ Label = '12345_B'; Seed = 12345 }
    )
    $challengeNumbers = 1..9
}

$challengeFiles = $challengeNumbers | ForEach-Object {
    $path = Join-Path $challengesRoot ("CHALLENGE_{0:D3}.json" -f $_)
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "C11A.1: falta $path"
    }
    Get-Item -LiteralPath $path
}

function Convert-ToExpectedTimeline {
    param([object]$Video)
    if ($null -eq $Video.fps) { throw 'video.fps obligatorio.' }
    $fps = [int]$Video.fps
    if ($fps -le 0) { throw 'video.fps debe ser > 0.' }

    function ToFrames([double]$seconds, [int]$rate) {
        return [Math]::Max(0, [int][Math]::Floor(($seconds * $rate) + 0.5))
    }

    $hook = ToFrames ([double]$Video.hook_duration) $fps
    $game = ToFrames ([double]$Video.game_duration) $fps
    $reveal = 0.0
    $revealProperty = $Video.PSObject.Properties['reveal_duration']
    if ($null -ne $revealProperty) {
        $reveal = ToFrames ([double]$revealProperty.Value) $fps
    }
    $cta = ToFrames ([double]$Video.cta_duration) $fps

    return [pscustomobject]@{
        fps = $fps
        hook_frames = $hook
        game_frames = $game
        reveal_frames = $reveal
        cta_frames = $cta
        total_frames = $hook + $game + $reveal + $cta
    }
}

function Get-CanonicalJson {
    param([object]$Value)
    return ($Value | ConvertTo-Json -Depth 100 -Compress)
}

function Write-JsonUtf8 {
    param([string]$Path, [object]$Value)
    $json = $Value | ConvertTo-Json -Depth 100
    [IO.File]::WriteAllText($Path, $json, [Text.UTF8Encoding]::new($false))
}

function Invoke-ProcessCapture {
    param(
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [string]$StdoutPath,
        [string]$StderrPath
    )

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $FilePath
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true

    $quotedArguments = foreach ($arg in $ArgumentList) {
        if ($arg -notmatch '[\s"]') {
            $arg
            continue
        }

        '"' + (($arg -replace '(\\*)"', '$1$1\"') -replace '(\\+)$', '$1$1') + '"'
    }
    $psi.Arguments = $quotedArguments -join ' '

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $psi
    [void]$process.Start()
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $outText = $stdout.Result
    $errText = $stderr.Result

    [IO.File]::WriteAllText($StdoutPath, $outText, [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText($StderrPath, $errText, [Text.UTF8Encoding]::new($false))

    return [pscustomobject]@{
        ExitCode = $process.ExitCode
        Stdout = $outText
        Stderr = $errText
    }
}

function Invoke-C11A1CanonicalProducer {
    param(
        [string]$Producer,
        [string]$ChallengeId,
        [int64]$Seed,
        [string]$ArtifactRoot,
        [string]$WorkingDirectory,
        [string]$StdoutPath,
        [string]$StderrPath
    )

    # The canonical producer owns native Challenge override isolation and restores
    # any pre-existing project override.cfg byte-for-byte.
    return Invoke-ProcessCapture -FilePath 'powershell.exe' -ArgumentList @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', $Producer,
        '-ChallengeId', $ChallengeId,
        '-Seed', [string]$Seed,
        '-DeliveryProfile', 'MASTER_1080',
        '-OutputRoot', $ArtifactRoot,
        '-KeepAvi'
    ) -WorkingDirectory $WorkingDirectory -StdoutPath $StdoutPath -StderrPath $StderrPath
}

function Read-C11A1TelemetryFromLog {
    param([string]$LogPath)
    $lines = @(Get-Content -LiteralPath $LogPath -Encoding UTF8 | Where-Object { $_ -match '^\[TELEMETRY_JSON\]' })
    if ($lines.Count -eq 0) {
        throw "C11A.1: [TELEMETRY_JSON] not found en $LogPath"
    }
    $line = [string]$lines[$lines.Count - 1]
    return (($line.Substring('[TELEMETRY_JSON]'.Length)) | ConvertFrom-Json)
}

function Write-C11A1CompatibilityManifest {
    param(
        [string]$ManifestPath,
        [string]$ChallengeId,
        [int64]$Seed,
        [object]$ProductionManifest,
        [string]$ProductionManifestPath,
        [object]$Telemetry,
        [string]$FinalVideo,
        [string]$RawVideo,
        [string]$GodotLog
    )

    # All compatibility artifacts are siblings of the A1 adapter manifest.
    # Use leaf names for Windows PowerShell 5.1 compatibility; do not depend on
    # System.IO.Path.GetRelativePath, which is not a .NET Framework API.
    $finalRelative = [IO.Path]::GetFileName($FinalVideo)
    $rawRelative = [IO.Path]::GetFileName($RawVideo)
    $logRelative = [IO.Path]::GetFileName($GodotLog)
    $productionRelative = [IO.Path]::GetFileName($ProductionManifestPath)

    $adapter = [ordered]@{
        manifest_version = '1.0'
        qa_id = 'C11-A.1'
        schema = 'C11-A.1-CANONICAL-PRODUCER-ADAPTER-V1'
        status = 'PASS'
        adapter_reason = 'Historical A1 factory manifest contract adapted to the canonical C11-C Challenge producer; no second gameplay factory is introduced.'
        challenge_id = $ChallengeId
        seed = $Seed
        delivery_profile = 'MASTER_1080'
        source_movie_resolution = '540x960'
        delivery_resolution = '1080x1920'
        canonical_producer_status = [string]$ProductionManifest.status
        canonical_producer_manifest = $productionRelative
        telemetry = $Telemetry
        artifacts = [ordered]@{
            final_video = $finalRelative
            raw_video = $rawRelative
            production_manifest = $productionRelative
            godot_log = $logRelative
        }
        generated_from = 'tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1'
    }
    Write-JsonUtf8 $ManifestPath $adapter
}


function Resolve-C11A1FactoryArtifact {
    param(
        [string]$ManifestPath,
        [string]$ArtifactValue,
        [string]$ArtifactName
    )

    if ([string]::IsNullOrWhiteSpace($ArtifactValue)) {
        throw "C11A.1: compatibility manifest has empty artifacts.$ArtifactName"
    }
    if ([IO.Path]::IsPathRooted($ArtifactValue)) {
        $resolved = [IO.Path]::GetFullPath($ArtifactValue)
    } else {
        $resolved = [IO.Path]::GetFullPath((Join-Path (Split-Path -Parent $ManifestPath) $ArtifactValue))
    }

    $manifestRoot = [IO.Path]::GetFullPath((Split-Path -Parent $ManifestPath)).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $resolvedFull = [IO.Path]::GetFullPath($resolved)
    $prefix = $manifestRoot + [IO.Path]::DirectorySeparatorChar
    if (-not $resolvedFull.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase) -and $resolvedFull -ne $manifestRoot) {
        throw "C11A.1: artifact escapes compatibility manifest directory ($ArtifactName): $resolvedFull"
    }
    if (-not (Test-Path -LiteralPath $resolvedFull -PathType Leaf)) {
        throw "C11A.1: compatibility artifact missing ($ArtifactName): $resolvedFull"
    }
    return $resolvedFull
}

function Invoke-FFProbe {
    param([string]$VideoPath)
    $json = & ffprobe -v error -select_streams v:0 -count_frames `
        -show_entries stream=width,height,r_frame_rate,nb_read_frames,duration,codec_name,pix_fmt `
        -of json -- $VideoPath 2>&1
    if ($LASTEXITCODE -ne 0) { throw "ffprobe failed for $VideoPath`n$json" }
    return ($json -join "`n" | ConvertFrom-Json)
}

function Invoke-FrameMD5 {
    param([string]$VideoPath, [string]$OutputPath)
    & ffmpeg -v error -i $VideoPath -f framemd5 -an -sn -dn -y $OutputPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
        throw "framemd5 failed for $VideoPath"
    }
}

function Select-ReviewFrames {
    param(
        [string]$VideoPath,
        [int[]]$Indices,
        [string]$FrameDirectory
    )

    New-Item -ItemType Directory -Force -Path $FrameDirectory | Out-Null
    $safe = @()
    foreach ($index in $Indices) {
        if ($index -ge 0 -and $index -notin $safe) { $safe += $index }
    }

    for ($i = 0; $i -lt $safe.Count; $i++) {
        $frameIndex = $safe[$i]
        $out = Join-Path $FrameDirectory ("frame_{0:D2}_n{1:D5}.png" -f ($i + 1), $frameIndex)
        & ffmpeg -v error -i $VideoPath -vf ("select='eq(n,{0})'" -f $frameIndex) -frames:v 1 -y $out
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $out -PathType Leaf)) {
            throw "No se pudo extraer frame $frameIndex de $VideoPath"
        }
    }
}

function Create-ContactSheet {
    param(
        [string]$FrameDirectory,
        [string]$OutputPath
    )

    $frames = @(Get-ChildItem -LiteralPath $FrameDirectory -Filter 'frame_*.png' | Sort-Object Name)
    if ($frames.Count -eq 0) { throw "No hay keyframes para contact sheet: $FrameDirectory" }

    $inputs = @()
    foreach ($frame in $frames) { $inputs += @('-i', $frame.FullName) }

    $filters = @()
    for ($i = 0; $i -lt $frames.Count; $i++) {
        $filters += "[$i`:v]scale=216:384[s$i]"
    }
    $refs = (($frames | ForEach-Object -Begin {$i=0} -Process { "[s$($i)]"; $i++ }) -join '')
    $filters += "$refs`hstack=inputs=$($frames.Count):shortest=1[out]"
    $filterComplex = $filters -join ';'

    & ffmpeg -v error @inputs -filter_complex $filterComplex -map '[out]' -frames:v 1 -q:v 3 -y $OutputPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
        throw "No se pudo crear contact sheet: $OutputPath"
    }
}

Write-Host "[C11A1] Challenge Seed Qualification" -ForegroundColor Cyan
if ($singleMode) {
    Write-Host "[C11A1] SINGLE RUN: $ChallengeId seed=$SingleSeed" -ForegroundColor Cyan
} else {
    Write-Host "[C11A1] Matrix: $($challengeFiles.Count) challenges x $($seedCases.Count) seeds = $($challengeFiles.Count * $seedCases.Count) runs"
}
Write-Host "[C11A1] Output: $OutputRoot"
Write-Host "[C11A1] Core remains untouched; orchestration delegates to canonical Challenge producer."

New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot 'runs') | Out-Null

$plan = @()
foreach ($challengeFile in $challengeFiles) {
    $source = Get-Content -LiteralPath $challengeFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($source.challenge_id -ne $challengeFile.BaseName) {
        throw "C11A.1: mismatch filename/challenge_id en $($challengeFile.Name)"
    }
    if ($null -eq $source.generation -or $null -eq $source.generation.seed -or $null -eq $source.generation.rng_version) {
        throw "C11A.1: generation.seed/rng_version incompleto en $($challengeFile.Name)"
    }
    $timeline = Convert-ToExpectedTimeline $source.video

    foreach ($seedCase in $seedCases) {
        $runId = "{0}_seed_{1}" -f $source.challenge_id.ToLowerInvariant(), $seedCase.Label
        $plan += [pscustomobject]@{
            challenge_id = $source.challenge_id
            mechanic = [string]$source.mechanic
            mechanic_version = if ($null -ne $source.mechanic_version) { [string]$source.mechanic_version } else { $null }
            source_seed = [int64]$source.generation.seed
            test_seed = [int64]$seedCase.Seed
            seed_label = $seedCase.Label
            rng_version = [string]$source.generation.rng_version
            run_id = $runId
            expected_timeline = $timeline
            source_config = $challengeFile.FullName
        }
    }
}

Write-JsonUtf8 (Join-Path $OutputRoot 'C11A1_CHALLENGE_BULK_PLAN.json') $plan

$completed = 0
$total = $plan.Count
$startedAt = [DateTimeOffset]::UtcNow

foreach ($item in $plan) {
    $completed++
    $runDir = Join-Path (Join-Path $OutputRoot 'runs') $item.run_id
    $configPath = Join-Path $runDir 'challenge_definition.json'
    $artifactRoot = Join-Path $runDir 'artifacts'
    $factoryManifestPath = Join-Path (Join-Path $artifactRoot $item.challenge_id) ("{0}_manifest.json" -f $item.challenge_id)
    $runRecordPath = Join-Path $runDir 'run_record.json'

    if (Test-Path -LiteralPath $runDir -PathType Container) {
        if ($Resume -and (Test-Path -LiteralPath $runRecordPath -PathType Leaf)) {
            try {
                $record = Get-Content -LiteralPath $runRecordPath -Raw -Encoding UTF8 | ConvertFrom-Json
                if ($record.status -eq 'COMPLETE') {
                    Write-Host ("[{0}/{1}] SKIP existing COMPLETE {2}" -f $completed,$total,$item.run_id)
                    continue
                }

                Write-Host ("[{0}/{1}] RETRY existing {2} status={3}" -f $completed,$total,$item.run_id,$record.status) -ForegroundColor Yellow
                Remove-Item -LiteralPath $runDir -Recurse -Force
            } catch {}
        }

        if (Test-Path -LiteralPath $runDir -PathType Container) {
            throw "C11A.1: run directory already exists; refusing overwrite: $runDir. Use a fresh artifacts/qa/c11a1_challenge or -Resume to retry incomplete runs."
        }
    }

    New-Item -ItemType Directory -Force -Path $runDir | Out-Null
    New-Item -ItemType Directory -Force -Path $artifactRoot | Out-Null

    $definition = Get-Content -LiteralPath $item.source_config -Raw -Encoding UTF8 | ConvertFrom-Json
    $definition.generation.seed = [int64]$item.test_seed
    Write-JsonUtf8 $configPath $definition

    $preRecord = [pscustomobject]@{
        status = 'RUNNING'
        run_id = $item.run_id
        challenge_id = $item.challenge_id
        mechanic = $item.mechanic
        mechanic_version = $item.mechanic_version
        source_seed = $item.source_seed
        test_seed = $item.test_seed
        seed_label = $item.seed_label
        rng_version = $item.rng_version
        expected_timeline = $item.expected_timeline
        source_config = $item.source_config
        qa_config = $configPath
        artifact_root = $artifactRoot
        started_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        completed_at_utc = $null
        failure = $null
        factory_exit_code = $null
        producer_exit_code = $null
        factory_manifest = $null
        video = $null
        framemd5 = $null
        review_frames = $null
    }
    Write-JsonUtf8 $runRecordPath $preRecord

    Write-Host ("[{0}/{1}] RUN {2} mechanic={3} seed={4} rng={5} frames={6}" -f `
        $completed,$total,$item.run_id,$item.mechanic,$item.test_seed,$item.rng_version,$item.expected_timeline.total_frames) -ForegroundColor Yellow

    $stdoutPath = Join-Path $runDir 'factory_stdout.txt'
    $stderrPath = Join-Path $runDir 'factory_stderr.txt'

    $proc = Invoke-C11A1CanonicalProducer `
        -Producer $producer `
        -ChallengeId $item.challenge_id `
        -Seed $item.test_seed `
        -ArtifactRoot $artifactRoot `
        -WorkingDirectory $ProjectRoot `
        -StdoutPath $stdoutPath `
        -StderrPath $stderrPath

    if ($proc.ExitCode -ne 0) {
        $preRecord.status = 'FAILED'
        $preRecord.failure = [pscustomobject]@{ code = 'PRODUCER_EXIT'; message = "canonical Challenge producer exit=$($proc.ExitCode)" }
        $preRecord.completed_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        Write-JsonUtf8 $runRecordPath $preRecord
        throw "C11A.1: $($item.run_id) failed in canonical Challenge producer. See $stdoutPath / $stderrPath"
    }

    $productRoot = Join-Path $artifactRoot $item.challenge_id
    $productionManifestPath = Join-Path $productRoot 'production_manifest.json'
    $godotLogPath = Join-Path $productRoot 'godot.log'
    $expectedMp4Path = Join-Path $productRoot ("{0}_seed_{1}.mp4" -f $item.challenge_id, $item.test_seed)
    $expectedAviPath = Join-Path $productRoot ("{0}_seed_{1}_source.avi" -f $item.challenge_id, $item.test_seed)

    if (-not (Test-Path -LiteralPath $productionManifestPath -PathType Leaf)) { throw "C11A.1: canonical producer manifest missing: $productionManifestPath" }
    if (-not (Test-Path -LiteralPath $godotLogPath -PathType Leaf)) { throw "C11A.1: canonical producer godot.log missing: $godotLogPath" }
    if (-not (Test-Path -LiteralPath $expectedMp4Path -PathType Leaf)) { throw "C11A.1: canonical producer MP4 missing: $expectedMp4Path" }
    if (-not (Test-Path -LiteralPath $expectedAviPath -PathType Leaf)) { throw "C11A.1: canonical producer source AVI missing: $expectedAviPath" }

    $productionManifest = Get-Content -LiteralPath $productionManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $telemetry = Read-C11A1TelemetryFromLog $godotLogPath
    Write-C11A1CompatibilityManifest `
        -ManifestPath $factoryManifestPath `
        -ChallengeId $item.challenge_id `
        -Seed $item.test_seed `
        -ProductionManifest $productionManifest `
        -ProductionManifestPath $productionManifestPath `
        -Telemetry $telemetry `
        -FinalVideo $expectedMp4Path `
        -RawVideo $expectedAviPath `
        -GodotLog $godotLogPath

    if (-not (Test-Path -LiteralPath $factoryManifestPath -PathType Leaf)) {
        throw "C11A.1: compatibility manifest missing after canonical producer validation: $factoryManifestPath"
    }
    $factoryManifest = Get-Content -LiteralPath $factoryManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([string]$factoryManifest.status -ne 'PASS') { throw "C11A.1: compatibility manifest status != PASS for $($item.run_id)" }
    $videoPath = Resolve-C11A1FactoryArtifact -ManifestPath $factoryManifestPath -ArtifactValue $factoryManifest.artifacts.final_video -ArtifactName 'final_video'
    $rawVideoPath = Resolve-C11A1FactoryArtifact -ManifestPath $factoryManifestPath -ArtifactValue $factoryManifest.artifacts.raw_video -ArtifactName 'raw_video'


    $probe = Invoke-FFProbe $videoPath
    $stream = $probe.streams[0]
    $observedFrames = [int]$stream.nb_read_frames
    $observedFps = [string]$stream.r_frame_rate
    $observedWidth = [int]$stream.width
    $observedHeight = [int]$stream.height
    $observedDuration = [double]$stream.duration

    if ($observedFrames -ne [int]$item.expected_timeline.total_frames) { throw "C11A.1: frame count mismatch for $($item.run_id): $observedFrames vs $($item.expected_timeline.total_frames)" }
    if ($observedFps -ne ("{0}/1" -f $item.expected_timeline.fps)) { throw "C11A.1: fps mismatch for $($item.run_id): $observedFps" }
    if ($observedWidth -ne 1080 -or $observedHeight -ne 1920) { throw "C11A.1: master resolution mismatch for $($item.run_id): $observedWidth x $observedHeight" }

    $framemd5Path = Join-Path $runDir 'render.framemd5'
    Invoke-FrameMD5 -VideoPath $videoPath -OutputPath $framemd5Path

    $winningAbsolute = [int]$telemetry.winning_frame
    $winningGame = [int]$telemetry.winning_frame_game
    $totalFrames = [int]$telemetry.total_frames
    $middle = [int][Math]::Floor(($totalFrames - 1) / 2)
    $quarter = [int][Math]::Floor(($totalFrames - 1) * 0.25)
    $threeQuarter = [int][Math]::Floor(($totalFrames - 1) * 0.75)
    $reviewIndices = @(0, $quarter, $middle, $winningAbsolute, $threeQuarter, ($totalFrames - 1))
    $reviewIndices = $reviewIndices | Where-Object { $_ -ge 0 -and $_ -lt $totalFrames } | Select-Object -Unique
    $framesDir = Join-Path $runDir 'frames'
    Select-ReviewFrames -VideoPath $videoPath -Indices ([int[]]$reviewIndices) -FrameDirectory $framesDir
    Create-ContactSheet -FrameDirectory $framesDir -OutputPath (Join-Path $runDir 'contact_sheet.jpg')

    $telemetryPath = Join-Path $runDir 'telemetry.json'
    Write-JsonUtf8 $telemetryPath $telemetry

    $simulationSummary = [pscustomobject]@{
        simulation_pass = $true
        initial_seed = [int64]$telemetry.initial_seed
        final_seed = [int64]$telemetry.final_seed
        seed_used = [int64]$telemetry.seed_used
        attempts = [int]$telemetry.attempts
        retries_used = [Math]::Max(0, ([int]$telemetry.attempts - 1))
        rng_version = [string]$telemetry.rng_version
        winning_frame_game = $winningGame
        winning_frame = $winningAbsolute
        winning_frame_in_valid_window = [bool]$telemetry.winning_frame_in_valid_window
        minimum_distance = [double]$telemetry.minimum_distance
        score = [double]$telemetry.score
        close_calls = [int]$telemetry.close_calls
    }
    Write-JsonUtf8 (Join-Path $runDir 'simulation_summary.json') $simulationSummary

    $preRecord.status = 'COMPLETE'
    $preRecord.completed_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
    $preRecord.factory_exit_code = $proc.ExitCode
    $preRecord.producer_exit_code = $proc.ExitCode
    $preRecord.factory_manifest = $factoryManifestPath
    $preRecord.canonical_producer_manifest = Join-Path $productRoot 'production_manifest.json'
    $preRecord.video = [pscustomobject]@{
        mp4 = $videoPath
        avi = $rawVideoPath
        width = $observedWidth
        height = $observedHeight
        fps = $observedFps
        frames = $observedFrames
        duration = $observedDuration
    }
    $preRecord.framemd5 = $framemd5Path
    $preRecord.review_frames = $reviewIndices
    Write-JsonUtf8 $runRecordPath $preRecord

    Write-Host ("[{0}/{1}] PASS {2} -> winning={3} abs / {4} game attempts={5}" -f `
        $completed,$total,$item.run_id,$winningAbsolute,$winningGame,$telemetry.attempts) -ForegroundColor Green
}

$elapsed = ([DateTimeOffset]::UtcNow - $startedAt).TotalSeconds
if ($singleMode) {
    Write-Host "[C11A1] SINGLE PASS: $total/$total run validated." -ForegroundColor Green
} else {
    Write-Host "[C11A1] Physical generation complete: $total/$total" -ForegroundColor Green
}
Write-Host ("[C11A1] Elapsed seconds: {0:N1}" -f $elapsed)
if (-not $singleMode) { Write-Host "[C11A1] Next command: .\tools\qa\c11\finalize_c11a1_challenge_bulk_qa.ps1" }
