# C11-E next-window start prompt â€” V21

Continue the C11-E project in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Do not regenerate snapshots or repeat accepted E0/E1, V9 reconciliation, Godot numeric 30/30, Python 9/9, V19 test repair or V20 runner pin repair.

## Authority and invariants

The active checkout is authoritative. First verify branch, HEAD, parent, worktree status, R3 evidence, V9/V19/V20 receipts, current runner source SHA, Python test SHA and frozen C11-C manifest. Accept local commits as normal descendants; require E0/E1 lineage and exact source pins. Do not reset, clean, rebase, amend, push or alter Git refs. User commits locally each iteration.

C11-C 2.19.12 remains production authority until E8 independent acceptance, freeze and explicit promotion. Frozen manifest is 796,318 bytes, SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Never modify protected C generators/mechanics or use c11d-control. No release authority is granted by E2 tests.

## Current verified status

- E0 accepted; E1 automation 2/2 PASS; manual GUI observation pending.
- E2 Godot JSON numeric 30/30 PASS; Python contract 9/9 PASS.
- V9 installed by reconciliation receipt `d039360862d034b8f05f67cf8d0ddf914a1ed27075200f6a6c04462b92367972`.
- R1/R2 failed at stale Python test 09 before render.
- R3 rendered A only. The MP4 is H.264 High, 720Ã—1280, 30 FPS, 270 frames, no audio, but FFprobe reported `yuvj420p/pc`; B and A/B comparisons did not occur. Failure ZIP SHA `cff29f245a1c8cf97ac02cd7bed3455a0a2ac364248f7cf257a2b148f2e0f6ab`.
- Runner was corrected to normalize source full-range `pc` into limited `tv`: `scale=720:1280:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p`, encoder flags `-pix_fmt yuv420p -color_range tv`, probe requires `h264/yuv420p/tv`. Actual installed FFmpeg 9.0 test transcode of R3 A AVI passed FFprobe.
- Current runner SHA: `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`.

## Immediate action

Make the user's ordinary local commit after validating the V21 V3 range-fix receipt. Then run the existing runner in a new child PowerShell process with fresh ID `C11E-E2-CH001-AB-20261101-V9-R4`, gameplay seed 193847 and music seed 840001. Use Godot 4.7.1 Mono, Python 3.13 and FFmpeg/FFprobe 9.0. Do not reuse R1/R2/R3. Runner repeats Godot numeric 30/30 and Python 9/9, then must produce exactly A and B. Verify both MP4s H.264 High, yuv420p, tv, 720Ã—1280, 30fps, 270 frames, no audio; source AVIs 540Ã—960 60fps 540 frames; three nonuniform samples; gameplay crop identical 540/540; title slot different 540/540; header outside slot identical; final MP4 different 270/270; SHA integrity and failure/success ZIP integrity.

Only after R4 automated PASS may the human visual review of both videos be recorded. E2 acceptance requires separate independent decision. E3 cannot start before E2 is accepted.

## Full E roadmap â€” do not lose scope

E3 D3 Music V5 independent `request.music_seed`, deterministic music, FFmpeg mux, FFprobe A/V; E4A Challenge adapter; E4B Visual Loop adapter; E4C Visual Drill adapter; E5 determinism, seed isolation and GUI/CLI parity; E6 Smoke18 (six per family); E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill); E8 independent acceptance, freeze and explicit promotion. CH_008/009 remain held due 11s declared versus 12s phase sum (3+7+0+2), so only 99 currently runnable. Do not claim Matrix101 complete until authority resolves the discrepancy.

The final objective is full Challenge + Visual Loop + Visual Drill production with presentation, enabled editorial and music, not merely CH001. Keep all preflight and governance locks intact.