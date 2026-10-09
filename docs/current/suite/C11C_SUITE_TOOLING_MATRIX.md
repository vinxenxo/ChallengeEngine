# C11-C Suite — Tooling Matrix / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 frozen

## Active surfaces

| Surface | Responsibility | D9 current state | Target |
|---|---|---|---|
| `c11c-test` | QA / regression / acceptance | Test 0.2.0; legacy C11-C routes preserved + D2–D9 route registry, negative/parity bundles and no-media GUI E2E preflight; Windows GUI acceptance pending | 0.2.0 |
| `c11c-producer` | production / review / job orchestration | 0.11.1; D4 GUI preserved + D9.9 universal editorial and D9.10 plan-only bridge tabs/output | D9.9 selector matrix and D9.10 bridge contract/CLI parity PASS; operator-confirmed Windows plan-only bridge output tab |
| `c11c-catalog` | catalog / product / provenance / reproduction | 0.2.0; D7 + D9 pilot coverage integrated | 0.2.x |
| `c11c-config` | configuration / profiles / snapshots | 0.2.0; D9.8 model + D9.10 bridge + D9.11 maintenance policy registered read-only; 23/23 registries validate; Windows Qt acceptance pending | 0.2.x |
| `c11c-maintenance` | cleanup / organization / quarantine / freeze | 0.2.0 D9.11 PASS/CLOSED; operator-confirmed Windows GUI and full Suite acceptance passed | 0.2.0 |

## Canonical D routes

| Capability | GUI surface | Canonical backend | Certification state |
|---|---|---|---|
| D4 request construction | Producer | D4 request/normalization | integrated |
| D4.3 Challenge personalization | Producer | D4.3 personalization resolver | integrated |
| D4 plan identity | Producer | D4.4 canonical orchestrator | integrated |
| D7 catalog inspection | Catalog | canonical catalog/identity | integrated |
| D9 pilot product inspection | Catalog | D9 acceptance/provenance | integrated |
| D9 configuration contracts | Config | D2–D9 contract registry (read-only, 23 contracts) | D9.10 and D9.11 invariants registered; static Config tests PASS; Windows GUI acceptance pending |
| D9.8 universal editorial model | Config (read-only registry) + shared resolver | `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` + `tools/c11d/d9/universal_editorial_model.py` | model/resolver and negative matrix PASS |
| D9.9 universal Producer | Existing Producer GUI + CLI | `tools/c11d/d9/universal_producer.py` + `tools/c11d/d9/universal_producer_cli.py` | all current selectors resolve; CLI process parity per type; plan-only; Windows GUI plan creation confirmed by operator |
| D9.10 bridge planning | Existing Producer GUI + CLI | `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` + `tools/c11d/d9/editorial_render_bridge.py` | 3/3 content types; bridge-record CLI parity 3/3; 15 negatives; renderer input/media not emitted; Windows plan-only output-tab check confirmed by operator |
| D9 real GUI production | Producer/Test | future D renderer authority | pending |
| D9 maintenance operations | Maintenance 0.2.0 + canonical backend | `tools/c11d/d9/maintenance.py` | PASS/CLOSED; Windows GUI and Windows focused/full regression confirmed by operator |
| D9 GUI E2E | Test 0.2.0 | `docs/current/d/D9_GUI_E2E_CERTIFICATION_PLAN_V1.md` + canonical backends | preflight route PASS; real-media GUI execution remains a later D9.14 gate |

## Existing C11-C routes remain authoritative

The Suite continues to invoke the existing C11-C canonical production/review/QA commands. D9 integration must wrap them rather than clone their behavior.

## Retired/historical

`c11c-studio` is historical/retired. It must not be revived as a current operational suite. The incoming D9.7.2 archive also contains an unregistered legacy `c11d-control` directory; the shared launcher must expose only the five canonical surfaces. Do not register it. Physical quarantine/restore is now gated by the D9.11 Maintenance backend and an append-only manifest reconciliation ledger; the operation remains operator-triggered and never rewrites the historical C11-C manifest.

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

The existing `c11c-maintenance` GUI delegates to `tools/c11d/d9/maintenance.py`. It provides dry-run plan/docs/freeze-preflight, reversible transient cleanup against exactly two roots, confirmation-gated `c11d-control` quarantine/restore with tree+manifest hash verification, and cleanup archive restoration. The canonical policy is registered read-only in Config (23 contracts). The frozen C11-C manifest is never rewritten and `release_authority=NONE` remains invariant. Static acceptance and the operator-confirmed Windows GUI bring-up/focused/full Suite regression pass; D9.11 is PASS/CLOSED.


## D9.12 Test 0.2.0 route integration

`c11c-test/BUILD_MANIFEST.json` is the declarative GUI-route index. `test_d9_test_integration.py` proves that the GUI registry, manifest entries, target files, test list and five-surface shell topology agree. The GUI exposes explicit D2 asset contracts, D3 deterministic music, D4 request/personalization and GUI/CLI parity, D4.8 blocked activation governance, D5 provenance/lifecycle, D6 seed isolation, D7 catalog/provenance, D8 visual/audio QA and non-authoritative release dry-run, D9.8–D9.11 canonical test routes, aggregated D9 negative controls, D9 GUI/CLI parity, and a GUI E2E certification-plan preflight.

The E2E route validates the 11-case certification plan only and is explicitly no-media. It does not claim real-media GUI acceptance. Physical GUI production certification stays at D9.14, conditional on a separately authorized future D renderer baseline. `D4.8=BLOCKED`, `renderer_activation=false`, `media_created=false`, `release_authority=NONE`, and the frozen C11-C baseline remains immutable.
