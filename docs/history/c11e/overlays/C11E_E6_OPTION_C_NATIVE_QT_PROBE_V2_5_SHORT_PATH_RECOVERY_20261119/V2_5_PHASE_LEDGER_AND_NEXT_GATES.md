# C11-E E6 — phase ledger and next gates — V22

Date: 2026-11-19. This ledger supersedes V21 for the Option C Qt probe installer incident only; it does not supersede governance or authorize media execution.

## Current exact state

| Item | State | Evidence / constraint |
|---|---|---|
| C11-C 2.19.12 | FROZEN / IMMUTABLE | 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` |
| D4.8 V2 | BLOCKED / UNCHANGED | 12,996 bytes / SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` |
| Option C | Operator-approved D-only post-compositor | Source C immutable; distinct D output |
| Geometry V3 | APPROVED_GEOMETRY_RETAINED_RESAMPLER_IMPLEMENTATION_ONLY | 720x1280 canvas; body 504x896 at (108,192); black header/footer and side gutters |
| Python compositor V4 | NOT HOT-PATH QUALIFIED | P95 2050.1467 ms / about 0.48777 fps |
| V2.1 | INSTALL PASS; RUNNER BLOCKED | A3 check stopped before QImage; preserve receipt |
| V2.2 | INSTALL PASS; RUNNER BLOCKED | Generic `support` import error; preserve receipt |
| V2.3 | INSTALL PASS; 13/13 focused tests PASS; RUNNER BLOCKED | A3 old expected/actual domains were incorrectly equated; preserve receipt |
| V2.4 | NOT INSTALLED; EXTRACTION FAILED | `Expand-Archive` failed at a 276-character path; no installer receipt; no V2.4 tests or runner executed |
| V2.5 | PATH-RECOVERY OVERLAY BUILT; TARGET INSTALL PENDING | Retains V2.4 A3/runner/tests byte-identically; short outer extraction, internal stage and same-directory temp paths |
| QImage 37-test suite | NOT RUN | Existing payload is reused by exact path |
| Native Qt benchmark | NOT RUN | Seven target iterations required |
| Resampler quality | NOT APPROVED | Geometry approval does not qualify filtering quality |
| E6 accepted | 0 | Synthetic tests are not Smoke18 rows/videos |
| Renderer / dispatch / media | OFF | Exact successor policy and E6 TEST_ONLY manifest required first |
| E1 / D9.10 | PREPARE_ONLY | No dispatch |
| D9.14 / D9.16 | BLOCKED | No bypass |
| D9.17 | BLOCKED_NO_GO | No bypass |
| D10 | BLOCKED_FOR_PROMOTION | `release_authority=NONE` |

## V2.4 incident analysis

The operator selected a deep Downloads extraction directory. The V2.4 ZIP's longest member path is 175 characters; the absolute target reached 276 characters, beyond the reliable Windows PowerShell 5.1/.NET Framework extraction path. `Expand-Archive` failed before the installer script existed at the requested `-File` path. The subsequent PowerShell process exit is downstream and is not an installer transaction result. No receipt was emitted. V2.5 also hardens V2.4's latent internal stage path and long destination-derived `.partial.<GUID>` path before any destination write.

## Ordered gates

1. Install V2.5 add-only using the `%TEMP%\c11e25` extraction root after absolute-path preflight. Verify PowerShell 5.1 AST, immutable pins, 20 manifest rows / 21 ZIP members, stage/write path budgets and 18/18 destination postimages.
2. Run the 17 V2.4 focused regression tests once. Preserve full output.
3. Run the V2.4 native Qt/QImage runner once: Python 3.13.14, PySide6 6.11.2, seven iterations. Require A3 PASS, all source/evidence pins PASS, QImage 37/37 and P95 <=33.333 ms.
4. Inspect the three synthetic previews; explicitly approve or decline resampler quality. Geometry V3 approval is not filtering-quality approval.
5. Perform read-only source closure on the real immutable C Loop input and D9.9/D9.10/R1P metadata: exact frame source, ordered frame stream, RGB24 bytes, stride, dimensions, colour contract, selector identity and hash pins. Do not assume a decoder or path.
6. Separately prepare and obtain approval for a bounded successor to D4.8 and an exact E6 TEST_ONLY execution manifest (executable path/hash/version/args, exact inputs, output roots, process counts, prohibited side effects, stop-on-first-failure and one-shot identity). D4.8 V2 itself remains untouched and BLOCKED.
7. Only after those gates, one copied real frame at the existing D seam (L2), negative controls and human review (L3), then six Loop selectors with the same consumer (L4). Smoke18 integration is a later separately gated step (L5), not enabled by QImage PASS.
8. Continue the wider D+E replacement roadmap: preserve Challenge/Loop/Drill family contracts, E5 cross-family seed isolation and GUI/CLI parity, E6 Smoke18, E7 Matrix101 and E8 independent historical acceptance plus separate promotion decision.

## Coverage and family architecture

Smoke18 remains 18 top-level rows (six per family), not a complete historical regression. Thirteen reuse candidates remain candidates, zero E6 accepted. Six Loop A/V closeout artifacts are reuse candidates; six Smoke18 D-composited Loop outputs are outstanding. Five fresh Challenge A/V outputs remain. Six Drill A/V closeouts are reuse candidates, not Smoke18 acceptance. CH_008/009 remain held (11-second declaration vs 12-second phase sum); Matrix101 is not frozen.

The D+E replacement remains a complete factory replacement, not just a compositor: shared E1 service plus distinct Challenge, Loop and Drill mechanics/timelines/binders, presentation/editorial layer, family-correct music, authorized delivery encoding/mux, FFprobe/audio QA, manifests, sidecars, review and receipts. `request.seed` and `request.music_seed` remain orthogonal. Do not add a second Producer, family binder, adapter or sixth module.

## Permanent governance

Active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is sole authority. ZIPs are evidence, never extracted over checkout. No Git checks; operator commits; source-file pins enforced. No protected C11-C generator/mechanics/core audio/frozen-manifest changes. No Godot, FFmpeg, FFprobe, audio generation, mux, renderer, dispatch, BatchId or production media in this phase. `e6_accepted=0`; `release_authority=NONE`.
