# C11-D — Dynamic Request → Payload Binding Checkpoint V1

**Current state after Visual Loop grammar runtime gates:** the separate Grammar Binding Audit and Grammar Parameter Instance gates have been operator-reported PASS on Godot 4.7.1. This increment composes their pinned `harmonic_membrane@0` 20-parameter instance into the existing D dynamic request→payload review object for the one admitted Visual Loop selector. It does not make `VisualLoopAuthoringAdapter` grammar-aware and does not instantiate a renderer, execute a shader, emit renderer-native input, or create media.

**Checkpoint state:** JSON numeric-type compatibility repair prepared after the first real Godot 4.7.1 run rejected integer-valued JSON numbers as non-`TYPE_INT`; Python contract tests pass in the isolated merged preparation tree; **actual Godot 4.7.1 Windows rerun remains required**. Not approved for candidate input or rendering.

## 1. Why this increment exists

Prior request-scoped binding proved canonical chain lineage for three fixed selector fixtures, but the source materialization harnesses were not receiving a strict per-request envelope and their Python tests used mocked subprocesses. This increment introduces a D-owned, strict envelope and a Godot headless probe that materializes two deterministic in-memory payload copies for each received request.

The default Python runner evaluates ten requests: a base and a gameplay-seed-only mutation for each of the three supported selector representatives, plus four Visual Loop orthogonality changes (music seed, variation index, delivery profile identity, editorial title).

## 2. Current selector matrix and truthful status

| Content type | Pinned selector | Payload claim |
|---|---|---|
| Challenge | `parking_v2 / CHALLENGE_004` | Dynamic source copy changes `generation.seed` in memory and passes through the runtime bridge. It captures source-timebase gameplay-frame visual records. Exact fixed selector payload probe: `true`. |
| Visual Loop | `c11c_geometric_waves_v1 / harmonic_membrane` | D-owned composite keeps the authoring envelope (`geometric`) and adds a hash-bound `grammar_parameter_instance` for `harmonic_membrane@0`, branch `field_harmonic_membrane`, uniform `grammar_mode`, 20 style parameters. Exact pinned selector composite payload: `true`, scope `VISUAL_LOOP_SELECTOR_PAYLOAD_HARMONIC_MEMBRANE_V1`. The family adapter itself remains grammar-agnostic; other grammar IDs remain rejected. |
| Visual Drill | `tracking / tier-2` | Dynamic seed is applied to the Visual Authoring context and checks the seeded motion/trajectory envelope. Exact fixed selector payload probe: `true`. |

No additional family, grammar, Drill tier, Challenge variant or Longform selector is admitted. The selector matrix is a review-only sample, not a catalogue-wide certification.

## 3. Request identity vs visual state

Each Godot summary emits both:

- `payload_sha256`: hash of the complete bounded in-memory payload, including its request-specific source identity.
- `visual_state_sha256`: a separate digest of seed-derived visual evidence, excluding a bare seed label where applicable. For Challenge, this is the actual serialized gameplay-frame record signature; for Visual Loop, the deterministic family variation/palette/authoring visual parameters and timing; for Visual Drill, the seed-derived trajectory and motion parameters with direct seed/version labels removed.

The runner requires the visual-state digest to change between base and gameplay-seed-only requests in all three content types. For Visual Loop, the nested grammar-parameter evidence and complete in-memory composite hashes are included; the hashes must remain unchanged when only music seed, `variation_index`, delivery profile identity or editorial title changes, while canonical request-binding identity changes.

These relations still require execution against real Godot 4.7.1. The Python test intentionally mocks the subprocess, proving Python contract behavior only.

## 4. Strict envelope and receipts

Input envelope has exact keys and is constrained by JSON Schema Draft 2020-12 to the fixed selector matrix, seed domains, `social_default_v1`, and four non-Longform delivery IDs. Unknown keys, unsupported selectors, `LONGFORM_1080` and unapproved presentation profiles fail closed.

The Python runner reuses the existing D9.9 canonical universal-request evaluator, D9.10 editorial bridge, D-owned adapter and request-scoped binding, then passes only the canonical envelope fields to Godot. It verifies the summary, strict in-memory receipt schema, source lineage pins (46 total after adding the output-schema and frozen grammar/prototype source identities; frozen C11-C manifest first), and nested binding digest. Receipts are printed to stdout, not persisted.

## 5. Safety / governance boundary

- No edits to C11-C or frozen source files.
- Challenge source JSON is read and hash-checked, deep-copied in memory, and the request seed is applied only to the copy.
- No use of `winning_frame` or `close_calls` as timing; simulation telemetry is excluded.
- No delivery resampling, coordinate projection, visual-region policy, editorial visual consumption, audio/music rendering, renderer-native input, renderer dispatch or media output.
- `music_seed` stays outside visual-state generation; `variation_index` remains metadata only; delivery-profile identity does not apply geometric/timing transforms.
- Existing editorial carrier still has 14/14 canonical values hash-bound and 0/14 visually consumed. The composite grammar instance is not editorial visual consumption.
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

Required final summary includes `cases=10`, `selector_types=3/3`, `gameplay_seed_binding=3/3`, `orthogonality=4/4`, `loop_grammar_instance=HARMONIC_MEMBRANE_COMPOSITE_MATERIALIZED`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`. The runtime must provide valid `grammar_parameter_evidence` for the Loop case; all four orthogonality variants must preserve visual/payload digests.

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

Review runtime evidence and source/seed relationships before proposing another additive increment. The previously open selector-to-grammar composition gap is now addressed for the single pinned `harmonic_membrane` selector only, pending Windows acceptance of this new composite integration increment. The remaining I/O gaps, exact native renderer input, renderer-visible drawing, delivery/timebase/coordinate projection, and editorial field-to-region/visibility policies are still open. Do not build a visual editor/consumer until the relevant presentation/timing/editorial policies receive explicit approval. This checkpoint does not authorize D4.8, D9.14 full media certification, D9.16, D9.17 closure, D10 closure, renderer baseline approval/freeze, or release.

## 10. Future C11-D promotion/cutover target

The intended end state, only after all C11-D gates are formally closed and a new baseline is explicitly accepted/frozen, is for the accepted C11-D branch and its Producer to replace frozen C11-C as the authoritative working baseline. This is a future target, not current release authority. Until formal D closure, independent baseline approval, freeze and cutover are complete, C11-C 2.19.12 and its manifest remain immutable and authoritative for all existing pins. Do not mutate the C11-C freeze package or promote D from this checkpoint.
