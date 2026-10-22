# C11-D Overhand Master Prompt V20 — Allowlisted Coordinate Consumer Design Gate

## Mission

Continue the C11-D vertical challenge-video factory through evidence-based gates toward a controlled D-baseline render. C11-C remains the frozen authoritative Producer until the full D branch is formally accepted, approved, frozen and promoted.

## Accepted latest gate

V2-B allowlisted coordinate consumer specification test suite: `1038/1038` in the active Windows checkout. stdout SHA-256 `c5daea5a270aec81d76aa1c5b1499f8826d1d09e9047b3ad7ae0a7941dfc3682`; stderr empty SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA `c52d3f5ca276beea0482eb1ab521d163e201023f818e9448f6f7279c306b2ef0`.

## Next engineering sequence

1. Apply and run the implementation-design contract suite in the active checkout.
2. If green, add an isolated review-only GDScript implementation of the allowlisted logical target-marker track consumer.
3. Test strict type/domain handling, source cardinality and ordinal preservation, CHALLENGE_005 per-run constancy, output closure, source-data non-leakage, and atomic rejection with no partial track. Planned negative runtime matrix is 261 cases; it is not yet executed.
4. Keep the helper outside production dispatch. No renderer nodes, RenderingServer, asset loading, pixel rounding, crop, viewport capture, native renderer input, payload file, media, or production binding during these gates.
5. Only after the implementation runtime gate and separate formal authorization may the project consider a controlled renderer gate. Do not bypass D4.8, D9.14, D9.16, D9.17, D10 or baseline approval.

## Permanent immutable safeguards

C11-C freeze manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, all approved binding counts `0`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE`. Never serialize `FrameSnapshot.custom_data`; do not mutate challenge JSON, `CoordinateMapper`, or CHALLENGE_004 V1.
