# C11-C Suite — Current Operator Rules / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 FROZEN
**Producer:** 0.11.1
**Catalog:** 0.2.0
**Config:** 0.2.0 integration; D9.8 model, D9.10 bridge, D9.11 maintenance, D9.13 lifecycle and D9.14 fail-closed gate registered read-only (25/25 static registry validation; Windows Config Qt acceptance still pending)
**Maintenance:** 0.2.0 PASS/CLOSED for D9.11; Windows GUI opens and focused/full Suite tests pass
**Test:** 0.2.0 D9.12 route/manifest contract PASS; D9.13 lifecycle and D9.14 blocked gate registered; 23/23 D routes, 53 total GUI routes; Windows Test GUI bring-up not explicitly confirmed

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

D contracts and operator profiles are exposed through the existing Config surface. The read-only registry now includes the D9.10 editorial-render bridge contract and validates that renderer input/media remain absent, D4.8 remains BLOCKED, and release authority remains NONE. Generic editing must remain blocked for protected/canonical roots.

### Maintenance 0.2.0 target

Exposes D9-safe dry-run, two-root allowlisted reversible cleanup, legacy-surface quarantine/restore, conflict handling, documentation audit and freeze preflight through one canonical backend. Quarantine/restore is confirmation-gated, ledgered, non-overwriting and does not rewrite the historical C11-C manifest. Freeze preflight cannot create archives or grant authority. The operator confirmed Windows GUI bring-up and the focused/full Suite tests now pass; D9.11 is PASS/CLOSED.

### Test 0.2.0 target

Test 0.2.0 registers D2–D9 validation, seed governance, provenance, media QA, negative controls, GUI/CLI parity, a no-media GUI E2E certification preflight, D9.13 lifecycle tests and the D9.14 fail-closed real-media certification gate. It invokes existing canonical tests/backends and does not duplicate domain logic.

## Production authority

D4.8 remains `BLOCKED` until a future explicit governance checkpoint authorizes physical production through the D renderer. D9 GUI integration must not infer authority from successful planning or from D8/D9 pilot evidence.

## Protected C11-C boundary

Do not modify C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 semantics, logical 540×960 geometry or proven C11-C presentation/production behavior merely to support GUI integration.


## D9.8 universal editorial contract

The read-only canonical model is `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`, resolved by `tools/c11d/d9/universal_editorial_model.py`. Config may inspect/hash/validate it; it must not make generic edits to the canonical contract. Resolver coverage now reflects 9 Challenges, 5 Loop families/27 concrete grammars and 4 Drill types/20 declared tiers. Longform is shown but disabled until the D request schema supports it. D9.9 supplies a universal request identity and deterministic plan for all supported types. Operator confirmed in Windows that the GUI generates plans for all currently implemented D types without errors. D9.10 adds a deterministic bridge-planning record with GUI/CLI parity; it is not renderer input. Only Challenge embeds a canonical D4 subordinate plan; Loop/Drill remain editorial-intent plans until the future D renderer baseline. Longform remains disabled.


## D9.9 Producer universal editorial contract

Producer 0.11.1 exposes the universal editorial controls and D9.10 bridge-planning record inside the existing `c11c-producer` application. GUI and CLI call `tools/c11d/d9/universal_producer.py`; the GUI also invokes the canonical CLI as a separate process and compares the normalized request, request hash, editorial hash, plan and plan hash. The static acceptance matrix covers every live selector and 20 negative cases. The operator confirmed that both universal plan generation and the D9.10 bridge-output tab work in Windows. This certifies a plan-only adapter, not physical production: renderer and execution remain `false`, D4.8 remains `BLOCKED`, `release_authority=NONE`, and real-media GUI production acceptance remains a later D9 gate.


## D9.10 bridge-planning boundary

The Producer tab displays the canonical `C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-PLAN-V1` record from `tools/c11d/d9/editorial_render_bridge.py`. The same record is emitted by `universal_producer_cli.py` and compared by hash/content in GUI/CLI parity. `renderer_input_emitted=false`, `renderer_adapter_invoked=false`, `media_output_created=false`, `D4.8=BLOCKED`, and `release_authority=NONE` are mandatory. The newly added bridge output tab's interactive Windows check is a checkpoint-level operator action; previous D9.9 plan-creation confirmation does not constitute real-media GUI acceptance.


## D9.13 cross-suite lifecycle

Producer's `CROSS-SUITE LIFECYCLE (D9.13 · PLAN ONLY)` view builds the canonical receipt through `tools/c11d/d9/cross_suite_lifecycle.py` from persisted request, editorial resolution, plan, bridge and GUI/CLI parity evidence. Config, Producer, Test, Catalog and Maintenance all bind the same lifecycle ID, identity SHA-256 and seed/profile binding SHA-256 in exact stage order. Catalog projects the sealed receipt as `CROSS_SUITE_LIFECYCLE_INTENT` with no media; Maintenance validates the same receipt read-only. The latest static regression passes for Challenge, Visual Loop and Visual Drill, including 12 negatives. Operator must still confirm the new Producer tab, Catalog filter and Maintenance audit button in Windows.


D9.14 adds a read-only, fail-closed real-media certification gate to the existing Producer/Test surfaces. The gate is expected to stay BLOCKED until a separately approved future D frozen renderer baseline and an explicit D4.8 governance checkpoint exist. The gate route is preflight-only, exposes the ten required cases, and cannot create media, invoke a renderer or grant authority.
