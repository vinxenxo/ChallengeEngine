# C11-E E4A.6 — GeneradorMaestro Optional Consumer / Manifest Reconciliation V1

**Date:** 2026-11-07  
**Source:** V80 archive, E4A.6 historical implementation/runtime records and live read-only diagnostic.

## Correct interpretation of the historical change

The user's recollection that the `GeneradorMaestro.gd` change related to optional fields is close at the integration-boundary level, but the precise contract is:

- E4A.6 V2 added an **opt-in D-only Challenge consumer** at the root scene's existing native bind points.
- The D consumer is loaded only when the explicit argument `--c11e-editorial-envelope=<path>` is supplied.
- When that argument is absent, the D consumer is not loaded and the legacy C path is a no-op/unchanged path.
- When the argument is present, the consumer validates and applies the D-owned envelope after the single native binder call.

The optional item is the **presence of the D envelope/consumer invocation**, not the mandatory canonical editorial field structure. E4A.6 documents no deletion or relaxation of canonical Challenge editorial keys.

## Editorial fields remain canonical

D9.8/D9.9 keeps all six Challenge keys:

`title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label`.

Loop and Drill keep their four-field shared allowlist. Blank optional text values normalize to the existing `UNKNOWN` sentinel; a blank value does not remove its key. No per-field omission controls are introduced by E4A.6 or the D99 GUI correction.

In particular, the D99 correction removed only the premature GUI Hook/countdown control and the unsupported `presentation_options` property from the raw D9.9 universal request. The E1 service retains its existing internal Challenge default. D9.9 schema and E1 service were not changed by that correction.

## Exact source divergence

The frozen C11-C manifest remains unchanged:

- Manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Manifest `GeneradorMaestro.gd` entry: 36,991 bytes, SHA-256 `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`.
- E4A.6 V2 active postimage: 39,767 bytes, SHA-256 `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`.

The implementation checkpoint identifies the changed path as a precise preimage/postimage transaction and lists the D-only consumer/envelope builder/tests as add-only. The runtime closeout records `generadormaestro_written=false` during its later test and proves the exact D-only postimage ran in the test-only root fixture.

Protected C mechanics/simulation truth were not changed by the documented E4A.6 work: `SimulationResult`, `FrameSnapshot`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, native Challenge binder/presentation components, Loop/Drill binders, launcher and QA caller remain outside the stated patch scope.

## Why the D baseline still blocks

The D baseline candidate policy explicitly protects this root path and requires exact equality with the frozen manifest. The V3 read-only diagnostic therefore correctly rejects the current candidate on a byte-level basis:

`BLOCKED_READ_ONLY_PREFLIGHT` / `CandidateAuditError` / `Protected C11-C source drift detected: ['GeneradorMaestro.gd']`.

The diagnostic's generic wording does not mean the divergence is unknown or accidental. Its meaning is now classified as:

`KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT`.

This is a **policy/isolation conflict**, not a claim that C mechanics or simulation truth changed. The D baseline candidate nevertheless remains ineligible under the current strict candidate policy.

## Required handling

- Do not restore or overwrite `GeneradorMaestro.gd` blindly.
- Do not rewrite the frozen manifest to absorb the D-only postimage.
- Do not create a silent path exception or mark the candidate clean.
- Keep D4.8 blocked.
- Before resolving the baseline seam, compare a D/E-owned root/scene boundary, a bounded exact source exception with the original C preimage retained, and a post-composition consumer route. Prefer a design that removes D integration from the protected C root without changing C behavior.

The user's local Git history may later provide the exact frozen C preimage and reviewed diff. It is not required to accept the D99 GUI proof or proceed with non-rendering E4B parameter analysis. Request it only if the selected isolation design requires historical source reconstruction.
