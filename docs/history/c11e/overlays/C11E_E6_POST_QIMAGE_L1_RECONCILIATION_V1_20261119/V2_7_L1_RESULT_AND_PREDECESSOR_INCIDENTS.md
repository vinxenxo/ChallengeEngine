# V2.7 L1 result and phase reconciliation — incident/evidence record

## Accepted operator output

- Installer: `PASS_ADD_ONLY`, 18/18 verified, 11/11 docs verified; receipt SHA `48dc18147f2e2f3eaed4b72d42df1d97fa39eb20b0a464eea9debc6b3acd6173`.
- Bootstrap regressions: 8/8 PASS.
- Runner: 23/23 source pins; A3 V4 PASS; QImage test module import PASS; 37/37 QImage tests PASS.
- Runtime: Python 3.13.14; PySide6 6.11.2.
- Benchmark: 7 iterations, P50 4.7681 ms, P95 5.5743 ms, 179.3947 fps at P95.
- Runner status: `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`; receipt SHA `95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783`.

## Classification of previous failures

- V2.4: no installer invocation; outer `Expand-Archive` failed due long extraction path.
- V2.6: post-write PowerShell 5.1 expression-binding error; rollback PASS removed all 16 owned additions. The later `Ran 0 tests` was exit code 5, not a pass; runner path absent after rollback.
- V2.7: supersedes the installer defect and completes the synthetic L1 stage. No prior failure receipt or evidence is rewritten.

## Remaining qualification boundaries

Synthetic preview PNG hashes and geometry can be machine-verified, but the resampler still requires operator visual review. Geometry approval 720×1280 with content 504×896 at (108,192) does not approve `SmoothTransformation` quality. Challenge static consumer audit is not Godot runtime readback. CH004 is eligible for E6 ledger requalification, not accepted. Six Loop D-composited Smoke18 outputs remain outstanding; six Drill row-level runtime/editorial predicates remain outstanding.
