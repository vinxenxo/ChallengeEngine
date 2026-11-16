# C11-E E5 Cross-Family Qualification Plan — V3

**Date:** 2026-11-16  
**Status:** E5 opening canary authorized; V1 installer was rejected before execution by PowerShell 5.1 AST; V2 is the corrected replacement package.

## Purpose and boundary

This is the formal opening canary for E5, not E6 Smoke18 and not a claim that all E5 acceptance is closed. It exercises one historically accepted representative selector per family through the existing shared E1 production-intent service, using GUI-origin and CLI-origin service calls. It performs no Qt user-interface session, renderer call, Godot launch, D3 V5 audio generation, FFmpeg mux, FFprobe, or media output.

The canary is PREPARE_ONLY because the current E1 family adapter remains `NOT_CONNECTED_E1`. It validates the cross-family request, source-binding, music-profile, seed-domain, family-boundary and service-origin parity contracts before a separately authorized media qualification. `E5_OVERALL` remains `OPEN_MEDIA_QUALIFICATION_REQUIRED` after this canary, even on a technical PASS.

## Pinned family representatives

| Family | Selector | Canonical source / SHA-256 | Native timing reference | Music profile / route | Gameplay seed | Music seed |
|---|---|---|---|---|---:|---:|
| Challenge | `challenges / parking_v2 / CHALLENGE_004` | `challenges/CHALLENGE_004.json` — `6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71` | 15s canonical phase sum (3+7+3+2) at 60fps; accepted delivery reference 450 frames / 15s at 30fps | `challenge_8bit_v1` / `D3_V5_CHALLENGE_8BIT_PLANNING_BINDING_ONLY` | 314159 | 840001 |
| Visual Loop | `visual_loops / c11c_fractal_bloom_v1 / radial_bloom` | `c11c-suite/c11c-producer/producer_schema.json` — `564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0` | accepted native source 660 frames / 22s at 30fps; no E5 rematerialization | `ORGANIC_BLOOM` / `PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH` | 100006 | 500006 |
| Visual Drill | `visual_drills / tracking / tier-2` | `definitions/visual_drill_tracking_canonical.json` — `54d432c80f190f4ac5dcb8ef5b135e16f18c378da120f35723fd5be944719ec3` | native gameplay 630 frames / 21s; PRE_ROLL 3s + GAME 21s + END_CTA 3s = 810 frames / 27s at 30fps | `FLOWING_VECTOR` / `PRESERVE_EXISTING_C11C_FAMILY_MUSIC_V4` | 12345 | 840001 |

All three use delivery `REVIEW_720`, presentation `social_default_v1`, audio intent enabled, personalization enabled and variation index 0. Request modes remain family-native: Challenge `REVIEW`; Loop and Drill `PRODUCTION`. E1 preparation prevents these requests from entering production dispatch.

The contract pins 31 static source/evidence files, including the frozen C11-C manifest (796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`) and PowerShell style guide V36 (65,465 bytes; SHA-256 `4f3940d50b07ccd48e30f44dbc8653a9021791d20382dbccdb7ca0d93f98f337`). The service-origin run also captures the dynamic source-pin union and checks it pre/post.

## Bulk probe matrix

Each family executes four probes, each through both GUI-origin and CLI-origin service paths: 3 families × 4 probes = 12 probe pairs / 24 service-origin rows.

| Probe | Gameplay seed | Music seed | Required relation |
|---|---|---|---|
| A | family baseline | family baseline | baseline plan |
| B | unchanged from A | unchanged from A | semantic replay of A; only request-scoped identifiers may differ |
| C | unchanged from A | changed only | independent music-seed domain |
| D | changed only | unchanged from A | independent gameplay-seed domain |

The changed C music seeds are Challenge/Drill `840002` and Loop `500007`. The changed D gameplay seeds are Challenge `314160`, Loop `100007` and Drill `12346`.

## Acceptance checks

- 12/12 GUI-origin/CLI-origin service preparation pairs have equal semantic intent hashes, equal family-boundary preparation and equivalent validated family shapes; origin-bound full intent hashes remain distinct as expected.
- 24/24 service-origin rows validate as `PASS_E1_PREPARATION_ONLY`.
- A/B semantic replay and seed pairs match independently in each family.
- C changes only `request.music_seed`; D changes only `request.seed`.
- Challenge remains on its D3 V5 planning-only route; Loop retains its existing Loop family stage/binder/music route; Drill retains its own Drill stage, V2 binder, native phase order and native END_CTA precedence.
- Three music profile IDs remain distinct: `challenge_8bit_v1`, `ORGANIC_BLOOM`, `FLOWING_VECTOR`.
- No cross-family profile, binder, grammar, gameplay seed, music seed or timeline contract leakage.
- 31 static source pins, historical evidence pins and the service-generated dynamic pin union remain stable pre/post.
- All receipts are immutable/create-new and linked by SHA-256. One fresh E5 BatchId is generated only after full preflight and output-receipt-path validation.
- Renderer, Godot, FFmpeg, production media and production dispatch remain false; `release_authority=NONE`.

## GUI qualification semantics

The canary calls the shared service directly with `request_origin="GUI"` and `request_origin="CLI"`. It also statically verifies that the current Producer GUI wires to that same service. It does **not** open the Qt Producer window or simulate a user click. The result field `actual_qt_gui_runtime` must remain `NOT_RUN_OPERATOR_UI_SESSION_REQUIRED`; this is not silently promoted to an observed GUI runtime result. Existing E4 GUI/CLI evidence remains accepted and is not repeated.

## One-shot execution and evidence

The V2 combined PowerShell 5.1 overlay performs ZIP/manifest validation, staged root reconstruction, Python 3.13 compilation, 18 exact Python tests including an isolated 24-row bulk integration run, 7 atomic-I/O tests, AST validation of every package PowerShell file, 31 static source pins and frozen manifest validation before the first repository payload write. It then commits 16 ADD_ONLY payload files and their immutable install receipt/journal before starting the real one-shot E5 PREPARE_ONLY bulk.

Active-checkout evidence root:

`artifacts/tests/c11e/e5_cross_family_prepare_canary/`

Install run directories begin `E5_INSTALL_`; the batch coordinator generates a fresh `E5-XF-PREP-...` BatchId. Never reuse a BatchId, reserved lock, failed batch directory or result-receipt path. A failure after reservation consumes that BatchId. A batch failure after installation commit does not roll back the installed add-only payload.

## Exit state

A successful opening canary records `PASS_E5_PREPARE_ONLY_CROSS_FAMILY`, 24 service-origin rows, 12 probe pairs, source-pin equality and three distinct profiles. It explicitly records `actual_qt_gui_runtime=NOT_RUN_OPERATOR_UI_SESSION_REQUIRED`, `av_media_gate=BLOCKED_FAMILY_ADAPTER_NOT_CONNECTED_E1`, `e5_overall=OPEN_MEDIA_QUALIFICATION_REQUIRED` and `release_authority=NONE`. Full E5 requires the remaining governed runtime/A-V qualification; E6 Smoke18 remains held until E5 is accepted.


## V1 package failure / one-shot disposition

The V1 install attempt failed at PowerShell parse time because its `Write-ProgressSnapshot` ordered hash literal repeated six keys. The installer body did not execute, so it did not create an install run, reserve an E5 BatchId, write a transaction journal or modify checkout payload. The V1 extraction is retained as failed input and must not be invoked again. V2 provides a separate extraction directory and a saved launcher; the launcher enforces archive member safety, outer ZIP SHA, PowerShell AST and child-process exit capture.

Use only V2. Any new V2 failure after a BatchId reservation consumes that ID. Preserve all generated evidence and do not retry.
