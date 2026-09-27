function Enter-C11CMovieOverride {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$ProjectRoot,
        [Parameter(Mandatory=$false)][int]$Width = 720,
        [Parameter(Mandatory=$false)][int]$Height = 1280
    )
    if ($Width -lt 1 -or $Height -lt 1) { throw 'Movie resolution must be positive.' }
    # `override.cfg` is a project-global file. Serialize the complete Movie Maker
    # transaction so concurrent C11-C workers cannot overwrite each other's resolution.
    $mutex = New-Object System.Threading.Mutex($false, 'Global\ChallengeEngineV01_C11C_MovieCapture')
    $mutexAcquired = $false
    try {
        try {
            $mutexAcquired = $mutex.WaitOne([TimeSpan]::FromHours(12))
        } catch [System.Threading.AbandonedMutexException] {
            # The previous owner terminated unexpectedly. The mutex is now owned by us.
            $mutexAcquired = $true
        }
        if (-not $mutexAcquired) { throw 'Timed out waiting for the C11-C Movie Maker resolution lock.' }
    } catch {
        $mutex.Dispose()
        throw
    }
    $overridePath = Join-Path $ProjectRoot 'override.cfg'
    $backupPath = Join-Path ([System.IO.Path]::GetTempPath()) ('C11C_override_backup_' + [Guid]::NewGuid().ToString('N') + '.cfg')
    $hadExisting = Test-Path -LiteralPath $overridePath
    if ($hadExisting) { Copy-Item -LiteralPath $overridePath -Destination $backupPath -Force }
    # C11-B remains frozen at 540x960. This temporary override changes only the effective
    # Movie Maker viewport/window for C11-C delivery; the prototype scene scales its
    # 540x960 logical composition by 4/3 to fill 720x1280.
    try {
        $cfg = "[display]`r`n`r`nwindow/size/viewport_width=$Width`r`nwindow/size/viewport_height=$Height`r`nwindow/size/window_width_override=$Width`r`nwindow/size/window_height_override=$Height`r`n"
        [System.IO.File]::WriteAllText($overridePath, $cfg, (New-Object System.Text.UTF8Encoding($false)))
        return [pscustomobject]@{ OverridePath=$overridePath; BackupPath=$backupPath; HadExisting=$hadExisting; Width=$Width; Height=$Height; Mutex=$mutex; MutexAcquired=$mutexAcquired }
    } catch {
        if ($hadExisting -and (Test-Path -LiteralPath $backupPath)) { Copy-Item -LiteralPath $backupPath -Destination $overridePath -Force; Remove-Item -LiteralPath $backupPath -Force -ErrorAction SilentlyContinue }
        elseif (Test-Path -LiteralPath $overridePath) { Remove-Item -LiteralPath $overridePath -Force -ErrorAction SilentlyContinue }
        if ($mutexAcquired) { try { $mutex.ReleaseMutex() } catch {} }
        $mutex.Dispose()
        throw
    }
}

function Exit-C11CMovieOverride {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)]$State)
    try {
        if ($State.HadExisting) {
            if (-not (Test-Path -LiteralPath $State.BackupPath)) { throw "Movie override backup missing: $($State.BackupPath)" }
            Copy-Item -LiteralPath $State.BackupPath -Destination $State.OverridePath -Force
            Remove-Item -LiteralPath $State.BackupPath -Force -ErrorAction SilentlyContinue
        } elseif (Test-Path -LiteralPath $State.OverridePath) {
            Remove-Item -LiteralPath $State.OverridePath -Force
        }
    } finally {
        if ($State.MutexAcquired) {
            try { $State.Mutex.ReleaseMutex() } catch {}
            $State.Mutex.Dispose()
        }
    }
}
