# C11-E E4B R1V — Actual Frame Inventory and Pixel Payload Design V2

**Date:** 2026-11-07  
**Design state:** `DESIGN_COMPLETE_AWAITING_ARCHITECTURE_DECISION_AND_BOUNDED_D4_8_AUTHORIZATION`  
**Execution state:** `BLOCKED`  
**Scope:** 5 Loop families / 27 explicit grammar selectors. No launchers, renderers, extraction or media are invoked by this design update.

## 1. Purpose

R1P is closed and provides 27 deterministic request-bound parameter recipes. R1V must measure real C11-C output frames, ordering, timing and decoded pixel identity. It must never infer actual frames from R1P descriptors.

The recommended architectural direction is an immutable C source artifact followed by a D-owned post-composition stage. R1V therefore measures and hashes the C source video before D composition. The D output is a separate artifact; it must never overwrite or masquerade as the C source.

## 2. Entry conditions — all required

1. R1P recovery status is `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`; original/recovered archives and recovery process evidence are hash-pinned.
2. The operator has selected and approved the D/C isolation architecture. The recommended option is the external D-only post-composition route in `C11E_D_BASELINE_ISOLATION_DECISION_DOCKET_20261107_V1.md`.
3. The E4A.6 `GeneradorMaestro.gd` conflict has an explicit approved disposition that preserves the frozen C11-C manifest and does not create a silent protected-path exception.
4. A separately approved, bounded D4.8 qualification authorization exists for only the declared silent C11-C family launcher calls and read-only source-frame/pixel inspection. D4.8/D4.9 historical PASS/CLOSED under renderer DISABLED is not this authorization.
5. All active-checkout source pins for the selected family launcher, prototype, shared helpers, R1P receipt and parent bindings are revalidated immediately before execution.
6. Output roots are isolated and collision-free; existing artifacts are never overwritten. Every visual launcher uses its declared CLI contract and `-NoSound`. No D3, music, mux or final media delivery is part of R1V.

Failure of any condition means `R1V=BLOCKED`; no partial family launcher attempt.

## 3. Proposed five-family qualification set

Use the first explicit grammar in each accepted family selector map as a deterministic pilot proposal. These are proposed selectors, not execution authorization:

| Family | Pilot grammar | R1P case | Gameplay seed |
|---|---|---:|---:|
| Fractal Bloom | `radial_bloom` | 06 | 100006 |
| Geometric Waves | `harmonic_membrane` | 01 | 100001 |
| Invisible Forces | `dipole_field` | 21 | 100021 |
| Living Particles | `swarm` | 16 | 100016 |
| Sacred Symmetry | `astrolabe` | 11 | 100011 |

Use the existing R1P receipt's request-bound gameplay seed and identity. Do not pass or consume `music_seed` in the visual launcher. Each selector is executed twice into two independent, unique output roots to test repeat determinism. No selector remapping or automatic family selection is allowed.

## 4. R1V-A — actual source artifact capture

Invoke only the accepted C11-C family launcher for each authorized selector, by its declared CLI contract, with its exact R1P gameplay seed, grammar ID/index and timing request. Keep `-NoSound`; no D renderer or editorial consumer is invoked in this step. Preserve source artifact bytes and SHA-256. Capture executable paths/hashes, tool versions, arguments, environment, process exit code, stdout/stderr files and hashes.

The launcher may create its normal C source video artifact. This is the first point at which R1V performs physical source rendering and is therefore blocked until the bounded authorization in Section 2 is recorded.

## 5. R1V-B — measured frame inventory

Measure from the produced source artifact, not the R1P descriptor:

- run, family, grammar, R1P receipt SHA and D9.9/D9.10 parent hashes;
- launcher, prototype, helper and manifest source pins;
- source artifact path, byte length and SHA-256;
- container/codec, profile/level, pixel format, width/height, SAR/DAR, frame rate, timebase, start PTS and duration;
- measured decoded-frame count;
- per-frame zero-based index, PTS/best-effort timestamp, rational time-base value, timestamp seconds, dimensions, pixel format and decoded-pixel SHA-256.

At 30 FPS the R1P descriptors predict 600, 660 or 690 frames for 20, 22 or 23 seconds. Compare measured counts with these only as a consistency assertion. Never pad, drop, duplicate, interpolate, retime or normalize away a mismatch.

## 6. R1V-C — pixel hashing contract

Use the exact installed FFprobe/FFmpeg executable versions and SHA-256 pins. The implementation must fix one deterministic decode serialization before the first run. Recommended implementation: direct source-decoder frame stream into the hasher, avoiding a filesystem spool of thousands of intermediate images. The contract must record decoder command, frame selection semantics, pixel format, plane/stride serialization, color range, primaries, transfer, matrix, chroma location and byte order. Hash each decoded frame's exact serialized bytes and record the hash with its metadata. If the source format cannot be preserved deterministically, fail closed rather than silently convert; a documented canonical conversion requires a separately reviewed contract.

R1V reads source pixels only. It does not crop, stretch, resize, resample, grade, overlay, palette-remap or otherwise mutate the C source. The D compositor consumes the source separately and emits a distinct output file.

## 7. R1V-D — deterministic repeat

Repeat each pilot selector into a different empty output root. Compare measured frame count, index/PTS order, timestamps, dimensions, format/color metadata, and every decoded-pixel SHA-256. Compare source-media hashes as a separate byte-level diagnostic. Any frame identity/pixel mismatch fails; do not repair it by retiming or normalizing.

## 8. Scale-up

First qualify exactly five selectors (one per family) with two independent C source executions each. Review source media, full frame inventories, pixel hashes and repeat comparisons. Only after all five pass and the D-only post-composition consumer seam is accepted may the remaining 22 selectors be admitted as a separate 27-selector batch. The eventual goal is all 27 Loop grammars across five families, not stopping at the five pilots.

## 9. Deliverables

The implementation package must create a unique versioned evidence root containing `r1v_run_manifest.json`, one `frame_inventory.json` per execution, canonical pixel hash manifests, optional pixel payload files only if the approved consumer requires them, source artifact hashes, process logs/hashes, runtime executable pins, `r1v_report.json` plus sidecar, and a verification receipt. The verifier must independently validate R1P receipt/parent links, source pins, entry authorization scope, output-root isolation, observed frame metadata and pixel hashes.

## 10. Explicit non-goals

R1V does not modify C11-C sources/mechanics/RNG, any protected root file, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C11-C binders/timelines, or the five GUI surfaces. It does not build a parallel binder, run D3/music, create PCM, mux audio, run Smoke18/Matrix99, freeze a D baseline or promote a release.

## 11. Governance locks

`renderer=OFF`; `D4.8=BLOCKED_FOR_R1V_QUALIFICATION`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. No R1V physical evidence exists yet.
