# C11-E Execution Backlog — V60

**Date:** 2026-11-07

## Priority 0 — Close the existing R1P archive false negative (no rerun)

1. Add-only install `C11E_E4B_R1P_ARCHIVE_RECOVERY_V1`.
2. Run `RECOVER_C11E_E4B_R1P_EXISTING_RUN_V1.ps1` once for `E4B_R1P_20261107_032743_5F75045C`.
3. Require `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`, 27 receipt JSON + 27 sidecars, 30/30 active-checkout source pins, matching D9.9/D9.10 bindings, matching stdout/stderr hashes and the new recovered ZIP SHA.
4. Do not rerun Godot or recipe generation. Preserve the original failed ZIP as immutable evidence; recovery writes a new `_RECOVERED.zip` and a separate report.

The R1P materialization itself already reports `PASS_R1P_PARAMETER_PAYLOADS_27_OF_27`. The recovery verifier has also passed against an isolated V84 extraction and produced a normalized archive. The error was the V1 ZIP-entry predicate: .NET/PowerShell wrote `receipts\...` names and the runner searched only `receipts/...`. Normalize entry names before counting JSON and SHA-256 sidecars. V2 provides the corrected predicate for any genuinely new R1P run; it is not needed to complete the retained run. The active-checkout recovery invocation remains the only operator action needed to close packaging evidence.

## Priority 1 — E4B R1V / actual visual payload (design complete; execution gated)

R1V is the next technical workstream, but this backlog entry authorizes design/preflight only. The separate versioned R1V design defines the required evidence contract: actual C11-C output-frame inventory, per-frame decoded-pixel hashes, stable frame index/PTS order, dimensions, timebase, codec/pixel-format metadata, source-media hash and immutable links back to the R1P receipt and D9.9/D9.10 parent. The measured count must agree with the resolved duration × 30 FPS (600/660/690 for 20/22/23 seconds); observed output, not the recipe descriptor, remains authoritative.

Execution is blocked until D4.8 has explicit authorization and the D-only baseline/policy conflict has an approved disposition. Until then, do not invoke a family launcher, prototype, renderer, FFmpeg, audio/D3, compositor, or frame/pixel extraction. No R1V frame inventory or pixel payload exists yet.

## Priority 2 — E4B R1V / actual visual payload

Design the distinct D-owned stage that obtains an actual C11-C output-frame inventory and hashes without mutating C11-C mechanics or protected sources. The R1P report is not a substitute for frame evidence. The future stage must preserve frame count, frame identity, frame order, timing and source pixels. Renderer-native input and D-only composition remain blocked pending D4.8 authorization and the independent baseline/policy resolution.

## Priority 2 — E4B visual acceptance and audio

After separate D4.8 authorization and accepted R1V frame/pixel evidence plus a real D-only consumer: five isolated silent family visual pilots, one per family; review all layers, pixel identity, text fit, geometry and deterministic repeats; then extend to 27 grammars. Continue to keep the visual launcher `-NoSound`. A future approved audio adapter may use `request.music_seed` independently; no family music synthesis, D3 V5, PCM, mux or FFmpeg is authorized by R1P.

## Subsequent work

E4C Drill retains its distinct timeline/binder/music contract. E5, Smoke18, Matrix99 (99 provisional runnable; CH_008/009 held) and E8 remain later and independently gated. C11-C 2.19.12 remains immutable until a separate approved replacement freeze and promotion.
