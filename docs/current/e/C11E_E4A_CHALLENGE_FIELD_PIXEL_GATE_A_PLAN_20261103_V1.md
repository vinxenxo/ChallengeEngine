# C11-E E4A.1 Challenge Field/Pixel Gate A — Plan V1

**State:** `READ_ONLY_REFRESH_PENDING`  
**Date:** 2026-11-03  
**Purpose:** refresh the D renderer candidate-I/O and request-specific carrier/materialization evidence after the E3/E4A service updates, without implementing or authorizing a visual consumer.

## Why this gate comes next

E4A static source/GUI contract audit is now closed read-only. The Challenge source inventory found the existing runtime/binder path, but a source-symbol scan does not prove D9.9 fields are consumed by the visual payload or drawn. The previous field-consumption checkpoint reports canonical-to-review parity 14/14 and visual-payload consumption 0/14. Challenge universal-field window policy is absent; Challenge phase fields are not aliases; semantic geometry remains unresolved. This Gate A refreshes the current request/payload input readiness and identity evidence so the next policy work starts from current source bytes.

## Exact Windows sequence

1. `python -B .\tools\c11d\d9\test_d_renderer_candidate_io_gap_audit.py`
2. `python -B .\tools\c11d\d9\d_renderer_candidate_io_gap_audit.py`
3. `python -B .\tools\c11d\d9\test_d_renderer_candidate_identity_inventory.py`
4. `python -B .\tools\c11d\d9\d_renderer_candidate_identity_inventory.py`
5. `python -B .\tools\c11d\d9\test_d_renderer_request_scoped_editorial_value_carrier.py`
6. `python -B .\tools\c11d\d9\d_renderer_request_scoped_editorial_value_carrier.py --godot <Godot 4.7.1 executable>`
7. `python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding.py`
8. `python -B .\tools\c11d\d9\d_renderer_request_scoped_payload_materialization_binding.py --godot <Godot 4.7.1 executable>`
9. `python -B .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py`

The bundled PowerShell 5.1 runner executes the steps sequentially, captures stdout/stderr separately, records process exit code immediately, hashes all outputs, validates 21 exact source pins before and after, and packages a report/receipt. It checks Python 3.13 and Godot 4.7.1. It adds the V30 documents via add-only handling and never overwrites an existing different file.

## Gate A acceptance

All nine processes must exit zero; all 21 source pins must match before and after; report and receipt must validate. A PASS means only that candidate I/O/identity/carrier/materialization/baseline preflight contracts run successfully on the current Windows source. The resulting gap counts and governance flags must be reviewed. It does not mean a renderer input is admissible, editorial text is part of the visual payload, a field is approved for a region/window, or a video contains the requested text.

## Prohibited in this increment

No source patch, no GUI launch, no production CLI job, no gameplay render, no D3 music render, no FFmpeg mux, no MP4/WAV/media, no renderer-native input, no dispatch, no C11-C code/mechanics/audio mutation, no D policy approval and no release/promotion. Godot is invoked only by the existing read-only fixed-fixture materialization/binding harnesses.

## Next after Gate A

Reconcile current input-group and identity results. Then prepare a D-owned review proposal for each Challenge field, including semantic region, profile/family inheritance, geometry source, visibility window/timebase and empty/disabled behavior. Keep `title/subtitle/call_to_action` distinct from phase `hook/reveal/cta`; `language` is metadata-only. Obtain explicit hash-bound policy approval before designing the payload-side visual consumer.
