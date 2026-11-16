# C11-E E6 Smoke18 Scope Plan — V1

**Phase:** E6 Smoke18  
**Status:** `PLAN_PREPARATION_ONLY / MEDIA_EXECUTION_HELD`  
**Entry:** E5 `PASS_CLOSED_TEST_ONLY` (2026-11-16)  
**Target:** 18 audiovisual smoke scenarios, six per family, as specified by the current E roadmap V114.

## 1. Definition and reconciliation

The current C11-E roadmap defines E6 Smoke18 as exactly 18 A/V scenarios: six Challenge, six Visual Loop and six Visual Drill. An older C11-D recovery plan described an 18-output split of nine Challenge, five Loop and four Drill; that is a historical D-plan definition and is not the current E6 matrix. E6 follows the current E roadmap, not the old D-plan split.

E6 is a representative smoke gate, not the full E7 Matrix101 and not a substitute for E8's row-by-row historical C-to-E regression.

## 2. Candidate selector pool (not yet frozen)

These are candidates for read-only selection review. They are not execution requests, not reservations, not BatchIds and not approval to render. Final six-per-family membership must be frozen only after checking current active-checkout selector definitions, family contracts, source pins, timebases, A/V qualification receipts and historical reuse eligibility.

### Challenge — candidate pool

`CHALLENGE_001`, `CHALLENGE_002`, `CHALLENGE_003`, `CHALLENGE_004`, `CHALLENGE_005`, `CHALLENGE_006`, `CHALLENGE_007`.

`CHALLENGE_008` and `CHALLENGE_009` are excluded pending authoritative resolution of declared 11 seconds versus phase sum 12 seconds. E5 representative `parking_v2/CHALLENGE_004` is an accepted family anchor; whether it counts as one of the six smoke cases must be decided by the E6 test contract rather than silently double-counted.

### Visual Loop — candidate pool

- `c11c_fractal_bloom_v1 / radial_bloom` — gameplay seed 100006, family music seed 500006; E5 representative and approved.
- `c11c_geometric_waves_v1 / harmonic_membrane` — gameplay seed 100001, music seed 500001; five-family pilot representative.
- `c11c_invisible_forces_v1 / dipole_field` — gameplay seed 100021, music seed 500021; five-family pilot representative.
- `c11c_living_particles_v1 / swarm` — gameplay seed 100016, music seed 500016; five-family pilot representative.
- `c11c_sacred_symmetry_v1 / astrolabe` — gameplay seed 100011, music seed 500011; five-family pilot representative.
- `c11c_geometric_waves_v1 / interference_plane` — gameplay seed 100002, music seed 500002; selector present in the accepted E4B 22-selector matrix.

The Loop matrix retains each selector's family music profile and grammar. Do not infer a generic shared family binder or change music routes.

### Visual Drill — candidate pool

- `tracking / tier-2` — E5 representative; accepted E4C technical A/V receipt `f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7`.
- `pursuit / tier-1` — accepted E4C receipt `57206b4560b917c7a7fe5e738c5afd5d900d293e01c99fcd554f0926acc6eee7`.
- `saccade / tier-1` — accepted E4C receipt `930ba103153fbca0226a0b7abd1226b46dfd3c2e523204e83e6cb39f1282e606`.
- `peripheral_scan / tier-1` — accepted E4C receipt `eb290666163df0e89daac9c683a95a39c38d536c5da735def15cd3a19964083b`.
- `tracking / tier-5` — accepted E4C receipt `6e55dc3fd4fc13745347cc641d29103fbfb7fa90dee932910f920703690c3c61`.
- `peripheral_scan / tier-5` — accepted E4C receipt `5644ffa386c2d1388e7dd657cb566c796a87de93b22c28db84197b8ad3a224`.

These Drill receipts are prior E4C A/V evidence. Reuse may be counted only if the E6 test contract explicitly permits receipt reuse and validates all E6-required fields; do not rerun an accepted E4C BatchId merely to populate E6.

## 3. E6 acceptance contract to define before execution

The pre-execution contract must explicitly specify:

1. Exact six selector identities per family and canonical source hashes.
2. Per-scenario source timebase, expected output profile, frame/duration constraints and family-specific binder/timeline/music profile.
3. Gameplay and music seeds from existing canonical authority; no invented seed derivation and no cross-domain sharing.
4. Whether an accepted E4/E5 A/V artifact can satisfy an E6 scenario, or whether a fresh E6 output is required. The rule must be identical across comparable scenarios and documented before launch.
5. Exact family-owned executor entrypoints and their source pins; no generic renderer shortcut or new Producer/binder.
6. FFprobe metadata, video pixel/geometry/rate/timebase, audio codec/rate/channel/non-silence and A/V offset rules.
7. Visual/editorial/layout/music operator review receipts and failure/partial-run preservation policy.
8. Unique E6 run identity, output roots and immutable receipt locations. Reserve a one-shot BatchId only after all read-only checks pass.

## 4. Execution authorization conflict — hard stop

The pinned `definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json` has SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`. Its exact authority is ten silent C11-C qualification launcher invocations over five selectors with A/B repeats. It explicitly prohibits `smoke18_or_matrix99`, D3/music generation, PCM audio generation, FFmpeg filters/mux, D compositor dispatch and general renderer activation. D4.8 remains `BLOCKED`.

Therefore this V1 is **not** an E6 media-execution authorization. No E6 renderer, Godot, D3 audio, FFmpeg encode/filter/mux, media generation or dispatch may run under the existing R1V-only approval. Do not change, replace or reinterpret that policy.

Before Smoke18 media execution, complete a separate read-only audit of existing family-specific A/V qualification entrypoints and submit a distinct `E6_SMOKE18_TEST_ONLY` authorization proposal with exact source pins, selectors, run count, tool invocations, outputs and prohibitions. Require explicit operator approval of that bounded scope and a separate governance review. If a safe test-only seam cannot be proven without violating D4.8 or family contracts, stop and keep E6 held.

## 5. Current actions allowed

- Documentation and roadmap reconciliation.
- Read-only selector/receipt/source inventory.
- Pin and output-collision preflight that writes no source files, reservations, locks or media.
- Design of the bounded E6 authorization proposal.

Not allowed at this stage: any E6 media execution, audio generation, mux, renderer activation, production dispatch, release or promotion.

## 6. Downstream

E7 Matrix101 follows accepted E6: 54 Challenge + 27 Loop + 20 Drill. `CHALLENGE_008/009` remain held on the 11s/12s conflict; 99 provisional runnable. E8 remains historical C-to-E regression, independent acceptance, immutable freeze and a separately authorized transition decision.
