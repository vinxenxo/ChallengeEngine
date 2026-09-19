[CmdletBinding()]
param(
    [string]$ProjectRoot = "",
    [string]$OutputRoot = "",
    [switch]$Resume
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

$buildFactory = Join-Path $ProjectRoot 'build_factory.py'
$challengesRoot = Join-Path $ProjectRoot 'challenges'

if (-not (Test-Path -LiteralPath $buildFactory -PathType Leaf)) {
    throw "C11A.1: no existe build_factory.py en $ProjectRoot"
}
if (-not (Test-Path -LiteralPath $challengesRoot -PathType Container)) {
    throw "C11A.1: no existe la carpeta challenges/"
}

foreach ($tool in @('python','ffmpeg','ffprobe')) {
    if ($null -eq (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "C11A.1: herramienta obligatoria no encontrada en PATH: $tool"
    }
}

# Matriz contractual: mismo orden para todos los challenges.
$seedCases = @(
    [pscustomobject]@{ Label = '12345_A'; Seed = 12345 },
    [pscustomobject]@{ Label = '54321'; Seed = 54321 },
    [pscustomobject]@{ Label = '314159'; Seed = 314159 },
    [pscustomobject]@{ Label = '7770001'; Seed = 7770001 },
    [pscustomobject]@{ Label = '998877'; Seed = 998877 },
    [pscustomobject]@{ Label = '12345_B'; Seed = 12345 }
)

$challengeFiles = 1..9 | ForEach-Object {
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
    $reveal = ToFrames ([double]$Video.reveal_duration) $fps
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

function Invoke-FFProbe {
    param([string]$VideoPath)
    $json = & ffprobe -v error -select_streams v:0 -count_frames `
        -show_entries stream=width,height,r_frame_rate,nb_read_frames,duration,codec_name,pix_fmt `
        -of json -- $VideoPath 2>&1
    if ($LASTEXITCODE -ne 0) { throw "ffprobe falló para $VideoPath`n$json" }
    return ($json -join "`n" | ConvertFrom-Json)
}

function Invoke-FrameMD5 {
    param([string]$VideoPath, [string]$OutputPath)
    & ffmpeg -v error -i $VideoPath -f framemd5 -an -sn -dn -y $OutputPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
        throw "framemd5 falló para $VideoPath"
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
Write-Host "[C11A1] Matrix: $($challengeFiles.Count) challenges x $($seedCases.Count) seeds = $($challengeFiles.Count * $seedCases.Count) runs"
Write-Host "[C11A1] Output: $OutputRoot"
Write-Host "[C11A1] Core remains untouched; orchestration delegates to build_factory.py."

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

    $proc = Invoke-ProcessCapture -FilePath 'python' -ArgumentList @(
        '-u', $buildFactory,
        '--config', $configPath,
        '--output', $artifactRoot,
        '--no-gif'
    ) -WorkingDirectory $ProjectRoot -StdoutPath $stdoutPath -StderrPath $stderrPath

    if ($proc.ExitCode -ne 0) {
        $preRecord.status = 'FAILED'
        $preRecord.failure = [pscustomobject]@{ code = 'FACTORY_EXIT'; message = "python build_factory.py exit=$($proc.ExitCode)" }
        $preRecord.completed_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        Write-JsonUtf8 $runRecordPath $preRecord
        throw "C11A.1: $($item.run_id) failed in build_factory.py. See $stdoutPath / $stderrPath"
    }

    if (-not (Test-Path -LiteralPath $factoryManifestPath -PathType Leaf)) {
        $preRecord.status = 'FAILED'
        $preRecord.failure = [pscustomobject]@{ code = 'MISSING_FACTORY_MANIFEST'; message = $factoryManifestPath }
        $preRecord.completed_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        Write-JsonUtf8 $runRecordPath $preRecord
        throw "C11A.1: missing factory manifest: $factoryManifestPath"
    }

    $factoryManifest = Get-Content -LiteralPath $factoryManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([string]$factoryManifest.status -ne 'PASS') {
        throw "C11A.1: factory manifest status != PASS for $($item.run_id)"
    }

    $telemetry = $factoryManifest.telemetry
    $videoPath = Join-Path (Join-Path $artifactRoot $item.challenge_id) ([string]$factoryManifest.artifacts.final_video)
    $rawVideoPath = Join-Path (Join-Path $artifactRoot $item.challenge_id) ([string]$factoryManifest.artifacts.raw_video)

    if (-not (Test-Path -LiteralPath $videoPath -PathType Leaf)) { throw "C11A.1: MP4 missing: $videoPath" }
    if (-not (Test-Path -LiteralPath $rawVideoPath -PathType Leaf)) { throw "C11A.1: AVI missing: $rawVideoPath" }

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
    $preRecord.factory_manifest = $factoryManifestPath
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
Write-Host "[C11A1] Physical generation complete: $total/$total" -ForegroundColor Green
Write-Host ("[C11A1] Elapsed seconds: {0:N1}" -f $elapsed)
Write-Host "[C11A1] Next command: .\tools\qa\c11\finalize_c11a1_challenge_bulk_qa.ps1"
