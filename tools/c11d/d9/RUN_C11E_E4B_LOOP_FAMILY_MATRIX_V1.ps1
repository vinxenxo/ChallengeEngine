[CmdletBinding()]
param(
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Projects\ChallengeEngineV01_STATELESS'),
    [string]$PythonExe = '',
    [Parameter(Mandatory = $true)][string]$GuiEvidenceRoot
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
    return [pscustomobject]@{ path = $RelativePath; sha256 = $actual }
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
    $process = Start-Process -FilePath $FilePath -ArgumentList ($quoted -join ' ') -WorkingDirectory $WorkingDirectory -Wait -PassThru -NoNewWindow -RedirectStandardOutput $StdoutPath -RedirectStandardError $StderrPath
    $stdoutHash = Get-Sha256 $StdoutPath
    $stderrHash = Get-Sha256 $StderrPath
    if ($process.ExitCode -ne 0) {
        throw ("PROCESS_FAILED: {0}; exit={1}; stdout_sha256={2}; stderr_sha256={3}" -f $Label, $process.ExitCode, $stdoutHash, $stderrHash)
    }
    return [pscustomobject]@{
        name = $Label
        executable = $FilePath
        arguments = $Arguments
        exit_code = [int]$process.ExitCode
        stdout_sha256 = $stdoutHash
        stderr_sha256 = $stderrHash
    }
}

Write-Host '========== C11-E E4B LOOP FAMILY MATRIX V1 =========='
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
    if ($scriptBytes[$byteIndex] -gt 127) { throw 'RUNNER_SOURCE_ENCODING_INVALID: ASCII_ONLY_REQUIRED' }
}
Write-Host 'RUNNER_SOURCE_ENCODING=ASCII_SAFE'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; RENDERER_AND_MEDIA=OFF'

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
$GuiEvidenceRoot = [System.IO.Path]::GetFullPath($GuiEvidenceRoot)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "PROJECT_ROOT_NOT_FOUND: $ProjectRoot" }
if (-not (Test-Path -LiteralPath $GuiEvidenceRoot -PathType Container)) { throw "GUI_EVIDENCE_ROOT_NOT_FOUND: $GuiEvidenceRoot" }
foreach ($required in @('matrix_request_template.json', 'matrix_request_template.sha256', 'matrix_report.json', 'matrix_report.sha256')) {
    if (-not (Test-Path -LiteralPath (Join-Path $GuiEvidenceRoot $required) -PathType Leaf)) { throw "GUI_MATRIX_EVIDENCE_MISSING: $required" }
}

$expectedPins = [ordered]@{
    'c11c-suite/c11c-producer/main.py' = '982bce475811c5e4f9cad2e84b33cee9a3460f6add4f095476e950db15b806ab'
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
    'tools/c11d/d9/c11e_e4b_loop_family_matrix.py' = 'bd83489b8154d692d7b226d0edd84ed3fe2375db62ebc4385adf01223324fa35'
    'tools/c11d/d9/test_c11e_e4b_loop_family_matrix.py' = '37eb3c94fccff9a368d9f441cd8aed427e8af3dfc25c88c8bd5766783343f349'
}

Write-Stage 'SOURCE_PIN_VERIFICATION'
$pinReceipts = @()
foreach ($entry in $expectedPins.GetEnumerator()) {
    $actual = Assert-Sha256 $entry.Key $entry.Value
    $pinReceipts += $actual
}
$manifestPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$manifestBytes = [System.IO.File]::ReadAllBytes($manifestPath)
$manifestSha = Get-Sha256 $manifestPath
if ($manifestSha -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') { throw 'FROZEN_C11C_MANIFEST_MISMATCH' }
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
$evidenceBase = Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_loop_family_matrix'
$runRoot = Join-Path $evidenceBase ('CLI_' + $runId)
$logsRoot = Join-Path (Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_loop_family_matrix_runner_logs') $runId
if (Test-Path -LiteralPath $runRoot) { throw "RUN_ROOT_ALREADY_EXISTS: $runRoot" }
if (Test-Path -LiteralPath $logsRoot) { throw "LOG_ROOT_ALREADY_EXISTS: $logsRoot" }
New-Item -ItemType Directory -Path $logsRoot -Force | Out-Null

$testPath = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e4b_loop_family_matrix.py'
$proposalTestPath = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e4b_loop_editorial_composition_proposal.py'
$helperPath = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e4b_loop_family_matrix.py'
foreach ($path in @($testPath, $proposalTestPath, $helperPath)) { if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "E4B_MATRIX_COMPONENT_MISSING: $path" } }

$processes = @()
Write-Stage 'STATIC_REGRESSION'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @('-B', $proposalTestPath) -WorkingDirectory (Split-Path -Parent $proposalTestPath) -StdoutPath (Join-Path $logsRoot 'composition_proposal_tests.stdout.txt') -StderrPath (Join-Path $logsRoot 'composition_proposal_tests.stderr.txt') -Label 'E4B composition proposal tests 17/17'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @('-B', $testPath) -WorkingDirectory (Split-Path -Parent $testPath) -StdoutPath (Join-Path $logsRoot 'loop_family_matrix_tests.stdout.txt') -StderrPath (Join-Path $logsRoot 'loop_family_matrix_tests.stderr.txt') -Label 'E4B full-family matrix tests 13/13'

Write-Stage 'D9_9_D9_10_E1_ALL_FAMILY_MATRIX'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @(
    '-B',
    $helperPath,
    '--project-root', $ProjectRoot,
    '--origin', 'CLI',
    '--gui-evidence-root', $GuiEvidenceRoot,
    '--output-root', $runRoot
) -WorkingDirectory (Split-Path -Parent $helperPath) -StdoutPath (Join-Path $logsRoot 'loop_family_matrix.stdout.txt') -StderrPath (Join-Path $logsRoot 'loop_family_matrix.stderr.txt') -Label '27 Loop grammars x 3 seed scenarios via D9.9/D9.10/E1'

$reportPath = Join-Path $runRoot 'matrix_report.json'
$report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($report.status -ne 'PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY') { throw 'LOOP_FAMILY_MATRIX_NOT_PASS' }
if ([int]$report.scope.family_count -ne 5 -or [int]$report.scope.grammar_count -ne 27 -or [int]$report.scope.case_count -ne 81) { throw 'LOOP_FAMILY_MATRIX_SCOPE_MISMATCH' }
if ($report.gui_cli_parity.status -ne 'PASS_GUI_CLI_ALL_27_SELECTOR_PARITY_ONLY' -or [int]$report.gui_cli_parity.case_count -ne 81) { throw 'LOOP_FAMILY_GUI_CLI_PARITY_NOT_PASS' }
if ($report.governance.renderer -ne $false -or $report.governance.renderer_input_emitted -ne $false -or $report.governance.renderer_dispatch_invoked -ne $false -or $report.governance.production_execution -ne $false -or $report.governance.media_created -ne $false -or $report.governance.c11c_baseline_modified -ne $false -or $report.governance.godot_invoked -ne $false -or $report.governance.c11c_family_visual_generators_invoked -ne $false -or $report.governance.c11c_family_music_generator_invoked -ne $false -or $report.governance.d3_v5_invoked -ne $false -or $report.governance.ffmpeg_invoked -ne $false -or $report.governance.d4_8 -ne 'BLOCKED' -or $report.governance.d9_10 -ne 'PREPARE_ONLY' -or $report.governance.d9_14 -ne 'BLOCKED' -or $report.governance.d9_16 -ne 'BLOCKED' -or $report.governance.d9_17 -ne 'BLOCKED_NO_GO' -or $report.governance.d10 -ne 'BLOCKED_FOR_PROMOTION' -or $report.governance.release_authority -ne 'NONE') { throw 'LOOP_FAMILY_GOVERNANCE_MISMATCH' }
$sidecarHash = (Get-Content -LiteralPath (Join-Path $runRoot 'matrix_report.sha256') -Raw -Encoding ASCII).Trim().Split(' ')[0]
if ((Get-Sha256 $reportPath) -ne $sidecarHash) { throw 'MATRIX_REPORT_SIDECAR_HASH_MISMATCH' }
$templatePath = Join-Path $runRoot 'matrix_request_template.json'
$templateSidecarHash = (Get-Content -LiteralPath (Join-Path $runRoot 'matrix_request_template.sha256') -Raw -Encoding ASCII).Trim().Split(' ')[0]
if ((Get-Sha256 $templatePath) -ne $templateSidecarHash) { throw 'MATRIX_TEMPLATE_SIDECAR_HASH_MISMATCH' }

$runnerReceipt = [ordered]@{
    schema = 'C11E-E4B-LOOP-FAMILY-MATRIX-RUNNER-RECEIPT-V1'
    status = 'PASS_GUI_CLI_ALL_27_SELECTOR_PARITY_ONLY'
    run_id = $runId
    completed_at = (Get-Date).ToString('o')
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_version = $versionOutput.Trim()
    project_root = $ProjectRoot
    gui_evidence_root = $GuiEvidenceRoot
    source_pin_count = $pinReceipts.Count
    source_pins = $pinReceipts
    family_count = [int]$report.scope.family_count
    grammar_count = [int]$report.scope.grammar_count
    case_count = [int]$report.scope.case_count
    seed_relations = [int]$report.seed_domain_relations.Count
    gui_cli_parity = $report.gui_cli_parity.status
    gui_cli_parity_case_count = [int]$report.gui_cli_parity.case_count
    matrix_request_template_sha256 = $templateSidecarHash
    matrix_report_sha256 = $sidecarHash
    process_logs_root = $logsRoot
    tests = $processes
    governance = [ordered]@{
        renderer = $false
        renderer_input_emitted = $false
        renderer_dispatch_invoked = $false
        production_execution = $false
        media_created = $false
        c11c_baseline_modified = $false
        godot_invoked = $false
        c11c_family_visual_generators_invoked = $false
        c11c_family_music_generator_invoked = $false
        d3_v5_invoked = $false
        ffmpeg_invoked = $false
        git_invoked = $false
        d4_8 = 'BLOCKED'
        d9_10 = 'PREPARE_ONLY'
        release_authority = 'NONE'
    }
}
$receiptPath = Join-Path $runRoot 'C11E_E4B_LOOP_FAMILY_MATRIX_RUNNER_RECEIPT_V1.json'
$runnerReceipt | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath $receiptPath -Encoding UTF8

Write-Host ('PROPOSAL_TESTS=17/17_PASS; FAMILY_MATRIX_TESTS=13/13_PASS')
Write-Host ('FAMILIES=' + $report.scope.family_count + '; GRAMMARS=' + $report.scope.grammar_count + '; CASES=' + $report.scope.case_count)
Write-Host ('SEED_RELATIONS=' + $report.seed_domain_relations.Count + '; GUI_CLI_PARITY=' + $report.gui_cli_parity.status)
Write-Host ('MATRIX_TEMPLATE_SHA256=' + $templateSidecarHash)
Write-Host ('MATRIX_REPORT_SHA256=' + $sidecarHash)
Write-Host ('MATRIX_REPORT=' + $reportPath)
Write-Host ('RUNNER_RECEIPT=' + $receiptPath)
Write-Host 'RENDERER=OFF; DISPATCH=FALSE; MEDIA=FALSE; GODOT=NOT_INVOKED; D3_V5=NOT_INVOKED; FFMPEG=NOT_INVOKED; RELEASE_AUTHORITY=NONE'
Write-Host 'C11E_E4B_LOOP_FAMILY_MATRIX=PASS_GUI_CLI_ALL_27_SELECTOR_PARITY_ONLY'
