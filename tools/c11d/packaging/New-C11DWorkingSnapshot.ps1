[CmdletBinding()]
param(
    [Parameter()][string]$OutputDirectory = (Join-Path $env:USERPROFILE 'Desktop\C11D_CONTEXT_EXPORT'),
    [Parameter()][string]$ArchiveName = '',
    [Parameter()][ValidateRange(1,4096)][int]$MaxFileMiB = 250,
    [Parameter()][switch]$PreflightOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$ExpectedCManifestSha256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedCManifestBytes = [long]796318
$SnapshotSchema = 'C11D-WORKING-CONTEXT-SNAPSHOT-V2-DIRECT-ZIP'
$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..')).TrimEnd([char[]]@('\','/'))

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
    if ($IsReparsePoint) { return 'REPARSE_POINT_OR_SYMLINK' }
    $directoryRules = @(
        '^artifacts\\production(?:\\|$)',
        '^artifacts\\releases(?:\\|$)'
    )
    foreach ($rule in $directoryRules) { if ($p -match $rule) { return 'GENERATED_MEDIA_OR_RELEASE_OUTPUT_TREE' } }
    $archiveExt = [System.IO.Path]::GetExtension($p).ToLowerInvariant()
    if ($p -match '^artifacts\\prototypes\\c11c_art_direction_review\\' -and $archiveExt -in @('.mp4','.avi','.mkv','.webm','.mov','.wav','.ogg','.flac','.png','.jpg','.jpeg')) { return 'GENERATED_ART_DIRECTION_REVIEW_MEDIA' }
    if (($p -match '^(artifacts|release)\\') -and $archiveExt -in @('.zip','.7z','.rar','.tar','.gz','.tgz')) {
        return 'NESTED_ARCHIVE_EXCLUDED_TO_AVOID_STALE_OR_DUPLICATE_SNAPSHOTS'
    }
    if ($lowerLeaf -eq '.env' -or ($lowerLeaf.StartsWith('.env.') -and $lowerLeaf -ne '.env.example')) { return 'LOCAL_ENVIRONMENT_FILE' }
    if ($lowerLeaf -in @('id_rsa','id_ed25519','.git-credentials','.npmrc','.pypirc','credentials.json','secrets.json')) { return 'POTENTIAL_CREDENTIAL_FILE' }
    if ($archiveExt -in @('.pem','.pfx','.p12','.key','.kdbx')) { return 'POTENTIAL_PRIVATE_KEY_OR_CREDENTIAL' }
    if ($Length -gt ([long]$MaxMiB * 1MB)) { return 'FILE_EXCEEDS_MAX_FILE_MIB' }
    return $null
}

function Get-GitCommit {
    param([string]$RepoPath)
    try {
        $git = Get-Command git -ErrorAction SilentlyContinue
        if ($null -eq $git) { return $null }
        $value = & $git.Source -C $RepoPath rev-parse HEAD 2>$null
        if ($LASTEXITCODE -eq 0 -and $value) { return ([string]$value).Trim() }
    } catch { }
    return $null
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

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) { throw ('SNAPSHOT_REPO_ROOT_NOT_FOUND=' + $RepoRoot) }
$RequiredPaths = @(
    'AGENTS.md',
    '.continue\rules\CONTINUE.md',
    'project.godot',
    'c11c-suite\self_test.py',
    'tools\qa\c11\run_c11c_challenge_bulk_qa.ps1',
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

$ExcludedDirectoryNames = @('.git','.godot','.venv','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','node_modules','.cache','bin','obj','coverage')
$Included = New-Object 'System.Collections.Generic.List[object]'
$Skipped = New-Object 'System.Collections.Generic.List[object]'
$Stack = New-Object 'System.Collections.Generic.Stack[string]'
$Stack.Push($RepoRoot)

while ($Stack.Count -gt 0) {
    $CurrentDirectory = $Stack.Pop()
    foreach ($Item in (Get-ChildItem -LiteralPath $CurrentDirectory -Force -ErrorAction Stop)) {
        $Relative = Get-RelativePath -BasePath $RepoRoot -FullPath $Item.FullName
        $HasReparse = (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
        if ($Item.PSIsContainer) {
            if ($HasReparse) {
                $Skipped.Add([pscustomobject]@{path=$Relative;reason='REPARSE_POINT_OR_SYMLINK';bytes=0})
                continue
            }
            if ($Item.Name.ToLowerInvariant() -in $ExcludedDirectoryNames) {
                $Skipped.Add([pscustomobject]@{path=$Relative;reason='CACHE_OR_BUILD_DIRECTORY';bytes=0})
                continue
            }
            $NormalizedDir = $Relative.Replace('/','\')
            if ($NormalizedDir -match '^(artifacts\\production|artifacts\\releases)(\\|$)') {
                $Skipped.Add([pscustomobject]@{path=$Relative;reason='GENERATED_MEDIA_OR_RELEASE_OUTPUT_TREE';bytes=0})
                continue
            }
            $Stack.Push($Item.FullName)
            continue
        }
        $Reason = Get-RelativeSkipReason -RelativePath $Relative -Length ([long]$Item.Length) -MaxMiB $MaxFileMiB -IsReparsePoint $HasReparse
        if ($null -ne $Reason) {
            $Skipped.Add([pscustomobject]@{path=$Relative;reason=$Reason;bytes=[long]$Item.Length})
            continue
        }
        $Hash = Get-Sha256Hex -LiteralPath $Item.FullName
        $Included.Add([pscustomobject]@{source_path=$Item.FullName;path=$Relative.Replace('\','/');bytes=[long]$Item.Length;sha256=$Hash})
    }
}

if ($Included.Count -lt 100) { throw ('INCLUDED_SOURCE_COUNT_SUSPICIOUSLY_LOW=' + $Included.Count) }
$ManifestEntry = @($Included | Where-Object { $_.path -ceq 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' })
if ($ManifestEntry.Count -ne 1 -or $ManifestEntry[0].sha256 -ne $ExpectedCManifestSha256 -or [long]$ManifestEntry[0].bytes -ne $ExpectedCManifestBytes) {
    throw 'CANONICAL_C_MANIFEST_MUST_BE_INCLUDED_EXACTLY_ONCE_WITH_EXPECTED_HASH_AND_SIZE'
}

$SkippedCounts = @{}
foreach ($entry in $Skipped) {
    if (-not $SkippedCounts.ContainsKey($entry.reason)) { $SkippedCounts[$entry.reason] = 0 }
    $SkippedCounts[$entry.reason]++
}
$GitCommit = Get-GitCommit -RepoPath $RepoRoot
Write-Host 'SNAPSHOT_ENTRYPOINT=New-C11DWorkingSnapshot.ps1'
Write-Host ('ACTIVE_CHECKOUT=' + $RepoRoot)
Write-Host ('OUTPUT_DIRECTORY=' + $OutputFull)
Write-Host ('SNAPSHOT_ROOT=' + $RepoRoot)
Write-Host ('CANONICAL_C_MANIFEST=PASS sha256=' + $CManifestHash + ' bytes=' + $CManifestItem.Length)
Write-Host ('SOURCE_FILES_INCLUDED=' + $Included.Count)
Write-Host ('SKIPPED_PATHS=' + $Skipped.Count)
foreach ($key in ($SkippedCounts.Keys | Sort-Object)) { Write-Host ('SKIP_REASON=' + $key + ':' + $SkippedCounts[$key]) }
Write-Host ('GIT_COMMIT=' + $(if ($GitCommit) { $GitCommit } else { 'NOT_AVAILABLE' }))
if ($PreflightOnly) {
    Write-Host 'C11D_CONTEXT_EXPORT_PREFLIGHT=PASS_NO_FILES_WRITTEN'
    Write-Host 'NEXT_ACTION=REVIEW_SKIP_REASONS_THEN_RUN_WITHOUT_PREFLIGHTONLY'
    return
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
New-Item -ItemType Directory -Path $OutputFull -Force | Out-Null
$PartialPath = Join-Path $OutputFull ('.' + $ArchiveName + '.' + [guid]::NewGuid().ToString('N') + '.partial')
$Zip = $null
$FileStream = $null
try {
    $Encoding = [System.Text.UTF8Encoding]::new($false)
    $Inventory = New-Object 'System.Collections.Generic.List[object]'
    foreach ($entry in $Included) {
        $Inventory.Add([pscustomobject]@{path=$entry.path;bytes=[long]$entry.bytes;sha256=$entry.sha256})
    }
    $Readme = @'
# C11-D working-context snapshot

This archive is a filtered copy of the active Windows working tree for source/documentation review. It is NOT a release, freeze package, build artifact or replacement for the live checkout. The frozen C11-C manifest is carried unchanged and independently pinned in the snapshot manifest.

The snapshot is written directly from the active files into ZIP entries; it does not recreate a temporary copy of the directory tree. Generated production media, old release/snapshot archives, caches, symlinks/reparse points, local environment files and oversized files may be excluded. Inspect `C11D_CONTEXT_SNAPSHOT_MANIFEST.json` and the companion `.report.json` `skipped_paths` list before relying on any omitted material.

The inventory manifest hashes each included source file and lists exact relative paths. The manifest file itself is deliberately excluded from its own inventory to avoid a self-referential hash. The companion `.sha256` hashes the final ZIP. This is a review/context export only; do not extract it over the active checkout.
'@
    $ReadmeBytes = $Encoding.GetBytes($Readme)
    $ReadmeHash = Get-BytesSha256Hex -Bytes $ReadmeBytes
    $Inventory.Add([pscustomobject]@{path='C11D_CONTEXT_SNAPSHOT_README.md';bytes=[long]$ReadmeBytes.Length;sha256=$ReadmeHash})
    $InventorySorted = @($Inventory | Sort-Object -Property path)
    $TreeLines = New-Object 'System.Collections.Generic.List[string]'
    foreach ($entry in $InventorySorted) { $TreeLines.Add($entry.path + "`t" + $entry.bytes + "`t" + $entry.sha256) }
    $TreeText = ($TreeLines -join "`n") + "`n"
    $TreeHash = Get-BytesSha256Hex -Bytes $Encoding.GetBytes($TreeText)

    $SnapshotManifest = [ordered]@{
        schema = $SnapshotSchema
        snapshot_kind = 'FILTERED_ACTIVE_WORKING_TREE_CONTEXT_NOT_RELEASE_NOT_FREEZE'
        captured_at_utc = [DateTime]::UtcNow.ToString('o')
        source_root = $RepoRoot
        git_commit = $GitCommit
        canonical_c11c_manifest = [ordered]@{path='release/C11C_FREEZE_PACKAGE_MANIFEST.json';sha256=$ExpectedCManifestSha256;bytes=$ExpectedCManifestBytes;included_exactly_once=$true}
        source_file_count_included = $Included.Count
        payload_file_count_before_this_manifest = $InventorySorted.Count
        archive_entry_count_expected = $InventorySorted.Count + 1
        context_tree_sha256 = $TreeHash
        tree_hash_definition = 'SHA256(UTF8(join LF of sorted relative_path<TAB>size_bytes<TAB>sha256 rows, final LF)); excludes this manifest only'
        max_file_mib = $MaxFileMiB
        skip_reason_counts = $SkippedCounts
        skipped_paths_count = $Skipped.Count
        skipped_paths = @($Skipped | Sort-Object -Property path)
        files = $InventorySorted
        non_claims = @('not a canonical D baseline tree hash','not a C11-C freeze manifest','not a release package','does not prove D render acceptance','does not contain its own SHA-256 in its own file list')
    }
    $ManifestJson = ($SnapshotManifest | ConvertTo-Json -Depth 12) + "`n"
    $ManifestBytes = $Encoding.GetBytes($ManifestJson)
    $ManifestHash = Get-BytesSha256Hex -Bytes $ManifestBytes

    $FileStream = [System.IO.File]::Open($PartialPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    $Zip = [System.IO.Compression.ZipArchive]::new($FileStream, [System.IO.Compression.ZipArchiveMode]::Create, $true, $Encoding)
    foreach ($entry in $Included) {
        $zipEntry = $Zip.CreateEntry($entry.path, [System.IO.Compression.CompressionLevel]::Optimal)
        $sourceStream = $null
        $targetStream = $null
        try {
            $sourceStream = [System.IO.File]::Open($entry.source_path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
            $targetStream = $zipEntry.Open()
            $sourceStream.CopyTo($targetStream, 1048576)
        } finally {
            if ($null -ne $targetStream) { $targetStream.Dispose() }
            if ($null -ne $sourceStream) { $sourceStream.Dispose() }
        }
    }
    Add-ZipBytes -Archive $Zip -EntryName 'C11D_CONTEXT_SNAPSHOT_README.md' -Bytes $ReadmeBytes
    Add-ZipBytes -Archive $Zip -EntryName 'C11D_CONTEXT_SNAPSHOT_MANIFEST.json' -Bytes $ManifestBytes
    $Zip.Dispose(); $Zip = $null
    $FileStream.Dispose(); $FileStream = $null

    # Verify every compressed payload directly from the ZIP. Reading each stream also exercises its CRC check.
    $VerifyZip = [System.IO.Compression.ZipFile]::OpenRead($PartialPath)
    try {
        $ArchiveEntries = @($VerifyZip.Entries)
        $Names = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
        $ExpectedByPath = New-Object 'System.Collections.Generic.Dictionary[string,object]' ([System.StringComparer]::Ordinal)
        foreach ($expected in $InventorySorted) { $ExpectedByPath.Add([string]$expected.path, $expected) }
        $Verified = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
        $CCount = 0
        $ManifestCount = 0
        foreach ($zipEntry in $ArchiveEntries) {
            $normalized = $zipEntry.FullName.Replace('\','/')
            if (-not $Names.Add($normalized)) { throw ('DUPLICATE_ARCHIVE_ENTRY=' + $normalized) }
            if ($normalized -ceq 'release/C11C_FREEZE_PACKAGE_MANIFEST.json') { $CCount++ }
            if ($normalized -ceq 'C11D_CONTEXT_SNAPSHOT_MANIFEST.json') { $ManifestCount++ }
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
        if ($ArchiveEntries.Count -ne ($InventorySorted.Count + 1)) { throw ('ARCHIVE_ENTRY_COUNT_MISMATCH expected=' + ($InventorySorted.Count + 1) + ' actual=' + $ArchiveEntries.Count) }
        if ($Verified.Count -ne $InventorySorted.Count) { throw ('ARCHIVE_VERIFIED_PAYLOAD_COUNT_MISMATCH expected=' + $InventorySorted.Count + ' actual=' + $Verified.Count) }
        if ($CCount -ne 1) { throw ('ARCHIVE_C_MANIFEST_ENTRY_COUNT=' + $CCount) }
        if ($ManifestCount -ne 1) { throw ('ARCHIVE_SNAPSHOT_MANIFEST_ENTRY_COUNT=' + $ManifestCount) }
    } finally { $VerifyZip.Dispose() }

    [System.IO.File]::Move($PartialPath, $ArchivePath)
    $ZipHash = Get-Sha256Hex -LiteralPath $ArchivePath
    $ZipBytes = (Get-Item -LiteralPath $ArchivePath).Length
    $Sidecar = $ZipHash + '  ' + [System.IO.Path]::GetFileName($ArchivePath) + "`n"
    [System.IO.File]::WriteAllText($ArchivePath + '.sha256', $Sidecar, $Encoding)
    $ExternalReport = [ordered]@{
        schema='C11D-WORKING-CONTEXT-EXPORT-REPORT-V2-DIRECT-ZIP'
        archive_path=$ArchivePath
        archive_sha256=$ZipHash
        archive_bytes=$ZipBytes
        archive_entries=$ArchiveEntries.Count
        duplicate_entries=0
        canonical_c11c_manifest_sha256=$ExpectedCManifestSha256
        canonical_c11c_manifest_bytes=$ExpectedCManifestBytes
        source_file_count_included=$Included.Count
        payload_file_count_before_snapshot_manifest=$InventorySorted.Count
        context_tree_sha256=$TreeHash
        snapshot_manifest_sha256=$ManifestHash
        skipped_paths_count=$Skipped.Count
        skipped_paths=@($Skipped | Sort-Object -Property path)
    }
    [System.IO.File]::WriteAllText($ArchivePath + '.report.json', (($ExternalReport | ConvertTo-Json -Depth 12) + "`n"), $Encoding)

    Write-Host ('ARCHIVE=' + $ArchivePath)
    Write-Host ('ARCHIVE_SHA256=' + $ZipHash)
    Write-Host ('ARCHIVE_BYTES=' + $ZipBytes)
    Write-Host ('ARCHIVE_ENTRIES=' + $ArchiveEntries.Count)
    Write-Host 'DUPLICATE_ARCHIVE_ENTRIES=0'
    Write-Host ('C11C_MANIFEST_IN_ARCHIVE=1/' + $ExpectedCManifestSha256 + '/' + $ExpectedCManifestBytes)
    Write-Host ('SOURCE_FILES_INCLUDED=' + $Included.Count)
    Write-Host ('SKIPPED_PATHS=' + $Skipped.Count)
    Write-Host ('CONTEXT_TREE_SHA256=' + $TreeHash)
    Write-Host 'C11D_CONTEXT_EXPORT=PASS_DIRECT_ZIP_FILTERED_WORKTREE_COPY'
    Write-Host 'NEXT_ACTION=UPLOAD_ZIP_AND_OPTIONAL_REPORT; NEVER_EXTRACT_OVER_ACTIVE_CHECKOUT'
} finally {
    if ($null -ne $Zip) { $Zip.Dispose() }
    if ($null -ne $FileStream) { $FileStream.Dispose() }
    if (Test-Path -LiteralPath $PartialPath -PathType Leaf) { Remove-Item -LiteralPath $PartialPath -Force -ErrorAction SilentlyContinue }
}
