# C11-E E6 CH004 historical source-pin adjudication — V2

**Date:** 2026-11-18  
**Status:** `READ_ONLY_AUDIT_OVERLAY_PREPARED / ACTIVE_CHECKOUT_EXECUTION_PENDING`

## Current accepted point

`C11E_E6_D9_PIN_RECONCILIATION_V2` has completed successfully in the active Windows checkout. Operator receipt `E6D9PINREC_20261118T094345Z_2B9358D1` has report SHA-256 `0e2c977f1122d9cfc69da255d8fa539720a23f00cdc2f4c030d48bd01019a59a` and confirms:

- V2 focused repair tests: 13/13 PASS.
- Fixed evidence/sidecar pins: 13/13.
- Accepted active source pins: 33/33.
- Additional route dependencies: 9/9.
- Observed current CH004 hashes: 2/2.
- Reconciliation failures: 0.
- Checkout source files modified: false; media/Godot/FFmpeg/FFprobe/audio/mux/BatchId false; release authority NONE.

The earlier D9 plan V1 and its report remain immutable. The newer reconciliation receipt supersedes the stale nine-dependency finding only as a current verified dependency fact; it does not rewrite historical output.

## Historical source-pin issue

The E4A.7 CH004 receipt (SHA-256 `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`) pins:

| Source | E4A.7 historical preimage | Current source |
|---|---|---|
| `tools/c11d/d9/universal_editorial_model.py` | 26,574 bytes / `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5` | 27,585 bytes / `dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd` |
| `c11c-suite/c11c-producer/c11e_production_service.py` | 32,885 bytes / `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` | 86,687 bytes / `e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87` |

E4B V2's immutable source patch manifest maps those exact preimages to later postimages. E4B V3's recovery receipt maps the preimages to the exact `b/05.bak` and `b/01.bak` files under the recorded overlay run root. The corresponding E4B V3 test receipt confirms a PASS_TEST_ONLY shared Loop boundary preparation, renderer OFF, dispatch/media/audio false, D4.8 BLOCKED and release NONE.

This is a coherent post-qualification source-evolution chain. It is not yet an E6 reuse waiver. The adjudicator must verify exact historical backup bytes from the active checkout and generate a reviewable diff. The source paths, backup root and backup names are matched exactly to the recovery receipt, not merely by suffix.

## V1 defect correction carried into this V2 overlay

- Current source hashes and byte counts are checked even when a historical backup is missing.
- Dangling symlinks are rejected before relying on `Path.exists()`.
- Reparse-point ancestors and path escapes are rejected.
- E4B recovery root and full backup paths must exactly match the immutable receipt.
- E4B governance state is checked across renderer, launcher, dispatch, audio, media, C11-C modification, D4.8, D9.10, D9.14, D9.16, D9.17, D10 and release authority.

## Status interpretation

- `PASS_HISTORICAL_PREIMAGES_RECOVERED_REVIEW_REQUIRED`: both exact preimages are present and match SHA-256 plus byte count. The diff is available for manual semantic review. CH004 is still only a reuse candidate.
- `BLOCKED_HISTORICAL_PREIMAGE_MISSING_OR_MISMATCH_NO_WAIVER`: at least one historic backup cannot be verified. CH004 remains ineligible for E6 reuse; do not restore a source or regenerate old E4 evidence.
- `BLOCKED_AUDIT_PRECONDITION`: an immutable receipt/manifest, current source pin, path binding or governance field does not match. Stop and preserve evidence.

No status automatically accepts CH004 reuse. Manual semantic review and a separate E6 ledger requalification are required.

## Next steps after this adjudication

1. Inspect the exact generated unified diff and AST symbol delta, if both historical preimages were recovered.
2. Decide CH004 reuse eligibility only after reviewing whether changed hunks affect E4A.7 request inputs, editorial resolver behavior, Challenge compositor semantics, source-video identity, A/B/C audio/mux outputs or any E6 acceptance predicate.
3. Build a new D9 capture-plan V2 from the exact 2026-11-18 reconciliation receipt. The old V1 plan remains unchanged. Retire only the stale nine-dependency finding; preserve six Challenge groups, 18 E1 intents, 18 D envelopes and one visual source per selector shared by A/B/C.
4. Freeze the 18 top-level Smoke18 family rows and complete reuse ledger. Challenge A/B/C are sub-probes, not additional top-level scenarios.
5. Prepare separate E6 TEST_ONLY authorization and a formal governance resolution of D4.8 before any media execution.

## Historical timing note

The operator explains the one/two-second Challenge duration differences as early family-design history: initial definitions predated settled countdown/HOOK/CTA blocks and social-duration decisions. Preserve that provenance. For CH008/009, declared duration (11 s) and current phase-sum duration (12 s) remain separate facts. Do not edit definitions, frame counts or durations in this audit. A canonical delivery duration requires an explicit later policy decision.

## Permanent boundaries

C11-C 2.19.12 remains sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. D4.8 R1V V2 SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` remains unchanged and BLOCKED for Smoke18, D3/audio/PCM and FFmpeg mux. E1/D9 PREPARE_ONLY; renderer OFF; dispatch/media false; no Godot/Movie Maker/FFmpeg/FFprobe/audio/mux/BatchId; `release_authority=NONE`.

`GIT_CHECKS=SKIPPED`; commits operator-managed; SHA-256 pins enforced.
