# C11-D → C11-E Full-Family Roadmap — V19

**Date:** 2026-11-03. V19 records E4A discovery success, the V3 static audit result, and V4 evidence that the remaining GUI contract test contains a stale application-version literal. No production promotion is implied.

## Product outcome

A single C11-E service and family adapters create validated audiovisual output for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics and family audio implementations. Add authorized D presentation/layout, family-scoped editorial, correct family audio, mux, FFprobe/audio QA and immutable receipts.

## Development workflow

Implement shared service/worker through CLI first where practical. Wire the same implementation into current low-fidelity Producer GUI as dispatcher. Both CLI and GUI must be executable and tested during engineering. A future new GUI that owns all generation applies only after D/E replaces C; CLI remains for CI/compatibility.

## Ordered gates

1. E0 foundation — accepted.
2. E1 shared service — accepted.
3. E2 bounded CH001 R4 title-to-pixels — accepted within scope.
4. E3.2 D3 V5/E1 contract — accepted.
5. E3 physical CH001 R4 audio/mux pilot — accepted; operator confirmed expected audiovisual result.
6. E3 V1.5 negative controls — 50/50, zero skips, supplemental recovery PASS; E3 formally closed test-only.
7. E4A.0 Challenge source discovery V2 — PASS_READ_ONLY (751 scanned / 803 matches / 111 candidates / zero scan errors).
8. E4A source audit — V3: 10/10 source pins, six D9 focused tests PASS; historical GUI contract test blocked at stale APP_VERSION literal 0.11.1. V4 established current Producer APP_VERSION 0.12.0-E3 and clean target-file state. Run versioned successor test V1, retaining all other assertions.
9. E4A static audit closure — requires successor GUI contract test PASS. Then review D field-to-slot route and implement minimal change in existing Challenge consumer only.
10. E4A physical Challenge audiovisual test and operator acceptance.
11. E4B Loop adapter/binder, grammar/variant timeline, editorial/layout and existing Loop music.
12. E4C Drill adapter/binder, phase/END_CTA precedence, editorial/layout and existing Drill music.
13. E5 cross-family determinism, gameplay/music seed isolation, profile/adapter non-leakage and CLI/GUI parity.
14. E6 Smoke18: six complete audiovisual scenarios per family.
15. E7 Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held due 11s declared vs 12s phase sum; 99 provisional runnable.
16. E8 independent acceptance, historical corpus coverage, immutable freeze and explicit promotion.

## Historical coverage obligation

Before E8, map every C11-C historical production/review/test case row-by-row, including 27 review cases, 9 Challenges and all other visual/review categories. Each applicable row must cover D layout/presentation, scoped editorial, family audio, independent seeds, visual identity, determinism, mux/FFprobe/audio QA, CLI/GUI path and immutable receipt. Smoke18 and Matrix101 do not waive this obligation.

## Hard governance

C11-C 2.19.12 remains sole production authority; manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No protected generators/mechanics, `core/audio`, D3 engine, E1 service, canonical definitions, C11-C manifest or governance lock changes. No second binder/producer/renderer. `renderer=OFF`, `release_authority=NONE`, no freeze or promotion before E8 and separate approval.
