# C11-E E0 restart package V1 review incident (2026-10-30)

The first E0 restart package V1 correctly preflighted three V9 archive destinations but omitted the copy operation that was supposed to preserve the exact pre-E instruction files before replacing them. The omission was found by source review before the user applied that package. V1 is superseded and must not be applied.

V2 adds an explicit archive plan. Before any write, it resolves and validates all archive destinations, rejects directories/reparse points/hash collisions, and checks source preimages. It then copies exact V9 bytes atomically, verifies each archived SHA-256 and records all three archives in the E0 receipt before applying replacement payloads. If any archive or overlay preflight fails, no overlay payload write begins.

The V1 package should be retained as a historical rejected artifact, not used. This incident is recorded to prevent repetition: an installer is not accepted merely because it checks a destination; every stated preservation operation must exist in its write path and in its receipt.
