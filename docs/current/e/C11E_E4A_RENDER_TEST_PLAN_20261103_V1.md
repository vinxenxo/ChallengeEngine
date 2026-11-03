# C11-E E4A Challenge — Isolated Pixel/Render Test Plan V1

**Status:** `READY_FOR_SOURCE_BOUND_IMPLEMENTATION`  
**Authorization:** isolated E4A test rendering authorized by operator instruction dated 2026-11-03; production renderer remains unauthorized.

## 1. Goal

Demonstrate that the approved D9.9 Challenge editorial values are consumed by the existing D-only in-memory visual composition and appear in the correct pixels and named source-time windows, without changing gameplay source frames or frozen C11-C behavior.

## 2. Existing implementation boundary to reuse

Do not create a new binder or second renderer. The next patch must be based on the exact current bytes of:
- `tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd`
- `tools/c11d/d9/challenge_visual_payload_v2b_safe_projection_runtime_in_memory.gd`
- `tools/c11d/d9/challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd`
- `tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd`
- `tools/c11d/d9/test_allowlisted_coordinate_consumer_review_only_runtime_v2.gd`
- `tools/c11d/d9/editorial_render_bridge.py`
- `tools/c11d/d9/d_render_adapter.py`
- `tools/c11d/d9/universal_editorial_model.py`
- `c11c-suite/c11c-producer/c11e_production_service.py`
- `c11c-suite/c11c-producer/main.py`
- `challenges/CHALLENGE_004.json`

Read-only C11-C references (must not be changed):
- `core/presentation/ChallengePresentationBinder.gd`
- `core/presentation/C11CVisualEditorialLayer.gd`
- `core/presentation/rendering/VisualContentPlayer.gd`

Read-only D contracts/checkpoints to reuse: D1.1, D1.5, D1.7, V2B Runtime Contract V2, V2B Source Composition Contract V1 and Runtime Evidence V2, V2C source-frame receipt and Gate A receipt/sidecar.

## 3. Test sequence

### Test A — source and composition join

For CHALLENGE_004, resolve canonical effective editorial values with D9.8, canonical request/plan identity with D9.9 and the existing source-timebase Challenge payload/materializer. Bind exact value hashes, field names, approved semantic region, named phase windows, policy SHA-256, profile/source identity and payload identity into the existing D-owned composition. No serialization of `FrameSnapshot.custom_data`.

If the existing V2B coordinate allowlist excludes CHALLENGE_004, do not silently bypass it. Extend only the D-owned test contract/allowlist for this bounded fixture after the source shows how that allowlist is intended to expand; preserve strict candidate identity and negative coverage.

### Test B — off-screen pixel proof

Use an isolated Godot off-screen test surface that consumes the actual D composition result. It may create PNG/frame artifacts only under a test evidence directory. It must not be called by the production Producer or D9.10 dispatch path.

A/B inputs use the same source Challenge, gameplay seed, materialized source frames and profile. A contains empty editorial values; B contains distinctive test strings. Assert:
- `title`/`subtitle` change pixels only inside HEADER and only in HOOK;
- `call_to_action` changes pixels only inside FOOTER and only in CTA;
- `player_name`/`challenge_label` draw only if the existing approved profile resolves CHALLENGE_OVERLAY geometry; otherwise they fail closed and are recorded unresolved, not guessed;
- `language` causes no pixel change;
- fields are absent outside their named windows;
- empty/whitespace values produce no placeholder or fallback;
- gameplay/body regions and source frame hashes remain identical A/B;
- no `SimulationResult`, `winning_frame`, `close_calls`, RNG or source `FrameSnapshot.custom_data` mutation occurs;
- same inputs repeat to identical composition and pixel hashes.

The first positive visual pair should prove at least one known region/window (HEADER/HOOK) through the real D composition path. Do not claim all five visual fields pass until each has a positive pixel proof.

### Test C — isolated audiovisual acceptance

After Test B passes, use the existing accepted E3 D3 V5/FFmpeg/FFprobe pipeline as test-only mux/QC, without rerendering gameplay unless the visual frames have to be regenerated. Preserve independent `request.seed` and `request.music_seed`. Validate exactly one H.264 video and one AAC audio stream, frame geometry/rate/count, 48 kHz stereo, durations/drift, non-silence, `faststart` and video copy where the accepted E3 contract applies. Keep all outputs/evidence under an E4A test-only root.

## 4. Required evidence

- policy approval JSON and SHA-256;
- source and request/payload/profile lineage;
- source frame sequence hashes before/after;
- composition record and deterministic hashes;
- per-field A/B PNG/pixel-diff metrics and region/window assertions;
- stdout/stderr/exit code for focused Godot test, no wrapper-generated exit codes;
- optional test-only MP4 + FFprobe JSON + audio QA after pixel pass;
- immutable E4A test receipt and report.

## 5. Exit criteria and governance

E4A pixel test closes only when all supported visual fields have positive/negative coverage and all protected invariants pass. If `CHALLENGE_OVERLAY` cannot be resolved by the existing profile hierarchy, its two fields remain explicitly blocked while other proven fields may be closed; do not fabricate geometry.

The user authorized isolated E4A testing only. This plan does not authorize production GUI/CLI dispatch, renderer activation, candidate input admission, D4.8, D9.14/D9.16/D9.17 closure, D10 promotion, release, baseline freeze or C11-C replacement.
