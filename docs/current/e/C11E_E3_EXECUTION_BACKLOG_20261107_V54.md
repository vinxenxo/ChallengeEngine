# C11-E Execution Backlog — V54

## Priority 0 — E4B contract audit correction
- Install/run E4B Loop Family Contract V2. Confirm 8/8 tests, 40/40 base pins, 8/8 local pins, audit report and receipt sidecars. MP4 count is observational; visual review remains false.
- Preserve V1 failed logs/receipt; do not overwrite.

## Priority 1 — Existing D boundary consumer
- Inspect current GUI/CLI resolution path and call graph again against active source pins.
- Integrate `build_loop_family_stage_contract` into the existing D9.9→D9.10 preparation boundary without new request fields, a parallel Producer, sixth GUI surface, or direct C11-C modifications.
- Keep output non-dispatchable until request-scoped materialized payload receipt contract is proven.

## Priority 2 — Request-scoped family payloads
- Derive frame_count/FPS/duration from actual materialized payload receipts, never historical manifest metadata.
- Review 27 selector/family binding cases; geometric-only historic Godot payload admission remains 5/27.
- Add positive/negative tests and GUI/CLI semantic parity.

## Priority 3 — Visual composition and render evidence
- Implement approved 720x1280 canvas, 192px header/footer, 504x896 viewport at (108,192), contain/no crop/no stretch/no resampling.
- Isolated Godot render tests must be separately authorized and must use fresh roots, receipt-bound payloads, stdout/stderr hashes and ffprobe/visual review.
- File presence is not visual acceptance.

## Priority 4 — A/V
- Visual launcher remains `-NoSound`; `request.seed` only. Prove `request.music_seed` independently before audio route. D.1 technical envelope alone does not approve music selection, generation, mixing, loudness or mux.

## Locks
C11-C immutable; renderer/dispatch/media off; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 NO_GO; D10 BLOCKED; release NONE.
