# C11-E E4A.6 — Minimum D-only Challenge live consumer integration design V1

**Date:** 2026-11-05  
**Design status:** READY FOR IMPLEMENTATION REVIEW; NOT IMPLEMENTED  
**Source basis:** user-supplied latest snapshot SHA-256 `a70ff52e89c28ce527cc8e4af897d80043b64549a2a74aab34c012994779061c`

## 1. Objective and non-goals

Connect approved D editorial presentation to the existing live Challenge root without replacing or cloning the C Challenge generator, phase timeline, `SocialUIBinder`, `PresentationUI`, renderer, producer or GUI. Keep all edits presentation-only and D-owned. This design does not authorize production dispatch, media creation, release promotion or changes to C11-C 2.19.12.

Non-goals: change `SimulationResult`, `FrameSnapshot`, `winning_frame`, `close_calls`, `WinningFrameDetector`, mechanics, seed/RNG ownership, `VideoTimeline`, phase durations, `timeline.advance()`, native Challenge phase text, C7 audio, C11-C binders, Loop/Drill presentation, or shared C11-C source files.

## 2. Proven root topology

`project.godot` selects `Main.tscn`. `Main.tscn` attaches `GeneradorMaestro.gd` and `UnifiedSocialFrame.tscn`. `GeneradorMaestro.gd` resolves `OptimizadorVertical/PantallaVideo/UnifiedSocialFrame` as the `presentation_ui_root`. It creates `PresentationUI` with its default `use_c11c_shared_social_editorial=false`, then a single `SocialUIBinder`.

The runtime match contains exactly four phase branches:

| Native phase | Render model | Existing binder | D consumer insertion |
|---|---:|---:|---|
| HOOK | 1147 | 1150 | immediately after 1150 |
| GAME | 1167 | 1170 | immediately after 1170 |
| REVEAL | 1179 | 1182 | immediately after 1182 |
| CTA | 1191 | 1194 | immediately after 1194 |

`timeline.advance()` is called once after the match (line 1199 in this snapshot). `timeline.get_current_block()` remains the only phase authority. The D consumer must use the absolute source frame while the current frame is still active and before that single advance.

## 3. D-owned component boundary

Introduce one new D-only Challenge consumer under `tools/c11d/d9/` (proposed name `C11EChallengeLiveEditorialConsumer.gd`, final filename subject to repository naming check). It owns only:

- Validating a D-only editorial envelope and Challenge-only E1 presentation option.
- Constructing the shared editorial render model through the existing `C11EChallengeEditorialPresentationAdapter`.
- Mounting one `C11CVisualEditorialLayer` instance once on the already-resolved `UnifiedSocialFrame`.
- Updating the mounted layer per frame.
- Applying three targeted visibility overrides after the native binder has completed.

It must not call `SocialUIBinder.bind_render_model` or `PresentationUI.apply_render_model` itself. It must not create a second RevealManager, WinningHighlight, PresentationUI or CTA component. No changes to the existing C11C shared layer API are required.

## 4. Per-frame algorithm

1. Native Challenge phase branch builds `rm` using `ChallengePresentationBinder.build_frame_render_model(...)` exactly as today.
2. Call `social_ui_binder.bind_render_model(rm)` exactly once.
3. When D envelope is absent, keep the current C behavior and return from the D consumer (legacy-safe no-op).
4. When D envelope is present, validate its schema/status, Challenge identity, total source frame count, FPS/timebase, E1 intent identity, policy/layout hashes, six-field allowlist and every half-open range. Any mismatch is a hard fail before changing visible UI.
5. Read the absolute source frame from `timeline.get_current_frame()` (pre-advance) and native hook text from the current native render model. Use the approved composition rows and `C11EChallengeEditorialPresentationAdapter.build_shared_editorial_model(...)`. Do not invent phase ranges and do not alias field names to phase names.
6. Run `adapt_native_challenge_render_model(rm, intent, shared_model)` to calculate the D edge's desired native visibility; do not replace or mutate `rm`.
7. If this is the first active D frame, mount `C11CVisualEditorialLayer` once on the existing `UnifiedSocialFrame`. Mount failure is fail-closed. On every frame call `layer.apply_render_model(shared_model.render_model)` only. The current `apply_to_shared_layer(...)` convenience function MUST NOT be called per frame because it calls `mount()`, whose implementation clears/recreates both header/footer nodes.
8. Apply only targeted post-bind visibility:
   - `presentation_ui.hook_label.visible = adapted_model.show_hook`.
   - `presentation_ui.countdown.visible = adapted_model.countdown_visible`.
   - `presentation_ui.cta.visible = adapted_model.cta_visible`.
   Native Hook text, Countdown value and CTA content remain set by the single native binder call. Do not call component-wide or full-UI binders again.
9. Return to the native loop; the existing single `timeline.advance()` executes unchanged.

The consumer runs after all four branches to guarantee stale D overlays are hidden during GAME/REVEAL and across transitions, even though current approved Challenge title/subtitle windows are HOOK-only and CTA is CTA-only.

## 5. Ownership rules

### Hook / header

- If an approved non-empty title or subtitle is active in its HOOK window and `show_hook_countdown=true`, adapter migrates the native hook into the shared header's primary line and joins title/subtitle into its secondary string. Hide the native HookComponent only; keep Countdown visible in BODY.
- If the Challenge-only option is explicitly OFF, hide native HookComponent and CountdownComponent. The D header contains title and subtitle only. This is a live-root presentation control; it does not rewrite or erase previously baked pixels in a C11-C base video.
- If D header fields are empty/inactive, preserve native HookComponent visibility from the original Challenge render model.
- If header migration is requested but native hook text is empty while the option is ON, keep the adapter's current fail-closed behavior.

### CTA / footer

- D owns CTA only if the approved `call_to_action` field is non-empty and the current absolute frame lies in its approved CTA half-open source interval.
- On those frames, the D shared footer label/background is visible and the native C CTA component is hidden. This is the only period in which the D footer takes ownership.
- On empty/inactive D CTA frames, the D footer is hidden and native Challenge CTA remains visible according to the original `rm`.
- Never show native and D CTA simultaneously. Do not alter CTA phase timing or extend the CTA beyond the source window.

### Other UI

Badge, RevealManager, WinningHighlight, mechanics and BODY geometry remain exclusively under the native binder/runtime. The D consumer must not call `PresentationUI.apply_render_model` a second time.

## 6. Envelope / transport requirement

The current D9.9 materializer returns an in-memory composition marked `IN_MEMORY_D_ONLY_COMPOSITION_FOR_ISOLATED_PIXEL_TEST`. It is not a live runtime transport. E4A.6 must add a D-owned, fail-closed envelope with at least:

- schema/version and `status=PREPARED_E1_NOT_DISPATCHED` (or a narrowly scoped test status during test harness use);
- Challenge content type and Challenge ID;
- E1 request/intent hash and the Challenge-only `show_hook_countdown` option;
- source FPS, total frames, phase segments and the exact six approved field rows;
- `source_phase_windows`, validated `source_frame_ranges` with half-open intervals;
- approved policy and layout contract hashes;
- explicit `renderer_input_emitted=false`, `production_dispatch=false`, `media_created=false`, `release_authority=NONE`.

Keep the envelope separate from the canonical C Challenge JSON and outside `SimulationResult`/`FrameSnapshot.custom_data`. Do not infer it from arbitrary config keys. It must be tied to the same Challenge ID, source phase durations and frame count loaded by `Main.tscn`; fail if those do not match.

Suggested D-only CLI carrier: a separate `--c11e-editorial-envelope=<path>` user argument read by the D consumer. Do not change the frozen C11-C bulk launcher or QA caller for this test-only design. The D-owned test harness/service contract may pass this argument while reusing the existing project and scene; no parallel renderer or new GUI surface is introduced. Actual D service dispatch remains disabled.

## 7. A/V integration boundary

The existing physical C path is:

`C Challenge JSON -> run_c11c_challenge_production.ps1 -> Godot Main.tscn Movie Maker (540x960, challenge FPS) -> optional C7 PCM 44.1 kHz mono -> FFmpeg scale/H.264 -> optional AAC-LC 48 kHz stereo mux -> FFprobe frame/rate/duration checks (A/V delta <=50 ms)`.

This is not D3 V5. Current E1 service creates a prepared D3 V5 music contract/plan and independent `music_seed`, but engine invocation, D audio generation and FFmpeg mux are not proven. E4A.6 visual consumer tests must not claim full A/V acceptance. The separate Challenge D3 audio/render/mux path must be integrated and independently validated before E4A completion and before E4B/E4C.

## 8. Required E4A.6 tests and acceptance

### Static / unit

- Four exact consumer insertion points; one native binder call in each branch; one `timeline.advance()` after match.
- D envelope absent => byte-for-byte legacy render model and no D layer mount.
- Envelope identity/source frame count/FPS/phase ranges mismatch => fail-closed, no UI mutation.
- HOOK header title+subtitle, title-only, subtitle-only, all-empty variants.
- Native hook migration ON and explicit OFF; countdown ON/OFF; no duplicate hook.
- CTA active/non-empty => D-only owner; CTA empty/inactive => native owner; no overlap across frame boundaries.
- D shared layer mounts once; no remount or node duplication during repeated frame updates.
- GAME/REVEAL `RevealManager` and `WinningHighlight` processed once per frame only.
- `rm` input immutable; no C model mutation; no reads/writes of protected gameplay fields.
- Challenge-only scope rejects Loop/Drill.
- Source frame windows use approved half-open intervals; exact frame immediately before/at/after each transition.

### Isolated runtime proof

Use the existing `Main.tscn` with a test-only D envelope and test-only arguments in isolated output. Capture targeted frames from HOOK/GAME/REVEAL/CTA to verify single ownership and visibility. Keep Godot stderr and exit status, frame counts and per-region pixel checks. Do not call the production C launcher with its normal media destination; do not use FFmpeg or publish media unless a later authorized A/V phase explicitly allows it.

### E4A.6 gate requires

- source diff limited to D-owned Challenge consumer / D transport / narrowly scoped post-bind call sites in `GeneradorMaestro.gd`; no C11-C mechanics, timeline, binder, launcher or QA modifications;
- full baseline source SHA checks unchanged outside the declared D-only file list;
- static/unit tests and py_compile as applicable; focused Godot test with exit 0 and empty stderr;
- exact owner matrix for HOOK/Countdown/CTA;
- unchanged timeline sequence, frame count, fps and current phase progression;
- GUI/CLI prepare-intent parity; still no production dispatch;
- independent review of D3 V5 audio/mux path before E4A closure.

No production activation, release promotion, C11-C unfreeze or E4B/E4C start is implied by this design.
