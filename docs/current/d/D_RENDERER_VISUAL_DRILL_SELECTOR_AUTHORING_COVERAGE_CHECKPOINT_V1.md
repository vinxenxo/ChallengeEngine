# C11-D — Visual Drill Selector Authoring Coverage Checkpoint V1

**State:** `PREPARATION_ONLY_AUTHORING_ADAPTER_CAPABILITY_AUDIT_NOT_DYNAMIC_PAYLOAD_BINDING_OR_RENDERER_INPUT`

## Purpose

The next selector-expansion candidate is the existing Visual Drill authoring path. D9.8's canonical selector catalog has four Visual Drill types (`tracking`, `pursuit`, `saccade`, `peripheral_scan`) and five explicit difficulty tiers per type. The existing D-owned `VisualAuthoringGenerator`, `VisualAuthoringPolicyRegistry`, `VisualDifficultyResolver`, and `VisualDrillAuthoringAdapter` declare that path. Before extending the existing request-to-payload binder, run the single Godot audit in this checkpoint against all 20 type/tier combinations.

## Exact scope

- Four canonical Visual Drill types × five tiers = **20 selector combinations**.
- For each selector, verify canonical source and difficulty-policy hashes; requested type/tier identity; canonical duration/fps/frame_count; deterministic repeat under the same gameplay seed; and a changed visual-state digest under a second gameplay seed.
- Uses the current authoring adapter and its policies. It does not add a second request binder, create the request-specific payload manifest, or claim that these selectors are admitted by the existing dynamic binder.
- Challenge remains pinned to `parking_v2 / CHALLENGE_004`; Visual Loop remains pinned to `c11c_geometric_waves_v1 / harmonic_membrane`; the dynamic binder's full-selector expansion is a later increment.

## Runtime command

Run from the active Windows repo root with Godot 4.7.1 Mono available at `$env:C11D_GODOT_EXECUTABLE`:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_visual_drill_selector_authoring_coverage.py
if ($LASTEXITCODE -ne 0) { throw 'Visual Drill selector coverage contract failed.' }

python -B .\tools\c11d\d9\d_renderer_visual_drill_selector_authoring_coverage.py --contract-only
if ($LASTEXITCODE -ne 0) { throw 'Visual Drill selector coverage source/canonical catalog audit failed.' }

python -B .\tools\c11d\d9\d_renderer_visual_drill_selector_authoring_coverage.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 180
if ($LASTEXITCODE -ne 0) { throw 'Visual Drill selector authoring runtime audit failed.' }
```

Expected runtime summary: `families=4/4`, `selectors=20/20`, `deterministic_repeat=20/20`, `visual_seed_change=20/20`, `identity=20/20`, `policy_tier=20/20`. Preserve all 20 `VERIFIED` JSON receipt lines and the final report SHA-256. A Python/mock PASS or `--contract-only` PASS is not runtime acceptance.

## Gate after this audit

If all 20 runtime selectors pass, extend the **existing** dynamic request→payload binder in a separate versioned increment so that it accepts the four Visual Drill types and tiers 1–5, binds each canonical source/policy into the request manifest, and validates all 20 selector identities with actual Godot receipts. Do not start a parallel binder. If a case fails, keep that type/tier out of dynamic support and diagnose its exact authoring/policy defect.

## Governance locks

This checkpoint is authoring capability evidence only. It emits no request-bound payload manifest or renderer input and writes no report files. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, `baseline_approval=MISSING`, `freeze_eligible=false`. All presentation-region/visibility, timebase/temporal, coordinate/sample and audio/music proposals remain unapproved; no visual editorial consumer, renderer, dispatch, media, freeze or promotion is authorized. Frozen C11-C 2.19.12 and its manifest remain immutable.

## Future baseline/Producer cutover

After all C11-D gates close and formal approval, freeze and promotion are completed and explicitly accepted, C11-D and its Producer are intended to replace frozen C11-C as the authoritative baseline and Producer. This is a future cutover target, not present authority.

## V1.2 runtime guard correction

V1 runtime reached the matrix identity guard but rejected the canonical contract even though the Python contract-only audit validated its four family IDs, tiers 1–5, and selector count. The cause was a direct equality comparison between JSON-parsed Variant arrays and typed GDScript constant arrays. V1.2 normalizes JSON values into typed arrays, verifies every member in order, and validates the numeric selector count without relaxing the fixed 4 × 5 scope. The contract source pins and `output.harness_sha256` are updated to the corrected harness and regression test.

After applying V1.2, repeat the focused test, `--contract-only` audit, and actual Godot 4.7.1 20-selector runtime sweep. A Python PASS is not runtime acceptance.
