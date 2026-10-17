# C11-D context migration runbook — 2026-10-17 V1

## Start a new ChatGPT context

1. Open the repository context/snapshot file from the Library if needed, but treat the user's active Windows checkout as authoritative for current state.
2. Read `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261017_V7.md` first.
3. Read `docs/current/d/C11D_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_CLOSEOUT_CHECKPOINT_20261017_V1.md` and `docs/current/d/C11D_V2B_SEMANTIC_BINDING_REVIEW_AND_RUNTIME_GATE_PLAN_20261017_V1.md`.
4. Use `prompts/C11D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261017_V3.md` for the enduring project instructions.
5. Start the actual session with `prompts/C11D_FINAL_CLOSEOUT_START_PROMPT_20261017_V3.md`; use the V2B-specific start prompt when beginning only the next narrow work item.
6. Verify the actual tree, manifest hashes, and latest reports before treating document claims as current. Do not assume an extracted snapshot contains the operator's latest work.

## Current checkpoint

- Challenge visual payload capability matrix V1: 15/15 tests PASS; audit PASS (9 selectors, 43 source pins, 27 asset references, 15 unique assets, 9 custom-data inventories).
- Semantic binding proposal V1: 20/20 tests PASS; audit PASS; 9 secondary proposals; 6 candidate custom-data fields; 0 approved bindings.
- Current proposed work is a semantic review and acceptance-gate design, not yet materializer implementation.

## Required safeguards

- Never overwrite an add-only target with different contents. If a target name already exists, preserve it and create a new versioned filename or explicitly review a guarded replacement with a known previous hash and backup.
- Preflight every target before making the first change. A conflict anywhere must abort before any destination changes.
- Do not print PASS after a failed command or missing output. Capture native stdout/stderr and check real exit codes.
- Keep staging paths short under `%TEMP%` on Windows, and create parent directories explicitly when extracting ZIP entries.
- Use complete, paste-ready PowerShell 5.1 blocks; avoid `&&`, `$PSScriptRoot`, and detached `finally` fragments.
- Separate apply and test blocks. Do not rerun an already successful apply merely because a later test failed.

## Governance locks

C11-C remains frozen and immutable. Keep renderer OFF, media creation false, candidate input inadmissible, seed-domain completeness false, D4.8 blocked, D9.10 preparation-only, D9.17 blocked/no-go, D10 blocked for promotion, and release authority NONE until the formal gates and approvals are actually closed.
