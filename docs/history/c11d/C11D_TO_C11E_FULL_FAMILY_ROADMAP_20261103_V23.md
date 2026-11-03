# C11-D → C11-E Full-Family Roadmap — V23

**Date:** 2026-11-03. Records Challenge policy approval and the next D-only pixel-render increment.

## Product outcome

One production service for Challenge, Visual Loop and Visual Drill. Preserve C11-C mechanics/generators and existing family audio. Add approved D presentation/editorial, family-correct music, FFmpeg mux, FFprobe/A-V QA, and immutable receipts. The current Producer GUI remains the operator surface; CLI remains compatibility/automation over the same service.

## E4A Challenge — current state

- Gate A readiness assessment closed with blockers: 0/10 I/O groups complete, 6 partial, 4 blocked; candidate identity 164 sources; sidecar 14/14; visual payload consumption 0/14. Five Python test exits unverified due the PowerShell stderr capture defect. No blanket rerun.
- Challenge Policy V1 approved by the operator 2026-11-03. It defines semantic fields/regions/windows only; geometry remains tied to D1.5/profile/family and unknown values fail closed.
- D1.1 mapping evidence PASS; D1.7 declarative mapping PASS 9/9; D1.5 canonical logical frame is 540×960 (HEADER 0–144, BODY 144–816, FOOTER 816–960).
- Reuse existing D-only materializer, V2B safe coordinate projection/allowlisted consumer and source-composition lineage. The historic V2B 277-case review and 402-check source-composition evidence do not prove pixels and must not be rerun absent source drift.

## Ordered delivery

1. **E4A.2 — source-bound D-only integration:** extend the existing Challenge in-memory source-composition boundary with exact canonical editorial values, value hashes, policy ID/hash, semantic region, named source phase window, source lineage and request/payload identity. No second binder/renderer.
2. **E4A.3 — isolated pixel render:** use an off-screen Godot test-only surface consuming the same D composition output. A/B with identical Challenge source/gameplay and distinct editorial values. Prove expected pixel changes only in approved region/windows; prove game/body/source pixels and source-frame hashes unchanged. `language` and empty values cause no draw. Missing/ambiguous window or unresolved `CHALLENGE_OVERLAY` geometry fails closed.
3. **E4A.4 — isolated A/V acceptance:** after pixel proof, reuse the accepted E3 D3 V5 + FFmpeg/FFprobe QC path for a test-only A/V output. Do not rerender gameplay for a music-seed test. E4A closes only when visual fields and audiovisual output are evidenced.
4. **E4B Loop:** grammar/variant timeline, editorial/layout mapping, preserve footer omission and existing Loop music.
5. **E4C Drill:** type/tier mapping, phase/END_CTA precedence, editorial/layout and existing Drill music.
6. **E5:** determinism, independent gameplay/music seed domains, family/profile non-leakage, GUI/CLI parity.
7. **E6 Smoke18:** six A/V scenarios per family.
8. **E7 Matrix101:** 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held until 11s/12s timing conflict is authoritatively resolved (99 provisional).
9. **E8:** row-by-row historical C11-C production/review corpus reconciliation, including 27 review cases, 9 Challenges and all other visual cases; independent acceptance, immutable freeze and explicit promotion.

## Governance

C11-C 2.19.12 remains the only production baseline; manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Production renderer OFF, D9.10 PREPARE_ONLY, D4.8 blocked, D9.14/D9.16 blocked, D9.17 no-go, D10 blocked, release authority NONE, no freeze or promotion.
