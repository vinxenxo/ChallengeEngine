# C11-E E4A Challenge — Pixel Render Increment V1

**Date:** 2026-11-03  
**Status:** `PREPARED_SANDBOX_TESTS_PASS; WINDOWS_GODOT_RUNTIME_PENDING`  
**Authority:** active Windows checkout remains authoritative. This increment implements an opt-in D-only pixel-test path; it is not yet a Windows runtime acceptance or E4A phase closure.

## 1. What this increment adds

The existing `tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd` remains the single Challenge source-timebase materializer. Its original invocation, without `--e4a-config`, retains the previous read-only preview behavior. The opt-in path is entered only when the dedicated test runner supplies `--e4a-config`.

The new Python driver calls the existing C11-E E1 shared service and canonical D9.9 resolver to prepare three non-dispatched intents for the same `CHALLENGE_004` selection, seed domains, delivery profile and presentation profile:

- A: all six effective editorial values empty; D9.8 resolves them to `UNKNOWN`, and the visual consumer omits them.
- B: distinctive title, subtitle and CTA; language `es`; non-empty Challenge-only `player_name` and `challenge_label`.
- C: same three visible strings as B; language `en`; Challenge-only values empty. This isolates metadata and unresolved-overlay behavior.

The GDScript then attaches an in-memory D editorial composition to a duplicate of the materialized payload. Every field carries its exact effective value hash, semantic region, approved named phase windows, source-frame interval, policy SHA-256 and D1.5 layout SHA-256. It validates that the original 420 game-frame record hash remains unchanged and refuses to serialize protected gameplay fields.

## 2. Isolated pixel fixture

The opt-in test draws an off-screen `SubViewport` at the D1.5 logical size 540×960. It produces 18 PNGs (A/B/C × six source-phase boundary samples) and 12 pixel comparisons.

The positive pixel claims are deliberately bounded:

- `title` and `subtitle`: change pixels only within HEADER and only at first/last sampled HOOK frames.
- `call_to_action`: change pixels only within FOOTER and only at first/last sampled CTA frames.
- A/B: no text pixels at sampled GAME/REVEAL frames.
- B/C: no pixel change when only language and the two unresolved Challenge-overlay values differ.
- Empty effective values produce no placeholder or fallback text.

The surface is explicitly a **test fixture**, not production typography, a safe-area specification or the complete Challenge composition. Its BODY is a neutral comparison field; it does not rasterize the 420 gameplay frames or the three physical game assets. Accordingly the report marks `gameplay_body_pixel_identity=NOT_TESTED_GAMEPLAY_NOT_RASTERIZED_IN_THIS_EDITORIAL_LAYER_FIXTURE`. It does not claim gameplay pixel identity.

`player_name` and `challenge_label` are carried, hashed and included in the composition, but their disposition remains `BLOCKED_GEOMETRY_UNRESOLVED`. No CHALLENGE_OVERLAY rectangle, typography, z-order, clipping or pixel position is guessed. `language` is metadata-only.

## 3. Preparation validation already performed

In the artifact-preparation environment:

- `test_c11e_e4a_challenge_pixel_review.py`: **23/23 PASS**.
- `py_compile` for the runner and focused test: **PASS**.
- Source payload materializer preimage from the user's current-source handoff: SHA-256 `8f8e4c9be6170d48319b62512a1e1cdb40c4f126563deb3546dfd302b080179e`.
- Prepared materializer postimage: SHA-256 `4cf2c754c9675ebb3952a292a21af71634102cf7d880f71a871ba7d7555ac6ed`.
- New shared-service runner SHA-256: `939a12f369df9eaa0dbaf5b06b0635a0d4dc906e14fd7d5bdf9c12b3ec2b97a0`.
- New focused test SHA-256: `f6adf4a10a55af167d9ac255cbce0c49b521dc87897d0519c0e955650d642fa9`.

No Godot executable is installed in the preparation environment. Therefore no Godot parse/runtime result, PNG output, Windows acceptance or visual PASS is claimed here. The active Windows run is the next evidence gate.

## 4. Windows runtime command

After applying the companion overlay and confirming the existing frozen manifest, run from the repository root:

```powershell
python -B .\tools\c11d\d9\c11e_e4a_challenge_pixel_review.py --godot $env:C11D_GODOT_EXECUTABLE
```

The driver checks the frozen manifest, Challenge source, approved policy and D1.5 source pins; runs the 23 focused Python tests; resolves A/B/C through the existing E1 shared service; probes Godot 4.7.1; invokes the opt-in existing materializer; verifies Godot exit code, output report, 18 PNG hashes/dimensions and 12 comparison outcomes; and writes the receipt and SHA list under `artifacts/tests/c11e/e4a_pixel_review/RUN_*`.

A nonzero exit, missing PASS marker, Godot `ERROR:` / `SCRIPT ERROR:`, missing image/report, hash mismatch or unexpected comparison blocks the run. It does not call FFmpeg or the C11-C production producer.

## 5. What is still required before E4A can close

1. Run the opt-in Godot test on Windows and inspect all 18 PNGs plus its report/receipt.
2. If the fixture passes, implement the actual D-owned visual composition on the existing Challenge presentation/render route, without using C11-C reserved editorial aliases. That subsequent integration must render the real Challenge body and prove body/gameplay pixel identity while changing only the approved editorial regions/windows.
3. Resolve `CHALLENGE_OVERLAY` only from an authoritative D1.5/profile/family geometry source, or keep the two Challenge-only fields blocked.
4. Use the accepted E3 D3 V5 mux/QC path for test-only audiovisual acceptance after visual pixels pass. Reuse existing gameplay output when possible; do not rerender gameplay just to vary the music seed.
5. Complete the E4A review receipt and operator visual acceptance. Only then mark E4A closed.

## 6. Immutable boundaries

No C11-C source file is changed. `SimulationResult`, `winning_frame`, `close_calls`, RNG, mechanics, `FrameSnapshot.custom_data`, C7/core audio, D3 V5, D9.10 dispatch and the E1 service are not modified. No production renderer activation, production dispatch, MP4/media, baseline freeze, promotion or release authority is introduced. C11-C 2.19.12 remains the sole production baseline.
