# C11-E Current Authority — V39

**Date:** 2026-11-04. The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is authoritative. ZIPs are evidence or hash-gated overlays only; never extract snapshots over the checkout.

## 1. Accepted and reusable gates

E0/E1, bounded E2 R4, E3.2, E3 Challenge D3 V5/audio-mux pilot and E3 50/50 negative controls remain accepted within their recorded scope. E4A source discovery, GUI contract successor, Gate A assessment and operator-approved Challenge Editorial Policy V1 remain accepted within scope. E4A.1 remains fixture-only. **E4A.2 is accepted within its limited real-gameplay BODY identity and region-confinement scope.**

## 2. E4A.2 — accepted bounded real-gameplay evidence

Operator evidence: `RUN_20261104_002559_542bcf60.zip`, 7,751,764 bytes, SHA-256 `49736fb268af00bb92868a29b819ad54cc6a4dc011000cae20505ee56e496893`; ZIP CRC valid, 85 entries.

Windows result: 33/33 focused Python tests; 18/18 PNG; 12/12 comparisons; 18/18 body crop hashes; BODY identical across A/B/C at six real delivery samples. Original C11-C MP4 SHA `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de` (`yuvj420p/pc`, 60fps/900, 720×1280, 15s, no audio); test-only normalized derivative SHA `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e` (`yuv420p/tv`, 30fps/450, 720×1280, 15s, no audio). Report SHA `e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159`; receipt SHA `b23a5f0c1557b52b724c99ac90a671e0a8d8457dcd5e605f8d097c517f366308`.

E4A.2 does not approve text placement, safe areas, typography, final layout or production compositor. Placeholder title/subtitle overlap the existing C11-C HOOK headline. D1.5 generic safe area and typography remain UNKNOWN. `player_name`/`challenge_label` stay geometry-blocked; language is metadata-only.

## 3. E4A.3 V1 — harness incident, not a Godot content failure

The operator applied E4A.3 V1; all 46/46 focused Python tests passed. Execution then stalled at the Godot invocation, which V1 built with `--headless` and which awaited `RenderingServer.frame_post_draw` for each SubViewport capture.

**Root cause established:** Godot's official `RenderingServer` documentation states that `--headless` disables all rendering and window management functions and that most RenderingServer functions return dummy values. Waiting for an actual render-completion signal while rendering is disabled is incompatible. The issue is the harness launch mode, not the C11-C MP4 or E4A.2 evidence. See https://docs.godotengine.org/en/latest/classes/class_renderingserver.html and the Viewport capture guidance at https://docs.godotengine.org/en/latest/tutorials/rendering/viewports.html.

V1 has no completed Godot receipt or PASS. Its Python 46/46 is accepted only as static/contract test evidence. If its foreground execution is still active, stop it with Ctrl+C. Preserve its partial `RUN_*` directory; do not repeat V1.

## 4. E4A.3 V2 — corrected execution harness prepared

V2 keeps the exact accepted E4A.2 source run and the same six sample frames. It changes the Godot invocation to a normal renderer-enabled run (no `--headless`), retains the existing D-owned SubViewport materializer, emits a progress heartbeat every five seconds, writes stdout/stderr directly to the evidence directory, and terminates Godot after 90 seconds with logs preserved. The GDScript emits per-sample `BEGIN/DONE` markers and marks the `process_frame` / `frame_post_draw` wait boundaries. No gameplay re-render is invoked.

Current exact hashes:
- Materializer: `3d1c8288ffbea3ff328d785def5fabba250b042c0d2d1b1f94215b1c62cde29b`.
- Runner: `3165f99ddf37252b3ed2fc5becbe98877b0c945d5ef57dcbfb59dd18cc7852f1`.
- Focused tests: `1e51fa2e47339097e6c66354cf2920eccff804d032787d0b268e2bdef2c22300`.
- Preparation tests: 50/50 PASS; Python `py_compile` PASS.

Expected Windows run: 6 extracted base frames, 18 Godot alpha-composited PNGs, 12 comparisons, exact A/background identity, zero BODY changes and explicit test-only layout disposition. Runtime acceptance remains OPEN until Godot exits 0, exact marker/report/receipt are present and hashes are reviewed.

## 5. Immediate next action

1. Stop any still-running V1 PowerShell/Python foreground process with Ctrl+C; do not kill unrelated Godot sessions.
2. Apply `C11E_E4A_D_GODOT_COMPOSITOR_PIXEL_OVERLAY_V2.zip` using its sidecar and exact preimage/postimage hashes.
3. Run 50 focused Python tests.
4. Reuse the accepted E4A.2 path `artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60` and invoke Godot **without `--headless`**. The runner has a 90-second maximum and emits heartbeat/progress.
5. Preserve the complete new `RUN_*` evidence ZIP. Do not rerun C11-C capture.

## 6. Product sequence and historical reconciliation

E4A.3 bounded Godot-layer proof → E4A.4 test-only A/V using accepted E3 D3 V5 / FFmpeg mux / FFprobe and operator visual review → Challenge layout decision or explicit continued field blocks → E4A close → E4B Loop → E4C Drill → E5 seed isolation/determinism/profile non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 → E8 historical C11-C corpus reconciliation, independent acceptance, immutable freeze and separate explicit promotion.

Before any typography/layout decision, inspect the live checkout root `README.md` and every root `README*`, `AGENTS.md`, `.continue/rules/CONTINUE.md`, active D1.1/D1.5/D1.7 and relevant historical C11-B/C READMEs and presentation contracts. Historical content must be reconciled with live sources; do not treat an old convention as automatic authorization.

## 7. Immutable authority and governance

C11-C 2.19.12 remains the sole production baseline. Frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796,318 bytes. Do not change C11-C generators/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, protected presentation/binders, `FrameSnapshot.custom_data`, `core/audio`, D3 V5, E1 service or manifest. No parallel producer/binder, sixth module or `c11d-control`.

Production D renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze or promotion.
