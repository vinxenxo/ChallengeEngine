# C11E E5 Cross-Family Qualification Plan — V1 (2026-11-16)

**State: READY TO PREPARE; NOT STARTED.** E4C is closed at 20/20. This plan defines the next qualification scope; it does not authorize execution, source changes or rendering.

## Objective

Demonstrate that the single C11-E orchestration path can invoke Challenge, Visual Loop and Visual Drill without cross-family state leakage, while preserving each family's canonical contract and correct music route. Prove repeatability, independent gameplay/music seed domains and parity between the current Producer GUI and CLI adapters over the same E1 business service.

## Opening canary proposed by operator

Run one controlled representative case for each family:

1. Challenge
2. Visual Loop
3. Visual Drill

Treat this as the E5 opening canary, not as a rerun of E4 and not as E6 Smoke18. Choose each selector, canonical, native timebase, family profile, binder and seed from the exact accepted definitions in the active checkout. Pin all selected inputs before creating requests. Do not guess or copy one family's selector/profile/timeline into another.

## Required matrix

For each of the three family routes:

| Probe | Controlled change | Expected invariant |
|---|---|---|
| A baseline | Fixed gameplay seed + fixed music seed | Establish canonical media and receipt |
| B replay | Repeat exact A request and seeds | Deterministic output identity under the family's defined contract |
| C music variation | Change only music seed | Visual/video content stays invariant; music stream changes |
| D gameplay variation | Change only gameplay seed, hold music seed fixed | Gameplay-dependent content may change; music stream remains invariant |
| GUI/CLI parity | Same normalized request through GUI and CLI | Same E1 service/business semantics and equivalent qualified result |

The exact number of processes/exports, replay tolerances and equality levels must be fixed in an E5 test contract before execution. Do not assume bitwise determinism for elements explicitly defined as nondeterministic; define the canonical comparison boundary (request, frame stream, video, audio, mux, receipt) for each family.

## Family isolation checks

- Challenge uses only its accepted Challenge canonical, selector rules, presentation/editorial binder and family music route.
- Visual Loop retains its C11-C grammar, variant timeline, binder and family music profile.
- Visual Drill retains its C11-C phase semantics, END_CTA precedence, binder and family music profile.
- A family request must not activate another family's profile, binder, grammar, title role, timeline or selector contract.
- Shared fields/service plumbing are allowed only where already defined; do not add a parallel Producer, binder, renderer or business service.

## Preflight / evidence requirements

1. Read-only E5 source inventory from the active checkout, plus current E4A/E4B/E4C closeout references.
2. Exact selectors, canonical hashes, family music route/profile, timebase, seed plan, CLI/GUI request pair and output cardinality documented for all families.
3. Source pins and frozen C11-C manifest pre/post unchanged.
4. Fresh E5 BatchId, one-shot lock, authorization, separate per-family request IDs and non-colliding evidence roots. Never reuse E4 BatchIds or E4 media outputs as new E5 execution evidence.
5. Full per-family qualification receipts, A/B/C/D media and audio hashes as applicable, FFprobe/audio QA, source snapshots, CLI/GUI parity report and immutable combined receipt.
6. Operator A/V approval for the three canary outputs.

Any attempt reserved under an E5 one-shot lock is consumed on failure; preserve evidence and do not rerun the same BatchId.

## Exit criteria

E5 closes only when all three family canaries pass every declared seed, determinism, family isolation, GUI/CLI and media/receipt gate. Then proceed to E6 Smoke18: six A/V cases per family, 18 total. E6 acceptance is not implied by three E5 canaries.

## Governance

C11-C 2.19.12 frozen manifest `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953`. E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority none. Git checks skipped; commits operator-managed; SHA-256 source pins enforced. No mechanics, core audio, family binders, RNG or canonical definitions may be modified under this qualification plan.
