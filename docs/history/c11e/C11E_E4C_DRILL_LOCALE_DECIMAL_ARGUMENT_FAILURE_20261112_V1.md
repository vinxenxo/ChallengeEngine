# C11-E E4C Drill — D99 GUI A/V locale decimal argument failure and V1.4 remediation

**Date:** 2026-11-12  
**Request:** `D99-GUI-85201B7B4FF7`  
**Selector:** `visual_drills / tracking / tier-1`  
**Gameplay seed:** `12345`  
**Music seed:** A/B `840001`, C `840002`  
**Delivery:** `REVIEW_720`

## Evidence identity

- `D99-GUI-85201B7B4FF7.zip`: SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`.
- `D99-GUI-85201B7B4FF7-tests.zip`: SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

## What passed

1. E1 intent validation: `PASS_E1_PREPARATION_ONLY`, valid true, source pin count 91.
2. GUI/CLI semantic parity: PASS; request, editorial, plan and D envelope hashes equal.
3. Producer universal receipt: `PASS_BRIDGE_PLANNING_ONLY`, expected plan-only status.
4. D composition plan: PASS/ready for isolated execution; title/subtitle/CTA are non-empty and visible during GAME, hidden during PRE_ROLL, END_CTA and DONE.
5. FAMILY_MUSIC_V4 selection: `FLOWING_VECTOR`, consistent with tracking.
6. Frozen C11-C manifest and source preflight identities match expected pins.

The tests ZIP contains planning and contract receipts; it is not a second independent A/V failure report. Plan-only flags (`renderer=false`, `media_created=false`) in those receipts are expected and must not be interpreted as GUI errors.

## Root cause of the A/V failure

The exact log says the existing `run_visual_drill_production.ps1` parameter `SpeedMultiplier` rejected value `75000` because maximum is `3`. The tracking profile's tier-1 speed multiplier is the pinned numeric value `0.75`. The D adapter previously called `locale.setlocale(LC_NUMERIC, "")`, then replaced decimal point with the host locale separator. On the operator's comma-decimal locale, the argument string became `0,75000`. Windows PowerShell 5.1's `-File` script parameter binding treated that comma decimal as an argument separator/conversion and delivered `75000` to the existing `[double][ValidateRange(0.1,3.0)]` parameter. This is a D-owned process-boundary serialization defect. It is not a defect in C11-C, the difficulty profile, E1, D composition, Qt, family music, FFmpeg or media QA.

## Stage boundary reached

The adapter successfully prepared both E1 intents, checked GUI/CLI semantic identity, validated E1, built/validated the D composition plan and checked pins immediately before native capture. It then failed inside native launcher parameter validation. No native source MP4/manifest/authoring product was emitted; therefore D frame composition, A/B/C music generation, mux, FFprobe, stream hashes and post-execution pin comparison were not reached.

The `RUNNING` receipt is retained alongside `FAILURE`; the original request output root is non-overwritable and should be preserved. Use a fresh request ID for retry.

## V1.4 corrective implementation

- Remove `locale` import and every host-locale numeric conversion.
- Format speed as invariant ASCII text (`0.75000`) and pass it only to `[string]$SpeedMultiplierInvariant`.
- Generated wrapper parses with `InvariantCulture`, range-checks 0.1..3.0, sets thread current culture/UI culture invariant for the invocation, and passes typed `$speed` to the unchanged C11-C script's `[double]$SpeedMultiplier` parameter.
- Restore thread cultures in `finally`; retain wrapper file/hash and invariant speed string in the run receipt.
- Add three unit tests: invariant format/range, wrapper parse/type bridge, and no locale-dependent formatter in the executor. Total adapter tests become 16.
- Installer stages and compiles a wrapper-emitter probe, parses generated wrapper/dummy scripts with the PowerShell 5.1 AST, forces `es-ES`, calls the exact wrapper against a dummy launcher with `[double]$SpeedMultiplier`, and requires captured invariant text `0.75` before repository transaction.
- C11-C launcher, E1 service, Qt consumer, GUI and CLI source remain unchanged in V1.4.

## Next gate

Install V1.4; require `INVARIANT_SPEED_WRAPPER=PASS`, `STAGED_TESTS=16/16`, `PY_COMPILE=7/7`, source/destination checks, transaction preflight and complete receipt. Audit postimages. Generate a fresh GUI request ID and repeat only the one-selector `tracking/tier-1` A/V test. If native capture completes, proceed through D composition, FAMILY_MUSIC_V4 A/B/C, mux/FFprobe, bitstream comparison and operator visual/listening acceptance. Then CLI parity smoke; then the 20-selector A/V qualification. E4C remains open until those gates pass.

## Governance

E1 `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`; C11-C 2.19.12 sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; production dispatch false; release authority NONE; no Git checks; commits operator-managed.
