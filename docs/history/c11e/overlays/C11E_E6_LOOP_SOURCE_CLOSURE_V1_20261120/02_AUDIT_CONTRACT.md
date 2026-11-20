# Read-only audit contract

The runner validates fixed evidence SHA-256/byte pins and their sidecars; checks R1V and Loop22 report/process links; checks human closeout records; validates the six exact Smoke18 selector rows against their R1P receipts; rehashes selected current source files; and verifies frame inventory/PTS/pixel manifest contracts.

The report distinguishes: `PASS_REHASHED` media, `PENDING_MEDIA_NOT_PRESENT_IN_CHECKOUT`, and blocking mismatches. It must never convert absence to PASS. It records source frame identity and dimensions, not a D renderer input.

L2 is not ready: no materialized RGB24 bytes, no approved color conversion, no approved visual resampler decision, and no successor D4.8 authorization/manifest.
