# C11-E E2 V6 — Godot GDScript parse error and blank-grey AVI incident

**Date:** 2026-10-31. **Request:** `C11E-E2-CH001-AB-20261031-V6`. **Disposition:** FAILED; no E2 acceptance.

## Evidence

Failure ZIP: `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_111109_2fe56abc.zip`; 46,460 bytes / 48 entries; SHA-256 `1a5d6341fae51152fb9684cc4fc158bf7c9849716a7028015f6d84b013a1cc21`.

The Python pair contract tests passed 9/9 and the pair receipt was generated. Godot 4.7.1 Mono started Movie Maker, returned exit code 0, and reported 540 frames at 540×960 / 60 FPS / 9 seconds. However, stderr stated that `var parsed := JSON.parse_string(...)` inferred a Variant and that the warning was treated as an error, followed by `Failed to load script` for `C11EChallenge001E2.gd:54`.

FFprobe confirmed a 540-frame MJPEG AVI. Independent decoding confirmed sampled frames 0, 270 and 539 each consisted of exactly one RGB colour, `(77,77,77)`. Therefore the movie contains a flat grey viewport, not a rendered Challenge.

## Root cause and prevention

`JSON.parse_string` returns Variant. The typed project configuration treated `:=` inferred-Variant warning as fatal. V7 changes only the declaration to `var parsed: Variant = JSON.parse_string(...)`, pins the new GDScript hash, rejects script parse/load diagnostics, and probes source frames 60/270/480 before A/B processing. The failure receipt is corrected to distinguish process invocation, media creation and media acceptance.

The source generator, `Main.tscn`, Challenge definition, gameplay RNG, presentation binder and C11-C manifest remain unmodified.
