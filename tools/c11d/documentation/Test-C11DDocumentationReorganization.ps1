[CmdletBinding()]
param(
    [Parameter()][string]$Root = '',
    [Parameter()][switch]$ApplyRootMigration,
    [Parameter()][switch]$GenerateSnapshot,
    [Parameter()][string]$OutputDirectory = (Join-Path $env:USERPROFILE 'Desktop\C11D_CONTEXT_EXPORT')
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
if ([string]::IsNullOrWhiteSpace($Root)) { $Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..')) }
$Root = (Resolve-Path -LiteralPath $Root).Path
if ($GenerateSnapshot -and -not $ApplyRootMigration) { throw 'GENERATE_SNAPSHOT_REQUIRES_-ApplyRootMigration_TO_REBUILD_MAP_AND_CATALOG_FIRST' }
$ExpectedPins = @(
    [pscustomobject]@{path='AGENTS.md';sha256='0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37'},
    [pscustomobject]@{path='.continue/rules/CONTINUE.md';sha256='52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86'},
    [pscustomobject]@{path='release/C11C_FREEZE_PACKAGE_MANIFEST.json';sha256='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953';bytes=796318}
)
function Get-Sha256Lower([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Assert-PowerShellSyntax([string]$Path) {
    $tokens = $null; $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($Path,[ref]$tokens,[ref]$parseErrors) | Out-Null
    if ($parseErrors.Count -gt 0) { throw ('POWERSHELL_SYNTAX_FAIL=' + $Path + '; ' + (($parseErrors | ForEach-Object { $_.Message }) -join ' | ')) }
}
foreach ($pin in $ExpectedPins) {
    $path = Join-Path $Root ($pin.path.Replace('/','\'))
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('CORE_PIN_MISSING=' + $pin.path) }
    if ((Get-Sha256Lower $path) -ne $pin.sha256) { throw ('CORE_PIN_MISMATCH=' + $pin.path) }
    $bytesProperty = $pin.PSObject.Properties['bytes']
    if ($null -ne $bytesProperty -and $null -ne $bytesProperty.Value -and [long](Get-Item -LiteralPath $path).Length -ne [long]$bytesProperty.Value) { throw ('CORE_PIN_SIZE_MISMATCH=' + $pin.path) }
}
$rootOrganizer = Join-Path $Root 'tools\c11d\documentation\organize_c11d_root_documentation.ps1'
$catalogOrganizer = Join-Path $Root 'tools\c11d\documentation\organize_c11d_documentation.ps1'
$snapshotScript = Join-Path $Root 'tools\c11d\packaging\New-C11DWorkingSnapshot.ps1'
$snapshotTester = Join-Path $Root 'tools\c11d\packaging\Test-C11DWorkingSnapshot.ps1'
foreach ($script in @($rootOrganizer,$catalogOrganizer,$snapshotScript,$snapshotTester,$PSCommandPath)) {
    if (-not (Test-Path -LiteralPath $script -PathType Leaf)) { throw ('REQUIRED_TEST_SCRIPT_MISSING=' + $script) }
    Assert-PowerShellSyntax $script
}
Write-Host 'POWERSHELL_SYNTAX=PASS_ROOT_ORGANIZER_CATALOG_GENERATOR_SNAPSHOT_GENERATOR_AND_TESTS'

Write-Host 'STEP=ROOT_DOCUMENTATION_PREFLIGHT'
& $rootOrganizer -Root $Root -PreflightOnly
if ($ApplyRootMigration) {
    Write-Host 'STEP=ROOT_DOCUMENTATION_APPLY'
    & $rootOrganizer -Root $Root -Apply
}
if (-not $ApplyRootMigration) {
    Write-Host 'C11D_DOCUMENTATION_REORGANIZATION_TEST=PASS_PREFLIGHT_ONLY_NO_MUTATION'
    Write-Host 'NEXT_ACTION=REVIEW_ROOT_MIGRATION_PLAN_THEN_RUN_WITH_-ApplyRootMigration_-GenerateSnapshot'
    exit 0
}

Write-Host 'STEP=CATALOG_PREFLIGHT'
& $catalogOrganizer -Root $Root -PreflightOnly
Write-Host 'STEP=CATALOG_GENERATION'
& $catalogOrganizer -Root $Root
$mapPath = Join-Path $Root 'docs\current\d\C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json'
$mapMdPath = Join-Path $Root 'docs\current\d\C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.md'
$catalogPath = Join-Path $Root 'docs\current\d\C11D_DOCUMENTATION_CATALOG_GENERATED.json'
$catalogMdPath = Join-Path $Root 'docs\current\d\C11D_DOCUMENTATION_CATALOG_GENERATED.md'
foreach ($path in @($mapPath,$mapMdPath,$catalogPath,$catalogMdPath)) { if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('GENERATED_DOCUMENTATION_OUTPUT_MISSING=' + $path) } }
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$catalog = Get-Content -LiteralPath $catalogPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$map.schema -ne 'C11D-ROOT-DOCUMENTATION-MIGRATION-MAP-V1') { throw 'ROOT_MIGRATION_MAP_SCHEMA_FAIL' }
if ([string]$catalog.schema -ne 'C11D-LIVE-DOCUMENTATION-CATALOG-V1') { throw 'DOCUMENTATION_CATALOG_SCHEMA_FAIL' }
$catalogByPath = @{}
foreach ($item in $catalog.files) { $catalogByPath[[string]$item.path] = $item }
$movedCount = 0
$retainedCount = 0
foreach ($entry in $map.entries) {
    $action = [string]$entry.action
    $destination = [string]$entry.destination
    if ($action -eq 'MOVED' -or $action -eq 'DEDUPLICATED_IDENTICAL') {
        $target = Join-Path $Root ($destination.Replace('/','\'))
        if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw ('MIGRATED_DOCUMENT_MISSING=' + $destination) }
        if ((Get-Sha256Lower $target) -ne [string]$entry.sha256) { throw ('MIGRATED_DOCUMENT_HASH_MISMATCH=' + $destination) }
        if (-not $catalogByPath.ContainsKey($destination)) { throw ('MIGRATED_DOCUMENT_NOT_IN_LIVE_CATALOG=' + $destination) }
        if ([string]$catalogByPath[$destination].sha256 -ne [string]$entry.sha256) { throw ('CATALOG_HASH_MISMATCH=' + $destination) }
        $movedCount++
    } elseif ($action -like 'RETAIN_*') {
        $source = Join-Path $Root ([string]$entry.source)
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw ('RETAINED_ROOT_DOCUMENT_MISSING=' + [string]$entry.source) }
        if ((Get-Sha256Lower $source) -ne [string]$entry.sha256) { throw ('RETAINED_ROOT_DOCUMENT_HASH_MISMATCH=' + [string]$entry.source) }
        $retainedCount++
    }
}
Write-Host ('ROOT_DOCUMENTS_HASH_VERIFIED=' + $movedCount)
Write-Host ('ROOT_DOCUMENTS_RETAINED_WITH_REASON=' + $retainedCount)
Write-Host ('LIVE_CATALOG_ENTRIES=' + [string]$catalog.entry_count)
Write-Host ('CATALOG_SHA256=' + (Get-Sha256Lower $catalogPath))
Write-Host ('ROOT_MIGRATION_MAP_SHA256=' + (Get-Sha256Lower $mapPath))

if ($GenerateSnapshot) {
    Write-Host 'STEP=SNAPSHOT_PREFLIGHT'
    & $snapshotScript -OutputDirectory $OutputDirectory -PreflightOnly
    $before = @()
    if (Test-Path -LiteralPath $OutputDirectory -PathType Container) {
        $before = @(Get-ChildItem -LiteralPath $OutputDirectory -File -Filter 'C11D_WORKING_CONTEXT_*.zip' | ForEach-Object { $_.FullName })
    }
    Write-Host 'STEP=SNAPSHOT_GENERATION'
    $outputLines = @(& $snapshotScript -OutputDirectory $OutputDirectory 2>&1)
    foreach ($line in $outputLines) { Write-Host ([string]$line) }
    $archivePath = $null
    foreach ($line in $outputLines) {
        $lineText = [string]$line
        if ($lineText.StartsWith('ARCHIVE=')) { $archivePath = $lineText.Substring('ARCHIVE='.Length).Trim() }
    }
    if ([string]::IsNullOrWhiteSpace($archivePath)) {
        $latest = Get-ChildItem -LiteralPath $OutputDirectory -File -Filter 'C11D_WORKING_CONTEXT_*.zip' | Sort-Object -Property LastWriteTimeUtc -Descending | Select-Object -First 1
        if ($null -ne $latest) { $archivePath = $latest.FullName }
    }
    if ([string]::IsNullOrWhiteSpace($archivePath) -or -not (Test-Path -LiteralPath $archivePath -PathType Leaf)) { throw 'NEW_SNAPSHOT_ARCHIVE_NOT_FOUND' }
    $newArchive = (Resolve-Path -LiteralPath $archivePath).Path
    if ($before -contains $newArchive) { throw ('SNAPSHOT_ARCHIVE_WAS_NOT_NEW=' + $newArchive) }
    Write-Host 'STEP=INDEPENDENT_SNAPSHOT_VALIDATION'
    & $snapshotTester -Root $Root -ArchivePath $newArchive
    Write-Host ('NEXT_CONTEXT_SNAPSHOT=' + $newArchive)
    Write-Host ('NEXT_CONTEXT_SNAPSHOT_SHA256=' + (Get-Sha256Lower $newArchive))
}
Write-Host 'C11D_DOCUMENTATION_REORGANIZATION_TEST=PASS_ROOT_MIGRATION_CATALOG_AND_HASH_INTEGRITY'
if ($GenerateSnapshot) { Write-Host 'C11D_DOCUMENTATION_OVERLAY_TESTS=PASS_INCLUDING_NEW_SNAPSHOT' }
