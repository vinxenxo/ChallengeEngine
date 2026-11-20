# V3 documentation overlay — build and evidence notes

- Documentation package ID: `C11E_E6_L1_CLOSEOUT_DOCS_V3_20261120`.
- This is an ADD_ONLY documentation update. It does not alter project source code, test runners, media, policies or receipts.
- Six historical documents are installed in the versioned V3 overlay directory; seven current documents are added under `docs/current/e/`; three prompts are added under `prompts/`.
- All documentation destinations are inside the active repository. No project documentation destination points to Downloads.
- The installer verifies the package SHA supplied by the operator, manifest/member cardinality, every payload byte count and SHA-256, its own source pin, C11-C/D4.8 immutable pins, destination allowlist, path budgets and collision preflight.
- Installation is ADD_ONLY. Existing identical files may be skipped; any differing destination blocks. Writes use same-directory temporary files and atomic move. Failure rollback removes only exact postimages owned by the current transaction.
- The receipt records the exact postimages, documentation count and unchanged governance state.
- The current Linux build environment cannot execute Windows PowerShell 5.1. Installer AST self-parse is therefore target-verified, not pre-claimed as passed here.
- No Git checks, Godot, FFmpeg, FFprobe, decoder, audio, mux, renderer, media, dispatch or BatchId action is included.
