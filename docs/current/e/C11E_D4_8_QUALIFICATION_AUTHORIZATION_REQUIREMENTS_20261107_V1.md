# C11-E / C11-D D4.8 Bounded Qualification Authorization Requirements V1

**Date:** 2026-11-07  
**State:** `REQUIREMENTS_ONLY_NOT_APPROVED`

## Why this record is needed

The active `C11D_PRODUCTION_ACTIVATION_POLICY_V1.json` is version 1.0 and sets `renderer_activation_policy.state=DISABLED`. Its D4.8 test suite returns PASS/CLOSED because it verifies the expected denial of PRODUCTION (`RENDERER_POLICY_DISABLED`) and REVIEW (`REVIEW_MODE`) plus six integrity/negative cases. D4.9's 8/8 governance and 102/102 GUI/CLI parity results validate that disabled policy; they do not grant physical execution authority.

A Loop R1V qualification run is test-only physical use of existing C11-C family launchers. The current policy has no dedicated qualification-only authorization mode. REVIEW is deliberately non-authorizing, and changing the active v1 production policy to APPROVED would overstate the requested scope.

## Required future policy/checkpoint

Create a new versioned policy or a separately governed test-only authorization contract. Do not rewrite policy v1 in place. Its authority must be limited to:

- exactly five predeclared Loop selectors (one per family) and one deterministic repeat each;
- exact active source pins, frozen C11-C manifest hash and R1P receipt/parent identities;
- existing C11-C family launchers only, using their declared CLI contract and `-NoSound`;
- unique empty output roots; no overwrite or cleanup of prior artifacts;
- read-only source video metadata and decoded frame/pixel inspection;
- captured process exit/stdout/stderr evidence and FFprobe/FFmpeg executable/version hashes;
- fail-closed abort on any selector, source pin, timing, toolchain, governance or output-path mismatch.

Explicitly forbidden in this qualification scope: D renderer dispatch, D9.10 consumer dispatch, D3/music, PCM/audio generation, FFmpeg mux or D post-composition, production delivery, Smoke18/Matrix99, release, freeze, promotion, and any modification to C11-C source/mechanics/RNG/protected paths.

## Required approvals and evidence

1. Architecture selection and source-isolation disposition are recorded.
2. Candidate source fingerprint and exact C11-C manifest identity are independently checked.
3. Policy identifies author, independent reviewer, operator approver, timestamp and exact allowed execution scope.
4. The authorization receipt binds policy SHA, R1P run/report/receipt hashes, source pins, tool versions and output-root policy.
5. The D4.8 validator returns an explicit qualification authorization state; the old 8/8 deny suite remains a separate regression and must still reject requests outside scope.
6. No `release_authority` or production/freeze approval is emitted.

This is a requirements record only. It grants no renderer, launcher, frame extraction or media permission.
