## Latest authoritative checkpoint — 2026-11-08 (V6; supersedes older pending-state wording)

## Latest authoritative checkpoint — 2026-11-08: Geometric Waves replacement technically qualified; human-review ledger updated

The operator installed V5 successfully (`PASS_ADD_ONLY_DOCUMENTATION_OVERLAY_V5`, 65/65 source pins, 11/11 files). The corrected mux-only runner V2 completed `GEOAVR2_224356_841F9B` and returned `PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE`.

### Audited GEOAVR2 evidence

- Evidence ZIP: `GEOAVR2_224356_841F9B_EVIDENCE.zip`; SHA-256 `721e33202cad7a0885cf7de72ba3dac0a26f92bca296677dd7702d3f77b7933f`; 28,680,809 bytes; 22 entries; CRC clean.
- Report: `GEO_AV_REUSE_MUX_REPORT_V1.json`; SHA-256 `15712f3187237f118df05c0c013558c65b2a2f7d342a0e765da8307e7a7ff037`.
- Two outputs A/B, each 14,298,259 bytes, same complete MP4 SHA-256 `a3c5d820fbed7be5392f1b5514b4bbc8437c0de50d2c0e22b63204ea4233a0ce`.
- 720×1280, H.264 High, yuvj420p source, 30 fps, 690 frames, 23.000 seconds; AAC-LC, 44.1 kHz, stereo, 23.000 seconds; A/V duration delta 0.000 seconds and start offset 0.
- Video and audio were copied as elementary streams, not re-encoded. H.264 stream SHA `cb66b21fb92f74760406253c01b89a63c442ea217b73c868e9391f5258de9ac2`; AAC stream SHA `ba3ad357b90de7af6d1a3df39470376e473611fed799003677dcc7de912aa51b`.
- Frame checks: 690/690 A/B decoded frame hashes match; video PTS equal; H.264 preserved 2/2; AAC reused exactly 2/2; decoded global pixel stream and complete MP4 file hashes equal.
- Source pins 23/23 before and after; 21 input files unchanged; no capture, music generation, integrated wrapper or tests invoked; C11-C source not modified.

### Historical Geometric B anomaly disposition

The original `Q5_040414_B6BE4D` report remains immutable `FAIL_R1V_AV_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED` (report SHA `85de2645621acd6f8183508e0da9b5466b8a00cf9d2cb340a170f7d2803285ba`; process receipt SHA `8820d36ffd6c1969eb4e148fe640f08f4324a243fe49ca1e43299e6db1201d26`). Its original Geometric B source hash was `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`, different from A (`b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`). The new AVI diagnostic A/B outputs were byte-identical (AVI SHA `78be4ab46e7b04f3d7544e628c58e2d2f1d018e1ee7992e8db57bbd819ab6a1a`) and MP4 A/B outputs were byte-identical to the historic A MP4 (`b7b841...249eca`). The new mux-only A/B replacement reuses the corresponding historical A/B AAC carriers, and the AAC streams are byte-identical.

Disposition: the historic B outlier is **superseded for the R1V qualification artifact set** by the new exact A/B replacement pair. Its underlying one-off cause remains `UNKNOWN / NOT ATTRIBUTED`; do not claim a root cause or patch C11-C. Keep the original fail report as immutable historical evidence. This is a reconciliation of qualification outputs, not a rewrite of the old report or a rerun of the integrated wrapper.

### Human review recorded from operator statement

The operator explicitly confirmed that the new Geometric Waves A/B videos were reviewed and render correctly, including presentation/layout/editorial layers and music. Record the two new Geometric slots as `OPERATOR_CONFIRMED_AV_PASS` (visual + music review).

Previously accepted Fractal Bloom A visual review remains PASS. All other reviews remain outstanding:

- Visual/layer review pending: Fractal Bloom B; Invisible Forces A/B; Living Particles A/B; Sacred Symmetry A/B (7 slots).
- Audio/music listening pending: Fractal Bloom A/B; Invisible Forces A/B; Living Particles A/B; Sacred Symmetry A/B (8 slots).

Do not infer that the operator's Geometric review covers the other four families. Do not repeat the already-confirmed Geometric A/B review or Fractal Bloom A visual review.

### Current phase disposition and next action

`R1V_GEOMETRIC_WAVES_TECHNICAL_SUBGATE=PASS`; `R1V_GEOMETRIC_WAVES_OPERATOR_AV_REVIEW=PASS`; `R1V_FIVE_FAMILY_TECHNICAL_EVIDENCE=RECONCILED_PASS_WITH_GW_REPLACEMENT`; `R1V_FULL_PHASE=OPEN_PENDING_HUMAN_REVIEW`.

No further rendering, capture, mux, music generation, full wrapper, 52-test suite, R1P, Option C or accepted family-pair execution is authorized or needed for this human-review subphase. Finish the 7 visual/layer and 8 audio reviews using the existing A/V outputs. After that, record the human register and close R1V. Only then admit the remaining 22 Loop grammars and return to the E roadmap in order.

C11-C 2.19.12 remains immutable; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; Git checks skipped and commits operator-managed.


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

# C11-E R1V Five-Family A/V Qualification Runbook — V18
**Current run:** `Q5_040414_B6BE4D`. **State:** OPEN / FAIL-CLOSED on Geometric Waves exact-pixel repeatability.

## Accepted execution — do not repeat

- Integrated Windows wrapper tests: 52/52 PASS, zero skips/errors/failures.
- A/V sequence: 10 outputs, 10 source inventories, 10 family-native WAV generations, 10 AAC muxes, nine new C11-C launches plus one accepted Fractal A source reuse.
- Four selector A/B pairs are pixel-identical. Geometric Waves `harmonic_membrane` remains 0/690 exact matches despite 690 frames and PTS matching; authoring JSON and WAV/AAC are identical.
- Do not repeat the 52-test wrapper, other four family pairs, Fractal A, music generation, R1P, Option C or prior accepted captures unless a concrete regression/dependency change exists.

## Existing-source forensic result — read-only

The operator-provided `geometric_waves.zip` SHA is `b40ba2ddab6518c456ee822acd22a8fee2f143dcfb98c541b2f6049bdb6cc86e`. The A/B MP4 source hashes are A `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`; B `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`. Both decode to 690 frames / 720×1280 / 30fps with equal PTS. Read-only regional luma MAE: Header 1.754676188; Body 0.719716678; Footer 3.770366166. Best spatial translation for all three bands is 0,0. The Footer is the strongest region, but it is not proven as the cause. Forensic report SHA `aa0eac36e41057520fad0156f42862315aaf536b542ab2df77192ebd6f7192a4`.

The ZIP has no AVI intermediate. Therefore stage attribution (Movie Maker AVI vs FFmpeg conversion) remains unresolved. `fwidth()` remains a shader hypothesis only.

## Prepared bounded next diagnostic — NOT AUTHORIZED YET

Kit: `C11E_GEOMETRIC_WAVES_AVI_INTERMEDIATE_DIAGNOSTIC_V1.zip`, SHA-256 `86f18fc6de5706d99a9383b10ac23422916ad87d6bde8d1efacc33b12da6406e`. It is a no-install, two-slot A/B diagnostic only:

- Selector `c11c_geometric_waves_v1`, grammar `harmonic_membrane`, gameplay seed 100001, duration 23 s, 720×1280@30, expected 690 frames.
- Uses the existing pinned C11-C launcher exactly twice, A then B, with `-NoSound -KeepAvi` into two new empty per-run folders.
- Preserves AVI and MP4; hashes decoded frames per stage with FFmpeg `framehash`; records FFprobe metadata and the source/override restoration receipts.
- It does not run the integrated R1V wrapper or 52 tests, music, AAC mux, other families, Fractal A, R1P, Option C, or any source patch. It does not modify C11-C files.
- 23 source SHA-256 pins are checked before and after. Unknown `override.cfg` bytes are never overwritten.

**Do not run this kit until the operator explicitly approves this bounded two-capture diagnostic.** The previous V1 investigation expressly reserved AVI-retaining capture for a separate approval. This package is prepared, not authorized or executed.

After approval, extract to a fresh Downloads folder (never checkout) and run the script once from PowerShell 5.1:

```powershell
$Kit = "$env:USERPROFILE\Downloads\C11E_GEOMETRIC_WAVES_AVI_INTERMEDIATE_DIAGNOSTIC_V1"
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11E_GEOMETRIC_WAVES_AVI_INTERMEDIATE_DIAGNOSTIC_V1.zip" -DestinationPath $Kit
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "$Kit\RUN_C11E_GEOMETRIC_WAVES_AVI_INTERMEDIATE_DIAGNOSTIC_V1.ps1" `
  -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
```

Expected diagnostic marker is `PASS_DIAGNOSTIC_PAIR_CAPTURED_NOT_R1V_ACCEPTANCE`, not an R1V PASS. Upload the resulting `*_EVIDENCE.zip` and `.sha256`. Do not re-run it if the evidence already exists.

## Decision logic

- AVI A/B exact, MP4 A/B non-exact: first divergence is after AVI, in conversion/packaging/metadata handling.
- AVI A/B non-exact: divergence already present at the Movie Maker AVI output boundary; do not claim GPU root cause without further proof.
- AVI and MP4 both exact: old mismatch not reproduced; historical R1V remains fail-closed pending a separately justified resolution.
- Any other outcome: report exact framehash and PTS differences; never weaken exact pixel acceptance.

## Closure / roadmap

R1V closes only when all five family A/B pairs are exact, ten A/V technical QA records are valid, and the outstanding operator visual/layer and audio listening reviews are complete. Then proceed to remaining 22 Loop grammars → generalized Option C D post-composition consumer → E4B closeout → E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8. CH_008/CH_009 remain held for 11s/12s mismatch.

## Governance

C11-C 2.19.12 and frozen manifest unchanged (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No Git checks; operator commits.


## V3 authoritative status update — 2026-11-08

This section supersedes any earlier statement in this document that the AVI-retaining diagnostic was pending, prepared, or not authorized. The operator installed documentation overlay V2 successfully (11/11 ADD files; install manifest SHA-256 `1b4c36ee2ed9d6ce8e7604cba585247d2cbabd4370b86ac9b662b488c802dd32`) and explicitly authorized exactly two Geometric Waves A/B captures with `-KeepAvi`. Those two captures are complete and independently audited.

**Diagnostic disposition:** `PASS_DIAGNOSTIC_NOT_REPRODUCED`. Run `GWDIAG_192813_C56B9C`; evidence ZIP SHA-256 `b76e1fb276d91c831f11bcba6069e751cab7afbc8248300b89c97843753b53d9`; diagnostic receipt SHA-256 `56e95b8c16590126d4ab082d1519988bed6edac6f3bfbe06463e5178f5b375f2`; AVI/MP4 stage-comparison JSON SHA-256 `eb533995f76617665040013933eea159b3c4c583787c029ae285d279652a3402`. Both slots exited 0. The A and B AVI files are byte-identical (50,692,122 bytes; SHA-256 `78be4ab46e7b04f3d7544e628c58e2d2f1d018e1ee7992e8db57bbd819ab6a1a`); the A and B MP4 files are byte-identical (13,728,044 bytes; SHA-256 `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`). Each stage has 690/690 exact framehash matches and equal PTS/DTS. The authoring JSON for A/B is identical (SHA-256 `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`). All 23 source pins matched before/after; `override.cfg` was absent before and after. No tests, full R1V wrapper, music generator, Git, or source modification occurred in this diagnostic.

**Critical distinction:** the new pair reproduces the historic R1V Geometric A source MP4 exactly, but does not explain or erase the historic B outlier (`a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`). Historical run `Q5_040414_B6BE4D` remains `FAIL_R1V_AV_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED`, with 0/690 exact Geometric A/B frame matches. The diagnostic proves that the two newly captured runs are repeatable at both AVI and MP4 stages; it does **not** establish the cause of the earlier B divergence or prove the pipeline is universally deterministic. Do not attribute the old event to Movie Maker, FFmpeg, GPU, `fwidth()`, timing, or any other component without new evidence. Do not relax pixel-hash acceptance and do not patch C11-C.

**Current R1V remains OPEN / FAIL-CLOSED.** Four other family A/B pairs remain accepted; do not repeat them. Do not repeat the 52/52 integrated test gate, R1P, Option C, or Fractal Bloom A absent a real dependency regression. Visual operator review is still only confirmed for Fractal Bloom A; all other required visual/layer slots are pending. All ten audio listening reviews remain pending.

**Next bounded action:** run the separate read-only kit `C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_PREFLIGHT_V1.zip` (SHA-256 `efe7d2de99b0b2a7ab925a482b5a815d93516774bf65cfd1c471ad164ab31fda`). It verifies the existing historical source MP4s, WAV/PCM/AAC outputs, final mux streams, new AVI/MP4 pair, historic reports/receipts, and 23 active source pins. It invokes FFmpeg/FFprobe only to probe and hash existing streams in memory and writes one JSON report plus SHA sidecar. It does **not** render, capture, generate music, mux, or alter source/media files. Expected marker: `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`. On any mismatch, stop fail-closed.

Only after that preflight passes, prepare a separate exact-scope two-output Geometric Waves mux-only requalification using the new identical MP4 A/B videos and reuse of the already-validated identical AAC audio streams from the historic A/V outputs. That future action is not part of the preflight and has not been authorized or executed here. It must not invoke C11-C capture, the music generator, the integrated five-family runner, the other four families, or the 52-test suite. Require separate explicit authorization before media mux. R1V acceptance remains withheld until the historical B discrepancy is formally resolved by evidence and the ten visual/layer plus ten audio listening reviews are complete.

Governance remains unchanged: C11-C 2.19.12 immutable; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; Git checks skipped and commits operator-managed. Remaining 22 Loop grammars and every downstream phase remain blocked pending R1V closeout.


## V4 update — operator-authorized two-output Geometric Waves A/V requalification

## Latest operator checkpoint — 2026-11-08: bounded mux-only requalification authorized, prepared, not executed

- Documentation V3 is installed PASS: 39/39 source pins, 11/11 documents, manifest SHA-256 `a899723f377780745299efcccceb3176212067e65ebe1ed10dc308f86d0a76d5`.
- The operator-uploaded receipt archive `r1v_geometric_av_reuse_preflight_ab_repeatability.zip` is 4,556 bytes, SHA-256 `12e4a9e1fd164cea9741260900049926be9e11b0d35072752b7c14cedb598b2e`; ZIP CRC is clean. It contains the reuse-preflight report, its SHA sidecar, and the V3 install receipt.
- Reuse preflight `GEOAVP_221712_C50A95`: `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`; report SHA-256 `fa8ecbcdefeca7299e983cb81d42326424cb1659bf6353190c3edec5eca80817`; 23/23 active source pins passed. No capture, media creation, music generation, mux, tests, or Git occurred.
- Historical WAV A/B, decoded PCM A/B and AAC elementary streams A/B are byte-identical: WAV SHA `dfe29efc0a3d945d55fbb7e278252d211abfb6f56deaaec3a292258e8b17d5ee`; PCM SHA `1f03e69f9546e52e3856b4228d4b6d4072f8af85abd2a67055d64c0058ec2a10`; AAC/ADTS SHA `ba3ad357b90de7af6d1a3df39470376e473611fed799003677dcc7de912aa51b`. Each WAV is 44.1 kHz, stereo, 16-bit PCM, 1,014,300 samples, 23 seconds.
- New diagnostic A/B source MP4s are byte-identical to each other and to historic Geometric A: SHA `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`. Their H.264 elementary stream SHA is `cb66b21fb92f74760406253c01b89a63c442ea217b73c868e9391f5258de9ac2`. Historic Geometric B remains the distinct outlier SHA `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`.
- The operator explicitly approved continuing with exactly two Geometric Waves A/V requalification outputs. The bounded runner in this package uses the new diagnostic MP4 A/B pair for video and the corresponding already-qualified historic A/B A/V files solely as AAC audio carriers. It performs `-c:v copy -c:a copy`; it does not encode AAC, alter H.264, generate WAV, capture, invoke Godot, run the integrated R1V wrapper, or repeat the 52 tests.
- Expected success status is `PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE`. It requires two outputs, H.264 preservation, exact AAC reuse, 690/690 decoded pixel hashes equal A/B, identical video PTS, conforming stream layout and A/V duration/start alignment, 23/23 protected source pins unchanged, and all source media unchanged.
- This is only a Geometric Waves technical replacement/requalification evidence pair. It does not erase the historic B anomaly's unknown cause, grant full R1V acceptance, complete human visual/layer or audio listening review, admit the remaining 22 Loop grammars, activate D rendering, or change `release_authority=NONE`.

### Run

Extract the package into a fresh Downloads folder (never into the checkout), install the docs, then run:

```powershell
$Kit = "$env:USERPROFILE\Downloads\C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_MUX_ONLY_V1_20261108"
py -3.13 "$Kit\RUN_C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_MUX_ONLY_V1.py" `
  --project-root "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
```

No other command is part of this step. The runner performs a complete preflight before creating its evidence directory. It requires the exact historical report/receipt, the AVI diagnostic evidence, the operator preflight report+sidecar, the V3 install receipt, 23 live source pins, exact MP4/AVI/authoring hashes, historic WAV/PCM/AAC hashes, and FFmpeg/FFprobe 9.0. Any mismatch stops before output creation.

### Expected pass and interpretation

Expected: `PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE`, `MUX_OUTPUTS=2/2`, `VIDEO_FRAME_HASH_MATCHES=690/690`, `H264_STREAM_PRESERVED=2/2`, `AAC_STREAM_REUSED_EXACT=2/2`, `SOURCE_PINS_BEFORE_AFTER=23/23`, `INPUT_MEDIA_UNCHANGED=True`. The runner creates only `A/GW_A_AV.mp4` and `B/GW_B_AV.mp4`, plus QA/evidence. It uses `-c:v copy -c:a copy`; audio is not re-encoded.

Upload the run's `*_EVIDENCE.zip` and `.sha256`. A technical PASS qualifies this new Geometric A/B pair only. It does not claim the original historic B cause is known, does not complete listening/visual review, and does not close R1V. If failed, preserve partial files and report; do not repeat without reviewing the failure.
