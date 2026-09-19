# C11 Freeze Gate

Final gate before C11-C Art Direction.

## Gates

1. Core suite.
2. C11 presentation contracts.
3. Logical corpus.
4. 54-run simulation retrocompatibility against the frozen C11-A.1 manifest.
5. Physical export smoke.
6. Fixed-seed stress with repeatability.
7. Only then: artifact migration and documentation archival.

## Retrocompatibility

The 54 C11-A.1 runs are replayed with their exact QA definition copies and compared field-by-field against the frozen telemetry. Presentation frame hashes are intentionally excluded because C11-B.0/B.0.2/B.1 changed the presentation layer while preserving simulation truth.

## Seed stress

The stress corpus is deterministic. It contains 32 fixed seeds and is repeated twice by default, yielding 288 cases / 576 headless executions. This is a reproducibility test, not a flaky runtime-random test.

## Freeze criterion

No logical suite, retrocompatibility comparison, physical smoke, or repeatability case may fail. Legacy roots may only be moved after the gates are green.
