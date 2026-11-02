[CmdletBinding()]
param(
    [string]$Root = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS',
    [string]$ExpectedAuthorityCommit = '02f5fac7698fe6d73076d3da1e3dfa852bd06725'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Quote-ProcessArgument {
    param([string]$Value)
    if ($Value -notmatch '[\s"]') { return $Value }
    return '"' + $Value.Replace('"', '\"') + '"'
}

function Invoke-CapturedProcess {
    param(
        [Parameter(Mandatory=$true)][string]$FilePath,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$WorkingDirectory
    )
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $FilePath
    $psi.Arguments = (($Arguments | ForEach-Object { Quote-ProcessArgument ([string]$_) }) -join ' ')
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $psi
    if (-not $p.Start()) { throw "Could not start $FilePath" }
    $outTask = $p.StandardOutput.ReadToEndAsync()
    $errTask = $p.StandardError.ReadToEndAsync()
    $p.WaitForExit()
    return [pscustomobject]@{
        ExitCode = [int]$p.ExitCode
        Stdout = $outTask.Result
        Stderr = $errTask.Result
    }
}

function Invoke-Git {
    param([string[]]$Arguments)
    $r = Invoke-CapturedProcess -FilePath 'git' -Arguments (@('-C', $Root) + $Arguments) -WorkingDirectory $Root
    if ($r.ExitCode -ne 0) {
        throw "git $($Arguments -join ' ') failed ($($r.ExitCode)): $($r.Stderr) $($r.Stdout)"
    }
    return $r.Stdout.TrimEnd()
}

function Assert-Sha256 {
    param([string]$Path,[string]$Expected,[string]$Label)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Label missing: $Path" }
    $actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $Expected.ToLowerInvariant()) { throw "$Label SHA mismatch: $actual" }
    return $actual
}

function Get-RelativePath {
    param([string]$Base,[string]$Path)
    $b = [IO.Path]::GetFullPath($Base).TrimEnd('\') + '\'
    $p = [IO.Path]::GetFullPath($Path)
    if (-not $p.StartsWith($b,[StringComparison]::OrdinalIgnoreCase)) { return $null }
    return $p.Substring($b.Length).Replace('\','/')
}

$RunId = 'C11E-E3-D3MUSIC-V5-PREFLIGHT-' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8)
$Documents = [Environment]::GetFolderPath('MyDocuments')
$RunDir = Join-Path $Documents $RunId
New-Item -ItemType Directory -Path $RunDir | Out-Null

Write-Host '========== C11-E E3 D3 MUSIC V5 PREFLIGHT =========='
Write-Host "RUN_ID=$RunId"
Write-Host "ROOT=$Root"

if (-not (Test-Path -LiteralPath $Root -PathType Container)) { throw "Checkout missing: $Root" }
$branch = Invoke-Git @('branch','--show-current')
$head = Invoke-Git @('rev-parse','HEAD')
if ($branch -ne 'main') { throw "Expected branch main; found $branch" }
$ancestry = Invoke-CapturedProcess -FilePath 'git' -Arguments @('-C',$Root,'merge-base','--is-ancestor',$ExpectedAuthorityCommit,'HEAD') -WorkingDirectory $Root
if ($ancestry.ExitCode -ne 0) { throw "Expected authority commit is not in HEAD ancestry: $ExpectedAuthorityCommit" }
$status = Invoke-Git @('status','--porcelain','--untracked-files=all')
if (-not [string]::IsNullOrWhiteSpace($status)) { throw "Checkout is not clean; stop before E3 preflight:`n$status" }

$Manifest = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$manifestSha = Assert-Sha256 $Manifest 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953' 'Frozen C11-C manifest'
$manifestBytes = (Get-Item -LiteralPath $Manifest).Length
if ($manifestBytes -ne 796318) { throw "Frozen C11-C manifest byte count mismatch: $manifestBytes" }

$ClosureDoc = Join-Path $Root 'docs\history\c11e\C11E_E2_R4_FORMAL_CLOSURE_DECISION_20261102_V1.md'
$closureSha = Assert-Sha256 $ClosureDoc '4679a5b2c93cad53c740e6ac85374a2c6437f9011faa68b30b084a27f000c1c3' 'E2 formal closure decision'
$VisualAuditDoc = Join-Path $Root 'docs\history\c11e\C11E_E2_R4_FULL_DECODED_FRAME_VISUAL_AUDIT_20261102_V1.md'
$visualAuditSha = Assert-Sha256 $VisualAuditDoc '5763edef9561ff5f6b17e584376a1354d6ca1ab24d2dd7456c10c0e514409dec' 'E2 full-frame visual audit'
$VisualManifest = Join-Path $Root 'docs\history\c11e\C11E_E2_R4_FULL_FRAME_VISUAL_AUDIT_MANIFEST_20261102_V1.json'
$visualManifestSha = Assert-Sha256 $VisualManifest '3ac2e1d2e7e157740954749002a27eb35ebe90c3c5c52d37fe73cd24c827811e' 'E2 visual audit manifest'
foreach ($trackedPath in @(
    'docs/history/c11e/C11E_E2_R4_FORMAL_CLOSURE_DECISION_20261102_V1.md',
    'docs/history/c11e/C11E_E2_R4_FULL_DECODED_FRAME_VISUAL_AUDIT_20261102_V1.md',
    'docs/history/c11e/C11E_E2_R4_FULL_FRAME_VISUAL_AUDIT_MANIFEST_20261102_V1.json'
)) {
    $null = Invoke-Git @('ls-files','--error-unmatch',$trackedPath)
}
$visualManifestData = Get-Content -LiteralPath $VisualManifest -Raw -Encoding UTF8 | ConvertFrom-Json
if (@($visualManifestData.boards).Count -ne 12) { throw 'E2 visual audit manifest must identify all 12 contact sheets.' }
$visualBoardResults = @()
foreach ($board in $visualManifestData.boards) {
    $boardRel = 'docs/history/c11e/C11E_E2_R4_FULL_FRAME_AUDIT/' + [string]$board.file
    $boardPath = Join-Path $Root ($boardRel.Replace('/','\'))
    $boardSha = Assert-Sha256 $boardPath ([string]$board.sha256) ('Visual audit board ' + [string]$board.file)
    if ((Get-Item -LiteralPath $boardPath).Length -ne [long]$board.bytes) { throw 'E2 visual audit board byte count mismatch.' }
    $null = Invoke-Git @('ls-files','--error-unmatch',$boardRel)
    $visualBoardResults += [pscustomobject]@{Path=$boardRel;Bytes=[long]$board.bytes;SHA256=$boardSha}
}

$R4Id = 'C11E-E2-CH001-AB-20261101-V9-R4'
$R4Root = Join-Path $Root ('artifacts\production\c11e\' + $R4Id)
$Receipt = Join-Path $R4Root 'C11E_E2_RENDER_RECEIPT.json'
$receiptSha = Assert-Sha256 $Receipt '2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f' 'R4 receipt'
$sidecar = $Receipt + '.sha256'
if (-not (Test-Path -LiteralPath $sidecar -PathType Leaf)) { throw 'R4 receipt sidecar missing.' }
$sideText = (Get-Content -LiteralPath $sidecar -Raw -Encoding UTF8).Trim()
if ($sideText -ne ($receiptSha + '  C11E_E2_RENDER_RECEIPT.json')) { throw 'R4 receipt sidecar does not match.' }
$record = Get-Content -LiteralPath $Receipt -Raw -Encoding UTF8 | ConvertFrom-Json
if ($record.schema -ne 'C11E-E2-CHALLENGE-TITLE-AB-RENDER-RECEIPT-V1' -or $record.request_id -ne $R4Id -or @($record.render_rows).Count -ne 2) {
    throw 'R4 receipt identity or render count mismatch.'
}

$docsZip = Join-Path $Documents 'C11E_E2_CH001_AB_EVIDENCE_20261101_154340_38e2c012.zip'
$zipSha = Assert-Sha256 $docsZip 'f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de' 'R4 evidence ZIP'

$expectedMedia = @(
    @{ Path = (Join-Path $R4Root 'A\CHALLENGE_001_A_REVIEW_720.mp4'); Sha = '3d72e52cc7f7f8fc4b32c8719ab9800ba622e6069c7fa956526c108defce1afd'; Name='A_MP4' },
    @{ Path = (Join-Path $R4Root 'B\CHALLENGE_001_B_REVIEW_720.mp4'); Sha = '77c5ec4d432db9bebd174309d4e8e4039b437e78d08a16b30a3497fb5e1d3045'; Name='B_MP4' },
    @{ Path = (Join-Path $R4Root 'A\CHALLENGE_001_A_source.avi'); Sha = '0f265d8526793e25c12ae1fc55287133024d34716d92bcc47494023b70859e54'; Name='A_AVI' },
    @{ Path = (Join-Path $R4Root 'B\CHALLENGE_001_B_source.avi'); Sha = '23ffc36f6121511f224e6f251f09f5f465393559dabefdf83e65cf711b271945'; Name='B_AVI' }
)
$mediaResults = @()
foreach ($m in $expectedMedia) {
    $mediaResults += [pscustomobject]@{ Name=$m.Name; Path=$m.Path; SHA256=(Assert-Sha256 $m.Path $m.Sha $m.Name) }
}

# Read-only source inventory. The specification, implementation and tests must be source-pinned before functional E3 tests are designed.
$scanRoots = @(
    'docs\current\d',
    'docs\history\c11d',
    'docs\history\c11e',
    'docs\current\e',
    'definitions',
    'schemas',
    'tools\c11d',
    'tools\c11e',
    'c11c-suite',
    'tests'
)
$extensions = @('.md','.json','.py','.gd','.tscn','.ps1','.cs','.toml','.yaml','.yml','.txt','.cfg')
$seen = @{}
$candidateMatchesList = New-Object System.Collections.Generic.List[object]
$exactD3 = New-Object System.Collections.Generic.List[object]
$contractCandidates = New-Object System.Collections.Generic.List[object]
$musicSeedRefs = New-Object System.Collections.Generic.List[object]
$musicTests = New-Object System.Collections.Generic.List[object]

foreach ($relRoot in $scanRoots) {
    $dir = Join-Path $Root $relRoot
    if (-not (Test-Path -LiteralPath $dir -PathType Container)) { continue }
    $items = Get-ChildItem -LiteralPath $dir -File -Recurse -ErrorAction SilentlyContinue
    foreach ($file in $items) {
        if ($file.Length -gt 5242880) { continue }
        if ($extensions -notcontains $file.Extension.ToLowerInvariant()) { continue }
        $full = [IO.Path]::GetFullPath($file.FullName)
        if ($seen.ContainsKey($full)) { continue }
        $seen[$full] = $true
        try { $content = [IO.File]::ReadAllText($full) } catch { continue }
        $rel = Get-RelativePath $Root $full
        if ($null -eq $rel) { continue }
        if ($rel -match '(?i)20261102_V23|C11E_E3_D3_MUSIC_V5_SOURCE_DISCOVERY_PREFLIGHT_20261102_V1|RUN_C11E_E3_D3_MUSIC_V5_PREFLIGHT_20261102') { continue }
        $hasD3 = $content -match '(?i)D3[\s_-]*MUSIC[\s_-]*V5|D3MusicV5|MUSIC_V5'
        $hasSeed = $content -match '(?i)music_seed'
        $hasAudio = $content -match '(?i)music|audio|ffmpeg|ffprobe|mux'
        $isTest = ($rel -match '(?i)(^|/)(tests?|test_)[^/]*|(^|/)test[^/]*\.(py|gd|ps1)$')
        $isContractPath = ($rel -match '(?i)(d3|music|audio).*(contract|spec|schema|v5)|(contract|spec|schema).*(d3|music|audio)') -and ($hasD3 -or $hasSeed)
        $isImplementationPath = ($hasSeed -and $hasAudio -and $rel -match '(?i)(producer|music|audio|engine|service|pipeline)')
        if (-not ($hasD3 -or $hasSeed -or ($hasAudio -and $isTest))) { continue }
        $sha = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant()
        $lineHits = New-Object System.Collections.Generic.List[object]
        $lineNo = 0
        foreach ($line in [IO.File]::ReadAllLines($full)) {
            $lineNo++
            if ($line -match '(?i)D3[\s_-]*MUSIC[\s_-]*V5|D3MusicV5|MUSIC_V5|music_seed|music|audio|ffmpeg|ffprobe|mux') {
                $safeLine = $line.Trim()
                if ($safeLine -match '(?i)(api[_-]?key|client[_-]?secret|password|token|credential)') {
                    $safeLine = '[REDACTED_SECRET_LIKE_LINE]'
                }
                if ($safeLine.Length -gt 180) { $safeLine = $safeLine.Substring(0,180) + '…' }
                $lineHits.Add([pscustomobject]@{ Line=$lineNo; Text=$safeLine })
                if ($lineHits.Count -ge 30) { break }
            }
        }
        $entry = [pscustomobject]@{ Path=$rel; Bytes=[long]$file.Length; SHA256=$sha; HasD3MusicV5=$hasD3; HasMusicSeed=$hasSeed; TestCandidate=$isTest; LikelyContractPath=$isContractPath; LikelyImplementationPath=$isImplementationPath; MatchLines=@($lineHits.ToArray()) }
        $candidateMatchesList.Add($entry)
        if ($hasD3) { $exactD3.Add($entry) }
        if ($isContractPath) { $contractCandidates.Add($entry) }
        if ($hasSeed) { $musicSeedRefs.Add($entry) }
        if ($isTest -and $hasAudio) { $musicTests.Add($entry) }
    }
}

$allMatches = @($candidateMatchesList | Sort-Object Path)
$exactMatches = @($exactD3 | Sort-Object Path)
$seedMatches = @($musicSeedRefs | Sort-Object Path)
$likelyContracts = @($contractCandidates | Sort-Object Path)
$testMatches = @($musicTests | Sort-Object Path)
$discoveryStatus = 'SOURCE_CANDIDATES_REQUIRE_MANUAL_REVIEW'
if ($likelyContracts.Count -gt 0 -and $seedMatches.Count -gt 0 -and $testMatches.Count -gt 0) {
    $discoveryStatus = 'CONTRACT_IMPLEMENTATION_TEST_CANDIDATES_FOUND_PINS_REQUIRE_REVIEW'
}
if ($exactMatches.Count -eq 0) { $discoveryStatus = 'BLOCKED_EXACT_D3_MUSIC_V5_IDENTIFIER_NOT_FOUND' }

$report = [ordered]@{
    schema = 'C11E-E3-D3-MUSIC-V5-SOURCE-DISCOVERY-PREFLIGHT-V1'
    run_id = $RunId
    created_at = (Get-Date).ToString('o')
    checkout = $Root
    branch = $branch
    head = $head
    expected_authority_commit = $ExpectedAuthorityCommit
    expected_authority_in_head_ancestry = $true
    worktree_clean = $true
    frozen_c11c_manifest = [ordered]@{ bytes=$manifestBytes; sha256=$manifestSha }
    e2_formal_closure = [ordered]@{ decision_sha256=$closureSha; visual_audit_sha256=$visualAuditSha; visual_manifest_sha256=$visualManifestSha; visual_audit_board_count=@($visualBoardResults).Count; visual_audit_boards=$visualBoardResults }
    e2_r4 = [ordered]@{ request_id=$R4Id; receipt_sha256=$receiptSha; evidence_zip_sha256=$zipSha; media=$mediaResults }
    discovery_status = $discoveryStatus
    scan_roots = $scanRoots
    scanned_candidate_file_count = $seen.Count
    exact_d3_music_v5_matches = $exactMatches
    likely_contract_candidates = $likelyContracts
    music_seed_references = $seedMatches
    music_test_candidates = $testMatches
    all_candidate_matches = $allMatches
    renderer_invoked = $false
    audio_media_created = $false
    ffmpeg_mux_invoked = $false
    production_media_created = $false
    repository_modified = $false
}
$reportPath = Join-Path $RunDir 'C11E_E3_D3_MUSIC_V5_PREFLIGHT_REPORT.json'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $reportPath -Encoding UTF8
$summaryPath = Join-Path $RunDir 'C11E_E3_D3_MUSIC_V5_PREFLIGHT_SUMMARY.txt'
$summary = @(
    'C11E E3 D3 MUSIC V5 SOURCE DISCOVERY PREFLIGHT',
    "RUN_ID=$RunId",
    "BRANCH=$branch",
    "HEAD=$head",
    'E2_FORMAL_CLOSURE_RECORDS=PASS',
    ("E2_FULL_FRAME_VISUAL_BOARDS={0}/12" -f $visualBoardResults.Count),
    'E2_R4_EVIDENCE=PASS',
    "SCANNED_CANDIDATE_FILES=$($seen.Count)",
    "EXACT_D3_MUSIC_V5_MATCHES=$($exactMatches.Count)",
    "LIKELY_CONTRACT_CANDIDATES=$($likelyContracts.Count)",
    "MUSIC_SEED_SOURCE_MATCHES=$($seedMatches.Count)",
    "MUSIC_TEST_CANDIDATES=$($testMatches.Count)",
    "DISCOVERY_STATUS=$discoveryStatus",
    'RENDERER_INVOKED=false',
    'AUDIO_MEDIA_CREATED=false',
    'FFMPEG_MUX_INVOKED=false',
    'PRODUCTION_MEDIA_CREATED=false',
    'REPOSITORY_MODIFIED=false',
    "REPORT=$reportPath"
)
$summary | Set-Content -LiteralPath $summaryPath -Encoding UTF8
Write-Host ''
$summary | ForEach-Object { Write-Host $_ }
Write-Host '========== DISCOVERY CANDIDATES =========='
foreach ($m in ($allMatches | Select-Object -First 40)) {
    $flags = @()
    if ($m.HasD3MusicV5) { $flags += 'D3_V5' }
    if ($m.HasMusicSeed) { $flags += 'MUSIC_SEED' }
    if ($m.TestCandidate) { $flags += 'TEST' }
    if ($m.LikelyContractPath) { $flags += 'CONTRACT_PATH' }
    if ($m.LikelyImplementationPath) { $flags += 'IMPLEMENTATION_PATH' }
    Write-Host ("{0} | {1} | {2}" -f ($flags -join ','),$m.SHA256,$m.Path)
}
Write-Host 'E3_AUDIO_RENDER_AND_MUX=NOT_INVOKED'
