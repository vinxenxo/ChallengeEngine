# C11-E E5 Execution Incident Register — V1 (2026-11-16)

This register is an append-only documentary record of E5 Loop C runner/recovery defects and their final disposition. It exists to prevent repeat execution loops. Preserve all original partial and failure evidence.

## Incident 1 — Loop C A/V V1 preflight contract

- Runner: `RUN_C11E_E5_LOOP_C_CHANGED_MUSIC_AV_V1.py`.
- Observed: `E5_LOOP_C_PREFLIGHT=BLOCKED_FAIL_CLOSED: KeyError: 'path'`.
- Cause: the verifier expected a `path` field in each source-pin object, while the source map had used paths as dictionary keys.
- Disposition: failed before audiovisual generation and before BatchId consumption. Do not rerun V1.

## Incident 2 — Loop C A/V V2 post-run scope error

- Run ID: `E5LC_20261116T203121Z_9C48A2`.
- Six V2 unit tests passed. Two deterministic native WAV files and the Loop C MP4 were produced.
- Observed: `FAIL_CLOSED_PARTIAL_EVIDENCE_RETAINED`, `NameError: name 'source_pre' is not defined`.
- Cause: post-run source-pin verification referenced `source_pre` outside the local scope of the pre-run verification function.
- Disposition: keep the generated WAV/MP4, progress file and original failure receipt. Never rerun or remux this run.

## Incident 3 — Recovery V1 ZIP member-root mismatch

- The recovery ZIP expanded successfully but contained an unexpected nested directory relative to the command path. Both named Python scripts were therefore absent at the expected extraction root.
- No recovery test or recovery runner executed; Python reported `[Errno 2] No such file or directory`.
- Disposition: do not infer a code failure or media change. Recovery V1 is unusable; retain as failed package evidence.

## Recovery V2 — PASS

- Recovery V2 extracted scripts at the package root and its seven contract tests passed.
- Status: `PASS_EXISTING_OUTPUT_VERIFIED_TEST_ONLY_OPERATOR_AV_REVIEW_REQUIRED`.
- H.264 is bitstream-identical to accepted Loop A; AAC differs from accepted Loop A; native music C is repeatable; FFprobe contract passes; source evidence pins 134/134 PASS.
- MP4 SHA-256: `2c14f825a1e00a19a9d27cffdffa854947dfb22da0c7fae089e3a0344a643c83`.
- Recovery receipt SHA-256: `86105f8cba04cf7ad5ed2516049c6b16845e95fe21d7940019b8046bb7c75f21`.
- `NEW_BATCH_ID_CONSUMED=false`; `MEDIA_REGENERATED=false`; no existing files deleted or overwritten.

## Human review disposition

After Recovery V2 passed, the operator explicitly approved Loop C video and audio, editorial line, music and layout. The approval applies to the retained MP4 identified by the SHA above. This closes the Loop C operator A/V review gate and E5's representative A/V review gate when combined with the accepted Challenge and Drill representatives. The original machine receipt is not rewritten; this register and `C11E_E5_CROSS_FAMILY_AV_CLOSEOUT_20261116_V1.md` record the later approval.

## Process correction

The next E5 action is not another media runner, installer, source capture or adapter implementation. It is the visible Qt Producer runtime acceptance described in `C11E_E5_QT_GUI_RUNTIME_ACCEPTANCE_20261116_V1.md`. Keep E1 PREPARE_ONLY and `family_adapter=NOT_CONNECTED_E1`. Once the three visible GUI request cases pass, close E5 and then start E6 Smoke18. Do not repeat E4 or E5 A/V.
