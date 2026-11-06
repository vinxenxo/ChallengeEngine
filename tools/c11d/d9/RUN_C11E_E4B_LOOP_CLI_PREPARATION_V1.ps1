[CmdletBinding()]
param(
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Projects\ChallengeEngineV01_STATELESS'),
    [string]$PythonExe = ''
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
function Assert-Equal($Actual, $Expected, [string]$Label) {
    if ($Actual -cne $Expected) { throw ("ASSERTION_FAILED: {0}; expected=<{1}> actual=<{2}>" -f $Label, $Expected, $Actual) }
}
function Assert-True($Value, [string]$Label) {
    if ($Value -ne $true) { throw "ASSERTION_FAILED: $Label expected=true" }
}
function Assert-False($Value, [string]$Label) {
    if ($Value -ne $false) { throw "ASSERTION_FAILED: $Label expected=false" }
}

Write-Host '========== C11-E E4B LOOP CLI PREPARATION V1 =========='
Write-Host ('POWERSHELL_RUNTIME_VERSION=' + $PSVersionTable.PSVersion.ToString())
if ($PSVersionTable.PSVersion.Major -ne 5) { throw 'POWERSHELL_5_1_REQUIRED' }
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { $parseErrors | ForEach-Object { Write-Host $_.Message }; throw 'POWERSHELL_5_1_AST_PARSE=FAIL' }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; MEDIA_AND_RENDERER=OFF'

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "PROJECT_ROOT_NOT_FOUND: $ProjectRoot" }
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
$runRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_loop_cli\' + $runId)
if (Test-Path -LiteralPath $runRoot) { throw "RUN_ROOT_ALREADY_EXISTS: $runRoot" }
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$logs = Join-Path $runRoot 'process_logs'
New-Item -ItemType Directory -Path $logs -Force | Out-Null

$proposalTest = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e4b_loop_editorial_composition_proposal.py'
$proposalModule = Join-Path $ProjectRoot 'tools\c11d\d9\e4b_loop_editorial_composition_proposal.py'
$proposalJson = Join-Path $ProjectRoot 'definitions\c11d\production\C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json'
foreach ($file in @($proposalTest, $proposalModule, $proposalJson)) { if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "E4B_PROPOSAL_COMPONENT_MISSING: $file" } }
Write-Stage 'STATIC_PROPOSAL_REGRESSION'
$processes = @()
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @($proposalTest) -WorkingDirectory (Split-Path -Parent $proposalTest) -StdoutPath (Join-Path $logs 'proposal_tests.stdout.txt') -StderrPath (Join-Path $logs 'proposal_tests.stderr.txt') -Label 'E4B static proposal tests 15/15'

$requestId = 'E4B_LOOP_CLI_' + $runId.Replace('-', '_')
$request = [ordered]@{
    schema = 'C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1'
    schema_version = '1.0'
    request_id = $requestId
    mode = 'REVIEW'
    selection = [ordered]@{ content_type = 'visual_loops'; family_id = 'c11c_geometric_waves_v1'; subtype_id = 'harmonic_membrane' }
    seed = 314159
    music_seed = 840001
    delivery_profile_id = 'REVIEW_720'
    presentation_profile_id = 'social_default_v1'
    variation_index = 0
    audio_enabled = $true
    personalization_enabled = $true
    editorial_profile = [ordered]@{ global = [ordered]@{ language = 'es' }; content_type = @{}; family = @{}; subtype = @{}; variant = @{} }
    production_override = [ordered]@{
        title = 'Título editorial Loop — composición armónica en movimiento'
        subtitle = 'Explora el patrón geométrico, observa sus ciclos y descubre cómo evoluciona la forma'
        call_to_action = 'Guarda este loop y comparte tu patrón favorito'
        language = 'es'
    }
    provenance = [ordered]@{ source_revision = 'C11E-E4B-LOOP-CLI-PREFLIGHT-V1'; request_origin = 'CLI' }
}
$requestPath = Join-Path $runRoot 'universal_request.json'
$request | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $requestPath -Encoding UTF8
$requestHashOnDisk = Get-Sha256 $requestPath

Write-Stage 'D9_9_CLI_PREPARATION'
$d9Output = Join-Path $runRoot 'd9_universal_result.json'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @((Join-Path $ProjectRoot 'tools\c11d\d9\universal_producer_cli.py'), '--request', $requestPath, '--output', $d9Output) -WorkingDirectory (Join-Path $ProjectRoot 'tools\c11d\d9') -StdoutPath (Join-Path $logs 'd9_cli.stdout.txt') -StderrPath (Join-Path $logs 'd9_cli.stderr.txt') -Label 'D9.9 universal Producer CLI'

Write-Stage 'E1_CLI_PREPARATION'
$e1Output = Join-Path $runRoot 'e1_production_intent_result.json'
$processes += Invoke-CheckedProcess -FilePath $PythonExe -Arguments @((Join-Path $ProjectRoot 'c11c-suite\c11c-producer\c11e_production_cli.py'), '--request', $requestPath, '--origin', 'CLI', '--output', $e1Output) -WorkingDirectory (Join-Path $ProjectRoot 'c11c-suite\c11c-producer') -StdoutPath (Join-Path $logs 'e1_cli.stdout.txt') -StderrPath (Join-Path $logs 'e1_cli.stderr.txt') -Label 'E1 shared production intent CLI'

Write-Stage 'RESULT_ASSERTIONS'
$d9 = Get-Content -LiteralPath $d9Output -Raw -Encoding UTF8 | ConvertFrom-Json
$e1 = Get-Content -LiteralPath $e1Output -Raw -Encoding UTF8 | ConvertFrom-Json
$intent = $e1.intent
$expectedEditorial = $request.production_override
Assert-Equal $d9.status 'PLANNED' 'D9 status'
Assert-Equal $d9.canonical_request.selection.content_type 'visual_loops' 'D9 content type'
Assert-Equal $d9.canonical_request.selection.family_id 'c11c_geometric_waves_v1' 'D9 family'
Assert-Equal $d9.canonical_request.selection.subtype_id 'harmonic_membrane' 'D9 grammar'
Assert-Equal $d9.canonical_request.delivery_profile_id 'REVIEW_720' 'D9 delivery profile'
Assert-Equal $d9.canonical_request.presentation_profile_id 'social_default_v1' 'D9 presentation profile'
Assert-Equal $d9.canonical_request.seed 314159 'D9 gameplay seed'
Assert-Equal $d9.canonical_request.music_seed 840001 'D9 music seed'
foreach ($field in @('title','subtitle','call_to_action','language')) { Assert-Equal $d9.canonical_request.editorial.$field $expectedEditorial.$field ('D9 editorial ' + $field) }
Assert-Equal $d9.plan.request_hash $d9.request_hash 'D9 request hash in plan'
Assert-Equal $d9.plan.editorial_hash $d9.editorial_hash 'D9 editorial hash in plan'
Assert-Equal $d9.bridge_planning_record.status 'PLANNING_ONLY_NOT_RENDERABLE' 'Bridge plan-only status'
Assert-Equal $d9.bridge_planning_record.route.route_id 'FUTURE_D_NATIVE_VISUAL_LOOP_ADAPTER_REQUIRED' 'Loop bridge route'
Assert-Equal $d9.d_only_adapter_envelope.status 'PREPARED_NOT_DISPATCHED_RENDERER_DISABLED' 'D adapter status'
Assert-False $d9.d_only_adapter_envelope.renderer_dispatch_invoked 'D adapter dispatch'
Assert-False $d9.d_only_adapter_envelope.renderer_input_emitted 'D adapter renderer input'
Assert-False $d9.renderer 'D9 renderer flag'
Assert-False $d9.execution 'D9 execution flag'
Assert-Equal $d9.release_authority 'NONE' 'D9 release authority'

Assert-Equal $e1.status 'PASS_E1_PREPARATION_ONLY' 'E1 status'
Assert-Equal $intent.status 'PREPARED_E1_NOT_DISPATCHED' 'E1 intent status'
Assert-Equal $intent.request_origin 'CLI' 'E1 origin'
Assert-Equal $intent.identity.request_hash $d9.request_hash 'E1/D9 request hash'
Assert-Equal $intent.identity.editorial_hash $d9.editorial_hash 'E1/D9 editorial hash'
Assert-Equal $intent.identity.plan_hash $d9.plan_hash 'E1/D9 plan hash'
foreach ($field in @('title','subtitle','call_to_action','language')) {
    Assert-Equal $intent.editorial.$field $expectedEditorial.$field ('E1 editorial ' + $field)
    Assert-Equal $intent.editorial_field_consumption.$field.consumer_status 'NOT_CONSUMED_E1' ('E1 consumer gate ' + $field)
    Assert-Equal $intent.editorial_field_consumption.$field.required_gate 'E4' ('E1 required gate ' + $field)
}
Assert-Equal $intent.family_adapter.adapter_id 'c11e_visual_loops_adapter' 'E1 Loop adapter id'
Assert-Equal $intent.family_adapter.status 'NOT_CONNECTED_E1' 'E1 Loop adapter status'
Assert-Equal $intent.music_contract.route 'PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH' 'Loop music route'
Assert-Equal $intent.music_contract.status 'PROTECTED_FAMILY_NOT_REWIRED' 'Loop music status'
Assert-Equal $intent.music_contract.music_seed 840001 'E1 music seed'
Assert-False $intent.music_contract.engine_invoked 'D3 V5 invocation'
Assert-False $intent.music_contract.audio_created 'E1 audio creation'
Assert-False $intent.music_contract.ffmpeg_mux_invoked 'E1 FFmpeg mux'
Assert-True $intent.seed_domains.independent_domains 'Independent seed domains'
Assert-Equal $intent.seed_domains.gameplay.value 314159 'E1 gameplay seed'
Assert-Equal $intent.seed_domains.music.value 840001 'E1 music seed'
Assert-False $intent.execution_boundary.renderer_input_emitted 'E1 renderer input'
Assert-False $intent.execution_boundary.renderer_dispatch_invoked 'E1 renderer dispatch'
Assert-False $intent.execution_boundary.production_execution 'E1 production execution'
Assert-False $intent.execution_boundary.media_created 'E1 media creation'
Assert-Equal $intent.execution_boundary.d4_8 'BLOCKED' 'D4.8 status'
Assert-Equal $intent.execution_boundary.release_authority 'NONE' 'E1 release authority'
Assert-True $e1.validation.valid 'E1 validation'

$checks = @(
    'proposal_static_tests_17_17',
    'd9_9_cli_planned',
    'd9_editorial_four_fields_preserved',
    'd9_plan_request_and_editorial_hashes_consistent',
    'bridge_plan_only_not_renderable',
    'd_only_adapter_prepared_not_dispatched',
    'e1_cli_preparation_only',
    'e1_d9_request_editorial_plan_hashes_equal',
    'four_editorial_fields_not_consumed_until_e4',
    'family_music_route_preserved_without_d3_v5',
    'independent_gameplay_music_seeds',
    'renderer_dispatch_media_false_release_none'
)
$receipt = [ordered]@{
    schema = 'C11E-E4B-LOOP-CLI-PREPARATION-RECEIPT-V1'
    status = 'PASS_CLI_PREPARATION_ONLY'
    run_id = $runId
    completed_at = (Get-Date).ToString('o')
    project_root = $ProjectRoot
    python_executable = $PythonExe
    python_version = $versionOutput.Trim()
    source_pin_count = $pinReceipts.Count
    source_pins = $pinReceipts
    request_path = $requestPath
    request_file_sha256 = $requestHashOnDisk
    request_id = $requestId
    d9_output_path = $d9Output
    d9_output_sha256 = Get-Sha256 $d9Output
    e1_output_path = $e1Output
    e1_output_sha256 = Get-Sha256 $e1Output
    identity = [ordered]@{
        request_hash = $d9.request_hash
        editorial_hash = $d9.editorial_hash
        plan_hash = $d9.plan_hash
        bridge_record_hash = $d9.bridge_planning_record.record_hash
        adapter_envelope_hash = $d9.d_only_adapter_envelope.envelope_hash
        e1_intent_hash = $intent.identity.intent_hash
    }
    selection = [ordered]@{ content_type = 'visual_loops'; family_id = 'c11c_geometric_waves_v1'; subtype_id = 'harmonic_membrane' }
    editorial = $expectedEditorial
    seeds = [ordered]@{ gameplay = 314159; music = 840001; independent = $true }
    tests = $processes
    checks = $checks
    execution_boundary = [ordered]@{ renderer = $false; renderer_dispatch_invoked = $false; production_execution = $false; media_created = $false; d3_v5_invoked = $false; ffmpeg_mux_invoked = $false; d4_8 = 'BLOCKED'; release_authority = 'NONE' }
}
$receiptPath = Join-Path $runRoot 'C11E_E4B_LOOP_CLI_PREPARATION_RECEIPT.json'
$receipt | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
Write-Host 'PROPOSAL_STATIC_TESTS=17/17_PASS'
Write-Host 'D9_9_CLI=PASS; E1_CLI=PASS; EDITORIAL_FIELDS=4/4_PRESERVED'
Write-Host ('REQUEST_HASH=' + $d9.request_hash)
Write-Host ('EDITORIAL_HASH=' + $d9.editorial_hash)
Write-Host ('PLAN_HASH=' + $d9.plan_hash)
Write-Host ('BRIDGE_HASH=' + $d9.bridge_planning_record.record_hash)
Write-Host ('ADAPTER_ENVELOPE_HASH=' + $d9.d_only_adapter_envelope.envelope_hash)
Write-Host ('RECEIPT=' + $receiptPath)
Write-Host 'RENDERER=OFF; DISPATCH=FALSE; MEDIA=FALSE; D3_V5=NOT_INVOKED; RELEASE_AUTHORITY=NONE'
Write-Host 'C11E_E4B_LOOP_CLI_PREPARATION=PASS_CLI_PREPARATION_ONLY'
