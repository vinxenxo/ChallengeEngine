# C11-E E4A.5B — Read-only Challenge root/source closure V6

**Working base:** `ChallengeEngineV01_STATELESS_C11-E3-LATEST.zip`

**Snapshot SHA-256:** `a70ff52e89c28ce527cc8e4af897d80043b64549a2a74aab34c012994779061c`

The supplied archive passed full ZIP CRC validation (18,911 entries; no directory entries). The archive contains no `.git` metadata, so this report does not assert Git branch, HEAD or worktree cleanliness.

## Historical handoff reconciliation

The 88 historical source members in the E4A.5 base handoff reconcile as **83 exact matches + 5 exact, authorized postimages = 88/88**. There are no extra/unrecognized deltas. The five accepted deltas are the two E4A.1 GUI/service postimages and the three E4A.3D.1 compositor/materializer/test postimages. The C11-C freeze manifest and mechanics are not modified.

## V3/V4 pin failure

The file `tools/c11d/d9/test_c11e_challenge_editorial_presentation_adapter.py` in this latest snapshot is 6,715 bytes with SHA-256:

`d5c1dcaf553ace24f1f55b808e63ed47ee8d5f66f30334f422a19e3f238a0fc4`

V3/V4 expected `8f3e65619048c40bfa0f7c5e0d9a8ae274f0f18f00a7276bde5881dc16034478`. That expected value is not an individual E4A.3D.1 postimage recorded in the closeout receipt. The E4A.3D.1 apply script source explicitly includes this test as a pytest input; the invocation exited 0 and the receipt records 82 passed. The receipt does not store this file's SHA individually. Therefore `d5c1...` is classified as a **snapshot baseline pin**, not as an authorized E4A.3D.1 postimage. No source test change is proposed.

## Challenge root seam

`project.godot` selects `Main.tscn`; `Main.tscn` attaches `GeneradorMaestro.gd` and `UnifiedSocialFrame.tscn`. The Challenge root obtains the existing `UnifiedSocialFrame` as `presentation_ui_root`; `PresentationUI` is initialized in native non-shared mode.

The `_process` match has four canonical branches: `HOOK`, `GAME`, `REVEAL`, `CTA`. Each branch builds one native render model and calls `SocialUIBinder.bind_render_model(rm)` exactly once. `timeline.advance()` occurs once after the match. This is the proven insertion seam for E4A.6: immediately after each existing binder call and before the single advance. Phase keys remain the native timeline namespace, not D9.9 editorial field aliases.

## E4A.6 implementation design correction

Keep one complete `SocialUIBinder.bind_render_model(rm)` call per frame. **Do not call the binder or `PresentationUI.apply_render_model` a second time** with an adapted model: that would re-run `RevealManager` and `WinningHighlight` in addition to the native single pass.

After the native binder returns, a D-owned Challenge-only consumer should:

1. Build the shared editorial model from the already-approved D composition fields and the absolute source frame from `timeline.get_current_frame()` (before `timeline.advance()`). Use only the existing approved half-open `source_frame_ranges`; do not derive new phase ranges or alias HOOK/GAME/REVEAL/CTA to editorial fields.
2. Apply the native adaptation only as targeted visibility overrides: `HookComponent.visible`, `CountdownComponent.visible`, and `CTAComponent.visible`. Native content/text remains supplied by the native binder.
3. Mount `C11CVisualEditorialLayer` once on the existing `UnifiedSocialFrame`, then call only `layer.apply_render_model(...)` per frame. Do not use the current `apply_to_shared_layer` helper per frame: it calls `mount`, which clears/recreates the layer nodes.
4. Give D the CTA only when a non-empty approved `call_to_action` row is active in its CTA source window; hide the native CTA component for those frames. When D CTA is empty/inactive, preserve native C CTA ownership.
5. Migrate the native hook into the D header only when the adapter says `header_native_hook_migrated`; hide the native HookComponent then. Keep Countdown in the BODY when the request option is ON; hide Hook and Countdown when the Challenge-only option is OFF. Never modify gameplay state or timeline.

The design is not yet implemented or runtime-tested. The current D9.9 materializer labels its composition as isolated-pixel-test-only. E4A.6 must add a fail-closed D envelope transport to the root. Keep the C11-C launcher and QA caller unchanged; do not enable renderer/production dispatch as part of this work.

## Physical A/V path reviewed

The current C Challenge launcher invokes the existing Godot `Main.tscn` Movie Maker path at native 540x960 and challenge FPS, optionally captures C7 PCM (44.1 kHz mono), then uses FFmpeg for Lanczos scaling and H.264 delivery; when PCM exists it encodes AAC-LC at 48 kHz stereo and uses FFprobe to validate A/V duration within 50 ms. The QA caller reuses that C launcher for 54 runs (9 challenges x 6 seed cases).

This is the C7/native audio route, not the D3 V5 music path. E1 service currently prepares D3 V5 contract/plan with separate `music_seed`, but no D3 engine invocation, renderer dispatch, audio creation or FFmpeg mux has been proven. E4A full A/V acceptance remains pending.

## Scope and safety

Read-only source inspection only. No Godot, FFmpeg, renderer, producer, GUI job, test execution or media creation occurred during this review. No source or documentation files were written into the supplied snapshot. C11-C 2.19.12 stays frozen; production renderer/dispatch/media remain OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
