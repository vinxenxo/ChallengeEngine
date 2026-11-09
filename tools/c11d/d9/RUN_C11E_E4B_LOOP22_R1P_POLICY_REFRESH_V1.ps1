[CmdletBinding()]
param(
    [string]$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "MISSING_FILE: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$Root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
if ($Root.TrimEnd('\').ToLowerInvariant() -ne $ExpectedRoot.ToLowerInvariant()) {
    throw "ACTIVE_CHECKOUT_PATH_MISMATCH: $Root"
}
Set-Location -LiteralPath $Root
if (-not (Test-Path -LiteralPath '.\project.godot' -PathType Leaf)) { throw 'PROJECT_MARKER_MISSING' }

$FrozenManifest = '.\release\C11C_FREEZE_PACKAGE_MANIFEST.json'
if ((Get-Sha256 $FrozenManifest) -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') {
    throw 'FROZEN_C11C_MANIFEST_MISMATCH'
}

$V7InstallReceipt = '.\artifacts\tests\c11e\r1v_human_acceptance_loop22_handoff_v7\INSTALL_RECEIPT.json'
if ((Get-Sha256 $V7InstallReceipt) -ne '917ea340f345956c40e0fa9e60ba9be2721ca920b8cee867ceffe4bdbca3e15b') {
    throw 'R1V_V7_INSTALL_RECEIPT_MISMATCH'
}
$Closeout = '.\artifacts\tests\c11e\r1v_operator_human_review_closeout\R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json'
if ((Get-Sha256 $Closeout) -ne 'a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a') {
    throw 'R1V_HUMAN_CLOSEOUT_RECEIPT_MISMATCH'
}
$SourceAudit = '.\artifacts\tests\c11e\e4b_loop22_source_reconciliation\LOOP22_READ_ONLY_AUDIT_20261108T232702Z.json'
$SourceAuditSha = '3d5102aa7eca0a4eb50d2532f66459823446855c4ab6c62ae4fccd1e2f817667'
if ((Get-Sha256 $SourceAudit) -ne $SourceAuditSha) { throw 'LOOP22_SOURCE_AUDIT_REPORT_MISMATCH' }
$SourceAuditSidecar = $SourceAudit + '.sha256'
if (-not (Test-Path -LiteralPath $SourceAuditSidecar -PathType Leaf)) { throw 'LOOP22_SOURCE_AUDIT_SIDECAR_MISSING' }
$SideToken = ((Get-Content -LiteralPath $SourceAuditSidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
if ($SideToken -ne $SourceAuditSha) { throw 'LOOP22_SOURCE_AUDIT_SIDECAR_MISMATCH' }

Write-Host '========== C11-E E4B LOOP22 R1P PROJECTION / POLICY REFRESH V1 =========='
Write-Host 'STEP=PRECONDITIONS_PASS'
Write-Host 'FROZEN_C11C_MANIFEST=PASS; R1V_CLOSEOUT=PASS; SOURCE_AUDIT=PASS'

$Python = Get-Command py -ErrorAction Stop
$TestScript = Join-Path $Root 'tools\c11d\d9\test_project_c11e_e4b_r1p_loop22_policy_refresh_v1.py'
$Projector = Join-Path $Root 'tools\c11d\d9\project_c11e_e4b_r1p_loop22_policy_refresh_v1.py'
if (-not (Test-Path -LiteralPath $TestScript -PathType Leaf)) { throw 'PROJECTION_TEST_FILE_MISSING' }
if (-not (Test-Path -LiteralPath $Projector -PathType Leaf)) { throw 'PROJECTION_TOOL_MISSING' }

Write-Host 'STEP=FOCUSED_NEW_PROJECTION_TESTS_10'
& $Python.Source -3.13 -B $TestScript
if ($LASTEXITCODE -ne 0) { throw "PROJECTION_TESTS_FAILED_EXIT_$LASTEXITCODE" }

Write-Host 'STEP=READ_ONLY_27_RECEIPT_PROJECTION_AND_5_POLICY_FINGERPRINTS'
& $Python.Source -3.13 -B $Projector --project-root $Root --source-audit $SourceAudit
$ProjectionExit = $LASTEXITCODE
if ($ProjectionExit -ne 0) { throw "PROJECTION_AUDIT_FAILED_EXIT_$ProjectionExit" }

Write-Host 'GIT=False; GODOT=False; C11C_LAUNCHERS=False; MUSIC=False; FFMPEG=False; FFPROBE=False; RENDERER=False; DISPATCH=False; MEDIA=False'
Write-Host 'LOOP22_MEDIA_AUTHORIZATION=NOT_GRANTED_BY_THIS_REFRESH'
Write-Host 'RELEASE_AUTHORITY=NONE'
