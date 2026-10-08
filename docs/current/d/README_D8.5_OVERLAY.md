# C11-D D8.5 Overlay V1

Purpose: deterministic release-manifest preview and staging-boundary checkpoint.

PS5.1 design rules used here:
- no generic `List[T]` collections;
- no `.Sum` aggregation;
- arrays are normalized with `@(...)` before collection properties;
- no ambiguous `TrimStart()` overloads;
- no naked `true`/`false` command tokens;
- UTF-8 output uses the no-argument `System.Text.UTF8Encoding` constructor;
- project root defaults to the current workspace and is validated before use;
- no runtime-generated timestamps in the deterministic manifest.

Current expected state: empty D8 media registry, `PASS_NO_MEDIA`, no physical staging.
