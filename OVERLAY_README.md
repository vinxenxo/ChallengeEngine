# C11-C 2.19.12 - V21 PRE-FREEZE / SUITE + MAINTENANCE CONSOLIDATION

Apply this root-relative overlay on the already-installed C11-C 2.19.12/V19 state.

## Scope
- Aligns c11c-suite GUI/CLI routing with the current 2.19.12 canonical scripts.
- Keeps historical C11-A.1 qualification separate from current C11-C Challenge review.
- Hardens Suite self-test against stale acceptance references.
- Keeps Maintenance cleanup conservative and adds fail-closed frozen-source packaging validation.
- Makes the frozen package contain the current D handover and operational 2.19.12 acceptance launchers while excluding generated artifacts/caches.
- Consolidates active C11-C/D documentation and leaves historical evidence intact for the documentation archiver.

## Safety
No `core/` files are modified. No simulation/RNG/SimulationResult/winning_frame/close_calls/WinningFrameDetector/RenderedFrameStream/C7/C9/logical-geometry changes are included.

## Final workstation sequence
```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\verify_repository_layout.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\consolidate_c11c_2_19_documentation.ps1 -DryRun
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\consolidate_c11c_2_19_documentation.ps1
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.12.ps1
```

Then install the final historical `build_factory.py`, verify its SHA-256, and use Maintenance -> `CREAR ZIP FROZEN C11-C 2.19.12`.

Do not use the generic root `Make_zip.ps1` or `clean-videos.ps1` for the C11-C freeze.
