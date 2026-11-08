## V5 correction checkpoint — 2026-11-08: preflight JSON nesting defect fixed; no mux occurred

The operator installed V4 successfully and then reported the V4 runner stopping with:

```text
STATUS=FAIL_GEO_AV_REUSE_MUX_ONLY_FAIL_CLOSED
ERROR=PREFLIGHT_NOT_READY_OR_ERRORS_PRESENT
```

Audit of the uploaded archive `r1v_geometric_av_reuse_mux_only_overlay_v4.zip` (1,295 bytes; SHA-256 `4c82f3f6486d7ac2405ceb278bfe379a34166df623ea0d70dcf0429cc913a63a`; CRC clean) found that it contains the V4 installer receipt only. That receipt confirms `PASS_ADD_ONLY_DOCUMENTATION_OVERLAY_V4`, manifest SHA `28510049c6c9785bfdab969cc6d07b90d3cab5564e72741cf4acbc365abdcad9`, 53 source pins verified, 11 payloads verified, zero changed files and 11 identical documents skipped. Its exact receipt SHA-256 is `49b09f3f32dfeb99521b86af4e0f59f650f9e4b57f53213277a8da98697b487f`.

The separate operator evidence archive `r1v_geometric_av_reuse_preflight_ab_repeatability.zip` (4,556 bytes; SHA-256 `12e4a9e1fd164cea9741260900049926be9e11b0d35072752b7c14cedb598b2e`) contains a valid preflight report and sidecar plus the V3 installer receipt. The report SHA-256 is `fa8ecbcdefeca7299e983cb81d42326424cb1659bf6353190c3edec5eca80817`; its status is `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`; `findings.errors=[]`; and both `findings.next_step.ready_for_scoped_geometric_waves_av_rebuild` and `findings.next_step.mux_not_performed` are `true`.

**Root cause is a V4 runner schema-navigation bug:** the report's `next_step` object is nested under `findings`, but V4 read `preflight.get("next_step")` at the document root. This raised `PREFLIGHT_NOT_READY_OR_ERRORS_PRESENT` even though the evidence report was valid. The failure happened in preflight before output-directory creation: no `GEOAVR_*` run folder, FFmpeg mux, A/V output, capture, music generation, or source mutation was produced by that attempt. The archive named `r1v_geometric_waves_av_reuse_mux_only_overlay_v4.zip` is an installer-receipt archive, not a mux-run evidence package.

V5 carries a corrected runner V2. It reads the schema-defined `findings.next_step`, explicitly validates the object types/flags/errors, and adds fail-closed negative controls. It also verifies and pins the exact V4 install receipt before proceeding. Six local regression tests include the actual operator-supplied preflight JSON fixture, missing/mislocated next_step, false ready/mux flags, and nonempty errors. This is a runner-only correction; no C11-C source, media source, preflight report, acceptance threshold, capture/mux scope or 52-test suite changes.

**Next operator action:** install this V5 documentation overlay with `INSTALL_C11E_R1V_GEOMETRIC_WAVES_PREFLIGHT_SCHEMA_FIX_V2.ps1`, then execute only `RUN_C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_MUX_ONLY_V2.py` from the extracted kit. Exact PowerShell commands are in `README_INSTALL_AND_RUN.txt`. It still authorizes exactly two A/V test outputs and no more. The runner must repeat the full read-only source/media preflight; only then can it perform H.264/AAC stream-copy muxes. No prior failed attempt needs replaying. Upload its newly-created `GEOAVR2_*_EVIDENCE.zip` and `.sha256` for audit.

R1V remains OPEN / FAIL-CLOSED. No full acceptance, no human-review closure, no remaining 22 Loop grammars, no E4B closure, no E4C/E5/E6/E7/E8 admission. C11-C 2.19.12 remains immutable; renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.


---

# C11-E R1V Geometric Waves A/B Repeatability Investigation — V5
**Date:** 2026-11-08. **Disposition:** AVI and MP4 diagnostic pair PASS; historic R1V qualification remains OPEN / FAIL-CLOSED.

## Diagnostic evidence and stage outcome

Operator explicitly authorized exactly two diagnostic captures with AVI retention. Run `GWDIAG_192813_C56B9C` completed 2/2. Evidence ZIP SHA-256 `b76e1fb276d91c831f11bcba6069e751cab7afbc8248300b89c97843753b53d9`; receipt SHA-256 `56e95b8c16590126d4ab082d1519988bed6edac6f3bfbe06463e5178f5b375f2`; comparison JSON SHA-256 `eb533995f76617665040013933eea159b3c4c583787c029ae285d279652a3402`.

- AVI A/B: 690/690 exact frame hashes; equal PTS/DTS; file bytes 50,692,122; both SHA-256 `78be4ab46e7b04f3d7544e628c58e2d2f1d018e1ee7992e8db57bbd819ab6a1a`.
- MP4 A/B: 690/690 exact frame hashes; equal PTS/DTS; file bytes 13,728,044; both SHA-256 `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`.
- Authoring JSON A/B equal; SHA-256 `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`.
- 23/23 source pins were unchanged before/after; `override.cfg` remained absent. Both Godot capture slots exit 0.
- Stage classification: `BOTH_STAGES_EXACT_REPEATABLE_DIAGNOSTIC_DID_NOT_REPRODUCE_DIVERGENCE`. No tolerance/SSIM was used.

## Interpretation — bounded, not causal

The new MP4 pair is byte-identical to historic Geometric A, not to historic B. Historic B SHA remains `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`. Therefore this diagnostic establishes repeatability for this new two-run pair but does not explain the historical B outlier. It does not prove a systematic Movie Maker, FFmpeg, GPU, `fwidth()`, timing, or shader defect. No code change is justified. C11-C remains frozen.

Historic `Q5_040414_B6BE4D` is still fail-closed: Geometric 0/690 exact A/B pixels, though 690 frames/PTS, authoring JSON, WAV, AAC and seeds match; four other family A/B pairs are exact. The earlier spatial comparison had zero best alignment offset, SSIM 0.984889, PSNR average 35.61258 dB; footer luma MAE 3.770366166, header 1.754676188, body 0.719716678. These metrics describe the old pair only and are not causal evidence.

## Next controlled step

Run the read-only `C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_PREFLIGHT_V1.zip` (SHA-256 `efe7d2de99b0b2a7ab925a482b5a815d93516774bf65cfd1c471ad164ab31fda`). It verifies prior WAV/PCM/AAC/AV assets and the new exact diagnostic pair; no media is created. If it passes, a separate, explicitly authorized two-output A/V mux-only requalification can be designed using the new MP4 video and existing approved audio. No integrated wrapper, C11-C capture, audio generation, other family, or 52-test rerun.

R1V will not close until historical B divergence is resolved by evidence and all outstanding visual/layer and audio reviews pass. Remaining 22 Loop grammars stay blocked.


## Latest operator checkpoint — 2026-11-08: bounded mux-only requalification authorized, prepared, not executed

- Documentation V3 is installed PASS: 39/39 source pins, 11/11 documents, manifest SHA-256 `a899723f377780745299efcccceb3176212067e65ebe1ed10dc308f86d0a76d5`.
- The operator-uploaded receipt archive `r1v_geometric_av_reuse_preflight_ab_repeatability.zip` is 4,556 bytes, SHA-256 `12e4a9e1fd164cea9741260900049926be9e11b0d35072752b7c14cedb598b2e`; ZIP CRC is clean. It contains the reuse-preflight report, its SHA sidecar, and the V3 install receipt.
- Reuse preflight `GEOAVP_221712_C50A95`: `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`; report SHA-256 `fa8ecbcdefeca7299e983cb81d42326424cb1659bf6353190c3edec5eca80817`; 23/23 active source pins passed. No capture, media creation, music generation, mux, tests, or Git occurred.
- Historical WAV A/B, decoded PCM A/B and AAC elementary streams A/B are byte-identical: WAV SHA `dfe29efc0a3d945d55fbb7e278252d211abfb6f56deaaec3a292258e8b17d5ee`; PCM SHA `1f03e69f9546e52e3856b4228d4b6d4072f8af85abd2a67055d64c0058ec2a10`; AAC/ADTS SHA `ba3ad357b90de7af6d1a3df39470376e473611fed799003677dcc7de912aa51b`. Each WAV is 44.1 kHz, stereo, 16-bit PCM, 1,014,300 samples, 23 seconds.
- New diagnostic A/B source MP4s are byte-identical to each other and to historic Geometric A: SHA `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`. Their H.264 elementary stream SHA is `cb66b21fb92f74760406253c01b89a63c442ea217b73c868e9391f5258de9ac2`. Historic Geometric B remains the distinct outlier SHA `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`.
- The operator explicitly approved continuing with exactly two Geometric Waves A/V requalification outputs. The bounded runner in this package uses the new diagnostic MP4 A/B pair for video and the corresponding already-qualified historic A/B A/V files solely as AAC audio carriers. It performs `-c:v copy -c:a copy`; it does not encode AAC, alter H.264, generate WAV, capture, invoke Godot, run the integrated R1V wrapper, or repeat the 52 tests.
- Expected success status is `PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE`. It requires two outputs, H.264 preservation, exact AAC reuse, 690/690 decoded pixel hashes equal A/B, identical video PTS, conforming stream layout and A/V duration/start alignment, 23/23 protected source pins unchanged, and all source media unchanged.
- This is only a Geometric Waves technical replacement/requalification evidence pair. It does not erase the historic B anomaly's unknown cause, grant full R1V acceptance, complete human visual/layer or audio listening review, admit the remaining 22 Loop grammars, activate D rendering, or change `release_authority=NONE`.

## Execution contract for the approved two-slot mux

Run `RUN_C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_MUX_ONLY_V1.py` from the extracted kit folder with Python 3.13. The script revalidates all input and lineage pins before creating its unique evidence folder. It selects only the A/B diagnostic MP4s and each corresponding historic final A/V file as the audio carrier; it maps only `0:v:0` and `1:a:0`, stream-copies both, strips nonessential global/chapter metadata, and uses MP4 faststart. It does not use `-shortest`, audio encoding, resampling, scaling, filtering, or video encoding. It checks the AAC elementary-stream hash against the preflight-approved hash and checks source/final H.264 equality.

The runner decodes only the two new final outputs in memory to calculate 690 per-frame YUV420P SHA-256 hashes and a global pixel-stream hash; no frame files are written. It also inventories frame PTS. It preserves any partial output and fails closed if any slot or postcondition fails. Do not retry a failed run into the same evidence directory; inspect its report first.
