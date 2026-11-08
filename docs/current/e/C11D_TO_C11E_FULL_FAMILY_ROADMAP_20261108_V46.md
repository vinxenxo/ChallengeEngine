# C11-D to C11-E Full-Family Roadmap — V46
**Date:** 2026-11-08. Continue from accepted E4B mapping/R1P/Option C; do not rerun accepted phases.

## Outcome

One validated D+E production route across Challenge, Visual Loop and Visual Drill. Preserve C11-C visual mechanics/generators, family-specific binders/timelines and native music. Add D presentation/layout/editorial at the accepted family seams; orchestrate correct family audio, FFmpeg mux, FFprobe/audio QA, provenance, GUI/CLI parity and deterministic receipts.

## Current Loop checkpoint

- 5 families / 27 grammars mapped and R1P 27/27 parameter receipts accepted.
- Option C is operator-approved and its 27 D handoffs pass PREPARE_ONLY. D post-composition consumer is not yet implemented.
- Fractal Bloom A source capture exists and operator visual review passes. R1V active Windows 52/52 preflight and the 259-character path guard are accepted. The next A/V attempt stopped at FFmpeg 9 pixel decoding because the code used removed `-vsync 0`; no new family launch/audio/mux has yet started.
- Current next step is to install the FFmpeg 9 compatibility correction (`-fps_mode passthrough`) and run the integrated wrapper once. The five-family A/B pilot remains the gateway before the remaining 22 grammars.

## Ordered gates

1. R1V integrated A/V five-family qualification (10 outputs, nine new source launches + reuse Fractal A). Music is integrated per slot via C11-C FAMILY_MUSIC_V4 and R1P music_seed; no D3 V5 for Loop.
2. Human visual/layer review and audio listening for all ten outputs.
3. Qualify other 22 Loop grammars with family-native music and D presentation contracts.
4. Implement one generalized Option C D post-composition consumer consuming immutable C video; preserve all native C binders/timing/music and do not mutate C source files.
5. Complete E4C Drill preserving native Drill music and phase/END_CTA semantics.
6. E5 cross-family determinism, independent seed domains, no adapter/profile leakage, GUI/CLI parity.
7. E6 Smoke18 (six audiovisual cases per family).
8. E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill); CH_008/009 remain held until declared 11s vs 12s phase sum is resolved.
9. E8 full historical C-to-E regression, independent acceptance, immutable freeze and separate explicit promotion decision.

## Current package state

V1.1 A/V, lineage correction V2 and path-budget correction V2 are installed in the active Windows checkout. The integrated Windows wrapper passed 52/52 tests with zero skips/errors/failures. The compact path guard passed; the latest run reused accepted Fractal A and stopped before any new launcher/audio/mux because FFmpeg 9 removed `-vsync 0`. The FFmpeg 9 pixel-decode correction V1 is the current prepared package.

## Governance

R1V A/V approval is narrow test authority only. General D4.8 production renderer stays DISABLED; runtime authority NONE; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; release authority NONE. C11-C 2.19.12 and frozen manifest remain immutable.


## Latest R1V execution checkpoint (2026-11-08)

V1.1 (`PASS_ADD_ONLY_INSTALL`, 21/21) and V2 lineage correction (`PASS_PINNED_CODE_REPLACEMENT_AND_ADD_ONLY_DOCS`, 12/12) are installed locally. The Library V1.0 package was **not** installed and is not a prerequisite.

The first integrated wrapper run had one test_20 schema mismatch and stopped before capture. Lineage correction V2 installed; the subsequent wrapper `R1V_AV_WRAPPER_V1_20261108_003543_5D7E5320` passed 52/52 with zero skips/errors/failures. It then reused the accepted Fractal A and stopped before any new launcher/audio/mux because an FFprobe sidecar path exceeded Win32 MAX_PATH. The current blocker is the path-budget installer package pin defect; corrected installer package V2 is prepared. No silent recapture phase is inserted.

The ordered gates remain: (1) pass the integrated 52-test Windows preflight, (2) capture/reuse and mux all ten A/V outputs in one sequence, (3) human review of the ten videos/layers and ten tracks, (4) remaining 22 Loop grammars, (5) generalized Option C compositor, (6) E4B closure and E4C Drill, then E5 → Smoke18 → Matrix101 → E8. No later gate is inferred from this correction.


## Lineage-fix installer correction (2026-11-08)

The first lineage-fix package V1 failed complete preflight before any filesystem write: versioned successor document filenames were incorrectly marked as same-path PINNED_REPLACE. The installed predecessor documents remain V16/V42/V95/V56/V70/V93/Runbook V8/Master and Start V96/First V20. V2 classifies each successor document as ADD while verifying those ten installed predecessor paths/hashes. The validator source module remains the sole same-path PINNED_REPLACE. Do not run the V1 installer or manually stage docs.

The next operation is FFmpeg 9 pixel-decode correction V1 PowerShell install PASS, followed by the existing integrated wrapper once. The wrapper must report 52 tests, zero skips/errors/failures before any capture. The prior Fractal A, R1P and Option C remain accepted and are not repeated.


### R1V Windows path-budget defect — current active blocker

V2 lineage correction is installed and its 52-test active Windows suite passed. The first A/V slot reused Fractal A and stopped before any new launcher because an R1V FFprobe sidecar path exceeded the conservative Win32 MAX_PATH budget. R1V Windows path-budget implementation V1 with corrected installer package V2 adds 16-character run IDs and a preflight guard (<=259 characters); the actual maximum planned path is 257. Do not rerun prior accepted stages.


## Current R1V corrective package checkpoint

The path-budget implementation V2 is installed and its receipt is pinned. The current active blocker is FFmpeg 9 compatibility in the in-memory pixel decoder: legacy `-vsync 0` is no longer accepted. Install the FFmpeg 9 pixel-decode fix V1 and run the integrated wrapper once.


## Latest Windows R1V execution — FFmpeg 9 decode compatibility (2026-11-08)

- Path-budget correction V2 installed PASS: 13/13 payloads; install receipt SHA `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`.
- Active Windows integrated wrapper `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF` passed 52/52, zero skips/errors/failures; wrapper receipt SHA `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V preflight passed with the compact run ID and 257-character max path. It reused the accepted Fractal Bloom A MP4; FFprobe found 660 frames at 720x1280/30 and 22 seconds.
- Run `Q5_022257_316922` failed closed in the in-memory pixel decoder because the host is FFmpeg 9.0 and the code still supplied removed `-vsync 0`. Decoder stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`.
- No new launcher, music generation, mux or A/V output was started/completed (0/0/0/0). The source MP4 remains pinned/unchanged. Full incident record: `C11E_R1V_FFMPEG9_PIXEL_DECODE_COMPATIBILITY_CORRECTION_20261108_V1.md`.
- Corrective code V1 replaces only `-vsync 0` with `-fps_mode passthrough`, retains rawvideo pipe-to-memory and exact frame hashing, and extends the existing test_04 without changing the combined 52-test count. Error diagnostics now include FFmpeg stderr and decoded/expected frame counts.
- Next step: install the FFmpeg9 pixel-decode fix V1 after exact receipt/evidence/predecessor preflight, then run the same integrated wrapper once. Do not repeat accepted 52-test work manually, R1P, Option C, or Fractal A. No separate silent-only stage.


## E phase order remains unchanged

R1V audiovisual pilot (five representative families, A/B) → operator visual/layer/audio review → remaining 22 Loop grammars → generalized Option C D post-composition consumer → E4B closure → E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8 independent acceptance/freeze/promotion decision. CH_008/CH_009 remain held pending the 11-second declared duration versus 12-second phase-sum reconciliation.

## Latest operator execution checkpoint (supersedes prior live next-step statements) — 2026-11-08 (authoritative; supersedes prior next-step text)

- Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. V1.1 A/V overlay PASS 21/21; lineage correction V2 PASS 12/12; path-budget correction V2 PASS 13/13. Latest path-budget install receipt SHA-256: `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`. Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Active Windows wrapper `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF` passed the combined gate: 52/52, zero skips, errors or failures. Receipt SHA-256: `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V run `Q5_022257_316922` passed preflight, reused the accepted Fractal Bloom A, then failed closed during in-memory pixel decoding. Report SHA-256 `67759765d0c4d55737b3480d1d54f56e9b878dde75f2e462225bbc57f5412a70`; process receipt SHA-256 `f904e08edac76d07f5324b88937c71b0104ea1db18201d12154e6ec7df4ec74b`.
- Exact FFmpeg 9.0 stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`. No new C11-C launcher, WAV generation, AAC mux or completed A/V output occurred. The existing Fractal A source and its MP4 hash remain unchanged.
- Root cause: FFmpeg 9 removed legacy `-vsync`; the compatible per-output video sync option is `-fps_mode passthrough`. The correction preserves in-memory rawvideo pipe decoding, 660-frame identity accounting, and the no-frame-files policy. A local FFmpeg 7.1.5 reproduction returned all 660 frames / 912,384,000 bytes; Windows FFmpeg 9 confirmation remains pending.
- **Current next action:** install `C11E_R1V_FFMPEG9_PIXEL_DECODE_FIX_V1_20261108.zip` from a fresh Downloads folder, then run the existing integrated wrapper once. Do not reinstall V1.1, lineage V2 or path-budget V2; do not rerun R1P, Option C or Fractal A.
- No silent-only intermediate stage. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.

