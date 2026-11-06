# C11-E E4B LOOP POLICY READINESS V1
[CmdletBinding()]
param(
    [string]$GuiEvidenceRoot = "artifacts\tests\c11e\e4b_loop_family_matrix\E4B_LOOP_GUI_20261106T211920Z_F9377504",
    [string]$CliEvidenceRoot = "artifacts\tests\c11e\e4b_loop_family_matrix\CLI_20261106T212054Z-DE8364C4"
)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
Write-Host '========== C11-E E4B LOOP POLICY READINESS V1 =========='
$Tokens = $null
$ParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$Tokens, [ref]$ParseErrors) | Out-Null
if ($ParseErrors.Count -gt 0) { throw 'POWERSHELL_5_1_AST_PARSE=FAIL' }
Write-Host ('POWERSHELL_RUNTIME_VERSION=' + $PSVersionTable.PSVersion.ToString())
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
Write-Host 'RUNNER_SOURCE_ENCODING=ASCII_SAFE'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; READ_ONLY_AUDIT=TRUE'
$ProjectRoot = (Get-Location).Path
$ManifestPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) { throw 'Run from the active checkout root; frozen manifest missing.' }
$ExpectedManifestSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedManifestBytes = 796318
$ManifestItem = Get-Item -LiteralPath $ManifestPath
$ManifestSha = (Get-FileHash -LiteralPath $ManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ManifestItem.Length -ne $ExpectedManifestBytes -or $ManifestSha -ne $ExpectedManifestSha) { throw 'FROZEN_C11C_MANIFEST=FAIL' }
Write-Host 'FROZEN_C11C_MANIFEST=PASS'
$SourcePins = ConvertFrom-Json -InputObject @'
[{"path":"c11c-suite/c11c-producer/main.py","sha256":"982bce475811c5e4f9cad2e84b33cee9a3460f6add4f095476e950db15b806ab"},{"path":"c11c-suite/c11c-producer/c11e_production_service.py","sha256":"348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951"},{"path":"c11c-suite/c11c-producer/c11e_production_cli.py","sha256":"e7272231dca2eb730506308b092fce9b3644f7f8cfd9f2c2bbbbd1b695e82fc4"},{"path":"tools/c11d/d9/universal_producer.py","sha256":"9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1"},{"path":"tools/c11d/d9/universal_producer_cli.py","sha256":"c648a3722299b4700a9b74d1cabc6cac1fa48ad6275497ae8073bc07f442bb54"},{"path":"tools/c11d/d9/universal_editorial_model.py","sha256":"5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5"},{"path":"tools/c11d/d9/editorial_render_bridge.py","sha256":"fe9d40052b0f4ff6f1c862c010ae7b3b13070b6ce935be6d62f9dcaec63a644a"},{"path":"tools/c11d/d9/d_render_adapter.py","sha256":"222742677cd498368429a3ec0dcdd922c44197bb5ada3638081138fb77c31bf1"},{"path":"c11c-suite/c11c-producer/producer_schema.json","sha256":"564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0"},{"path":"definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json","sha256":"50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53"},{"path":"definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json","sha256":"342a61338c80a2f1616e8e9f38986bd90f410257c0e321f99840380fb0fd804b"},{"path":"profiles/delivery/c11c_video_delivery_profiles.json","sha256":"967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"},{"path":"release/C11C_FREEZE_PACKAGE_MANIFEST.json","sha256":"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"},{"path":"assets/fonts/Inter-Bold.otf","sha256":"9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d"},{"path":"assets/fonts/NotoSansMono-Regular.ttf","sha256":"6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f"},{"path":"core/presentation/C11CVisualEditorialLayer.gd","sha256":"f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d"},{"path":"core/presentation/UnifiedSocialFrame.gd","sha256":"d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba"},{"path":"tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd","sha256":"44c4a9a11c334e6e84fcc1413667accac175781787866c3d6b894beeba3ea255"},{"path":"core/presentation/C11CVisualTypography.gd","sha256":"9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633"},{"path":"tools/prototypes/c11c_common/C11CSafeAmbient.py","sha256":"c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c"},{"path":"tools/prototypes/c11c_common/generate_c11c_family_music.py","sha256":"41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d"},{"path":"profiles/presentation/c11c_visual_music_profiles.json","sha256":"b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58"},{"path":"tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd","sha256":"ab2560cbe7fa42c5cad3b143aa59d1f2a0dc047682f7667983c7c0a0f6dbb61c"},{"path":"tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd","sha256":"b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55"},{"path":"tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd","sha256":"12fdbc13e05df28b26cf95fe1907d150bd41f29196287700153521e9baee336b"},{"path":"tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd","sha256":"835ba0df2c160a259be39bd1977bfac0e6a66f903ce1aa6b4247af7c508ad94a"},{"path":"tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd","sha256":"a68661a5fdf792aa7fe701afa6fbf1631a2b8215c214032f58ecfe0c69d8374a"},{"path":"definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json","sha256":"9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da"},{"path":"tools/c11d/d9/e4b_loop_editorial_composition_proposal.py","sha256":"3956282bfc29bbe919cf70ae6b76046095f24325d7de2391c38a3765fcf2b93d"},{"path":"tools/c11d/d9/test_c11e_e4b_loop_editorial_composition_proposal.py","sha256":"3dd877a473bd15a593238f32799dbd566bae887021aaa09a90873e158d8847f9"},{"path":"tools/c11d/d9/e4b_loop_gui_cli_parity_v2.py","sha256":"d1a98f9962ae912531ae5920c071cb98a60cdcc91e3a1b420d1178b49ef89b73"},{"path":"tools/c11d/d9/test_c11e_e4b_loop_gui_cli_parity_v2.py","sha256":"3f32fcbd52034f4f8b774954860a9da24231f9b84ca42acea62fd76498cadcda"},{"path":"tools/c11d/d9/c11e_e4b_loop_family_matrix.py","sha256":"bd83489b8154d692d7b226d0edd84ed3fe2375db62ebc4385adf01223324fa35"},{"path":"tools/c11d/d9/test_c11e_e4b_loop_family_matrix.py","sha256":"37eb3c94fccff9a368d9f441cd8aed427e8af3dfc25c88c8bd5766783343f349"},{"path":"definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json","sha256":"101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a"},{"path":"definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json","sha256":"609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"},{"path":"definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json","sha256":"41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85"},{"path":"definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json","sha256":"3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23"},{"path":"docs/current/d/D_RENDERER_POLICY_APPROVAL_DECISION_PACKET_V1.md","sha256":"5c5e1979f5b395e1a95437fd579bc24fc21409ae3682768571e36b300acbc3dc"},{"path":"docs/current/d/C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_RUNTIME_ACCEPTANCE_CHECKPOINT_20261017.md","sha256":"272e0c5637c003e2acc925b3c548f04131978a0c9b6549ee39015acae2358df2"},{"path":"docs/current/d/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REQUEST_BOUND_REFERENCE_CARRIER_CHECKPOINT_20261016.md","sha256":"89535b0a98e0eb26642e17bc94faa78abcdf766739b665b5e6883c8b40b689d6"},{"path":"docs/current/d/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_UNIFIED_REVIEW_INTEGRATION_CHECKPOINT.md","sha256":"51c545fc31ce97753eef28088d67fa3bd52a455abda246ac13cd1523b490da1c"},{"path":"docs/current/d/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_CHECKPOINT_V1.md","sha256":"db2ed4a6565315e1446bec153b34bbe2fc6fc28e8083ecbee22e0dc5856312c3"},{"path":"docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md","sha256":"e2ca811e2ea454f519208845d4ae4a945b72cad569050474e9ba42e7cc357646"}]
'@
$PinCount = 0
foreach ($Pin in $SourcePins) {
    $Path = Join-Path $ProjectRoot $Pin.path.Replace('/', '\')
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw ('SOURCE_PIN_MISSING=' + $Pin.path) }
    $Actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Actual -ne $Pin.sha256) { throw ('SOURCE_PIN_MISMATCH=' + $Pin.path) }
    $PinCount++
}
$HelperPath = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e4b_loop_policy_readiness.py'
$TestPath = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e4b_loop_policy_readiness.py'
if ((Get-FileHash -LiteralPath $HelperPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b9ed539c371b961d61e3065699ce666efe18f59b380a156eeae6bc47f52e2124') { throw 'POLICY_READINESS_HELPER_PIN=FAIL' }
if ((Get-FileHash -LiteralPath $TestPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '98ea4c5c225be42ffa4f93b305bce81cb4439ccbc6e73b42da31540482f4a04c') { throw 'POLICY_READINESS_TEST_PIN=FAIL' }
Write-Host ('SOURCE_PINS=PASS; COUNT=' + $PinCount + '; LOCAL_TOOL_PINS=2/2')
$GuiPath = if ([System.IO.Path]::IsPathRooted($GuiEvidenceRoot)) { $GuiEvidenceRoot } else { Join-Path $ProjectRoot $GuiEvidenceRoot }
$CliPath = if ([System.IO.Path]::IsPathRooted($CliEvidenceRoot)) { $CliEvidenceRoot } else { Join-Path $ProjectRoot $CliEvidenceRoot }
foreach ($EvidencePath in @($GuiPath, $CliPath)) { if (-not (Test-Path -LiteralPath $EvidencePath -PathType Container)) { throw ('EVIDENCE_ROOT_MISSING=' + $EvidencePath) } }
$Python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    $PythonCommand = Get-Command 'py.exe' -ErrorAction SilentlyContinue
    if (-not $PythonCommand) { throw 'PYTHON_3_13_NOT_FOUND' }
    $PythonPathOutput = & $PythonCommand.Source -3.13 -c 'import sys; print(sys.executable)' 2>&1
    if ($LASTEXITCODE -ne 0) { throw ('PYTHON_3_13_RESOLUTION_FAILED=' + ($PythonPathOutput -join ' ')) }
    $Python = ($PythonPathOutput | Select-Object -Last 1).ToString().Trim()
    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw 'PYTHON_3_13_EXECUTABLE_MISSING' }
}
$VersionOutput = & $Python -c 'import sys; print(sys.version_info[0], sys.version_info[1], sys.version_info[2])' 2>&1
if ($LASTEXITCODE -ne 0 -or ($VersionOutput -join '').Trim() -notmatch '^3 13 ') { throw ('PYTHON_RUNTIME_UNSUPPORTED=' + ($VersionOutput -join ' ')) }
Write-Host ('PYTHON_RUNTIME=' + ($VersionOutput -join '').Trim())
$RunId = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '-' + ([Guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$OutputRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_loop_policy_readiness\' + $RunId)
$LogRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_loop_policy_readiness_runner_logs\' + $RunId)
[System.IO.Directory]::CreateDirectory($LogRoot) | Out-Null
$OldProject = $env:C11E_PROJECT_ROOT
$OldGui = $env:C11E_GUI_EVIDENCE_ROOT
$OldCli = $env:C11E_CLI_EVIDENCE_ROOT
$env:C11E_PROJECT_ROOT = $ProjectRoot
$env:C11E_GUI_EVIDENCE_ROOT = $GuiPath
$env:C11E_CLI_EVIDENCE_ROOT = $CliPath
try {
    Write-Host 'STAGE=FOCUSED_READ_ONLY_TESTS'
    $TestStdout = Join-Path $LogRoot 'policy_readiness_tests.stdout.txt'
    $TestStderr = Join-Path $LogRoot 'policy_readiness_tests.stderr.txt'
    $TestStart = Start-Process -FilePath $Python -ArgumentList ('-m unittest discover -s "' + (Split-Path -Parent $HelperPath) + '" -p "test_c11e_e4b_loop_policy_readiness.py" -v') -WorkingDirectory $ProjectRoot -RedirectStandardOutput $TestStdout -RedirectStandardError $TestStderr -Wait -PassThru
    if ($TestStart.ExitCode -ne 0) { throw ('POLICY_READINESS_TESTS=FAIL; EXIT=' + $TestStart.ExitCode) }
    Write-Host 'POLICY_READINESS_TESTS=11/11_PASS'
    Write-Host 'STAGE=POLICY_AND_MATRIX_READ_ONLY_AUDIT'
    $AuditStdout = Join-Path $LogRoot 'policy_readiness_audit.stdout.txt'
    $AuditStderr = Join-Path $LogRoot 'policy_readiness_audit.stderr.txt'
    $ArgumentLine = '"' + $HelperPath + '" --project-root "' + $ProjectRoot + '" --gui-evidence-root "' + $GuiPath + '" --cli-evidence-root "' + $CliPath + '" --output-root "' + $OutputRoot + '"'
    $AuditStart = Start-Process -FilePath $Python -ArgumentList $ArgumentLine -WorkingDirectory $ProjectRoot -RedirectStandardOutput $AuditStdout -RedirectStandardError $AuditStderr -Wait -PassThru
    if ($AuditStart.ExitCode -ne 0) { throw ('POLICY_READINESS_AUDIT=FAIL; EXIT=' + $AuditStart.ExitCode) }
    $ReportPath = Join-Path $OutputRoot 'C11E_E4B_LOOP_POLICY_READINESS_REPORT_V1.json'
    $Report = Get-Content -LiteralPath $ReportPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($Report.status -ne 'PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED' -or $Report.stale_packet_v1_hash_count -ne 3) { throw 'POLICY_READINESS_REPORT_ASSERTION=FAIL' }
    $Receipt = [ordered]@{
        schema = 'C11E-E4B-LOOP-POLICY-READINESS-RUNNER-RECEIPT-V1'
        status = $Report.status
        run_id = $RunId
        completed_at = (Get-Date).ToUniversalTime().ToString('o')
        powershell_version = $PSVersionTable.PSVersion.ToString()
        python_version = ($VersionOutput -join '').Trim()
        project_root = $ProjectRoot
        gui_evidence_root = $GuiPath
        cli_evidence_root = $CliPath
        source_pin_count = $PinCount
        local_tool_pins = @{ helper = 'b9ed539c371b961d61e3065699ce666efe18f59b380a156eeae6bc47f52e2124'; tests = '98ea4c5c225be42ffa4f93b305bce81cb4439ccbc6e73b42da31540482f4a04c' }
        focused_tests = @{ count = '11/11'; exit_code = $TestStart.ExitCode; stdout_sha256 = (Get-FileHash -LiteralPath $TestStdout -Algorithm SHA256).Hash.ToLowerInvariant(); stderr_sha256 = (Get-FileHash -LiteralPath $TestStderr -Algorithm SHA256).Hash.ToLowerInvariant() }
        audit = @{ exit_code = $AuditStart.ExitCode; report_sha256 = (Get-FileHash -LiteralPath $ReportPath -Algorithm SHA256).Hash.ToLowerInvariant(); stdout_sha256 = (Get-FileHash -LiteralPath $AuditStdout -Algorithm SHA256).Hash.ToLowerInvariant(); stderr_sha256 = (Get-FileHash -LiteralPath $AuditStderr -Algorithm SHA256).Hash.ToLowerInvariant(); direct_identity_fields = 9; cases = 81; stale_packet_v1_hash_count = 3; stale_labels = @('loop_drill_windows','delivery_timebase','audio_music_delivery') }
        governance = @{ renderer = $false; renderer_input_emitted = $false; renderer_dispatch_invoked = $false; production_execution = $false; media_created = $false; c11c_baseline_modified = $false; git_invoked = $false; godot_invoked = $false; c11c_visual_generator_invoked = $false; c11c_family_music_generator_invoked = $false; d3_v5_invoked = $false; ffmpeg_invoked = $false; d4_8 = 'BLOCKED'; d9_10 = 'PREPARE_ONLY'; d9_14 = 'BLOCKED'; d9_16 = 'BLOCKED'; d9_17 = 'BLOCKED_NO_GO'; d10 = 'BLOCKED_FOR_PROMOTION'; release_authority = 'NONE' }
    }
    $ReceiptJson = $Receipt | ConvertTo-Json -Depth 20
    $ReceiptPath = Join-Path $OutputRoot 'C11E_E4B_LOOP_POLICY_READINESS_RUNNER_RECEIPT_V1.json'
    [System.IO.File]::WriteAllText($ReceiptPath, $ReceiptJson, (New-Object System.Text.UTF8Encoding($false)))
    $ReceiptSha = (Get-FileHash -LiteralPath $ReceiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
    [System.IO.File]::WriteAllText((Join-Path $OutputRoot 'C11E_E4B_LOOP_POLICY_READINESS_RUNNER_RECEIPT_V1.sha256'), ($ReceiptSha + '  C11E_E4B_LOOP_POLICY_READINESS_RUNNER_RECEIPT_V1.json' + "`n"), [System.Text.Encoding]::ASCII)
    Write-Host ('REPORT_SHA256=' + $Receipt.audit.report_sha256)
    Write-Host ('STALE_APPROVAL_PACKET_V1_HASHES=3; LABELS=loop_drill_windows,delivery_timebase,audio_music_delivery')
    Write-Host ('RECEIPT=' + $ReceiptPath)
    Write-Host 'RENDERER=OFF; MEDIA=FALSE; RELEASE_AUTHORITY=NONE'
    Write-Host 'C11E_E4B_LOOP_POLICY_READINESS=PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED'
} finally {
    $env:C11E_PROJECT_ROOT = $OldProject
    $env:C11E_GUI_EVIDENCE_ROOT = $OldGui
    $env:C11E_CLI_EVIDENCE_ROOT = $OldCli
}
