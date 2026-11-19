# C11-E E6 Option C Native Qt Probe V2.7 — PowerShell transaction repair

V2.7 recovers from the V2.6 installer defect without re-running V2.1–V2.6 receipts. It corrects the PowerShell 5.1 documentation-postimage verification by using explicit `foreach` checks instead of embedding `-and` in a command invocation passed to `Where-Object`. V2.6's rollback had already removed its 16 added postimages; V2.7 installs a new versioned runner and 11 documentation files, all add-only.

The runner preserves the V2.4 A3 V4 adjudicator and V2.6 payload-tools-root bootstrap, but now explicitly SHA/byte-pins the existing QImage module and its original 37-test suite. It verifies that the target test suite resolves the same imported module instance.

The installer validates the complete ZIP/member manifest, frozen C11-C and D4.8 V2 pins, all destination collisions, path budgets, and documentation destinations before the first destination write. It writes documentation inside the active checkout under `docs/history/c11e/overlays/` and updates the current document index to V175. It does not extract over the checkout.

A green installation does not qualify Qt. The target runner still must execute on the operator's Python 3.13.14 / PySide6 6.11.2 environment, with 8 focused bootstrap tests, the 37 original QImage tests, and seven benchmark iterations.

**Governance remains unchanged:** C11-C frozen, D4.8 V2 blocked, E6 accepted zero, renderer/dispatch/media OFF, `release_authority=NONE`. No Godot, FFmpeg, FFprobe, audio, mux, BatchId or production renderer invocation.
