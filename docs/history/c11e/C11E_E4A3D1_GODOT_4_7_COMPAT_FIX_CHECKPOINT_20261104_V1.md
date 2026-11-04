# C11-E E4A.3D.1 — Godot 4.7 API compatibility checkpoint V1

**Date:** 2026-11-04  
**Scope:** D-only Challenge isolated compositor; fixture `CHALLENGE_004`.  
**Parent:** E4A.3D.1 hook-recomposition V1, statically applied on Windows.

## Triggering failure

User ran the compositor with Godot `4.7.1.stable.mono.official.a13da4feb` after the V1 static transaction. Evidence archive `RUN_20261104_145434_04dc007f.zip` has SHA-256 `3b29a511737ec837fcc500f391b6741e0f161141bd7b4ab49d47b3c8589d90c1` (771,258 bytes, 32 entries, CRC clean).

The six real C11-C sample frames were extracted, and FFprobe confirmed H.264 720×1280 at 30 fps, 15 seconds, 450 frames. Godot then exited 1 during script reload. The first decisive error was `Cannot find member "join" in base "PackedStringArray"` at adapter line 145; the follow-on inability to infer `header_line_2` is derivative. No compositor PNGs, pixel comparisons or visual review were produced in this run.

## Root cause and exact correction

The adapter used `PackedStringArray(d_header_parts).join(" · ")`. Godot 4.7's `PackedStringArray` documentation explicitly instructs use of `String.join()` with the separator as receiver, e.g. `" ".join(string_array)`. The corrected expression is explicitly typed:

```gdscript
var header_line_2: String = " · ".join(PackedStringArray(d_header_parts)) if header_native_hook_migrated else subtitle_text
```

The D adapter's focused Python source contract is updated to require that exact direction and reject the invalid receiver call. No fallback algorithm or custom join implementation is introduced.

## Patch boundary

The compatibility patch replaces exactly two D-owned files in the Windows checkout: the Challenge editorial presentation adapter and its Python source-contract test. Preimages are the V1 applied postimages. No materializer, compositor runner, C11-C source, family binder, generator, timeline, RNG, music code or production path is changed. Eight new documentation records are add-only.

## Verification boundary and next action

The package can verify exact pre/post SHA-256, all 16 protected pins, frozen C11-C manifest, focused Python tests (expected 81 passed) and py_compile. This environment cannot run the user's Godot 4.7.1 project. Therefore do not mark E4A.3D.1 technically or visually closed on package/static success alone.

After applying the package, rerun the same bounded command against the accepted E4A.2 base run. Require Godot exit 0, 6/6 extracted frames, 18/18 PNGs, 12/12 comparisons, BODY identity, no native-hook overlap, exact canonical HOOK as first shared-header line at both endpoints, fit diagnostics (≤3 lines, ≤468 px, ≤120 px), and singular CTA owner. Review the images manually.

## Governance

`visual_placement_approved=false`; generic D1.5 safe-area and Challenge overlay remain unapproved; `player_name` and `challenge_label` remain blocked. C11-C 2.19.12 stays the production authority; production renderer/dispatch/media remain OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.17 NO-GO; D10 blocked; `release_authority=NONE`.
