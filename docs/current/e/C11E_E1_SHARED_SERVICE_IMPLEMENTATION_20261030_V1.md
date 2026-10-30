# C11-E E1 — Shared Production Intent Service Implementation V1

Date: 2026-10-30  
Status: `IMPLEMENTED_IN_ISOLATED_VALIDATION_PENDING_ACTIVE_CHECKOUT_ACCEPTANCE`  
Worktree target: `main`  
Expected base HEAD: `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`

## 1. Scope of this increment

This is the first code increment of C11-E E1. It establishes one shared, preparation-only production-intent service inside the existing `c11c-suite/c11c-producer` module. The Producer GUI and the new E1 CLI facade delegate request preparation to that service. The service delegates semantic validation and editorial resolution to the existing canonical D9.9 `evaluate_universal_request` implementation.

The increment does not create a renderer adapter, dispatch a C runner, start Godot or FFmpeg, create media, enable release authority, or change C11-C mechanics. It does not turn D9.10's plan-only bridge/adapter into an execution path.

## 2. Implemented files

- `c11c-suite/c11c-producer/c11e_production_service.py` — shared request resolver, sealed E1 intent, source identities, seed-domain preservation, output collision rejection, and fail-closed validation.
- `c11c-suite/c11c-producer/c11e_production_cli.py` — CLI facade that calls the same service.
- `c11c-suite/c11c-producer/test_c11e_production_service.py` — focused unit/integration tests.
- `c11c-suite/c11c-producer/main.py` — GUI D9.9 workflow delegates to the shared E1 service and compares its semantic intent with the E1 CLI result.
- `c11c-suite/c11c-producer/test_producer_gui_contract.py` — updates the static GUI contract to assert the service delegation while keeping D9.9 as canonical resolver.
- `c11c-suite/c11c-producer/self_test.py` — includes the E1 sources/tests in Producer self-test.
- `c11c-suite/c11c-producer/BUILD_MANIFEST.json` — records the E1 service/CLI/test and current fail-closed status.

## 3. Request identity and seed invariants

The service preserves the D9.9 canonical request, editorial, and plan hashes, and derives a separate E1 semantic intent hash. The semantic hash is independent of the transport origin (`GUI` or `CLI`), while the envelope preserves the origin for provenance.

Gameplay seed remains `request.seed`. Music seed remains `request.music_seed`. The two domains are independently represented, automatic generation and runtime derivation remain disabled, and cross-domain sharing is forbidden.

The selected C11-C Challenge definition is checked against the exact frozen manifest entry. The frozen manifest itself is checked by byte length and SHA-256. D9 implementation sources used by the resolver are pinned to the reviewed E0/E1 capture.

## 4. GUI/CLI parity

The GUI continues to build its existing canonical D9.9 request. It passes that request to `prepare_c11e_production_intent(..., request_origin="GUI", resolver_module=D9_UNIVERSAL)`. The E1 CLI calls the same public service with origin `CLI`.

The GUI compares semantic intent hash, request/editorial/plan hashes, selection, resolved editorial fields, seed domains, origin provenance, and execution boundary. It writes an E1 intent, parity record, and receipt alongside the existing D9 test evidence. D9.9 and D9.10 receipts retain their original schema and meaning.

## 5. Explicit E1 execution boundary

All values remain fail-closed:

- `renderer_input_emitted=false`
- `renderer_dispatch_invoked=false`
- `renderer_activation=false`
- `production_execution=false`
- `media_created=false`
- `D4.8=BLOCKED`
- `release_authority=NONE`

No E1 output directory is created. A request is rejected when its planned E output root already exists; validation also rejects a root that appears after preparation. Overwrite is forbidden. Challenge editorial consumption is deferred to E2. Loop and Drill adapters remain unconnected until E4.

## 6. Isolated validation evidence

The isolated implementation workspace passed:

- Python compilation of the E1 service, CLI, tests, and patched Producer entrypoint.
- C11-E E1 production-intent service: **13/13 tests**.
- Producer test discovery: all discovered Producer tests passed, including GUI contract, D9.13 lifecycle contract, and D9.14 certification-gate contract.
- `c11c-suite/c11c-producer/self_test.py`: PASS, including D9.5.1, D9.9 universal request matrix, D9.10 bridge/adapter and D9.13/D9.14 checks, plus the E1 service tests.

These are isolated-copy results. They are not yet Windows active-checkout acceptance and do not close E1.

## 7. D candidate evaluator compatibility incident

The historical D candidate evaluator was run against the E checkout and stopped with `C11-C source changes outside D extension roots: ['.continue/rules/CONTINUE.md', 'AGENTS.md']`. This is the expected mismatch between the old D evaluator's allowlist and the explicit E0 transition of the two root instruction files. Their exact pre-E guidance is archived under `docs/history/c11d/`; the E0/V3 guidance is archived under `docs/history/c11e/`.

Do not revert the E root instructions and do not change the D evaluator's canonical allowlist. The failure does not mean the four `c11c-suite` integration paths are protected-C drift. C11-E must use a separate reconciliation wrapper that recognizes the exact E-owned root-guidance transition while preserving the historical D evaluator unchanged. No D governance flag, D gate, baseline approval, or release authority is altered by this implementation.

## 8. Active-checkout acceptance still required

After applying the add-only/strict-preimage code overlay to the Windows `main` checkout:

1. Verify the receipt and all final source hashes.
2. Run the Producer self-test and focused GUI/service contracts in the active checkout.
3. Launch the existing Producer GUI and run one D9.9 request. Confirm the E1 tab displays `PASS`, semantic GUI/CLI hashes match, both origins are retained, and no renderer/media is created.
4. Preserve stdout, stderr, exit codes, runtime version, source pins, and receipt hashes.

E1 is not accepted until these active-checkout checks pass. A real MP4 and visual title A/B evidence belong to E2, not E1.
