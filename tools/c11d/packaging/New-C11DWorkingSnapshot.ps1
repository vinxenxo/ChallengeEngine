[CmdletBinding()]
param(
    [Parameter()][string]$OutputDirectory = (Join-Path $env:USERPROFILE 'Desktop\C11D_CONTEXT_EXPORT'),
    [Parameter()][string]$ArchiveName = '',
    [Parameter()][ValidateRange(1,4096)][int]$MaxFileMiB = 100,
    [Parameter()][ValidateRange(16,4096)][int]$MaxArchiveMiB = 256,
    [Parameter()][switch]$PreflightOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$ExpectedCManifestSha256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedCManifestBytes = [long]796318
$SnapshotSchema = 'C11D-WORKING-CONTEXT-SNAPSHOT-V3-C11C-PACKAGING-STYLE'
$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..')).TrimEnd([char[]]@('\','/'))
$Encoding = New-Object System.Text.UTF8Encoding($false)

function Get-Sha256Hex {
    param([Parameter(Mandatory=$true)][string]$LiteralPath)
    return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-BytesSha256Hex {
    param([Parameter(Mandatory=$true)][byte[]]$Bytes)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $digest = $sha.ComputeHash($Bytes) } finally { $sha.Dispose() }
    return ([System.BitConverter]::ToString($digest)).Replace('-','').ToLowerInvariant()
}

function Get-StreamSha256Hex {
    param([Parameter(Mandatory=$true)][System.IO.Stream]$Stream)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $digest = $sha.ComputeHash($Stream) } finally { $sha.Dispose() }
    return ([System.BitConverter]::ToString($digest)).Replace('-','').ToLowerInvariant()
}

function Get-RelativePath {
    param([string]$BasePath, [string]$FullPath)
    return $FullPath.Substring($BasePath.Length).TrimStart([char[]]@('\','/')).Replace('\','/')
}

function Get-RelativeSkipReason {
    param([string]$RelativePath, [long]$Length, [int]$MaxMiB, [bool]$IsReparsePoint)
    $p = $RelativePath.Replace('/','\')
    $leaf = [System.IO.Path]::GetFileName($p)
    $lowerLeaf = $leaf.ToLowerInvariant()
    $ext = [System.IO.Path]::GetExtension($p).ToLowerInvariant()
    if ($IsReparsePoint) { return 'REPARSE_POINT_OR_SYMLINK' }
    foreach ($pattern in $script:ExcludeFilePatterns) {
        if ($leaf -like $pattern) { return 'TEMPORARY_BACKUP_OR_ARCHIVE_FILE' }
    }
    if ($ext -in $script:ArchiveExtensions) { return 'NESTED_ARCHIVE_EXCLUDED_TO_AVOID_DUPLICATE_OR_STALE_SNAPSHOT' }
    if ($ext -in $script:GeneratedMediaExtensions) { return 'BINARY_MEDIA_EXCLUDED_FROM_CONTEXT_SNAPSHOT' }
    if ($lowerLeaf -eq '.env' -or ($lowerLeaf.StartsWith('.env.') -and $lowerLeaf -ne '.env.example')) { return 'LOCAL_ENVIRONMENT_FILE' }
    if ($lowerLeaf -in @('id_rsa','id_ed25519','.git-credentials','.npmrc','.pypirc','credentials.json','secrets.json')) { return 'POTENTIAL_CREDENTIAL_FILE' }
    if ($ext -in @('.pem','.pfx','.p12','.key','.kdbx')) { return 'POTENTIAL_PRIVATE_KEY_OR_CREDENTIAL' }
    if ($Length -gt ([long]$MaxMiB * 1MB)) { return 'FILE_EXCEEDS_MAX_FILE_MIB' }
    return $null
}

function Add-SkippedPath {
    param([System.Collections.Generic.List[object]]$List, [string]$Path, [string]$Reason, [long]$Bytes = 0)
    $List.Add([pscustomobject]@{path=$Path;reason=$Reason;bytes=$Bytes})
}

function Add-IncludedFile {
    param(
        [System.Collections.Generic.List[object]]$List,
        [string]$SourcePath,
        [string]$ArchivePath,
        [string]$SourceRelativePath,
        [string]$Category
    )
    $item = Get-Item -LiteralPath $SourcePath
    if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        Add-SkippedPath -List $script:Skipped -Path $SourceRelativePath -Reason 'REPARSE_POINT_OR_SYMLINK' -Bytes ([long]$item.Length)
        return
    }
    $reason = Get-RelativeSkipReason -RelativePath $SourceRelativePath -Length ([long]$item.Length) -MaxMiB $script:MaxFileMiB -IsReparsePoint $false
    if ($null -ne $reason) {
        Add-SkippedPath -List $script:Skipped -Path $SourceRelativePath -Reason $reason -Bytes ([long]$item.Length)
        return
    }
    $hash = Get-Sha256Hex -LiteralPath $SourcePath
    $List.Add([pscustomobject]@{
        source_path=$SourcePath
        archive_path=$ArchivePath.Replace('\','/')
        source_relative_path=$SourceRelativePath.Replace('\','/')
        bytes=[long]$item.Length
        sha256=$hash
        category=$Category
    })
}

function Add-ZipBytes {
    param(
        [Parameter(Mandatory=$true)][System.IO.Compression.ZipArchive]$Archive,
        [Parameter(Mandatory=$true)][string]$EntryName,
        [Parameter(Mandatory=$true)][byte[]]$Bytes
    )
    $entry = $Archive.CreateEntry($EntryName, [System.IO.Compression.CompressionLevel]::Optimal)
    $stream = $entry.Open()
    try { $stream.Write($Bytes, 0, $Bytes.Length) } finally { $stream.Dispose() }
}

$script:MaxFileMiB = $MaxFileMiB
$script:Skipped = New-Object 'System.Collections.Generic.List[object]'
$script:ExcludeFilePatterns = @('*.pyc','*.pyo','*.pyd','*.uid','*.import','*.tmp','*.temp','*.bak','*.old','*.orig','*.swp','*.swo','*~','.DS_Store','Thumbs.db','Desktop.ini','*.coverage','*.dmp','*.stackdump')
$script:ArchiveExtensions = @('.zip','.7z','.rar','.tar','.gz','.tgz','.bz2','.xz')
$script:GeneratedMediaExtensions = @('.mp4','.avi','.mkv','.webm','.mov','.wmv','.flv','.m4v','.mpg','.mpeg','.3gp','.wav','.ogg','.flac','.mp3','.m4a','.aac','.wma','.aiff','.png','.jpg','.jpeg','.jpe','.gif','.webp','.bmp','.tif','.tiff','.heic','.heif','.ico')

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) { throw ('SNAPSHOT_REPO_ROOT_NOT_FOUND=' + $RepoRoot) }
$RequiredPaths = @(
    'AGENTS.md',
    '.continue\rules\CONTINUE.md',
    'project.godot',
    'c11c-suite\self_test.py',
    'tools\qa\c11\run_c11c_challenge_bulk_qa.ps1',
    'tools\maintenance\create_c11c_freeze_zip.ps1',
    'c11c-suite\c11c-maintenance\run_freeze_package.bat',
    'docs\current\c11c\C11-C_2.19_FREEZE_COMMANDS.md',
    'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
)
foreach ($relative in $RequiredPaths) {
    if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot $relative) -PathType Leaf)) {
        throw ('REQUIRED_SOURCE_MISSING=' + $relative)
    }
}

$CManifestPath = Join-Path $RepoRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$CManifestItem = Get-Item -LiteralPath $CManifestPath
if ([long]$CManifestItem.Length -ne $ExpectedCManifestBytes) {
    throw ('C11C_FROZEN_MANIFEST_SIZE_MISMATCH expected=' + $ExpectedCManifestBytes + ' actual=' + $CManifestItem.Length)
}
$CManifestHash = Get-Sha256Hex -LiteralPath $CManifestPath
if ($CManifestHash -ne $ExpectedCManifestSha256) {
    throw ('C11C_FROZEN_MANIFEST_HASH_MISMATCH expected=' + $ExpectedCManifestSha256 + ' actual=' + $CManifestHash)
}

$OutputFull = [System.IO.Path]::GetFullPath($OutputDirectory).TrimEnd([char[]]@('\','/'))
$RootPrefix = $RepoRoot.TrimEnd([char[]]@('\','/')) + '\'
if ($OutputFull.Equals($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
    $OutputFull.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'OUTPUT_DIRECTORY_MUST_BE_OUTSIDE_ACTIVE_CHECKOUT'
}
if ([string]::IsNullOrWhiteSpace($ArchiveName)) { $ArchiveName = 'C11D_WORKING_CONTEXT_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.zip' }
if ([System.IO.Path]::GetFileName($ArchiveName) -ne $ArchiveName -or -not $ArchiveName.EndsWith('.zip',[System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'ARCHIVE_NAME_MUST_BE_A_SINGLE_FILENAME_ENDING_IN_ZIP'
}
$ArchivePath = Join-Path $OutputFull $ArchiveName
if (-not $PreflightOnly) {
    foreach ($candidate in @($ArchivePath, ($ArchivePath + '.sha256'), ($ArchivePath + '.report.json'))) {
        if (Test-Path -LiteralPath $candidate) { throw ('OUTPUT_ALREADY_EXISTS=' + $candidate) }
    }
}

# This follows the C11-C freeze's directory hygiene: artifacts and repository caches/build trees are not recursively packaged.
$ExcludedDirectoryNames = @('.git','.godot','.mono','.import','.vscode','.idea','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.venv','venv','env','artifacts','c11c-studio','c11c-maintenace','node_modules','.cache','bin','obj','coverage')
$ExcludedRelativePrefixes = @('docs/history/root_conflicts/')
$Included = New-Object 'System.Collections.Generic.List[object]'
$Stack = New-Object 'System.Collections.Generic.Stack[string]'
$Stack.Push($RepoRoot)
while ($Stack.Count -gt 0) {
    $CurrentDirectory = $Stack.Pop()
    foreach ($Item in (Get-ChildItem -LiteralPath $CurrentDirectory -Force -ErrorAction Stop)) {
        $Relative = Get-RelativePath -BasePath $RepoRoot -FullPath $Item.FullName
        $HasReparse = (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
        if ($Item.PSIsContainer) {
            if ($HasReparse) {
                Add-SkippedPath -List $script:Skipped -Path $Relative -Reason 'REPARSE_POINT_OR_SYMLINK'
                continue
            }
            if ($Item.Name.ToLowerInvariant() -in $ExcludedDirectoryNames) {
                if ($Item.Name -ieq 'artifacts') {
                    Add-SkippedPath -List $script:Skipped -Path $Relative -Reason 'ARTIFACTS_TREE_EXCLUDED_EXCEPT_COMPACT_EVIDENCE_ALLOWLIST'
                } else {
                    Add-SkippedPath -List $script:Skipped -Path $Relative -Reason 'CACHE_BUILD_OR_RETIRED_DIRECTORY'
                }
                continue
            }
            $normalizedDir = $Relative.Replace('\','/')
            $skipPrefix = $false
            foreach ($prefix in $ExcludedRelativePrefixes) {
                if ($normalizedDir.Equals($prefix.TrimEnd('/'),[StringComparison]::OrdinalIgnoreCase) -or $normalizedDir.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)) { $skipPrefix = $true; break }
            }
            if ($skipPrefix) {
                Add-SkippedPath -List $script:Skipped -Path $Relative -Reason 'HISTORICAL_ROOT_CONFLICT_ARCHIVE'
                continue
            }
            $Stack.Push($Item.FullName)
            continue
        }
        $reason = Get-RelativeSkipReason -RelativePath $Relative -Length ([long]$Item.Length) -MaxMiB $MaxFileMiB -IsReparsePoint $HasReparse
        if ($null -ne $reason) {
            Add-SkippedPath -List $script:Skipped -Path $Relative -Reason $reason -Bytes ([long]$Item.Length)
            continue
        }
        Add-IncludedFile -List $Included -SourcePath $Item.FullName -ArchivePath $Relative -SourceRelativePath $Relative -Category 'WORKTREE_SOURCE'
    }
}

# Preserve only compact acceptance/evidence records from artifacts; do not pull in generated QA corpora or rendered media.
$EvidenceIncludedBefore = $Included.Count
$ExactEvidence = @(
    'artifacts\tests\reports\C11C_2.19.12_ACCEPTANCE_REPORT.json',
    'artifacts\prototypes\c11c_art_direction_review\C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json'
)
foreach ($relative in $ExactEvidence) {
    $path = Join-Path $RepoRoot $relative
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        $archiveRelative = 'C11D_CONTEXT_EVIDENCE\' + $relative.Replace('\','/')
        Add-IncludedFile -List $Included -SourcePath $path -ArchivePath $archiveRelative -SourceRelativePath $relative -Category 'COMPACT_ACCEPTANCE_EVIDENCE'
    }
}
$OperatorEvidenceRoot = Join-Path $RepoRoot 'artifacts\evidence\d9_15_operator'
if (Test-Path -LiteralPath $OperatorEvidenceRoot -PathType Container) {
    foreach ($evidenceFile in (Get-ChildItem -LiteralPath $OperatorEvidenceRoot -Recurse -File -Force -ErrorAction Stop | Sort-Object FullName)) {
        $relative = Get-RelativePath -BasePath $RepoRoot -FullPath $evidenceFile.FullName
        $ext = [System.IO.Path]::GetExtension($evidenceFile.Name).ToLowerInvariant()
        if ($ext -notin @('.json','.md','.txt','.csv')) {
            Add-SkippedPath -List $script:Skipped -Path $relative -Reason 'NON_TEXT_OPERATOR_EVIDENCE_EXCLUDED' -Bytes ([long]$evidenceFile.Length)
            continue
        }
        if ([long]$evidenceFile.Length -gt (10MB)) {
            Add-SkippedPath -List $script:Skipped -Path $relative -Reason 'OPERATOR_EVIDENCE_FILE_EXCEEDS_10MIB' -Bytes ([long]$evidenceFile.Length)
            continue
        }
        $prefix = 'artifacts\evidence\d9_15_operator\'
        $suffix = $relative.Substring($prefix.Length)
        $archiveRelative = 'C11D_CONTEXT_EVIDENCE\d9_15_operator\' + $suffix
        Add-IncludedFile -List $Included -SourcePath $evidenceFile.FullName -ArchivePath $archiveRelative -SourceRelativePath $relative -Category 'D9_15_OPERATOR_EVIDENCE'
    }
}

if ($Included.Count -lt 100) { throw ('INCLUDED_SOURCE_COUNT_SUSPICIOUSLY_LOW=' + $Included.Count) }
$CManifestEntries = @($Included | Where-Object { $_.archive_path -ceq 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' })
if ($CManifestEntries.Count -ne 1 -or $CManifestEntries[0].sha256 -ne $ExpectedCManifestSha256 -or [long]$CManifestEntries[0].bytes -ne $ExpectedCManifestBytes) {
    throw 'CANONICAL_C_MANIFEST_MUST_BE_INCLUDED_EXACTLY_ONCE_WITH_EXPECTED_HASH_AND_SIZE'
}

$SkippedCounts = @{}
foreach ($entry in $script:Skipped) {
    if (-not $SkippedCounts.ContainsKey($entry.reason)) { $SkippedCounts[$entry.reason] = 0 }
    $SkippedCounts[$entry.reason]++
}
$GitCommit = $null
try {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if ($null -ne $git) {
        $gitValue = & $git.Source -C $RepoRoot rev-parse HEAD 2>$null
        if ($LASTEXITCODE -eq 0 -and $gitValue) { $GitCommit = ([string]$gitValue).Trim() }
    }
} catch { }

$Included = @($Included | Sort-Object -Property archive_path)
$SourceIncludedCount = @($Included | Where-Object { $_.category -eq 'WORKTREE_SOURCE' }).Count
$CompactEvidenceCount = $Included.Count - $SourceIncludedCount
$IncludedBytes = [long]0
foreach ($entry in $Included) { $IncludedBytes += [long]$entry.bytes }
Write-Host 'SNAPSHOT_ENTRYPOINT=New-C11DWorkingSnapshot.ps1'
Write-Host ('ACTIVE_CHECKOUT=' + $RepoRoot)
Write-Host ('OUTPUT_DIRECTORY=' + $OutputFull)
Write-Host 'PACKAGING_POLICY=C11C_FREEZE_STYLE_EXCLUDE_ARTIFACTS_CACHES_AND_NESTED_ARCHIVES'
Write-Host ('CANONICAL_C_MANIFEST=PASS sha256=' + $ExpectedCManifestSha256 + ' bytes=' + $ExpectedCManifestBytes)
Write-Host ('SOURCE_FILES_INCLUDED=' + $SourceIncludedCount)
Write-Host ('COMPACT_EVIDENCE_INCLUDED=' + $CompactEvidenceCount)
Write-Host ('INCLUDED_UNCOMPRESSED_BYTES=' + $IncludedBytes)
Write-Host ('MAX_ARCHIVE_MIB=' + $MaxArchiveMiB)
Write-Host ('SKIPPED_PATHS=' + $script:Skipped.Count)
foreach ($reasonName in ($SkippedCounts.Keys | Sort-Object)) { Write-Host ('SKIP_REASON=' + $reasonName + ':' + $SkippedCounts[$reasonName]) }
if ($null -ne $GitCommit) { Write-Host ('GIT_COMMIT=' + $GitCommit) }
if ($PreflightOnly) {
    Write-Host 'C11D_CONTEXT_EXPORT_PREFLIGHT=PASS_NO_FILES_WRITTEN'
    Write-Host 'NEXT_ACTION=REVIEW_SKIPS_THEN_RUN_WITHOUT_PREFLIGHTONLY'
    exit 0
}

$Inventory = New-Object 'System.Collections.Generic.List[object]'
foreach ($entry in $Included) {
    $Inventory.Add([pscustomobject]@{
        path=[string]$entry.archive_path
        source_relative_path=[string]$entry.source_relative_path
        bytes=[long]$entry.bytes
        sha256=[string]$entry.sha256
        category=[string]$entry.category
    })
}
$Readme = @'
# C11-D Working Context Snapshot

This is a filtered copy of the active checkout for source/documentation review. It is not a C11-C freeze, a D release package, a renderer acceptance receipt, or authority to promote a baseline.

Packaging follows the C11-C freeze hygiene where applicable: the entire `artifacts/` tree, caches/build outputs, nested archives, temporary files, local environment files, credentials and generated binary media are omitted. To retain compact provenance, the snapshot may carry the C11-C acceptance report, complete video-review report and text/JSON evidence from `artifacts/evidence/d9_15_operator/` under `C11D_CONTEXT_EVIDENCE/`. These copies do not replace the originals and do not alter the canonical C11-C manifest.

`release/C11C_FREEZE_PACKAGE_MANIFEST.json` is included from the active checkout exactly once and must retain SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` and size 796,318 bytes. The snapshot's own inventory is stored at the archive root as `C11D_CONTEXT_SNAPSHOT_MANIFEST.json`; it never reuses or overwrites the C11-C manifest path.

Review `C11D_CONTEXT_SNAPSHOT_MANIFEST.json` and the external `.report.json` before relying on the package. This archive is for context transfer only; never extract it over the active checkout.
'@
$ReadmeBytes = $Encoding.GetBytes($Readme)
$ReadmeHash = Get-BytesSha256Hex -Bytes $ReadmeBytes
$Inventory.Add([pscustomobject]@{path='C11D_CONTEXT_SNAPSHOT_README.md';source_relative_path=$null;bytes=[long]$ReadmeBytes.Length;sha256=$ReadmeHash;category='SNAPSHOT_METADATA'})
$InventorySorted = @($Inventory | Sort-Object -Property path)
$TreeLines = New-Object 'System.Collections.Generic.List[string]'
foreach ($entry in $InventorySorted) { $TreeLines.Add($entry.path + "`t" + $entry.bytes + "`t" + $entry.sha256) }
$TreeText = ($TreeLines -join "`n") + "`n"
$TreeHash = Get-BytesSha256Hex -Bytes $Encoding.GetBytes($TreeText)
$SnapshotManifest = [ordered]@{
    schema=$SnapshotSchema
    snapshot_kind='FILTERED_ACTIVE_WORKTREE_CONTEXT_NOT_RELEASE_NOT_FREEZE'
    captured_at_utc=[DateTime]::UtcNow.ToString('o')
    source_root=$RepoRoot
    git_commit=$GitCommit
    packaging_reference='tools/maintenance/create_c11c_freeze_zip.ps1'
    canonical_c11c_manifest=[ordered]@{path='release/C11C_FREEZE_PACKAGE_MANIFEST.json';sha256=$ExpectedCManifestSha256;bytes=$ExpectedCManifestBytes;included_exactly_once=$true}
    worktree_source_file_count=$SourceIncludedCount
    compact_evidence_file_count=$CompactEvidenceCount
    payload_file_count_before_snapshot_manifest=$InventorySorted.Count
    archive_entry_count_expected=$InventorySorted.Count+1
    included_uncompressed_bytes=$IncludedBytes
    context_tree_sha256=$TreeHash
    tree_hash_definition='SHA256(UTF8(join LF of sorted archive_path<TAB>size_bytes<TAB>sha256 rows, final LF)); excludes this snapshot manifest only'
    max_file_mib=$MaxFileMiB
    max_archive_mib=$MaxArchiveMiB
    excluded_directory_names=$ExcludedDirectoryNames
    excluded_relative_prefixes=$ExcludedRelativePrefixes
    excluded_file_patterns=$script:ExcludeFilePatterns
    excluded_archive_extensions=$script:ArchiveExtensions
    excluded_binary_media_extensions=$script:GeneratedMediaExtensions
    skip_reason_counts=$SkippedCounts
    skipped_paths_count=$script:Skipped.Count
    skipped_paths=@($script:Skipped | Sort-Object -Property path)
    files=$InventorySorted
    non_claims=@('not a canonical C11-C tree hash','not a freeze package','not a release package','does not prove D render acceptance','does not authorize renderer activation or baseline promotion')
}
$ManifestJson = ($SnapshotManifest | ConvertTo-Json -Depth 12) + "`n"
$ManifestBytes = $Encoding.GetBytes($ManifestJson)
$ManifestHash = Get-BytesSha256Hex -Bytes $ManifestBytes

if (-not (Test-Path -LiteralPath $OutputFull -PathType Container)) { New-Item -ItemType Directory -Path $OutputFull -Force | Out-Null }
$PartialPath = $ArchivePath + '.partial'
if (Test-Path -LiteralPath $PartialPath) { throw ('PARTIAL_ARCHIVE_ALREADY_EXISTS=' + $PartialPath) }
$FileStream = $null
$Zip = $null
try {
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $FileStream = [System.IO.File]::Open($PartialPath,[System.IO.FileMode]::CreateNew,[System.IO.FileAccess]::ReadWrite,[System.IO.FileShare]::None)
    $Zip = [System.IO.Compression.ZipArchive]::new($FileStream,[System.IO.Compression.ZipArchiveMode]::Create,$true,$Encoding)
    foreach ($entry in $Included) {
        $zipEntry = $Zip.CreateEntry([string]$entry.archive_path,[System.IO.Compression.CompressionLevel]::Optimal)
        $sourceStream = $null
        $targetStream = $null
        try {
            $sourceStream = [System.IO.File]::Open([string]$entry.source_path,[System.IO.FileMode]::Open,[System.IO.FileAccess]::Read,[System.IO.FileShare]::ReadWrite)
            $targetStream = $zipEntry.Open()
            $sourceStream.CopyTo($targetStream,1048576)
        } finally {
            if ($null -ne $targetStream) { $targetStream.Dispose() }
            if ($null -ne $sourceStream) { $sourceStream.Dispose() }
        }
        if ([long]$FileStream.Length -gt ([long]$MaxArchiveMiB * 1MB)) { throw ('ARCHIVE_SIZE_LIMIT_EXCEEDED_MIB=' + $MaxArchiveMiB) }
    }
    Add-ZipBytes -Archive $Zip -EntryName 'C11D_CONTEXT_SNAPSHOT_README.md' -Bytes $ReadmeBytes
    Add-ZipBytes -Archive $Zip -EntryName 'C11D_CONTEXT_SNAPSHOT_MANIFEST.json' -Bytes $ManifestBytes
    $Zip.Dispose(); $Zip = $null
    $FileStream.Dispose(); $FileStream = $null
    $PartialBytes = [long](Get-Item -LiteralPath $PartialPath).Length
    if ($PartialBytes -gt ([long]$MaxArchiveMiB * 1MB)) { throw ('ARCHIVE_SIZE_LIMIT_EXCEEDED_MIB=' + $MaxArchiveMiB + '; actual_bytes=' + $PartialBytes) }

    # Verify ZIP CRC by reading each entry and verify payload SHA-256 and sizes before publishing.
    $VerifyZip = [System.IO.Compression.ZipFile]::OpenRead($PartialPath)
    try {
        $ArchiveEntries = @($VerifyZip.Entries)
        $Names = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
        $ExpectedByPath = New-Object 'System.Collections.Generic.Dictionary[string,object]' ([System.StringComparer]::Ordinal)
        foreach ($expected in $InventorySorted) { $ExpectedByPath.Add([string]$expected.path,$expected) }
        $Verified = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
        $CManifestCount = 0
        $SnapshotManifestCount = 0
        foreach ($zipEntry in $ArchiveEntries) {
            $normalized = $zipEntry.FullName.Replace('\','/')
            if (-not $Names.Add($normalized)) { throw ('DUPLICATE_ARCHIVE_ENTRY=' + $normalized) }
            if ($normalized -ceq 'release/C11C_FREEZE_PACKAGE_MANIFEST.json') { $CManifestCount++ }
            if ($normalized -ceq 'C11D_CONTEXT_SNAPSHOT_MANIFEST.json') { $SnapshotManifestCount++ }
            if ($ExpectedByPath.ContainsKey($normalized)) {
                $expected = $ExpectedByPath[$normalized]
                $stream = $zipEntry.Open()
                try { $actualHash = Get-StreamSha256Hex -Stream $stream } finally { $stream.Dispose() }
                if ([long]$zipEntry.Length -ne [long]$expected.bytes -or $actualHash -ne $expected.sha256) {
                    throw ('ARCHIVE_PAYLOAD_HASH_MISMATCH=' + $normalized)
                }
                [void]$Verified.Add($normalized)
            } elseif ($normalized -ceq 'C11D_CONTEXT_SNAPSHOT_MANIFEST.json') {
                $stream = $zipEntry.Open()
                try { $actualManifestHash = Get-StreamSha256Hex -Stream $stream } finally { $stream.Dispose() }
                if ([long]$zipEntry.Length -ne [long]$ManifestBytes.Length -or $actualManifestHash -ne $ManifestHash) {
                    throw 'ARCHIVE_SNAPSHOT_MANIFEST_HASH_MISMATCH'
                }
            } else {
                throw ('UNEXPECTED_ARCHIVE_ENTRY=' + $normalized)
            }
        }
        if ($ArchiveEntries.Count -ne ($InventorySorted.Count+1)) { throw ('ARCHIVE_ENTRY_COUNT_MISMATCH expected=' + ($InventorySorted.Count+1) + ' actual=' + $ArchiveEntries.Count) }
        if ($Verified.Count -ne $InventorySorted.Count) { throw ('ARCHIVE_VERIFIED_PAYLOAD_COUNT_MISMATCH expected=' + $InventorySorted.Count + ' actual=' + $Verified.Count) }
        if ($CManifestCount -ne 1) { throw ('ARCHIVE_C_MANIFEST_ENTRY_COUNT=' + $CManifestCount) }
        if ($SnapshotManifestCount -ne 1) { throw ('ARCHIVE_SNAPSHOT_MANIFEST_ENTRY_COUNT=' + $SnapshotManifestCount) }
    } finally { $VerifyZip.Dispose() }

    [System.IO.File]::Move($PartialPath,$ArchivePath)
    $ZipHash = Get-Sha256Hex -LiteralPath $ArchivePath
    $ZipBytes = (Get-Item -LiteralPath $ArchivePath).Length
    $Sidecar = $ZipHash + '  ' + [System.IO.Path]::GetFileName($ArchivePath) + "`n"
    [System.IO.File]::WriteAllText($ArchivePath + '.sha256',$Sidecar,$Encoding)
    $ExternalReport = [ordered]@{
        schema='C11D-WORKING-CONTEXT-EXPORT-REPORT-V3-C11C-PACKAGING-STYLE'
        archive_path=$ArchivePath
        archive_sha256=$ZipHash
        archive_bytes=$ZipBytes
        archive_maximum_mib=$MaxArchiveMiB
        archive_entries=$ArchiveEntries.Count
        duplicate_entries=0
        canonical_c11c_manifest_sha256=$ExpectedCManifestSha256
        canonical_c11c_manifest_bytes=$ExpectedCManifestBytes
        worktree_source_file_count=$SourceIncludedCount
        compact_evidence_file_count=$CompactEvidenceCount
        included_uncompressed_bytes=$IncludedBytes
        context_tree_sha256=$TreeHash
        snapshot_manifest_sha256=$ManifestHash
        skipped_paths_count=$script:Skipped.Count
        skipped_paths=@($script:Skipped | Sort-Object -Property path)
    }
    [System.IO.File]::WriteAllText($ArchivePath + '.report.json',(($ExternalReport | ConvertTo-Json -Depth 12)+"`n"),$Encoding)
    Write-Host ('ARCHIVE=' + $ArchivePath)
    Write-Host ('ARCHIVE_SHA256=' + $ZipHash)
    Write-Host ('ARCHIVE_BYTES=' + $ZipBytes)
    Write-Host ('ARCHIVE_ENTRIES=' + $ArchiveEntries.Count)
    Write-Host 'DUPLICATE_ARCHIVE_ENTRIES=0'
    Write-Host ('C11C_MANIFEST_IN_ARCHIVE=1/' + $ExpectedCManifestSha256 + '/' + $ExpectedCManifestBytes)
    Write-Host ('SOURCE_FILES_INCLUDED=' + $SourceIncludedCount)
    Write-Host ('COMPACT_EVIDENCE_INCLUDED=' + $CompactEvidenceCount)
    Write-Host ('SKIPPED_PATHS=' + $script:Skipped.Count)
    Write-Host ('CONTEXT_TREE_SHA256=' + $TreeHash)
    Write-Host 'C11D_CONTEXT_EXPORT=PASS_C11C_STYLE_FILTERED_DIRECT_ZIP'
    Write-Host 'NEXT_ACTION=UPLOAD_ZIP_AND_OPTIONAL_REPORT; NEVER_EXTRACT_OVER_ACTIVE_CHECKOUT'
} finally {
    if ($null -ne $Zip) { $Zip.Dispose() }
    if ($null -ne $FileStream) { $FileStream.Dispose() }
    if (Test-Path -LiteralPath $PartialPath -PathType Leaf) { Remove-Item -LiteralPath $PartialPath -Force -ErrorAction SilentlyContinue }
}
