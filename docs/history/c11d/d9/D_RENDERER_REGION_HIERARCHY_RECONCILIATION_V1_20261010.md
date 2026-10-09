# Historical Record — Renderer Region Hierarchy Reconciliation V1

**Date:** 2026-10-10  
**State:** preparation-only; no approvals granted.

This increment was created after Windows acceptance of the initial normalized region proposal. Review against the existing D1.5 contract and frozen presentation implementation identified that the repository already has a shared 540×960 logical frame (`HEADER` / `BODY` / `FOOTER`) and a distinct profile-driven composition geometry. The family catalog and existing Visual Loop renderer routing supply family identity/render behavior; they do not turn the proposed normalized-permille boxes into canonical family geometry.

The new reconciliation contract makes that source hierarchy explicit and declares the normalized proposal exploratory and noncanonical. It does not modify the previous proposal's test implementation; that test continues to verify deterministic proposal generation and its non-approval locks. The old proposal may not drive a temporal schedule or renderer.

No frozen C11-C source or manifest was changed. This increment creates no frames, durations, renderer-native input or media. All approval and activation locks remain closed.
