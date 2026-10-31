# C11-E — E0 re-entry and actual-checkout reconciliation (V2)

## Purpose

Restart E0 as a disciplined re-baseline of the real Windows checkout after the V4 E2 physical-run attempt failed before Python execution. This is a control restart, not a Git reset or a project restart. Preserve commits, E1 and E2 overlays, all receipts, D history and C11-C.

## Confirmed current identity

- `main` HEAD `a3c7c5d284a96ce115ca52208b4039002502753b`, direct parent `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.
- C11-C manifest 796318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- E1 Windows tests 2/2 PASS; GUI operator runtime observation pending.
- E2 V4 overlay installation 21/21 and path guard 4/4 PASS.
- E2 physical process did not start Python, did not generate pair requests/sidecars/AVI/MP4 and did not reach Godot. Failure ZIP was not created; only an empty stage folder exists.

## E0 V2 installer semantics

The installer validates the exact active commit ancestry, C manifest, E1 installation+test receipts, E2 V4 install receipt and all 21 live E2 postimages. It preflights all 13 E0 payload destinations. It also prepares a three-entry archive plan for the exact current V9 `AGENTS.md`, `CONTINUE.md`, and E README. Before replacing any active instruction, it copies those exact preimages to `docs/history/c11e/` and rechecks each archive hash. The resulting receipt reports both archival operations and overlay operations. No renderer or media is invoked.

## Root cause and repaired E2 runner

The WindowsApps execution alias and real Python 3.13 were returned together by `Get-Command`. V4 cast the multi-result `.Source` collection to one string. V5 resolves one absolute existing `.exe`, rejects WindowsApps, records all candidates and the chosen executable, and writes per-process start diagnostics before `Process.Start()`. It captures full exception/inner exception and produces a failure ZIP only after verifying existence, nonzero bytes, readable ZIP entries and SHA-256.

The operator-provided exact Python path is `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe`. Godot 4.7.1 Mono and FFmpeg 9/FFprobe were independently started successfully.

## E0 acceptance

E0 closes only when the V2 installer receipt verifies the exact archive preimages, 12 payload postimages, live E1/E2 receipts, active checkout identity and C manifest. E2 remains a separate physical gate. No E0 operation proves any render or family acceptance.
