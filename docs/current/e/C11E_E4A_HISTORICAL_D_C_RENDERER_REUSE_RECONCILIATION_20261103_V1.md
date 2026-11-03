# C11-E E4A — Historical D/C Renderer Reuse Reconciliation V1

**Date:** 2026-11-03  
**Purpose:** prevent a second consumer/binder and recover the already completed D/C work relevant to Challenge editorial rendering.

## 1. Historical C11-C baseline behavior (reference only)

C11-C 2.19.12 already has the protected presentation path represented by:
- `core/presentation/ChallengePresentationBinder.gd`
- `core/presentation/C11CVisualEditorialLayer.gd`
- `core/presentation/rendering/VisualContentPlayer.gd`

These are frozen reference sources. Do not edit or vendor-copy them into a second renderer. D/E may use the established logical frame/profile/family semantics but must keep implementation and editorial payload D-owned.

Canonical source preview remains at its native timebase. Delivery scaling to 720×1280/30 is downstream and must not change source frame identity or policy windows. The shared logical frame is 540×960: HEADER y=0–144, BODY y=144–816, FOOTER y=816–960.

## 2. Historical D presentation decisions

- D1.1 Challenge visual/editorial mapping: `PASS_MAPPING_EVIDENCE_NON_RENDERING`.
- D1.5 platform layout template: canonical 540×960 frame, HEADER/BODY/FOOTER hierarchy and presentation topology.
- D1.7 declarative Challenge mapping: 9/9 selector mappings, canonical inherited layout, no Challenge-specific layout override, explicit UNKNOWN handling.
- Historical region hierarchy reconciliation: semantic roles are not coordinate boxes. The normalized-permille boxes from the semantic-region proposal were explicitly not approved and are not canonical.
- Challenge phase ordering is `HOOK → GAME → REVEAL → CTA`; phase boundaries are sourced from the selected Challenge's canonical timeline. `winning_frame` remains the only Challenge temporal anchor; `close_calls` is only an episode count.

## 3. Existing D-only visual composition work

### V2B allowlisted coordinate review consumer

The existing files/contracts include:
- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CONTRACT_V2.json` (historical SHA-256 `0bd65e8f64c13850670d927d62209276ae94999ce57c790db7ae1592fa793ae9`)
- `tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd` (historical SHA-256 `2376d4c9208d749b3681f8083d1d0be1a5658f62930b9b92167916196aec3eef`)
- `tools/c11d/d9/test_allowlisted_coordinate_consumer_review_only_runtime_v2.gd` (historical SHA-256 `8b30bc90fa7f95ac8b38e8ad2b01670ed1fb97416acfc437225db4f478f8ded5`)

The isolated consumer passed 277 runtime cases (241 negative + 36 positive). It projects only allowlisted candidate coordinate pairs into closed in-memory logical marker descriptors. It intentionally has no RenderingServer/Sprite2D/Texture2D calls and proves no pixels were drawn.

### V2B source-composition runtime evidence

The accepted evidence validator reports 402/402 checks and the corrected source composition runtime run reports four candidate Challenges, 1680/1680 source frames and 1680/1680 logical marker frames. The review harness reads raw `custom_data` zero times; one allowlisted lookup per frame is attributed to the D consumer. It is source/runtime composition evidence only: no payload is persisted, no native renderer input is emitted and no video is produced.

These accepted historical results are reusable. Do not rerun them without a relevant source-pin change.

## 4. E4A integration boundary

The approved Challenge policy must be joined in the existing D-only composition route, upstream of any isolated off-screen drawing:

`D9.8 effective editorial values → D9.9 canonical request/plan → D9.10 prepare-only bridge → D-only source-timebase materializer → V2B allowlisted coordinate/composition boundary → isolated test-only pixel surface`.

The source-timebase materializer/consumer must provide source identity, named phase bounds, frame count/timebase, asset identities and deterministic hashes. Editorial binding carries exact field/value hashes and policy identity alongside the visual composition; it never reads or serializes all `FrameSnapshot.custom_data`.

The isolated pixel surface is a test harness only. It must not be linked from the production Producer, D9.10 dispatch or the frozen C11-C renderer. It should consume the same D-owned composition output that production would eventually use, so the test cannot become an alternate policy/binder implementation.

## 5. No repeated work

Do not rerun V2B 277 runtime cases, V2B source-composition 402-check validator, Gate A report/preview commands, the E4A static GUI contract, E3 pilot or E3 negative suite unless a relevant dependency source changes. The five Gate A Python test exits remain unverified due to the PS stderr capture defect; they do not invalidate the independently successful report and Godot preview commands.
