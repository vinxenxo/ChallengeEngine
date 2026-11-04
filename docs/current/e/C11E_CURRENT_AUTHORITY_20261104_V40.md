# C11-E Current Authority — V40

**Date:** 2026-11-04  
**Checkout authority:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`  
**Current engineering point:** E4A.3 V2 accepted as an isolated real-body compositor proof; E4A.4 Challenge audiovisual/mux pilot prepared, not yet run.  
**Production authority:** C11-C 2.19.12 remains the sole production baseline.

## 1. Product objective

Deliver one shared C11-E production path for Challenge, Visual Loop and Visual Drill. Preserve existing C11-C visual generators and mechanics. Add the D-owned presentation/editorial consumer, family-correct music (D3 V5 for Challenge; preserve existing C11-C family music paths for Loop/Drill), FFmpeg mux, FFprobe/audio QA, independent gameplay/music seed domains, and GUI/CLI parity through the existing shared E1 service. No second producer, parallel binder, sixth suite module or `c11d-control`.

## 2. Immutable authority and governance

C11-C 2.19.12 remains production authority. `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: **796,318 bytes**, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Protected boundaries remain unchanged: no edits to C11-C generators/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, `core/audio`, D3 V5 engine, E1 service, historical C11-C presentation/binders or frozen manifest.

Governance remains locked: production renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze, promotion or production dispatch.

## 3. Accepted evidence carried forward

### E4A.2 — real C11-C BODY reference

Accepted bounded evidence `RUN_20261104_002559_542bcf60`:
- Evidence ZIP SHA-256: `49736fb268af00bb92868a29b819ad54cc6a4dc011000cae20505ee56e496893`.
- Receipt SHA-256: `b23a5f0c1557b52b724c99ac90a671e0a8d8457dcd5e605f8d097c517f366308`.
- Report SHA-256: `e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159`.
- Normalized, test-only CHALLENGE_004 review MP4 SHA-256: `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e` (H.264, 720x1280, 30 FPS, 450 frames, 15 seconds, `yuv420p`, no audio).
- Six real delivery samples and all BODY comparison checks passed. This is a reference artifact, not a production output.

### E4A.3 V2 — D-owned Godot compositor

Accepted bounded evidence `RUN_20261104_021444_0cfefef6`:
- Evidence ZIP SHA-256: `75c5b37426eea6e40a41d3daa821fc74a08f69590e569b1080cbc9305ae5db91` (3,247,479 bytes; CRC verified).
- Receipt SHA-256: `3670428feae3b34766677b4cdba3985babecbda9ee781eebe4cc57c318cd9f1c`.
- Report SHA-256: `ee1be803f4d0433347778793aab12228301aea5108f426011836c27dc268dc08`.
- Godot 4.7.1 exited 0 with rendering enabled and not headless. 6/6 real C11-C frame extracts, 18/18 compositor PNGs and 12/12 pixel comparisons passed. BODY pixels remain identical at all six sampled delivery times. Frozen C11-C manifest stayed unchanged.
- E4A.3 proves an isolated D-owned SubViewport layer alpha-composited over real C11-C frames. It does not produce or approve a full D audiovisual MP4.

### E4A.3 visual disposition — explicitly not approved

The E4A.3 report records `visual_placement_approved=false` and `production_compositor_layout_acceptance=NOT_GRANTED`. The B sample visibly overlaps the existing C11-C hook headline with test title/subtitle; the CTA sample overlaps existing footer CTA. D1.5 generic safe-area insets, typography and CTA geometry remain UNKNOWN. No title/subtitle/CTA layout is accepted for production. `player_name` and `challenge_label` remain blocked on unresolved geometry; `language` is metadata-only.

D1.1 is source mapping only. D1.5 establishes the 540x960 logical canvas with Header 0..144, Body 144..816, Footer 816..960; it does not define generic safe-area padding, typography or CTA geometry. D1.7 inherits the layout and forbids converting UNKNOWN into defaults. Before the next layout proposal, inspect the active checkout's AGENTS/CONTINUE instructions and all relevant historical C11-B/C social-frame and presentation contracts; do not improvise dimensions or font metrics.

## 4. E4A.4 — next bounded physical test (prepared, not run)

Overlay `C11E_E4A4_CHALLENGE_AUDIO_MUX_OVERLAY_V1.zip` adds only a D9-side test runner, its focused contract tests and versioned documentation. It does not replace existing source files. The runner:

1. Revalidates the exact E4A.2 and E4A.3 receipt/report/video hashes and all E1/D9/D3/E3 source pins.
2. Reuses the accepted normalized CHALLENGE_004 15-second MP4 unchanged. No gameplay rerender and no renderer invocation.
3. Prepares three E1 intents through the existing shared service (`request_origin=TEST`, `audio_enabled=true`), validates all three, and retains independent seed domains: gameplay seed `314159`; music A/B `840001`; changed-seed control C `840002`.
4. Invokes the pinned D3 Music V5 engine only for test audio. A/B use the same request; C changes only `request.music_seed`. Tempo 104 BPM remains the historical D9.2 pilot fixture, not a product default. Duration is derived from FFprobe's 450 frames / 30 FPS.
5. Reuses E3's pinned D3.3 mastering, FFmpeg, FFprobe, stream identity and decoded-audio QA helpers. It requires deterministic A/B audio, changed-seed C audio, unchanged H.264 video, exactly one H.264 720x1280/30fps/450-frame stream and one AAC 48kHz stereo stream, non-silence and A/V start/end drift <=0.15 seconds.
6. Emits isolated test MP4s, raw WAVs, 30-second mastering windows, delivery masters, command logs, a report/receipt and an evidence ZIP.

**Important scope boundary:** E4A.4 MP4s contain the accepted E4A.2 C11-C review video plus D3 audio. The E4A.3 overlay PNGs are separate samples and are not embedded. This deliberately tests D3/mux/A/V sync without claiming that the unresolved D layout is ready. Operator video/audio listening review remains pending until the Windows evidence is inspected.

Prepared sandbox static validation: E4A.4 runner compiles and the new focused contract suite passes **42/42**. This is not Windows runtime or D3 audio-render acceptance.

## 5. Remaining ordered gates

- E4A.4: run test-only D3 V5 / D3.3 / FFmpeg mux / FFprobe; inspect the returned evidence and capture operator audio/video review. Then close only its bounded scope.
- E4A visual-layout resolution: inspect D1.1/D1.5/D1.7 and historical C11-B/C contracts; resolve header/body/footer collision and safe-area/typography evidence before an integrated D composited audiovisual render. Unknown geometry remains fail-closed.
- E4B: Visual Loop grammar/variant timeline and editorial/layout binding; preserve its existing C11-C music path.
- E4C: Visual Drill phase/END_CTA precedence and editorial/layout binding; preserve its existing C11-C music path.
- E5: cross-family determinism, gameplay/music seed isolation, adapter/profile non-leakage and GUI/CLI parity.
- E6: Smoke18, six audiovisual scenarios per family.
- E7: Matrix101 target = 54 Challenge + 27 Loop + 20 Drill. CH_008/CH_009 remain held because declared duration 11s conflicts with phase sum 12s (3+7+0+2); 99 provisional runnable cases.
- E8: complete row-by-row C11-C historical corpus regression map, independent acceptance, immutable freeze and explicit promotion.

No accepted gate is repeated unless its source/test pins change. E4A.3 V1's Ctrl+C is a consumed failed attempt caused by waiting for rendered frame output in Godot headless mode; V2 corrects this by enabling rendering, adding progress markers and a finite timeout. Do not rerun V1.
