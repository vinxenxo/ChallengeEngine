# C11-D Challenge V2-C Source-Frame Runtime Receipt Overlay

**Status: prepared; Windows Godot runtime execution is not claimed.** This is an add-only overlay for the active `ChallengeEngineV01_STATELESS` checkout, based for design/pinning on the user-selected `ChallengeEngineV01_STATELESS_NIGHTLY_20261710_1555.zip`.

## Contents

- A new V2-C contract with 81 SHA-256 source pins, source selectors, asset references, canonical planning boundaries, timebase blockers and governance locks.
- Contract, receipt and report JSON Schemas.
- A Python runner that reconciles pins, uses the canonical D9.9 planner (`evaluate_universal_request`), checks the D9.10 planning-only bridge/adapter, then launches two independent Godot 4.7.1 Mono processes per selector.
- A new in-memory Godot harness that calls `ChallengeRuntimeBridge.run_effective_pipeline` once per process and emits only a source-frame receipt.
- 26 fail-closed Python contract/negative tests.
- A uniquely named V2-C plan document. Existing V6 checkpoint and the existing `CHALLENGE_004` V1 harness are not modified.

## Safety boundaries

V2-C is source-frame and route acceptance only. It hashes only the ordered index plus these base fields: `position`, `rotation`, `scale`, `opacity`, `texture_index`, and `variant_id`. It never serializes the full `FrameSnapshot.custom_data` map or any candidate custom-data values; candidate observations are field-presence/type histograms only. `approved_bindings` remains zero, the renderer remains OFF, no media or payload is created, and visual seed sensitivity remains `NOT_TESTED`.

`CHALLENGE_008` and `CHALLENGE_009` remain blocked for phase/timeline acceptance: declared total 11 s versus phase sum 12 s. This overlay neither mutates the two challenge JSON files nor infers which timebase is authoritative.

## Apply and test

Use the separate paste-ready PowerShell 5.1 APPLY and TEST blocks accompanying the overlay. Run from the repository root. Application is guarded by the frozen-manifest pin, archive/manifest/file hashes, and absent add-only destinations. Python tests must pass before the runtime runner is called. The runtime runner writes reports and process stdout/stderr only to the operator-specified short `%TEMP%` evidence directory. It exits nonzero and reports every selector as accepted, blocked, or not run after first failure; it never silently shrinks the nine-selector denominator.

The archive is not evidence that the overlay has been applied to the Windows checkout, and the generated harness is not runtime evidence until executed with the actual Godot 4.7.1 Mono executable.
