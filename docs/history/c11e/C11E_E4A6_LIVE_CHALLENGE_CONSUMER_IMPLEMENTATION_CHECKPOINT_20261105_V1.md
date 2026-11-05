# C11-E E4A.6 Live Challenge Consumer — Implementation Checkpoint V1

**Date:** 2026-11-05. Scope: isolated, opt-in, D-only Challenge consumer implementation. This is not production activation, visual acceptance, D3 music closure, or release promotion.

## Implementation status

`IMPLEMENTED_STATIC_TESTS_PASS_WINDOWS_GODOT_RUNTIME_REQUIRED`.

The implementation is prepared against the user-supplied and reviewed work snapshot `ChallengeEngineV01_STATELESS_C11-E4A5B-REVIEWED_20261105.zip`. The Windows apply runner must verify all source preimages before applying. The supplied source snapshot has no `.git`; no branch, HEAD, or clean-worktree assertion is possible from that archive.

## Changed source surface

One existing file is changed, with an exact preimage/postimage transaction:

- `GeneradorMaestro.gd`: preimage `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`; E4A.6 postimage `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`.

Three D-only files are add-only:

- `tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd` — optional post-native-bind consumer.
- `tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py` — E1-backed test-only envelope preparation.
- `tools/c11d/d9/test_c11e_e4a6_challenge_live_editorial_envelope.py` — static/contract regression suite.

No changes are made to C11-C mechanics, `SimulationResult`, `FrameSnapshot`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C `SocialUIBinder`, `PresentationUI`, Loop/Drill binders, C launcher, or QA caller.

## Runtime contract

- D consumer is loaded lazily only when `--c11e-editorial-envelope=<path>` is supplied. Absence of the argument is a no-op; it does not preload D consumer code into the normal C path.
- Each native phase continues to make exactly one `SocialUIBinder.bind_render_model(rm)` call.
- The D consumer runs immediately after each native call in HOOK/GAME/REVEAL/CTA and before the single existing `timeline.advance()`.
- The D consumer does not call the full binder or `PresentationUI.apply_render_model` a second time. That would repeat `RevealManager`/`WinningHighlight` processing.
- The C11C shared editorial layer mounts at most once; subsequent frames call only `apply_render_model`.
- D changes only Hook/Countdown/CTA component visibility. It does not replace native text payloads or mutate the native render model.
- The E1-backed sidecar pins Challenge identity, intent identity, 60 FPS / 900 source frames, four half-open phase ranges, the six-field allowlist, policy/layout hashes, and no-dispatch/no-media governance. The sidecar `.sha256` is checked by the live consumer.
- Approved content remains unchanged: title/subtitle = HEADER during HOOK; call_to_action = FOOTER during CTA; language metadata-only; player_name/challenge_label blocked by unresolved overlay geometry.

## Test evidence available before Windows apply

- Python envelope builder executed against the real E1 service; it produced a sealed `PREPARED_E1_NOT_DISPATCHED` intent for CHALLENGE_004.
- Envelope source timebase: 60 FPS / 900 frames; HOOK [0,180), GAME [180,600), REVEAL [600,780), CTA [780,900).
- `py_compile` passed for the builder and tests.
- 16 focused Python tests passed.
- The local development environment has no Godot executable. Therefore no GDScript parser/runtime claim is made here. The flat Windows runner requires Godot 4.7.1 and performs a headless live-root logic run with no Movie Maker, FFmpeg, audio export, or media creation.

## Windows runtime acceptance criteria

The runner must record process exit codes, stdout/stderr files, source pre/post hashes, and a JSON receipt. It must reject non-empty stderr and verify the runtime summary:

- `status=PASS_TEST_ONLY`, `enabled=true`, `failed=false`;
- `frames_seen=900`, `mount_count=1`;
- `header_d_owner_frames=180`, `footer_d_owner_frames=120`;
- `native_cta_owner_frames=0`;
- `production_dispatch=false`, `renderer_input_emitted=false`, `media_created=false`, `release_authority=NONE`.

A failed or unavailable Godot runtime leaves E4A.6 open. No production dispatch, GUI production activation, render promotion, or media creation is authorized by this checkpoint.

## Required next work

1. Run the flat Windows PS5.1 apply/test runner against the extracted reviewed snapshot.
2. Inspect the resulting Godot 4.7.1 receipt and summary; repair only evidence-backed D-only defects.
3. Separately review the visual and timing behavior; do not infer visual acceptance from a headless logic run.
4. Complete D3 V5 actual Challenge audio generation, mux and FFprobe evidence before E4A final.
5. Hold E4B/E4C until Challenge E4A.6 and D3 A/V are accepted.
