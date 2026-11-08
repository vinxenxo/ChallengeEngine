# C11-E R1V Five-Family A/V Qualification Runbook — V15
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
