# C11-D → C11-E Full-Family Roadmap — V49
**Target:** a reliable D+E audiovisual production factory that can supersede C11-C only after independent evidence, complete historical regression, immutable freeze and an explicit promotion decision.

## Current location

Five Loop families and 27 grammars are mapped. R1P payload proof is closed 27/27. Option C handoffs are 27/27 `PASS_PREPARE_ONLY`; the generalized D post-composition consumer is not implemented. The bounded R1V five-family A/V attempt has generated 10/10 outputs but remains OPEN / FAIL-CLOSED because Geometric Waves A/B pixel frames are not identical. Four family pairs are exact. Geometric A/B has equal input metadata, seeds, frame count, PTS, WAV and AAC, but 0/690 exact pixel hashes; global SSIM 0.984889 / average PSNR 35.61258 dB. Do not admit later phases yet.

## Required order (no skipping)

1. **R1V closeout:** resolve Geometric A/B source pixel determinism using read-only analysis of the two existing source MP4s; prove cause; make only an evidenced D/E-side fix if needed; requalify affected scope. Complete all ten visual/layer and audio human reviews. R1V closes only after exact A/B pixel identity and all acceptance conditions pass.
2. **Remaining 22 Loop grammars:** qualify all untested grammar variants and their family-native music; retain distinct family binders, grammar semantics, timing, and separate gameplay/music seed domains.
3. **Option C D consumer:** implement one generalized D post-composition consumer over immutable C video; preserve C mechanics, binders, timing and family-native music. Handoff PASS PREPARE_ONLY does not imply implementation or acceptance.
4. **E4B closeout:** close Loop family presentation/editorial/music requirements only on complete evidence.
5. **E4C Drill:** integrate layout/editorial; preserve C11-C Drill music, phase precedence and END_CTA behavior.
6. **E5:** cross-family determinism, isolated gameplay/music seeds, no adapter/profile leakage, GUI/CLI execution parity.
7. **E6 Smoke18:** six audiovisual scenarios per family.
8. **E7 Matrix101:** 54 Challenge + 27 Loop + 20 Drill. CH_008/CH_009 remain held until declared 11 s versus summed 12 s is resolved.
9. **E8:** full historical C-to-E case-by-case regression, independent acceptance, immutable freeze, and separate explicit promotion decision.

Before E8 reconcile the complete historical C11-C corpus, including known 27 review cases, nine Challenge cases and all other visual/review categories, into a row-by-row regression map. Smoke18 is a sample, not a substitute for complete family coverage.

## Current locks

C11-C 2.19.12 remains the immutable production baseline (manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). No C11-C code, shader, launcher, audio, mechanics, binders, RNG or manifest changes. General renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. R1V authority is bounded test-only.


## R1V latest forensic disposition (2026-11-08)

Latest pilot is OPEN / FAIL-CLOSED (52/52 test gate PASS, 10 outputs, 4/5 exact A/B family pairs). The Geometric Waves 690-frame pair is non-identical (0/690 hashes). Read-only regional metrics show strongest luma variation in Footer, then Header, then Body; no spatial offset. Source ZIP omitted AVI intermediates, so capture-vs-transcode stage is not yet known.

The next bounded diagnostic is prepared but awaits separate operator approval: two Geometric Waves captures only, existing C11-C launcher, `-KeepAvi`, same seed 100001/23 s/720×1280@30. This diagnostic is not full qualification, not a 52-test rerun and not production authority. The remaining 22 Loop variants remain blocked until R1V closes.

After R1V closure, keep order: remaining 22 Loop grammars → generalized Option C D post-composition consumer → E4B closeout → E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8. CH_008/CH_009 remain held at 11s/12s.


## V3 authoritative status update — 2026-11-08

This section supersedes any earlier statement in this document that the AVI-retaining diagnostic was pending, prepared, or not authorized. The operator installed documentation overlay V2 successfully (11/11 ADD files; install manifest SHA-256 `1b4c36ee2ed9d6ce8e7604cba585247d2cbabd4370b86ac9b662b488c802dd32`) and explicitly authorized exactly two Geometric Waves A/B captures with `-KeepAvi`. Those two captures are complete and independently audited.

**Diagnostic disposition:** `PASS_DIAGNOSTIC_NOT_REPRODUCED`. Run `GWDIAG_192813_C56B9C`; evidence ZIP SHA-256 `b76e1fb276d91c831f11bcba6069e751cab7afbc8248300b89c97843753b53d9`; diagnostic receipt SHA-256 `56e95b8c16590126d4ab082d1519988bed6edac6f3bfbe06463e5178f5b375f2`; AVI/MP4 stage-comparison JSON SHA-256 `eb533995f76617665040013933eea159b3c4c583787c029ae285d279652a3402`. Both slots exited 0. The A and B AVI files are byte-identical (50,692,122 bytes; SHA-256 `78be4ab46e7b04f3d7544e628c58e2d2f1d018e1ee7992e8db57bbd819ab6a1a`); the A and B MP4 files are byte-identical (13,728,044 bytes; SHA-256 `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`). Each stage has 690/690 exact framehash matches and equal PTS/DTS. The authoring JSON for A/B is identical (SHA-256 `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`). All 23 source pins matched before/after; `override.cfg` was absent before and after. No tests, full R1V wrapper, music generator, Git, or source modification occurred in this diagnostic.

**Critical distinction:** the new pair reproduces the historic R1V Geometric A source MP4 exactly, but does not explain or erase the historic B outlier (`a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`). Historical run `Q5_040414_B6BE4D` remains `FAIL_R1V_AV_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED`, with 0/690 exact Geometric A/B frame matches. The diagnostic proves that the two newly captured runs are repeatable at both AVI and MP4 stages; it does **not** establish the cause of the earlier B divergence or prove the pipeline is universally deterministic. Do not attribute the old event to Movie Maker, FFmpeg, GPU, `fwidth()`, timing, or any other component without new evidence. Do not relax pixel-hash acceptance and do not patch C11-C.

**Current R1V remains OPEN / FAIL-CLOSED.** Four other family A/B pairs remain accepted; do not repeat them. Do not repeat the 52/52 integrated test gate, R1P, Option C, or Fractal Bloom A absent a real dependency regression. Visual operator review is still only confirmed for Fractal Bloom A; all other required visual/layer slots are pending. All ten audio listening reviews remain pending.

**Next bounded action:** run the separate read-only kit `C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_PREFLIGHT_V1.zip` (SHA-256 `efe7d2de99b0b2a7ab925a482b5a815d93516774bf65cfd1c471ad164ab31fda`). It verifies the existing historical source MP4s, WAV/PCM/AAC outputs, final mux streams, new AVI/MP4 pair, historic reports/receipts, and 23 active source pins. It invokes FFmpeg/FFprobe only to probe and hash existing streams in memory and writes one JSON report plus SHA sidecar. It does **not** render, capture, generate music, mux, or alter source/media files. Expected marker: `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`. On any mismatch, stop fail-closed.

Only after that preflight passes, prepare a separate exact-scope two-output Geometric Waves mux-only requalification using the new identical MP4 A/B videos and reuse of the already-validated identical AAC audio streams from the historic A/V outputs. That future action is not part of the preflight and has not been authorized or executed here. It must not invoke C11-C capture, the music generator, the integrated five-family runner, the other four families, or the 52-test suite. Require separate explicit authorization before media mux. R1V acceptance remains withheld until the historical B discrepancy is formally resolved by evidence and the ten visual/layer plus ten audio listening reviews are complete.

Governance remains unchanged: C11-C 2.19.12 immutable; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; Git checks skipped and commits operator-managed. Remaining 22 Loop grammars and every downstream phase remain blocked pending R1V closeout.


## 2026-11-08 checkpoint — R1V Geometric controlled requalification

## Latest operator checkpoint — 2026-11-08: bounded mux-only requalification authorized, prepared, not executed

- Documentation V3 is installed PASS: 39/39 source pins, 11/11 documents, manifest SHA-256 `a899723f377780745299efcccceb3176212067e65ebe1ed10dc308f86d0a76d5`.
- The operator-uploaded receipt archive `r1v_geometric_av_reuse_preflight_ab_repeatability.zip` is 4,556 bytes, SHA-256 `12e4a9e1fd164cea9741260900049926be9e11b0d35072752b7c14cedb598b2e`; ZIP CRC is clean. It contains the reuse-preflight report, its SHA sidecar, and the V3 install receipt.
- Reuse preflight `GEOAVP_221712_C50A95`: `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`; report SHA-256 `fa8ecbcdefeca7299e983cb81d42326424cb1659bf6353190c3edec5eca80817`; 23/23 active source pins passed. No capture, media creation, music generation, mux, tests, or Git occurred.
- Historical WAV A/B, decoded PCM A/B and AAC elementary streams A/B are byte-identical: WAV SHA `dfe29efc0a3d945d55fbb7e278252d211abfb6f56deaaec3a292258e8b17d5ee`; PCM SHA `1f03e69f9546e52e3856b4228d4b6d4072f8af85abd2a67055d64c0058ec2a10`; AAC/ADTS SHA `ba3ad357b90de7af6d1a3df39470376e473611fed799003677dcc7de912aa51b`. Each WAV is 44.1 kHz, stereo, 16-bit PCM, 1,014,300 samples, 23 seconds.
- New diagnostic A/B source MP4s are byte-identical to each other and to historic Geometric A: SHA `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`. Their H.264 elementary stream SHA is `cb66b21fb92f74760406253c01b89a63c442ea217b73c868e9391f5258de9ac2`. Historic Geometric B remains the distinct outlier SHA `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`.
- The operator explicitly approved continuing with exactly two Geometric Waves A/V requalification outputs. The bounded runner in this package uses the new diagnostic MP4 A/B pair for video and the corresponding already-qualified historic A/B A/V files solely as AAC audio carriers. It performs `-c:v copy -c:a copy`; it does not encode AAC, alter H.264, generate WAV, capture, invoke Godot, run the integrated R1V wrapper, or repeat the 52 tests.
- Expected success status is `PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE`. It requires two outputs, H.264 preservation, exact AAC reuse, 690/690 decoded pixel hashes equal A/B, identical video PTS, conforming stream layout and A/V duration/start alignment, 23/23 protected source pins unchanged, and all source media unchanged.
- This is only a Geometric Waves technical replacement/requalification evidence pair. It does not erase the historic B anomaly's unknown cause, grant full R1V acceptance, complete human visual/layer or audio listening review, admit the remaining 22 Loop grammars, activate D rendering, or change `release_authority=NONE`.

The roadmap sequence remains unchanged: finish R1V technical and human acceptance; complete the remaining 22 Loop grammars; complete the generalized D-owned Option C post-composition consumer; close E4B; implement E4C Drill; then E5 cross-family determinism/seed isolation/adapter-profile non-leakage/GUI-CLI parity; E6 Smoke18; E7 Matrix101; E8 independent acceptance, immutable freeze and explicit promotion decision. CH_008/009 remain held for the declared 11-second versus 12-second phase-sum discrepancy. No phase is advanced by the mux-only preparation.
