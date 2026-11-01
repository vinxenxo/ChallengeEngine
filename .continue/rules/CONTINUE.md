# C11-E continuation rules — V18

1. Treat the live Windows checkout as authoritative. Do not repeat accepted E0/E1 gates or regenerate snapshots unnecessarily.
2. Keep C11-C 2.19.12 immutable: frozen manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. It remains production authority until E8.
3. Complete product target is Challenge + Visual Loop + Visual Drill, with C mechanics intact, D presentation/editorial, D3 Music V5, independent music seed, FFmpeg mux, FFprobe checks and shared GUI/CLI service. CH001 A/B is an early seam test only.
4. User commits locally per iteration. Never reset/clean/switch/rebase/amend/push. Accept verified descendant HEADs with E0/E1 ancestry and exact pins.
5. For installers, validate all receipts, pins, manifest, payload hashes and destination preimages before writes. Only allow exact declared preimage => replace, exact intended postimage => ALREADY_PRESENT, unknown => abort. Add-only may be absent or exact postimage only. Recheck immediately before each mutation; keep same-volume backups.
6. V9 installer V1 must not be run. It incorrectly rejected `C11EChallenge001E2.gd` SHA `4787b445...755dae5`, which was already the exact V9 postimage. Use V9 V2 only.
7. Run isolated Godot 4.7.1 Mono numeric test and require structured JSON PASS, type float for both seeds, full sidecar true and 30/30 cases. No E2 render before this. Preserve stdout/stderr and native exit code.
8. E2 has exactly two CH001 A/B renders and no audio. Verify media, FFprobe, hashes, body pixel identity, title-slot pixel difference and header invariance. Human review is separate. E3 blocked until E2 accepted.
9. PowerShell 5.1-safe scripts. Capture exit codes immediately. On failure halt; never print a success marker or continue validations after failure. No false PASS from stale variables or `$?`.
10. Continue E3, E4A Challenge, E4B Loop, E4C Drill, E5, E6 Smoke18, E7 Matrix101 and E8 in authority order. Keep CH008/009 held for 11s/12s discrepancy until decision.
