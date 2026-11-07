# C11-E E4B Loop Shared-Service Integration Review — V1

**Date:** 2026-11-07. Review target: V79 Nightly snapshot, never a substitute for live checkout pins.

## Architectural finding

The right integration point is `c11c-suite/c11c-producer/c11e_production_service.py`, the existing shared GUI/CLI E1 service. The GUI had been building D9.10 bridge/envelope records separately after E1 preparation, while the CLI already uses the D9 universal Producer CLI for its own D9.10 plan route. A parallel binder or another Producer would duplicate orchestration and create parity drift.

## V1 boundary

For `visual_loops`, the shared E service now:

1. Revalidates the exact five operator policy decisions and their proposal file hashes.
2. Resolves D9.9 canonical request and plan.
3. Builds the existing D9.10 planning bridge record and D-only adapter envelope.
4. Builds the existing D-owned Loop family-stage contract.
5. Verifies every self-hash and cross-link among canonical request, bridge, envelope and family-stage contract.
6. Adds all relevant D sources, policy proposals and selected family launcher to E source identity pins.
7. Adds an immutable in-intent boundary record and binds its identities into the E intent hash.
8. Returns `schema_version=1.2` for Loop; Challenge/Drill keep the existing 1.1 shape.

The GUI reads the Loop preparation from E1's returned intent. Its separate-process E CLI parity record compares `d9_boundary_preparation` exactly. The CLI naturally returns the same nested object because it calls the same service. Non-Loop GUI bridge behavior is unchanged.

## Selector and seed contract

Local tests prepare all 27 explicit grammars across five Loop families. Each contract carries family/grammar identity and the canonical family launcher. The prepared argument vector contains `-NoSound`, `request.seed`, grammar, a fresh isolated output-root placeholder and request tag. It never forwards `request.music_seed` to the visual launcher. `music_seed` remains separately recorded in the family stage and E music contract as `PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH`.

## Fail-closed and source changes

Exactly six existing D/E source/test files are replaced only after exact V79 preimage SHA checks and immutable backups:

- shared E service;
- Producer GUI orchestration;
- E service tests;
- D9.8 model JSON;
- D9.8 resolver;
- D9.8 focused test.

No D9.9 request schema, CLI implementation, D9.10 contract, C11-C generator, family launcher, family music generator or frozen manifest is modified.

## Test evidence in isolated V79 snapshot workspace

- `test_c11e_production_service`: 25/25 PASS, including all 27 selectors, GUI/CLI semantic equality, repeated preparation, tamper rejection and no-dispatch locks.
- D9.8 model test: PASS; negative 25/25.
- Python `compile()` in-memory for the five changed Python source/test files: PASS; no bytecode files are written by the Windows runner.
- A separate read-only D baseline candidate diagnostic is included; V79 archive preflight is blocked by three missing `.githooks` manifest paths, to be rechecked on the live checkout.
- The V2 V2 audit test is not replayed after source hashes intentionally change; its previous live Windows PASS remains historical evidence. New runner verifies V80 source postimages.

## Deliberately not implemented

- No request-scoped payload materialization or receipt.
- No actual compositor frame consumer; `family_adapter=NOT_CONNECTED_E1` remains true.
- No Godot launcher, renderer, FFmpeg, audio generator, mux or media output.
- No visual/human acceptance, release or promotion.

## Exit criteria for next stage

First validate this exact patch in live Windows PS 5.1/Python 3.13. Then implement and test a receipt-bound request-scoped payload materializer for each of 27 selectors, preserving actual frame count/FPS/duration and the silent visual seed boundary. Only after the independent D renderer baseline and D4.8 authorization may five family pilots be rendered and reviewed.
