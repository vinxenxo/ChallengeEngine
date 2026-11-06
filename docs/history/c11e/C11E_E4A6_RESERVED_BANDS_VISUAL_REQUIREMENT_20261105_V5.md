# C11-E E4A.6 Reserved-Band Visual Requirement — V5

**Source:** explicit operator clarification, 2026-11-05; V3 adds the accepted current video-background disposition and records the V2 runner defect.

## Requirement

The logical social frame is 540x960. HEADER occupies y=0..144 and FOOTER y=816..960. Whenever the optional D editorial envelope is enabled, both bands render opaque pure black (RGBA 0,0,0,1) across every source frame, regardless of whether the corresponding editorial field is supplied.

- HEADER displays user-selected non-empty `title` and/or `subtitle` only in HOOK.
- FOOTER displays user-selected non-empty `call_to_action` only in CTA.
- Empty/inactive region: black background remains visible; its editorial label and separator are hidden.
- BODY remains native and unchanged.
- When the D envelope is absent, legacy C rendering remains unchanged.
- The current body/video background colour is accepted and is not an E4A.6 blocker. Making it selectable by the user is a separate later editorial feature; it must not change the always-black HEADER/FOOTER contract.

## Implementation boundary

Implement only in D-owned `tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd`. Mount the existing `C11CVisualEditorialLayer` once for an enabled-D envelope, then reassert regional background visibility/color after each shared layer update and toggle labels/rules independently. Do not alter `C11CVisualEditorialLayer.gd`, `UnifiedSocialFrame`, `PresentationUI`, binders, `GeneradorMaestro.gd`, timelines, mechanics, RNG or simulation data.

## Verification

Require the 900-frame runtime counter, one mount, 22/22 focused source tests, 900 black-band frames and captured pixel evidence. Inactive-band samples must have RGB channels <=8 for at least 99.9% of interior samples. Active HOOK header and CTA footer each contain non-black editorial pixels. Record exact still and MP4 hashes. This bounded test-only requirement does not grant generalized safe-area/typography approval or resolve `player_name`/`challenge_label` overlay geometry.

## V1/V2 runner incident record

- V1 did not execute: PowerShell 5.1 rejected two `$i:` interpolations. Use `${i}` or `-f` formatting; do not put `$variable:` inside expandable strings.
- V2 passed AST, 22 focused tests, Godot import, live-root and Movie Maker capture, but returned BLOCKED because a path-based `Test-CaptureLog` received in-memory `$movie.Stdout` text. The Movie Maker stdout actually contains the expected configure and phase markers. Recovery-only V1 separates `Test-CaptureLogText` from `Test-CaptureLogFile` and resumes from the captured AVI; no recapture is required.


## Recovery orchestration clarification — V4

The visual requirement is already operator-confirmed. Recovery V1 stopped before media processing because of an obsolete Git HEAD pin, unrelated to visual correctness. Per-iteration runners must not inspect Git; the operator commits each iteration. Exact source-file hashes and the frozen manifest remain independently checked. The body/video background colour remains accepted and is not part of this reserved-band gate.


## Recovery handoff clarification

The V1.1 postprocessor's two documentation preflight blocks were packaging defects only; neither invalidates the confirmed black-band/editorial/layout visual result. V1.2 embeds and verifies the documentation bundle and requires only the runner file in Downloads.
