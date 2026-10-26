[CmdletBinding()]
param(
    [string]$RepoRoot = "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS",
    [string]$OverlayZip = (Join-Path $env:USERPROFILE "Downloads\C11D_CONTINUITY_RECONCILIATION_OVERLAY_20261026_V1.zip")
)

$ErrorActionPreference = "Stop"

& {
    $ExpectedOverlaySha = "FB4E337A5C27609E6A0F1E2B02D762095D3C07A3D31EC88F8C56401737803C28"
    $ExpectedOverlayManifestSha = "63039C9C0A040FC92A040A99D7FA4A90418A0683865CC5BAE8397FCAC3435C84"
    $ExpectedC11CManifestSha = "E405D08E4D166B1AD95953558F4A088E73EEA9527E6E89244BEB4096EAC4B953"
    $ExpectedC11CManifestBytes = 796318
    $ExpectedManifestRelative = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    $ManifestName = "C11D_CONTINUITY_RECONCILIATION_OVERLAY_MANIFEST_20261026_V1.json"

    if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
        throw ("REPO_ROOT_MISSING=" + $RepoRoot)
    }
    if (-not (Test-Path -LiteralPath $OverlayZip -PathType Leaf)) {
        throw ("OVERLAY_ZIP_MISSING=" + $OverlayZip)
    }

    $ActualZipSha = (Get-FileHash -LiteralPath $OverlayZip -Algorithm SHA256).Hash.ToUpperInvariant()
    Write-Host ("OVERLAY_ZIP_SHA256=" + $ActualZipSha)
    if ($ActualZipSha -ne $ExpectedOverlaySha) {
        throw ("OVERLAY_ZIP_SHA_MISMATCH expected=" + $ExpectedOverlaySha + " actual=" + $ActualZipSha)
    }

    Write-Host "=== 1. FROZEN C11-C LIVE CHECKOUT GUARD ==="
    $C11CPath = Join-Path $RepoRoot ($ExpectedManifestRelative.Replace('/', '\'))
    if (-not (Test-Path -LiteralPath $C11CPath -PathType Leaf)) {
        throw ("FROZEN_C11C_MANIFEST_MISSING=" + $C11CPath)
    }
    $C11CShaBefore = (Get-FileHash -LiteralPath $C11CPath -Algorithm SHA256).Hash.ToUpperInvariant()
    $C11CLengthBefore = (Get-Item -LiteralPath $C11CPath).Length
    Write-Host ("C11C_MANIFEST_SHA256_BEFORE=" + $C11CShaBefore)
    Write-Host ("C11C_MANIFEST_BYTES_BEFORE=" + $C11CLengthBefore)
    if ($C11CShaBefore -ne $ExpectedC11CManifestSha -or $C11CLengthBefore -ne $ExpectedC11CManifestBytes) {
        throw "FROZEN_C11C_MANIFEST_GUARD_FAILED. No file has been changed. Do not restore the manifest from the uploaded snapshot ZIP; reconcile provenance first."
    }

    Write-Host "=== 2. STAGE AND VERIFY OVERLAY ==="
    $StageRoot = Join-Path $env:TEMP ("C11D_CONTINUITY_OVERLAY_STAGE_" + [Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $StageRoot | Out-Null
    Expand-Archive -LiteralPath $OverlayZip -DestinationPath $StageRoot

    $OverlayManifestPath = Join-Path $StageRoot $ManifestName
    if (-not (Test-Path -LiteralPath $OverlayManifestPath -PathType Leaf)) {
        throw "OVERLAY_MANIFEST_MISSING. Repository has not been changed."
    }
    $ActualOverlayManifestSha = (Get-FileHash -LiteralPath $OverlayManifestPath -Algorithm SHA256).Hash.ToUpperInvariant()
    Write-Host ("OVERLAY_MANIFEST_SHA256=" + $ActualOverlayManifestSha)
    if ($ActualOverlayManifestSha -ne $ExpectedOverlayManifestSha) {
        throw ("OVERLAY_MANIFEST_SHA_MISMATCH expected=" + $ExpectedOverlayManifestSha + " actual=" + $ActualOverlayManifestSha)
    }

    $OverlayManifest = Get-Content -LiteralPath $OverlayManifestPath -Raw | ConvertFrom-Json
    if ($OverlayManifest.schema -ne "C11D-CONTINUITY-RECONCILIATION-OVERLAY-MANIFEST-V1") {
        throw "OVERLAY_MANIFEST_SCHEMA_MISMATCH"
    }
    if ($OverlayManifest.overlay_id -ne "C11D_CONTINUITY_RECONCILIATION_20261026_V1") {
        throw "OVERLAY_ID_MISMATCH"
    }
    if ($OverlayManifest.frozen_c11c_manifest.canonical_sha256 -ne $ExpectedC11CManifestSha -or
        $OverlayManifest.frozen_c11c_manifest.canonical_bytes -ne $ExpectedC11CManifestBytes -or
        $OverlayManifest.frozen_c11c_manifest.snapshot_matches_canonical -ne $false) {
        throw "OVERLAY_C11C_DISCREPANCY_METADATA_MISMATCH"
    }

    $Entries = @($OverlayManifest.files)
    if ($Entries.Count -ne 13) {
        throw ("OVERLAY_TARGET_COUNT_MISMATCH expected=13 actual=" + $Entries.Count)
    }
    $SeenPaths = @{}
    foreach ($Entry in $Entries) {
        $Relative = [string]$Entry.target_path
        if ([string]::IsNullOrWhiteSpace($Relative) -or [System.IO.Path]::IsPathRooted($Relative) -or $Relative -match '(^|[\\/])\.\.([\\/]|$)') {
            throw ("UNSAFE_OVERLAY_RELATIVE_PATH=" + $Relative)
        }
        if ($SeenPaths.ContainsKey($Relative)) {
            throw ("DUPLICATE_OVERLAY_TARGET=" + $Relative)
        }
        $SeenPaths[$Relative] = $true

        $StagePath = Join-Path $StageRoot ($Relative.Replace('/', '\'))
        if (-not (Test-Path -LiteralPath $StagePath -PathType Leaf)) {
            throw ("STAGED_TARGET_MISSING=" + $Relative)
        }
        $StagedSha = (Get-FileHash -LiteralPath $StagePath -Algorithm SHA256).Hash.ToUpperInvariant()
        if ($StagedSha -ne ([string]$Entry.after_sha256).ToUpperInvariant()) {
            throw ("STAGED_TARGET_SHA_MISMATCH=" + $Relative + " actual=" + $StagedSha)
        }

        $TargetPath = Join-Path $RepoRoot ($Relative.Replace('/', '\'))
        if ($Entry.operation -eq "REPLACE_EXACT_SHA256") {
            if (-not (Test-Path -LiteralPath $TargetPath -PathType Leaf)) {
                throw ("REPLACEMENT_TARGET_MISSING=" + $Relative)
            }
            $CurrentSha = (Get-FileHash -LiteralPath $TargetPath -Algorithm SHA256).Hash.ToUpperInvariant()
            if ($CurrentSha -ne ([string]$Entry.before_sha256).ToUpperInvariant()) {
                throw ("REPLACEMENT_PRECONDITION_SHA_MISMATCH=" + $Relative + " actual=" + $CurrentSha)
            }
            if ($Entry.backup_required -ne $true) {
                throw ("REPLACEMENT_BACKUP_POLICY_INVALID=" + $Relative)
            }
        }
        elseif ($Entry.operation -eq "ADD_ONLY") {
            if (Test-Path -LiteralPath $TargetPath) {
                throw ("ADD_ONLY_TARGET_ALREADY_EXISTS=" + $Relative)
            }
            if ($null -ne $Entry.before_sha256 -or $Entry.backup_required -ne $false) {
                throw ("ADD_ONLY_METADATA_INVALID=" + $Relative)
            }
        }
        else {
            throw ("UNKNOWN_OVERLAY_OPERATION=" + [string]$Entry.operation)
        }
        Write-Host ("PREFLIGHT_TARGET_PASS=" + $Relative)
    }

    Write-Host "=== 3. CREATE BACKUPS BEFORE APPLY ==="
    $BackupRoot = Join-Path $env:TEMP ("C11D_CONTINUITY_RECONCILIATION_BACKUP_" + (Get-Date -Format "yyyyMMdd_HHmmss_fff"))
    New-Item -ItemType Directory -Path $BackupRoot | Out-Null
    foreach ($Entry in $Entries | Where-Object { $_.operation -eq "REPLACE_EXACT_SHA256" }) {
        $Relative = [string]$Entry.target_path
        $TargetPath = Join-Path $RepoRoot ($Relative.Replace('/', '\'))
        $BackupPath = Join-Path $BackupRoot ($Relative.Replace('/', '\'))
        $BackupParent = Split-Path -Parent $BackupPath
        if (-not (Test-Path -LiteralPath $BackupParent -PathType Container)) {
            New-Item -ItemType Directory -Path $BackupParent -Force | Out-Null
        }
        Copy-Item -LiteralPath $TargetPath -Destination $BackupPath
        $BackupSha = (Get-FileHash -LiteralPath $BackupPath -Algorithm SHA256).Hash.ToUpperInvariant()
        if ($BackupSha -ne ([string]$Entry.before_sha256).ToUpperInvariant()) {
            throw ("BACKUP_SHA_MISMATCH=" + $Relative)
        }
        Write-Host ("BACKUP_VERIFIED=" + $Relative)
    }

    Write-Host "=== 4. APPLY WITH ROLLBACK ON ERROR ==="
    $Applied = New-Object 'System.Collections.Generic.List[object]'
    try {
        foreach ($Entry in $Entries) {
            $Relative = [string]$Entry.target_path
            $StagePath = Join-Path $StageRoot ($Relative.Replace('/', '\'))
            $TargetPath = Join-Path $RepoRoot ($Relative.Replace('/', '\'))
            $Parent = Split-Path -Parent $TargetPath
            if (-not (Test-Path -LiteralPath $Parent -PathType Container)) {
                New-Item -ItemType Directory -Path $Parent -Force | Out-Null
            }

            # Record before touching destination so rollback also handles a partial Copy-Item.
            $Applied.Add($Entry) | Out-Null
            Copy-Item -LiteralPath $StagePath -Destination $TargetPath -Force
            $NowSha = (Get-FileHash -LiteralPath $TargetPath -Algorithm SHA256).Hash.ToUpperInvariant()
            if ($NowSha -ne ([string]$Entry.after_sha256).ToUpperInvariant()) {
                throw ("POST_APPLY_SHA_MISMATCH=" + $Relative + " actual=" + $NowSha)
            }
        }

        $C11CShaAfter = (Get-FileHash -LiteralPath $C11CPath -Algorithm SHA256).Hash.ToUpperInvariant()
        $C11CLengthAfter = (Get-Item -LiteralPath $C11CPath).Length
        if ($C11CShaAfter -ne $ExpectedC11CManifestSha -or $C11CLengthAfter -ne $ExpectedC11CManifestBytes) {
            throw "FROZEN_C11C_MANIFEST_CHANGED_DURING_APPLY"
        }
        Write-Host ("C11C_MANIFEST_SHA256_AFTER=" + $C11CShaAfter)
        Write-Host ("C11C_MANIFEST_BYTES_AFTER=" + $C11CLengthAfter)
    }
    catch {
        $ApplyError = $_
        Write-Host ("APPLY_ERROR=" + $ApplyError.Exception.Message)
        Write-Host "ROLLBACK_STATUS=STARTED"
        for ($i = $Applied.Count - 1; $i -ge 0; $i--) {
            $Entry = $Applied[$i]
            $Relative = [string]$Entry.target_path
            $TargetPath = Join-Path $RepoRoot ($Relative.Replace('/', '\'))
            try {
                if ($Entry.operation -eq "REPLACE_EXACT_SHA256") {
                    $BackupPath = Join-Path $BackupRoot ($Relative.Replace('/', '\'))
                    Copy-Item -LiteralPath $BackupPath -Destination $TargetPath -Force
                    $RollbackSha = (Get-FileHash -LiteralPath $TargetPath -Algorithm SHA256).Hash.ToUpperInvariant()
                    if ($RollbackSha -ne ([string]$Entry.before_sha256).ToUpperInvariant()) {
                        throw ("ROLLBACK_HASH_MISMATCH=" + $Relative)
                    }
                }
                elseif ($Entry.operation -eq "ADD_ONLY" -and (Test-Path -LiteralPath $TargetPath)) {
                    Remove-Item -LiteralPath $TargetPath -Force
                    if (Test-Path -LiteralPath $TargetPath) {
                        throw ("ROLLBACK_ADD_REMOVE_FAILED=" + $Relative)
                    }
                }
            }
            catch {
                Write-Host ("ROLLBACK_FAILURE=" + $Relative + " | " + $_.Exception.Message)
            }
        }
        Write-Host ("BACKUP_ROOT=" + $BackupRoot)
        throw ("OVERLAY_APPLY_FAILED; inspect rollback messages and backups. Original error: " + $ApplyError.Exception.Message)
    }

    Write-Host "=== 5. FINAL CHECKS ==="
    foreach ($Entry in $Entries) {
        $Relative = [string]$Entry.target_path
        $TargetPath = Join-Path $RepoRoot ($Relative.Replace('/', '\'))
        if (-not (Test-Path -LiteralPath $TargetPath -PathType Leaf)) {
            throw ("FINAL_TARGET_MISSING=" + $Relative)
        }
        $FinalSha = (Get-FileHash -LiteralPath $TargetPath -Algorithm SHA256).Hash.ToUpperInvariant()
        if ($FinalSha -ne ([string]$Entry.after_sha256).ToUpperInvariant()) {
            throw ("FINAL_TARGET_SHA_MISMATCH=" + $Relative + " actual=" + $FinalSha)
        }
        Write-Host ("FINAL_SHA_PASS=" + $Relative)
    }

    $C11CShaFinal = (Get-FileHash -LiteralPath $C11CPath -Algorithm SHA256).Hash.ToUpperInvariant()
    $C11CLengthFinal = (Get-Item -LiteralPath $C11CPath).Length
    if ($C11CShaFinal -ne $ExpectedC11CManifestSha -or $C11CLengthFinal -ne $ExpectedC11CManifestBytes) {
        throw "FINAL_FROZEN_C11C_MANIFEST_GUARD_FAILED"
    }

    Write-Host "OVERLAY_APPLY_STATUS=PASS"
    Write-Host ("TARGET_COUNT=" + $Entries.Count)
    Write-Host "REPLACEMENTS=4"
    Write-Host "ADD_ONLY=9"
    Write-Host ("BACKUP_ROOT=" + $BackupRoot)
    Write-Host ("STAGE_ROOT=" + $StageRoot)
    Write-Host "TESTS_RUN=false"
    Write-Host "RENDERER=OFF"
    Write-Host "MEDIA_CREATED=false"
    Write-Host "PAYLOAD_MATERIALIZED=false"
    Write-Host "APPROVED_BINDINGS=0"
    Write-Host "CANDIDATE_INPUT_ADMISSIBLE=false"
    Write-Host "RELEASE_AUTHORITY=NONE"
}
