# Build validation — V2

- V2 package is separately versioned and ADD_ONLY.
- 18 repository destinations: 3 audit/test code artifacts, 5 historical overlay docs, 7 current docs, 3 prompts.
- All 15 documentation/prompt destinations are under repository `docs/` or `prompts/`; none is installed into Downloads.
- Installer verifies ZIP member cardinality, SHA-256, byte lengths, source C11-C/D4.8 pins, allowlisted destinations, reparse points, path budgets, preflight collisions, atomic same-directory temporary writes, exact postimages, documentation postimages and immutable install receipt/sidecar.
- Read-only auditor requires all 23 source SHA pins; byte count is exact where declared, explicitly unprovided where null.
- Unit tests exercise null byte-count handling, mandatory SHA matching, exact declared byte-count matching and malformed-value rejection.
- Windows PowerShell 5.1 AST is self-checked by installer and runner on the operator target; this Linux package-build environment did not execute Windows PowerShell 5.1.
- No Godot, FFmpeg, FFprobe, audio, mux, renderer, media, dispatch or BatchId invocation.
