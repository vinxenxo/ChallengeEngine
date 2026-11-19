# C11-E — next phase gate plan after native Qt/QImage qualification

Status: PREPARE_ONLY / NOT AUTHORIZED FOR REAL FRAME EXECUTION.

## Entry criteria

All must be independently demonstrated before L2:

- V2.5 installer complete, Add-only receipt and sidecar verified.
- V2.4 A3/source adjudication PASS against original producer contract.
- All 17 focused regressions pass.
- Existing target suite passes 37/37 QImage tests.
- Seven-iteration native benchmark P95 <=33.333 ms; preserve per-iteration timings and receipt.
- Operator inspects the three synthetic previews and explicitly approves the resampler. Geometry approval is already fixed separately and does not imply resampler acceptance.
- Read-only source closure identifies the exact immutable C Loop frame producer/output, selector, source artifact and sequence ordering; the D9.9/D9.10/R1P mapping; exact decoded RGB24 byte count, width, height, stride and color interpretation. All source files and evidence are SHA-pinned. Do not guess a media decoder or input path.
- A separate bounded successor policy to D4.8 V2 and a separate exact E6 TEST_ONLY execution manifest are approved. Both specify executable paths/hashes/versions, arguments, inputs, outputs, process counts, side effects, stop-on-first-failure and identity reservation. D4.8 V2 itself is never edited or bypassed.

## L2 — one copied real frame only

- Read the exact approved source frame via the already identified existing D seam. Make a byte-identical copy as the test input; do not mutate source artifacts or family output.
- Run only the approved D-owned post-composition consumer on that one copied frame.
- Verify input copy hash, exact RGB24 dimensions/stride, output 720x1280 geometry, body 504x896 at (108,192), black bands/gutters, body pixel mapping and the output/receipt hashes.
- No media encoding, audio, mux, FFmpeg, FFprobe, Godot, renderer dispatch or production writes unless a separate authorization explicitly includes them. This is a pixel-stage proof only.

## L3 — negative controls and human review

- Include wrong dimensions, wrong byte count, incorrect stride, altered source hash, frame-order mismatch and forbidden-source-write controls; each must fail closed.
- Compare body region against the approved reference, verify reserved bands/gutters, inspect text/edges/artifacts and record explicit human visual review.
- Accept or reject the resampler independently from geometry. Preserve all failed controls and receipts.

## L4 — six Loop selectors

Only after L2/L3 PASS and a separate scope approval, apply the same consumer to exactly the six Smoke18 Loop selectors. Preserve each family's binder, grammar, timeline, seeds, frame identity and existing family music. No new binder/adapter/Producer. Keep source C and existing accepted media immutable.

## L5 — Smoke18 integration

A later, separately authorized stage may link eligible Loop rows into Smoke18. The native Qt test result alone does not authorize Smoke18 rendering, media creation or E6 acceptance. All 18 top-level rows still require their own acceptance predicates and immutable evidence.

## Governance

C11-C remains the sole production baseline. D4.8 V2 stays BLOCKED and unchanged. E1/D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION. Renderer/dispatch/media OFF; E6 accepted 0; no BatchId; `release_authority=NONE`. `GIT_CHECKS=SKIPPED`; commits operator-managed; active source pins enforced.
