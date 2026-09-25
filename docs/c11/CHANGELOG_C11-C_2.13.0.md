# CHANGELOG C11-C 2.13.0

## Regression hygiene
- Fixed two contract suites that could print PASS and then fall through to a FAIL line despite `failures=0` by returning immediately after the successful `quit(0)` path.
- Hardened `tests/run_all.py` so an explicit suite FAIL marker is never accepted as a PASS.

## Duration policy
- Introduced a shared 20..30 second Visual Loop duration policy based on complete authored cycles.
- Production/review Visual Drill gameplay defaults extended while retaining the existing countdown and terminal CTA.
- Updated physical delivery checks to derive frame count from the resolved duration rather than 540 hard-coding.

## Seed spacing
- Added stratified batch seed allocation and minimum-gap validation for weekly, monthly and multi-seed review workflows.
- Monthly validation now enforces spacing across the entire month.

## Sacred Symmetry
- Tightened visual containment inside the Body without changing logical social geometry.

## Long-form Visual Loops
- Added a sequence-composer architecture for 180 second family anthologies.
- Reuses canonical production/render/audio code; no renderer duplication.
- Five-grammar families use six 30s chapters with a deterministic encore. Invisible Forces uses 25/25/25/25/25/25/30 seconds across all seven grammars.


## Regression hygiene extension
- Production schedule and subtype coverage focused tests now have a single terminal result.
- The aggregate runner rejects explicit suite FAIL markers even when a legacy suite exits with code 0.

## Seed allocation extension
- One-family bulk and 5x5 production now use the same stratified spread allocator as weekly/monthly production.
- Monthly manifest records global seed spacing metadata.

## Long-form production
- Long-form composer accepts ordinary base seeds while deriving separated segment seeds.
- Five-family long-form bulk remains composition, not a new renderer/runtime mode.

## Historical compatibility
- Old 18-second documents remain immutable history; active production/review uses the 20..30-second policy.
