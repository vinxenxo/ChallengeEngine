# C11-E E4A.3D.1 — C11-C Header Diagnostic Semantics Fix V3

**Date:** 2026-11-04
**Status:** PASS — isolated technical compositor proof only

## Incident

The frame-signature correction V2 applied successfully: materializer, compositor runner and test preimages matched; all three postimages matched; 82 focused tests and py_compile passed; Godot 4.7.1 exited 0 with empty stderr. The closeout PowerShell then rejected `hook_first` because it expected the combined D title/subtitle string to occupy a predetermined line-2/line-3 split.

## Root cause

The established `C11CVisualEditorialLayer.gd` contract composes `header.line_1` as the primary line and `header.line_2` as one secondary string. The shared layer wraps that secondary string into two lines using the active Inter Bold font and `HEADER_MAX_WIDTH=468`. The split point depends on actual font metrics; it is not a semantic field boundary. The prior PowerShell assertion was therefore stricter than the C11-C renderer contract and rejected valid rendered text.

## Contract-correct validation

The corrected independent Python report gate obtains the exact B-variant `title` and `subtitle` from the accepted E1 intent, joins them with the adapter's ` · ` separator, and validates that the concatenated rendered second/third lines reconstruct that exact ordered text. It permits either valid word-boundary split but rejects omission, duplication, reordering or substitution. It separately verifies that the exact canonical Challenge hook is line one at both HOOK endpoints, there are exactly three nonempty lines, width is at most 468 and height at most 120.

The C11-C phase namespace remains `HOOK/GAME/REVEAL/CTA`; D9.9 editorial keys are not aliases. Approved E4A policy places title/subtitle in HOOK HEADER and call_to_action in CTA FOOTER. The Challenge adapter intentionally keeps Matrix rotation disabled within this phase-scoped HOOK composition; existing Loop/Drill Matrix behavior is untouched.

## Frame signature correction

`_frame_signature_sha256()` now has nine format placeholders for its nine explicit arguments. The signature includes only approved snapshot visual fields and never accesses `FrameSnapshot.custom_data`.

## Apply reconciliation

The report-schema apply V1 subsequently stopped before any source write. Its exact runner/test preimages already contained the corrected materializer pin `01deb241…`, the regex import and the frame-signature arity regression test. The apply incorrectly tried to migrate those states a second time and failed on the obsolete `a5297d…` source anchor. V3 verifies each already-correct state exactly once and changes only the report validator and its semantic regression test. The failed apply's log is retained as evidence; no rollback or repository repair is required for that preflight-only failure.

## Evidence and acceptance boundary

A clean pass requires 82/82 focused tests, py_compile, Godot 4.7.1 exit 0, empty Godot stderr, 6/6 real frames, 18/18 PNG, 12/12 comparisons, BODY identity, hook/text order, CTA single ownership and immutable source/payload/simulation invariants. This checkpoint closes only E4A.3D.1's isolated test-only technical proof. It does not grant D1.5 placement, safe-area, production compositor, CHALLENGE_OVERLAY or release approval.

## Next phase

E4A.5B: read-only Challenge root/launcher source closure. E4A.6: integrate the proven D consumer at the existing Challenge root seam and validate a single owner for HookComponent, CountdownComponent and CTAComponent. Then finish Challenge A/V before E4B Loop and E4C Drill. C11-C 2.19.12 remains frozen.