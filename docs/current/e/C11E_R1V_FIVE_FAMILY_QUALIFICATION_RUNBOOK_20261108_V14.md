# C11-E R1V Five-Family A/V Qualification Runbook — V14
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
