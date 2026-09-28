$ErrorActionPreference = "Stop"

Write-Host "=============================================="
Write-Host " C11-C 2.19.2 — FULL ACCEPTANCE"
Write-Host "=============================================="

Write-Host "`n[1/10] C11-C SUITE SELF TEST"
python .\c11c-suite\self_test.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[2/10] PRODUCER SELF TEST"
python .\c11c-suite\c11c-producer\self_test.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[3/10] PRODUCER GUI CONTRACT"
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[4/10] RETRO REFERENCE CONTRACT"
python .\c11c-suite\test_retro_reference_contract.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[5/10] FULL LOGICAL CORPUS — 137 SUITES"
python .\tests\run_all.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[6/10] CORE + C11 + RETRO + PHYSICAL + STRESS"
.\tools\c11freeze\run_all.ps1 -SeedLimit 32 -SeedRepeat 2 -StressRetries 3
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[7/10] C11-A.1 — 54 RUNS"
.\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[8/10] ART DIRECTION — COMPLETE CORPUS"
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
    -All `
    -Workers 7 `
    -Reset
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[9/10] LONGFORM — 5 FAMILIES"
.\tools\prototypes\c11c_bulk\run_c11c_visual_loop_longform_production_bulk.ps1 `
    -Seed 314159 `
    -Force
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n[10/10] REPOSITORY LAYOUT"
.\tools\maintenance\verify_repository_layout.ps1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================="
Write-Host " C11-C 2.19.2 — FULL ACCEPTANCE PASS"
Write-Host " =============================================="