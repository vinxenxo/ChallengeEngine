# C11-D to C11-E Full-Family Roadmap — V67

## Current point: E4B Loop family contract correction

E4B planning matrix is accepted for 27 selectors in plan-only mode. Five policy decisions are approved. Family-stage contract V1 was installed add-only, but its Windows runner exposed a false test assumption: the test and runner required zero MP4 files although the active checkout had 27 manifest-listed files. V2 fixes the observation semantics and adds tests for 0, 13 and 27.

## Remaining E4B closure
1. Run V2 in Windows PS 5.1; verify 8/8 tests, pins, report, receipt and sidecars.
2. Integrate the family-stage contract into the existing D boundary.
3. Prove request-scoped materialization for 27/27 selectors, with payload receipts supplying frame_count/FPS/duration.
4. Implement approved D-only visual composition and verify isolated Godot output.
5. Resolve music_seed-bound audio route separately and complete A/V acceptance.
6. Obtain human visual review and close E4B.

## Subsequent phases
E4C Drill follows the accepted Loop consumer pattern but needs its own contract and evidence. Then E5 integration closure → Smoke18 → Matrix101 (CH_008/009 remain held until their timing discrepancy is fixed) → E8 final freeze/promotion decision.

## Permanent controls
No C11-C source modifications; no parallel Producer or sixth GUI surface; no renderer/media until explicitly authorized by gate; no inference from file existence; separate gameplay/music seeds; no release authority until formal promotion.
