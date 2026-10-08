# Test helpers reserved for artifact-path consolidation

All new tests must resolve generated paths through one helper instead of embedding `output/`, `export/`, `qa/` or checkpoint-specific roots.

The first implementation pass can be incremental: existing tests are classified and repaired in groups rather than mass-edited blindly.

## Current D7/D8 state

C11-C 2.19.12 is frozen. C11-D D7 is PASS/CLOSED and FROZEN; D8.0 is the next phase. The active C11-D baseline is `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip` (SHA-256 `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`).

## Directory contents

### Subdirectories
- None.

### Representative files
- `ArtifactPaths.gd`
- `FailTestUnknownAsset.gd`
- `FailTestUnknownEvent.gd`
