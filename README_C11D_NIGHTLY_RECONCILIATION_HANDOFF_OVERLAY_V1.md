# C11-D Nightly Reconciliation / Handoff Overlay V1

**Purpose:** normalize the active handover and start prompt to the 2026-10-14 nightly context, document the parallel-work delta, and gate the next functional change on the real Visual Drill authoring sweep. This is a documentation-only overlay; it does not change production code, schemas, renderer behavior, media, or governance.

**Context source ZIP SHA-256:** `562ee7a4108c1588fe8457a64f567715a88b4dff36bf7b6a18f974e5badf2bac`  
**Frozen C11-C manifest SHA-256:** `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`  
**Overlay scope:** replace the current handover/start-prompt documents using strict hash preconditions and add `docs/current/d/C11D_NIGHTLY_RECONCILIATION_CHECKPOINT_20261014.md`.

The source context ZIP contains duplicate `release/C11C_FREEZE_PACKAGE_MANIFEST.json` entries. First member is canonical; second member is not. Never extract the context archive wholesale into the active checkout.

The Visual Drill audit contract and `--contract-only` passed in an isolated preparation copy only after restoring the canonical first manifest entry. Actual Windows Godot 4.7.1 runtime acceptance is pending. Do not prepare/apply a Visual Drill dynamic-binder expansion until all 20 selector runtime receipts pass.

The handover/start prompt retain their historical content below a new authoritative header. The new header explicitly supersedes older next-step instructions when they conflict.
