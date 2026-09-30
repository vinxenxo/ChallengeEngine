[CmdletBinding()]
param()

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

            $workers += [pscustomobject]@{
                Slot       = $i
                WorkerRoot = $workerRoot
                Root       = $workerRoot
            }
        }

        # Preferred path: reuse the source project's already-valid Godot class cache.
        # Fallback path: generate it once in the real project root. We deliberately do
        # not launch the editor inside a temporary worker project because that native
        # startup was the source of the previous 0xC0000005 acceptance failure.
        $sourceCache = Initialize-C11CReviewSourceClassCache -ProjectRoot $sourceRoot

        # The worker clone intentionally starts without the source project's `.godot` tree.
        # C11-C editorial typography uses imported font resources, however, and Godot's
        # Movie Maker runtime must see the same read-only `.fontdata` cache that exists
        # after the source project has been initialized/tested. Propagate only the two
        # active C11-C font import artifacts into each worker's private `.godot`.
        $sourceImportedDir = Join-Path $sourceRoot '.godot\imported'
        $fontImportPatterns = @(
            'Inter-Bold.otf-*.fontdata',
            'NotoSansMono-Regular.ttf-*.fontdata'
        )
        $sourceFontImports = @()
        if (Test-Path -LiteralPath $sourceImportedDir -PathType Container) {
            foreach ($pattern in $fontImportPatterns) {
                $sourceFontImports += @(Get-ChildItem -LiteralPath $sourceImportedDir -File -Filter $pattern -ErrorAction SilentlyContinue)
            }
        }
        if ($sourceFontImports.Count -ne 2) {
            throw "C11-C worker font-cache bootstrap expected exactly two imported font resources in source `.godot\imported`: $sourceImportedDir"
        }

        foreach ($worker in @($workers)) {
            $workerRoot = [string]$worker.WorkerRoot
            $godotDir = Join-Path $workerRoot '.godot'
            $importedDir = Join-Path $godotDir 'imported'
            $cacheFile = Join-Path $godotDir 'global_script_class_cache.cfg'
            New-Item -ItemType Directory -Force -Path $godotDir | Out-Null
            New-Item -ItemType Directory -Force -Path $importedDir | Out-Null
            Copy-Item -LiteralPath $sourceCache -Destination $cacheFile -Force
            foreach ($fontImport in @($sourceFontImports)) {
                Copy-Item -LiteralPath $fontImport.FullName -Destination (Join-Path $importedDir $fontImport.Name) -Force
            }
            Assert-C11CReviewWorkerClassCache -WorkerRoot $workerRoot
        }

        return [pscustomobject]@{
            Root = $poolRoot
            Workers = $workers
            SourceRoot = $sourceRoot
            BootstrapMode = 'source_project_godot_class_cache_then_private_worker_clone'
        }
    } catch {
        Remove-C11CReviewWorkerPool -Pool $poolRoot
        throw
    }
}

function Initialize-C11CReviewSourceClassCache {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$ProjectRoot
    )

    $projectRoot = (Resolve-Path $ProjectRoot).Path
    $projectFile = Join-Path $projectRoot 'project.godot'
    $presentationProfile = Join-Path $projectRoot 'core\presentation\PresentationProfile.gd'
    $godotDir = Join-Path $projectRoot '.godot'
    $cacheFile = Join-Path $godotDir 'global_script_class_cache.cfg'
    $bootstrapLog = Join-Path $godotDir '.c11c_worker_class_cache_bootstrap.log'

    if (-not (Test-Path -LiteralPath $projectFile -PathType Leaf)) {
        throw "Source project bootstrap missing project.godot: $projectRoot"
    }
    if (-not (Test-Path -LiteralPath $presentationProfile -PathType Leaf)) {
        throw "Source project bootstrap missing PresentationProfile.gd: $presentationProfile"
    }

    New-Item -ItemType Directory -Force -Path $godotDir | Out-Null

    if (Test-Path -LiteralPath $cacheFile -PathType Leaf) {
        $cacheText = Get-Content -Raw -LiteralPath $cacheFile -ErrorAction Stop
        if ($cacheText -match 'PresentationProfile') {
            return $cacheFile
        }
        Remove-Item -LiteralPath $cacheFile -Force -ErrorAction SilentlyContinue
    }

    $nativeEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & godot --headless --editor --path $projectRoot --quit 2>&1 | Tee-Object -FilePath $bootstrapLog | Out-Null
        $godotExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $nativeEap
    }

    if ($godotExit -ne 0) {
        throw "Source Godot class-cache bootstrap failed: exit=$godotExit root=$projectRoot"
    }
    if (-not (Test-Path -LiteralPath $cacheFile -PathType Leaf)) {
        throw "Source Godot class-cache bootstrap produced no global_script_class_cache.cfg: $projectRoot"
    }

    $cacheText = Get-Content -Raw -LiteralPath $cacheFile -ErrorAction Stop
    if ($cacheText -notmatch 'PresentationProfile') {
        throw "Source Godot class-cache bootstrap did not register PresentationProfile: $projectRoot"
    }

    return $cacheFile
}

function Initialize-C11CReviewWorkerClassCache {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$WorkerRoot
    )
    Assert-C11CReviewWorkerClassCache -WorkerRoot $WorkerRoot
}

function Assert-C11CReviewWorkerClassCache {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][string]$WorkerRoot)

    $cacheFile = Join-Path $WorkerRoot '.godot\global_script_class_cache.cfg'
    if (-not (Test-Path -LiteralPath $cacheFile -PathType Leaf)) {
        throw "Worker Godot class-cache bootstrap produced no global_script_class_cache.cfg: $WorkerRoot"
    }

    $cacheText = Get-Content -Raw -LiteralPath $cacheFile -ErrorAction Stop
    if ($cacheText -notmatch 'PresentationProfile') {
        throw "Worker Godot class-cache bootstrap did not register PresentationProfile: $WorkerRoot"
    }

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
