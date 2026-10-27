& {
    $ErrorActionPreference = 'Stop'
    $Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
    Set-Location -LiteralPath $Root
    $AttemptMarker = Join-Path $env:TEMP 'C11D_CHALLENGE_SEED_COLLISION_REJECTION_AUDIT_20261027.started.json'
    $CompletedMarker = Join-Path $env:TEMP 'C11D_CHALLENGE_SEED_COLLISION_REJECTION_AUDIT_20261027.completed.json'
    if ((Test-Path -LiteralPath $AttemptMarker) -or (Test-Path -LiteralPath $CompletedMarker)) { throw "La auditoría Challenge 9-selectores ya se intentó o completó; no se repite: $AttemptMarker | $CompletedMarker" }
    $ExpectedManifest = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
    $Manifest = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
    if (-not (Test-Path -LiteralPath $Manifest -PathType Leaf) -or (Get-Item -LiteralPath $Manifest).Length -ne 796318 -or (Get-FileHash -LiteralPath $Manifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedManifest) { throw 'Manifiesto congelado C11-C distinto.' }
    $Python = (Get-Command python.exe -ErrorAction Stop).Source
    $Runner = Join-Path $Root 'tools\c11d\d9\d_renderer_challenge_seed_collision_rejection_audit_v1.py'
    if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw "Falta runner de auditoría: $Runner" }
    $ExpectedRunnerSha = '266e6909b3b23c9ee08652a1dc78c0846ce3c52b1bf9c2d0f1394202e11683cc'
    $ActualRunnerSha = (Get-FileHash -LiteralPath $Runner -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($ActualRunnerSha -ne $ExpectedRunnerSha) { throw "Hash del runner inesperado: $ActualRunnerSha" }
    $LogDir = Join-Path $env:TEMP ('C11D_CHALLENGE_SEED_COLLISION_AUDIT_20261027_' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $LogDir | Out-Null
    $Attempt = [ordered]@{ schema='C11D-CHALLENGE-SEED-COLLISION-REJECTION-AUDIT-ATTEMPT-V1'; started_local=(Get-Date).ToString('o'); repository_root=$Root; log_directory=$LogDir; runner_sha256=$ActualRunnerSha; frozen_c11c_manifest_sha256=$ExpectedManifest }
    Set-Content -LiteralPath $AttemptMarker -Value ($Attempt | ConvertTo-Json -Depth 5) -Encoding UTF8
    $Stdout = Join-Path $LogDir 'challenge_seed_collision_stdout.txt'
    $Stderr = Join-Path $LogDir 'challenge_seed_collision_stderr.txt'
    $Args = '-B "' + $Runner + '" --root "' + $Root + '" --full-report'
    $Process = Start-Process -FilePath $Python -ArgumentList $Args -WorkingDirectory $Root -Wait -PassThru -NoNewWindow -RedirectStandardOutput $Stdout -RedirectStandardError $Stderr
    $OutSha = (Get-FileHash -LiteralPath $Stdout -Algorithm SHA256).Hash.ToLowerInvariant()
    $ErrSha = (Get-FileHash -LiteralPath $Stderr -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Process.ExitCode -ne 0) { throw "Audit exit code $($Process.ExitCode); conservar $LogDir; stdout=$OutSha; stderr=$ErrSha" }
    $Lines = @(Get-Content -LiteralPath $Stdout -Encoding UTF8)
    if ($Lines.Count -lt 2 -or $Lines[0] -notmatch '^C11-D CHALLENGE SEED COLLISION REJECTION AUDIT V1 PASS') { throw "No aparece marcador PASS/reporte completo; conservar $LogDir" }
    try { $Report = $Lines[$Lines.Count - 1] | ConvertFrom-Json }
    catch { throw "Última línea stdout no es reporte JSON; conservar $LogDir" }
    if ($Report.selectors -ne 9 -or $Report.explicit_seed_negative_cases.passed -ne 90 -or $Report.explicit_seed_negative_cases.total -ne 90 -or $Report.numeric_seed_collision_rejections.passed -ne 18 -or $Report.numeric_seed_collision_rejections.total -ne 18 -or $Report.source_pin_count -ne 27 -or $Report.runtime_invocations -ne 0 -or $Report.all_rejections_precede_godot -ne $true -or $Report.seed_domains_complete_for_candidate_input -ne $false -or $Report.frozen_c11c_manifest_sha256 -ne $ExpectedManifest) { throw "Campos de reporte distintos de lo esperado; conservar $LogDir" }
    $ExpectedIds = @('CHALLENGE_001','CHALLENGE_002','CHALLENGE_003','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007','CHALLENGE_008','CHALLENGE_009')
    if ((@($Report.selector_matrix | ForEach-Object { $_.challenge_id }) -join ',') -cne ($ExpectedIds -join ',')) { throw "La matriz no contiene CHALLENGE_001..009 en orden; conservar $LogDir" }
    if ($Report.rejection_outcomes.Count -ne 108) { throw "Cardinalidad de outcomes incorrecta; conservar $LogDir" }
    $ReportPath = Join-Path $LogDir 'challenge_seed_collision_report.json'
    Set-Content -LiteralPath $ReportPath -Value ($Lines[$Lines.Count - 1]) -Encoding UTF8
    $ReportFileSha = (Get-FileHash -LiteralPath $ReportPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $SelfHash = [string]$Report.audit_sha256
    if ($SelfHash -notmatch '^[0-9a-f]{64}$') { throw "audit_sha256 ausente/malformado; conservar $LogDir" }
    if ((Get-Item -LiteralPath $Manifest).Length -ne 796318 -or (Get-FileHash -LiteralPath $Manifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedManifest) { throw 'El manifiesto congelado C11-C cambió durante el audit.' }
    $Completion = [ordered]@{ schema='C11D-CHALLENGE-SEED-COLLISION-REJECTION-AUDIT-COMPLETION-V1'; completed_local=(Get-Date).ToString('o'); repository_root=$Root; exit_code=$Process.ExitCode; selectors=9; negative_cases='90/90'; collision_rejections='18/18'; source_pins='27/27'; audit_sha256=$SelfHash; report_file_sha256=$ReportFileSha; stdout_sha256=$OutSha; stderr_sha256=$ErrSha; log_directory=$LogDir; report_file=$ReportPath; renderer='OFF'; media_created=$false; candidate_input_admissible=$false; D4_8='BLOCKED'; release_authority='NONE' }
    Set-Content -LiteralPath $CompletedMarker -Value ($Completion | ConvertTo-Json -Depth 6) -Encoding UTF8
    Write-Host 'C11D_CHALLENGE_SEED_COLLISION_REJECTION_AUDIT=PASS'
    Write-Host ("AUDIT_EXIT_CODE=" + $Process.ExitCode)
    Write-Host 'SELECTORS=9'
    Write-Host 'EXPLICIT_SEED_NEGATIVE_CASES=90/90'
    Write-Host 'NUMERIC_SEED_COLLISION_REJECTIONS=18/18'
    Write-Host 'COLLISION_VALUES=12345,840001'
    Write-Host 'ALL_REJECTIONS_PRECEDE_GODOT=true'
    Write-Host 'SOURCE_PINS=27/27'
    Write-Host 'RUNTIME_INVOCATIONS=0'
    Write-Host ("AUDIT_SHA256=" + $SelfHash)
    Write-Host ("REPORT_FILE_SHA256=" + $ReportFileSha)
    Write-Host ("STDOUT_SHA256=" + $OutSha)
    Write-Host ("STDERR_SHA256=" + $ErrSha)
    Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
    Write-Host 'RENDERER=OFF'; Write-Host 'MEDIA_CREATED=false'; Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'; Write-Host 'D4.8=BLOCKED'; Write-Host 'RELEASE_AUTHORITY=NONE'
    Write-Host ("LOG_DIRECTORY=" + $LogDir)
    Write-Host ("REPORT_FILE=" + $ReportPath)
    Write-Host ("ATTEMPT_MARKER=" + $AttemptMarker)
    Write-Host ("COMPLETION_MARKER=" + $CompletedMarker)
} 
