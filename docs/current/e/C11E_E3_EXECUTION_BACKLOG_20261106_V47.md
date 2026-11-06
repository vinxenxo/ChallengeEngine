# C11-E Execution Backlog — V47

**Date:** 2026-11-06. E4A Challenge is closed `PASS_TEST_ONLY`. E4B Visual Loop is opened in read-only source/contract audit; no Loop render or media was run.

## Completed: full E4A Challenge

- E4A.6 visual/reserved bands: PASS_TEST_ONLY; user visual review PASS. Silent D-composited H.264 SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`.
- E4A.7 A/V: PASS_TEST_ONLY independently audited; worker ZIP `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`; receipt `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`; report `efb0f1a9245d3fce15bf48041c8972e90f6874d308fa99340afb5c731f94403a`; 267/267 files. Human listening A/B/C explicitly PASS.
- D99 V2: source `main.py` postimage `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6`; focus test `872bfd49a99b289b1980feb06d38e44dc55766818fe344fcf3678bcc7d3f325d`; E1 19/19, D9.9 and GUI regression preflights PASS; 14 documents installed.
- Manual Producer `D99-GUI-37559C528640`: E1 GUI/CLI parity PASS, D9 plan/bridge/adapter parity PASS, D9.13 lifecycle 5/5, renderer/dispatch/media false, release NONE.

Do not rerun any E4A.6/E4A.7 visual/audio/listening step without an evidenced regression.

## E4B P0 — one manual Loop plan-only GUI/CLI run

Use the existing Producer tab `C11-D · EDITORIAL UNIVERSAL (D9.9)`. Exact fixture and receipt requirements are in `C11E_E4B_LOOP_GUI_CLI_PARITY_PLAN_20261106_V1.md`. This run validates request/plan/bridge parity only. It must not call Godot, C11C family render runners, C11CSafeAmbient, FFmpeg, D3 V5, D9.14, E3, or any media dispatch.

Required first selector: `visual_loops` / `c11c_geometric_waves_v1` / `harmonic_membrane`. Keep `mode=REVIEW`, delivery `REVIEW_720`, presentation `social_default_v1`, variation 0, audio enabled true (plan metadata only), gameplay seed 314159 and music seed 840001 (test fixtures, not product defaults), personalization on, global language `es`; title/subtitle/CTA blank. Four D9.8 keys remain present; blank strings normalize to `UNKNOWN`.

## E4B P1 — resolve visual editorial coexistence, no source patch yet

The five active family scenes already mount `C11CVisualEditorialLayer`; it is not missing. Their animated header/footer already carry C11-C generated grammar/math/technobabble, seed/duration/FPS/loop counts, palette/family-music and family/version identifiers. The existing Loop field-window proposal is unapproved and its full-span HEADER/FOOTER mapping could overwrite native C11-C content. Write and validate a non-destructive D-owned coexistence policy before implementing an adapter. Do not patch the C11C shared layer, scenes, binders or timeline.

## E4B P2 — family music seed separation

C11C family audio remains the owner; no D3 V5 for Loop. Existing family `run_prototype.ps1` scripts currently pass one `$Seed` to both visual rendering and `C11CSafeAmbient.py`. E4B orchestration must run visual capture silent using `request.seed`, invoke `C11CSafeAmbient.py` / `generate_c11c_family_music.py` with `request.music_seed`, selected family, existing mapped profile, loop cycles, duration and exact grammar, then mux audio while stream-copying H.264. This is a D orchestration change; do not alter C11C generator source. Audio disabled must skip generation/mux.

## E4B P3 — isolated family runtime verification

After P0 parity and approved D editorial composition policy, run one isolated representative from each of five families, each under a unique `artifacts/tests/c11e/e4b_loop/<run-id>/...` output root. Use the existing family prototype runners only with `-NoSound` and a unique non-existing `-OutputRoot`/`-OutputTag`; then call the existing family audio wrapper with the separate music seed. Preserve existing family/grammar/timeline/music mappings. Verify authoring JSON, video hashes, music seed binding, family/grammar/profile, mux, FFprobe, A/V drift and no output overwrite. No full Matrix101 or production use here.

## Evidence and blockers

Nine Loop-focused static suites passed 159/159 tests in the V70 snapshot. E1/D9 in-memory Loop plan probe passed identity equality for request, editorial, plan, intent, bridge and adapter. One separate Challenge provenance-join suite has one stale source pin (expected 27,036 bytes / SHA `8f8e4c9b...`; actual V70 `materialize_challenge_visual_payload_in_memory.gd` is 89,712 bytes / SHA `01deb241...`); do not silently reseal it under E4B.

After E4B closes, proceed E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8.

## Governance

C11-C 2.19.12 immutable; manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No sixth module, second Producer, parallel binder, or C11C source changes. Renderer OFF, dispatch/media OFF, D4.8 blocked, D9.10 preparation only, D9.14/D9.16 blocked, D9.17 no-go, D10 blocked, `release_authority=NONE`. No Git.
