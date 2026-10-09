# C11-C Suite — Tooling Matrix / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 frozen

## Active surfaces

| Surface | Responsibility | D9 current state | Target |
|---|---|---|---|
| `c11c-test` | QA / regression / acceptance | Test 0.2.0; legacy C11-C routes preserved + 25 D routes / 55 total GUI routes, negative/parity bundles, no-media E2E preflight, D9.14 blocked gate, D9.15 operational preflight and D9.16 full-acceptance preflight; Test GUI gate launch/execute confirmed on Windows | 0.2.0 |
| `c11c-producer` | production / review / job orchestration | 0.11.1; D4 GUI preserved + D9.9 universal editorial, D9.10 plan-only bridge, D9.13 lifecycle receipt and D9.14 blocked certification-gate view (Windows confirmed) | D9.9 selector matrix and D9.10 bridge contract/CLI parity PASS; operator-confirmed Windows plan-only bridge output tab |
| `c11c-catalog` | catalog / product / provenance / reproduction | 0.2.0; D7 + D9 pilot coverage integrated | 0.2.x |
| `c11c-config` | configuration / profiles / snapshots | 0.2.0; D9.8 model + D9.10 bridge + D9.11 maintenance + D9.13 lifecycle + D9.14 blocked gate + D9.15 operational matrix and D9.16 full-acceptance gate registered read-only; 27/27 contracts validate; all-surface Windows GUI evidence pending | 0.2.x |
| `c11c-maintenance` | cleanup / organization / quarantine / freeze | 0.2.0 D9.11 PASS/CLOSED; operator-confirmed Windows GUI and full Suite acceptance passed | 0.2.0 |

## Canonical D routes

| Capability | GUI surface | Canonical backend | Certification state |
|---|---|---|---|
| D4 request construction | Producer | D4 request/normalization | integrated |
| D4.3 Challenge personalization | Producer | D4.3 personalization resolver | integrated |
| D4 plan identity | Producer | D4.4 canonical orchestrator | integrated |
| D7 catalog inspection | Catalog | canonical catalog/identity | integrated |
| D9 pilot product inspection | Catalog | D9 acceptance/provenance | integrated |
| D9 configuration contracts | Config | D2–D9 contract registry (read-only, 27 contracts) | D9.10–D9.16 invariants registered; 27/27 Config contracts PASS; Windows Config GUI acceptance pending |
| D9.8 universal editorial model | Config (read-only registry) + shared resolver | `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` + `tools/c11d/d9/universal_editorial_model.py` | model/resolver and negative matrix PASS |
| D9.9 universal Producer | Existing Producer GUI + CLI | `tools/c11d/d9/universal_producer.py` + `tools/c11d/d9/universal_producer_cli.py` | all current selectors resolve; CLI process parity per type; plan-only; Windows GUI plan creation confirmed by operator |
| D9.10 bridge planning | Existing Producer GUI + CLI | `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` + `tools/c11d/d9/editorial_render_bridge.py` | 3/3 content types; bridge-record CLI parity 3/3; 15 negatives; renderer input/media not emitted; Windows plan-only output-tab check confirmed by operator |
| D9 real GUI production | Producer/Test | future D renderer authority | pending |
| D9 maintenance operations | Maintenance 0.2.0 + canonical backend | `tools/c11d/d9/maintenance.py` | PASS/CLOSED; Windows GUI and Windows focused/full regression confirmed by operator |
| D9 GUI E2E | Test 0.2.0 | `docs/current/d/D9_GUI_E2E_CERTIFICATION_PLAN_V1.md` + canonical backends | preflight route PASS; real-media GUI execution remains a later D9.14 gate |

## Existing C11-C routes remain authoritative

The Suite continues to invoke the existing C11-C canonical production/review/QA commands. D9 integration must wrap them rather than clone their behavior.

## Retired/historical

`c11c-studio` is historical/retired. It must not be revived as a current operational suite. `c11d-control` is not present as a live canonical surface; Maintenance test fixtures simulate any retired legacy tree only in temporary storage. The shared launcher must expose exactly the five canonical surfaces. Never recreate/register the legacy surface in the live tree; the historical C11-C manifest remains read-only.

## D9 acceptance evidence requirements

For any new GUI capability, retain:

- canonical request/plan evidence;
- GUI/CLI parity evidence;
- provenance evidence;
- reproducibility evidence;
- negative-control evidence;
- physical media evidence when a D renderer is authorized;
- protected-root mutation evidence.


## D9.8–D9.9 content contract (static model and Producer plan state)

| Content type | Live inventory | Editable model | Current canonical D4 plan path |
|---|---|---|---|
| Challenge | 9 challenge IDs | title/subtitle/CTA/language/player name/challenge label | Supported by current D4 request path |
| Visual Loop | 5 families / 27 concrete grammars (`auto` excluded from grammar count) | title/subtitle/CTA/language | D9.9 universal editorial-intent plan only; no D4/renderer activation |
| Visual Drill | 4 types / 20 type-tier variants | title/subtitle/CTA/language | D9.9 universal editorial-intent plan only; no D4/renderer activation |
| Longform | Not declared as a Producer content type | Disabled; no editable fields | Unsupported by current D4 request schema |

The resolver and universal Producer plans remain declarative. D9.10 adds a bridge-planning record and explicitly does not emit renderer input, execute production/rendering or change seed/telemetry/provenance/simulation truth. D9.8, D9.9 and D9.10 tests are integrated into `c11c-suite/self_test.py`. The operator has confirmed D9.9 plan creation and the D9.10 output tab in Windows. Real-media GUI production acceptance remains a separate future gate.


## D9.11 Maintenance 0.2.0

The existing `c11c-maintenance` GUI delegates to `tools/c11d/d9/maintenance.py`. It provides dry-run plan/docs/freeze-preflight, reversible transient cleanup against exactly two roots, confirmation-gated `c11d-control` quarantine/restore with tree+manifest hash verification, and cleanup archive restoration. The canonical policy and lifecycle contract are registered read-only in Config (27 contracts, including the D9.16 full-acceptance preflight contract). The frozen C11-C manifest is never rewritten and `release_authority=NONE` remains invariant. Static acceptance and the operator-confirmed Windows GUI bring-up/focused/full Suite regression pass; D9.11 is PASS/CLOSED.


## D9.12 Test 0.2.0 route integration

`c11c-test/BUILD_MANIFEST.json` is the declarative GUI-route index. `test_d9_test_integration.py` proves that the GUI registry, manifest entries, target files, test list and five-surface shell topology agree. The GUI exposes explicit D2 asset contracts, D3 deterministic music, D4 request/personalization and GUI/CLI parity, D4.8 blocked activation governance, D5 provenance/lifecycle, D6 seed isolation, D7 catalog/provenance, D8 visual/audio QA and non-authoritative release dry-run, D9.8–D9.11 canonical test routes, aggregated D9 negative controls, D9 GUI/CLI parity, and a GUI E2E certification-plan preflight.

The D9.12 E2E route validates the 11-case certification plan only and is explicitly no-media. D9.13 adds the cross-suite lifecycle route and revalidates the five-surface topology. D9.14 adds a fail-closed real-media certification gate and does not claim real-media GUI acceptance. D9.15 adds an 8-capability operational preflight; operator GUI evidence across all five surfaces is still required. D9.16 adds a full-acceptance preflight that confirms the D9.14 gate stays blocked and does not infer D9.15 operator evidence. Physical GUI production certification remains blocked until a separately authorized future D renderer baseline exists and D4.8 is explicitly authorized. `D4.8=BLOCKED`, `renderer_activation=false`, `media_created=false`, `release_authority=NONE`, and the frozen C11-C baseline remains immutable.


## D9.13 — Cross-suite lifecycle

| Concern | Canonical component | Acceptance |
|---|---|---|
| Contract/profile binding | `c11c-config` / `D9_13_CROSS_SUITE_LIFECYCLE_V1.json` + D9.14 gate contract | Read-only, config contracts 27/27 |
| Request, plan and bridge identity | `c11c-producer` / `cross_suite_lifecycle.py` | Replay request/plan/bridge; GUI/CLI parity 3/3 |
| Test/QA contract | `c11c-test` / `test_d9_test_integration.py` | 25 D routes; 55 all routes; D9.14 gate shown/executed PASS (remains blocked); D9.15/D9.16 preflights added |
| Provenance projection | `c11c-catalog` / `c11d_catalog.py` | `CROSS_SUITE_LIFECYCLE_INTENT`, no media/release |
| Policy and historical manifest audit | `c11c-maintenance` / `maintenance.py audit-lifecycle` | Read-only audit, zero file side effects |

Status: static/backend acceptance PASS (three supported content types, five ordered stages, catalog 3/3, maintenance audit 3/3, negative 12/12). Operator must verify the lifecycle view and Catalog/Maintenance presentation on Windows. `D4.8=BLOCKED`, `renderer_activation=false`, `media_created=false`, and `release_authority=NONE`.


## D9.14 — Real-media GUI certification gate (blocked)

`c11c-producer` exposes `D9.14 · REAL-MEDIA CERTIFICATION GATE (BLOCKED)` and `c11c-test` routes the canonical no-media gate test. The pass criterion proves that the gate remains blocked; it is not a real-media certification PASS. No renderer, media output, D4.8 authorization or release authority is enabled. Real-media GUI E2E waits for a separately approved future D frozen baseline and explicit governance authorization.


## D9.15 — GUI operational acceptance

The canonical contract `definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json` is registered read-only in Config and validated through the existing Test 0.2.0 route `D9.15 GUI OPERATIONAL ACCEPTANCE PREFLIGHT (PLAN ONLY)`. Its static PASS certifies 8/8 structural capabilities across the five existing surfaces, validates launchers/manifests, checks required controls and preserves the freeze-manifest hash. It explicitly returns `operator_confirmation=REQUIRED`; this is not Windows GUI acceptance. Capture operator evidence in Config, Producer, Test, Catalog and Maintenance before marking D9.15 closed. D9.14 still remains blocked for physical media; `D4.8=BLOCKED`, renderer/media are false and release authority is NONE.


## D9.16 — Full D9 acceptance preflight (blocked as required)

The existing Test 0.2.0 GUI registers `D9.16 FULL D9 ACCEPTANCE PREFLIGHT (NO MEDIA)`. Config 0.2.0 registers `D9_16_FULL_ACCEPTANCE_V1.json` read-only (27 governed contracts). The preflight verifies D9.8–D9.16 test paths, exact five-surface topology, the immutable historical C11-C manifest hash, D9.14's fail-closed state, and that D9.15 has not inferred five-surface operator evidence. It runs no renderer and writes no evidence. Expected focused result is `PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED` with 21/21 negative controls; this is not D9.16 acceptance closure.
