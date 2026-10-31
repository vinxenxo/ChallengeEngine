# C11-E E2 V7 — blank-frame remediation and V7 V2 retry authority

## Established V6 physical failure

- Failure evidence ZIP: `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_111109_2fe56abc.zip`; 46,460 bytes, 48 entries; SHA-256 `1a5d6341fae51152fb9684cc4fc158bf7c9849716a7028015f6d84b013a1cc21`.
- Python contract tests 9/9 PASS and pair receipt prepared. Godot 4.7.1 Mono process returned exit 0; Movie Maker reported 540 frames, 540×960, 60 FPS, 9 s.
- `godot.stderr.log`: Variant-inference warning treated as error at `C11EChallenge001E2.gd:54`, followed by `Failed to load script`.
- FFprobe confirms MJPEG 540×960, 60/1, 540 frames, 9 s. Independent decode confirms sampled frames 0/270/539 each contain one RGB value, `(77,77,77)`. This is blank grey output, not a challenge render.

## Code and runner correction

GDScript changes only `var parsed := JSON.parse_string(...)` to `var parsed: Variant = JSON.parse_string(...)`. Runner rejects parse/load error patterns regardless of process exit or Movie Maker completion, checks source frames 60/270/480 for spatial variation via FFmpeg `signalstats`, and records actual renderer invocation/media paths on failure. Existing 9 Python tests, pair-builder, scene, Challenge source, C11-C manifest and D locks remain pinned.

## Per-iteration commits and checkout identity

Operator commits every iteration. V7 V1 had stale installer identity (`a3c7c5d`/`bc8330e`) and correctly refused the actual valid checkout (`b92434d`/`a3c7c5d`) without writes. V7 V2 installer pins exact current checkout `b92434d`/`a3c7c5d`. The V7 runtime runner accepts the current `main` HEAD and later local descendants only when E1 `a3c7c5d` and E0 `b92434d` remain ancestors and exact source hashes match. It records actual runtime HEAD and first parent in the receipt. Each future installation package must refresh its own exact HEAD/parent pins from the current operator checkout.

## Install safety and preconditions

V7 V2 installer validates exact branch/HEAD/parent, clean initial worktree, C11-C manifest (796318 bytes / `e405d08e...`), E0 receipt, V6 V2 APPLIED 9/9 receipt, V6 failure ZIP size/hash, V6 runner/GDScript/README exact preimages, pair-builder/test/scene pins, package manifest/payload hashes, add-only absence and all backup conditions before writing. It records the observed commit and preserves three preimage backups. It never invokes Godot or creates media.

After the installer returns exit 0, verify receipt schema/status APPLIED, 12/12 operations, three replacement backups and all 12 postimages. Then the operator may commit this iteration locally. The V7 runtime runner is ancestry-aware and will bind the actual new HEAD/parent. Execute E2 with `C11E-E2-CH001-AB-20261031-V7`, Python 3.13.14 and Godot 4.7.1 Mono explicit paths.

## Acceptance remains strict

No E2 pass from process exit 0 alone. Require script-load clean logs, two nonuniform source AVIs, FFprobe metadata, two final REVIEW_720 MP4s, gameplay/body pixel identity, expected title-slot differences, header outside-slot identity, provenance and human visual review. E2 is still two Challenge 001 renders, audio disabled. E3/E4 remain blocked until independent E2 acceptance.
