# C11-E Gates and Acceptance Matrix — V172 (2026-11-19)

| Gate | Status | Evidence / next action |
|---|---|---|
| E0–E3 | PASS retained | No rerun absent source drift |
| E4A Challenge | CLOSED in declared TEST_ONLY scope | E4A.7 CHALLENGE_004 A/V accepted; E4A policy V1 remains operative |
| E4B Visual Loop | CLOSED | R1V 10/10 and Loop22 44/44 human accepted |
| E4C Visual Drill | CLOSED 20/20 | Preserve accepted family closeouts |
| E5 Cross-Family | CLOSED `PASS_CLOSED_TEST_ONLY` | E5 full closeout + Qt runtime 3/3 accepted |
| E6 Challenge PREPARE_ONLY | PASS retained | Six selectors / 18 E1 intents / 18 D envelopes |
| E6 family editorial fixture | PASS PREPARE_ONLY | 18 rows / 30 assignments; runtime readback not proven |
| E6 Challenge editorial binding | READY_TO_EXECUTE_PREPARE_ONLY | New overlay creates 18 derived D envelopes; zero-second windows intentionally suppress fields; 27 visible / 27 suppressed expected |
| E6 Challenge runtime/readback | HELD | Requires bounded authorized consumer readback; no Godot in binding step |
| E6 Drill editorial readback | HELD | Six targets remain unproven |
| E6 Loop D compositor | BLOCKED_NOT_ADMITTED | D-owned postcompositor and six pixel outputs required |
| E6 Smoke18 media | HELD | D4.8 V2 BLOCKED; successor and separate E6 TEST_ONLY authorization required |
| E7 Matrix101 | HELD | 54 Challenge +27 Loop +20 Drill; CH_008/009 held; 99 provisional |
| E8 | BLOCKED / downstream | Historical C-to-E regression, independent acceptance, immutable freeze and transition decision |

## Challenge zero-duration semantics

Operator confirmed 2026-11-19 that `HOOK=0s` or `CTA=0s` is intentional suppression, not an implementation defect. E4A title/subtitle remain HOOK-only; CTA remains CTA-only. Zero-frame half-open intervals are `OMITTED_EMPTY` and must not be redirected to GAME. The E6 binding runner validates this over all 18 nested probes.

## Failed preflight lineage

Render Gate Apply V2 and V2.1 remain `FAILED_CLOSED` before install transaction. Do not rerun. Preserve failure receipts. The manually printed parent-console PASS after child failure is invalid and does not change gate state.

## Invariants

C11-C frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; D4.8 V2 unchanged/BLOCKED; E1 PREPARE_ONLY; renderer OFF; dispatch/media false; release authority NONE; E6 acceptance 0; matrix not frozen. No Git checks; operator commits; source SHA-256 pins enforced.
