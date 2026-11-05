# C11-E E4A.6 Live Root Pixel Capture — Plan V2

## Objective

Produce the first pixel-level evidence of the live Challenge D consumer in `Main.tscn`, using the exact V3 E1 envelope. This is a bounded test-only silent capture, not an A/V release or production render.

## Preconditions

- Sole authority: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
- Git HEAD: `a18444655cdb844104561840a59a473b7bbbb172`.
- `GeneradorMaestro.gd`: SHA-256 `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`.
- V3 E1 envelope SHA-256 `d7f3814ef1bcce4719f59e4eab013ff6f650475a77f5d290d7f46c142f6914ec`.
- `CHALLENGE_004.json`: SHA-256 `6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71`.
- Godot 4.7.1, FFmpeg and FFprobe available.

Any source drift, missing envelope, tool mismatch or output collision stops the run.

## Procedure

1. Run a headless 900-iteration root compatibility smoke **without** the D envelope. Require root startup, clean exit/stderr and no D summary.
2. Run Godot Movie Maker directly against `Main.tscn`, with the Challenge config and V3 envelope; native 540x960, 60 FPS, exactly 900 frames. Omit `--audio-output`.
3. FFprobe verifies the source AVI at 540x960, 60/1 and 900 decoded frames.
4. FFmpeg creates a silent review MP4 at 720x1280, 30/1, H.264/yuv420p, exactly 450 frames. Require zero audio streams.
5. Extract eight exact delivery-frame samples, preserving phase boundaries (delivery frame -> source frame at 60 FPS):
   - 0 -> 0: HOOK first frame
   - 89 -> 178: HOOK last frame
   - 90 -> 180: GAME first frame
   - 299 -> 598: GAME last frame
   - 300 -> 600: REVEAL first frame
   - 389 -> 778: REVEAL last frame
   - 390 -> 780: CTA first frame
   - 449 -> 898: CTA last frame
6. Verify `GeneradorMaestro.gd` is byte-identical to the pinned SHA; record tool versions, commands, stdout/stderr, FFprobe JSON, frame hashes and Git status before/after.

## Test-only boundary

Test media is written only to `artifacts/tests/c11e/e4a6_live_visual_capture/`. The run does not call the physical production launcher, Producer GUI/CLI, production renderer or dispatch. It does not generate D3 audio, mux audio or change source code. The silent review MP4 is for inspection only. `release_authority=NONE`.

## Acceptance interpretation

A successful receipt closes only execution of the pixel-capture subgate. It does not approve layout. Inspect all eight samples and the silent review video for header/footer safe areas, typography and font-metric wrapping, hook/title/subtitle overlap, CTA ownership, clipping, phase transitions and unintended D text during GAME/REVEAL. D1.5/D1.1/D1.7 visual geometry approval remains a separate human decision. Any defect blocks the D3-composited A/V mux step until a minimal versioned D-only correction is tested.
