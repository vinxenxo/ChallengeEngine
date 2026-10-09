# D Renderer Semantic Region Proposal V1 — preparation record

**Date:** 2026-10-10. **State:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`.

The operator confirmed Windows PASS for the renderer-neutral frame program, its parent logical composition and the 22-step C11-C suite. This increment adds a strict D-only normalized region-layout proposal to enable technical review before defining timing. Its four regions (HEADER, CONTENT_STAGE, CHALLENGE_OVERLAY, FOOTER) are all unapproved; bounds use normalized permille axes and do not reuse C11-C geometry.

The builder is pure in-memory, source-bound to the frame program and rejects any attempt to approve regions, emit pixel coordinates, define timing, activate/dispatch a renderer, create media, modify C11-C, or grant release authority. Windows acceptance is pending.

D9.10 remains PREPARE_ONLY; D4.8 BLOCKED; renderer OFF; media false; release authority NONE; D9 OPEN; D10 BLOCKED. A real-video D9.14 run must wait for independent renderer-baseline approval/freeze and explicit D4.8 authorization.
