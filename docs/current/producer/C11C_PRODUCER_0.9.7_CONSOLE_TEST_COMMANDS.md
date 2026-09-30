# C11-C Producer 0.9.7 — Console Test Commands

Run from the repository root.

## Producer static checks

```powershell
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
```

## Producer runtime entry point

Use the canonical Producer command surface under:

`c11c-suite/c11c-producer/`

The Producer delegates to the C11-C backend/prototype launchers. It does not reimplement simulation, mechanics or the visual backend.

## Visual Loop review

The current Art Direction review authority is:

```text
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1
```

The consolidated 52-product review authority is:

```text
.\tools\qa\c11\run_c11c_complete_video_review.ps1
```

## Visual Drill production

The current Producer-side launcher is:

```text
.\c11c-suite\c11c-producer\run_visual_drill_production.ps1
```

## Operator rule for D

When D introduces a new production/test capability, first establish or preserve its canonical console command. The GUI must invoke that same operation rather than becoming a second backend.
