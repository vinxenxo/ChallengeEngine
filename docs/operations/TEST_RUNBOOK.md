# Test Runbook

All commands are run from the repository root in Windows PowerShell.

## 0. Repository layout preflight

```powershell
.\tools\maintenance\verify_repository_layout.ps1
.\tools\c11freeze\verify_freeze_structure.ps1
```

These checks catch missing canonical directories, missing fixtures/tools/docs and accidental reintroduction of retired roots before expensive rendering begins.

## 1. Fast logical regression

```powershell
python .\tests\run_all.py
```

Expected C11-B reference: 103 logical suites PASS. Physical export consumer tests are intentionally skipped here and executed by the physical suite.

## 2. Core suite

```powershell
.\tools\c11freeze\run_core_suite.ps1
```

Covers deterministic mechanics, RNG architecture and core invariants.

## 3. C11 contract suite

```powershell
.\tools\c11freeze\run_c11_suite.ps1
```

Covers framing, Unified Social Frame and Social UI integration.

## 4. Retrocompatibility

```powershell
.\tools\c11freeze\run_retrocompatibility.ps1
```

Reference corpus: 54 C11-A.1 executions, including telemetry comparison and deterministic A/B checks.

## 5. Seed stress

```powershell
python .\tools\c11freeze\run_seed_stress.py --repeat 2 --retries 3
```

Reference corpus: 288 cases × 2 repeats = 576 logical executions. Retries are restricted to transient process-level failures; deterministic telemetry mismatches never become passes through retry.

## 6. Physical export

```powershell
.\tools\c11freeze\run_physical_export_suite.ps1
```

This is the authoritative graphical Movie Maker smoke. It uses Godot 4.7.1 Compatibility rendering, then FFmpeg/FFprobe validation. Do not replace it with headless rendering.

## 7. QA video matrix

```powershell
python .\tools\c11freeze\generate_qa_video_matrix.py --include-canonical --limit 0
.\tools\c11freeze\run_qa_video_matrix.ps1
```

Reference matrix: 54/54 video renders. It is intentionally video-only; C7-A2's mixed-audio policy remains a separate production contract.

## Full organization/release validation

Use this sequence after a repository reorganization or before a freeze/release:

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

## Evidence locations

- tests → `artifacts/tests/`
- retro/regression → `artifacts/regression/`
- C11 QA → `artifacts/qa/`
- production → `artifacts/production/`
- retained releases/freeze evidence → `artifacts/releases/`

## Debugging discipline

Run the smallest failing layer first. Do not skip a failed logical suite because a physical export succeeds, and do not interpret a video-only C7-A2 policy failure as a video-render failure when the 54 render results are individually PASS.
