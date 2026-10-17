# C11-D Challenge Visual Payload Materializer V2 — Design Proposal

**Status:** `PROPOSED_NOT_IMPLEMENTED_NOT_APPROVED_NOT_FROZEN`  
**Purpose:** Define a test-first, source-driven V2 path for Challenge visual-payload preparation without broadening the accepted V1 binder in place, changing frozen C11-C, emitting renderer-native input, or creating media.

## Why a distinct V2 is required

The Challenge seed-domain planner preflight passed for all nine canonical selectors, but planner support is not runtime-payload support. The current `tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py` still declares the Challenge expected selection as `parking_v2 / CHALLENGE_004`. The accepted V1 Godot harness `tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd` pins `CHALLENGE_004.json`, its `parking_v2` mechanics dependencies, three specific assets, 60 FPS and a 900-frame/15-second HOOK+GAME+REVEAL+CTA timeline. The related V1 tests and contract correctly reject any drift from that scope. Do not relax these assumptions in place.

The canonical definitions are also mechanically heterogeneous. `ChallengeRuntimeBridge.gd` explicitly routes `pilot`, `parking_v2`, `hit_v1`, `catch_v1`, `find_v1`, `count_v1`, and `choose_v1` through its native-V2 mechanic path; `key` and `parking` use the other bridge path. That observed dispatch split is a test requirement, not a claim that all nine routes produce interchangeable snapshots. Payload support must be demonstrated per selector/mechanic and fail closed where unsupported.

## Proposed architecture (additive)

1. **Canonical selector and plan input.** Consume the accepted D9.9 universal planner and existing editorial-selection resolver; do not implement a second selector catalog or duplicate the planner. Carry the selector, canonical source identity and validated gameplay/music seed domains separately.
2. **Versioned V2 orchestration.** Add a new Challenge-specific V2 contract, schemas, Python orchestrator, tests and Godot in-memory harness. Reuse selector-agnostic canonical request / bridge / D-only adapter helpers where signatures support the required selector. Where V1 helpers encode a fixed selector or shape, do not bypass their guards or clone the whole 1,378-line V1 binder; provide a narrow V2 path or a separately tested shared helper whose V1 regression stays green.
3. **Per-selector exact lineage.** Pin the frozen manifest; Challenge JSON bytes; canonical D9.9/D4 inputs; runtime bridge and timeline builder; presentation binder/profile; `FrameSnapshot`; actual mechanic code and RNG path; and every declared asset loaded. Report hashes from the active checkout at test time. Asset paths must come from the pinned Challenge definition, be root-confined, be allowlisted, resolve to real files, and be hashed before loading. No fuzzy/fallback assets.
4. **Mechanic capability matrix.** Cover `CHALLENGE_001/key`, `002/parking`, `003/pilot`, `004/parking_v2`, `005/hit_v1`, `006/catch_v1`, `007/find_v1`, `008/choose_v1`, and `009/count_v1`. Inventory differences in definition shape, mechanics dispatch, asset roles, relevant snapshot fields, and returned frame cardinality before claiming support. Do not assume a fixed three-node asset list or a fixed 420-frame GAME segment for every selector.
5. **Source-frame receipt separated from temporal presentation.** First prove the authentic runtime route, deterministic source-frame receipt and safe visual-state projection at the mechanic's source timebase. Only assemble a phase-bound presentation payload when phase ordering and total duration are coherent and explicitly supported. Preserve native source FPS, frame indices and source timeline; do not downsample to delivery FPS, apply coordinate projection, infer timing from `winning_frame`, or interpret `close_calls` as timing.
6. **Deterministic payload projections.** Produce hashes for (a) request, (b) plan/adapter lineage, (c) safe simulation-frame signature, (d) asset/source binding, and (e) the assembled source-timebase semantic payload where eligible. Whole envelope hashes are expected to change with request seed identities; tests must compare the intended visual subprojection to test music-seed orthogonality.
7. **Strictly in-memory review.** Resource loading and Dictionaries/Arrays are allowed only within the review harness. No render nodes, shaders, `RenderingServer`, viewport capture, file output, renderer-native command, dispatch, export or media. Output must state renderer input `false`, media `false`, release authority `NONE`, and candidate admissibility `false`.

## Seed matrix and required semantics

For each selector with a demonstrably supported runtime route, use explicit controlled cases:

- baseline: gameplay seed `12345`, music seed `840001`;
- gameplay-only mutation: gameplay seed `54321`, music seed `840001`;
- music-only mutation: gameplay seed `12345`, music seed `840002`.

Use two independently launched Godot processes per case when evaluating runtime receipts/payloads, not two calls in one process masquerading as independent runs. A full nine-selector × three-case × two-run matrix is 54 runtime invocations; if a selector is blocked or cannot consume the intended input safely, report its explicit blocking reason rather than silently shrinking the denominator.

Acceptance semantics: identical selector/seed/source pins repeat identically; changing gameplay seed changes request/plan identity and, where the frozen mechanic accepts that seed, changes the safe visual simulation projection; changing music seed changes request/plan identity but leaves the visual simulation projection identical. If an existing mechanic cannot express the seed or the bridge ignores it, that is a fail/blocked row requiring source-level resolution—not a fabricated mutation. Editorial identity must remain invariant across the seed-only pairs.

## Explicit temporal conflict handling

`CHALLENGE_008` (`choose_v1`) and `CHALLENGE_009` (`count_v1`) each declare `total_duration=11s`, while `hook_duration=3s + game_duration=7s + reveal_duration=0s + cta_duration=2s = 12s`. Do not change these files, infer whether the total or segment sum wins, or allow a `PASS` for assembled phase-timebase payloads before the shared temporal-policy decision. The source-frame receipt and seed-projection subtests may run only if they can be cleanly isolated from phase timing; their evidence must not imply timeline acceptance. The other seven definitions still require an explicit source-timebase validation rather than a universal assumed duration.

## Test-first gates

**V2-A: Static contract and source matrix.** Validate schemas; exact selector set; 9 Challenge hashes; path confinement; all referenced source/asset pins; actual mechanic dispatch classification; source-FPS/timeline arithmetic; governance locks; negatives for selector mismatch, modified source, unknown asset, path traversal, missing mechanic dependency, invalid seed, repeated-seed mismatch and attempted approval. Python only; no Godot.

**V2-B: Canonical planner / adapter parity.** Reuse D9.9 and D4 paths. Verify request/plan seed identity, D4 parity and editorial invariance; zero payload calls. Keep the accepted 20-test preflight unchanged and regression-test it.

**V2-C: Runtime source-frame receipts.** Godot 4.7.1 active Windows only, exact source pins. Per mechanic: first/repeat runtime, frame/snapshot shape, expected invariants and bounded allowlisted assets. Record separate exit code, stdout/stderr hashes, report hashes, Godot version, and invocation count. No renderer or media.

**V2-D: Eligible semantic payloads and seed variants.** Create source-timebase in-memory payloads only for selectors whose runtime and timebase are demonstrably coherent. For `CHALLENGE_008/009`, keep phase payload status blocked while separately reporting any permissible source-frame/seed evidence. Assert gameplay visual sensitivity, music visual orthogonality and independent-repeat equality at the correct visual subprojection.

**V2-E: Regressions and closure.** Re-run V1 Challenge payload tests, Visual Loop exact-selector/seed-domain tests, Visual Drill V2 tests, C11-C manifest pin, D4 parity, PowerShell parse tests if scripts changed, and the relevant unified suite. No test gate authorizes renderer activation or candidate admission.

## Acceptance report minimums

The report must publish explicit counts and per-selector statuses rather than a single misleading aggregate: selectors inventoried; runtime routes supported/blocked; exact source pins; repeat pairs; request/plan seed sensitivity; safe visual sensitivity; music orthogonality; asset bindings; frame records/hashes; timeline conflicts; payloads assembled/blocked; Godot calls; payload/media files written; renderer-native inputs; policy values consumed; candidate admissibility and all authority locks.

## Out of scope

No editing of C11-C, simulation truth, RNG algorithm/ownership, gameplay semantics, `winning_frame`, `close_calls`, challenge definitions, D9.9 canonical planner, accepted Challenge V1 contract, Visual Loop/Drill V2 contracts or any release/freeze authority. No renderer implementation, first render or media.
