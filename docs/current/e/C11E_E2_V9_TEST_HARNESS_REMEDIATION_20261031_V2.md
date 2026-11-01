# C11-E E2 V9 test-harness remediation — V2 package/installer correction

## Code/harness content retained from V9 V1

The test no longer preloads/instantiates `C11EChallenge001E2.gd` or `GeneradorMaestro.gd`. Production and the test use the same lightweight `C11EE2SidecarValidator.gd`. The native test performs a real JSON serialize/parse round trip, validates the complete sidecar, executes 30 positive/negative numeric cases and writes a structured result JSON. The runtime runner verifies that result before Python pair preparation and renderer invocation.

## V9 V1 installer defect

The operator's V9 V1 installer stopped at the GDScript check: expected V8 preimage SHA `af142fc5fc41f4e398e981e60c014d9ddd09dccc888c1d3fbc2e1b0e77911493`; found `4787b4459eb509117c6d752d1b6744236bb5a291372f2ef5a5cb1eb58755dae5`. The latter is exactly the V9 payload postimage. This path was therefore already at the exact intended V9 content, but V1's blanket V8 pin equality loop failed before per-file preflight. V1 stopped before writes; do not rerun.

## V9 V2 installer policy

V2 is strictly idempotent and state-aware. For every replacement destination:
- hash equals declared V8 preimage: plan a guarded atomic replacement and preserve a backup;
- hash equals exact V9 payload postimage: leave unchanged and record `ALREADY_PRESENT`;
- any other hash or missing file: abort before any write.

For every add-only destination:
- absent: plan add;
- present with exact intended payload hash: leave unchanged and record `ALREADY_PRESENT`;
- present with different hash: abort before any write.

It checks all 16 payloads and destinations, verifies V8 receipt consistency, C11-C manifest, E0/V7 evidence and E0/E1 ancestry before the first repository mutation. It rechecks each destination immediately before writing. Receipt schema is `C11E-E2-V9-FIX-V2-RECEIPT-V1`; status must be `APPLIED`; all 16 target hashes must be final postimages; records per-file disposition and backup details; renderer/media remain false.

## Runtime preflight

After installation and local commit, execute the isolated test with Godot 4.7.1 Mono, writing a unique result JSON. Require exit code 0 and structured result schema `C11E-E2-GODOT-JSON-NUMERIC-TEST-RESULT-V1`, `status=PASS`, both parsed seed types `float`, complete sidecar validation true, and 30/30 numeric cases. A missing result is failure regardless of exit code. Inspect stdout/stderr.

Only then run two isolated CHALLENGE_001 A/B renders (no audio) via RequestId `C11E-E2-CH001-AB-20261031-V9`. Automated E2 success still needs independent human visual review. E3 is blocked until E2 accepted. C11-C remains production baseline to E8.
