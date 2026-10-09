# C11-C Suite — Tooling Matrix / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 frozen

## Active surfaces

| Surface | Responsibility | D9 current state | Target |
|---|---|---|---|
| `c11c-test` | QA / regression / acceptance | C11-C routes active | 0.2.0 with D2–D9 + GUI E2E |
| `c11c-producer` | production / review / job orchestration | 0.11.1; D4 GUI preserved + D9.9 universal editorial and D9.10 plan-only bridge tabs/output | D9.9 selector matrix, Windows GUI plan creation (operator-confirmed), D9.10 contract/CLI parity PASS; new bridge-output tab Windows confirmation pending |
| `c11c-catalog` | catalog / product / provenance / reproduction | 0.2.0; D7 + D9 pilot coverage integrated | 0.2.x |
| `c11c-config` | configuration / profiles / snapshots | 0.2.0; D9.8 model + D9.10 bridge contract registered read-only; 22/22 registries validate; Windows Qt acceptance pending | 0.2.x |
| `c11c-maintenance` | cleanup / organization / quarantine / freeze | C11-C baseline | 0.2.0 |

## Canonical D routes

| Capability | GUI surface | Canonical backend | Certification state |
|---|---|---|---|
| D4 request construction | Producer | D4 request/normalization | integrated |
| D4.3 Challenge personalization | Producer | D4.3 personalization resolver | integrated |
| D4 plan identity | Producer | D4.4 canonical orchestrator | integrated |
| D7 catalog inspection | Catalog | canonical catalog/identity | integrated |
| D9 pilot product inspection | Catalog | D9 acceptance/provenance | integrated |
| D9 configuration contracts | Config | D2–D9 contract registry (read-only, 22 contracts) | D9.10 invariants registered; static Config tests PASS; Windows GUI acceptance pending |
| D9.8 universal editorial model | Config (read-only registry) + shared resolver | `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` + `tools/c11d/d9/universal_editorial_model.py` | model/resolver and negative matrix PASS |
| D9.9 universal Producer | Existing Producer GUI + CLI | `tools/c11d/d9/universal_producer.py` + `tools/c11d/d9/universal_producer_cli.py` | all current selectors resolve; CLI process parity per type; plan-only; Windows GUI plan creation confirmed by operator |
| D9.10 bridge planning | Existing Producer GUI + CLI | `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` + `tools/c11d/d9/editorial_render_bridge.py` | 3/3 content types; bridge-record CLI parity 3/3; 15 negatives; renderer input/media not emitted; new output-tab Windows check pending |
| D9 real GUI production | Producer/Test | future D renderer authority | pending |
| D9 maintenance operations | Maintenance/Test | maintenance tools | pending |
| D9 GUI E2E | Test | canonical backend | pending |

## Existing C11-C routes remain authoritative

The Suite continues to invoke the existing C11-C canonical production/review/QA commands. D9 integration must wrap them rather than clone their behavior.

## Retired/historical

`c11c-studio` is historical/retired. It must not be revived as a current operational suite. The incoming D9.7.2 archive also contains an unregistered legacy `c11d-control` directory; the shared launcher must expose only the five canonical surfaces. Do not register it. Physical quarantine/removal requires D9.11 Maintenance and manifest reconciliation.

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

The resolver and universal Producer plans remain declarative. D9.10 adds a bridge-planning record and explicitly does not emit renderer input, execute production/rendering or change seed/telemetry/provenance/simulation truth. D9.8, D9.9 and D9.10 tests are integrated into `c11c-suite/self_test.py`. The operator has confirmed D9.9 plan creation in Windows; D9.10 output-tab validation and real-media GUI acceptance remain separate gates.
