# C11-E E4C tracking batch runner reconciliation — V4

Date: 2026-11-15

## Evidence reviewed

- V2.1 install attempt remains a RUNNING pre-transaction journal with no payload operations. Preserve it; do not rerun.
- V3 install receipt `C11E_E4C_TRACKING_PREROLL_FIX_V3_INSTALL_20261115T073428Z_4d3049a3` reports PASS, 19/19 operations, 5 replacements, 14 adds, 30/30 source pins pre/post, atomic I/O 6/6 and focused Python suites PASS.
- Independent evidence audit verifies all five durable V3 replacement backups against journal preimage SHA values and all 19 installed postimages against the V3 package manifest.

## Incident C — wrapper cannot launch the V3 coordinator

The V3 wrapper's driver SHA is stale (`a032f759baad9c339ce8c58ff47062694050264d86b1b31d51a699c07de2f946`) while its installed coordinator SHA is `9b868c33a705257c8343c58033e2afb44b502992dbd04d73d72a1050cdde2820`. It also checks style guides V25 and V26, not supplied by V3. The coordinator's `--require-v26-guide` guard likewise targets a missing V26 even though V3 added V27. Hence V3 installation PASS is valid, but the V3 wrapper is not a viable execution entrypoint. No selector execution was started by this stale wrapper; this is corrected before any further batch attempt.

## V4 correction

V4 updates only the existing tracking coordinator, its tests and the PowerShell runner (three preimage-pinned replacements). The coordinator and wrapper now both require installed style guide V27. The wrapper pins the exact coordinator postimage SHA. A new static Python contract suite checks those values, the default PREPARE_ONLY behavior, explicit `-Execute` gating and governance strings. The current PowerShell style guide advances to V28 and all current authority/index/backlog/execution/gate/incident docs and the three continuity prompts are reconciled.

The installer stages and runs py_compile, the executor contract suite, the tracking batch suite and the new runner contract suite; parses the installer/support/atomic-test/runner scripts via Windows PowerShell 5.1 AST; and runs the six atomic I/O regression checks before checkout writes. It validates the exact V3 install receipt/journal/backups, all 30 source pins, the frozen C11-C manifest, and replacement preimages. Transaction is 3 REPLACE + 14 ADD. After installation it invokes the corrected runner exactly once in default PREPARE_ONLY mode with a fresh BatchId and saves logs under the V4 evidence root. It does not pass `-Execute` and must not create a one-shot lock/authorization marker.

## Next acceptance boundary

Audit the V4 installer journal, backups, postimages, 30 source pins, frozen manifest, test receipts, AST receipt and embedded PREPARE_ONLY output. The preview must contain precisely `tracking/tier-2` to `tracking/tier-5`, `PASS_PREPARE_ONLY_NO_RENDER`, and no render/Godot/FFmpeg/media/dispatch. Only after that independent review may the new BatchId be invoked once with `-Execute`. Any execution failure after the authorization marker permanently consumes that ID.

E4C accepted coverage remains `tracking/tier-1 = 1/20`. Tiers 2–5 and the remaining 15 selectors are not accepted. E4C closes at 20/20 only after technical receipts plus operator visual and audio review per selector. Frozen C11-C SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; production dispatch false; release authority NONE; Git checks skipped; commits operator-managed.
