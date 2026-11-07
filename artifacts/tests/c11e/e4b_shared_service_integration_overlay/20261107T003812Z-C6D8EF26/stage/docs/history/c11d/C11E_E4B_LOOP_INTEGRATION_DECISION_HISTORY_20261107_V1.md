# C11-E E4B Loop Integration Decision History — V1

## 2026-11-06 — Contract V1 incident

- V1 install completed add-only.
- Runner completed 6/7 tests; only failure was `mp4_present_in_snapshot_count == 0` although the helper inspected the active project root and found 27 files.
- Root cause was audit vocabulary/assertion, not a broken selector contract. Preserve V1 receipt and failure logs.

## 2026-11-06 — V2 audit correction

- V2 distinguishes file presence in active project root from visual review.
- Windows install PASS_ADD_ONLY: 14 new files, zero replacements.
- Windows runner PASS: base pins 40/40, local pins 8/8, tests 8/8, canonical selectors 27/27.
- Report SHA `788ab1352a3e11bd91cc2ddf34fc8f11334b7713b9bc1a2b246156c79f40444e`.
- Observed MP4 presence 27/27; `VISUAL_REVIEW=NOT_PERFORMED`.

## Operator policy approvals

The operator approved all five current-hash E4B decisions (A.1, A.3, Loop composition, B.1, D.1). Approval is restricted to D-only design/contract implementation. Renderer activation, production dispatch, media and audio operations remain unauthorized; D4.8 remains BLOCKED.

## 2026-11-07 — V79 inspection / V80 integration

- V79 snapshot SHA `75987d4c353f951c2cede95b6a904355d8925e8ccd413526af3e9ad08fadc465`; ZIP CRC passed.
- Found D9.8 stale wording that left D9.9 plan-only compatibility marked pending. V80 adds explicit plan-only vs D4-executable flags, without changing D4 status.
- Put Loop bridge/envelope/family-stage preparation behind the shared E service, then had the existing GUI consume it. CLI continues to call the same service. No parallel Producer or request-schema expansion.
- Local tests 25/25 service, D9.8 model PASS, in-memory Python syntax compile PASS. All 27 Loop grammars prepared, not rendered.
- The V2 source-pinned test is not re-run after the service/GUI source postimages intentionally change; preserve V2 as historical accepted evidence.
- V79 archive D9.15 revalidation cannot resolve an evidence PNG. The live checkout must be checked read-only.

## Current boundary

Shared E service can prepare a Loop family-stage contract. It does not materialize C11-C payload, produce renderer input, call launchers, create media, invoke audio/mux or grant release authority. `family_adapter=NOT_CONNECTED_E1` and the global locks remain unchanged.
