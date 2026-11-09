# C11-E E4B Loop22 — Shared Output Directory Collision Root Cause (V1)

**Date:** 2026-11-09  
**Disposition:** Confirmed from the operator's V2 Windows evidence bundle.  
**Scope:** TEST_ONLY runner initialization; no media process was launched.

## Evidence and confirmed cause

The V2 PowerShell process bridge itself passed its self-test, separated stdout/stderr, preserved child exit codes 0 and 23, parsed under Windows PowerShell 5.1, parsed the pinned Python sources, and ran all 24 pre-existing Loop22 focused tests successfully. The fail-closed prelaunch marker was emitted.

The pinned V1 Python runner then exited with code 2. Its stderr log contains `FileExistsError: [WinError 183]` for the path `artifacts/tests/c11e/e4b_loop22_av/L22_114530_E51BDA/source/geometric/A`.

The defect is in the runner's directory bootstrap. It builds 44 logical jobs (22 selectors × A/B). Jobs for different selectors in the same family and repeat intentionally share four physical roots: `source`, `native_audio`, `delivery_pcm`, and `delivery_av`. The old bootstrap iterated every job and called `mkdir(parents=True, exist_ok=False)` on all four paths. The first job created a shared path; a later selector attempted to create the same path again and Windows raised WinError 183.

The evidence archive contains only the run folder and empty planned output directories; the processes folder is empty. Runner stdout is empty. No C11-C launcher, native family music generator, resampler, FFmpeg mux or audiovisual output was started. The run failed before the runner's first media-launch line. This is not a FFmpeg/FFprobe, audio, R1P, R1V, PowerShell stderr, or operator policy failure.

## Corrective implementation

A new, separately versioned runner V2 adds an ordered path-identity planner. It normalizes each path using absolute path, `normpath`, `normcase`, and `casefold`; shared paths are deduplicated only when they have the same `(role, internal_family_id, repeat)` owner. Any cross-role/family/repeat alias fails closed.

The 44 jobs are expected to reference exactly 40 unique physical output directories: 5 families × 2 repeats × 4 roles. The runner checks that cardinality, verifies each unique destination is absent, then creates each directory exactly once with `exist_ok=False`. It does not weaken overwrite protection or change paths, slot identities, media commands, audio settings, seeds, source pins or governance.

The original V1 runner and the V2 PowerShell bridge wrapper remain unchanged and pinned. A new V3 PowerShell wrapper uses the same .NET process bridge, revalidates V1/V2 install receipts and the 37 V2 source pins, parses the V2 runner/tests, and requires 25 focused tests before any capture. The additional regression creates the 44 logical jobs, proves the 40-directory plan, creates all 40 exactly once, then proves a second exclusive create still fails.

## Current status and next gate

- V1 package installation: `PASS_ADD_ONLY_INSTALL`.
- V2 process-bridge package installation: `PASS_ADD_ONLY_INSTALL`.
- V2 bridge self-test: PASS.
- V2 PowerShell AST: PASS.
- V2 Python AST: PASS.
- V2 focused tests: 24/24 PASS.
- V1 runner initialization: FAIL before media launch, due to duplicate shared-directory creation.
- Captures / launcher invocations / music / PCM delivery / mux / AV outputs from the failed run: 0.

Install the new shared-directory-fix overlay add-only and then run **only** `RUN_C11E_E4B_LOOP22_AV_QUALIFICATION_V3.ps1`. The wrapper must report 25/25 and all prelaunch gates before handing off to the new pinned runner V2. A technical 44/44 + 22/22 result will still require operator visual/editorial/layout and audio review of all 44 outputs.

## Governance

C11-C 2.19.12 and frozen manifest SHA-256 `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953` remain immutable. R1P 27/27 and the five-selector R1V pilot remain accepted and are not repeated. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No D renderer, D3 V5, dispatch, production promotion, or release. No Git checks; commits operator-managed.
