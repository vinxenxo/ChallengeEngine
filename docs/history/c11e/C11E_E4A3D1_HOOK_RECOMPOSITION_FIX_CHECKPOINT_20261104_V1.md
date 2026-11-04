# C11-E E4A.3D.1 — Challenge native HOOK recomposition checkpoint V1

**Date:** 2026-11-04  
**Scope:** D-only isolated test compositor; Challenge only; fixture `CHALLENGE_004`.  
**Parent:** E4A.3D shared-layer consumer V1, statically applied and exercised once in Godot.

## Triggering evidence

The first E4A.3D Godot run used the accepted E4A.2 real C11-C delivery frames and completed with Godot exit 0: 6/6 source frames extracted, 18/18 PNGs and 12/12 pixel comparisons; BODY identity held at all six samples. Its report also correctly showed `existing_c11c_hook_content_overlap_observed=true`: the D header had been transparent, so title/subtitle were drawn over the native Challenge HOOK already baked into the C11-C base video.

That is a visual integration defect, not a failure of the source frames, the E4A.2 base or the BODY-pixel identity checks.

## D-only correction

- When non-empty D `title` and/or `subtitle` are active in the canonical HOOK source interval and `show_hook_countdown=true`, the adapter reads the selected fixture's existing native hook text and builds one C11-C shared header: native Challenge hook as line one, optional D title/subtitle in the remaining two-line capacity.
- The shared C11-C header background is opaque and covers the baked native hook pixels before the shared header is drawn. The adapted live render model suppresses the native UI hook to avoid a second live owner; the BODY countdown remains visible when ON.
- With visibility OFF, the shared header omits the native hook. The real-base pixel harness cannot erase hook/countdown pixels already baked into the immutable C11-C base MP4; the report continues to describe OFF as a live-model contract only.
- The C11-C shared header algorithm remains unchanged: its own three-line wrapping and deterministic font fit-down are reused. A D-side diagnostic reads the mounted Label/font and fails closed unless rendered hook samples fit within 3 lines, 468 logical px and the existing 120 logical px label box.
- FOOTER/CTA remains single-owner: the shared D footer replaces native C CTA pixels only while a non-empty approved D CTA is active.
- `CHALLENGE_OVERLAY` (`player_name`, `challenge_label`), generic D1.5 safe-area policy and Challenge production placement remain blocked/unapproved.

No C11-C source, binder, timeline, generator, mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream` or `FrameSnapshot.custom_data` is changed.

## Verification in packaging environment

- Focused Python contract suite: **80 passed**.
- `py_compile`: exit 0 for runner and focused tests.
- The Python runner now checks the Godot report's two real HOOK samples, confirms the native Challenge hook is exactly the first rendered header line, validates measured line count/width/height, and rejects any overlap flag.
- Godot 4.7.1 is not available in the packaging environment. Therefore this checkpoint does **not** claim the revised GDScript has passed the Windows Godot runtime or the pixel rerun. That remains the next operator execution.

## Next action

Apply the pinned D-only overlay transaction on the active Windows checkout. Then rerun the same bounded E4A.2 real-body compositor command. Accept only if Godot exits 0, 18 PNG/12 comparisons pass, BODY identity remains intact, both HOOK samples prove one recomposed hook/header and fit diagnostics pass. Preserve `visual_placement_approved=false` until separate operator visual review and D1.5/Challenge layout authority are reconciled.

## Governance

`renderer=OFF` for production; production dispatch/media false; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `release_authority=NONE`. The isolated E4A test compositor is not the production renderer and its PASS is not promotion authority.
