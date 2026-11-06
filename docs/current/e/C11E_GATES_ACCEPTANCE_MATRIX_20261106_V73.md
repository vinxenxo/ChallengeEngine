# C11-E Gates & Acceptance Matrix — V73

| Gate | State | Evidence / exit condition |
|---|---|---|
| E4A.6 Challenge visual | PASS_TEST_ONLY | Recovery V1.2; visual review PASS |
| E4A.7 Challenge A/V | PASS_TEST_ONLY | 267/267 hashes; AAC/H.264 identity and sync verified |
| E4A human A/B/C | PASS | Operator confirmed |
| E4A D99 GUI contract | PASS | V2 code patch + targeted tests |
| E4A GUI/E1/D9 parity | PASS | `D99-GUI-37559C528640` |
| **Full E4A** | **CLOSED PASS_TEST_ONLY** | No rerun absent regression |
| E4B Loop overlay | PASS_ADD_ONLY | V1 installed; 27 pins/17 files |
| E4B composition static checks | PASS | 17/17, proposal-only, no renderer authority |
| E4B populated GUI | PASS_TEST_ONLY | `D99-GUI-439FD530F839`, correct Unicode |
| E4B CLI V1 | STRUCTURAL_ONLY | D9/E1 accepted structure, but mojibake invalidates populated parity |
| E4B populated GUI/CLI V2 | PENDING | Active Windows runner + receipt; existing GUI reused |
| E4B composition policy | PROPOSED_NOT_APPROVED | Human/technical review required before consumer code |
| E4B D-owned consumer | NOT_IMPLEMENTED | After composition approval, at existing D boundary |
| E4B family/A-V matrix | PENDING | 5 families/27 grammars, seeds, family music, stream-copy, QA |
| E4C Drill | HOLD | After E4B exit |
| E5 | HOLD | Determinism, seeds, isolation, full GUI/CLI |
| E6 Smoke18 | HOLD | After E5 |
| E7 Matrix101 | HOLD | CH_008/009 held; 99 provisional |
| E8 | HOLD | Historical C-to-E regression and independent acceptance |

## E4B CLI V2 acceptance

- Existing GUI JSON is parsed by Python UTF-8; exact four-field Unicode values are independently checked against a fixture.
- CLI request differs only in request ID and request provenance/origin; D9.9 and E1 receive the same raw JSON.
- GUI and CLI `editorial_hash` must match; within the CLI run D9/E1 request and plan hashes must match.
- All seed domains remain separate; family music route stays protected and not invoked.
- No renderer, input, dispatch, production execution or media; D4.8 remains BLOCKED and release authority NONE.

## Immutable governance

C11-C 2.19.12 frozen manifest unchanged. No Git/HEAD/status/branch checks. No sixth module, parallel Producer or binder. Renderer/dispatch/media OFF; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.
