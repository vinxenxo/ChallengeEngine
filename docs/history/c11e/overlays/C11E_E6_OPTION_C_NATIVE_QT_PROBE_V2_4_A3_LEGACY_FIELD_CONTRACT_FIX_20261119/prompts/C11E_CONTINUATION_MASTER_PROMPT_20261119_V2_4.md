# C11-E continuation master prompt — V2.4 (2026-11-19)

Continue the C11-E project only from the operator's active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The checkout is sole authority; evidence ZIPs are reference only and must never be extracted over it.

## Established state from this window

- V2.1 installer: 16/16 PASS_ADD_ONLY; its runner failed on A3 `old_pointer_expected` comparison before QImage tests.
- V2.2 installer: 9/9 PASS_ADD_ONLY; the runner failed loading a generic `support` import.
- V2.3 installer: 10/10 PASS_ADD_ONLY; its 13 focused tests passed; its direct-file loader worked; the runner then failed because it incorrectly required `old_pointer_expected == old_pointer_actual`.
- Root cause is now proven from the original diagnostic producer source SHA `90375a6c21550d67e6aa1f374d5e5c8dcd7c06b630c51b34ad83313fbb7b2fc2`. `old_pointer_expected` is the historical whole-manifest SHA, while `old_pointer_actual` is the old D9.8 hash stored at `/source_lineage/6/sha256`. These intentionally differ. The V2.2/V2.3 adjudicator equality assumption was incorrect.
- V2.4 maps each diagnostic field independently to its exact source field, pins the original diagnostic generator source and retains exact manifest and single-pointer reconstruction checks.

## Immediate next step

Install V2.4 add-only, execute 17 focused regression tests, then run its native Qt/QImage probe once with Python 3.13.14 / PySide6 6.11.2 / seven iterations. Do not rerun V2.1/V2.2/V2.3 or their accepted tests. Preserve all prior receipts and sidecars.

## Immutable governance

C11-C freeze manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). D4.8 V2: `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`, unchanged and BLOCKED. Renderer OFF, E1 PREPARE_ONLY, dispatch/media OFF, D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, `e6_accepted=0`, `release_authority=NONE`. No Godot/FFmpeg/FFprobe/audio/mux. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.

## Next gate after successful QImage stage

Only after a true A3 pass, source closure, 37/37 QImage pass and native stage performance pass may planning proceed to one copied real frame at the existing D seam, then the six Loop selectors, all under separate static/test-only gates. Do not jump to full Smoke18 media execution or renderer dispatch. Prepare scoped successor policy and exact E6 TEST_ONLY execution manifest separately; original D4.8 V2 is not edited or bypassed.
