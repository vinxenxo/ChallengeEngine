# Testing and Regression

The project uses layered validation so that logical determinism, presentation contracts, physical rendering and production orchestration fail independently and remain diagnosable.

## Test authority

`tests/run_all.py` is the logical corpus runner. It discovers `*Test.gd`, requires explicit registration in `KNOWN_SUITES`, executes suites in deterministic order and checks their declared PASS markers.

Physical consumer tests are intentionally excluded from the default logical run because they require freshly generated media. They are executed by `run_physical_export_suite.ps1`.

## Test levels

### A. Fast logical regression

```powershell
python .\tests\run_all.py
```

This is the first command after any source or path change.

### B. Core contract validation

```powershell
.\tools\c11freeze\run_core_suite.ps1
```

Mechanics, RNG architecture and core simulation invariants.

### C. C11 presentation contracts

```powershell
.\tools\c11freeze\run_c11_suite.ps1
```

Unified Social Frame, presentation framing and UI integration.

### D. Retrocompatibility

```powershell
.\tools\c11freeze\run_retrocompatibility.ps1
```

Replays the 54 C11-A.1 reference executions and compares gameplay telemetry plus A/B determinism. Presentation-only frame hashes are intentionally not part of this gate after C11-B framing changes.

### E. Seed stress

```powershell
python .\tools\c11freeze\run_seed_stress.py --repeat 2 --retries 3
```

The frozen corpus is 288 challenge/seed cases, repeated twice for 576 logical executions. Retries apply only to transient process-level failures; telemetry mismatches remain hard failures.

### F. Physical smoke

```powershell
.\tools\c11freeze\run_physical_export_suite.ps1
```

Exercises the actual graphical Godot Compatibility + Movie Maker + FFmpeg path. Headless mode is not a substitute for physical export.

### G. 54-video QA matrix

```powershell
python .\tools\c11freeze\generate_qa_video_matrix.py --include-canonical --limit 0
.\tools\c11freeze\run_qa_video_matrix.ps1
```

This is a video-only QA matrix. The internal C7-A2 mixed-audio rule is expected to report out-of-scope when all 54 QA definitions are audio-off. The C11 gate requires the 54 video renders themselves to pass.

## Organization-checkpoint validation order

After applying a repository reorganization, run exactly:

```powershell
.\tools\maintenance\verify_repository_layout.ps1
.\tools\c11freeze\verify_freeze_structure.ps1
.\tools\c11freeze\run_core_suite.ps1
.\tools\c11freeze\run_c11_suite.ps1
python .\tests\run_all.py
.\tools\c11freeze\run_retrocompatibility.ps1
python .\tools\c11freeze\run_seed_stress.py --repeat 2 --retries 3
.\tools\c11freeze\run_physical_export_suite.ps1
python .\tools\c11freeze\generate_qa_video_matrix.py --include-canonical --limit 0
.\tools\c11freeze\run_qa_video_matrix.ps1
```

Expected C11-B reference counts are:

```text
logical        103/103
retro          54/54
stress         288 cases / 576 logical executions
physical       2/2
video matrix   54/54
```

The runner output is authoritative for the current number of discovered logical suites; the 103 count is the C11-B reference baseline.

## Targeted QA

C11 qualification/audit utilities live under `tools/qa/c11/`. C7 helpers live under `tools/qa/c7/`; C10 physical smoke lives under `tools/qa/c10/`.

Use these when a specific checkpoint needs diagnosis. They do not replace the canonical freeze gates.

## Evidence ownership

- logical/test reports → `artifacts/tests/`
- retro/regression → `artifacts/regression/`
- C11 QA → `artifacts/qa/`
- production outputs → `artifacts/production/`
- retained release evidence → `artifacts/releases/`

The exact output path is part of the tool contract and should be changed only through an explicit repository-organization checkpoint.

## What counts as a real regression

A failing assertion, changed deterministic telemetry, missing required fixture, broken `res://` dependency, failed physical validation or incorrect PASS/FAIL marker is a real failure. Do not hide it by broadening ignores or excluding the test from discovery.

Transient native-process failures may be retried only where the runner explicitly supports retries. A retry must never convert a deterministic mismatch into a pass.

## Maintenance rule

When reorganizing paths:

1. preserve tests and fixtures;
2. update explicit references;
3. run the fast logical corpus;
4. run the checkpoint/reproducibility gates;
5. inspect `git diff` for unintended semantic edits;
6. commit only after all required gates are green.
