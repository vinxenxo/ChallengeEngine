# C11-E Option C — D Post-Composition Consumer Contract V1

**Date:** 2026-11-07  
**Architecture decision:** `OPERATOR_APPROVED_OPTION_C`  
**Implementation state:** `STATIC_HANDOFF_CONTRACT_PASS_27_OF_27_PREPARE_ONLY`  
**Scope:** Five C11-C Loop families / 27 explicit R1P grammar selectors.

## 1. Approved architecture

The operator approved Option C: a single D-owned post-composition consumer reads the immutable silent C11-C source artifact and its R1V actual-frame/pixel evidence, applies D-owned editorial/presentation, and emits a distinct D-owned output. C11-C continues to own visual mechanics, deterministic gameplay seed, source-video rendering and source timing. D3 audio and A/V mux remain later, separately gated stages.

This approval is architectural only. It does not authorize R1V launchers, FFprobe/FFmpeg, D compositor dispatch, media generation, D3/audio, mux, production, promotion or release.

## 2. Static handoff implementation

`tools/c11d/d9/c11e_option_c_postcomposition_contract.py` verifies the accepted recovered R1P archive and emits 27 non-dispatchable handoff records. Each handoff binds:

- R1P receipt, payload and deterministic repeat digests;
- canonical D9.9 request, plan and editorial hashes;
- D9.10 bridge identity and D-only adapter envelope hash;
- D-only family-stage contract identity;
- frozen C11-C manifest digest;
- gameplay seed from `request.seed`, with `request.music_seed` retained only as future D3 lineage;
- R1P duration/FPS/frame-count consistency descriptors, explicitly not measured frame inventory.

The validator rechecks 30 R1P source pins against the project root plus three new Option C policy/decision pins (33 live validations total), recalculates the canonical receipt-set and report digests, and verifies four embedded process-log hashes and their zero exit codes. The composition proposal and frozen C11-C manifest remain covered by the original 30 R1P source pins; they are not counted twice.

The result is `PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY`. The test harness adds negative checks for dispatch flags, source/output path collision, seed-domain separation and the absence of process/media dispatch calls in the contract module.

## 3. Artifact boundary

The future D consumer must require all of the following before it is allowed to run:

1. A byte-pinned C source video, kept separate and immutable.
2. R1V measured container/stream metadata and actual ordered frame inventory.
3. Per-frame decoded-pixel identity evidence and repeat comparison.
4. Canonical D9.9/D9.10/R1P parent identities.
5. Approved Loop layout, fonts, text fit and field windows. The present 720×1280 layout is only a proposal and is not executable renderer input.
6. A separate D compositor authorization after R1V acceptance.

The consumer may not overwrite, rename as D output, or mutate the C source. It must preserve source frame identity/order and must fail closed on any undefined transformation. A D output will be a different path and artifact identity.

## 4. R1V qualification-only request

`definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V1.json` proposes exactly five selectors, one per family, each executed twice (10 C11-C launcher invocations). It pins each launcher and prototype against the R1P source set, requires `-NoSound`, uses only the gameplay seed bound in R1P and requires ten unique, initially nonexistent output roots.

Permitted inspection is limited to read-only FFprobe metadata and FFmpeg decode-only frame streaming into an in-memory pixel hasher. FFmpeg encode/filter/mux, D compositor, D9.10 renderer dispatch, D3/audio/PCM, production, Smoke18/Matrix99, freeze, promotion and release are explicitly forbidden.

The policy remains `PROPOSED_NOT_APPROVED`: author and independent reviewer are unassigned, operator approval is pending, and `execution_authorized=false`. D4.8 renderer policy v1 remains DISABLED. No R1V launcher invocation is authorized by this package.

## 5. Implementation tests and invocation

Run from the active Windows checkout in PowerShell 5.1:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_OPTION_C_POSTCOMPOSITION_CONTRACT_V1.ps1" -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
```

The runner executes Python 3.13 unit/negative tests and then builds the handoff report. It captures exit codes and stdout/stderr hashes for both processes. It does not call Godot, FFprobe, FFmpeg or any launcher.

Expected status:

```text
OPTION_C_STATUS=PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY
R1P_RECEIPTS=27/27
OPTION_C_HANDOFFS=27/27
R1P_SOURCE_PINS=30/30
OPTION_C_POLICY_PINS=3/3
TOTAL_LIVE_PIN_VALIDATIONS=33/33
R1V_QUALIFICATION_POLICY=PROPOSED_NOT_APPROVED
R1V_EXECUTION_AUTHORIZED=FALSE
RENDERER=OFF
MEDIA_CREATED=false
RELEASE_AUTHORITY=NONE
```

The active checkout runner receipt, not an isolated development copy, is the authority for the current run.

## 6. Known E4A.6 protected-path disposition

`GeneradorMaestro.gd` remains classified `KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT`. Option C is designed to eliminate the Loop D consumer's dependency on the protected C root path, but this static handoff acceptance does not retire the current postimage. Do not restore the file, edit the C11-C manifest or add a protected-path exception as part of this increment. Revisit retirement only after the D-only consumer is implemented and accepted without that path.

## 7. Current hard locks

`C11-C=IMMUTABLE`; `renderer=OFF`; `D4.8=BLOCKED_FOR_R1V_QUALIFICATION`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`.

No visual or audio media was created by the static contract implementation.
