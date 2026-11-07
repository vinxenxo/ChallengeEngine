# C11-E Current Authority — V87

**Date:** 2026-11-07  
**Authority rule:** the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` remains the only source authority. V84 and all ZIPs are evidence/context only. Never unpack a snapshot over the checkout. Do not inspect or operate Git. Use PowerShell 5.1, Python 3.13 and Godot 4.7.1 where a gated test requires them.

## 1. Immutable baseline and global constraints

C11-C 2.19.12 remains immutable. Frozen manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). Do not edit the manifest, mechanics, RNG, renderer, binder, timeline, protected paths, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream` or `FrameSnapshot.custom_data` serialization policy. Preserve five GUI surfaces, no parallel binder or sixth operational surface. Keep `request.seed` and `request.music_seed` independent.

## 2. Accepted prior phases

- E4A D99 GUI/CLI parity: `PASS_TEST_ONLY`; fixture `artifacts/tests/c11d_d9/producer_universal/D99-GUI-37559C528640/` already exists. Do not repeat.
- E4B static family mapping: `PASS_STATIC_SOURCE_MAPPING`, 5/5 families and 27/27 explicit selectors. Do not repeat absent regression.
- E4B family-stage/D9.9/D9.10 contracts: accepted static/plan-only; not a renderer consumer.
- E4B R1P run `E4B_R1P_20261107_032743_5F75045C`: **CLOSED_PASS_27_OF_27**. Operator recovery exit 0; 27/27 canonical receipts and sidecars; 5/5 family coverage (5/5/7/5/5); 30/30 live source pins; Python/Godot executable pins PASS; recovered ZIP path separators normalized, all 72 archive member byte streams preserved. Do not rerun or reinstall R1P.

R1P evidence:

| Item | SHA-256 |
|---|---|
| Original ZIP | `a3bb4ddd6f4933026b0221c7e0eb1b62ffe40d477d72ce0190bbe9587b67b800` |
| Recovered ZIP | `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52` |
| Recovery report | `6bd16983a01919c7c41f785b281988139ae2a569a23daa81db6a20694f21c640` |
| Recovery process receipt | `b4299cca349b646cc05fffaf83765f5108ad55b70d177d27ce0745031a4c07a0` |
| Canonical R1P report | `9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41` |
| Parent bindings | `460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a` |

R1P timings (20/22/23 seconds at 30 FPS; 600/660/690) are parameter descriptors, not measured frame inventories. R1P created no prototypes, C source video, frame inventory, pixel payload, audio, mux or media.

## 3. Operator architecture decision — Option C approved

The operator explicitly approved Option C: one D-owned post-composition consumer reads an immutable silent C11-C source artifact, binds the measured R1V source/frame/pixel evidence and canonical D9.9/D9.10/R1P lineage, then emits a separate D-owned output. D3/music/mux remains a later independent gate.

This approval is architecture-only. It does not authorize R1V launchers, FFprobe/FFmpeg, D compositor dispatch, media generation, audio, mux, production, promotion or release. Do not ask the operator to select A/B/C again.

## 4. Option C static contract implementation

New D-only files:

- `tools/c11d/d9/c11e_option_c_postcomposition_contract.py`
- `tools/c11d/d9/test_c11e_option_c_postcomposition_contract.py`
- `tools/c11d/d9/RUN_C11E_OPTION_C_POSTCOMPOSITION_CONTRACT_V1.ps1`
- Three fixed JSON records under `definitions/c11d/production/`: architecture decision, non-dispatchable boundary and R1V qualification-only policy proposal.

Overlay package: `C11E_OPTION_C_POSTCOMPOSITION_HANDOFF_V1_20261107.zip`. Installer is add-only, preflights 17 unique destinations and validates the frozen C manifest plus accepted static audit before writing.

The validator checks the recovered R1P archive, 27 canonical receipts/sidecars, all canonical D9.9/D9.10/family-stage bindings and the family distribution. It revalidates the 30 R1P source pins and three new Option C policy pins (33 live pin validations; proposal/manifest are already among the 30 inherited pins), recomputes canonical receipt/report digests and verifies four process-log hashes. It produces 27 handoffs in `PREPARED_WAITING_FOR_R1V_ACTUAL_SOURCE_EVIDENCE` state.

Local isolated validation against the 30 source files reconstructed from V84 and the recovered R1P archive: Python 3.13, 9/9 unit/negative tests; contract `PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY`; R1P receipts 27/27; handoffs 27/27; source pins 30/30; new policy pins 3/3; total live pin validations 33/33. This was a reconstructed local sandbox, not a claim about the active Windows checkout. The next Windows runner must create the authoritative active-checkout process receipt.

The contract module has no process/media dispatch surface. It does not invoke C launchers, Godot, FFprobe, FFmpeg, compositor, D3, audio or mux; it creates no media.

## 5. E4A.6 protected-root conflict remains open

`GeneradorMaestro.gd` frozen C preimage SHA: `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`; intentional E4A.6 D-only postimage SHA: `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. State remains `KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT`. Option C should remove the Loop consumer's reliance on this protected root path, but current static handoff acceptance does not retire the postimage. Do not restore blindly, alter the frozen manifest or weaken baseline candidate policy. Reassess only after the D-only Loop consumer is implemented and accepted independently.

## 6. R1V and composition authorization

R1V design is complete. The exact five-family / ten-launch policy is recorded in `C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V1.json`, currently `PROPOSED_NOT_APPROVED`, `execution_authorized=false`; policy author and independent reviewer remain unassigned, operator approval pending. The active production activation policy v1 remains `DISABLED`. Historical D4.8/D4.9 PASS/CLOSED (8/8 governance and 102/102 parity) proves denial behavior, not authorization.

First run the new static Option C contract runner from the active checkout and capture its receipt. Then assign a policy author and independent reviewer and obtain explicit approval of the exact five-selector/two-repeat (10 calls) R1V-only scope. The policy allows only five pinned C11-C launchers with `-NoSound`, gameplay seed from `request.seed`, ten unique empty output roots, read-only FFprobe and FFmpeg decode-only frame hashing. It forbids D compositor, D9.10 renderer dispatch, D3/audio, PCM, FFmpeg encode/filter/mux, production, Smoke18/Matrix99, freeze, promotion and release.

After the five pilots and repeat comparisons pass, separately admit the remaining 22 selectors. Only after measured source evidence and approved layout/field windows should the single D compositor be implemented/executed under its own authorization. D3/audio/mux comes after visual consumer acceptance.

## 7. Current gate states

| Gate | State |
|---|---|
| E4B R1P | CLOSED_PASS_27_OF_27 |
| Option C architecture | OPERATOR_APPROVED_OPTION_C |
| Option C static handoff | PASS_LOCAL_9_OF_9_AND_27_OF_27; active Windows run pending |
| R1V design | DESIGN_COMPLETE |
| R1V physical qualification | BLOCKED_PENDING_SEPARATE_D4.8_AUTHORIZATION |
| D-only Loop compositor | NOT_IMPLEMENTED; separate authorization later |
| Loop layout/font/field windows | PROPOSED_NOT_APPROVED |
| E4A.6 protected path conflict | KNOWN_OPEN_PENDING_CONSUMER_ACCEPTANCE |
| D9.10 | PREPARE_ONLY |
| D9.14 | BLOCKED |
| D9.16 | BLOCKED |
| D9.17 | BLOCKED_NO_GO |
| D10 | BLOCKED_FOR_PROMOTION |
| Release authority | NONE |

CH_008/009 remain held: declared 11 seconds vs 12-second phase sum. Provisional Challenge runnable scope remains 99. Do not expand longform.

## 8. Immediate next actions

1. Install the Option C static overlay add-only in the active checkout.
2. Run `RUN_C11E_OPTION_C_POSTCOMPOSITION_CONTRACT_V1.ps1` from the active checkout. Expected `PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY`, 9/9 tests, 33/33 pin validations and renderer OFF. Preserve report/process receipt/stdout/stderr hashes.
3. Reconcile that live receipt. Do not rerun R1P, D99, static family audit or documentation phases.
4. Complete policy author + independent reviewer assignments and operator authorization for the bounded R1V scope before any launcher invocation.

## 9. Hard locks

`C11-C=IMMUTABLE`; `renderer=OFF`; `D4.8=BLOCKED_FOR_R1V_QUALIFICATION`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`.
