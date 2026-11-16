# C11E_E4C_PURSUIT_FAMILY_CLOSEOUT_20261116_V1

## Family closeout — accepted 5/5 — 2026-11-16

### Disposition

**Pursuit is ACCEPTED 5/5.** All five tiers passed technical qualification, and the operator explicitly approved layout, editorial, music and execution after viewing the generated results.

### Batch identity and execution

- Batch: `E4C-PURSUIT-T2-5-20261115T231337Z-3fc2161e`
- Coverage: 5/5 (`pursuit/tier-1..tier-5`)
- T1: existing qualified output reused and audited; no rerender.
- T2–T5: each executed once; process exit 0 and `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.
- Overall technical summary: `PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW` was the machine-written pre-review state. The operator's subsequent explicit approval supersedes that pending status for current acceptance.
- Technical acceptance: five of five.
- Operator review: five of five approved.

### Native and composition contract

Pursuit gameplay is 17.0 seconds /510 frames at 30fps. D composition phases: PRE_ROLL 90 + GAME 510 + END_CTA 90 = 690 frames /23.0 seconds. Canonical SHA-256 `dfe2bce9913df8ebe4f92d06eec5d22736338214e71b497dde3562a6927600bc`. Music profile `ORGANIC_BLOOM`.

### Evidence and traceability

The batch evidence ZIP `E4C-PURSUIT-T2-5-20261115T231337Z-3fc2161e.zip` includes batch result, lock, progress, execution authorization, per-row request JSON, CLI summaries and stdout/stderr logs. The BATCH_RESULT records final A/C paths and hashes, per-row qualification receipt path/SHA, music A/B/C hashes, native timing and source snapshot hashes. The evidence ZIP does not contain the MP4/WAV bytes or full per-row qualification receipt JSON; these remain at the exact paths in the operator's active checkout. The operator viewed and approved the media. Do not claim the ZIP itself embeds those media files.

- Source pin count: 35; pre/post equality true.
- Per-row source snapshot SHA-256: `e4d883e63852a471a4a22cce855596943f999147087857765cf1effcff78d550`.
- A/B music SHA-256: `52f6659de16f3508d40b9add5c8073ce1f5ceef7295bb4e7399f28f4a6fc00ba`.
- C changed music SHA-256: `49bb1449469441816a47737c402b23135a21107f8d328d24411fed1a3955a662`.
- C11-C frozen manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

### Governance

`production_dispatch=false`, `release_authority=NONE`, E1 `PREPARE_ONLY`, family adapter `NOT_CONNECTED_E1`, C11-C source mutation false, Git checks skipped and commits operator-managed. This family closeout is test qualification only and does not authorize production release.

### E4C matrix after Pursuit

Tracking 5/5 accepted; Pursuit 5/5 accepted; Saccade 0/5; Peripheral Scan 0/5. E4C total 10/20. Next family: Saccade (`CIRCUIT_PULSE`). E4C remains open until 20/20.
