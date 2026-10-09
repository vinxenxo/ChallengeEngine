# C11-C Suite — Current Operator Rules / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 FROZEN
**Producer:** 0.11.1
**Catalog:** 0.2.0
**Config:** 0.2.0 integration; D9.8 model, D9.10 bridge + D-only adapter boundary, D9.11 maintenance, D9.13 lifecycle, D9.14 fail-closed gate, D9.15 operational matrix and D9.16 full-acceptance preflight registered read-only (30/30 registry validation; all-surface GUI evidence is not inferred)
**Maintenance:** 0.2.0 PASS/CLOSED for D9.11; Windows GUI opens and focused/full Suite tests pass
**Test:** 0.2.0 D9.12 route/manifest contract PASS; D9.13 lifecycle, D9.14 blocked gate, D9.15 operational preflight and D9.16 full-acceptance preflight registered; 26/26 D routes, 57 total GUI routes; Windows Test GUI and D9.14 gate route confirmed

## Architecture

`c11c-suite` is the canonical operator surface. It is composed of existing suites with separate responsibilities:

- `c11c-test` — testing, QA and acceptance.
- `c11c-producer` — production, review and job orchestration.
- `c11c-catalog` — catalog, product identity, provenance and reproduction.
- `c11c-config` — configuration, profiles, snapshots and controlled editing.
- `c11c-maintenance` — cleanup, organization, quarantine, documentation and freeze operations.

**Do not create a sixth operational suite.** The shared launcher must expose exactly these five paths and no other operational surface. The legacy `c11d-control` surface is non-canonical and must not be recreated in the live tree; any simulated legacy tree exists only inside temporary Maintenance test fixtures. Do not register or launch it.

The historical `c11c-studio` attempt is retired/archived context. It is not an implementation target, operational dependency or source of current architecture.

## GUI/CLI invariant

GUI and CLI are co-equal surfaces over the same canonical backend commands. GUI must not duplicate production, validation, media-cleanup, provenance or packaging logic.

A D capability is complete only when:

1. canonical CLI works;
2. existing Suite can invoke the same canonical path;
3. GUI inputs normalize to the same request/plan identity;
4. provenance/reproducibility is equivalent;
5. focused parity tests exist.

## Current D9 integration state

### Producer 0.11.1

D4 Request + D4.3 Challenge personalization remains integrated. The D9.9 universal editorial tab uses the same canonical adapter as the CLI and covers all 9 Challenge identities, 27 concrete Loop grammars (+ five auto selectors) and 20 Drill type/tier variants. The operator confirmed the Windows GUI generates plans for all currently implemented D types. D9.10 adds a canonical hashed bridge-planning record in the same view and requires exact GUI/CLI record parity. Challenge delegates to the existing D4 plan; Loop/Drill return declarative editorial-intent plans only, not renderable products.

### Catalog 0.2.0

D7 matrix/catalog and D9 pilot/product provenance can be inspected through the existing catalog surface. Pilot media remains validation-only and does not imply release authority.

### Config 0.2.0

D contracts and operator profiles are exposed through the existing Config surface. The read-only registry includes D9.10 bridge, D9.11 maintenance, D9.13 lifecycle, D9.14 blocked gate, D9.15 operational acceptance and D9.16 full-acceptance preflight contracts. The 30/30 registry check validates the new read-only D-only adapter boundary alongside the existing contracts. It verifies that renderer input/media remain absent, D4.8 remains BLOCKED, and release authority remains NONE. Generic editing must remain blocked for protected/canonical roots.

### Maintenance 0.2.0 target

Exposes D9-safe dry-run, two-root allowlisted reversible cleanup, legacy-surface quarantine/restore, conflict handling, documentation audit and freeze preflight through one canonical backend. Quarantine/restore is confirmation-gated, ledgered, non-overwriting and does not rewrite the historical C11-C manifest. Freeze preflight cannot create archives or grant authority. The operator confirmed Windows GUI bring-up and the focused/full Suite tests now pass; D9.11 is PASS/CLOSED.

### Test 0.2.0 target

Test 0.2.0 registers 25 D routes in 55 total GUI routes, including D2–D9 validation, seed governance, provenance, media QA, negative controls, GUI/CLI parity, no-media GUI E2E preflight, D9.13 lifecycle, D9.14 fail-closed real-media gate, D9.15 operational preflight and D9.16 full-acceptance preflight. It invokes existing canonical tests/backends and does not duplicate domain logic.

## Production authority

D4.8 remains `BLOCKED` until a future explicit governance checkpoint authorizes physical production through the D renderer. D9 GUI integration must not infer authority from successful planning or from D8/D9 pilot evidence.

## Protected C11-C boundary

Do not modify C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 semantics, logical 540×960 geometry or proven C11-C presentation/production behavior merely to support GUI integration.


## D9.8 universal editorial contract

The read-only canonical model is `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`, resolved by `tools/c11d/d9/universal_editorial_model.py`. Config may inspect/hash/validate it; it must not make generic edits to the canonical contract. Resolver coverage now reflects 9 Challenges, 5 Loop families/27 concrete grammars and 4 Drill types/20 declared tiers. Longform is shown but disabled until the D request schema supports it. D9.9 supplies a universal request identity and deterministic plan for all supported types. Operator confirmed in Windows that the GUI generates plans for all currently implemented D types without errors. D9.10 adds a deterministic bridge-planning record with GUI/CLI parity; it is not renderer input. Only Challenge embeds a canonical D4 subordinate plan; Loop/Drill remain editorial-intent plans until the future D renderer baseline. Longform remains disabled.


## D9.9 Producer universal editorial contract

Producer 0.11.1 exposes the universal editorial controls and D9.10 bridge-planning record inside the existing `c11c-producer` application. GUI and CLI call `tools/c11d/d9/universal_producer.py`; the GUI also invokes the canonical CLI as a separate process and compares the normalized request, request hash, editorial hash, plan and plan hash. The static acceptance matrix covers every live selector and 20 negative cases. The operator confirmed that both universal plan generation and the D9.10 bridge-output tab work in Windows. This certifies a plan-only adapter, not physical production: renderer and execution remain `false`, D4.8 remains `BLOCKED`, `release_authority=NONE`, and real-media GUI production acceptance remains a later D9 gate.


## D9.10 bridge + adapter preparation boundary

The Producer test GUI and `tools/c11d/d9/universal_producer_cli.py` emit the canonical bridge record and a `C11-D-D9.10-D-ONLY-RENDER-ADAPTER-ENVELOPE-V1`. The envelope is derived from the normalized D9.9 canonical request, allowlisted editorial resolution, plan and bridge identities. It exposes a hash-bound binding preview, not renderer-native input. Challenge, Visual Loop and Visual Drill each pass separate-process parity: bridge 3/3 and adapter 3/3. Bridge negative controls are 15/15; adapter-specific negatives are 9/9.

The output boundary is explicitly PREPARE_ONLY: `renderer_dispatch_invoked=false`, `renderer_input_emitted=false`, `production_execution=false`, `media_output_created=false`, `D4.8=BLOCKED`, and `release_authority=NONE`. Config exposes the adapter boundary contract read-only (30/30 contracts). The existing Producer GUI remains a test/operator GUI; the definitive GUI is deferred until after final D baseline acceptance and freeze. Automated acceptance reports and per-command logs are generated without screenshot capture, with `operator_gui_runtime_observed=false` unless an actual GUI observation is separately recorded.

## D9.13 cross-suite lifecycle

Producer's `CROSS-SUITE LIFECYCLE (D9.13 · PLAN ONLY)` view builds the canonical receipt through `tools/c11d/d9/cross_suite_lifecycle.py` from persisted request, editorial resolution, plan, bridge and GUI/CLI parity evidence. Config, Producer, Test, Catalog and Maintenance all bind the same lifecycle ID, identity SHA-256 and seed/profile binding SHA-256 in exact stage order. Catalog projects the sealed receipt as `CROSS_SUITE_LIFECYCLE_INTENT` with no media; Maintenance validates the same receipt read-only. The latest static regression passes for Challenge, Visual Loop and Visual Drill, including 12 negatives. Operator must still confirm the new Producer tab, Catalog filter and Maintenance audit button in Windows.


D9.14 adds a read-only, fail-closed real-media certification gate to the existing Producer/Test surfaces. The gate is expected to stay BLOCKED until a separately approved future D frozen renderer baseline and an explicit D4.8 governance checkpoint exist. The gate route is preflight-only, exposes the ten required cases, and cannot create media, invoke a renderer or grant authority.


## D9.15 operational acceptance (preflight ready; operator confirmation required)

`tools/c11d/d9/gui_operational_acceptance.py` performs a side-effect-free structural preflight over the exact five canonical surfaces and eight operator capabilities. `c11c-test` exposes `D9.15 GUI OPERATIONAL ACCEPTANCE PREFLIGHT (PLAN ONLY)` and Config registers the canonical matrix read-only. A static PASS is not closure: collect Windows GUI evidence for Config, Producer, Test, Catalog and Maintenance. Keep D9.14 real-media gate blocked; no real media, renderer or release authority is implied.


## D9.14–D9.16 acceptance boundaries

D9.14 is operator-confirmed visible/executable in Producer and Test, but **real-media certification remains BLOCKED**. D9.15 structural preflight passes (8 capabilities/5 surfaces, 19 negatives), while recorded GUI evidence for all five surfaces is still required. D9.16 adds `D9.16 FULL D9 ACCEPTANCE PREFLIGHT (NO MEDIA)` in Test and a read-only Config registration; its static acceptance is deliberately `PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED`, with 9/9 evidence routes and 21 negative controls. It does not close D9, fabricate operator evidence, create media or grant release authority. The current aggregate Suite self-test has 21 steps; D9.10 bridge and D-only adapter assertions are integrated in the existing `bridge_test` step (no additional suite or step).

## D baseline candidate evaluation route (2026-10-09)

The existing `c11c-test` surface includes `D BASELINE CANDIDATE INTEGRITY PREFLIGHT (NO FREEZE)`, and Config exposes `D_BASELINE_CANDIDATE_POLICY` read-only. This is a source-integrity/governance preflight, not a freeze operation. It checks the preserved C11-C manifest and protected source hashes while reporting blockers to D freeze eligibility. It must not create release archives/media, activate a renderer, unlock D4.8, or grant authority. The expected passing status is `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED`.

## Current D9.10 and D9.14 update — 2026-10-09

D9.10 now has a D-only adapter **prepare-only** boundary: canonical request → editorial personalization → plan → bridge → hash-bound binding preview. Adapter parity is 3/3, adapter-specific negatives 9/9, Config is 30/30, and the adapter test is part of the current aggregate `bridge_test`. The output is not renderer-native input and cannot dispatch. A no-screenshot automated acceptance runner is available at `tools/c11d/d9/capture_d910_acceptance.py`; it stores a report and per-check logs and marks `operator_gui_runtime_observed=false` honestly.

D9.14 bounded production qualification subsequently passed on Windows using existing verified production launchers: four final A/V MP4s, eight checks, sealed qualification-baseline SHA-256 `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`. This does not close the full D9.14 GUI/end-to-end gate or authorize general D renderer use. C11-C 2.19.12 remains immutable, D4.8 remains BLOCKED, the Producer UI remains test-only, the definitive GUI is deferred until after baseline freeze, and `release_authority=NONE`.

## D9.10 automated Qt runtime acceptance (2026-10-09)

`tools/c11d/d9/test_d910_gui_runtime_contract.py` is a dependency-free static contract and is registered as step 22/22 in `c11c-suite/self_test.py`. On Windows, the optional `test_d910_gui_runtime_acceptance.py` instantiates the actual Producer test/operator GUI offscreen and executes the same D9.10 callback for Challenge, Visual Loop and Visual Drill. It verifies editorial override propagation, parity and the prepare-only adapter locks without screenshots or media. Include it in the bound report with `capture_d910_acceptance.py --include-qt-gui-runtime --include-aggregate`. This is not the definitive GUI and does not authorize renderer dispatch or close D9.14.

## D9.10 Qt runtime status — operator result (2026-10-09)

The dependency-free harness contract is PASS and `c11c-suite/self_test.py` passed 22/22. The separate offscreen Qt runner failed 0/3 content types, and the combined report failed 6/7 because the optional runtime check failed. The aggregate result therefore verifies the static safety contract only. Diagnose the recorded exception and logs before reporting runtime PASS; screenshots are not required and production remains forbidden in the harness.
