# C11-E Current Authority — V76

**Date:** 2026-11-06. Supersedes V75. Full E4A Challenge is closed `PASS_TEST_ONLY`. E4B populated GUI/CLI parity is now accepted `PASS_TEST_ONLY`; the next E4B increment is a five-family / 27-grammar D9.9→D9.10→D-only adapter→E1 plan-only matrix, with three seed scenarios per grammar. The new GUI action is inside the existing D9.9 Producer tab; the CLI runner replays the GUI matrix template. The GUI entrypoint `main.py` is D-owned and hash-gated from the accepted D99 V2 postimage `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e` to `982bce475811c5e4f9cad2e84b33cee9a3460f6add4f095476e950db15b806ab`. Neither path is a renderer or media test.

## Authority and immutable baseline

The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` remains the sole code authority. ZIPs are evidence/read-only snapshots; never extract them over the checkout. Operator manages commits. No runner may invoke Git, inspect HEAD/status/branch, require `.git`, or compare commit IDs. Use SHA-256 source pins and the frozen C11-C manifest only.

C11-C 2.19.12 remains immutable. `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## E4A Challenge — closed

Full E4A: `PASS_TEST_ONLY`. E4A.6 visual/user review PASS; E4A.7 independently audited A/V PASS (267/267 hashes, A/B repeatability, C seed difference, unchanged H.264, AAC-LC mux, 15 s/450 frames/0.000 s drift); operator listening A/B/C PASS. D99 V2 source correction and manual GUI/E1/D9.9 parity PASS. Do not repeat E4A absent a concrete regression.

## E4B Loop — accepted subgates

- E4B populated GUI evidence `D99-GUI-439FD530F839.zip`: SHA-256 `b933deefcf32764b9817641bd990c2879525e2931be5cbcf3cfa357574b6792f`; four exact NFC values; editorial hash `283e63025fa1a4e6f185a33d81f5a3c40a6defa4a047b9b7e089f5a159a2c214`.
- E4B CLI/GUI parity V2 evidence `20261106T204002Z-CF365847.zip`: SHA-256 `f81d384a3ffc6af7367c6a3eaea9db6cde51394e7539bdf13a52756fcc7079b9`; 32/32 source pins; static proposal tests 17/17; Unicode helper tests 5/5; D9.9 CLI and E1 CLI PASS; GUI/CLI editorial hash equal; all locks retained.
- The previous CLI V1 remains structural-only because PowerShell 5.1 decoded Spanish literals as mojibake. V2 resolves this by using UTF-8 GUI evidence; do not rerun V1 or repeat the populated parity fixture.
- E4B composition remains `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`; geometry 720x1280 with 192px bands and a contained 504x896 source viewport is only arithmetic proposal, not a visual acceptance.

## E4B full-family matrix — current increment

A D-owned verification helper now enumerates the live C11-C Producer schema and tests every concrete Loop grammar:

- Geometric Waves 5; Fractal Bloom 5; Sacred Symmetry 5; Living Particles 5; Invisible Forces 7.
- Three cases per selector: baseline, gameplay-seed-only change, music-seed-only change (81 total).
- Each case exercises canonical D9.9, D9.10 bridge planning, D-only adapter envelope and E1 intent preparation. It verifies four editorial keys, family/profile mapping, seed separation, deterministic repeat, the preserved C11-C family music route, and fail-closed governance.
- GUI and CLI call the same D-owned helper. The existing Producer D9.9 tab gains one diagnostic button; no new Producer, tab surface or binder is introduced. CLI replays the exact GUI-exported matrix template and compares all 81 selector/scenario editorial identities.
- Staging workspace verification: 13/13 focused tests PASS (including GUI entrypoint source checks); 27 selectors × 3 scenarios = 81/81 D9.9/D9.10/E1 cases PASS; GUI/CLI matrix comparison 81/81 PASS. This is preparation-tree evidence only. Windows GUI and CLI acceptance are still pending.

The matrix is **not** visual-payload materialization: it does not invoke Godot, C11-C visual prototypes, C11-C family music generator, D3 V5, FFmpeg, renderer, dispatch or media. E1 correctly leaves Loop fields `NOT_CONSUMED_E1`, family adapter `NOT_CONNECTED_E1`, gate E4.

## Historical D boundary — do not bypass

The accepted D exact-selector Godot composite checkpoint covers only the five Geometric Waves grammars, in-memory, with `renderer_inputs_emitted=0/5`; it does not admit four other families or all 27 grammars. Historical D request-bound timing/review, editorial field-window and approval gates remain separate. The 19/19 approvals recorded in the exact-selector checkpoint were still 0 granted. Do not remove old selector guards or infer renderer eligibility from this E4B plan-only matrix.

The D9.8 model still reports Loop `request_plan_compatible=false` / `PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER`. The current D9.9 evaluator nevertheless resolves the supported `visual_loops` selection into `UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY`; the matrix records that exact plan kind and does not claim a D4 executable subplan or renderer compatibility. Do not silently rewrite the D9.8 metadata flag in this increment.

## Ordered E4B work

1. Install `C11E_E4B_LOOP_FAMILY_MATRIX_V1.zip`; the installer pins 31 existing supporting source pins, including the frozen manifest, accepts only the D99 V2 `main.py` postimage as preimage, and patches only the D-owned Producer entrypoint. It adds 15 new versioned documents, three tools, and the new GUI action. C11-C source and manifest stay immutable.
2. Run the new button in the existing `C11-D · EDITORIAL UNIVERSAL (D9.9)` tab with Visual Loop / REVIEW / audio ON / personalization ON / two distinct seeds. It exercises all 27 grammars and writes `matrix_request_template.json`, `matrix_request_template.sha256`, `matrix_report.json` and `matrix_report.sha256`.
3. Run `tools/c11d/d9/RUN_C11E_E4B_LOOP_FAMILY_MATRIX_V1.ps1 -GuiEvidenceRoot <GUI matrix folder>`. It replays the GUI template through the same canonical D9.9/D9.10/E1 service and requires 81/81 GUI/CLI parity rows.
4. Audit both receipts, then resolve the outstanding presentation field-window/timing approval boundary and family-specific D payload binding scope. Only after those policy gates are approved may the D-only visual consumer be implemented.
5. Then perform isolated silent visual + existing family music seed split + H.264 stream-copy mux, A/V validation and human review, with independently authorized test execution.
6. E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8.

## Permanent governance

`renderer=OFF`; production dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No protected C11-C mechanics, generators, binders, timelines, Matrix, RNG, shared presentation, core audio or manifest changes. No sixth GUI surface, parallel Producer or binder.
