# C11-E FIRST PROMPT V66 — PIN-ALIGNED R1 STATE — 2026-11-13

Continue ChallengeEngine C11-E from the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. This is an ongoing governed project: do not restart accepted gates or repeat accepted A/V runs. The active checkout is sole source authority; ZIP snapshots/evidence are never extracted over it. `GIT_CHECKS=SKIPPED`; operator manages commits; no pip or shared dependency changes. ChatGPT owns architecture, coding, audit and documentation; operator executes tests.

## Current phase — E4C Visual Drill V2 composition requalification

The original CLI A/V smoke passed technically but V1 composition was visually rejected: native family header/footer were embedded in the center and D editorial bands were additional outer overlays.

Accepted V2 layout derives from frozen `PresentationProfile.gd` SHA `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24`: canvas 720×1280; header `(0,0,720,192)`; native GAME body `(0,192,720,896)`; footer `(0,1088,720,192)`. PRE_ROLL/END_CTA are complete native-frame passthrough; GAME body is exact pixel copy without resize/interpolation and D editorial occupies header/footer. Timebase 90/630/90 = 810 frames.

Consumer `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` and test `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf` remain unchanged. Isolated py_compile and 20/20 Qt-offscreen tests previously passed. `validate_plan()` enforces exact `social_regions.body_rect`, rejecting V1 centered viewport.

## Latest installation incident

Windows path preflight `C11E_E4C_DRILL_V2_V2_2_20261113T061924Z_7c2e5422` PASS: lengths 139/213/256/195 under 259; forward and rollback File.Replace PASS; probes cleaned. Old V2.1 temp sibling was identified as expected postimage and preserved (do not delete).

Superseded reviewed archive `ecfe23aca3de0474c717d03b1d719195612d754f8a5cd14b039fa1179cc1b3bf` then failed before transaction because its documentation payload modified the approved decision record. Consumer expects `DECISION_SHA=bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8`; original JSON is 2,925 bytes and must remain byte-for-byte immutable. Assistant appended `latest_execution_state`, changing the digest to `5d77eb...`; consumer correctly rejected it. Run `C11E_E4C_DRILL_V2_V2_2_20261113T061938Z_c33b887a`: `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES`, journal empty, rollback errors empty, no destination writes. Never use this old archive and do not weaken the pin.

Corrected package: `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_2_PIN_ALIGNED_R1_20261113.zip` with its new `.sha256` sidecar. It restores the original decision JSON SHA `bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8`. Consumer, tests and installer unchanged; mutable execution state lives in Authority/Gates/Backlog/Plan/Incident Register and these prompts. Standalone path preflight already passed and need not be repeated; installer includes its own built-in File.Replace preflight.

## Next actions

1. Verify ZIP using adjacent sidecar. Extract to new Downloads directory `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_2_PIN_ALIGNED_R1_20261113`, not checkout.
2. Run `INSTALL_C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_V2_2.ps1` once with active project root, existing Python313 and `-PackageZip $Zip`. Require 27/27 package files, 21/21 pins, frozen manifest, AST 2/2, 1 REPLACE +24 ADD_ONLY, py_compile 3/3, tests 20/20, internal File.Replace preflight, immediate recheck and final install PASS.
3. Audit receipt, journal, all 25 postimages and 21 source pins. Stop on any discrepancy.
4. Only after install PASS, run existing-media requalifier once using preserved CLI-native MP4/WAV A/B/C. No Godot, C11-C capture, music generation, GUI smoke or CLI smoke.
5. Review seven images and three MP4s. Operator visual/audio decision is required. Only on PASS count `tracking/tier-1` as row 1/20; then complete 19 remaining selectors.
6. E4C close at 20/20. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separate promotion authorization.

## Frozen governance

C11-C 2.19.12 and manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` remain sole production authority. E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no C11-C changes, dispatch false, release NONE. No D3 V5 on this Drill music route; no gameplay-seed-coupled music. Reuse FAMILY_MUSIC_V4 outputs with music seeds 840001/840002 only in the existing-media requalification.
