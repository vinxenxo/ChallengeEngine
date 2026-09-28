# C11-C Producer 0.9.7 — Console Test Commands

Run from the repository root.

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\tests\run_all.py
```

Single Visual Drill production smoke:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\c11c-suite\c11c-producer\run_visual_drill_production.ps1 `
  -Family tracking `
  -Seed 452878546 `
  -DifficultyTier 1 `
  -SpeedMultiplier 1.39686 `
  -PacingMode constant `
  -DeliveryProfile MASTER_1080 `
  -Force
```

Expected terminal marker:

```text
[C11-C-PRODUCER-DRILL] FINAL PRODUCT PASS:
```

The Art Direction multi-worker review is outside the single-product Producer route and is run through `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1`.
