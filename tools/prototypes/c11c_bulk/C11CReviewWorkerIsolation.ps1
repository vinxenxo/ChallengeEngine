function Initialize-C11CReviewWorkerProject {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$WorkerRoot,
        [Parameter(Mandatory=$true)][int]$WorkerSlot
    )

    # Fresh worker projects intentionally do not inherit source .godot state. Godot named
    # scripts (class_name) rely on the project/editor-generated global script class cache.
    # Bootstrap each worker once, before any Movie Maker capture. Only bootstrap is sequential;
    # all actual review captures remain concurrent after the pool has been prepared.
    $godotExecutable = if([string]::IsNullOrWhiteSpace($env:GODOT_BIN)) { 'godot.exe' } else { $env:GODOT_BIN }
    $bootstrapLog = Join-Path $WorkerRoot '.c11c_worker_bootstrap.log'
    $cachePath = Join-Path $WorkerRoot '.godot\global_script_class_cache.cfg'
    $args = @('--headless','--editor','--path',$WorkerRoot,'--audio-driver','Dummy','--quit')

    Write-Host "[C11-C-WORKER] bootstrap=class-cache slot=$WorkerSlot root=$WorkerRoot"
    $nativeEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & $godotExecutable @args 2>&1 | Tee-Object -FilePath $bootstrapLog | Out-Host
        $godotExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $nativeEap
    }
    if($godotExit -ne 0){
        throw "Worker bootstrap failed for slot ${WorkerSlot}: Godot exit=$godotExit; log=$bootstrapLog"
    }
    if(-not(Test-Path -LiteralPath $cachePath -PathType Leaf)){
        throw "Worker bootstrap failed for slot ${WorkerSlot}: missing Godot global script class cache: $cachePath"
    }
    $cacheText=Get-Content -Raw -LiteralPath $cachePath
    if($cacheText -notmatch 'PresentationProfile'){
        throw "Worker bootstrap failed for slot ${WorkerSlot}: PresentationProfile not registered in $cachePath"
    }
    Write-Host "[C11-C-WORKER] bootstrap=PASS slot=$WorkerSlot cache=global_script_class_cache.cfg"
}

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
    # therefore cannot be shared between concurrent Movie Maker processes. No global mutex is used.
    $excludeDirs = @(
        (Join-Path $sourceRoot 'artifacts'),
        (Join-Path $sourceRoot 'c11c-studio'),
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

            Initialize-C11CReviewWorkerProject -WorkerRoot $workerRoot -WorkerSlot $i

            $workers += [pscustomobject]@{
                Slot = $i
                Root = $workerRoot
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

function Remove-C11CReviewWorkerPool {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][AllowEmptyString()][string]$Pool)
    if ([string]::IsNullOrWhiteSpace($Pool)) { return }
    if (Test-Path -LiteralPath $Pool) {
        Remove-Item -LiteralPath $Pool -Recurse -Force -ErrorAction SilentlyContinue
    }
}
