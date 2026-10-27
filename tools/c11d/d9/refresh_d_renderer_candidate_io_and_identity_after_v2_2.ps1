& {
    $ErrorActionPreference = 'Stop'
    $Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
    Set-Location -LiteralPath $Root

    $CompletedMarker = Join-Path $env:TEMP 'C11D_V2_2_POST_RUNTIME_GAP_IDENTITY_REFRESH_20261027.completed.json'
    if (Test-Path -LiteralPath $CompletedMarker) {
        throw "Este refresco ya se completó en esta sesión de trabajo; no se repite: $CompletedMarker"
    }

    $Pins = @(
        @{ Path = 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'; Hash = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953' },
        @{ Path = 'tools\c11d\d9\d_renderer_request_scoped_payload_materialization_binding_v2.py'; Hash = '709d5ff670561d2bfc8b5926ba616b6773589bb783dc10f767354b26c3c62cbd' },
        @{ Path = 'tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding_v2.py'; Hash = '120b99b58e4ba09ff74c01a5f1acf57252353d61a659aaa440723436f5900da6' },
        @{ Path = 'definitions\c11d\production\D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V2.json'; Hash = '0c3f03cbfa3990e093ccbc3e74f777f8f537682570e75cc304b393c2a6eb1100' },
        @{ Path = 'definitions\c11d\production\D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V2.json'; Hash = 'e1b586f4ec4abc31ca92e2ebdbdbaa293c17efb9493b0385f1af79e652dfc83f' },
        @{ Path = 'tools\c11d\d9\d_renderer_candidate_io_gap_audit.py'; Hash = 'e056d45c02c00a9667b83335f40406064a6a994500ef8a51881db77e815d5ba1' },
        @{ Path = 'tools\c11d\d9\d_renderer_candidate_identity_inventory.py'; Hash = 'a0136498670045bede6f8bf68a337f5699d14d45c3d6088f64d4e09a6bae26ef' },
        @{ Path = 'definitions\c11d\production\D_RENDERER_CANDIDATE_IO_GAP_AUDIT_V1.json'; Hash = '429963458d6cbad3fc6a6ae8108ddd6e5578ad4fa4ee21a92d919f355184ac07' },
        @{ Path = 'definitions\c11d\production\D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json'; Hash = 'a3f480a76a526a67f77379191d82d1cb30876ae38b78b58ebefbd647b64529c8' },
        @{ Path = 'definitions\c11d\production\D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_SCHEMA_V1.json'; Hash = 'ad36c8f2b78fcc4f86a574b733f58cba5a4335156f6fe3882ef41dc4a4020205' }
    )

    foreach ($Pin in $Pins) {
        if (-not (Test-Path -LiteralPath $Pin.Path -PathType Leaf)) {
            throw "Falta fuente fijada: $($Pin.Path)"
        }
        $Actual = (Get-FileHash -LiteralPath $Pin.Path -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($Actual -ne $Pin.Hash) {
            throw "Hash inesperado antes del refresh: $($Pin.Path) = $Actual"
        }
    }

    $Manifest = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
    if ((Get-Item -LiteralPath $Manifest).Length -ne 796318) {
        throw 'Tamaño del manifiesto congelado C11-C incorrecto.'
    }

    $Python = (Get-Command python.exe -ErrorAction Stop).Source
    $IoRunner = Join-Path $Root 'tools\c11d\d9\d_renderer_candidate_io_gap_audit.py'
    $IdentityRunner = Join-Path $Root 'tools\c11d\d9\d_renderer_candidate_identity_inventory.py'
    $LogDir = Join-Path $env:TEMP ('C11D_V2_2_POST_RUNTIME_AUDITS_20261027_' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $LogDir | Out-Null

    # I/O gap audit: full report to stdout only; no report file is created by the audit itself.
    $IoOut = Join-Path $LogDir 'io_gap_stdout.json'
    $IoErr = Join-Path $LogDir 'io_gap_stderr.txt'
    $IoArgs = '-B "' + $IoRunner + '" --full-report'
    $IoProcess = Start-Process -FilePath $Python -ArgumentList $IoArgs -WorkingDirectory $Root -Wait -PassThru -NoNewWindow -RedirectStandardOutput $IoOut -RedirectStandardError $IoErr
    if ($IoProcess.ExitCode -ne 0) {
        if (Test-Path -LiteralPath $IoErr) { Get-Content -LiteralPath $IoErr }
        throw "La auditoría I/O gap falló. ExitCode=$($IoProcess.ExitCode). Logs=$LogDir"
    }
    try {
        $IoReport = Get-Content -LiteralPath $IoOut -Raw -Encoding UTF8 | ConvertFrom-Json
    }
    catch {
        throw "La salida I/O no es JSON válido: $($_.Exception.Message). Logs=$LogDir"
    }
    if ($IoReport.schema -ne 'C11-D-D9-RENDERER-CANDIDATE-IO-GAP-AUDIT-REPORT-V1' -or
        $IoReport.status -ne 'READ_ONLY_SOURCE_PINNED_GAP_AUDIT_PASS_NOT_READINESS_PASS' -or
        $IoReport.candidate_input_admissible -ne $false -or
        $IoReport.summary.schema_groups -ne 10 -or
        $IoReport.summary.complete_groups -ne 0 -or
        $IoReport.summary.partial_groups -ne 6 -or
        $IoReport.summary.blocked_groups -ne 4 -or
        $IoReport.summary.source_pins_verified -ne 54 -or
        $IoReport.summary.input_instance_emitted -ne $false -or
        $IoReport.summary.output_manifest_created -ne $false -or
        $IoReport.summary.media_created -ne $false -or
        $IoReport.governance.d4_8 -ne 'BLOCKED' -or
        $IoReport.governance.release_authority -ne 'NONE' -or
        $IoReport.audit_sha256 -notmatch '^[0-9a-f]{64}$') {
        throw "El informe I/O gap no cumple el estado esperado de auditoría. Logs=$LogDir"
    }
    $IoErrLength = (Get-Item -LiteralPath $IoErr).Length
    if ($IoErrLength -ne 0) { throw "stderr de I/O no está vacío. Logs=$LogDir" }

    # Identity inventory: output includes a compact JSON report line and a human-readable summary.
    $IdentityOut = Join-Path $LogDir 'identity_stdout.txt'
    $IdentityErr = Join-Path $LogDir 'identity_stderr.txt'
    $IdentityArgs = '-B "' + $IdentityRunner + '" --full-report'
    $IdentityProcess = Start-Process -FilePath $Python -ArgumentList $IdentityArgs -WorkingDirectory $Root -Wait -PassThru -NoNewWindow -RedirectStandardOutput $IdentityOut -RedirectStandardError $IdentityErr
    if ($IdentityProcess.ExitCode -ne 0) {
        if (Test-Path -LiteralPath $IdentityErr) { Get-Content -LiteralPath $IdentityErr }
        throw "El inventario de identidad falló. ExitCode=$($IdentityProcess.ExitCode). Logs=$LogDir"
    }

    $IdentityLines = @(Get-Content -LiteralPath $IdentityOut -Encoding UTF8)
    $Prefix = 'C11-D RENDERER CANDIDATE IDENTITY INVENTORY='
    $ReportLines = @($IdentityLines | Where-Object { $_.StartsWith($Prefix) })
    $SummaryLines = @($IdentityLines | Where-Object { $_.StartsWith('C11-D RENDERER CANDIDATE IDENTITY PASS |') })
    if ($ReportLines.Count -ne 1 -or $SummaryLines.Count -ne 1) {
        throw "La salida de identidad no tiene un único JSON y resumen. Logs=$LogDir"
    }
    try {
        $IdentityReport = $ReportLines[0].Substring($Prefix.Length) | ConvertFrom-Json
    }
    catch {
        throw "El JSON del inventario de identidad no es válido: $($_.Exception.Message). Logs=$LogDir"
    }
    if ($IdentityReport.schema -ne 'C11-D-RENDERER-CANDIDATE-IDENTITY-INVENTORY-V1' -or
        $IdentityReport.status -ne 'IDENTITY_ONLY_REVIEW_PACKET_NOT_BASELINE_READY' -or
        $IdentityReport.source_count -ne 164 -or
        $IdentityReport.protected_reference.matches_expected -ne $true -or
        $IdentityReport.governance.renderer_activation -ne 'OFF' -or
        $IdentityReport.governance.release_authority -ne 'NONE' -or
        $IdentityReport.governance.baseline_approval -ne 'MISSING' -or
        $IdentityReport.governance.freeze_eligible -ne $false -or
        $IdentityReport.source_fingerprint -notmatch '^[0-9a-f]{64}$' -or
        $IdentityReport.report_sha256 -notmatch '^[0-9a-f]{64}$') {
        throw "El informe de identidad no cumple los invariantes de gobernanza. Logs=$LogDir"
    }
    if ((Get-Item -LiteralPath $IdentityErr).Length -ne 0) {
        throw "stderr de identidad no está vacío. Logs=$LogDir"
    }

    $IoOutSha = (Get-FileHash -LiteralPath $IoOut -Algorithm SHA256).Hash.ToLowerInvariant()
    $IoErrSha = (Get-FileHash -LiteralPath $IoErr -Algorithm SHA256).Hash.ToLowerInvariant()
    $IdentityOutSha = (Get-FileHash -LiteralPath $IdentityOut -Algorithm SHA256).Hash.ToLowerInvariant()
    $IdentityErrSha = (Get-FileHash -LiteralPath $IdentityErr -Algorithm SHA256).Hash.ToLowerInvariant()

    $Marker = [ordered]@{
        schema = 'C11D-V2_2-POST-RUNTIME-AUDIT-REFRESH-EVIDENCE-V1'
        completed_local = (Get-Date).ToString('o')
        frozen_c11c_manifest_sha256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
        renderer = 'OFF'
        media_created = $false
        candidate_input_admissible = $false
        d4_8 = 'BLOCKED'
        release_authority = 'NONE'
        io_gap = @{
            exit_code = $IoProcess.ExitCode
            groups = '10/10'
            complete = 0
            partial = 6
            blocked = 4
            source_pins = '54/54'
            audit_sha256 = $IoReport.audit_sha256
            stdout_sha256 = $IoOutSha
            stderr_sha256 = $IoErrSha
        }
        identity = @{
            exit_code = $IdentityProcess.ExitCode
            source_files = $IdentityReport.source_count
            source_fingerprint = $IdentityReport.source_fingerprint
            report_sha256 = $IdentityReport.report_sha256
            python_version = $IdentityReport.toolchain.python_version
            godot_probe_status = $IdentityReport.toolchain.godot_probe_status
            godot_version = $IdentityReport.toolchain.godot_version
            stdout_sha256 = $IdentityOutSha
            stderr_sha256 = $IdentityErrSha
        }
        log_directory = $LogDir
    }
    $MarkerJson = $Marker | ConvertTo-Json -Depth 10
    Set-Content -LiteralPath $CompletedMarker -Value $MarkerJson -Encoding UTF8

    Write-Host 'C11D_POST_RUNTIME_IO_IDENTITY_REFRESH=PASS'
    Write-Host 'IO_AUDIT_EXIT_CODE=0'
    Write-Host 'IO_GROUPS=10/10'
    Write-Host 'IO_COMPLETE=0/10'
    Write-Host 'IO_PARTIAL=6'
    Write-Host 'IO_BLOCKED=4'
    Write-Host 'IO_SOURCE_PINS=54/54'
    Write-Host ("IO_AUDIT_SHA256=" + $IoReport.audit_sha256)
    Write-Host ("IO_STDOUT_SHA256=" + $IoOutSha)
    Write-Host ("IO_STDERR_SHA256=" + $IoErrSha)
    Write-Host 'IDENTITY_AUDIT_EXIT_CODE=0'
    Write-Host ("IDENTITY_SOURCE_FILES=" + $IdentityReport.source_count)
    Write-Host ("IDENTITY_FINGERPRINT=" + $IdentityReport.source_fingerprint)
    Write-Host ("IDENTITY_REPORT_SHA256=" + $IdentityReport.report_sha256)
    Write-Host ("IDENTITY_PYTHON=" + $IdentityReport.toolchain.python_version)
    Write-Host ("IDENTITY_GODOT_PROBE=" + $IdentityReport.toolchain.godot_probe_status)
    Write-Host ("IDENTITY_GODOT_VERSION=" + $IdentityReport.toolchain.godot_version)
    Write-Host ("IDENTITY_STDOUT_SHA256=" + $IdentityOutSha)
    Write-Host ("IDENTITY_STDERR_SHA256=" + $IdentityErrSha)
    Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
    Write-Host 'RENDERER=OFF'
    Write-Host 'MEDIA_CREATED=false'
    Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
    Write-Host 'D4.8=BLOCKED'
    Write-Host 'RELEASE_AUTHORITY=NONE'
    Write-Host ("LOG_DIRECTORY=" + $LogDir)
    Write-Host ("COMPLETION_MARKER=" + $CompletedMarker)
}
