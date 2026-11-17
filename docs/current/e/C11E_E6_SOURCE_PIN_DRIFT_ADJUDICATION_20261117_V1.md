# C11-E E6 — CHALLENGE_004 historical source-pin drift adjudication register

**Disposition:** `OPEN / HARD_BLOCKER / NO_AUTOMATIC_WAIVER`

The immutable E4A.7 receipt is `C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json`, SHA-256 `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`. It records source pins at its 2026-11-06 qualification time. The 2026-11-17 E6 reuse audit found two current source files whose bytes do not match those historical pins.

| Source path | Historical E4A.7 expected bytes / SHA-256 | Current audit-observed bytes / SHA-256 | State |
|---|---|---|---|
| `tools/c11d/d9/universal_editorial_model.py` | 26,574 / `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5` | 27,585 / `dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd` | `DRIFT_UNRECONCILED` |
| `c11c-suite/c11c-producer/c11e_production_service.py` | 32,885 / `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` | 86,687 / `e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87` | `DRIFT_UNRECONCILED` |

## Required read-only adjudication

1. Search the user's durable evidence and backup locations for exact files matching the two historical SHA-256 values and expected byte counts. Do not overwrite or restore them into the active checkout.
2. If exact preimages are found, preserve them as evidence, independently hash them, and perform a text/source diff against the current pinned files. Record the exact changed hunks and whether they touch E4A.7 request interpretation, editorial resolver semantics, D compositor inputs, output identity, or any E6 reuse predicate.
3. Compare the E4A.7 receipt's recorded intents, source identity, mux A/B/C output hashes and review evidence to the current E6 contract. An unrelated change still needs an explicit reasoned disposition; do not infer irrelevance from filename or line count.
4. If preimages cannot be recovered, or the change affects the qualification path, mark CHALLENGE_004 prior output `NOT_ELIGIBLE_FOR_E6_REUSE`. Do not mutate the historical receipt and do not regenerate CH004 until a separate E6 TEST_ONLY authorization and the D4.8 governance conflict are resolved.

## Forbidden shortcuts

- No update to old expected SHA values in E4A.7.
- No replacement of the historical receipt or output files.
- No `PASS` override, suppression or waiver based on operator intent alone.
- No Git/HEAD/status/branch inspection.
- No Godot, FFmpeg, FFprobe, audio, mux, render, dispatch, BatchId reservation or media creation.

This register remains open until source preimages and a reviewed disposition are recorded in a later versioned evidence overlay.
