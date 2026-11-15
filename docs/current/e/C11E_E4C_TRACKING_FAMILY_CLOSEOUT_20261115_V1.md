# E4C Tracking family batch closeout — 2026-11-15

## Tracking family final status — no change (2026-11-15)

`tracking/tier-1..tier-5` remains accepted 5/5. The subsequent Pursuit overlay V1 installer incident does not alter, reopen or invalidate the tracking family. Tracking batch V4, its four individual receipts/media hashes and the operator's A/V acceptance remain immutable evidence. Global E4C is still 5/20. Pursuit V1 failed before its own ADD_ONLY transaction and is handled separately by Pursuit overlay V2.


## Disposition

- Tracking family subtotal: **5/5 accepted** (`tracking/tier-1` through `tracking/tier-5`).
- E4C global matrix: **5/20 accepted**; the pursuit, saccade and peripheral_scan families remain pending (15 selectors).
- Batch: `E4C-TRACKING-T2-5-20261115T074835Z-6239dd21`.
- Batch technical status: `PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW` in the coordinator result; the operator's explicit visual/audio approval supplied on 2026-11-15 closes the four human-review rows.
- Installation: V4 `C11E_E4C_TRACKING_BATCH_RUNNER_V4_INSTALL_20261115T074834Z_7f33f450`, `PASS_PINNED_REPLACEMENTS_AND_ADD_ONLY_DOCS`; independent audit PASS in preceding handoff.

## Evidence archive and completeness

- Evidence ZIP: `E4C-TRK-T2-T3-T4-T5-66239dd21.zip`.
- Size: 73,518,230 bytes; SHA-256: `a96fd5f7f83e51dfc667dcdc79fbf8afda3461c107fa3a78870cce1a847084c5`.
- Archive inventory: 176 entries; ZIP CRC validation PASS; four selector trees, 44 entries each.
- The archive contains the full selector-level request/E1 intent/E1 validation/D plan/D receipt/A-V qualification receipt/family-music receipt/FFprobe summaries/native capture evidence and final A/C MP4 and A/B/C WAV media.
- The archive does **not** contain the aggregate `BATCH_RESULT.json`, four outer `CLI_EXECUTION_RESULT.json` files, or outer batch stdout/stderr files. Their status, paths and declared SHA-256 values were supplied in the operator's full PowerShell console transcript. Those CLI-summary hashes are therefore recorded as console-declared rather than independently rehashed from this ZIP.
- Separate small ZIP `e4c_tracking_tier_batch.zip` (4,781 bytes; SHA-256 `9f0002393020a24972094a826cb365fe6e18e3d6b32d331d90a0a859d1710e8c`) is the **old consumed failure** ending `a78c6c24`; it contains the old lock, authorization marker, request, progress, failure receipt and logs. Preserve it. Never retry or reuse that BatchId.

## Per-selector receipt and media hashes

| Selector | Request ID | Qualification receipt SHA-256 | Final A MP4 SHA-256 | Final C MP4 SHA-256 |
|---|---|---|---|---|
| tracking/tier-2 | `E4C-TRK-T2-6239dd21` | `f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7` | `7373f3644f130296a55a70a1f6f25e3763cee4966ba83cfc5763b4e71a1a3365` | `03dea7c193aae61a4cc33d62a4abac74920b64b206ba4c931652ed0cb218959d` |
| tracking/tier-3 | `E4C-TRK-T3-6239dd21` | `9f84ef692c67d4cfab8d25f7dd61d986ae1d24d1c2a86de78750471d502fa5e6` | `24f1c630a961842a5c6d61ebc75a4e8ddd2ce2ce25e0066e77548a9d7bcd0f6f` | `7ae74a20e614b5a49b1c5a50e3b8470a7447e8134d3df2e31e572a84d449aec6` |
| tracking/tier-4 | `E4C-TRK-T4-6239dd21` | `e45ffd2e63eb9e7d0016ab30f5b0edd1ae6e6819981cb2c9e861d900875f17dc` | `8768bbe296ddd5251681dd371cd37f5c75ad568d18a16374715e07a31ffdb027` | `1801bef3b2556b8583afe61b272e4a5f769ca063db4e7b4b757a49d7757677f5` |
| tracking/tier-5 | `E4C-TRK-T5-6239dd21` | `6e55dc3fd4fc13745347cc641d29103fbfb7fa90dee932910f920703690c3c61` | `f2097c8380d75cf4af86e016b0b75100f7e24b6a350c7ff3d249ae3f39f33d72` | `0b22f1e88dabc6176b59aea54d2ea913f699252d33fa3363e26ab4f7ac585a1c` |

All four physical A/C MP4 SHA-256 values and A/B/C WAV SHA-256 values recalculated from the evidence ZIP match the hashes in their full qualification receipts and the supplied aggregate console output. The MP4 byte counts also match the archive entries.

## Technical assertions verified from every full receipt

- `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION` on all four.
- E1 `PASS_E1_PREPARATION_ONLY`, `valid=true`, renderer/media creation false at E1 preparation; shared GUI/CLI semantic parity PASS; `family_adapter=NOT_CONNECTED_E1`.
- 810 frames, 30 fps, 27.0 seconds; D phase counts exactly PRE_ROLL 90 / GAME 630 / END_CTA 90.
- All three editorial fields present; family titles are selector-specific `SEGUIMIENTO VISUAL · NIVEL 2..5`.
- Family music profile `FLOWING_VECTOR`; seed A/B 840001 identical; C 840002 distinct. A/B WAV SHA-256 `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277`; C WAV SHA-256 `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40`.
- A/C video elementary streams identical per selector; AAC elementary streams A/C differ. Final A/C MP4s each contain exactly H.264 High 720x1280 yuv420p TV 30/1 fps and AAC-LC 48kHz stereo, 27 seconds, with A/V start delta 0.000 seconds.
- All 91 source pins are identical across pre-execution, immediately-pre-renderer and post-execution checkpoints for each selector; the four 91-row inventories are equal.
- Frozen C11-C manifest unchanged: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; no C11-C source mutation; dispatch false; release authority NONE.

## Operator audiovisual acceptance

On 2026-11-15 the operator explicitly approved T2–T5 after review: videos render correctly, sound is correct, editorial fields inherit correct styles, layout is correct and runtime behavior is as expected. This approval moves the four selectors to `OPERATOR_ACCEPTED`.

## Non-blocking shutdown warnings

Each native `godot_stderr.log` records two shutdown warnings: one leaked `CanvasItem` RID and one leaked `ObjectDB` instance. No `ERROR` or `SCRIPT ERROR` appears; the native stdout confirms recording completion at 810 frames; each full qualification receipt, physical media hash, bitstream isolation and FFprobe contract passes. These warnings are retained as a non-blocking quality/investigation note, not suppressed and not treated as a capture failure. Revisit if they recur outside the same clean-completion conditions or escalate.

## Governance and next step

- `PRODUCTION_DISPATCH=FALSE`; `RELEASE_AUTHORITY=NONE`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`.
- `GIT_CHECKS=SKIPPED`; commits operator-managed.
- The next scoped family is pursuit tiers 1–5 with expected family music profile `ORGANIC_BLOOM`. It must use its own family-bound coordinator and editorial contract; the tracking-only runner must not be reused for pursuit.
- E4C remains open at 5/20. Saccade (profile `CIRCUIT_PULSE`) and peripheral_scan (profile `ORBITAL_RITUAL`) remain pending after pursuit. E5 starts only after E4C reaches 20/20.
