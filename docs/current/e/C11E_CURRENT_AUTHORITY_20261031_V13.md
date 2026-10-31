# C11-E — current authority (V13)

**Cut-off:** 2026-10-31. **Active checkout expected:** `main` / `a3c7c5d284a96ce115ca52208b4039002502753b`, direct parent `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.

## Immutable baseline and governance

- C11-C frozen manifest remains 796318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not modify or replace it.
- C11-C 2.19.12 remains the production baseline until E8 independent acceptance and explicit promotion.
- D governance and release locks remain unchanged: D9.10 `PREPARE_ONLY`; D4.8 blocked; D9.14/D9.16/D9.17/D10 not authorized for promotion; release authority `NONE`.
- No Git ref movement, reset, clean, branch switch, commit or push is part of E2 remediation. Preserve the current worktree and all failed/partial evidence.

## Verified E0/E1 state

- E0 V2 applied on Windows: 13/13 payload postimages and 3/3 archived V9 instruction copies verified. Receipt SHA-256 `869a099c6d73e9b9230db954e68707e3b079db82c368dd151806f8e10a9c8315`.
- E1 shared service remains installed. Windows automated tests 2/2 exit code 0; manual GUI runtime observation remains pending.

## E2 V5 attempt — failed before renderer

- Preflight, toolchain probes, Python 3.13.14, Godot 4.7.1 Mono, FFmpeg 9 and FFprobe 9 succeeded.
- Pair contract tests passed 9/9; pair preparation exited 0 and created A/B requests, intents, effective configs, editorial sidecars and `E2_PAIR_PREPARED.json`.
- V5 queried `$Prepared.request_id`, which is absent from the CLI summary. The field exists in the separately hash-verified receipt. Runner failed before Godot. No AVI, MP4, pixel comparison or media acceptance resulted.
- Failure ZIP SHA-256 `e33086794ef150e3f6d851d95d7752162c97e43fda0422057ddd24ec3f43d3c7`; 26124 bytes, 41 entries.

## E2 V6 package V1 installer incident

- Installer preflight reached the write loop, created the first runner temp file and called `[IO.File]::Replace($Temp, $Destination, $null)`.
- Windows/.NET rejected the null backup path with `System.ArgumentException: La ruta de acceso no tiene un formato válido.`
- Receipt `C:\Users\vinxe\Documents\C11E_E2_V6_FIX_20261031_105922\C11E_E2_V6_FIX_RECEIPT.json`, SHA-256 `408fd6fa62f7e549475779621073a05e570d65b268168e4c87ce8b4f764d559e`; status `FAILED_PARTIAL_OR_NONE`, 0/9 applied. The live runner hash was checked afterward and remained V5: `9340907afd4e787495be5a9d711024a8a7ab2787aa507842ea7c7ada0c198b72`.
- Operator printed a later manual “INSTALLED AND VERIFIED” message after a thrown failure. This is a false PASS and is not evidence; no runner launch followed. See `docs/history/c11e/C11E_E2_V6_INSTALLER_FILE_REPLACE_INCIDENT_20261031_V1.md`.

## E2 V6 package V2 correction

- Keep the reviewed V6 runner postimage unchanged: `33186f24d6a531bbcbd249d647d5a2cbc5bb6cd9f116d0e8731bc29557cab6f5`.
- The V2 installer pins the failed V1 receipt and requires its 0/9 state. It finds exactly one leftover runner temp file from V1, verifies its SHA-256 equals the intended V6 runner postimage, copies it into a new evidence receipt folder, verifies that copy, then removes only that exact verified temp artifact.
- For replacement operations, V2 supplies a unique, non-null backup file path to `[IO.File]::Replace` on the same volume. Each backup is retained in the new receipt directory and hash-checked against the pinned preimage. Add-only destinations and exact preimages are preflighted before the first write.
- V2 package creation and ZIP/payload integrity can be statically checked here; Windows PowerShell 5.1 execution remains pending. No claim of installation/runtime PASS is made.

## Current gate and product path

E2 remains NOT ACCEPTED. Do not run the renderer until the V2 installer returns exit code 0, all 9 payload postimages are verified, and the live runner hash equals the V6 hash above. Then retry with fresh RequestId `C11E-E2-CH001-AB-20261031-V6`.

E2 remains Challenge-only title A/B with audio disabled. Acceptance requires two physical MP4s, FFprobe profile/stream/frame/duration checks, gameplay/body frame identity, approved title-region differences, provenance hashes and human visual review.

The full deliverable remains A/V MP4 production for Challenge, Visual Loop and Visual Drill. After E2: E3 D3 Music V5 + independent music seed + FFmpeg mux + FFprobe; E4A Challenge; E4B Loop; E4C Drill; E5 determinism/seed isolation/GUI-CLI parity; E6 Smoke18; E7 Matrix101; E8 independent acceptance and explicit freeze/promotion.

Enabled editorial fields: common `title`, `subtitle`, `call_to_action`, `language`; Challenge-only `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and show flags remain disabled. Do not map title to hook or CTA. Loop/Drill require E-owned universal family adapters. Challenge/Loop/Drill C mechanics and binders remain intact. CH_008/009 remain held over the 11 s declared versus 12 s phase duration discrepancy.
