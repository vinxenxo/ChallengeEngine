param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PackageRoot
)
$ErrorActionPreference = 'Stop'
$InstallerPath = $MyInvocation.MyCommand.Path
$Tokens = $null; $ParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($InstallerPath,[ref]$Tokens,[ref]$ParseErrors) | Out-Null
if ($ParseErrors.Count -gt 0) { throw 'INSTALLER_POWERSHELL_AST_PARSE_FAILED' }
$RunnerAst = Join-Path $PackageRoot 'payload\tools\c11d\d9\RUN_C11E_E6_COMPOSITION_READINESS_AUDIT_V2.ps1'
if (-not (Test-Path -LiteralPath $RunnerAst -PathType Leaf)) { throw 'RUNNER_PAYLOAD_MISSING' }
$RunnerTokens = $null; $RunnerErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($RunnerAst,[ref]$RunnerTokens,[ref]$RunnerErrors) | Out-Null
if ($RunnerErrors.Count -gt 0) { throw 'RUNNER_POWERSHELL_AST_PARSE_FAILED' }
$ManifestPath = Join-Path $PackageRoot 'PACKAGE_MANIFEST_V2.json'
$ManifestSidecar = $ManifestPath + '.sha256'
if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf) -or -not (Test-Path -LiteralPath $ManifestSidecar -PathType Leaf)) { throw 'PACKAGE_MANIFEST_OR_SIDECAR_MISSING' }
$ManifestSidecarParts = ([IO.File]::ReadAllText($ManifestSidecar).Trim() -split '\s+',2)
if ($ManifestSidecarParts.Count -ne 2 -or $ManifestSidecarParts[1] -ne 'PACKAGE_MANIFEST_V2.json' -or $ManifestSidecarParts[0] -notmatch '^[0-9a-fA-F]{64}$') { throw 'PACKAGE_MANIFEST_SIDECAR_INVALID' }
$ManifestSha = (Get-FileHash -LiteralPath $ManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ManifestSha -ne $ManifestSidecarParts[0].ToLowerInvariant()) { throw "PACKAGE_MANIFEST_SHA256_MISMATCH:$ManifestSha" }
$Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if ($Manifest.schema -ne 'C11E-E6-COMPOSITION-READINESS-PACKAGE-MANIFEST-V2' -or $Manifest.policy -ne 'ADD_ONLY') { throw 'PACKAGE_MANIFEST_SCHEMA_OR_POLICY_INVALID' }
$Root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$PayloadRoot = Join-Path $PackageRoot 'payload'
$Rows = @()
foreach ($Entry in $Manifest.files) {
    $Rel = [string]$Entry.path
    if ([string]::IsNullOrWhiteSpace($Rel) -or $Rel.Contains('..') -or [IO.Path]::IsPathRooted($Rel)) { throw "UNSAFE_PACKAGE_RELATIVE_PATH:$Rel" }
    $Source = Join-Path $PayloadRoot ($Rel.Replace('/','\'))
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) { throw "PAYLOAD_FILE_MISSING:$Rel" }
    $Info = Get-Item -LiteralPath $Source
    $Hash = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Info.Length -ne [int64]$Entry.bytes -or $Hash -ne ([string]$Entry.sha256).ToLowerInvariant()) { throw "PAYLOAD_IDENTITY_MISMATCH:$Rel" }
    $Dest = Join-Path $Root ($Rel.Replace('/','\'))
    $Disposition = 'ADD'
    if (Test-Path -LiteralPath $Dest -PathType Leaf) {
        $Existing = Get-Item -LiteralPath $Dest
        $ExistingHash = (Get-FileHash -LiteralPath $Dest -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($Existing.Length -eq [int64]$Entry.bytes -and $ExistingHash -eq ([string]$Entry.sha256).ToLowerInvariant()) { $Disposition = 'IDENTICAL' }
        else { throw "ADD_ONLY_COLLISION:$Rel" }
    } elseif (Test-Path -LiteralPath $Dest) { throw "DESTINATION_NOT_FILE:$Rel" }
    $Rows += [pscustomobject]@{ path=$Rel; source=$Source; destination=$Dest; bytes=[int64]$Entry.bytes; sha256=$Hash; disposition=$Disposition }
}
foreach ($Pin in $Manifest.protected_preconditions) {
    $Path = Join-Path $Root ($Pin.path.Replace('/','\'))
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "PROTECTED_PRECONDITION_MISSING:$($Pin.path)" }
    $Actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Actual -ne $Pin.sha256.ToLowerInvariant()) { throw "PROTECTED_PRECONDITION_MISMATCH:$($Pin.path):$Actual" }
}
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/INSTALLER_AND_RUNNER'
Write-Host "PACKAGE_MANIFEST_SHA256=PASS/$ManifestSha"
Write-Host ("PAYLOAD_PREFLIGHT=PASS/{0}" -f $Rows.Count)
Write-Host 'DESTINATION_COLLISION_PREFLIGHT=PASS'
Write-Host 'PROTECTED_PRECONDITIONS=PASS/2'
$RunId = 'E6COMPINSTV2_' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmss') + '_' + ([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$JournalRoot = Join-Path $Root ('artifacts\tests\c11e\e6_composition_readiness_install_v2\' + $RunId)
New-Item -ItemType Directory -Path $JournalRoot -Force | Out-Null
$Added = 0; $Identical = 0; $Receipts = @()
foreach ($Row in $Rows) {
    if ($Row.disposition -eq 'IDENTICAL') { $Identical++; $Receipts += [pscustomobject]@{path=$Row.path;disposition='IDENTICAL_SKIPPED';bytes=$Row.bytes;sha256=$Row.sha256}; continue }
    $Parent = Split-Path -Parent $Row.destination
    if (-not (Test-Path -LiteralPath $Parent)) { New-Item -ItemType Directory -Path $Parent -Force | Out-Null }
    $Bytes = [IO.File]::ReadAllBytes($Row.source)
    $Stream = [IO.File]::Open($Row.destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $Stream.Write($Bytes,0,$Bytes.Length); $Stream.Flush($true) } finally { $Stream.Dispose() }
    $Post = (Get-FileHash -LiteralPath $Row.destination -Algorithm SHA256).Hash.ToLowerInvariant()
    $PostBytes = (Get-Item -LiteralPath $Row.destination).Length
    if ($Post -ne $Row.sha256 -or $PostBytes -ne $Row.bytes) { throw "POSTIMAGE_VERIFICATION_FAILED:$($Row.path)" }
    $Added++
    $Receipts += [pscustomobject]@{path=$Row.path;disposition='ADDED_POSTIMAGE_VERIFIED';bytes=$Row.bytes;sha256=$Post}
}
$Postconditions = @()
foreach ($Pin in $Manifest.protected_preconditions) {
    $Path = Join-Path $Root ($Pin.path.Replace('/','\'))
    $Actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    $Postconditions += [pscustomobject]@{path=$Pin.path;sha256=$Actual;status=$(if($Actual -eq $Pin.sha256.ToLowerInvariant()){'PASS'}else{'FAIL'})}
    if ($Actual -ne $Pin.sha256.ToLowerInvariant()) { throw "PROTECTED_POSTCONDITION_FAILED:$($Pin.path)" }
}
$Receipt = [ordered]@{
 schema='C11E-E6-COMPOSITION-READINESS-INSTALL-RECEIPT-V2'; schema_version='2.0'; run_id=$RunId
 status='PASS_ADD_ONLY_E6_COMPOSITION_READINESS_INSTALL_V2'; project_root=$Root; package_manifest_sha256=$ManifestSha
 payload_expected=$Rows.Count; payload_added=$Added; payload_identical=$Identical
 files=$Receipts; protected_preconditions_post=$Postconditions
 governance=[ordered]@{git_checks='SKIPPED';commits='OPERATOR_MANAGED';source_file_pins='ENFORCED';d4_8='BLOCKED';e6_test_only_authorized=$false;renderer='OFF';release_authority='NONE'}
}
$ReceiptPath = Join-Path $JournalRoot 'INSTALL_RECEIPT_V2.json'
$ReceiptText = $Receipt | ConvertTo-Json -Depth 8
[IO.File]::WriteAllText($ReceiptPath,$ReceiptText,[Text.Encoding]::UTF8)
$ReceiptSha = (Get-FileHash -LiteralPath $ReceiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText(($ReceiptPath+'.sha256'),("{0}  {1}`n" -f $ReceiptSha,(Split-Path -Leaf $ReceiptPath)),[Text.Encoding]::ASCII)
Write-Host 'INSTALL_STATUS=PASS_ADD_ONLY_E6_COMPOSITION_READINESS_INSTALL_V2'
Write-Host "INSTALL_FILES=$($Rows.Count)/$($Rows.Count)"
Write-Host "INSTALL_ADDED=$Added; IDENTICAL_SKIPPED=$Identical"
Write-Host "INSTALL_RECEIPT=$ReceiptPath"
Write-Host "INSTALL_RECEIPT_SHA256=$ReceiptSha"
Write-Host 'D4_8=BLOCKED; E6_TEST_ONLY_AUTHORIZED=FALSE; RENDERER=OFF; RELEASE_AUTHORITY=NONE'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED'
Write-Host 'E6_COMPOSITION_READINESS_INSTALL_V2_FINAL=PASS'
exit 0
