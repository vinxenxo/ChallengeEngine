# C11-D — Visual Loop Composite Payload Integration Checkpoint V1

**State:** `PREPARATION_ONLY_COMPOSITE_PAYLOAD_READY_FOR_WINDOWS_ACCEPTANCE`

**Scope:** the existing dynamic request→payload binder now assembles the single admitted Visual Loop selector `visual_loops / c11c_geometric_waves_v1 / harmonic_membrane` as a deterministic, in-memory composite. The composite contains the existing family-level authoring envelope plus the request-bound 20-parameter grammar instance produced from the frozen C11-C geometric variation profile.

## Exact composition contract

- Selector fixed to `c11c_geometric_waves_v1 / harmonic_membrane`, grammar index `0`, shader branch `field_harmonic_membrane`, uniform `grammar_mode`. Other grammar selectors remain rejected.
- Nested member path is `grammar_parameter_instance`; `style_parameter_count=20`; source alias `glow` is mapped to the style key `glow_strength`. Style and instance digests are included in the D-owned payload and separately returned as `grammar_parameter_evidence`.
- Existing `VisualLoopAuthoringAdapter` still emits the family envelope subtype `geometric` and is not grammar-aware. This increment does not modify it or any frozen C11-C source.
- Gameplay seed affects the visual state; music seed, variation index, delivery-profile identity and editorial title must not affect Loop payload/visual-state digests. Request binding identities still differ when request metadata changes.

## What PASS means — and does not mean

PASS means the exact selector-specific **D-owned in-memory review composite** is hash-bound and deterministic for this one pinned selector. It does not mean the family adapter became grammar-aware, that a `ShaderMaterial`/renderer was instantiated, that a shader branch executed, that renderer-native input was emitted, that any pixels/video were produced, or that the full candidate I/O contract is complete.

Expected governance stays `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, candidate input inadmissible, video render readiness false. Editorial visual consumption stays `NOT_APPLIED`; the prior 14/14 values remain 0/14 visually consumed. Field-to-region/visibility, timebase/delivery projection, coordinates, audio and native renderer-input policy are not approved by this work.

## Files changed in this increment

- Dynamic request→payload in-memory Godot harness and Python strict receipt validator/tests.
- Dynamic payload receipt JSON Schema and source-pinned dynamic selector contract.
- Existing Visual Loop Grammar Binding Audit and Grammar Parameter Instance guards/tests updated to distinguish the composite payload from the still-family-level adapter and from the standalone parameter-only probe.
- This checkpoint; all existing frozen C11-C source files and manifest remain unchanged.

## Windows acceptance sequence

From `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, after applying the additive overlay and confirming manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, run each command separately and stop on the first failure:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_dynamic_request_payload_binding.py
python -B .\tools\c11d\d9\test_d_renderer_visual_loop_grammar_binding_audit.py
python -B .\tools\c11d\d9\test_d_renderer_visual_loop_grammar_parameter_instance.py
python -B .\tools\c11d\d9\d_renderer_dynamic_request_payload_binding.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120
python -B .\tools\c11d\d9\d_renderer_visual_loop_grammar_binding_audit.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120
python -B .\tools\c11d\d9\d_renderer_visual_loop_grammar_parameter_instance.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120
python -B .\tools\c11d\d9\d_renderer_candidate_io_gap_audit.py
python -B .\tools\c11d\d9\d_renderer_candidate_identity_inventory.py --no-godot-version-probe
```

The dynamic runner must report `loop_grammar_instance=HARMONIC_MEMBRANE_COMPOSITE_MATERIALIZED`; its ten-case matrix must confirm the selector types, seed binding and orthogonality. Audit and parameter-instance standalone receipts may continue to report their own `exact_selector_payload_materialized=false`: they are not the composite payload. The overall I/O report is expected to keep 0/10 complete, 6 partial and 4 blocked until further contracts close real I/O groups.

These are focused checks, not complete D baseline acceptance. Re-run lifecycle and baseline preflight separately in the active Windows checkout, where operator ledgers exist; do not claim preflight acceptance from a context export that omits them. Keep new tests out of the aggregate until Windows acceptance is confirmed.

## Later baseline replacement intent

Once **all** C11-D gates are closed and its baseline is separately approved, frozen and promoted, C11-D is intended to replace frozen C11-C as the new authoritative baseline and Producer. This checkpoint grants no promotion, release or freeze authority. C11-C 2.19.12 and its manifest remain immutable until that formal cutover.
