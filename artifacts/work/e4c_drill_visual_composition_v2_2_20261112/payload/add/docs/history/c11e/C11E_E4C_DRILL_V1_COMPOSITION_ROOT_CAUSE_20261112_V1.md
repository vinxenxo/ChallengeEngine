# E4C V1 composition defect — evidence and root-cause record V1 (2026-11-12)

## Evidence reviewed

- `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8.zip`, 17,780,165 bytes.
- `e4c_cli_smoke.zip`, 3,849 bytes (CLI runner result/logs).
- `Captura de pantalla 2026-11-12 102410.png`, 124,703 bytes.
- Qualification receipt SHA-256 `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`.
- E1 intent SHA-256 `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`.

The CLI runner records `SOURCE_PINS_PRE=PASS/19`, `SOURCE_PINS_POST=PASS/19`, CLI entrypoint/shared executor/parity/AV bitstream/music seed isolation PASS. Receipt records 91 E1 pins unchanged before execution, immediately before renderer and after execution. It records 810 frames at 30fps, phases 90/630/90, family music A/B exact and C changed, final H.264 A/C same and AAC A/C different, 27s 720×1280 H.264 High + AAC-LC 48k stereo.

The screenshot and operator review show the native tracking family description and native telemetry inside the central viewport, while GUI/CLI editorial is also drawn in new top/bottom bands. Music and render quality are accepted; visual composition is rejected.

## Root cause

The V1 consumer scaled the complete 720×1280 native frame to 504×896 with `IgnoreAspectRatio` and `SmoothTransformation`, then placed it at `(108,192)`. This makes native source header/footer content part of GAME's central image. The consumer separately paints D editorial into outer header/footer. PRE_ROLL and END_CTA are still processed through outer-band composition when they must remain native full-frame passthrough.

The previous V1 test suite asserted the 504×896 contained viewport and did not compare the complete PRE_ROLL/END_CTA frames. Thus implementation and test expectations agreed with each other but did not prove the intended social-body ownership.

## Corrective decision

Use `PresentationProfile.gd::get_social_regions()` whose exact pin is `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24`. V2 body rectangle is `(0,192,720,896)`; full-width header/footer are 192px each. GAME extracts/pastes body pixels at identical coordinates; PRE_ROLL/END_CTA are complete native passthrough; D editorial only on GAME. Preserve the existing 90/630/90 timing.

## Disposition

Underlying CLI technical/A/V receipt and native/audio evidence remain valid and are reused. V1 visual output is rejected. Historical GUI V1 A/V is not rerun. V2 candidate remains uninstalled until Windows acceptance; E4C remains open. Release authority remains NONE.

## V2.1 authoritative reconciliation (2026-11-12)

`E4C_OPEN_V2_REQUALIFICATION_PENDING`. Geometry V2 and the Test 04 boundary correction are accepted: `validate_plan()` now requires `source_frame_viewport == EXPECTED_SOCIAL_REGIONS["body_rect"]`. Reconciled consumer SHA-256: `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256: `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`; isolated Python 3.13.14 evidence is py_compile PASS and 20/20 PASS.

V1.7 destination preflight, V1.8 operation/package binding, V1.9 geometry contract and V2.0 staging Test 04 failures are closed before transaction; none installed this correction. V2.1 is rebuilt and pending Windows installation, complete receipt and postimage review. Do not install V2.0 and do not repeat GUI, CLI smoke, native capture, music or Binder.

Preserve evidence GUI `D99-GUI-6514F1066E79`, CLI `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, native silent MP4, WAV A/B/C, seeds and bitstreams. V1 composition was visually rejected; `tracking/tier-1` is not yet an accepted V2 matrix row.

Required sequence: documentation; V2.1 installation; receipt/postimage audit; one existing-media requalification; seven-image/three-MP4 review; operator visual/audio acceptance; row 1/20; remaining 19; E4C close; E5, E6 Smoke18, E7 Matrix101, E8. C11-C 2.19.12 only; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no Git, pip, C11-C mutation, dispatch or release; operator-managed commits.
