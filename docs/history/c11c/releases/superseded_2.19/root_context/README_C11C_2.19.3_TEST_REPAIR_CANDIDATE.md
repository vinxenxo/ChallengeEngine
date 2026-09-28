# C11-C 2.19.3 — Test/Contract Repair Candidate

Base: `ChallengeEngineV01_STATELESS-C11-C2.19.2-FROZEN.zip`

This overlay repairs three regressions exposed by the first post-freeze full regression:

1. C11-A.1 factory isolation helper was absent from the runner packaged in 2.19.2.
2. The Visual Drill review runner default had drifted to 21s even though the canonical policy is 17s for non-Tracking families.
3. The Longform source-artifact test referenced `_assert()` without defining it.

It also restores the missing registered C11-A.1 contract test file.

This is a **candidate**, not a new freeze. Freeze again only after the user workstation reports all suites PASS.
