# C11-E execution hygiene and assistant error log â€” V16

**Date:** 2026-11-01

## Incident: V9 runner retained a stale Python test source pin

The V19 repair updated `test_c11e_e2_challenge_pair.py` from SHA `36b6f296d17f72b51b96946953b1abc72e907f5823567fd8a9993ae5f4169342` to `ab4ed3fd421ef0cac86d4ef25167f0161a186ef5bd90373414abed7bea17d2a9` and executed the Python suite successfully (9/9). However, the V9 runner's `$ExpectedPairTestsSha` constant still referenced the old hash. Therefore a new physical run would have stopped at source-pin verification even though the Python test itself passed.

The V20 correction changes only that one constant in the runner. It checks the exact runner preimage SHA, exact Python postimage SHA, requires exactly one old pin occurrence, verifies the resulting runner SHA, re-runs the Python 9/9 suite and writes docs/receipt only after success.

## Failed physical attempts

R1 and R2 each stopped before rendering at Python test 09, which contained a stale source-layout assertion. The corrected test now validates scene inheritance, delegation to the shared validator, semantic-separation enforcement in the helper and the `editorial.title` label source. Both attempts have zero renderer invocations and no media. The repair receipt's suggested next ID `R2` was stale after R2 had already run; use R3.

## Hard execution rules

- Never print PASS markers after `throw`, a failed read, missing JSON or an undefined variable.
- Stop on the first nonzero process exit. Do not keep running a manually pasted tail of a failed script.
- Always match the runner's internal source pins to the current source postimages. A passing test file is not enough if the runner still pins its preimage.
- Use a unique request ID per attempt. R1/R2 are consumed; use R3.
- Keep installation, source/test repair, physical renderer acceptance, human review and release authority as distinct decisions.
- No new installer/ZIP for this one-line runner pin change; exact-hash guarded in-place edit with backup and rollback.

E2 remains no-audio, release authority NONE, baseline promotion false. C11-C protected sources and frozen manifest remain unchanged.