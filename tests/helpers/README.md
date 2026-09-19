# Test helpers reserved for artifact-path consolidation

All new tests must resolve generated paths through one helper instead of embedding `output/`, `export/`, `qa/` or checkpoint-specific roots.

The first implementation pass can be incremental: existing tests are classified and repaired in groups rather than mass-edited blindly.
