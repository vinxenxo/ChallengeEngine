# C11-C Suite — Tooling Matrix / C11-D Integration State

**Suite shell:** 0.1.4
**C11-C:** 2.19.12 frozen

## Active surfaces

| Surface | Responsibility | D9 current state | Target |
|---|---|---|---|
| `c11c-test` | QA / regression / acceptance | C11-C routes active | 0.2.0 with D2–D9 + GUI E2E |
| `c11c-producer` | production / review / job orchestration | 0.10.0; D4 request/personalization GUI integrated | 0.11.x universal editorial GUI/CLI coverage (D9.9); D9.10 bridge planning only, physical renderer deferred to future D frozen baseline |
| `c11c-catalog` | catalog / product / provenance / reproduction | 0.2.0; D7 + D9 pilot coverage integrated | 0.2.x |
| `c11c-config` | configuration / profiles / snapshots | 0.2.0; D9.8 model registered read-only; Windows Qt acceptance pending | 0.2.x |
| `c11c-maintenance` | cleanup / organization / quarantine / freeze | C11-C baseline | 0.2.0 |

## Canonical D routes

| Capability | GUI surface | Canonical backend | Certification state |
|---|---|---|---|
| D4 request construction | Producer | D4 request/normalization | integrated |
| D4.3 Challenge personalization | Producer | D4.3 personalization resolver | integrated |
| D4 plan identity | Producer | D4.4 canonical orchestrator | integrated |
| D7 catalog inspection | Catalog | canonical catalog/identity | integrated |
| D9 pilot product inspection | Catalog | D9 acceptance/provenance | integrated |
| D9 configuration contracts | Config | D2–D9 contract registry | integration prepared |
| D9.8 universal editorial model | Config (read-only registry) + shared resolver | `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` + `tools/c11d/d9/universal_editorial_model.py` | model/resolver static PASS; GUI coverage D9.9 pending |
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


## D9.8 content contract (static model state)

| Content type | Live inventory | Editable model | Current canonical D4 plan path |
|---|---|---|---|
| Challenge | 9 challenge IDs | title/subtitle/CTA/language/player name/challenge label | Supported by current D4 request path |
| Visual Loop | 5 families / 27 concrete grammars (`auto` excluded from grammar count) | title/subtitle/CTA/language | Pending D9.9 universal request adapter |
| Visual Drill | 4 types / 20 type-tier variants | title/subtitle/CTA/language | Pending D9.9 universal request adapter |
| Longform | Not declared as a Producer content type | Disabled; no editable fields | Unsupported by current D4 request schema |

The resolver is strictly declarative. It does not execute production/rendering or change seed/telemetry/provenance/simulation truth. D9.8 model tests are integrated into `c11c-suite/self_test.py`; this checkpoint does not close D9 or establish Windows GUI acceptance.
