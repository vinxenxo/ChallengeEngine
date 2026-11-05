# C11-E E4A.5B — Challenge root/source closure checkpoint V1

**Date:** 2026-11-05  
**Working snapshot:** `ChallengeEngineV01_STATELESS_C11-E3-LATEST.zip`  
**Snapshot SHA-256:** `a70ff52e89c28ce527cc8e4af897d80043b64549a2a74aab34c012994779061c`

## Disposition

`E4A5B_SOURCE_REVIEW=PASS_READ_ONLY_SOURCE_REVIEW_FROM_USER_SUPPLIED_LATEST_SNAPSHOT`

The ZIP passed CRC validation and contained 18,911 entries. Its source tree was extracted as an isolated working directory. No `.git` metadata is present, so branch/HEAD/dirty status is not asserted. This is a static source closure based on the user's latest supplied working snapshot, not a live Windows checkout receipt.

The original 88-member E4A.5 handoff inventory was reconciled as 83 exact matches plus five evidence-pinned postimages, with zero unrecognized deltas:

- E4A.1: `c11c-suite/c11c-producer/main.py` and `c11e_production_service.py`.
- E4A.3D.1: `materialize_challenge_visual_payload_in_memory.gd`, `c11e_e4a_d_compositor_real_body_pixel_review.py`, and its focused test.

The historical C11-C 2.19.12 source baseline remains protected. The E4A.1 `main.py` delta is accepted and not reverted.

## V4 stale pin correction

V3/V4 expected `8f3e6561...` for `test_c11e_challenge_editorial_presentation_adapter.py`. The latest snapshot contains `d5c1dcaf553ace24f1f55b808e63ed47ee8d5f66f30334f422a19e3f238a0fc4`. The E4A.3D.1 apply source shows this test in the explicit focused pytest command; that invocation exited 0 and its receipt says 82 passed. However, the receipt has no per-file SHA for this test. Therefore the observed hash is recorded only as a latest-snapshot baseline pin, not as a new authorized postimage. No test file change or blanket exclusion is proposed.

## Root and scene closure

- `project.godot` main scene: `res://Main.tscn`.
- `Main.tscn` loads `res://GeneradorMaestro.gd` and `res://core/presentation/UnifiedSocialFrame.tscn`.
- `GeneradorMaestro.gd` obtains the existing frame at `OptimizadorVertical/PantallaVideo/UnifiedSocialFrame`; native `PresentationUI` is initialized with shared mode default false.
- The root has four distinct native phase branches (HOOK/GAME/REVEAL/CTA), four render-model builds and four native binder calls. `timeline.advance()` occurs once after the match.
- Physical C launcher and QA caller are included and reviewed; QA reuses the C launcher.
- Transitive Godot text resources and local resource references were resolved; 10 referenced non-text assets are hash-recorded. Nine Challenge JSON definitions were included.

The candidate insertion seam for E4A.6 is immediately after each existing `social_ui_binder.bind_render_model(rm)` and before control leaves the current phase branch / before the one `timeline.advance()`.

## E4A.6 design correction

The existing `SocialUIBinder.bind_render_model` delegates to `PresentationUI.apply_render_model`, which applies Hook, Countdown, RevealManager, WinningHighlight and CTA. A second full binder call in the same frame would reprocess RevealManager/WinningHighlight and is rejected by this design.

A D-only Challenge consumer must instead run after the one native binder call and:

- Build the shared model from the six approved E4A field rows (`title`, `subtitle`, `player_name`, `challenge_label`, `call_to_action`, `language`) and the original half-open source-frame ranges supplied by the approved policy/materializer.
- Update only the targeted visibility of HookComponent, CountdownComponent and native CTA; native text/countdown values remain set by the existing binder.
- Mount the C11CVisualEditorialLayer once per Challenge session on the existing UnifiedSocialFrame; use `apply_render_model` only on later frames. The current `apply_to_shared_layer` helper remounts/clears nodes and is not frame-loop safe.
- Show the D CTA only in its approved non-empty CTA window while hiding the native CTA component; otherwise native C CTA retains ownership.
- Migrate native hook to the shared header only when the adapter says so; preserve countdown in BODY when ON and hide both native hook/countdown when the Challenge option is OFF.
- Keep timeline state, phase messages, `state_frame` offsets, mechanics, gameplay RNG and all C11-C components untouched.

The D9.9 materializer's existing composition status is test-pixel-only; E4A.6 must define a fail-closed D-owned envelope transport to the root, without changing the C11-C launcher/QA contract or enabling production dispatch.

## A/V route disposition

Existing C path: Godot Movie Maker native 540x960; optional C7 44.1 kHz mono PCM; FFmpeg scale/H.264; optional AAC-LC 48 kHz stereo mux; FFprobe A/V delta <=50 ms. This is not D3 V5. E1 currently prepares a D3 music contract/plan using a separate `music_seed`, but does not invoke the D3 engine, create audio, dispatch renderer or invoke FFmpeg mux. The A/V path is reviewed but not end-to-end accepted.

## Next phase and acceptance

`E4A.6=DESIGN_READY_IMPLEMENTATION_PENDING`. Build only the D-owned consumer/envelope path and isolated tests. Do not proceed to E4B/E4C until E4A.6 visual root tests and the Challenge D3/music/mux/FFprobe path are reviewed and accepted.

No Godot/FFmpeg execution, media generation, source edits, documentation writes to the snapshot, staging or commits occurred in E4A.5B. Production locks remain unchanged; `release_authority=NONE`.
