& {
    $ErrorActionPreference = 'Stop'
    $Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
    Set-Location -LiteralPath $Root
    $AttemptMarker = Join-Path $env:TEMP 'C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_20261027.started.json'
    $CompletedMarker = Join-Path $env:TEMP 'C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_20261027.completed.json'
    if ((Test-Path -LiteralPath $AttemptMarker) -or (Test-Path -LiteralPath $CompletedMarker)) {
        throw "La auditoría de colisión ya se intentó o completó; no se repite: $AttemptMarker | $CompletedMarker"
    }

    $ExpectedManifestSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
    $ExpectedContractSha = 'd68c9e342c6c6937f05737d5299dda0310b6b72157d009eb6706c527232e49c8'
    $ExpectedSchemaSha = '83fa12afb4809d5a1b8c7f1a97c637bd9f81a0f05643bc5daf5c805e1f4ddae4'
    $Manifest = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
    $Contract = Join-Path $Root 'definitions\c11d\production\D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_V1.json'
    $Schema = Join-Path $Root 'definitions\c11d\production\D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_SCHEMA_V1.json'
    $Runner = Join-Path $Root 'tools\c11d\d9\d_renderer_seed_domain_collision_audit.py'
    foreach ($File in @($Manifest, $Contract, $Schema, $Runner)) {
        if (-not (Test-Path -LiteralPath $File -PathType Leaf)) { throw "Falta fichero fijado: $File" }
    }
    if ((Get-Item -LiteralPath $Manifest).Length -ne 796318 -or (Get-FileHash -LiteralPath $Manifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedManifestSha) { throw 'El manifiesto congelado C11-C no coincide.' }
    if ((Get-FileHash -LiteralPath $Contract -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedContractSha) { throw 'Hash del contrato de colisión inesperado.' }
    if ((Get-FileHash -LiteralPath $Schema -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedSchemaSha) { throw 'Hash del schema de colisión inesperado.' }

    $Python = (Get-Command python.exe -ErrorAction Stop).Source
    $LogDir = Join-Path $env:TEMP ('C11D_SEED_DOMAIN_COLLISION_AUDIT_20261027_' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $LogDir | Out-Null
    $Attempt = [ordered]@{ schema = 'C11D-SEED-DOMAIN-COLLISION-REJECTION-AUDIT-ATTEMPT-V1'; started_local = (Get-Date).ToString('o'); repository_root = $Root; log_directory = $LogDir; frozen_c11c_manifest_sha256 = $ExpectedManifestSha }
    Set-Content -LiteralPath $AttemptMarker -Value ($Attempt | ConvertTo-Json -Depth 5) -Encoding UTF8
    $Stdout = Join-Path $LogDir 'seed_domain_collision_stdout.txt'
    $Stderr = Join-Path $LogDir 'seed_domain_collision_stderr.txt'
    $Args = '-B "' + $Runner + '" --root "' + $Root + '" --full-report'
    $Process = Start-Process -FilePath $Python -ArgumentList $Args -WorkingDirectory $Root -Wait -PassThru -NoNewWindow -RedirectStandardOutput $Stdout -RedirectStandardError $Stderr
    if ($Process.ExitCode -ne 0) {
        Write-Host 'C11D_SEED_DOMAIN_COLLISION_AUDIT=FAIL'
        if (Test-Path -LiteralPath $Stderr) { Get-Content -LiteralPath $Stderr }
        throw "La auditoría de colisión falló con ExitCode=$($Process.ExitCode). Evidencia=$LogDir"
    }
    $Lines = @(Get-Content -LiteralPath $Stdout -Encoding UTF8)
    if ($Lines.Count -ne 2 -or -not $Lines[0].StartsWith('C11-D SEED DOMAIN REJECTION AUDIT PASS |')) {
        throw "La auditoría no produjo exactamente un marker PASS y un informe JSON. Evidencia=$LogDir"
    }
    try { $Report = $Lines[1] | ConvertFrom-Json }
    catch { throw "El informe de semillas no es JSON válido: $($_.Exception.Message). Evidencia=$LogDir" }
    if ($Report.schema -ne 'urn:c11d:renderer-seed-domain-collision-audit:v1' -or
        $Report.schema_version -ne '1.0' -or
        $Report.status -ne 'PREPARATION_ONLY_EXPLICIT_SEED_AND_NUMERIC_COLLISION_AUDIT_NOT_INPUT_ADMISSION' -or
        $Report.selectors -ne 2 -or
        $Report.explicit_seed_negative_cases.passed -ne 20 -or
        $Report.explicit_seed_negative_cases.total -ne 20 -or
        $Report.numeric_seed_collision_rejections.passed -ne 4 -or
        $Report.numeric_seed_collision_rejections.total -ne 4 -or
        $Report.collision_values_tested.Count -ne 2 -or
        $Report.collision_values_tested[0] -ne 12345 -or
        $Report.collision_values_tested[1] -ne 840001 -or
        $Report.all_rejections_precede_godot -ne $true -or
        $Report.source_pin_count -ne 23 -or
        $Report.runtime_invocations -ne 0 -or
        $Report.runtime_seed_derivation_enabled -ne $false -or
        $Report.automatic_seed_generation -ne $false -or
        $Report.master_seed_adopted -ne $false -or
        $Report.seed_domains_complete_for_candidate_input -ne $false -or
        $Report.frozen_c11c_manifest_sha256 -ne $ExpectedManifestSha -or
        $Report.execution_boundary.renderer_activation -ne $false -or
        $Report.execution_boundary.renderer_dispatch_invoked -ne $false -or
        $Report.execution_boundary.media_created -ne $false -or
        $Report.execution_boundary.d4_8 -ne 'BLOCKED' -or
        $Report.execution_boundary.release_authority -ne 'NONE' -or
        $Report.audit_sha256 -notmatch '^[0-9a-f]{64}$') {
        throw "Los valores del informe no satisfacen el contrato fail-closed. Evidencia=$LogDir"
    }
    if ((Get-Item -LiteralPath $Stderr).Length -ne 0) { throw "stderr de auditoría no está vacío. Evidencia=$LogDir" }

    $JsonPath = Join-Path $LogDir 'seed_domain_collision_report.json'
    Set-Content -LiteralPath $JsonPath -Value $Lines[1] -Encoding UTF8
    $OutSha = (Get-FileHash -LiteralPath $Stdout -Algorithm SHA256).Hash.ToLowerInvariant()
    $ErrSha = (Get-FileHash -LiteralPath $Stderr -Algorithm SHA256).Hash.ToLowerInvariant()
    $JsonSha = (Get-FileHash -LiteralPath $JsonPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $MarkerObject = [ordered]@{
        schema = 'C11D-SEED-DOMAIN-COLLISION-REJECTION-AUDIT-EVIDENCE-V1'
        completed_local = (Get-Date).ToString('o')
        repository_root = $Root
        frozen_c11c_manifest_sha256 = $ExpectedManifestSha
        audit_exit_code = $Process.ExitCode
        selectors = 2
        explicit_seed_negative_cases = '20/20'
        numeric_seed_collision_rejections = '4/4'
        collision_values = @(12345,840001)
        all_rejections_precede_godot = $true
        source_pins = '23/23'
        runtime_invocations = 0
        audit_sha256 = $Report.audit_sha256
        report_file_sha256 = $JsonSha
        stdout_sha256 = $OutSha
        stderr_sha256 = $ErrSha
        log_directory = $LogDir
        renderer = 'OFF'
        media_created = $false
        candidate_input_admissible = $false
        d4_8 = 'BLOCKED'
        release_authority = 'NONE'
    }
    Set-Content -LiteralPath $CompletedMarker -Value ($MarkerObject | ConvertTo-Json -Depth 10) -Encoding UTF8

    Write-Host 'C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT=PASS'
    Write-Host 'AUDIT_EXIT_CODE=0'
    Write-Host 'SELECTORS=2'
    Write-Host 'EXPLICIT_SEED_NEGATIVE_CASES=20/20'
    Write-Host 'NUMERIC_SEED_COLLISION_REJECTIONS=4/4'
    Write-Host 'COLLISION_VALUES=12345,840001'
    Write-Host 'ALL_REJECTIONS_PRECEDE_GODOT=true'
    Write-Host 'SOURCE_PINS=23/23'
    Write-Host 'RUNTIME_INVOCATIONS=0'
    Write-Host ("AUDIT_SHA256=" + $Report.audit_sha256)
    Write-Host ("REPORT_FILE_SHA256=" + $JsonSha)
    Write-Host ("STDOUT_SHA256=" + $OutSha)
    Write-Host ("STDERR_SHA256=" + $ErrSha)
    Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
    Write-Host 'RENDERER=OFF'
    Write-Host 'MEDIA_CREATED=false'
    Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
    Write-Host 'D4.8=BLOCKED'
    Write-Host 'RELEASE_AUTHORITY=NONE'
    Write-Host ("LOG_DIRECTORY=" + $LogDir)
    Write-Host ("REPORT_FILE=" + $JsonPath)
    Write-Host ("ATTEMPT_MARKER=" + $AttemptMarker)
    Write-Host ("COMPLETION_MARKER=" + $CompletedMarker)
}
