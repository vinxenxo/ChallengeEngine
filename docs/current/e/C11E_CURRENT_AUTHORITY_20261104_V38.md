# C11-E Current Authority — V38

**Date:** 2026-11-04. The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is authoritative. ZIPs are evidence or hash-gated overlays only; never extract snapshots over the checkout.

## 1. Accepted and reusable gates

E0/E1, bounded E2 R4, E3.2, E3 Challenge D3 V5/audio-mux pilot and E3 50/50 negative controls remain accepted within their recorded scope. E4A source discovery, GUI contract successor, Gate A assessment and operator-approved Challenge Editorial Policy V1 remain accepted within scope. E4A.1 is accepted only as a neutral-body fixture; it is not a gameplay-pixel test.

## 2. E4A.2 — accepted real gameplay BODY pixel proof

The operator supplied `RUN_20261104_002559_542bcf60.zip`, 7,751,764 bytes, SHA-256 `49736fb268af00bb92868a29b819ad54cc6a4dc011000cae20505ee56e496893`; ZIP CRC is valid and it contains 85 entries.

Windows evidence:
- Status: `PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY`.
- Focused Python tests: 33/33 PASS.
- C11-C base video: SHA-256 `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`; H.264 720×1280, 60fps, 900 frames, 15s, `yuvj420p/pc`, no audio.
- Test-only normalized derivative: SHA-256 `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e`; H.264 720×1280, 30fps, 450 frames, 15s, `yuv420p/tv`, no audio.
- 18/18 PNG at 720×1280; 12/12 comparisons; all 18 BODY crop hashes match within each sample across A/B/C; A/B BODY identity holds at six real delivery samples.
- Title/subtitle changes are confined to HEADER/HOOK; CTA to FOOTER/CTA; B/C produce identical pixels. `player_name`/`challenge_label` remain geometry-blocked; language remains metadata-only.
- Report SHA `e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159`; receipt SHA `b23a5f0c1557b52b724c99ac90a671e0a8d8457dcd5e605f8d097c517f366308`.
- Frozen C11-C manifest remained unchanged.

**Acceptance boundary:** E4A.2 proves real gameplay BODY pixel identity and policy-region confinement at six sampled times only. It does not accept typography, text placement, safe areas, family layout, a full-length D compositor, final media or production dispatch. The montage shows placeholder title/subtitle overlap with the existing C11-C HOOK headline. D1.5 generic safe area and typography remain UNKNOWN. No layout coordinates are inferred from this fixture.

The earlier V1 test harness failure (`yuvj420p/pc` source vs assumed delivery `yuv420p/tv`) remains retained as a harness incident, not a C11-C generator failure. Its later manually typed PASS after throwing is invalid and is not evidence.

## 3. E4A.3 — D-owned Godot compositor test prepared; Windows runtime pending

The next increment reuses the accepted E4A.2 run and normalized MP4. FFmpeg extracts six unmodified still frames only. The existing D-owned `materialize_challenge_visual_payload_in_memory.gd` then runs its explicit isolated E4A config branch: a transparent Godot SubViewport draws the D-owned semantic editorial fields and alpha-composites its layer over the six real C11-C frames, writing 18 test PNGs and 12 comparisons under `artifacts/tests/c11e/e4a_d_compositor_pixel_review/RUN_*`.

It does not rerender C11-C, produce an MP4, dispatch D9.10, invoke a production renderer, create audio, or connect the production Producer button. Six samples are test coverage, not a full-duration compositor acceptance. The text stack uses test-only placeholder typography and placement; `VISUAL_PLACEMENT=UNAPPROVED` remains mandatory.

The source-side preparation now fingerprints only explicit visual `FrameSnapshot` properties (position, rotation, scale, opacity, texture index and variant ID). It does not read or serialize `FrameSnapshot.custom_data`. C11-C sources and the frozen manifest remain untouched.

Prepared source pins:
- D-owned materializer V3 SHA-256 `e925cc319852e9fe79c26f9dd791ff1f43a0d3465ae30159819be5f57fb001e1`.
- E4A.3 Python runner SHA-256 `9d00faf38213ade848f722a72bf0ba6ef102975f43bd9e960648780bf3d2c629`.
- E4A.3 focused tests SHA-256 `b33a158ddd29f1581f86a7d6ceabef4a66a1a5a8a51aaada9b8489c730876973`.
- Preparation tests: 46/46 PASS; Python `py_compile` PASS. Godot 4.7.1 runtime has not been run in this preparation environment; Windows execution and review remain required.

## 4. Immediate next action

Apply `C11E_E4A_D_GODOT_COMPOSITOR_PIXEL_OVERLAY_V1.zip` with the sidecar SHA. The integrated Windows block must validate all payloads and exact preimages before writes, replace only the pinned materializer, add the runner/tests/docs, run 46 focused tests, then invoke the runner once against the existing E4A.2 directory:

`artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60`

No Godot/C11-C base generation rerun is expected. Capture native exit codes and upload the complete new E4A.3 `RUN_*` ZIP. A nonzero exit means FAIL; no success marker may be printed afterward.

## 5. Next product sequence

E4A.3 bounded Godot-layer proof → E4A.4 test-only A/V using the accepted E3 D3 V5 / FFmpeg mux / FFprobe path and operator visual review → resolve/accept Challenge layout or explicitly keep specific fields blocked → E4A close → E4B Visual Loop → E4C Visual Drill → E5 seed isolation/determinism/profile non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 → E8 historical C11-C corpus reconciliation, independent acceptance, immutable freeze and separate explicit promotion.

Before visual/layout decisions, inspect the actual checkout root `README.md` and all root `README*`, `AGENTS.md`, `.continue/rules/CONTINUE.md`, plus the relevant historical C11-B/C11-C README files and presentation contracts. Historical material is evidence to reconcile against current source, not automatic authority.

## 6. Immutable authority and governance

C11-C 2.19.12 remains the sole production baseline. Frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796,318 bytes. Do not change C11-C generators/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, frozen C presentation/binders, `FrameSnapshot.custom_data`, `core/audio`, D3 V5, E1 service or the manifest. No parallel producer/binder, sixth module or `c11d-control`.

Production D renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze or promotion.
