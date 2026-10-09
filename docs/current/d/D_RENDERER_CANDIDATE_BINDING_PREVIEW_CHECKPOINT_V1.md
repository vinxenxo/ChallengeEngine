# C11-D Renderer Candidate Binding Preview — Checkpoint V1

**Status:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`  
**Checkpoint:** `D_RENDERER_CANDIDATE_BINDING_PREVIEW_V1`  
**Date:** 2026-10-09  
**Scope:** C11-D only. C11-C 2.19.12 and its historical freeze manifest are unchanged.

## Purpose

This is the first isolated implementation increment for the future D-owned renderer baseline. It creates a deterministic in-memory binding preview from an already validated D9.10 adapter envelope. It is deliberately not renderer-native input, not a render job, not a dispatch message, and not an approval checkpoint.

The preview makes request/plan/editorial/bridge/envelope lineage inspectable, resolves the delivery profile against the existing delivery registry, records the presentation profile by its canonical identifier, and shows proposed editorial slot mappings. The slot IDs are design proposals marked `PROPOSED_NOT_APPROVED`; no existing renderer is claimed to consume them.

## Files

- `definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_V1.json` — contract, supported scope, mapping proposals and governance locks.
- `definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_SCHEMA_V1.json` — versioned JSON Schema for the in-memory preview shape.
- `tools/c11d/d9/d_renderer_candidate.py` — deterministic, read-only builder/validator for binding previews.
- `tools/c11d/d9/test_d_renderer_candidate.py` — focused positives, determinism checks and fail-closed regressions.

## Behavior

- Input must be a valid D9.10 adapter envelope with status `PREPARED_NOT_DISPATCHED_RENDERER_DISABLED` and a valid self-hash.
- Supported content types are exactly `challenges`, `visual_loops`, and `visual_drills`. Longform and unknown types fail closed.
- Editorial bindings are checked against the canonical universal editorial model allowlist. Their combined identity hash must still match the envelope's immutable `editorial_hash`.
- Delivery profile IDs are resolved against `profiles/delivery/c11c_video_delivery_profiles.json`; aliases are resolved with cycle/target checks and only an explicit property allowlist is copied into the preview. The registry and resolved profile hashes are recorded.
- Gameplay and music seeds are copied into separate domains. Equal values, boolean/non-integer values, automatic generation, runtime derivation or domain sharing fail closed.
- `SimulationResult`, `winning_frame`, `close_calls`, simulation truth and derived telemetry are not bound.
- Preview hashes exclude no governed content other than the preview's own `preview_sha256` field. Validation rebuilds expected content from the source envelope; changing the preview and recomputing its self-hash does not bypass source-lineage checks.
- The module does not write files or media, launch processes, invoke Godot/FFmpeg, or connect to any renderer. Results exist only in memory.

## Preparation-workspace verification

Observed in the isolated preparation copy on 2026-10-09:

```text
C11-D D9.10 EDITORIAL-RENDER BRIDGE PLANNING PASS | content_types=3/3 | CLI bridge parity=3/3 | adapter parity=3/3 | negative=15/15 | adapter_negative=9/9 | adapter=PREPARE_ONLY | renderer_input=NOT_EMITTED | renderer=OFF | production=false | D4.8=BLOCKED | release_authority=NONE
C11-D RENDERER CANDIDATE BINDING PREVIEW PASS | content_types=3/3 | deterministic=3/3 | negative=13/13 | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE
Python compilation: PASS
```

These are preparation-workspace results, not yet operator-confirmed results on the active Windows checkout. The focused test is intentionally not added to the existing aggregate suite in this increment; current expected aggregate remains 22/22 until the focused Windows result and later review approve its integration into the suite.

## Windows verification

From `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` after applying the overlay:

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_candidate.py .\tools\c11d\d9\test_d_renderer_candidate.py
python .\tools\c11d\d9\test_d_renderer_candidate.py
python .\tools\c11d\d9\test_editorial_render_bridge.py
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

The candidate test target is `content_types=3/3`, `deterministic=3/3`, `negative=13/13`. The remaining existing D9 tests and aggregate must also stay green on Windows. Recompute the candidate fingerprint after applying files; do not reuse a previous tree SHA.

## Limits and next work

This checkpoint does **not** implement or execute the renderer kernel and does not prove that editor values are physically visible in rendered frames. That proof remains part of the separately reviewed D renderer implementation and authorized D9.14 real-media GUI/E2E acceptance.

Next engineering increments should define a separately versioned renderer input/output protocol and an isolated deterministic D-owned implementation. They must remain disconnected from dispatch until the separately approved/frozen D renderer baseline, explicit D4.8 authorization, D9.14 full PASS, D9.16 full PASS, D9.17 explicit closure and dispatch approval checkpoints all exist.

Mandatory locks remain: adapter `PREPARE_ONLY`; renderer input/dispatch/activation OFF; production and media false; `D4.8=BLOCKED`; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain immutable. Definitive GUI work remains deferred until the complete D baseline is accepted and frozen.
