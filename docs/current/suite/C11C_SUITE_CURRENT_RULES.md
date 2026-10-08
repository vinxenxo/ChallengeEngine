# C11-C Suite — Current Operator Rules / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 FROZEN
**Producer:** 0.10.0
**Catalog:** 0.2.0
**Config:** 0.2.0 integration; canonical D9.8 model registered read-only (Windows confirmation still tracked by D9)
**Maintenance:** current C11-C operator baseline; D9 target 0.2.0
**Test:** current C11-C operator baseline; D9 target 0.2.0

## Architecture

`c11c-suite` is the canonical operator surface. It is composed of existing suites with separate responsibilities:

- `c11c-test` — testing, QA and acceptance.
- `c11c-producer` — production, review and job orchestration.
- `c11c-catalog` — catalog, product identity, provenance and reproduction.
- `c11c-config` — configuration, profiles, snapshots and controlled editing.
- `c11c-maintenance` — cleanup, organization, quarantine, documentation and freeze operations.

**Do not create a sixth operational suite.** The shared launcher must expose exactly these five paths and no other operational surface. The `c11d-control` folder present in the incoming D9.7.2 archive is a legacy/unregistered path, not a canonical suite; do not register or launch it. Archive/quarantine reconciliation must go through Maintenance because the incoming freeze manifest references that path.

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

### Producer 0.10.0

D4 Request + D4.3 Challenge personalization is integrated into the existing producer GUI. Universal editorial coverage across all content families is the next D9 stage.

### Catalog 0.2.0

D7 matrix/catalog and D9 pilot/product provenance can be inspected through the existing catalog surface. Pilot media remains validation-only and does not imply release authority.

### Config 0.2.0

D contracts and operator profiles are exposed through the existing Config surface. Generic editing must remain blocked for protected/canonical roots.

### Maintenance 0.2.0 target

Will expose D9-safe cleanup, quarantine, organization and freeze workflows without deleting evidence or bypassing guards.

### Test 0.2.0 target

Will register D2–D9 contracts and GUI E2E acceptance without becoming a second backend.

## Production authority

D4.8 remains `BLOCKED` until a future explicit governance checkpoint authorizes physical production through the D renderer. D9 GUI integration must not infer authority from successful planning or from D8/D9 pilot evidence.

## Protected C11-C boundary

Do not modify C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 semantics, logical 540×960 geometry or proven C11-C presentation/production behavior merely to support GUI integration.


## D9.8 universal editorial contract

The read-only canonical model is `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`, resolved by `tools/c11d/d9/universal_editorial_model.py`. Config may inspect/hash/validate it; it must not make generic edits to the canonical contract. Resolver coverage now reflects 9 Challenges, 5 Loop families/27 concrete grammars and 4 Drill types/20 declared tiers. Longform is shown but disabled until the D request schema supports it. Only Challenge is currently D4 request/plan compatible; Loop/Drill GUI/CLI plan support belongs to D9.9.
