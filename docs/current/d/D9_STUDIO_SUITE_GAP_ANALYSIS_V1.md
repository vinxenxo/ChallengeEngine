# C11-D — Studio → Canonical Suite Gap Analysis

## Conclusion

The user's original objective was not lost: the old Studio specification describes the intended **unified operator/control surface**, while the current `c11c-suite` is only a modular shell around five independent applications.

D9 is therefore the correct phase to reconcile those layers.

## Historical Studio contribution worth preserving

- central project/environment context;
- tool discovery and environment validation;
- metadata-driven configuration;
- structured command construction;
- asynchronous job management;
- artifact registry and lifecycle awareness;
- centralized logs;
- seed/reproducibility views;
- production protection;
- validation center;
- catalog and product identity;
- review/production separation;
- complete configuration visibility with effective/derived/protected state.

## Current Suite reality

The active `c11c-suite` already has useful, tested C11-C applications:

- Test;
- Producer;
- Catalog;
- Maintenance;
- Config.

The root launcher is currently a thin five-button process launcher. D-aware state, D4–D9 contracts, provenance, seed governance and media QA are not yet presented as one coherent operator model.

## Integration strategy

Do not copy the historical application wholesale. Keep `c11c-suite` canonical and progressively add shared D-aware services/pages. Existing applications remain usable during migration.

## Required certification before D10

A real Windows GUI test must demonstrate, at minimum:

1. environment discovery;
2. D4 request/personalization/GUI-CLI parity visibility;
3. D6 seed governance and seed separation visibility;
4. D7 matrix/catalog identity inspection;
5. D8 media/release control-plane inspection;
6. D9 real pilot execution from GUI;
7. cleanup/configuration/review/test/freeze operations from GUI;
8. reproducibility via manifest/command/path;
9. asynchronous execution and logs;
10. safety guards and protected roots;
11. GUI-produced evidence matching canonical CLI evidence;
12. no mutation of frozen C11-C boundaries.

D10 remains blocked until those points pass.
