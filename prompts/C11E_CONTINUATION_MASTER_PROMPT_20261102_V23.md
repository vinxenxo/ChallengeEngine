# C11-E Continuation Master Prompt — V23

## Mission

Deliver the complete C11-E production system for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics. Add D presentation and enabled editorial, D3 Music V5 with independent `request.music_seed`, FFmpeg mux and FFprobe A/V validation. GUI and CLI must call one shared production service. CHALLENGE_001 is only the first integration control.

## Current authority and evidence (2026-11-02)

- C11-C 2.19.12 remains production authority. Frozen manifest 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- V22 docs commit `02f5fac7698fe6d73076d3da1e3dfa852bd06725` was verified in HEAD ancestry; branch main; clean worktree.
- E2 R4 RequestId `C11E-E2-CH001-AB-20261101-V9-R4`; receipt SHA `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`; evidence ZIP SHA `f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de`.
- Godot numeric 30/30; Python 9/9; two renders, gameplay body identical 540/540, title slot different 540/540, final MP4 different 270/270; both H.264 High, yuv420p/tv, 720×1280, 30 fps, 270 frames, 9 s, no audio.
- Read-only reconciliation passed: commit, clean worktree, documentary pins 9/9, whitespace corrections 3/3, frozen C/source pins, receipt and ZIP, AVI/MP4 hashes 2/2 and FFprobe 2/2.
- E2 formal closure decision V1 uses user's instruction to perform visual confirmation and close. Assistant inspected all 540 decoded frames (270 A + 270 B) in twelve contact sheets. Original receipt remains immutable with its original `human_visual_review=PENDING` field; no claim that user personally played the files.
- E2 scope closed only for CHALLENGE_001 editorial title-to-pixels integration. Not family-wide acceptance.

## E3 next action

Run `tools/c11e/e3/RUN_C11E_E3_D3_MUSIC_V5_PREFLIGHT_20261102.ps1` after V23 is committed. It is read-only and locates exact D3 Music V5 contract, request schema, implementation, test and media validation sources, recording hashes and matching lines. It must not invoke audio render, production video render or FFmpeg mux. Review every selected source pin and read the actual D3 contract before designing functional test cases.

Required E3 properties: deterministic output for identical canonical music request and `music_seed`; changing only music seed changes music without changing gameplay frames; changing gameplay seed does not change music when music seed is held; reject invalid seed/assets/configuration per exact contract; FFmpeg mux; FFprobe validation of streams/codecs/sample rate/channel layout/start times/durations/offsets/synchronization and truncation. Exact codec/settings/tolerances must come from D3 V5, never be invented.

## Remaining roadmap

E4A Challenge adapter; E4B Visual Loop adapter; E4C Visual Drill adapter; E5 deterministic seed isolation and GUI/CLI parity across all three; E6 Smoke18 (six per family); E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill; CH_008/009 held due 11 s declaration vs 12 s phase sum, currently 99 valid); E8 independent acceptance, freeze and explicit promotion.

## Governance invariants

`release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false` until E8. No protected C mechanics/generator or frozen manifest changes. No `c11d-control`. One shared service for GUI/CLI. No automatic seeds or cross-domain RNG consumption. Fresh RequestId for each physical attempt. Keep receipts and evidence immutable. User commits locally each iteration; do not make commits, resets, rebases, cleans or ref changes on their behalf.
