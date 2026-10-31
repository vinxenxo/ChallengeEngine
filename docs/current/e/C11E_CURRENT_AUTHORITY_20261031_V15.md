# C11-E — current authority (V15)

**Cut-off:** 2026-10-31. **Verified install-time checkout:** `main` / `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, direct parent `a3c7c5d284a96ce115ca52208b4039002502753b`, tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`, clean worktree, ahead 2 of origin/main.

## Commit-per-iteration operating rule

The operator commits locally at each iteration. This is expected. Each installer pins the exact HEAD and parent reported for that iteration. This V7 V2 installer is pinned to `b92434d` / parent `a3c7c5d`. The E2 runtime runner records the actual HEAD/parent at execution and requires E1 commit `a3c7c5d` and E0 re-entry commit `b92434d` to remain ancestors, while verifying exact source hashes. Therefore a user commit after installing V7 does not invalidate the runner merely because HEAD advanced. The next installer still must be rebuilt against that newest committed HEAD/parent.

## Immutable baseline and governance

- C11-C frozen manifest remains 796318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not modify or replace it.
- C11-C 2.19.12 remains production baseline until E8 independent acceptance and explicit promotion.
- D governance/release locks remain unchanged: D9.10 `PREPARE_ONLY`; D4.8 blocked; D9.14/D9.16/D9.17/D10 not authorized for promotion; release authority `NONE`.
- No installer changes Git refs, commits, pushes, resets, cleans, rebases or switches branch. Failed and partial evidence remains immutable.

## Previously verified E0/E1

- E0 V2 applied: 13/13 payload postimages and 3/3 archived V9 instruction copies. Receipt SHA-256 `869a099c6d73e9b9230db954e68707e3b079db82c368dd151806f8e10a9c8315`. E0 re-entry commit is `b92434d`; E1 foundation commit is `a3c7c5d`.
- E1 shared GUI/CLI service installed; Windows automated tests 2/2 exit code 0; manual GUI observation remains pending. E1 receipts retain their original install-time base HEAD `bc8330e`; the runtime runner validates those receipt values separately from current HEAD parent.

## E2 V5/V6 failures

- V5: 9/9 pair tests and preparation succeeded. Runner attempted to read `request_id` from the CLI summary rather than the verified pair receipt; no Godot render.
- V6 installer V1: 0/9 writes because `.NET File.Replace` received null backup path. V2: APPLIED 9/9 with backups and postimages verified. Receipt SHA-256 `c5cb29311d1da63fd8dab80054f99ec4e0681a081622905070ee6ecc962b47e7`.
- V6 runtime: pair tests 9/9. Godot returned exit 0 and Movie Maker reported 540 frames at 540×960/60 FPS/9 seconds. `godot.stderr.log` reports Variant-inference parse error at GDScript line 54 and `Failed to load script`. The AVI has 540 MJPEG frames; sampled frames 0/270/539 each contain exactly one RGB colour, `(77,77,77)`. It is a blank grey viewport, not accepted visual output. Failure ZIP SHA-256 `1a5d6341fae51152fb9684cc4fc158bf7c9849716a7028015f6d84b013a1cc21` (46,460 bytes / 48 entries).

## V7 V1 installer refusal — no writes

The first V7 installer package pinned stale `HEAD=a3c7c5d` and parent `bc8330e`. The operator had committed E0 re-entry, so actual HEAD was `b92434d` and parent `a3c7c5d`. The installer refused at checkout identity check before temp-file creation or receipt creation. No V7 payload was applied. Subsequent console lines reused V6 receipt variables and were not V7 evidence. The operator's checkout was valid and clean; the package was stale because assistant workflow failed to account for the user's commit-per-iteration rule.

## E2 V7 V2 correction

- GDScript explicitly declares `var parsed: Variant = JSON.parse_string(...)`, correcting the warning-as-error parse failure.
- Runner pins that corrected GDScript; treats `SCRIPT ERROR`, `Parse Error`, `Failed to load script`, and `Warning treated as error` as fatal; inspects source frames 60/270/480 with FFmpeg `signalstats`, rejecting spatially uniform frames; and records actual Godot invocation and media paths in failure evidence.
- Runtime checkout validation: branch must be `main`; E1 commit `a3c7c5d` and E0 re-entry commit `b92434d` must be ancestors of current HEAD. Exact source pins and frozen C11-C manifest remain mandatory. Actual HEAD and parent are bound into receipts.
- Installer V2 exact install-time identity: `b92434d` / parent `a3c7c5d`. It also requires the E0/V6 receipts and V6 failure ZIP pins. It performs no renderer/media operation.
- After installer APPLIED and complete postimage/backup verification, runtime retry is a new RequestId `C11E-E2-CH001-AB-20261031-V7`. A local commit after installation is compatible with the dynamic ancestry/source-pin check.

## Full product path unchanged

E2 acceptance requires two valid nonblank A/B outputs, FFprobe validation, gameplay/body pixel identity, expected title-slot visual difference, provenance hashes and human review. Then E3 D3 Music V5 + independent music seed + FFmpeg mux + FFprobe; E4A Challenge; E4B Loop; E4C Drill; E5 determinism/seed isolation/GUI-CLI parity; E6 Smoke18; E7 Matrix101; E8 independent acceptance and explicit freeze/promotion.

Enabled editorial fields: common `title`, `subtitle`, `call_to_action`, `language`; Challenge-only `player_name`, `challenge_label`. Hook/preparation/final/header/footer and show flags remain disabled. Do not map title to hook or CTA. Loop/Drill require E-owned family adapters. CH_008/009 remain held over 11 s declared versus 12 s summed phase durations.
