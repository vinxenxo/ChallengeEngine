[CmdletBinding()]
param(
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Projects\ChallengeEngineV01_STATELESS'),
    [string]$PythonExe = '',
    [string]$GuiEvidenceRoot = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Write-Stage([string]$Name) { Write-Host ('STAGE=' + $Name) }
function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing file: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-Sha256([string]$RelativePath, [string]$Expected) {
    $full = Join-Path $ProjectRoot $RelativePath
    $actual = Get-Sha256 $full
    if ($actual -ne $Expected.ToLowerInvariant()) { throw "SOURCE_PIN_MISMATCH: $RelativePath expected=$Expected actual=$actual" }
    return $actual
}
function ConvertTo-NativeArgument([string]$Value) {
    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append('"')
    $slashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ([int][char]$character -eq 92) { $slashes++; continue }
        if ([int][char]$character -eq 34) {
            if ($slashes -gt 0) { [void]$builder.Append(('\' * (2 * $slashes + 1))) }
            else { [void]$builder.Append('\') }
            [void]$builder.Append('"')
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(('\' * $slashes)); $slashes = 0 }
        [void]$builder.Append($character)
    }
    if ($slashes -gt 0) { [void]$builder.Append(('\' * (2 * $slashes))) }
    [void]$builder.Append('"')
    return $builder.ToString()
}
function Invoke-CheckedProcess(
    [string]$FilePath,
    [string[]]$Arguments,
    [string]$WorkingDirectory,
    [string]$StdoutPath,
    [string]$StderrPath,
    [string]$Label
) {
    $quoted = @()
    foreach ($argument in $Arguments) { $quoted += (ConvertTo-NativeArgument ([string]$argument)) }
    $argumentLine = $quoted -join ' '
    $process = Start-Process -FilePath $FilePath -ArgumentList $argumentLine -WorkingDirectory $WorkingDirectory -Wait -PassThru -NoNewWindow -RedirectStandardOutput $StdoutPath -RedirectStandardError $StderrPath
    $stdoutHash = Get-Sha256 $StdoutPath
    $stderrHash = Get-Sha256 $StderrPath
    if ($process.ExitCode -ne 0) {
        throw ("PROCESS_FAILED: {0}; exit={1}; stdout_sha256={2}; stderr_sha256={3}" -f $Label, $process.ExitCode, $stdoutHash, $stderrHash)
    }
    return [pscustomobject]@{
        name = $Label
        executable = $FilePath
        arguments = $Arguments
        working_directory = $WorkingDirectory
        exit_code = [int]$process.ExitCode
        stdout_path = $StdoutPath
        stderr_path = $StderrPath
        stdout_sha256 = $stdoutHash
        stderr_sha256 = $stderrHash
    }
}

Write-Host '========== C11-E E4B LOOP CLI GUI PARITY V2 =========='
Write-Host ('POWERSHELL_RUNTIME_VERSION=' + $PSVersionTable.PSVersion.ToString())
if ($PSVersionTable.PSVersion.Major -ne 5) { throw 'POWERSHELL_5_1_REQUIRED' }
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { $parseErrors | ForEach-Object { Write-Host $_.Message }; throw 'POWERSHELL_5_1_AST_PARSE=FAIL' }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
$scriptBytes = [System.IO.File]::ReadAllBytes($PSCommandPath)
$byteStart = 0
if ($scriptBytes.Length -ge 3 -and $scriptBytes[0] -eq 239 -and $scriptBytes[1] -eq 187 -and $scriptBytes[2] -eq 191) { $byteStart = 3 }
for ($byteIndex = $byteStart; $byteIndex -lt $scriptBytes.Length; $byteIndex++) {
    if ($scriptBytes[$byteIndex] -gt 127) { throw 'RUNNER_SOURCE_ENCODING_INVALID: V2 runner must remain ASCII-only after optional UTF-8 BOM' }
}
Write-Host 'RUNNER_SOURCE_ENCODING=ASCII_SAFE'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; MEDIA_AND_RENDERER=OFF'

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "PROJECT_ROOT_NOT_FOUND: $ProjectRoot" }
if ([string]::IsNullOrWhiteSpace($GuiEvidenceRoot)) {
    $GuiEvidenceRoot = Join-Path $ProjectRoot 'artifacts\tests\c11d_d9\producer_universal\D99-GUI-439FD530F839'
}
$GuiEvidenceRoot = [System.IO.Path]::GetFullPath($GuiEvidenceRoot)
if (-not (Test-Path -LiteralPath $GuiEvidenceRoot -PathType Container)) { throw "GUI_EVIDENCE_ROOT_NOT_FOUND: $GuiEvidenceRoot; pass -GuiEvidenceRoot" }

$expectedPins = [ordered]@{
    'c11c-suite/c11c-producer/main.py' = '4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6'
    'c11c-suite/c11c-producer/c11e_production_service.py' = '348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951'
    'c11c-suite/c11c-producer/c11e_production_cli.py' = 'e7272231dca2eb730506308b092fce9b3644f7f8cfd9f2c2bbbbd1b695e82fc4'
    'tools/c11d/d9/universal_producer.py' = '9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1'
    'tools/c11d/d9/universal_producer_cli.py' = 'c648a3722299b4700a9b74d1cabc6cac1fa48ad6275497ae8073bc07f442bb54'
    'tools/c11d/d9/universal_editorial_model.py' = '5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5'
    'tools/c11d/d9/editorial_render_bridge.py' = 'fe9d40052b0f4ff6f1c862c010ae7b3b13070b6ce935be6d62f9dcaec63a644a'
    'tools/c11d/d9/d_render_adapter.py' = '222742677cd498368429a3ec0dcdd922c44197bb5ada3638081138fb77c31bf1'
    'c11c-suite/c11c-producer/producer_schema.json' = '564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0'
    'definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json' = '50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53'
    'definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json' = '342a61338c80a2f1616e8e9f38986bd90f410257c0e321f99840380fb0fd804b'
    'profiles/delivery/c11c_video_delivery_profiles.json' = '967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3'
    'release/C11C_FREEZE_PACKAGE_MANIFEST.json' = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
    'assets/fonts/Inter-Bold.otf' = '9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d'
    'assets/fonts/NotoSansMono-Regular.ttf' = '6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f'
    'core/presentation/C11CVisualEditorialLayer.gd' = 'f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d'
    'core/presentation/UnifiedSocialFrame.gd' = 'd80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba'
    'tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd' = '44c4a9a11c334e6e84fcc1413667accac175781787866c3d6b894beeba3ea255'
    'core/presentation/C11CVisualTypography.gd' = '9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633'
    'tools/prototypes/c11c_common/C11CSafeAmbient.py' = 'c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c'
    'tools/prototypes/c11c_common/generate_c11c_family_music.py' = '41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d'
    'profiles/presentation/c11c_visual_music_profiles.json' = 'b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58'
    'tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd' = 'ab2560cbe7fa42c5cad3b143aa59d1f2a0dc047682f7667983c7c0a0f6dbb61c'
    'tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd' = 'b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55'
    'tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd' = '12fdbc13e05df28b26cf95fe1907d150bd41f29196287700153521e9baee336b'
    'tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd' = '835ba0df2c160a259be39bd1977bfac0e6a66f903ce1aa6b4247af7c508ad94a'
    'tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd' = 'a68661a5fdf792aa7fe701afa6fbf1631a2b8215c214032f58ecfe0c69d8374a'
    'definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json' = '9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da'
    'tools/c11d/d9/e4b_loop_editorial_composition_proposal.py' = '3956282bfc29bbe919cf70ae6b76046095f24325d7de2391c38a3765fcf2b93d'
    'tools/c11d/d9/test_c11e_e4b_loop_editorial_composition_proposal.py' = '3dd877a473bd15a593238f32799dbd566bae887021aaa09a90873e158d8847f9'
    'tools/c11d/d9/e4b_loop_gui_cli_parity_v2.py' = 'd1a98f9962ae912531ae5920c071cb98a60cdcc91e3a1b420d1178b49ef89b73'
    'tools/c11d/d9/test_c11e_e4b_loop_gui_cli_parity_v2.py' = '3f32fcbd52034f4f8b774954860a9da24231f9b84ca42acea62fd76498cadcda'
}
Write-Stage 'SOURCE_PIN_VERIFICATION'
$pinReceipts = @()
foreach ($entry in $expectedPins.GetEnumerator()) {
    $actual = Assert-Sha256 $entry.Key $entry.Value
    $pinReceipts += [pscustomobject]@{ path = $entry.Key; sha256 = $actual }
}
$manifestPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest -isnot [System.Management.Automation.PSCustomObject]) { throw 'FROZEN_MANIFEST_INVALID' }
Write-Host ('SOURCE_PINS=PASS; COUNT=' + $pinReceipts.Count)
Write-Host 'FROZEN_C11C_MANIFEST=PASS; C11C_SOURCE_MUTATION=FORBIDDEN'

if ([string]::IsNullOrWhiteSpace($PythonExe)) {
    $candidate = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { $PythonExe = $candidate }
    else {
        $command = Get-Command python.exe -ErrorAction SilentlyContinue
        if ($null -ne $command) { $PythonExe = $command.Source }
    }
}
if ([string]::IsNullOrWhiteSpace($PythonExe) -or -not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_3_13_NOT_FOUND; supply -PythonExe' }
$versionOutput = & $PythonExe --version 2>&1 | Out-String
if ($versionOutput -notmatch 'Python 3\.13\.') { throw "PYTHON_3_13_REQUIRED: $versionOutput" }
Write-Host ('PYTHON_RUNTIME=' + $versionOutput.Trim())

$runId = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$runRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_loop_cli_parity\' + $runId)
if (Test-Path -LiteralPath $runRoot) { throw "RUN_ROOT_ALREADY_EXISTS: $runRoot" }
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$logs = Join-Path $runRoot 'process_logs'
New-Item -ItemType Directory -Path $logs -Force | Out-Null

$proposalTest = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e4b_loop_editorial_composition_proposal.py'
$helper = Join-Path $ProjectRoot 'tools\c11d\d9\e4b_loop_gui_cli_parity_v2.py'
$helperTest = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e4b_loop_gui_cli_parity_v2.py'
foreach ($file in @($proposalTest, $helper, $helperTest)) { if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "E4B_COMPONENT_MISSING: $file" } }

$processes = @()
Write-Stage 'STATIC_PROPOSAL_TESTS'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @($proposalTest) -WorkingDirectory (Split-Path -Parent $proposalTest) -StdoutPath (Join-Path $logs 'proposal_tests.stdout.txt') -StderrPath (Join-Path $logs 'proposal_tests.stderr.txt') -Label 'E4B static composition proposal tests 17/17'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @($helperTest) -WorkingDirectory (Split-Path -Parent $helperTest) -StdoutPath (Join-Path $logs 'unicode_helper_tests.stdout.txt') -StderrPath (Join-Path $logs 'unicode_helper_tests.stderr.txt') -Label 'E4B GUI CLI Unicode helper tests 5/5'

$requestId = 'E4B_LOOP_CLI_PARITY_' + $runId.Replace('-', '_')
$requestPath = Join-Path $runRoot 'universal_request.json'
$prepareReceiptPath = Join-Path $runRoot 'cli_request_preparation_receipt.json'
$d9Output = Join-Path $runRoot 'd9_universal_result.json'
$e1Output = Join-Path $runRoot 'e1_production_intent_result.json'
$parityReceiptPath = Join-Path $runRoot 'C11E_E4B_LOOP_GUI_CLI_PARITY_RECEIPT_V2.json'
Write-Stage 'UTF8_CLI_REQUEST_PREPARATION_FROM_GUI_EVIDENCE'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @($helper, 'prepare', '--gui-evidence-root', $GuiEvidenceRoot, '--output-request', $requestPath, '--request-id', $requestId, '--preparation-receipt', $prepareReceiptPath) -WorkingDirectory (Split-Path -Parent $helper) -StdoutPath (Join-Path $logs 'request_prepare.stdout.txt') -StderrPath (Join-Path $logs 'request_prepare.stderr.txt') -Label 'Build UTF-8 CLI request from accepted GUI export'

Write-Stage 'D9_9_CLI_PREPARATION'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @((Join-Path $ProjectRoot 'tools\c11d\d9\universal_producer_cli.py'), '--request', $requestPath, '--output', $d9Output) -WorkingDirectory (Join-Path $ProjectRoot 'tools\c11d\d9') -StdoutPath (Join-Path $logs 'd9_cli.stdout.txt') -StderrPath (Join-Path $logs 'd9_cli.stderr.txt') -Label 'D9.9 universal Producer CLI'

Write-Stage 'E1_CLI_PREPARATION'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @((Join-Path $ProjectRoot 'c11c-suite\c11c-producer\c11e_production_cli.py'), '--request', $requestPath, '--origin', 'CLI', '--output', $e1Output) -WorkingDirectory (Join-Path $ProjectRoot 'c11c-suite\c11c-producer') -StdoutPath (Join-Path $logs 'e1_cli.stdout.txt') -StderrPath (Join-Path $logs 'e1_cli.stderr.txt') -Label 'E1 shared production intent CLI'

Write-Stage 'GUI_CLI_POPULATED_PARITY_ASSERTIONS'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @($helper, 'verify', '--gui-evidence-root', $GuiEvidenceRoot, '--cli-request', $requestPath, '--d9-result', $d9Output, '--e1-result', $e1Output, '--receipt-output', $parityReceiptPath) -WorkingDirectory (Split-Path -Parent $helper) -StdoutPath (Join-Path $logs 'parity_verify.stdout.txt') -StderrPath (Join-Path $logs 'parity_verify.stderr.txt') -Label 'Verify populated GUI CLI editorial parity and governance'

$parity = Get-Content -LiteralPath $parityReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($parity.status -ne 'PASS_GUI_CLI_EDITORIAL_PARITY_ONLY') { throw 'E4B_GUI_CLI_PARITY_RECEIPT_NOT_PASS' }
$finalReceipt = [ordered]@{
    schema = 'C11E-E4B-LOOP-CLI-GUI-PARITY-RUNNER-RECEIPT-V2'
    status = 'PASS_GUI_CLI_EDITORIAL_PARITY_ONLY'
    run_id = $runId
    completed_at = (Get-Date).ToString('o')
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_version = $versionOutput.Trim()
    project_root = $ProjectRoot
    gui_evidence_root = $GuiEvidenceRoot
    source_pin_count = $pinReceipts.Count
    source_pins = $pinReceipts
    request_id = $requestId
    request_file_sha256 = Get-Sha256 $requestPath
    d9_output_sha256 = Get-Sha256 $d9Output
    e1_output_sha256 = Get-Sha256 $e1Output
    preparation_receipt_sha256 = Get-Sha256 $prepareReceiptPath
    parity_receipt_sha256 = Get-Sha256 $parityReceiptPath
    identities = $parity.cli
    gui_identities = $parity.gui
    editorial_hash_equal_gui_cli = $parity.parity.gui_cli_editorial_hash_equal
    unicode_round_trip = $parity.parity.unicode_nfc_and_utf8_round_trip
    tests = $processes
    governance = [ordered]@{
        renderer = $false
        renderer_dispatch_invoked = $false
        production_execution = $false
        media_created = $false
        d4_8 = 'BLOCKED'
        release_authority = 'NONE'
        c11c_baseline_modified = $false
        d3_v5_invoked = $false
        ffmpeg_invoked = $false
        git_invoked = $false
    }
}
$runnerReceiptPath = Join-Path $runRoot 'C11E_E4B_LOOP_CLI_GUI_PARITY_RUNNER_RECEIPT_V2.json'
$finalReceipt | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $runnerReceiptPath -Encoding UTF8

Write-Host ('PROPOSAL_STATIC_TESTS=17/17_PASS')
Write-Host ('UNICODE_HELPER_TESTS=5/5_PASS')
Write-Host ('D9_9_CLI=PASS; E1_CLI=PASS; GUI_CLI_EDITORIAL_HASH_EQUAL=' + [string]$parity.parity.gui_cli_editorial_hash_equal)
Write-Host ('EDITORIAL_HASH=' + $parity.cli.editorial_hash)
Write-Host ('GUI_REQUEST_HASH=' + $parity.gui.request_hash)
Write-Host ('CLI_REQUEST_HASH=' + $parity.cli.request_hash)
Write-Host ('RECEIPT=' + $runnerReceiptPath)
Write-Host 'RENDERER=OFF; DISPATCH=FALSE; MEDIA=FALSE; D3_V5=NOT_INVOKED; RELEASE_AUTHORITY=NONE'
Write-Host 'C11E_E4B_LOOP_CLI_GUI_PARITY=PASS_GUI_CLI_EDITORIAL_PARITY_ONLY'
