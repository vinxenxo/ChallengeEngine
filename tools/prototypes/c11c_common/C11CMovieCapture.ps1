function Enter-C11CMovieOverride {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$ProjectRoot,
        [Parameter(Mandatory=$false)][int]$Width = 720,
        [Parameter(Mandatory=$false)][int]$Height = 1280
    )
    if ($Width -lt 1 -or $Height -lt 1) { throw 'Movie resolution must be positive.' }
    $overridePath = Join-Path $ProjectRoot 'override.cfg'
    $backupPath = Join-Path ([System.IO.Path]::GetTempPath()) ('C11C_override_backup_' + [Guid]::NewGuid().ToString('N') + '.cfg')
    $hadExisting = Test-Path -LiteralPath $overridePath
    if ($hadExisting) { Copy-Item -LiteralPath $overridePath -Destination $backupPath -Force }
    # C11-B remains frozen at 540x960. This temporary override changes only the effective
    # Movie Maker viewport/window for C11-C delivery; the prototype scene scales its
    # 540x960 logical composition by 4/3 to fill 720x1280.
    $cfg = "[display]`r`n`r`nwindow/size/viewport_width=$Width`r`nwindow/size/viewport_height=$Height`r`nwindow/size/window_width_override=$Width`r`nwindow/size/window_height_override=$Height`r`n"
    [System.IO.File]::WriteAllText($overridePath, $cfg, (New-Object System.Text.UTF8Encoding($false)))
    return [pscustomobject]@{ OverridePath=$overridePath; BackupPath=$backupPath; HadExisting=$hadExisting; Width=$Width; Height=$Height }
}

function Exit-C11CMovieOverride {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)]$State)
    if ($State.HadExisting) {
        if (-not (Test-Path -LiteralPath $State.BackupPath)) { throw "Movie override backup missing: $($State.BackupPath)" }
        Copy-Item -LiteralPath $State.BackupPath -Destination $State.OverridePath -Force
        Remove-Item -LiteralPath $State.BackupPath -Force -ErrorAction SilentlyContinue
    } elseif (Test-Path -LiteralPath $State.OverridePath) {
        Remove-Item -LiteralPath $State.OverridePath -Force
    }
}
