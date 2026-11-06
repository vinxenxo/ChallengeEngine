# C11-E Gates & Acceptance Matrix — V74

| Gate | State | Evidence / exit condition |
|---|---|---|
| E4A.6 Challenge visual | PASS_TEST_ONLY | Recovery V1.2; visual review PASS |
| E4A.7 Challenge A/V | PASS_TEST_ONLY | 267/267 hashes; AAC/H.264 identity and sync verified |
| E4A human A/B/C | PASS | Operator confirmed |
| E4A D99 GUI contract | PASS | V2 code patch + targeted tests |
| E4A GUI/E1/D9 parity | PASS | `D99-GUI-37559C528640` |
| **Full E4A** | **CLOSED PASS_TEST_ONLY** | No rerun absent regression |
| E4B overlay V1 | PASS_ADD_ONLY | 27 pins/17 files |
| E4B composition proposal | PASS_STATIC_ONLY | 17/17; proposal not approved, no renderer input |
| E4B populated GUI | PASS_TEST_ONLY | `D99-GUI-439FD530F839`; four exact Unicode values |
| E4B populated GUI/CLI parity V2 | PASS_TEST_ONLY | `20261106T204002Z-CF365847`; editorial hash `283e630...` |
| **E4B full-family matrix harness** | **STAGING PASS** | 13/13 focused tests; 5 families/27 grammars × 3 seed cases; 81/81 D9.9/D9.10/E1; no Windows GUI acceptance yet |
| E4B Windows GUI matrix | PENDING | New existing-tab diagnostic button; requires 27 grammars / 81 cases report |
| E4B Windows CLI matrix parity | PENDING | CLI runner replays GUI template; require 81/81 parity rows |
| E4B composition policy | PROPOSED_NOT_APPROVED | Field windows/timing/layout/typography and human review required |
| E4B all-family visual payload binding | NOT_IMPLEMENTED | Historical D exact-selector path is Geometric-only; no policy or family admission inferred |
| E4B A/V and human review | PENDING | Only after consumer and authorization gates |
| E4C Drill | HOLD | After E4B exit |
| E5 | HOLD | Determinism, seeds, isolation, full GUI/CLI |
| E6 Smoke18 | HOLD | After E5 |
| E7 Matrix101 | HOLD | CH_008/009 held; 99 provisional |
| E8 | HOLD | Historical C-to-E regression and independent acceptance |

## E4B full-family matrix acceptance

- The same D-owned matrix function is called from the existing D9.9 GUI tab and from the CLI runner; no separate Producer or binder.
- Inventory must resolve exactly five families and 27 concrete grammars (5/5/5/5/7), excluding `auto` selector entries.
- Three requests per grammar: baseline, gameplay-seed-only mutation, music-seed-only mutation; total 81. Each request travels through D9.9, D9.10 bridge, D-only adapter envelope and E1 intent preparation.
- Each case retains exactly four Loop editorial keys, NFC strings, independent seeds, family music profile mapping and deterministic repeated request/plan/bridge/adapter hashes.
- E1 remains `NOT_CONSUMED_E1`; family adapter `NOT_CONNECTED_E1`; C11-C family music route preserved and not invoked.
- GUI/CLI compare all 81 family/grammar/scenario editorial hashes and values from the same GUI-exported UTF-8 template. Request/intent hashes may differ where request identity or origin differs.
- Require renderer/input/dispatch/production/media false; no Godot, C11-C visual generator, family music generator, D3 V5 or FFmpeg; D4.8 BLOCKED; `release_authority=NONE`.

## Immutable governance

C11-C 2.19.12 frozen manifest unchanged. No Git/HEAD/status/branch checks. No sixth module, parallel Producer or binder. Renderer/dispatch/media OFF; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.
