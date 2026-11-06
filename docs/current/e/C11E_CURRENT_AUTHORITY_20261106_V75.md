# C11-E Current Authority — V75

**Date:** 2026-11-06. Supersedes V74. Full E4A Challenge remains closed `PASS_TEST_ONLY`. E4B Loop has accepted its populated GUI plan-only evidence and active-checkout V1 overlay/structural CLI run. The V1 CLI output is not accepted for populated editorial parity because PowerShell 5.1 mis-decoded Spanish literals. A corrected V2 runner now derives the CLI request from the existing GUI UTF-8 export and verifies all four exact values plus the D9.8 editorial hash. No GUI rerun is required. This V2 runner still requires execution in the active Windows checkout.

## Authority and immutable baseline

The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is the sole code authority. ZIPs are evidence/read-only snapshots; never extract them over the checkout. Operator manages commits. No runner may invoke Git, inspect HEAD/status/branch, require `.git`, or compare commit IDs. Use SHA-256 source pins and the frozen C11-C manifest only.

C11-C 2.19.12 remains immutable. `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## E4A Challenge — closed

Full E4A: `PASS_TEST_ONLY`. E4A.6 visual/user review PASS; E4A.7 independently audited A/V PASS (267/267 hashes, A/B repeatability, C seed difference, unchanged H.264, AAC-LC mux, 15 s/450 frames/0.000 s drift); operator listening A/B/C PASS. D99 V2 source patch applied/tested: active `main.py` postimage SHA `4141072659f307468900c1cfb09774479abc6c10abae6`; focused test SHA `872bfd49a99b289b1980feb06d38e44dc55766818fe344fcf3678bcc7d3f325d`; E1 19/19; D9.9 matrix and focused tests PASS. `D99-GUI-37559C528640.zip` audited PASS for populated GUI/E1/D9.9/D9.10 parity and D9.13 lifecycle 5/5. Do not repeat E4A absent concrete regression.

## E4B Loop — evidence ledger

### Accepted

- E4B docs overlay V1: run `20261106T120504Z-7FACC95E`; PS 5.1 AST PASS; 20 source pins PASS; 12/12 documentation files installed add-only; no code source change or media.
- E4B Step overlay V1: run `20261106T201250Z-1F9D8AB7`; PS 5.1 AST PASS; 27 source pins PASS; 17/17 payload files verified and added; no pre-existing source file modified; C11-C frozen manifest PASS; renderer/media OFF.
- Populated Producer GUI evidence `D99-GUI-439FD530F839.zip`: 19,789 bytes, SHA-256 `b933deefcf32764b9817641bd990c2879525e2931be5cbcf3cfa357574b6792f`. Four fields have exact NFC Spanish values: title `Título editorial Loop — composición armónica en movimiento`; subtitle `Explora el patrón geométrico, observa sus ciclos y descubre cómo evoluciona la forma`; CTA `Guarda este loop y comparte tu patrón favorito`; language `es`. GUI editorial hash `283e63025fa1a4e6f185a33d81f5a3c40a6defa4a047b9b7e089f5a159a2c214`. Internal GUI/E1/D9.9/D9.10 parity PASS; D9.13 five lifecycle surfaces PASS_PLAN_ONLY. Adapter remains prepare-only; renderer/dispatch/media false; D4.8 BLOCKED; release NONE.
- Active-checkout CLI V1 run `20261106T201324Z-B8D4F7C4`: 27 pins PASS; proposal tests actually 17/17; D9.9/E1 CLI exits 0; four fields structurally present. This is accepted only as structural CLI smoke, not populated-value parity.

### V1 Unicode defect — populated parity NOT accepted

The uploaded `e4b_loop_overlay_cli.zip` (17,927 bytes; SHA-256 `5402a3297991958cdb21a547fd21ef8f00e2a43303e334e734df1f2fe4e2a747`; CRC PASS) contains mojibake such as `TÃ­tulo`, `composiciÃ³n` and `patrÃ³n`. The source `.ps1` had non-ASCII literals in UTF-8 without BOM; Windows PowerShell 5.1 decoded them through the ANSI code page. The runner's expected strings were corrupted the same way, making its self-comparison ineffective. Its PASS is therefore not populated GUI/CLI parity evidence.

### Corrected V2

The V2 runner is ASCII-only. Its Python 3.13 helper reads `D99-GUI-439FD530F839/request.json` as UTF-8, validates exact expected values/NFC/no-mojibake and the GUI canonical request, plan, bridge, adapter, E1 receipt and lifecycle evidence. It clones that GUI request, changes only request ID and provenance to CLI, writes UTF-8 JSON, then feeds the same raw CLI JSON to D9.9 CLI and E1 CLI. It requires:

- all four editorial values equal GUI exactly;
- the D9.8 `editorial_hash` equal GUI;
- D9/E1 request and plan identities equal within the CLI run;
- separate gameplay/music seed domains and original `music_seed` value;
- family music route preserved and no engine/mux invocation;
- renderer, renderer input/dispatch, production, media false; D4.8 BLOCKED; release NONE.

A diagnostic run in the assistant sandbox against a read-only V70 snapshot completed D9.9/E1 and produced the same GUI editorial hash `283e630...`. This is not a Windows checkout receipt. The active Windows V2 run is still required. Existing GUI evidence is reused; do not rerun GUI.

## E4B Loop technical boundary

- Five C11-C families and 27 grammars are fixed: 5/5/5/5/7. Existing scenes, binders, timelines, Matrix, RNG, native text/metrics/palette and family music remain protected.
- The five Loop prototype scenes already mount `C11CVisualEditorialLayer`. Do not alter it to introduce D editorial. The C11-C-native header/footer/Matrix carry grammar and telemetry; a D consumer must preserve the entire source frame.
- D9.8 Loop has exactly four keys: `title`, `subtitle`, `call_to_action`, `language`. GUI and D9 resolve them. E1 properly reports `NOT_CONSUMED_E1`, family adapter `NOT_CONNECTED_E1`, required gate E4. This is the planned integration boundary, not a GUI defect.
- The D outer-band candidate remains `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`: 720x1280 canvas, top/bottom bands 192px, contained source viewport 504x896 at (108,192), uniform scale 0.7. This preserves all source pixels geometrically; it does not prove text shaping, glyph coverage, wrap, mobile readability or Godot implementation. No renderer input may be emitted from this candidate yet.
- Existing family music remains protected. Future D orchestration must use `request.seed` for silent visual output and `request.music_seed` for the existing C11-C family-music generator, preserve family/profile/grammar/cycle/duration, then mux by H.264 stream-copy. Do not edit C11-C generators or use D3 V5 for Loop.
- Historical Loop composite-payload checkpoint is preparation-only and does not prove an editorial visual consumer/field-to-region contract exists.

## Immediate ordered work

1. Install `C11E_E4B_LOOP_CLI_PARITY_V2.zip` add-only (18 payload files: 15 versioned documents + 3 Python/PowerShell runner files). V2 preflights 30 existing source pins and C11-C manifest; the installed runner then verifies 32 pins including itself/helper/test.
2. Run `tools/c11d/d9/RUN_C11E_E4B_LOOP_CLI_GUI_PARITY_V2.ps1` against the existing local GUI evidence directory `artifacts/tests/c11d_d9/producer_universal/D99-GUI-439FD530F839`. Do not rerun Producer GUI. Use `-GuiEvidenceRoot` if the extracted directory differs.
3. Accept populated GUI/CLI parity only after V2 Windows receipt is `PASS_GUI_CLI_EDITORIAL_PARITY_ONLY`, all four Unicode values and editorial hash match, and governance checks pass.
4. Then review the outer-band composition decision against C11-C full-frame visibility, social readability and font support. It remains not approved. Keep proposal inputs non-renderable until explicit acceptance and separate renderer authorization.
5. After composition policy approval, implement a D-owned Loop consumer at the existing D boundary only. No parallel binder/Producer and no changes to C11-C shared layer, family scenes, binders, timelines, Matrix, RNG or music generator.
6. Prove five-family/27-grammar behavior, visual `request.seed` isolation, family music `request.music_seed` isolation, H.264 stream-copy, GUI/CLI, A/V checks and operator review. E4B closes only after all required gates.
7. E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8.

## Permanent governance

`renderer=OFF`; production dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No C11-C edits, sixth module, parallel Producer/binder or Git invocation in runners.
