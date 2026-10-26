# C11-D continuity reconciliation overlay — V1 (2026-10-26)

Reference source snapshot: `ChallengeEngineV01_STATELESS_C11-D_20261026_013616.zip`
Reference ZIP SHA-256: `3e48ee2d815593137f5863139e05c1aa04eb40b4a58ddfb3bed4507125c96874`
Expected canonical frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

**Snapshot discrepancy:** the copy inside this ZIP hashes to `f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5` (`1070256` bytes); its self-entry declares `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (`796318` bytes). It is not accepted as canonical. Verify the live checkout manifest before applying; never copy the snapshot version over the canonical one.

This overlay has four exact-hash-guarded replacements for stable continuation pointers (`AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`, `docs/current/d/START_PROMPT_C11D_CURRENT.md`) and add-only versioned documents/receipt/schema/validator/prompts. Every replacement must be backed up before applying. Historical dated checkpoints and the 2026-10-23 V1 source-composition receipt/decision remain unchanged.

The current runtime evidence capture is deliberately marked `CAPTURED_OPERATOR_RUNTIME_PASS_PENDING_FORMAL_REVIEW`. The next gate begins by confirming the live frozen manifest SHA/size; the uploaded ZIP copy is not canonical. If the live check passes, validate the V2 receipt against the real Windows `%TEMP%` runtime logs, followed by a separate operator receipt review. The overlay does not authorize production wiring, renderer activation, media, payload materialization, render testing, baseline freeze, promotion or release.

Apply only to the active Windows checkout with the exact ZIP SHA, manifest and target preconditions. Do not extract the full repository snapshot over the checkout. Apply and test in separate operations.
