function New-C11CReviewWorkerPool {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$ProjectRoot,
        [Parameter(Mandatory=$true)][ValidateRange(1,7)][int]$Count
    )

    $sourceRoot = (Resolve-Path $ProjectRoot).Path
    $poolRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('C11C_ReviewWorkers_' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $poolRoot -Force | Out-Null

    # One real Godot project root per worker. The critical state (override.cfg and .godot)
    # therefore cannot be shared between concurrent Movie Maker processes.
    $excludeDirs = @(
        (Join-Path $sourceRoot 'artifacts'),
        (Join-Path $sourceRoot '.git'),
        (Join-Path $sourceRoot '.godot'),
        (Join-Path $sourceRoot '.pytest_cache'),
        (Join-Path $sourceRoot 'c11c-suite\.pytest_cache'),
        (Join-Path $sourceRoot 'c11c-suite\c11c-producer\__pycache__')
    )

    $workers = @()
    try {
        for ($i = 0; $i -lt $Count; $i++) {
            $workerRoot = Join-Path $poolRoot ('worker_{0:D2}' -f $i)
            New-Item -ItemType Directory -Path $workerRoot -Force | Out-Null

            # robocopy exit codes 0..7 are success/non-fatal copy states.
            & robocopy.exe $sourceRoot $workerRoot /E /XD $excludeDirs /XF 'override.cfg' /R:1 /W:1 /NFL /NDL /NJH /NJS /NP | Out-Null
            $robocopyExit = $LASTEXITCODE
            if ($robocopyExit -ge 8) {
                throw "Worker sandbox copy failed for slot ${i}: robocopy exit=$robocopyExit"
            }

            $null = Initialize-C11CReviewWorkerProject -WorkerRoot $workerRoot

            $workers += [pscustomobject]@{
                Slot       = $i
                WorkerRoot = $workerRoot
                # Root is retained as a compatibility alias for older orchestration code.
                Root       = $workerRoot
            }
        }

        return [pscustomobject]@{
            Root = $poolRoot
            Workers = $workers
            SourceRoot = $sourceRoot
        }
    } catch {
        Remove-C11CReviewWorkerPool -Pool $poolRoot
        throw
    }
}

function Initialize-C11CReviewWorkerProject {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][string]$WorkerRoot)

    $projectFile = Join-Path $WorkerRoot 'project.godot'
    $presentationProfile = Join-Path $WorkerRoot 'core\presentation\PresentationProfile.gd'
    $godotDir = Join-Path $WorkerRoot '.godot'
    $cacheFile = Join-Path $godotDir 'global_script_class_cache.cfg'
    $bootstrapLog = Join-Path $godotDir '.c11c_worker_class_cache_bootstrap.log'

    if (-not (Test-Path -LiteralPath $projectFile -PathType Leaf)) {
        throw "Worker project bootstrap missing project.godot: $WorkerRoot"
    }
    if (-not (Test-Path -LiteralPath $presentationProfile -PathType Leaf)) {
        throw "Worker project bootstrap missing PresentationProfile.gd: $presentationProfile"
    }

    New-Item -ItemType Directory -Force -Path $godotDir | Out-Null
    $nativeEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & godot --headless --editor --path $WorkerRoot --quit 2>&1 | Tee-Object -FilePath $bootstrapLog | Out-Null
        $godotExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $nativeEap
    }

    if ($godotExit -ne 0) {
        throw "Worker Godot class-cache bootstrap failed: exit=$godotExit root=$WorkerRoot"
    }
    if (-not (Test-Path -LiteralPath $cacheFile -PathType Leaf)) {
        throw "Worker Godot class-cache bootstrap produced no global_script_class_cache.cfg: $WorkerRoot"
    }

    $cacheText = Get-Content -Raw -LiteralPath $cacheFile -ErrorAction Stop
    if ($cacheText -notmatch 'PresentationProfile') {
        throw "Worker Godot class-cache bootstrap did not register PresentationProfile: $WorkerRoot"
    }

    # Marker used only to make the bootstrap state explicit in worker evidence.
    $readyMarker = Join-Path $WorkerRoot '.c11c_worker_class_cache_ready'
    [System.IO.File]::WriteAllText(
        $readyMarker,
        "PresentationProfile`n$cacheFile`n" + (Get-Date).ToUniversalTime().ToString('o'),
        (New-Object System.Text.UTF8Encoding($false))
    )
}

function Remove-C11CReviewWorkerPool {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][AllowEmptyString()][string]$Pool)
    if ([string]::IsNullOrWhiteSpace($Pool)) { return }
    if (Test-Path -LiteralPath $Pool) {
        Remove-Item -LiteralPath $Pool -Recurse -Force -ErrorAction SilentlyContinue
    }
}
