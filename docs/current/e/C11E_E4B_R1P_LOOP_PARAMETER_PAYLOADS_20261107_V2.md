# E4B R1P — Loop Family Parameter Payloads V2

**Date:** 2026-11-07  
**State:** `READY_TO_EXECUTE`; no Windows Godot runtime receipt exists yet.

## Purpose

Materialize a request-bound, deterministic in-memory family parameter payload for each of the 27 concrete Visual Loop grammars. This closes the gap between the accepted D9.9/D9.10 family-stage planning contract and a runtime-generated parameter recipe. It is deliberately not a rendered payload.

## Input and provenance chain

For each selector, the Python preparation stage creates a canonical `REVIEW` D9.9 request, calls `universal_producer.evaluate_universal_request`, builds the D9.10 planning record, and builds/validates the existing D-only family-stage contract. Every receipt binds:

- D9.9 request, plan and editorial hashes;
- D9.10 bridge record hash;
- D-only adapter envelope hash and family-stage contract SHA-256;
- family/grammar identity and index;
- `request.seed` and distinct `request.music_seed`;
- global source pins plus that family's prototype and launcher pins.

The 27 gameplay seeds are 100001–100027; the 27 music seeds are 500001–500027. The visual helper call chain accepts only the gameplay seed. `music_seed` remains request identity metadata and is not supplied to variation, palette or technobabble helpers.

## Exact C11-C helper behavior

The five current family prototypes share the same relevant call sequence:

1. `C11CVariationProfile.build(internal_family_id, _seed)`.
2. `_apply_grammar_override()` maps the explicit technical grammar ID to its exact index and sets `grammar_mode`/`grammar_name`.
3. `C11CVisualLoopDuration.resolve(variation.loop_cycles, DEFAULT_LOOP_DURATION)` where all five prototypes declare `DEFAULT_LOOP_DURATION := 0.0`; the runner clears `C11C_DURATION_SECONDS`, and the shared policy returns 20/22/23 seconds at 30 FPS.
4. `C11CPaletteBank.palette(internal_family_id, variation.palette_mode)` — no seed argument, matching the prototypes and avoiding any added seed-derived palette variant.
5. `C11CEditorialColors.palette(internal_family_id, palette)` — the seven resolved text/decor colors are serialized as six-digit HTML hex strings.
6. `TechnobabbleGenerator.generate_geek_text(internal_family_id, _seed, variation)`.

R1P verifies the prototype source still contains those exact integration tokens before running the helpers. A temporary Godot project receives byte-identical copies of these five RefCounted helper scripts and the R1P SceneTree script, avoiding writes to the active repository from the probe runtime.

## Determinism and receipt validation

Each selector is built twice independently in Godot. Canonical JSON bytes and SHA-256 values must match. The Python finalizer checks the Godot exit code/version, exact result count, request identity, selector/index, seed separation, source pins, variation grammar, resolved palette, all seven editorial text colors, timing, technobabble, governance flags and every payload hash. It then writes 27 per-grammar immutable receipts with SHA-256 sidecars and an aggregate report; the finalizer reopens the persisted 27 receipts and sidecars and revalidates their hashes before returning PASS.

## Execution boundary

R1P does not load or instantiate any family prototype, scene, renderer or shader. It does not call a C11-C launcher, create frame buffers or frame inventory, create pixels, emit renderer-native input, invoke the D compositor, invoke audio/D3, run FFmpeg or create media. It only materializes the parameter recipe and timing descriptor in memory. The output explicitly records `frame_inventory_materialized=false` and `pixel_payload_materialized=false`. Godot itself writes no checkout files; the Godot result marks `godot_checkout_files_written=false`; the Python/PowerShell finalizer writes only the designated evidence artifacts under `artifacts/tests/c11e/e4b_r1p/`, never C11-C source files. Import-time Python bytecode writes are disabled (`sys.dont_write_bytecode` and `py -B`).

## Run

Requirements: Windows PowerShell 5.1, Python 3.13 (`py -3.13`) and Godot 4.7.1 console executable. From the active checkout root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4B_R1P_LOOP_PARAMETER_PAYLOADS_V1.ps1"
```

When Godot is not on PATH, pass `-GodotExe "C:\full\path\to\Godot_v4.7.1-stable_win64_console.exe"`.

Expected output is a new run directory and ZIP under `artifacts/tests/c11e/e4b_r1p/`, with 27 receipts, parent D9.9/D9.10 bindings, source manifest, stdout/stderr logs, process receipt and aggregate report. The only acceptable R1P runtime status is `PASS_R1P_PARAMETER_PAYLOADS_27_OF_27`.

## What R1P does not close

R1P is not the actual C11-C rendered frame payload, frame inventory, pixel review, D-only compositor, five-family pilot, 27-grammar visual acceptance, music execution, mux, A/V QA, D4.8, D9.10 renderability or release. Those remain separate gates. C11-C 2.19.12 and all existing protected mechanics remain unchanged.
