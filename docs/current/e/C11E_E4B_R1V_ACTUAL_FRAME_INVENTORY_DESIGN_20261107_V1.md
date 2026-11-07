# C11-E E4B R1V — Actual Frame Inventory and Pixel Payload Design V1

**Date:** 2026-11-07  
**Design state:** `DESIGN_COMPLETE_PREPARE_ONLY`  
**Execution state:** `BLOCKED_D4_8_AND_BASELINE_POLICY`  
**Scope:** Visual Loop families only; 27 explicit grammar selectors; no execution in this increment.

## 1. Purpose and boundary

R1P has now materialized 27 request-bound, deterministic parameter recipes and timing descriptors in memory. R1V is a distinct evidence stage: it must establish the actual C11-C output frames, frame inventory, timing/order and decoded pixel identity. It must not infer rendered frames from R1P `frame_count`, and it must not turn a D9.10 plan into renderer input.

This document is a design record only. It does not authorize any C11-C family launcher, prototype, scene, renderer, frame extraction, FFmpeg, audio/D3, compositor, pilot or media operation. The user's authorization to continue the development plan does not constitute D4.8 renderer authorization.

## 2. Entry conditions

All of the following are required before any R1V execution:

1. R1P archive recovery has status `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`, with its report, process receipt and recovered ZIP SHA.
2. D4.8 has a separate approved evidence docket, verifier result and explicit operator authorization that names the allowed five-family launcher execution and read-only frame/pixel inspection scope.
3. The known `GeneradorMaestro.gd` E4A.6 D-only postimage conflict has an explicit architecture/policy disposition for the D candidate. Do not restore it, alter the frozen C11-C manifest or weaken the baseline protected-path policy.
4. The active checkout still matches the R1P source pins for the C11-C helpers, family prototypes/launchers and frozen manifest, or a newly versioned preflight identifies an approved postimage without changing the C11-C freeze.
5. The five D-only family-stage contracts and 27 R1P receipts/parent bindings remain valid and non-dispatchable until the specific D4.8 authorization is recorded.

Failure of any entry condition means `R1V=BLOCKED`; no partial launcher attempt is allowed.

## 3. Work units

### R1V-A — Single-family qualification design

After D4.8 authorization, select one explicit grammar per family from the already accepted static family/selector mapping. The selection must be deterministic and recorded before execution. Do not invent a new selector mapping or derive it from recommendation order. Use isolated, collision-free output roots/tags for every case. The launcher output directory must not contain prior output that a launcher could delete or replace.

Run the existing family launcher only through its declared C11-C CLI contract, using the exact R1P gameplay `request.seed`, explicit grammar ID and duration descriptor, and the silent option (`-NoSound`). No music seed is passed to the visual builder. Do not patch the launcher, prototype, mechanics, RNG, shared helpers or protected paths.

### R1V-B — Actual source-frame inventory

For every approved output, capture actual media metadata from the produced source artifact rather than trusting the R1P timing descriptor. At minimum record:

- run ID, family ID, grammar ID/index, linked R1P receipt SHA and parent-binding SHA;
- launcher path/SHA, prototype path/SHA, helper/source pin set, seed domain and `request.seed`;
- source artifact relative path, byte length and SHA-256;
- container/codec, pixel format, width, height, sample/display aspect ratio, frame rate, timebase, start PTS, duration and observed frame count;
- one ordered record per decoded frame containing zero-based frame index, integer PTS, rational/time-base interpretation, timestamp in seconds, dimensions/pixel format and decoded-pixel SHA-256.

The actual frame count must be measured from the source artifact. Compare it to `duration_seconds × fps` from R1P as a consistency assertion only: at 30 FPS the current policy descriptors imply 600, 660 or 690 frames for 20, 22 or 23 seconds. Any disagreement is a failed case requiring diagnosis; do not synthesize, drop, duplicate, pad, interpolate or silently retime frames to make the count fit.

### R1V-C — Pixel payload identity

The pixel evidence must refer to decoded source pixels before any D-only composition. Preserve source width/height, frame order, timestamps and decoded pixel content. No crop, stretch, resize, resample, frame-rate conversion, palette remap, overlay, color grade or editorial drawing is permitted in R1V.

Record exact decoder/tool versions and arguments, pixel format, color range, color primaries/transfer/matrix where present, and the hash algorithm/byte serialization used. A decoded-frame hash is meaningful only when its pixel-format and color metadata accompany it. Any extracted lossless frame payload must be an unmodified decode of the source frame; hash both each payload file and its decoded pixel bytes. The implementation choice between a lossless frame spool and a direct source-decoder frame stream must be fixed in a separate implementation contract after inspecting the existing D-only consumer seam; do not create a parallel binder or new operational surface.

### R1V-D — Deterministic repeat and review

Repeat the same approved selector in a separate unique output root. Compare frame count, frame identity/order, timestamps and per-frame decoded-pixel hashes. A mismatch fails determinism; it must not be normalized away. Retain both source-media hashes, inventories, frame hashes, stdout/stderr, process exit codes and verifier output.

## 4. Proposed staged scale

After explicit authorization, execute five isolated silent qualification cases, exactly one predeclared selector from each of the five families. Review all five inventories and payload hashes, plus one deterministic repeat per qualification case. Do not extend to the remaining 22 selectors until the qualification evidence and D-only consumer seam have been independently reviewed and accepted. The eventual 27-selector expansion is a separate gated batch, not implicit from five-case success.

## 5. Deliverables

The later R1V implementation should add, under a unique versioned evidence root:

- `r1v_run_manifest.json` — run identity, entry approvals, exact selector set and source pins;
- one `frame_inventory.json` per selector — measured media/frame metadata and ordered per-frame records;
- `frame_hashes.sha256` or equivalent canonical manifest — stable SHA-256 values for all decoded source frames;
- optional immutable lossless pixel-frame payloads only if required by the approved consumer contract;
- `r1v_report.json` and sidecar — acceptance status, measured counts, deterministic-repeat result, source/pixel identity, process evidence and governance flags;
- captured process stdout/stderr and hashes, tool executable pins and a verifier receipt.

No R1V result may overwrite an earlier run or source artifact. Use unique output names and fail closed on collisions.

## 6. Explicit non-goals

R1V does not build the D9.10 renderer consumer, alter `GeneradorMaestro.gd`, change C11-C generators/mechanics/RNG, change `SimulationResult`, `winning_frame` or `close_calls`, change `WinningFrameDetector` or `RenderedFrameStream`, add a sixth GUI surface, serialize all `FrameSnapshot.custom_data`, run music/D3, synthesize PCM, mux audio/video, run Smoke18/Matrix99 or promote a release.

R1V frame evidence alone does not make the D consumer production-ready. D4.8, D9.10, D9.14, D9.16, D9.17 and D10 remain separate acceptance/authority gates.

## 7. Current governance locks

`renderer=OFF`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. No R1V process has been executed and no actual frame inventory or pixel payload is claimed.
