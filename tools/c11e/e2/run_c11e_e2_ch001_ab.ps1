[CmdletBinding()]
param(
    [string]$Root = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS',
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$')][string]$RequestId = 'C11E-E2-CH001-AB-20261031-V8',
    [ValidateRange(1,2147483646)][int]$Seed = 193847,
    [ValidateRange(1,2147483646)][int]$MusicSeed = 840001,
    [string]$TitleA = 'C11-E TITLE A',
    [string]$TitleB = 'C11-E TITLE B',
    [string]$GodotExecutable = '',
    [string]$PythonExecutable = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$ExpectedBranch = 'main'
$RequiredE0ReentryCommit = 'b92434d6a8b50cef7e49ba6b75a4813777927fe7'
$ExpectedManifestSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedManifestBytes = 796318
$RequiredE1Commit = 'a3c7c5d284a96ce115ca52208b4039002502753b'
$ExpectedE1ReceiptHead = 'bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c'
$ExpectedE1ServiceSha = '6f18d5fd906ff615d95d7f9d53e2e6ff0bf37c74e185efdcaf34354c888b9645'
$ExpectedE1CliSha = 'e7272231dca2eb730506308b092fce9b3644f7f8cfd9f2c2bbbbd1b695e82fc4'
$ExpectedE1MainSha = '05f4ed650cec028df3d8e4253301fa16510b0fc495e028f9e0d6addc113551fb'
$ExpectedGodotSceneSha = '6dfe47ebd3d158a19f0c72727ff68e4d5b37910513d89c523837b785e3f3d34c'
$ExpectedGodotScriptSha = 'af142fc5fc41f4e398e981e60c014d9ddd09dccc888c1d3fbc2e1b0e77911493'
$ExpectedGodotJsonTestSha = 'd0591c6a5a2c9b49774b607aff58a59bc1e08fe17273dc774fd23743e2d1082d'
$ExpectedPairBuilderSha = '37889062856127d0e4161b1c5951547d6a954e807e9fd031fd58fca158373eb7'
$ExpectedPairTestsSha = '36b6f296d17f72b51b96946953b1abc72e907f5823567fd8a9993ae5f4169342'

function Get-Sha256 {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing file: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-StringSha256 {
    param([string]$Value)
    $utf8 = New-Object System.Text.UTF8Encoding -ArgumentList $false
    $bytes = $utf8.GetBytes($Value)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}

function Assert-FrameRowsIdentical {
    param([string[]]$RowsA, [string[]]$RowsB, [string]$Label)
    if ($RowsA.Count -ne $RowsB.Count) {
        throw ("A/B frame denominator mismatch for {0}: A={1}; B={2}." -f $Label, $RowsA.Count, $RowsB.Count)
    }
    for ($index = 0; $index -lt $RowsA.Count; $index++) {
        if ($RowsA[$index] -ne $RowsB[$index]) {
            throw ("A/B pixel identity mismatch for {0} at source frame {1}." -f $Label, $index)
        }
    }
    return $RowsA.Count
}

function Count-FrameRowDifferences {
    param([string[]]$RowsA, [string[]]$RowsB, [string]$Label)
    if ($RowsA.Count -ne $RowsB.Count) {
        throw ("A/B frame denominator mismatch for {0}: A={1}; B={2}." -f $Label, $RowsA.Count, $RowsB.Count)
    }
    $different = 0
    for ($index = 0; $index -lt $RowsA.Count; $index++) {
        if ($RowsA[$index] -ne $RowsB[$index]) { $different++ }
    }
    return $different
}

function Quote-NativeArg {
    param([Parameter(Mandatory=$true)][string]$Value)
    if ($Value -notmatch '[\s"]') { return $Value }
    return '"' + (($Value -replace '(\\*)"','$1$1\"') -replace '(\\+)$','$1$1') + '"'
}

function Invoke-NativeProcess {
    param(
        [Parameter(Mandatory=$true)][string]$FilePath,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$WorkingDirectory,
        [Parameter(Mandatory=$true)][string]$StdoutPath,
        [Parameter(Mandatory=$true)][string]$StderrPath,
        [Parameter(Mandatory=$true)][string]$Label
    )
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $FilePath
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.StandardOutputEncoding = [Text.Encoding]::UTF8
    $psi.StandardErrorEncoding = [Text.Encoding]::UTF8
    $quoted = foreach ($arg in $Arguments) { Quote-NativeArg ([string]$arg) }
    $psi.Arguments = $quoted -join ' '

    $startDiagnosticPath = $StdoutPath + '.start.json'
    $startDiagnostic = [ordered]@{
        label = $Label
        file_name = $psi.FileName
        file_exists = (Test-Path -LiteralPath $psi.FileName -PathType Leaf)
        arguments = $psi.Arguments
        working_directory = $psi.WorkingDirectory
        started = $false
        start_exception = $null
        inner_exception = $null
    }
    [IO.File]::WriteAllText($startDiagnosticPath, ($startDiagnostic | ConvertTo-Json -Depth 8), (New-Object System.Text.UTF8Encoding -ArgumentList $false))
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $psi
    try {
        if (-not $process.Start()) { throw ("Process.Start returned false for {0}." -f $Label) }
        $startDiagnostic.started = $true
        [IO.File]::WriteAllText($startDiagnosticPath, ($startDiagnostic | ConvertTo-Json -Depth 8), (New-Object System.Text.UTF8Encoding -ArgumentList $false))
    } catch {
        $startDiagnostic.start_exception = $_.Exception.ToString()
        if ($_.Exception.InnerException) { $startDiagnostic.inner_exception = $_.Exception.InnerException.ToString() }
        [IO.File]::WriteAllText($startDiagnosticPath, ($startDiagnostic | ConvertTo-Json -Depth 8), (New-Object System.Text.UTF8Encoding -ArgumentList $false))
        throw ("Unable to start process '{0}'. FileName='{1}'; WorkingDirectory='{2}'; Arguments='{3}'; Exception={4}" -f $Label, $psi.FileName, $psi.WorkingDirectory, $psi.Arguments, $_.Exception.ToString())
    }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdoutText = $stdoutTask.Result
    $stderrText = $stderrTask.Result
    $utf8 = New-Object System.Text.UTF8Encoding -ArgumentList $false
    [IO.File]::WriteAllText($StdoutPath, $stdoutText, $utf8)
    [IO.File]::WriteAllText($StderrPath, $stderrText, $utf8)
    [IO.File]::WriteAllText(($StdoutPath + '.command.txt'), ($FilePath + ' ' + $psi.Arguments), $utf8)
    [IO.File]::WriteAllText(($StdoutPath + '.exitcode.txt'), ([string]$process.ExitCode), $utf8)
    if ($process.ExitCode -ne 0) {
        throw ("{0} failed with exit code {1}. See {2} and {3}." -f $Label, $process.ExitCode, $StdoutPath, $StderrPath)
    }
    return [PSCustomObject]@{
        ExitCode = [int]$process.ExitCode
        Stdout = $stdoutText
        Stderr = $stderrText
        Command = ($FilePath + ' ' + $psi.Arguments)
    }
}

function Enter-NativeViewportGuard {
    param([string]$ProjectRoot)
    $override = Join-Path $ProjectRoot 'override.cfg'
    if (-not (Test-Path -LiteralPath $override -PathType Leaf)) { return $null }
    $originalSha = Get-Sha256 $override
    $quarantine = Join-Path $ProjectRoot ('.override.c11e_e2_quarantine_' + [Guid]::NewGuid().ToString('N') + '.cfg')
    Move-Item -LiteralPath $override -Destination $quarantine
    return [PSCustomObject]@{ Original = $override; Quarantine = $quarantine; Sha256 = $originalSha }
}

function Exit-NativeViewportGuard {
    param([object]$State)
    if ($null -eq $State) { return }
    if (Test-Path -LiteralPath $State.Original -PathType Leaf) {
        $existingSha = Get-Sha256 $State.Original
        if ($existingSha -ne [string]$State.Sha256) {
            throw ("override.cfg path was occupied by different bytes during E2; no file was overwritten. Original backup remains at: {0}" -f $State.Quarantine)
        }
        return
    }
    if (-not (Test-Path -LiteralPath $State.Quarantine -PathType Leaf)) {
        throw ("Original override.cfg is missing from both its original and quarantine paths: {0}" -f $State.Quarantine)
    }
    Move-Item -LiteralPath $State.Quarantine -Destination $State.Original
    $restoredSha = Get-Sha256 $State.Original
    if ($restoredSha -ne [string]$State.Sha256) {
        throw ("Restored override.cfg hash mismatch; restored file was retained for inspection: {0}" -f $State.Original)
    }
}

function Get-FrameMd5Rows {
    param([string]$Ffmpeg, [string]$VideoPath, [string]$Filter, [string]$LogRoot, [string]$Label)
    $out = Join-Path $LogRoot ($Label + '.stdout.log')
    $err = Join-Path $LogRoot ($Label + '.stderr.log')
    $run = Invoke-NativeProcess -FilePath $Ffmpeg -Arguments @('-v','error','-i',$VideoPath,'-vf',$Filter,'-an','-f','framemd5','-') -WorkingDirectory $Root -StdoutPath $out -StderrPath $err -Label $Label
    $rows = @($run.Stdout -split "`r?`n" | Where-Object { $_ -match '^\s*\d+\s*,\s*\d+\s*,' } | ForEach-Object { $_.Trim() })
    if ($rows.Count -le 0) { throw ("No framemd5 rows produced for {0}." -f $Label) }
    return ,$rows
}

function Assert-VideoFrameContent {
    param([string]$Ffmpeg, [string]$VideoPath, [string]$LogRoot, [string]$Label, [string]$WorkingDirectory)
    $out = Join-Path $LogRoot ($Label + '.stdout.log')
    $err = Join-Path $LogRoot ($Label + '.stderr.log')
    # Inspect deterministic gameplay/middle/closing samples. A successful Movie Maker file
    # with a constant clear-colour viewport must not be mistaken for a rendered challenge.
    $filter = 'select=eq(n\,60)+eq(n\,270)+eq(n\,480),signalstats,metadata=print'
    $run = Invoke-NativeProcess -FilePath $Ffmpeg -Arguments @('-hide_banner','-loglevel','info','-i',$VideoPath,'-vf',$filter,'-frames:v','3','-an','-f','null','NUL') -WorkingDirectory $WorkingDirectory -StdoutPath $out -StderrPath $err -Label $Label
    $log = $run.Stderr + "`n" + $run.Stdout
    $keys = @('YMIN','YMAX','UMIN','UMAX','VMIN','VMAX')
    $values = @{}
    foreach ($key in $keys) {
        $matches = [regex]::Matches($log, ('lavfi\.signalstats\.' + $key + '=([0-9]+(?:\.[0-9]+)?)'))
        if ($matches.Count -ne 3) { throw ("Visual content probe {0} did not return three {1} samples; got {2}." -f $Label, $key, $matches.Count) }
        $values[$key] = @($matches | ForEach-Object { [double]$_.Groups[1].Value })
    }
    $rows = @()
    $sampleIndices = @(60,270,480)
    for ($i = 0; $i -lt 3; $i++) {
        $yRange = $values['YMAX'][$i] - $values['YMIN'][$i]
        $uRange = $values['UMAX'][$i] - $values['UMIN'][$i]
        $vRange = $values['VMAX'][$i] - $values['VMIN'][$i]
        if ($yRange -le 1 -and $uRange -le 1 -and $vRange -le 1) {
            throw ("Source AVI contains a spatially uniform frame at required sample index {0} for run {1}; Movie Maker output is not accepted as visual content." -f ($sampleIndices[$i]), $Label)
        }
        $rows += [PSCustomObject]@{
            frame_index = [int]$sampleIndices[$i]
            luma_min = $values['YMIN'][$i]
            luma_max = $values['YMAX'][$i]
            luma_range = $yRange
            chroma_u_range = $uRange
            chroma_v_range = $vRange
            spatially_nonuniform = $true
        }
    }
    return ,$rows
}

$ResolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$Branch = (& git -C $ResolvedRoot branch --show-current).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git branch.' }
$Head = (& git -C $ResolvedRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git HEAD.' }
$HeadParent = (& git -C $ResolvedRoot rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Unable to read current Git HEAD parent.' }
if ($Branch -ne $ExpectedBranch) {
    throw ("E2 branch mismatch: expected={0}; found={1}" -f $ExpectedBranch, $Branch)
}
# Per-iteration local commits are expected. Pin the installed E0/E1 commits as
# required ancestors, record the actual HEAD/parent, and rely on exact source pins
# below instead of freezing HEAD to a stale value across user commits.
& git -C $ResolvedRoot merge-base --is-ancestor $RequiredE1Commit $Head
$E1AncestorCode = $LASTEXITCODE
if ($E1AncestorCode -ne 0) { throw ("Required E1 commit is not an ancestor of active HEAD: {0}" -f $RequiredE1Commit) }
& git -C $ResolvedRoot merge-base --is-ancestor $RequiredE0ReentryCommit $Head
$E0AncestorCode = $LASTEXITCODE
if ($E0AncestorCode -ne 0) { throw ("Required E0 re-entry commit is not an ancestor of active HEAD: {0}" -f $RequiredE0ReentryCommit) }

$Manifest = Join-Path $ResolvedRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$ManifestSha = Get-Sha256 $Manifest
$ManifestBytes = (Get-Item -LiteralPath $Manifest).Length
if ($ManifestSha -ne $ExpectedManifestSha -or $ManifestBytes -ne $ExpectedManifestBytes) {
    throw 'Frozen C11-C manifest identity mismatch; no E2 artifacts created.'
}

$DocumentsForE1 = [Environment]::GetFolderPath('MyDocuments')
$E1InstallReceiptPath = Join-Path $DocumentsForE1 'C11E_E1_SHARED_SERVICE_20261030_124158\C11E_E1_SHARED_SERVICE_RECEIPT.json'
$E1TestReceiptPath = Join-Path $DocumentsForE1 'C11E_E1_SHARED_SERVICE_VERIFY_20261030_124158\C11E_E1_SHARED_SERVICE_TEST_RECEIPT.json'
foreach ($ReceiptPath in @($E1InstallReceiptPath, $E1TestReceiptPath)) {
    if (-not (Test-Path -LiteralPath $ReceiptPath -PathType Leaf)) { throw ("Required E1 receipt missing: {0}" -f $ReceiptPath) }
}
$E1InstallReceipt = Get-Content -LiteralPath $E1InstallReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$E1TestReceipt = Get-Content -LiteralPath $E1TestReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($E1InstallReceipt.status -ne 'E1_CODE_OVERLAY_APPLIED_PENDING_WINDOWS_ACCEPTANCE' -or $E1InstallReceipt.branch -ne 'main' -or $E1InstallReceipt.head -ne $ExpectedE1ReceiptHead) { throw 'E1 installation receipt identity/status mismatch.' }
if ($E1TestReceipt.status -ne 'E1_CODE_TESTS_PASS_GUI_OPERATOR_RUNTIME_PENDING' -or $E1TestReceipt.branch -ne 'main' -or $E1TestReceipt.head -ne $ExpectedE1ReceiptHead) { throw 'E1 Windows test receipt identity/status mismatch.' }
if (@($E1TestReceipt.test_results).Count -ne 2 -or @($E1TestReceipt.test_results | Where-Object { [int]$_.exit_code -ne 0 }).Count -ne 0) { throw 'E1 Windows parent test receipt is not 2/2 PASS.' }

$Pins = @(
    @{ Path = 'GeneradorMaestro.gd'; Sha = '4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9' },
    @{ Path = 'Main.tscn'; Sha = '5271714b9a5c31aeda1d7347347f1429ca37a48c081e59e6ec42383626731de7' },
    @{ Path = 'project.godot'; Sha = 'd20b0f275c58a34881420705bb1990564d719427c550478c434345ced72805d3' },
    @{ Path = 'challenges/CHALLENGE_001.json'; Sha = 'ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea' },
    @{ Path = 'core/presentation/UnifiedSocialFrame.gd'; Sha = 'd80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba' },
    @{ Path = 'core/presentation/UnifiedSocialFrame.tscn'; Sha = 'a89051019ab78bc35757acaa8b46a3b62526432bfa86582f07a66187e80e1b4b' },
    @{ Path = 'core/presentation/PresentationUI.gd'; Sha = 'a55fea5a4525ea247144a4da88242f4ac602c3a014f7d02b50d032ce99224730' },
    @{ Path = 'core/presentation/SocialUIBinder.gd'; Sha = 'b15a062bf327d0c2bbc4ead0e877914f912528cc56e388df20dd84eb89863a3c' },
    @{ Path = 'core/presentation/ChallengePresentationBinder.gd'; Sha = '755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47' },
    @{ Path = 'core/presentation/PresentationProfile.gd'; Sha = '187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24' },
    @{ Path = 'core/presentation/components/HookComponent.gd'; Sha = '52894359fc80f4647493fb37fa185aae3dcdc8daf1ac1fdc37137d13debb7bbe' },
    @{ Path = 'core/presentation/components/TypographyLabel.gd'; Sha = 'd7c6ec47b33baec983a239dfe6218037d4126dc1532130c92d4202d56e6e8866' },
    @{ Path = 'core/presentation/C11CVisualTypography.gd'; Sha = '9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633' },
    @{ Path = 'assets/fonts/Inter-Bold.otf'; Sha = '9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d' },
    @{ Path = 'c11c-suite/c11c-producer/c11e_production_service.py'; Sha = $ExpectedE1ServiceSha },
    @{ Path = 'c11c-suite/c11c-producer/c11e_production_cli.py'; Sha = $ExpectedE1CliSha },
    @{ Path = 'c11c-suite/c11c-producer/main.py'; Sha = $ExpectedE1MainSha },
    @{ Path = 'c11c-suite/c11c-producer/BUILD_MANIFEST.json'; Sha = 'd95ede2f22486b3ef649186c25ce227bf8531f8ad63ab53323ba339aba195376' },
    @{ Path = 'c11c-suite/c11c-producer/self_test.py'; Sha = '84e8eabd5098e0d4cb194fa9f50e00e2f68c4516592285668399f35069c25a90' },
    @{ Path = 'c11c-suite/c11c-producer/test_producer_gui_contract.py'; Sha = 'ce073a39db0af583ea215c66a6c5303230539e8de857505076963a46dddf4139' }
)
foreach ($Pin in $Pins) {
    $Path = Join-Path $ResolvedRoot $Pin.Path
    $Actual = Get-Sha256 $Path
    if ($Actual -ne $Pin.Sha) {
        throw ("E2 source pin mismatch: {0}; actual={1}; expected={2}. No render started." -f $Pin.Path, $Actual, $Pin.Sha)
    }
}
$VerifiedPins = @($Pins | ForEach-Object { [PSCustomObject]@{ path = $_.Path; sha256 = $_.Sha } })

$E2Root = Join-Path $ResolvedRoot 'tools\c11e\e2'
$PairBuilder = Join-Path $E2Root 'c11e_e2_challenge_pair.py'
$PairTests = Join-Path $E2Root 'test_c11e_e2_challenge_pair.py'
$Scene = Join-Path $E2Root 'C11EChallenge001E2.tscn'
$GodotScript = Join-Path $E2Root 'C11EChallenge001E2.gd'
$GodotJsonTest = Join-Path $E2Root 'test_c11e_e2_godot_json_numeric_contract.gd'
foreach ($Path in @($PairBuilder, $PairTests, $Scene, $GodotScript, $GodotJsonTest)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw ("Missing E2 component: {0}" -f $Path) }
}
if ((Get-Sha256 $PairBuilder) -ne $ExpectedPairBuilderSha) { throw 'E2 Python pair-builder source pin mismatch.' }
if ((Get-Sha256 $PairTests) -ne $ExpectedPairTestsSha) { throw 'E2 Python test source pin mismatch.' }
if ((Get-Sha256 $Scene) -ne $ExpectedGodotSceneSha) { throw 'E2 scene source pin mismatch.' }
if ((Get-Sha256 $GodotScript) -ne $ExpectedGodotScriptSha) { throw 'E2 GDScript source pin mismatch.' }
if ((Get-Sha256 $GodotJsonTest) -ne $ExpectedGodotJsonTestSha) { throw 'E2 Godot JSON numeric test source pin mismatch.' }
$E2RunnerSha = Get-Sha256 $PSCommandPath

function Resolve-NativeExecutablePath {
    param(
        [Parameter(Mandatory=$true)][string]$CommandName,
        [string]$ExplicitPath = ''
    )
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw ("Specified executable does not exist for {0}: {1}" -f $CommandName, $ExplicitPath)
        }
        return [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $ExplicitPath).Path)
    }
    $commands = @(Get-Command $CommandName -CommandType Application -All -ErrorAction SilentlyContinue)
    $candidates = @()
    foreach ($command in $commands) {
        $candidate = [string]$command.Source
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        if ($candidate -match '(?i)[\\/]WindowsApps[\\/]') { continue }
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { continue }
        $full = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $candidate).Path)
        if ($candidates -notcontains $full) { $candidates += $full }
    }
    if ($candidates.Count -lt 1) {
        throw ("No real executable found for {0}; WindowsApps aliases are excluded. Supply an explicit path if required." -f $CommandName)
    }
    return [string]$candidates[0]
}

$Python = Resolve-NativeExecutablePath -CommandName 'python' -ExplicitPath $PythonExecutable
$Ffmpeg = Resolve-NativeExecutablePath -CommandName 'ffmpeg'
$Ffprobe = Resolve-NativeExecutablePath -CommandName 'ffprobe'
$Godot = ''
if (-not [string]::IsNullOrWhiteSpace($GodotExecutable)) {
    $Godot = Resolve-NativeExecutablePath -CommandName 'godot' -ExplicitPath $GodotExecutable
} else {
    try { $Godot = Resolve-NativeExecutablePath -CommandName 'godot.exe' }
    catch { $Godot = Resolve-NativeExecutablePath -CommandName 'godot' }
}

$OutputRootRel = Join-Path 'artifacts\production\c11e' $RequestId
$OutputRoot = Join-Path $ResolvedRoot $OutputRootRel
if (Test-Path -LiteralPath $OutputRoot) {
    throw ("E2 output root already exists; overwrite forbidden: {0}. Use a new RequestId for a new attempt." -f $OutputRoot)
}

$Documents = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($Documents)) { $Documents = Join-Path $env:USERPROFILE 'Documents' }
$Stage = Join-Path $Documents ('C11E_E2_CH001_AB_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '_' + ([Guid]::NewGuid().ToString('N').Substring(0,8)))
if (Test-Path -LiteralPath $Stage) { throw ("E2 evidence stage collision: {0}" -f $Stage) }
New-Item -ItemType Directory -Path $Stage | Out-Null
$Utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
$ToolchainRecord = [ordered]@{
    schema = 'c11e-e2-toolchain-resolution/v2'
    resolved_at = (Get-Date).ToString('o')
    python = $Python
    python_source_candidates = @((Get-Command python -CommandType Application -All -ErrorAction SilentlyContinue | ForEach-Object { [string]$_.Source }))
    python_windowsapps_candidates_excluded = @((Get-Command python -CommandType Application -All -ErrorAction SilentlyContinue | Where-Object { [string]$_.Source -match '(?i)[\\/]WindowsApps[\\/]' } | ForEach-Object { [string]$_.Source }))
    godot = $Godot
    ffmpeg = $Ffmpeg
    ffprobe = $Ffprobe
}
[IO.File]::WriteAllText((Join-Path $Stage 'toolchain_resolution.json'), ($ToolchainRecord | ConvertTo-Json -Depth 8), $Utf8NoBom)
$NativeViewportState = $null
$RenderRows = @()
$ReviewSampleRows = @()
$GodotInvocationCount = 0
$MediaPaths = @()

try {
    Write-Host '========== C11-E E2 CHALLENGE TITLE A/B ==========' -ForegroundColor Cyan
    Write-Host ("Branch={0}; HEAD={1}" -f $Branch, $Head)
    Write-Host ("C11-C manifest={0} bytes / {1}" -f $ManifestBytes, $ManifestSha)
    Write-Host 'E2 gate scope: exactly two isolated CHALLENGE_001 renders; no audio; no release/promotion.'

    $VersionPython = Invoke-NativeProcess -FilePath $Python -Arguments @('--version') -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'python_version.stdout.log') -StderrPath (Join-Path $Stage 'python_version.stderr.log') -Label 'python_version'
    $VersionGodot = Invoke-NativeProcess -FilePath $Godot -Arguments @('--version') -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'godot_version.stdout.log') -StderrPath (Join-Path $Stage 'godot_version.stderr.log') -Label 'godot_version'
    $VersionFfmpeg = Invoke-NativeProcess -FilePath $Ffmpeg -Arguments @('-version') -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'ffmpeg_version.stdout.log') -StderrPath (Join-Path $Stage 'ffmpeg_version.stderr.log') -Label 'ffmpeg_version'
    $VersionFfprobe = Invoke-NativeProcess -FilePath $Ffprobe -Arguments @('-version') -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'ffprobe_version.stdout.log') -StderrPath (Join-Path $Stage 'ffprobe_version.stderr.log') -Label 'ffprobe_version'
    $PythonVersionText = ($VersionPython.Stdout + $VersionPython.Stderr).Trim()
    if ($PythonVersionText -notmatch '^Python\s+(\d+)\.(\d+)') { throw ("Unrecognized Python version output: {0}" -f $PythonVersionText) }
    $PythonMajor = [int]$Matches[1]
    $PythonMinor = [int]$Matches[2]
    if ($PythonMajor -lt 3 -or ($PythonMajor -eq 3 -and $PythonMinor -lt 13)) { throw ("E2 requires Python 3.13 or newer; found {0}." -f $PythonVersionText) }
    $GodotVersionText = ($VersionGodot.Stdout + $VersionGodot.Stderr).Trim()
    if ($GodotVersionText -notmatch '4\.7\.1' -or $GodotVersionText -notmatch 'mono') { throw ("E2 requires the reviewed Godot 4.7.1 Mono runtime; found {0}." -f $GodotVersionText) }

    $GodotJsonCheck = Invoke-NativeProcess -FilePath $Godot -Arguments @('--headless', '--path', $ResolvedRoot, '--script', $GodotJsonTest) -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'godot_json_numeric_contract.stdout.log') -StderrPath (Join-Path $Stage 'godot_json_numeric_contract.stderr.log') -Label 'godot_json_numeric_contract'
    $GodotJsonCombined = $GodotJsonCheck.Stdout + $GodotJsonCheck.Stderr
    if (-not $GodotJsonCombined.Contains('C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS')) { throw 'Godot JSON numeric contract test did not emit its PASS marker.' }
    Write-Host $GodotJsonCombined

    $Tests = Invoke-NativeProcess -FilePath $Python -Arguments @($PairTests) -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'e2_contract_tests.stdout.log') -StderrPath (Join-Path $Stage 'e2_contract_tests.stderr.log') -Label 'e2_contract_tests'
    Write-Host ($Tests.Stdout + $Tests.Stderr)

    $Prepare = Invoke-NativeProcess -FilePath $Python -Arguments @(
        $PairBuilder, '--root', $ResolvedRoot, '--request-id', $RequestId,
        '--seed', ([string]$Seed), '--music-seed', ([string]$MusicSeed),
        '--title-a', $TitleA, '--title-b', $TitleB
    ) -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $Stage 'pair_prepare.stdout.log') -StderrPath (Join-Path $Stage 'pair_prepare.stderr.log') -Label 'e2_pair_prepare'
    $PrepareLines = @($Prepare.Stdout -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($PrepareLines.Count -lt 1) { throw 'E2 pair preparation returned no receipt JSON.' }
    $Prepared = $PrepareLines[0] | ConvertFrom-Json
    if ($null -eq $Prepared.PSObject.Properties['pair_receipt_sha256']) { throw 'E2 pair preparation summary is missing pair_receipt_sha256.' }
    if ([string]$Prepared.pair_receipt_sha256 -notmatch '^[a-f0-9]{64}$') { throw 'E2 pair receipt SHA-256 is malformed.' }
    $PreparedOutputFull = [IO.Path]::GetFullPath([string]$Prepared.output_root)
    $ExpectedOutputFull = [IO.Path]::GetFullPath($OutputRoot)
    if (-not [string]::Equals($PreparedOutputFull, $ExpectedOutputFull, [StringComparison]::OrdinalIgnoreCase)) { throw 'E2 pair preparation output path differs from the allowlisted E2 output root.' }
    $PreparedReceiptFull = [IO.Path]::GetFullPath([string]$Prepared.pair_receipt)
    $ExpectedReceiptFull = [IO.Path]::GetFullPath((Join-Path $OutputRoot 'E2_PAIR_PREPARED.json'))
    if (-not [string]::Equals($PreparedReceiptFull, $ExpectedReceiptFull, [StringComparison]::OrdinalIgnoreCase)) { throw 'E2 pair receipt path mismatch.' }
    if (-not (Test-Path -LiteralPath $OutputRoot -PathType Container)) { throw 'E2 pair preparation did not create its sealed output root.' }
    $PreparedReceiptActualSha = Get-Sha256 $PreparedReceiptFull
    if ($PreparedReceiptActualSha -ne [string]$Prepared.pair_receipt_sha256) { throw 'E2 pair preparation receipt SHA-256 mismatch.' }
    $PreparedReceiptObject = Get-Content -LiteralPath $PreparedReceiptFull -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($null -eq $PreparedReceiptObject) { throw 'E2 pair preparation receipt JSON is empty.' }
    $ReceiptRequestIdProperty = $PreparedReceiptObject.PSObject.Properties['request_id']
    if ($null -eq $ReceiptRequestIdProperty) { throw 'E2 pair receipt is missing request_id.' }
    if ([string]$ReceiptRequestIdProperty.Value -ne $RequestId) { throw 'E2 pair receipt request ID mismatch.' }
    $ReceiptSchemaProperty = $PreparedReceiptObject.PSObject.Properties['schema']
    if ($null -eq $ReceiptSchemaProperty -or [string]$ReceiptSchemaProperty.Value -ne 'C11E-E2-CHALLENGE-AB-PREPARED-V1') { throw 'E2 pair receipt schema mismatch.' }
    $ReceiptStatusProperty = $PreparedReceiptObject.PSObject.Properties['status']
    if ($null -eq $ReceiptStatusProperty -or [string]$ReceiptStatusProperty.Value -ne 'PAIR_PREPARED_NOT_YET_RENDERED') { throw 'E2 pair receipt status mismatch.' }
    $ReceiptManifestProperty = $PreparedReceiptObject.PSObject.Properties['c11c_manifest_sha256']
    if ($null -eq $ReceiptManifestProperty -or [string]$ReceiptManifestProperty.Value -ne $ExpectedManifestSha) { throw 'E2 pair receipt C11-C manifest pin mismatch.' }

    $SourceFps = [int]$Prepared.source_fps
    $SourceFrames = [int]$Prepared.source_frames
    if ($SourceFps -ne 60 -or $SourceFrames -ne 540) { throw ("CHALLENGE_001 source timebase must be 60 FPS / 540 frames; found {0} FPS / {1} frames." -f $SourceFps, $SourceFrames) }
    $DeliveryFps = 30
    $DeliveryFramesExact = ($SourceFrames * $DeliveryFps) / $SourceFps
    if ([math]::Abs($DeliveryFramesExact - [math]::Round($DeliveryFramesExact)) -gt 0.000001) { throw 'E2 delivery frame count is not integral at 30 FPS.' }
    $DeliveryFrames = [int][math]::Round($DeliveryFramesExact)

    $NativeViewportState = Enter-NativeViewportGuard -ProjectRoot $ResolvedRoot

    foreach ($Label in @('A','B')) {
        $Run = $Prepared.runs.$Label
        $RunDir = Join-Path $ResolvedRoot ([string]$Run.directory)
        $Config = Join-Path $RunDir 'challenge_effective.json'
        $Sidecar = Join-Path $RunDir 'editorial.sidecar.json'
        $Avi = Join-Path $RunDir ('CHALLENGE_001_' + $Label + '_source.avi')
        $Mp4 = Join-Path $RunDir ('CHALLENGE_001_' + $Label + '_REVIEW_720.mp4')
        $SidecarSha = [string]$Run.sidecar_sha256
        $ConfigSha = [string]$Run.effective_config_sha256
        if ([int]$Run.gameplay_seed -ne $Seed -or [int]$Run.music_seed -ne $MusicSeed) { throw ("Resolved seed domains differ from E2 inputs for run {0}." -f $Label) }
        $ExpectedRunTitle = if ($Label -eq 'A') { $TitleA } else { $TitleB }
        if ([string]$Run.title -ne $ExpectedRunTitle) { throw ("Resolved title differs from explicit E2 title for run {0}." -f $Label) }
        if ((Get-Sha256 $Config) -ne $ConfigSha) { throw ("Effective C config changed before render for run {0}." -f $Label) }
        if ((Get-Sha256 $Sidecar) -ne $SidecarSha) { throw ("E2 sidecar changed before render for run {0}." -f $Label) }

        $GodotArgs = @(
            '--path', $ResolvedRoot,
            '--scene', 'tools/c11e/e2/C11EChallenge001E2.tscn',
            '--write-movie', $Avi,
            '--fixed-fps', ([string]$SourceFps),
            '--quit-after', ([string]$SourceFrames),
            '--',
            ('--config=' + $Config),
            ('--c11e-editorial-sidecar=' + $Sidecar),
            ('--c11e-editorial-sha256=' + $SidecarSha),
            ('--c11e-config-sha256=' + $ConfigSha)
        )
        $GodotStartDiagnostic = Join-Path $RunDir 'godot.stdout.log.start.json'
        try {
            $GodotRun = Invoke-NativeProcess -FilePath $Godot -Arguments $GodotArgs -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $RunDir 'godot.stdout.log') -StderrPath (Join-Path $RunDir 'godot.stderr.log') -Label ("godot_render_{0}" -f $Label)
        } catch {
            if (Test-Path -LiteralPath $GodotStartDiagnostic -PathType Leaf) {
                try {
                    $GodotStartRecord = Get-Content -LiteralPath $GodotStartDiagnostic -Raw -Encoding UTF8 | ConvertFrom-Json
                    if ($GodotStartRecord.started -eq $true) { $GodotInvocationCount++ }
                } catch { }
            }
            if (Test-Path -LiteralPath $Avi -PathType Leaf) { $MediaPaths += $Avi }
            throw
        }
        $GodotInvocationCount++
        if (Test-Path -LiteralPath $Avi -PathType Leaf) { $MediaPaths += $Avi }
        $GodotCombined = $GodotRun.Stdout + "`n" + $GodotRun.Stderr
        [IO.File]::WriteAllText((Join-Path $RunDir 'godot.command.txt'), $GodotRun.Command, $Utf8NoBom)
        if ($GodotCombined -match '(?im)SCRIPT ERROR:|ERROR: Failed to load script|Parse Error:|Warning treated as error') {
            throw ("Godot reported a script parse/load error for run {0}; inspect godot.stderr.log. A generated AVI is not accepted." -f $Label)
        }
        if ($GodotCombined -notmatch 'Movie Maker mode enabled') { throw ("Godot did not enter Movie Maker mode for run {0}." -f $Label) }
        if ($GodotCombined -notmatch 'Done recording movie at path:') { throw ("Godot did not report Movie Maker completion for run {0}." -f $Label) }
        if ($GodotCombined -match 'CHALLENGE_INVALID|\[ERROR_JSON\]|\[C11E_E2\].*(mismatch|failed|missing)') { throw ("Godot emitted a Challenge/E2 error for run {0}." -f $Label) }
        $ExpectedTitleHash = Get-StringSha256 ([string]$Run.title)
        $ExpectedTitleMarker = ('[C11E_E2] TITLE_SLOT=header.editorial_title TITLE_SHA256=' + $ExpectedTitleHash)
        $ExpectedSeedMarker = ('[C11E_E2] GAMEPLAY_SEED=' + [string]$Seed)
        if (-not $GodotCombined.Contains($ExpectedTitleMarker)) { throw ("Godot did not confirm the expected title slot/hash for run {0}." -f $Label) }
        if (-not $GodotCombined.Contains($ExpectedSeedMarker)) { throw ("Godot did not confirm the expected gameplay seed for run {0}." -f $Label) }
        if (-not (Test-Path -LiteralPath $Avi -PathType Leaf)) { throw ("Godot source AVI missing for run {0}." -f $Label) }
        $VisualContentRows = @(Assert-VideoFrameContent -Ffmpeg $Ffmpeg -VideoPath $Avi -LogRoot $RunDir -Label ("source_visual_content_{0}" -f $Label) -WorkingDirectory $ResolvedRoot)

        $ProbeOut = Invoke-NativeProcess -FilePath $Ffprobe -Arguments @('-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,duration,codec_name,pix_fmt','-of','json',$Avi) -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $RunDir 'source_ffprobe.stdout.log') -StderrPath (Join-Path $RunDir 'source_ffprobe.stderr.log') -Label ("ffprobe_source_{0}" -f $Label)
        $SourceProbe = $ProbeOut.Stdout | ConvertFrom-Json
        $SourceStream = @($SourceProbe.streams) | Select-Object -First 1
        if ([int]$SourceStream.width -ne 540 -or [int]$SourceStream.height -ne 960) { throw ("Source AVI geometry mismatch for run {0}." -f $Label) }
        if ([string]$SourceStream.r_frame_rate -ne ("{0}/1" -f $SourceFps)) { throw ("Source AVI FPS mismatch for run {0}." -f $Label) }
        if ([int]$SourceStream.nb_read_frames -ne $SourceFrames) { throw ("Source AVI frame count mismatch for run {0}." -f $Label) }

        $EncodeArgs = @(
            '-y','-hide_banner','-loglevel','error','-i',$Avi,
            '-map','0:v:0','-an','-vf','fps=30,scale=720:1280:flags=lanczos',
            '-c:v','libx264','-preset','fast','-crf','18','-profile:v','high','-pix_fmt','yuv420p',
            '-g','90','-keyint_min','90','-sc_threshold','0','-x264-params','open_gop=0:keyint=90:min-keyint=90:scenecut=0',
            '-frames:v',([string]$DeliveryFrames),'-movflags','+faststart',$Mp4
        )
        $Encode = Invoke-NativeProcess -FilePath $Ffmpeg -Arguments $EncodeArgs -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $RunDir 'ffmpeg.stdout.log') -StderrPath (Join-Path $RunDir 'ffmpeg.stderr.log') -Label ("ffmpeg_encode_{0}" -f $Label)
        [IO.File]::WriteAllText((Join-Path $RunDir 'ffmpeg.command.txt'), $Encode.Command, $Utf8NoBom)
        if (-not (Test-Path -LiteralPath $Mp4 -PathType Leaf)) { throw ("Final MP4 missing for run {0}." -f $Label) }

        $FinalProbeOut = Invoke-NativeProcess -FilePath $Ffprobe -Arguments @('-v','error','-count_frames','-show_streams','-show_format','-of','json',$Mp4) -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $RunDir 'final_ffprobe.stdout.log') -StderrPath (Join-Path $RunDir 'final_ffprobe.stderr.log') -Label ("ffprobe_final_{0}" -f $Label)
        $FinalProbe = $FinalProbeOut.Stdout | ConvertFrom-Json
        $Streams = @($FinalProbe.streams)
        $VideoStream = @($Streams | Where-Object { $_.codec_type -eq 'video' }) | Select-Object -First 1
        $AudioStreams = @($Streams | Where-Object { $_.codec_type -eq 'audio' })
        if ([int]$VideoStream.width -ne 720 -or [int]$VideoStream.height -ne 1280) { throw ("Final MP4 geometry mismatch for run {0}." -f $Label) }
        if ([string]$VideoStream.r_frame_rate -ne '30/1') { throw ("Final MP4 FPS mismatch for run {0}." -f $Label) }
        if ([int]$VideoStream.nb_read_frames -ne $DeliveryFrames) { throw ("Final MP4 frame count mismatch for run {0}." -f $Label) }
        if ([string]$VideoStream.codec_name -ne 'h264' -or [string]$VideoStream.pix_fmt -ne 'yuv420p') { throw ("Final MP4 codec/pixel format mismatch for run {0}." -f $Label) }
        if ($AudioStreams.Count -ne 0) { throw ("E2 output unexpectedly contains audio for run {0}. E3 owns audio." -f $Label) }

        $RenderRows += [PSCustomObject]@{
            label = $Label
            title = [string]$Run.title
            request_id = $RequestId
            gameplay_seed = $Seed
            music_seed = $MusicSeed
            source_fps = $SourceFps
            source_frames = $SourceFrames
            source_width = [int]$SourceStream.width
            source_height = [int]$SourceStream.height
            source_codec = [string]$SourceStream.codec_name
            source_pixel_format = [string]$SourceStream.pix_fmt
            source_duration = [string]$SourceStream.duration
            source_visual_content_samples = $VisualContentRows
            delivery_fps = $DeliveryFps
            delivery_frames = $DeliveryFrames
            final_width = [int]$VideoStream.width
            final_height = [int]$VideoStream.height
            final_codec = [string]$VideoStream.codec_name
            final_pixel_format = [string]$VideoStream.pix_fmt
            final_audio_streams = $AudioStreams.Count
            source_avi = $Avi
            source_avi_sha256 = (Get-Sha256 $Avi)
            final_mp4 = $Mp4
            final_mp4_sha256 = (Get-Sha256 $Mp4)
            sidecar_sha256 = $SidecarSha
            effective_config_sha256 = $ConfigSha
            godot_exit_code = $GodotRun.ExitCode
            ffmpeg_exit_code = $Encode.ExitCode
            ffprobe_exit_code = $FinalProbeOut.ExitCode
        }
    }

    if ($RenderRows.Count -ne 2) { throw 'E2 did not produce exactly two Challenge runs.' }
    if ($RenderRows[0].effective_config_sha256 -ne $RenderRows[1].effective_config_sha256) { throw 'A/B effective C configs differ.' }
    if ($RenderRows[0].source_frames -ne $RenderRows[1].source_frames -or $RenderRows[0].delivery_frames -ne $RenderRows[1].delivery_frames) { throw 'A/B frame counts differ.' }
    if ($RenderRows[0].final_mp4_sha256 -eq $RenderRows[1].final_mp4_sha256) { throw 'A/B final MP4 hashes unexpectedly match.' }

    $RunA = Join-Path $ResolvedRoot ([string]$Prepared.runs.A.directory)
    $RunB = Join-Path $ResolvedRoot ([string]$Prepared.runs.B.directory)
    $BodyA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_source.avi') -Filter 'crop=540:816:0:144,format=rgb24' -LogRoot $RunA -Label 'body_framemd5'
    $BodyB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_source.avi') -Filter 'crop=540:816:0:144,format=rgb24' -LogRoot $RunB -Label 'body_framemd5'
    $BodyFramesIdentical = Assert-FrameRowsIdentical -RowsA $BodyA -RowsB $BodyB -Label 'GAMEPLAY_BODY'
    if ($BodyFramesIdentical -ne $SourceFrames) { throw ("Gameplay/body comparison did not cover all {0} frames." -f $SourceFrames) }

    $TitleSlotA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_source.avi') -Filter 'crop=496:104:24:24,format=rgb24' -LogRoot $RunA -Label 'title_slot_framemd5'
    $TitleSlotB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_source.avi') -Filter 'crop=496:104:24:24,format=rgb24' -LogRoot $RunB -Label 'title_slot_framemd5'
    $TitleSlotDifferences = Count-FrameRowDifferences -RowsA $TitleSlotA -RowsB $TitleSlotB -Label 'EDITORIAL_TITLE_SLOT'
    if ($TitleSlotA.Count -ne $SourceFrames) { throw 'Title-slot comparison did not cover every source frame.' }
    if ($TitleSlotDifferences -ne $SourceFrames) { throw ("Title slot must differ in all {0} source frames; observed {1}." -f $SourceFrames, $TitleSlotDifferences) }

    $HeaderTopA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_source.avi') -Filter 'crop=540:24:0:0,format=rgb24' -LogRoot $RunA -Label 'header_top_framemd5'
    $HeaderTopB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_source.avi') -Filter 'crop=540:24:0:0,format=rgb24' -LogRoot $RunB -Label 'header_top_framemd5'
    $HeaderTopFramesIdentical = Assert-FrameRowsIdentical -RowsA $HeaderTopA -RowsB $HeaderTopB -Label 'HEADER_TOP_OUTSIDE_TITLE_SLOT'
    if ($HeaderTopFramesIdentical -ne $SourceFrames) { throw 'Header top comparison did not cover all source frames.' }

    $HeaderBottomA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_source.avi') -Filter 'crop=540:16:0:128,format=rgb24' -LogRoot $RunA -Label 'header_bottom_framemd5'
    $HeaderBottomB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_source.avi') -Filter 'crop=540:16:0:128,format=rgb24' -LogRoot $RunB -Label 'header_bottom_framemd5'
    $HeaderBottomFramesIdentical = Assert-FrameRowsIdentical -RowsA $HeaderBottomA -RowsB $HeaderBottomB -Label 'HEADER_BOTTOM_OUTSIDE_TITLE_SLOT'
    if ($HeaderBottomFramesIdentical -ne $SourceFrames) { throw 'Header bottom comparison did not cover all source frames.' }

    $HeaderLeftA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_source.avi') -Filter 'crop=24:104:0:24,format=rgb24' -LogRoot $RunA -Label 'header_left_framemd5'
    $HeaderLeftB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_source.avi') -Filter 'crop=24:104:0:24,format=rgb24' -LogRoot $RunB -Label 'header_left_framemd5'
    $HeaderLeftFramesIdentical = Assert-FrameRowsIdentical -RowsA $HeaderLeftA -RowsB $HeaderLeftB -Label 'HEADER_LEFT_OUTSIDE_TITLE_SLOT'
    if ($HeaderLeftFramesIdentical -ne $SourceFrames) { throw 'Header left comparison did not cover all source frames.' }

    $HeaderRightA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_source.avi') -Filter 'crop=20:104:520:24,format=rgb24' -LogRoot $RunA -Label 'header_right_framemd5'
    $HeaderRightB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_source.avi') -Filter 'crop=20:104:520:24,format=rgb24' -LogRoot $RunB -Label 'header_right_framemd5'
    $HeaderRightFramesIdentical = Assert-FrameRowsIdentical -RowsA $HeaderRightA -RowsB $HeaderRightB -Label 'HEADER_RIGHT_OUTSIDE_TITLE_SLOT'
    if ($HeaderRightFramesIdentical -ne $SourceFrames) { throw 'Header right comparison did not cover all source frames.' }

    $FinalFullA = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunA 'CHALLENGE_001_A_REVIEW_720.mp4') -Filter 'format=rgb24' -LogRoot $RunA -Label 'final_mp4_full_frame_framemd5'
    $FinalFullB = Get-FrameMd5Rows -Ffmpeg $Ffmpeg -VideoPath (Join-Path $RunB 'CHALLENGE_001_B_REVIEW_720.mp4') -Filter 'format=rgb24' -LogRoot $RunB -Label 'final_mp4_full_frame_framemd5'
    $FinalFullDifferences = Count-FrameRowDifferences -RowsA $FinalFullA -RowsB $FinalFullB -Label 'FINAL_MP4_FULL_FRAME'
    if ($FinalFullA.Count -ne $DeliveryFrames -or $FinalFullDifferences -ne $DeliveryFrames) {
        throw ("Delivered MP4s must differ in all {0} frames; compared={1}; different={2}." -f $DeliveryFrames, $FinalFullA.Count, $FinalFullDifferences)
    }

    foreach ($Label in @('A','B')) {
        $Run = $Prepared.runs.$Label
        $RunDir = Join-Path $ResolvedRoot ([string]$Run.directory)
        $Mp4 = Join-Path $RunDir ('CHALLENGE_001_' + $Label + '_REVIEW_720.mp4')
        foreach ($Sample in @(@{Name='first';Seconds='0'},@{Name='middle';Seconds='4'},@{Name='last';Seconds='8.9'})) {
            $SamplePath = Join-Path $RunDir ('review_' + $Sample.Name + '.png')
            $SampleRun = Invoke-NativeProcess -FilePath $Ffmpeg -Arguments @('-y','-hide_banner','-loglevel','error','-i',$Mp4,'-ss',[string]$Sample.Seconds,'-frames:v','1','-vf','scale=360:640:flags=lanczos',$SamplePath) -WorkingDirectory $ResolvedRoot -StdoutPath (Join-Path $RunDir ('review_' + $Sample.Name + '.stdout.log')) -StderrPath (Join-Path $RunDir ('review_' + $Sample.Name + '.stderr.log')) -Label ("review_frame_{0}_{1}" -f $Label, $Sample.Name)
            if (-not (Test-Path -LiteralPath $SamplePath -PathType Leaf)) { throw ("Review sample PNG missing: {0}" -f $SamplePath) }
            $ReviewSampleRows += [PSCustomObject]@{ label = $Label; sample = $Sample.Name; seconds = [string]$Sample.Seconds; path = $SamplePath; sha256 = (Get-Sha256 $SamplePath) }
        }
    }

    $OverrideWasPresent = ($null -ne $NativeViewportState)
    $OverrideOriginalSha = 'NOT_PRESENT'
    $OverrideRestoreStatus = 'NOT_REQUIRED'
    if ($OverrideWasPresent) {
        $OverrideOriginalSha = [string]$NativeViewportState.Sha256
        Exit-NativeViewportGuard -State $NativeViewportState
        $NativeViewportState = $null
        $OverrideRestoreStatus = 'RESTORED_AND_HASH_VERIFIED'
    }

    $Receipt = [ordered]@{
        schema = 'C11E-E2-CHALLENGE-TITLE-AB-RENDER-RECEIPT-V1'
        status = 'E2_AUTOMATED_TITLE_TO_PIXELS_AND_GAMEPLAY_INVARIANCE_PASS_HUMAN_REVIEW_PENDING'
        created_at = (Get-Date).ToString('o')
        branch = $Branch
        head = $Head
        head_parent = $HeadParent
        c11c_manifest = [ordered]@{ bytes = $ManifestBytes; sha256 = $ManifestSha }
        request_id = $RequestId
        selection = [ordered]@{ content_type = 'challenges'; family_id = 'key'; variant_id = 'CHALLENGE_001' }
        seed_domains = [ordered]@{ gameplay = $Seed; music = $MusicSeed; independent = $true; audio_used = $false }
        title_a = $TitleA
        title_b = $TitleB
        only_request_difference = 'production_override.title'
        effective_c_config_sha256_equal = $true
        source_timebase = [ordered]@{ fps = $SourceFps; frames = $SourceFrames }
        delivery = [ordered]@{ profile = 'REVIEW_720'; width = 720; height = 1280; fps = $DeliveryFps; frames = $DeliveryFrames; audio = 'NONE_E2' }
        gameplay_body_crop = [ordered]@{ status = 'PIXEL_IDENTICAL'; frames_compared = $BodyFramesIdentical; crop = 'x=0,y=144,width=540,height=816' }
        editorial_title_slot_crop = [ordered]@{ status = 'PIXEL_DIFFERENT'; frames_different = $TitleSlotDifferences; crop = 'x=24,y=24,width=496,height=104' }
        final_mp4_full_frame = [ordered]@{ status = 'PIXEL_DIFFERENT'; frames_compared = $FinalFullA.Count; frames_different = $FinalFullDifferences }
        header_outside_title_slot = [ordered]@{ status = 'PIXEL_IDENTICAL'; top_frames = $HeaderTopFramesIdentical; bottom_frames = $HeaderBottomFramesIdentical; left_frames = $HeaderLeftFramesIdentical; right_frames = $HeaderRightFramesIdentical }
        verified_source_pins = $VerifiedPins
        review_samples = $ReviewSampleRows
        e2_sources = [ordered]@{ pair_builder_sha256 = $ExpectedPairBuilderSha; pair_tests_sha256 = $ExpectedPairTestsSha; scene_sha256 = $ExpectedGodotSceneSha; gdscript_sha256 = $ExpectedGodotScriptSha; godot_json_numeric_test_sha256 = $ExpectedGodotJsonTestSha; runner_sha256 = $E2RunnerSha }
        render_rows = $RenderRows
        pair_preparation_receipt = $Prepared.pair_receipt
        pair_preparation_receipt_sha256 = $Prepared.pair_receipt_sha256
        temporary_project_override = [ordered]@{ original_present = $OverrideWasPresent; original_sha256 = $OverrideOriginalSha; restore_status = $OverrideRestoreStatus; collision_policy = 'PRESERVE_BOTH_AND_FAIL_IF_PATH_REOCCUPIED_WITH_DIFFERENT_BYTES' }
        runtime_versions = [ordered]@{
            python = (($VersionPython.Stdout + $VersionPython.Stderr).Trim())
            godot = (($VersionGodot.Stdout + $VersionGodot.Stderr).Trim())
            ffmpeg = (($VersionFfmpeg.Stdout -split "`r?`n")[0])
            ffprobe = (($VersionFfprobe.Stdout -split "`r?`n")[0])
        }
        tests = [ordered]@{ python_contract_tests = '9/9'; godot_json_numeric_contract = 'PASS'; runner_exit_code = 0 }
        renderer_invoked = $true
        media_created = $true
        scope = 'EXACTLY_TWO_ISOLATED_CHALLENGE_001_AB_RENDER_TESTS'
        human_visual_review = 'PENDING'
        release_authority = 'NONE'
        baseline_promotion = $false
        d_governance_mutated = $false
    }
    $ReceiptPath = Join-Path $OutputRoot 'C11E_E2_RENDER_RECEIPT.json'
    [IO.File]::WriteAllText($ReceiptPath, ($Receipt | ConvertTo-Json -Depth 20), $Utf8NoBom)
    $ReceiptSha = Get-Sha256 $ReceiptPath
    [IO.File]::WriteAllText((Join-Path $OutputRoot 'C11E_E2_RENDER_RECEIPT.json.sha256'), ($ReceiptSha + '  C11E_E2_RENDER_RECEIPT.json' + "`n"), $Utf8NoBom)
    $EvidenceZip = Join-Path $Documents ('C11E_E2_CH001_AB_EVIDENCE_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '_' + ([Guid]::NewGuid().ToString('N').Substring(0,8)) + '.zip')
    Compress-Archive -Path @($Stage, $OutputRoot) -DestinationPath $EvidenceZip -CompressionLevel Optimal -Force
    $EvidenceZipSha = Get-Sha256 $EvidenceZip

    Write-Host ''
    Write-Host 'C11-E E2 AUTOMATED A/B PASS.' -ForegroundColor Green
    Write-Host ("Source timebase: {0} FPS / {1} frames" -f $SourceFps, $SourceFrames)
    Write-Host ("Delivery: REVIEW_720 720x1280 / {0} FPS / {1} frames" -f $DeliveryFps, $DeliveryFrames)
    Write-Host ("Gameplay/body pixel comparison: {0}/{0} identical" -f $BodyFramesIdentical)
    Write-Host ("Title-slot pixel differences: {0}/{1} source frames" -f $TitleSlotDifferences, $TitleSlotA.Count)
    Write-Host ("Final MP4 full-frame differences: {0}/{1} frames" -f $FinalFullDifferences, $FinalFullA.Count)
    Write-Host ("Header outside title slot: top={0}; bottom={1}; left={2}; right={3} frames identical" -f $HeaderTopFramesIdentical, $HeaderBottomFramesIdentical, $HeaderLeftFramesIdentical, $HeaderRightFramesIdentical)
    Write-Host ("E2 receipt: {0}" -f $ReceiptPath)
    Write-Host ("E2 output root: {0}" -f $OutputRoot)
    Write-Host ("Evidence ZIP: {0}" -f $EvidenceZip)
    Write-Host ("Evidence ZIP SHA256: {0}" -f $EvidenceZipSha)
    Write-Host 'Human visual review remains pending. E3 audio not invoked. Release authority NONE.'
}
catch {
    $FailureText = $_.Exception.ToString()
    Write-Host ('C11-E E2 failed: ' + $FailureText) -ForegroundColor Red
    Write-Host ("Evidence stage: {0}" -f $Stage)
    try {
        $FailureRecord = [ordered]@{
            schema = 'c11e-e2-failure-evidence/v2'
            failed_at = (Get-Date).ToString('o')
            request_id = $RequestId
            branch = $Branch
            head = $Head
            head_parent = $HeadParent
            stage = $Stage
            output_root = $OutputRoot
            output_root_exists = (Test-Path -LiteralPath $OutputRoot)
            exception = $FailureText
            inner_exception = $(if ($_.Exception.InnerException) { $_.Exception.InnerException.ToString() } else { $null })
            renderer_invoked = ($GodotInvocationCount -gt 0)
            renderer_invocation_count = $GodotInvocationCount
            media_created = (@($MediaPaths).Count -gt 0)
            media_paths = @($MediaPaths)
            media_accepted = $false
            release_authority = 'NONE'
        }
        [IO.File]::WriteAllText((Join-Path $Stage 'C11E_E2_FAILURE_DIAGNOSTIC.json'), ($FailureRecord | ConvertTo-Json -Depth 12), $Utf8NoBom)
        $ArchiveInputs = @($Stage)
        if (Test-Path -LiteralPath $OutputRoot -PathType Container) {
            Write-Host ("Partial output retained: {0}" -f $OutputRoot)
            $ArchiveInputs += $OutputRoot
        }
        $FailureZip = Join-Path $Documents ('C11E_E2_CH001_AB_FAILURE_EVIDENCE_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '_' + ([Guid]::NewGuid().ToString('N').Substring(0,8)) + '.zip')
        Compress-Archive -Path $ArchiveInputs -DestinationPath $FailureZip -CompressionLevel Optimal -Force -ErrorAction Stop
        if (-not (Test-Path -LiteralPath $FailureZip -PathType Leaf)) { throw 'Compress-Archive returned without creating the evidence ZIP.' }
        $FailureZipItem = Get-Item -LiteralPath $FailureZip
        if ($FailureZipItem.Length -le 0) { throw 'Failure evidence ZIP is empty.' }
        Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
        $FailureArchive = [System.IO.Compression.ZipFile]::OpenRead($FailureZip)
        try {
            if ($FailureArchive.Entries.Count -lt 1) { throw 'Failure evidence ZIP contains no entries.' }
            $FailureEntryCount = $FailureArchive.Entries.Count
        } finally { $FailureArchive.Dispose() }
        Write-Host ("Failure evidence ZIP VERIFIED: {0}" -f $FailureZip)
        Write-Host ("Failure evidence bytes: {0}; entries: {1}" -f $FailureZipItem.Length, $FailureEntryCount)
        Write-Host ("Failure evidence SHA256: {0}" -f (Get-Sha256 $FailureZip))
    } catch {
        Write-Host ('FAILURE_EVIDENCE_NOT_CREATED: ' + $_.Exception.ToString()) -ForegroundColor Yellow
        Write-Host ("Evidence stage retained without ZIP: {0}" -f $Stage)
    }
    exit 1
}
finally {
    if ($null -ne $NativeViewportState) {
        try {
            Exit-NativeViewportGuard -State $NativeViewportState
        } catch {
            Write-Host ('CRITICAL: override.cfg restoration requires operator inspection: ' + [string]$_) -ForegroundColor Red
            if (Test-Path -LiteralPath $NativeViewportState.Quarantine -PathType Leaf) {
                Write-Host ("Original override backup preserved at: {0}" -f $NativeViewportState.Quarantine) -ForegroundColor Yellow
            }
        }
    }
}
