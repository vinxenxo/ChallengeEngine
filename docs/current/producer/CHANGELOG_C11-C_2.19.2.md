# C11-C 2.19.2 — Producer Test Contract Alignment

- Updated `C11CArtDirectionProductionHygieneContractTest.gd` from the obsolete 2.18.9 OGV contract to the current 2.19.x temporary AVI Producer route.
- Updated `C11CVisualDrillMovieCaptureContractTest.gd` to validate the actual `$movieArgs=@('--path','.'...)` invocation used by the working Producer instead of a mismatched literal search.
- Preserved the runtime Producer implementation from 2.19.1 unchanged.
- No changes to simulation, RNG, runtime mechanics, presentation truth, timing, audio ownership, delivery semantics, or logical social geometry.

## Verification target

After applying this overlay on the already-applied 2.19.1 state, the two previously failing suites should reflect the current AVI contract.
