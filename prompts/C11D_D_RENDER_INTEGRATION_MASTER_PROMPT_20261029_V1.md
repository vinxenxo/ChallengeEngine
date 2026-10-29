# C11-D Render Integration — Master Prompt V1 (29-10-2026)

## Mission

Continue engineering `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` so the accepted D baseline becomes the default path for generating videos through the existing `c11c-suite`. D adds editable universal editorial, presentation/composition and music behavior around the already-working C generation mechanics. The end product must be operable from both CLI and GUI through the same canonical service and must pass real-video acceptance for Challenge, Visual Loops and Visual Drills.

**This is a functional production task, not an endless contract-preparation task.** Move from source inspection to a minimal D-only integration and real MP4 validation as soon as the checked-out contracts and gates permit it. Static PASS reports must not be presented as video acceptance.

## Product boundaries

- Keep frozen C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` untouched; expected SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, expected size 796318.
- Reuse the existing generator/mechanics and rendering path where behavior is unchanged. Add the D layer in a separately owned path; don't rewrite C's engine to get D output.
- D9.8 Universal Editorial Model exists; D9.9 request/plan and GUI/CLI parity exist in their tested scope; D9.10 is a PREPARE_ONLY bridge, not a renderer dispatcher.
- A historical audit reported editorial review-chain parity 14/14 but visual payload consumption 0/14. The renderer candidate inventory historically declared `NOT_IMPLEMENTED`. Verify current checkout hashes and later changes, then close the actual code gap.
- D3 Music Engine V5 / audio/mux route has bounded A/V evidence. The D coverage matrix must prove it for all supported family variants. Keep `request.seed` separate from `request.music_seed`.
- Only five operational surfaces: `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`. No `c11d-control`, no `c11c-studio`, no sixth suite.
- `winning_frame` is the temporal anchor; `close_calls` counts episodes. Do not serialize full `FrameSnapshot.custom_data` or put editorial values into simulation truth.
- Longform is out of scope until supported by the active D contracts. CHALLENGE_008/009 stay out of the first media pilot while their 11s vs 12s timing conflict remains unresolved.

## Current verified continuity supplied 2026-10-29

- Phase AD tests: 60/60 PASS; closeout add-only overlay applied and verified.
- Ledger V18, checkpoint V41, master/start closeout prompts V41 exist with the pins enumerated in `C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V1.md`.
- The user explicitly authorized continued render testing. That statement is evidence of operator intent, not release/freeze/promotion authority and not a reason to falsify a gate.
- Historical snapshot ZIPs are not the live source of truth. In particular the 2026-10-28 ZIP has duplicate C freeze manifest entries. Use the active checkout and the new filtered snapshot exporter; never extract a historical ZIP on top of the checkout.

## Working procedure

1. Read `AGENTS.md`, `.continue/rules/CONTINUE.md`, `C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V1.md`, the functional recovery plan, checkpoint V41, ledger V18 and AD closeout.
2. Verify exact hashes in the active checkout. If a pin differs, stop and reconcile; don't overwrite with a snapshot.
3. Review C acceptance docs/scripts and the current D renderer/payload/editorial/audio paths. Build a factual path map of current C generation and the desired D wrapper/consumer.
4. Find the real visual composition entrypoint. Reuse existing request-scoped binder, editorial resolver, timebase and audio policies. Do not create a parallel binder or another preflight contract just to avoid implementation.
5. Implement the smallest D-only vertical slice. Capture real outputs for one Challenge, one Loop and one Drill in a test-only output root. Verify visible editorial differences, audio and technical metadata.
6. Expand to 18 family-smoke outputs, then 101 supported matrix outputs (54 Challenge, 27 concrete Loop grammars, 20 Drill type/tier variants). Rely on source selector inventories and canonical seed cases, not inferred labels.
7. Exercise equivalent operations through CLI and GUI and through the existing five surfaces. Both entry points must route to the same canonical service.
8. Run affected focused tests then parent/aggregate regressions, update `c11c-test` route/build manifest as governed, and perform D9.14/D9.16/D9.17/D10 acceptance/freeze steps when their prerequisites hold.
9. At every increment document exact source pins, commands, process exit codes, stdout/stderr hashes, produced artifact paths/hashes, inspection results and current gate states. A pass on no-media tests is not a pass for real media.

## Rules against wasted work

- Do not rerun already-green tests unless relevant input hashes changed or the planned code change could invalidate them.
- Do not create more documentation-only phase packages as a substitute for the D visual consumer.
- Do not scan or re-adjudicate all old authority sources again unless a concrete gate needs new evidence.
- Do not claim an actual video was rendered unless the MP4 exists and has been validated by the real Windows/Godot/FFmpeg runner.
- Do not mutate gate flags manually. If a gate blocks a render, inspect its exact contract and identify the minimal missing requirement. A separate test-only mode is acceptable only if existing governance explicitly supports it or an authorized checkpoint records it.
- No release, freeze or production promotion occurs from a smoke render alone.

## Acceptance target

C11-D becomes the default generation baseline only after: visible D editorial/presentation output works in all supported families; the audio/mux path works; 54 Challenge + 27 Loop + 20 Drill videos are accepted or any exclusion has a documented gate-specific cause; determinism and seed isolation pass; CLI and GUI use the same service and produce equivalent identities/results; the five-surface evidence and required D acceptance/freeze checkpoints are closed. C11-C remains unchanged as the historical frozen reference.
