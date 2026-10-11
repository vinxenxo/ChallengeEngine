## Superseding next-step update — fixed-fixture request-scoped binding (2026-10-11)

The immediate next step below has been implemented as a bounded proposal in `D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_CHECKPOINT_V1.md`. It joins only the three fixed D9.9 review requests to the existing in-memory payload harness digests. This does not change this I/O contract's proposal status or make candidate input admissible. Obtain a real Godot 4.7.1 Windows run of both harnesses through the new console-only runner before considering dynamic request transport. Editorial-value consumption, temporal/sample and coordinate semantics, audio/mux/QA and every approval gate remain unresolved. Renderer stays OFF; no media or release authority is granted.

# D Renderer Candidate I/O Contract V1 — Checkpoint

**State:** `PREPARATION_ONLY_INTERFACE_PROPOSAL_NOT_IMPLEMENTED_NOT_APPROVED`  
**Date:** 2026-10-11  
**Scope:** C11-D only. This checkpoint defines prospective input/output interface schemas. It does not implement a renderer or emit an input/output instance.

## Why this increment exists

The source-pinned review confirmed three separate upstream preparation artifacts:

1. `D_RENDERER_CANDIDATE_BINDING_PREVIEW_V1` — inspectable D9.10 binding metadata.
2. `D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1` — deterministic semantic text composition.
3. `D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1` — ordered declarative text bindings with no frame schedule or pixel geometry.

None of these is a renderer-native input, and none defines the complete future renderer I/O boundary. They must not be merged into an implicit dispatch path. The new contract defines the prospective boundary and its admission requirements without producing a runnable payload.

## New files

- `definitions/c11d/production/D_RENDERER_CANDIDATE_IO_CONTRACT_V1.json` — versioned interface and source-pinned requirement contract.
- `definitions/c11d/production/D_RENDERER_CANDIDATE_IO_CONTRACT_SCHEMA_V1.json` — strict Draft 2020-12 schema for the contract document.
- `definitions/c11d/production/D_RENDERER_CANDIDATE_INPUT_SCHEMA_V1.json` — strict prospective input schema, usable only after all applicable policies and authorization gates pass.
- `definitions/c11d/production/D_RENDERER_CANDIDATE_OUTPUT_MANIFEST_SCHEMA_V1.json` — strict prospective output manifest schema for a completed, QA-passing run.
- `tools/c11d/d9/test_d_renderer_candidate_io_contract.py` — read-only source-pin, schema, governance-lock and negative validation.

## Interface contents

The prospective input requires source lineage from D9.9/D9.10 through the frame program, a request-specific hash-bound payload instance, separate gameplay/music seed domains, explicitly approved editorial/presentation/timebase/sample/coordinate/audio policies, a resolved delivery profile, and both renderer-baseline approval/freeze and the explicit D4.8 authorization.

The prospective output manifest records input/source lineage, renderer contract/implementation/build identity, resolved profile and policy hashes, separate video/audio/final-mux hashes and sizes, video/audio/visual/replay/provenance QA reports, decoded-output determinism fingerprints, Catalog identity/provenance and an explicit `release_authority=NONE` state. Audio may be present or explicitly disabled only under an approved policy; enabled audio must pass decode and loudness/peak/mobile QA.

## Current admission and governance state

The candidate input is **not admissible**. A later fixed-fixture checkpoint joins three representative canonical D9.9 requests to existing in-memory payload digests, but dynamic/arbitrary request transport and full editorial-value consumption are not established. Presentation regions, delivery timebase, Challenge sample/time alignment, coordinate composition/projection, editorial field windows and audio/music delivery remain proposals. The D renderer implementation and independent renderer-baseline approval are absent, and D4.8 remains blocked.

No input instance, output manifest instance, artifact path, renderer implementation, dispatcher, media file or approval checkpoint is created by this increment. C11-C 2.19.12 and its manifest remain immutable (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9 remains open and D10 remains blocked.

## Verification in the preparation copy

```text
C11-D RENDERER CANDIDATE I/O CONTRACT PASS | source_pins=30/30 | schemas=3/3 | schema_validation=DRAFT202012_VALIDATED | schema_fixtures=2/2
fail_closed_negatives=13/13 | schema_instance_negatives=8/8 | candidate_input_admissible=false | renderer_input_emitted=false | renderer_dispatch_invoked=false | media_created=false | D4.8=BLOCKED | release_authority=NONE
```

Also rerun after this change:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_candidate_io_contract.py
python -B .\tools\c11d\d9\test_d_renderer_frame_program.py
python -B .\tools\c11d\d9\test_d_renderer_logical_composition.py
python -B .\tools\c11d\d9\test_d_renderer_candidate.py
```

These commands are static/Python contract checks, not a Godot renderer run or release acceptance. The source archive used for this isolated design test omits some operator-runtime ledgers and contains a duplicate ZIP member for the historical freeze manifest; do not extract that full archive over the active Windows checkout. Operator-confirmed Windows lifecycle and candidate-preflight results from 2026-10-11 remain the accepted evidence for that checkout.

## Next step

Review this interface proposal independently and confirm the exact field-level contract. After that, proceed with the smallest D-only implementation that remains non-dispatching: request-specific payload materialization/binding must supply a real hash-bound instance for each supported content type without inventing unresolved temporal, coordinate, editorial or audio behavior. Do not create an input instance until all required dependencies and approval gates are satisfied. Do not implement or invoke the renderer until the separately approved/frozen D renderer baseline and D4.8 authorization exist.

## Regression reconciliation included in this increment

The pinned source in the inspected package is the byte-exact timebase proposal at SHA-256 `251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019`. Several downstream audio/unified-review lineage pins still referenced a different timebase digest; after reconciling the audio contract's timebase digest, its physical contract SHA-256 became `f6fac5edf88269885c18d9b8272214f28d8bb3569cc4da249d2d67c727dac0a8`. The unified-review contract, schema, and implementation pins now reference that exact audio-policy contract digest. The timebase negative test now snapshots and restores the contract as raw bytes, with an equality assertion after restoration, so running the test cannot alter pinned newline bytes.

Verified in this preparation copy after that repair:

- I/O contract: source pins 30/30; schemas 3/3; synthetic in-memory schema fixtures 2/2; fail-closed negatives 13/13 under full Draft 2020-12 validation. Forced `C11D_FORCE_NO_JSONSCHEMA=1` fallback also PASS with structural-only validation, static negatives 5/5 and schema fixtures explicitly not run.
- Delivery timebase: 13/13; exact source file hash remains `251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019` before and after its test.
- Audio/music delivery: 14/14.
- Unified content review: 36/36; cross-checks 17/17; negative 30/30; source lineage 22/22; source files 22/22.
- Presentation-region proposal: 15 tests PASS.
- Existing binding preview, logical composition, neutral frame program, request-scoped payload binding, Loop/Drill payload preview and Challenge payload preview focused tests pass (reported counts are in the current D handover).

These results are from the isolated preparation copy, not from the user's live Windows checkout. No Godot test, Windows GUI/runtime acceptance, renderer dispatch, media creation, aggregate Suite acceptance, or release was performed. The timebase and audio/presentation policies remain proposals; this repair aligns byte-level references and does not approve them.
