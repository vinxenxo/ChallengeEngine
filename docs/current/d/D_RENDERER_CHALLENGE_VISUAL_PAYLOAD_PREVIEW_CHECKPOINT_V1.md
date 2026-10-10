# C11-D Challenge Visual Payload Preview — Checkpoint V1

**State:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`

## Purpose

Materialize a deterministic, in-memory logical visual payload for `CHALLENGE_004` from the authentic frozen runtime output, the D-owned `social_default_v1` presentation binding, and the three canonical physical assets. This closes the prior evidence gap between the runtime result and an explicit semantic visual payload descriptor; it does **not** produce renderer-native input or media.

## Source-timebase payload

- Canonical source: `CHALLENGE_004`, mechanic `parking_v2` 2.0.
- Source timeline: 900 frames at 60 FPS / 15 seconds; phases HOOK 180, GAME 420, REVEAL 180, CTA 120.
- Physical assets: `garage_background.svg` (1080×1920), `car.svg` (160×320), and `parking_target.svg` (200×400); each is loaded as a `Texture2D` for compatibility verification and represented in the logical payload by resource path, byte hash, intrinsic dimensions and canonical semantic role.
- GAME animation: all 420 source snapshots are copied in source order, retaining only position, rotation, scale, opacity, texture index and variant ID. `custom_data`, scores, distance telemetry, `winning_frame`, and `close_calls` are excluded from the visual payload.
- Presentation: the D profile is rebound to `social_default_v1` on a deep copy, and its render model hash is pinned in the result.

## Explicitly unresolved

- The Challenge coordinate space is declared as `CANVAS_1080X1920`; the profile also advertises a 540×960 source canvas and 1080×1920 master output. This checkpoint does not select or apply a coordinate projection.
- Source-timebase GAME snapshots are preserved at 60 FPS. Delivery sample selection/interpolation to 30 FPS is not applied.
- Editorial field visibility windows remain a separate proposal. They are not inserted into this visual payload.
- The materialized data remains a logical review object; the harness does not instantiate scene nodes, draw frames, emit native renderer input, write payload files, or create media.

## Governance

C11-C remains immutable. Adapter mode remains `PREPARE_ONLY`; renderer baseline approval/freeze remain false; D4.8 remains `BLOCKED`; release authority remains `NONE`; D9.14/D9.16 full acceptance, D9.17 closure and D10 remain blocked.

## Acceptance command

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_challenge_visual_payload_preview.py .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_preview.py
godot --headless --path . --script res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd
python .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_preview.py
```

Expected runtime marker: `C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS`. Do not count a Python contract PASS as a substitute for the Godot runtime execution.
