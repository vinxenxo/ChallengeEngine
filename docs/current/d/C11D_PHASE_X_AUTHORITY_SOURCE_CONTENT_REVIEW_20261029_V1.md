# C11-D Phase X — Source Content Review Bundle V1

## Purpose
Create a read-only review archive of complete source bytes for the 50 high-priority Phase U/W candidate records and the seven previously unsearched documents. The archive is navigational evidence for human review, not an authority decision.

## Pinned inputs
- Phase U triage JSON SHA-256: `4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418`.
- Phase V source-review JSON SHA-256: `1c36ee0afc5bcb4a9ea5b9060487d172c9f251fe366205a8cdaaea2bfc31de67`.
- Phase W queue JSON SHA-256: `ee46f59a85b6b006115b239d5b628ad07f64c9f15b858e739b81c2d2285a239f`.
- Phase W queue Markdown SHA-256: `b3259f7389d1c3196a11a3bbf17976d058dfccf92534d9a8b0b360778fef020b`.
- Phase W receipt SHA-256: `98aeaa27d4f403b27b7c664dbbe422beea4d11462d773244413a018725c57871`.

## Process
1. Validate all pinned input hashes, expected counts and governance locks.
2. Resolve candidate paths under the active checkout root; reject traversal and symlink escapes.
3. Recompute live file size/SHA for all 107 candidates and the seven unsearched documents.
4. Add originals for all 50 high-priority candidates plus seven unsearched documents to a ZIP if within declared safety caps. Record path, priority/reason, size, SHA, member and state. Sensitive filename exclusions, oversize files, unsupported or changed files must be explicit and make the bundle incomplete; they may not be silently skipped.
5. Do not set an authority finding. Every candidate remains `NOT_REVIEWED` / `UNDETERMINED`; human review is required after the generated bundle is inspected.

## Governance
`renderer=OFF`; media/payload absent; candidate input inadmissible; seed domains incomplete; master seed not adopted; approved binding counters zero; release authority NONE. CHALLENGE_008/009 remain blocked at declared 11 seconds vs phase sum 12 seconds. No global absence claim is made. C11-C remains authoritative.
