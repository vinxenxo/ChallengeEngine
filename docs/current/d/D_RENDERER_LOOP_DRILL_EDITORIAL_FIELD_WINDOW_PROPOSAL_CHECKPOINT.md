# D Renderer Loop/Drill Editorial Field-Window Proposal Checkpoint V1

## Decision state

`PROPOSED_NOT_APPROVED`. This checkpoint proposes a testable visibility-window rule for the existing universal editorial fields on request-scoped Visual Loop and Visual Drill payloads. It does not replace or mutate the canonical editorial model, the neutral frame program, the temporal-bound preview, or the existing Challenge-only field-window proposal.

## Proposed rule

- Resolve the generated instance's actual in-memory `frame_count` and `fps`; never derive frame count from the editorial text or infer content subphases.
- For non-empty `title`, `subtitle`, and `call_to_action`, propose a full continuous-span window `[0, frame_count)` using zero-based, half-open intervals.
- Suppress an empty visual value and assign no window.
- `language` remains metadata-only and never receives a visibility window.
- Reject fields outside `title`, `subtitle`, `call_to_action`, and `language` until an explicit mapping is proposed and tested.
- Preserve source text exactly. Geometry, font/style, animation, renderer instructions, and media production remain out of scope.

## Pinned review fixtures

| Content type | Payload instance | FPS | Frames | Duration |
|---|---|---:|---:|---:|
| Visual Loop `harmonic_membrane` | `D-VLP-5ac67e64ff717d97` | 30 | 600 | 20 s |
| Visual Drill `tracking/tier-2` | `D-VDP-1a96afdd7a0d950e` | 30 | 630 | 21 s |

These two fixtures validate the proposal only. Runtime instances remain request-scoped; the rule uses their actual materialized frame count.

## Validation

Run:

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_loop_drill_editorial_field_windows.py .\tools\c11d\d9\test_d_renderer_loop_drill_editorial_field_windows.py
python .\tools\c11d\d9\test_d_renderer_loop_drill_editorial_field_windows.py
```

The validator checks the pinned C11-C manifest, payload/temporal/editorial contracts and source lineage. Tests exercise full-span windows, empty suppression, metadata-only language, unknown fields, interval arithmetic, immutable source text, and fail-closed governance locks.

## Approval and execution boundary

This proposal does **not** automatically clear `VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_UNDECLARED` or `VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_UNDECLARED`. The unified review should continue reporting these gates unresolved until a separately authorized integration/approval step exists.

C11-C remains immutable; renderer OFF; renderer-native input false; dispatch false; production false; payload files not written; media not created; D4.8 blocked; release authority none; D9.14/D9.16 full acceptance blocked as required; D9.17 no-go; D10 blocked.
