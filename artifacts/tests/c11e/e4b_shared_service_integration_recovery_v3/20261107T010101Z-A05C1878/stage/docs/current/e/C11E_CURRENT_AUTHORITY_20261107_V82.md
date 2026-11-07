# C11-E Current Authority — V82

**Date:** 2026-11-07. Sole authority: active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. V79 Nightly and all ZIPs are read-only source/evidence snapshots. Operator manages commits; do not inspect Git/HEAD/status/branch/`.git`; never extract ZIPs over checkout.

## 1. Accepted baseline and E4B evidence

- C11-C 2.19.12 remains immutable production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- E4B matrix remains accepted `PASS_TEST_ONLY`: five families, 27 grammars, 81 plan cases, deterministic repeats, 27 seed relations, GUI/CLI parity 81/81. Do not rerun absent regression.
- E4B Family Contract V2 remains accepted static audit only: 40/40 base pins, 8/8 local pins, 8/8 tests, 27/27 selectors. Report SHA `788ab1352a3e11bd91cc2ddf34fc8f11334b7713b9bc1a2b246156c79f40444e`; 27/27 historical MP4 path presence is not a visual review.
- V2 shared-service source patch postimages are pinned by `C11E_E4B_SHARED_SERVICE_INTEGRATION_V2_SOURCE_PINS.json`; they must be verified in the active checkout before further work.

## 2. V2 installer incident — corrected diagnosis

V2 printed all preflight confirmations, including the six short backup paths, then surfaced Windows PowerShell 5.1 `ArgumentException: Argument types do not match`. The exception is consistent with a documented PowerShell 5.1 issue: a `System.Collections.Generic.List[object]` created with `New-Object` was placed in an array-subexpression `@($list)` while constructing the post-install receipt. The reduced case is tracked in PowerShell issue #27558: https://github.com/PowerShell/PowerShell/issues/27558.

In the V2 installer, source backup, add-only installation and source replacement occur inside the guarded transaction. The final receipt array conversion occurs after that transaction. Therefore the observed unhandled exception likely happened **after** all 6 source postimages and 15 add-only files were written, not during the preflight. No V2 install receipt was emitted. Do not rerun V2 blindly: it would hit the same receipt defect again.

V3 is a reconciliation/finalization overlay. It does not reapply or modify the six V2 source patches. It verifies exact postimage hashes for all six sources, exact hashes/lengths for all 15 V2 add-only outputs, and all six backup slots against their preimage hashes. Only if all three sets pass does it add new versioned documents and a stable V3 runner and write a recovery receipt. A missing or differing item is a hard stop before V3 writes.

## 3. V3 acceptance semantics

Successful V3 recovery means:
- V2 integration files are present exactly at their pinned postimages;
- all V2 add-only files are present byte-identically;
- six exact preimage backups are found and validated;
- V3 recovery documents/tools are installed add-only;
- no source patch is reapplied by V3.

The V3 runner then verifies the V2 state, reruns the 25 E shared-service tests, D9.8 model tests, Python syntax compilation, and read-only D9.15/D-baseline diagnostics. The runner avoids the PowerShell generic-list array-subexpression defect by using ordinary arrays and explicit array materialization.

## 4. D/E blockers and order

1. Accept V3 recovery audit and V3 runner on Windows PowerShell 5.1 / Python 3.13.
2. E4B-R1: implement request-scoped Loop payload materialization; prove actual payloads and create 27 immutable per-grammar receipts (request identity, family/grammar, launcher pins, frame_count/FPS/duration, frame inventory and hashes). Historical authoring MP4 presence does not substitute.
3. E4B-R2: connect the D-only pixel consumer at the verified bridge/adapter seam; prove source-frame identity/order, 720x1280 geometry and approved no-crop/no-stretch/no-resampling composition.
4. D4.8 remains independently blocked. Candidate baseline/evidence, verifier and operator authority must be resolved through its own gate; E4B approvals and tests are not a waiver.
5. Only after payload receipts and D4.8 authorization, run five silent family pilots, one representative per family. Review geometry, typography, layers and pixel identity. Then scale to 27 Loop grammars.
6. Run existing C11-C family music separately using `request.music_seed`; visual stage uses `-NoSound` and `request.seed`. Then mux, FFprobe and A/V QA.
7. E4C Drill retains its distinct phase/timeline/binder/music contract. Then E5, Smoke18, Matrix101 (CH_008/009 held; 99 provisional) and E8 independent acceptance/freeze/separate promotion.

## 5. Governance

Renderer OFF; dispatch OFF; launchers NOT INVOKED by V3; media/audio false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; release authority NONE. Never modify C11-C core, generators, binders, mechanics, simulation truth, frame stream or RNG.
