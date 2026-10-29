# C11-D V2-B Allowlisted Coordinate Consumer Runtime Fix V2 (2026-10-22)

## Purpose

This ADD_ONLY overlay provides a new V2 review-only GDScript consumer and an isolated runtime harness. It does not modify the V1 files and introduces no production call sites.

## Observed V1 failure

The operator ran Godot `4.7.1.stable.mono.official.a13da4feb`. The V1 runtime emitted `Invalid operands 'float' and 'Object' in operator '=='` (and `Vector2` versus `Object`) at the `source_value == missing_sentinel` check. The harness printed case totals but exited `1`; this is a FAIL, not an acceptance. The observed V1 runtime stdout SHA-256 was `59e5531424b9dd30545ef5cf0422cc0a8d4abc95bc69ae0a23ebad40381417d8`; stderr SHA-256 was `2e6cb1ff66713d29a7c6346f5b4ab224702fac85d49d3afad2f42a51b92d3c00`.

## V2 correction

V2 checks `typeof(source_value) == TYPE_OBJECT` before comparing it to the `RefCounted` sentinel. If the key is absent, it returns `MISSING_ALLOWLISTED_FIELD`; an unexpected object value returns `INVALID_VALUE_TYPE`. Built-in numeric and `Vector2` values no longer participate in object equality. This change is isolated to a new filename; the V1 source stays unchanged.

## Required validation

1. APPLY all new files as ADD_ONLY, verifying inherited pins and destinations.
2. Run the V2 Python static suite; expected 115 checks, all passing.
3. Run the V2 Godot Mono runtime harness on the operator's Windows checkout; expected 241 negative + 36 positive = 277 runtime cases and exit code 0.
4. Inspect stdout/stderr hashes and the emitted test receipt before any further gate.

The runtime fix remains **pending operator verification**. It does not authorize production wiring, custom-data binding, renderer projection, render testing, materialization, or media creation. `renderer=OFF`, `release_authority=NONE`, C11-C frozen manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
