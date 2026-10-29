[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ArchivePath,
    [Parameter()][string]$Root = ''
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$ExpectedCManifestSha256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedCManifestBytes = [long]796318
if ([string]::IsNullOrWhiteSpace($Root)) { $Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..')) }
$Root = (Resolve-Path -LiteralPath $Root).Path
$ArchivePath = (Resolve-Path -LiteralPath $ArchivePath).Path
$SidecarPath = $ArchivePath + '.sha256'
$ReportPath = $ArchivePath + '.report.json'
foreach ($path in @($SidecarPath,$ReportPath)) { if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('SNAPSHOT_SIDECAR_MISSING=' + $path) } }
function Get-Sha256Lower([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Get-BytesSha256Lower([byte[]]$Bytes) { $sha=[Security.Cryptography.SHA256]::Create(); try { return ([BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant() } finally { $sha.Dispose() } }
function Get-StreamSha256Lower([System.IO.Stream]$Stream) { $sha=[Security.Cryptography.SHA256]::Create(); try { return ([BitConverter]::ToString($sha.ComputeHash($Stream))).Replace('-','').ToLowerInvariant() } finally { $sha.Dispose() } }
function Read-EntryBytes([System.IO.Compression.ZipArchiveEntry]$Entry) { $stream=$Entry.Open(); try { $memory=New-Object IO.MemoryStream; try { $stream.CopyTo($memory); return ,$memory.ToArray() } finally { $memory.Dispose() } } finally { $stream.Dispose() } }

$archiveHash = Get-Sha256Lower $ArchivePath
$archiveBytes = [long](Get-Item -LiteralPath $ArchivePath).Length
$sidecarText = Get-Content -LiteralPath $SidecarPath -Raw -Encoding UTF8
if ($sidecarText -notmatch '(?m)^([a-fA-F0-9]{64})\s+') { throw 'SNAPSHOT_SIDECAR_FORMAT_INVALID' }
$sidecarHash = $Matches[1].ToLowerInvariant()
if ($sidecarHash -ne $archiveHash) { throw ('SNAPSHOT_SIDECAR_SHA256_MISMATCH expected=' + $sidecarHash + '; actual=' + $archiveHash) }
$report = Get-Content -LiteralPath $ReportPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$report.schema -ne 'C11D-WORKING-CONTEXT-EXPORT-REPORT-V3-C11C-PACKAGING-STYLE') { throw ('SNAPSHOT_REPORT_SCHEMA_MISMATCH=' + [string]$report.schema) }
if ([string]$report.archive_sha256 -ne $archiveHash -or [long]$report.archive_bytes -ne $archiveBytes) { throw 'SNAPSHOT_REPORT_ARCHIVE_IDENTITY_MISMATCH' }
if ([int]$report.duplicate_entries -ne 0) { throw ('SNAPSHOT_REPORT_DUPLICATES_NONZERO=' + [string]$report.duplicate_entries) }
if ([long]$report.archive_maximum_mib -lt 1 -or $archiveBytes -gt ([long]$report.archive_maximum_mib * 1MB)) { throw 'SNAPSHOT_EXCEEDS_DECLARED_ARCHIVE_LIMIT' }

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($ArchivePath)
try {
    $nameSet = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    $entryMap = @{}
    foreach ($entry in $zip.Entries) {
        $name = [string]$entry.FullName.Replace('\','/')
        if ([string]::IsNullOrWhiteSpace($name) -or $name.StartsWith('/') -or $name -match '^[A-Za-z]:' -or @($name.Split('/') | Where-Object { $_ -eq '..' -or $_ -eq '' }).Count -gt 0) { throw ('UNSAFE_SNAPSHOT_ENTRY=' + $name) }
        if (-not $nameSet.Add($name)) { throw ('DUPLICATE_SNAPSHOT_ENTRY=' + $name) }
        if ($name -match '^(?i:artifacts)/' -or $name -match '(?i)(^|/)\.git(/|$)' -or $name -match '(?i)(^|/)__pycache__(/|$)' -or [IO.Path]::GetExtension($name).ToLowerInvariant() -in @('.zip','.7z','.rar','.tar','.gz','.tgz','.bz2','.xz','.mp4','.avi','.mkv','.webm','.mov','.wmv','.flv','.m4v','.mpg','.mpeg','.wav','.ogg','.flac','.mp3','.m4a','.aac','.wma','.aiff','.png','.jpg','.jpeg','.gif','.webp','.bmp','.tif','.tiff','.heic','.heif','.ico')) {
            throw ('FORBIDDEN_SNAPSHOT_ENTRY=' + $name)
        }
        $entryMap[$name] = $entry
    }
    if (-not $entryMap.ContainsKey('C11D_CONTEXT_SNAPSHOT_MANIFEST.json')) { throw 'SNAPSHOT_INTERNAL_MANIFEST_MISSING' }
    if (-not $entryMap.ContainsKey('C11D_CONTEXT_SNAPSHOT_README.md')) { throw 'SNAPSHOT_INTERNAL_README_MISSING' }
    $manifestBytes = Read-EntryBytes $entryMap['C11D_CONTEXT_SNAPSHOT_MANIFEST.json']
    $manifestHash = Get-BytesSha256Lower $manifestBytes
    $manifest = [Text.Encoding]::UTF8.GetString($manifestBytes) | ConvertFrom-Json
    if ([string]$manifest.schema -ne 'C11D-WORKING-CONTEXT-SNAPSHOT-V3-C11C-PACKAGING-STYLE') { throw ('SNAPSHOT_MANIFEST_SCHEMA_MISMATCH=' + [string]$manifest.schema) }
    if ([string]$manifest.snapshot_kind -ne 'FILTERED_ACTIVE_WORKTREE_CONTEXT_NOT_RELEASE_NOT_FREEZE') { throw 'SNAPSHOT_KIND_CLAIM_INVALID' }
    if ([string]$manifest.canonical_c11c_manifest.sha256 -ne $ExpectedCManifestSha256 -or [long]$manifest.canonical_c11c_manifest.bytes -ne $ExpectedCManifestBytes -or $manifest.canonical_c11c_manifest.included_exactly_once -ne $true) { throw 'SNAPSHOT_INTERNAL_C_MANIFEST_PIN_MISMATCH' }
    if ([string]$report.snapshot_manifest_sha256 -ne $manifestHash) { throw 'SNAPSHOT_EXTERNAL_INTERNAL_MANIFEST_HASH_MISMATCH' }
    if ([string]$report.context_tree_sha256 -ne [string]$manifest.context_tree_sha256) { throw 'SNAPSHOT_EXTERNAL_INTERNAL_TREE_HASH_MISMATCH' }
    if ([int]$manifest.archive_entry_count_expected -ne $zip.Entries.Count) { throw ('SNAPSHOT_ENTRY_COUNT_MISMATCH manifest=' + [string]$manifest.archive_entry_count_expected + '; actual=' + $zip.Entries.Count) }
    if ([int]$report.archive_entries -ne $zip.Entries.Count) { throw 'SNAPSHOT_REPORT_ENTRY_COUNT_MISMATCH' }
    if ([int]$manifest.payload_file_count_before_snapshot_manifest -ne $manifest.files.Count) { throw 'SNAPSHOT_MANIFEST_INVENTORY_COUNT_MISMATCH' }

    $manifestEntryCount = 0
    $verifiedCount = 0
    $treeRows = New-Object 'System.Collections.Generic.List[string]'
    foreach ($item in $manifest.files) {
        $path = [string]$item.path
        if (-not $entryMap.ContainsKey($path)) { throw ('SNAPSHOT_INVENTORY_PATH_MISSING=' + $path) }
        if ($path -ceq 'release/C11C_FREEZE_PACKAGE_MANIFEST.json') { $manifestEntryCount++ }
        $entry = $entryMap[$path]
        if ([long]$entry.Length -ne [long]$item.bytes) { throw ('SNAPSHOT_ENTRY_SIZE_MISMATCH=' + $path) }
        $stream = $entry.Open()
        try { $actualEntryHash = Get-StreamSha256Lower $stream } finally { $stream.Dispose() }
        if ($actualEntryHash -ne [string]$item.sha256) { throw ('SNAPSHOT_ENTRY_SHA256_MISMATCH=' + $path) }
        $treeRows.Add($path + "`t" + [string]$item.bytes + "`t" + [string]$item.sha256)
        $verifiedCount++
    }
    if ($manifestEntryCount -ne 1) { throw ('SNAPSHOT_C_MANIFEST_COUNT=' + $manifestEntryCount) }
    $cEntry = $entryMap['release/C11C_FREEZE_PACKAGE_MANIFEST.json']
    if ([long]$cEntry.Length -ne $ExpectedCManifestBytes) { throw 'SNAPSHOT_CANONICAL_C_MANIFEST_SIZE_MISMATCH' }
    $cStream = $cEntry.Open()
    try { $cHash = Get-StreamSha256Lower $cStream } finally { $cStream.Dispose() }
    if ($cHash -ne $ExpectedCManifestSha256) { throw 'SNAPSHOT_CANONICAL_C_MANIFEST_SHA256_MISMATCH' }
    $treeText = ($treeRows -join "`n") + "`n"
    $treeHash = Get-BytesSha256Lower ([Text.Encoding]::UTF8.GetBytes($treeText))
    if ($treeHash -ne [string]$manifest.context_tree_sha256) { throw ('SNAPSHOT_TREE_SHA256_MISMATCH expected=' + [string]$manifest.context_tree_sha256 + '; actual=' + $treeHash) }

    $requiredEntries = @(
        'docs/current/d/C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V3.md',
        'docs/current/d/C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V3.md',
        'docs/current/d/C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V3.md',
        'docs/current/d/C11D_ROOT_DOCUMENTATION_REORGANIZATION_POLICY_20261029_V1.md',
        'docs/current/d/C11D_ROOT_DOCUMENTATION_SNAPSHOT_AUDIT_20261029_V1.md',
        'docs/current/d/C11D_SNAPSHOT_VALIDATION_AND_DOCUMENTATION_REORGANIZATION_20261029_V2.md',
        'docs/current/d/C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.md',
        'docs/current/d/C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json',
        'docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.md',
        'docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.json',
        'prompts/C11D_D_RENDER_INTEGRATION_INITIAL_PROMPT_20261029_V3.md',
        'prompts/C11D_D_RENDER_INTEGRATION_MASTER_PROMPT_20261029_V3.md',
        'prompts/C11D_D_RENDER_INTEGRATION_OVERHAND_PROMPT_20261029_V3.md',
        'prompts/C11D_D_RENDER_INTEGRATION_START_PROMPT_20261029_V3.md',
        'prompts/C11D_D_RENDER_INTEGRATION_CONTINUATION_PROMPT_20261029_V2.md',
        'tools/c11d/documentation/organize_c11d_root_documentation.ps1',
        'tools/c11d/documentation/organize_c11d_documentation.ps1',
        'tools/c11d/documentation/Test-C11DDocumentationReorganization.ps1',
        'tools/c11d/packaging/Test-C11DWorkingSnapshot.ps1'
    )
    foreach ($required in $requiredEntries) { if (-not $entryMap.ContainsKey($required)) { throw ('REQUIRED_NEXT_CONTEXT_ENTRY_MISSING=' + $required) } }
    Write-Host ('SNAPSHOT_SHA256=PASS:' + $archiveHash)
    Write-Host ('SNAPSHOT_MANIFEST_SHA256=PASS:' + $manifestHash)
    Write-Host ('SNAPSHOT_TREE_SHA256=PASS:' + $treeHash)
    Write-Host ('SNAPSHOT_ZIP_ENTRIES=' + $zip.Entries.Count)
    Write-Host ('SNAPSHOT_PAYLOAD_HASHES_VERIFIED=' + $verifiedCount)
    Write-Host 'SNAPSHOT_C11C_MANIFEST=PASS_EXACTLY_ONCE'
    Write-Host 'SNAPSHOT_NEXT_CONTEXT_DOCUMENTATION=PASS'
    Write-Host 'C11D_WORKING_SNAPSHOT_VALIDATION=PASS'
} finally {
    $zip.Dispose()
}
