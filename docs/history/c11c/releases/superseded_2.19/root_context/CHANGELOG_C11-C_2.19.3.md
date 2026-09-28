# C11-C CHANGELOG — 2.19.3 Repair Candidate

## Workstation acceptance repair

This checkpoint consolidates the repairs needed after the 2.19.2 acceptance run exposed stale contracts and environmental friction.

### Contract repairs

- Restored C11-A.1 factory isolation/quarantine of `override.cfg`.
- Restored the C11-A.1 isolation contract test.
- Restored the Visual Drill duration policy default to 17s; Tracking remains 21s.
- Restored the missing `_assert()` helper in the Longform source-artifact contract.

### Toolchain repair

- Restored the known-good `run_c11c_art_direction_batch_v4.ps1` source after a local PowerShell parser corruption.

### QA runtime hardening

- C10-C's explicit `--qa-mode` 2-second physical fixture is exempt from C11-C's 20-second production-duration gate. The fixture remains validated as a 60-frame C10 smoke artifact.
- Added safe acceptance-root quarantine and unique C11-A.1 acceptance output roots so pre-existing artifacts no longer block a fresh acceptance run.

No gameplay or frozen C11-B/C7/C9 truth was changed.

- Repair-v2: project-scoped named mutex around temporary Movie Maker `override.cfg`; seven review workers can no longer race the 720×1280 override.
- Repair-v2: five Visual Loop runners and Producer Drill release the override immediately after Godot capture.
- Suite ownership: canonical `c11c-suite` launchers are validated; retired `c11c-studio` is untouched and no longer required by layout validation.
