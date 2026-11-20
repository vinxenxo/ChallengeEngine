# C11-D to C11-E Full-Family Roadmap — V126

**Date:** 2026-11-20

## Product target

Complete factory replacement for Challenge, Visual Loop and Visual Drill while preserving C11-C mechanics, family-native binders/grammars/timelines and family-native music. E1 remains the single service seam; D owns presentation/layout/editorial and the Option C post-composition boundary. Delivery/mux/QC/provenance remain distinct controlled stages. No parallel Producer/binder/GUI or generic family adaptation is introduced.

## Current sequence

1. **QImage synthetic L1 and phase reconciliation — closed.** V2.7 synthetic native Qt/QImage pixel stage: 37/37; P95 5.5743 ms; not end-to-end. V2 correction: 21/21 tests and 18/18 read-only evidence checks PASS.
2. **Human QImage resampler review — next.** Inspect the three pinned V2.7 previews and explicitly accept/decline `SmoothTransformation`. The 720×1280 geometry and 504×896 body at (108,192) remain approved independently.
3. **Read-only Loop source closure.** Establish exact selector-to-source mapping, source hash, frame order/index, PTS/timebase, decoded dimensions/pixel format/planes/stride/packing, color interpretation, orientation/alpha and D9.9/D9.10/R1P lineage. Unknown values remain UNKNOWN; no decoding or renderer/media execution in this gate.
4. **D-only QImage consumer at existing Option C seam.** One copied frame only after a separately approved successor policy and exact E6 TEST_ONLY execution manifest.
5. **L2/L3 one-frame proof.** Source no-change, geometry/bands/body identity, byte layout, negative controls and operator review; then **L4 six Loop selectors** with exact input/output hashes and per-row receipts.
6. Challenge runtime editorial readback and Drill runtime editorial readback remain independent family gates.
7. Smoke18 only after row-level source, consumer, family audio, visual/editorial, QA and governance predicates all pass.
8. E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill); CH_008/009 remain held until 11s/12s timeline conflict is resolved. E8 full historical regression, independent acceptance, freeze and separate promotion.

Smoke18 has 18 top-level rows (6+6+6) and 18 nested Challenge A/B/C subruns. Reuse requalification is 13 candidates, not accepted rows; five fresh Challenge A/V outputs remain, six Loop D-composited outputs remain, and six Drill row predicates remain.

## Governance

C11-C frozen manifest unchanged; D4.8 V2 immutable/BLOCKED; E1/D9.10 PREPARE_ONLY; renderer OFF; media/dispatch OFF. No engine/media/dispatch/BatchId until separately approved D4.8 successor and exact E6 TEST_ONLY manifest. `E6_ACCEPTED=0`; `RELEASE_AUTHORITY=NONE`.
