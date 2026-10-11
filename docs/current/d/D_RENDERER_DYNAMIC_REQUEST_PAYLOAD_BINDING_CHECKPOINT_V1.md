# C11-D — Dynamic Request → Payload Binding Checkpoint V1

**Checkpoint state:** JSON numeric-type compatibility repair prepared after the first real Godot 4.7.1 run rejected integer-valued JSON numbers as non-`TYPE_INT`; Python contract tests pass in the isolated merged preparation tree; **actual Godot 4.7.1 Windows rerun remains required**. Not approved for candidate input or rendering.

## 1. Why this increment exists

Prior request-scoped binding proved canonical chain lineage for three fixed selector fixtures, but the source materialization harnesses were not receiving a strict per-request envelope and their Python tests used mocked subprocesses. This increment introduces a D-owned, strict envelope and a Godot headless probe that materializes two deterministic in-memory payload copies for each received request.

The default Python runner evaluates ten requests: a base and a gameplay-seed-only mutation for each of the three supported selector representatives, plus four Visual Loop orthogonality changes (music seed, variation index, delivery profile identity, editorial title).

## 2. Current selector matrix and truthful status

| Content type | Pinned selector | Payload claim |
|---|---|---|
| Challenge | `parking_v2 / CHALLENGE_004` | Dynamic source copy changes `generation.seed` in memory and passes through the runtime bridge. It captures source-timebase gameplay-frame visual records. Exact fixed selector payload probe: `true`. |
| Visual Loop | `c11c_geometric_waves_v1 / harmonic_membrane` | Uses the deterministic geometric family variation, palette and authoring envelope. Authoring output remains `geometric`; grammar consumption is not proven. Exact selected grammar payload: `false`, scope remains `VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED`. |
| Visual Drill | `tracking / tier-2` | Dynamic seed is applied to the Visual Authoring context and checks the seeded motion/trajectory envelope. Exact fixed selector payload probe: `true`. |

No additional family, grammar, Drill tier, Challenge variant or Longform selector is admitted. The selector matrix is a review-only sample, not a catalogue-wide certification.

## 3. Request identity vs visual state

Each Godot summary emits both:

- `payload_sha256`: hash of the complete bounded in-memory payload, including its request-specific source identity.
- `visual_state_sha256`: a separate digest of seed-derived visual evidence, excluding a bare seed label where applicable. For Challenge, this is the actual serialized gameplay-frame record signature; for Visual Loop, the deterministic family variation/palette/authoring visual parameters and timing; for Visual Drill, the seed-derived trajectory and motion parameters with direct seed/version labels removed.

The runner requires the visual-state digest to change between base and gameplay-seed-only requests in all three content types. It also requires Visual Loop visual-state and payload hashes to remain unchanged when only music seed, `variation_index`, delivery profile identity or editorial title changes, while the canonical request-binding identity changes.

These relations still require execution against real Godot 4.7.1. The Python test intentionally mocks the subprocess, proving Python contract behavior only.

## 4. Strict envelope and receipts

Input envelope has exact keys and is constrained by JSON Schema Draft 2020-12 to the fixed selector matrix, seed domains, `social_default_v1`, and four non-Longform delivery IDs. Unknown keys, unsupported selectors, `LONGFORM_1080` and unapproved presentation profiles fail closed.

The Python runner reuses the existing D9.9 canonical universal-request evaluator, D9.10 editorial bridge, D-owned adapter and request-scoped binding, then passes only the canonical envelope fields to Godot. It verifies the summary, strict in-memory receipt schema, source lineage pins (40 total, frozen C11-C manifest first), and nested binding digest. Receipts are printed to stdout, not persisted.

## 5. Safety / governance boundary

- No edits to C11-C or frozen source files.
- Challenge source JSON is read and hash-checked, deep-copied in memory, and the request seed is applied only to the copy.
- No use of `winning_frame` or `close_calls` as timing; simulation telemetry is excluded.
- No delivery resampling, coordinate projection, visual-region policy, editorial visual consumption, audio/music rendering, renderer-native input, renderer dispatch or media output.
- `music_seed` stays outside visual-state generation; `variation_index` remains metadata only; delivery-profile identity does not apply geometric/timing transforms.
- Existing editorial carrier still has 14/14 canonical values hash-bound and 0/14 visually consumed.
- `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; baseline approval absent; freeze eligibility false; D9.14/D9.16 blocked; D9.17 NO-GO; D10 blocked.

## 6. Validation performed in preparation

- New Python contract test: PASS — 12 logical checks; 40/40 source pins; 2/2 schemas; 10/10 mocked matrix cases; gameplay seed relation 3/3; orthogonality 4/4; 20 fail-closed negative checks.
- Prior request-scoped payload binding test: PASS.
- Prior request-scoped materialization binding test: PASS (mocked Godot contracts, not actual Godot execution).
- A combined broader regression command hit the execution timeout before all regressions produced output; it is **not** recorded as a full-suite PASS.

## 7. Runtime defect found and repair prepared

The first actual Windows Godot 4.7.1 run failed at the harness input validator for `seed`, `music_seed` and `variation_index`. The canonical D9.9 request chain and Python JSON Schema checks had accepted these values; the mismatch was the GDScript validator requiring `typeof(value) == TYPE_INT` even though Godot's JSON parser can represent JSON numeric literals as `TYPE_FLOAT`. The harness now accepts only finite, mathematically integral `TYPE_INT`/`TYPE_FLOAT` values in the exact field ranges. Boolean, fractional, non-finite, and out-of-range values remain rejected. The contract's dedicated harness SHA-256 was refreshed; no source-lineage or frozen C11-C file was changed.

This repair has not been certified by a real runtime in the preparation environment. Windows must rerun the full 10-case matrix after applying the repair.

## 8. Windows runtime gate

From the repository root, after extracting the overlay and running the contract test, verify the configured executable reports `4.7.1.stable.mono.official.a13da4feb`, then run:

`python -B .\tools\c11d\d9\d_renderer_dynamic_request_payload_binding.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120`

Required final summary includes `cases=10`, `selector_types=3/3`, `gameplay_seed_binding=3/3`, `orthogonality=4/4`, `loop_grammar_instance=UNRESOLVED`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`. A failure should be diagnosed before any further payload-consumer work.

Then run the targeted regressions separately:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_binding.py
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding.py
python -B .\tools\c11d\d9\test_d_renderer_candidate_io_contract.py
python -B .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python -B .\tools\c11d\d9\test_cross_suite_lifecycle.py
python -B .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
```

## 9. Next step after runtime PASS

Review runtime evidence and source/seed relationships before proposing another additive increment. The most material remaining limitation is the Visual Loop selector-to-grammar gap. Do not build a visual editor/consumer for `harmonic_membrane` until its grammar-instance integration is proven and the relevant presentation/timing policies are formally approved. This checkpoint does not authorize D4.8, D9.14 full media certification, D9.16, D9.17 closure, D10 closure, renderer baseline approval/freeze, or release.
