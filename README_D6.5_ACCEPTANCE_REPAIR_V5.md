# C11-D D6.5 Acceptance Repair V5

Fixes two semantic predecessor-gate mismatches in D6.5:

1. D6.1 canonical authority count now supports scalar counts and collection-shaped declarations; when the receipt does not declare a count in a supported scalar/collection form, the canonical D6.1 seed registry is used as the evidence-backed fallback.
2. D6.4 D4.8 blocked gate now consumes the actual D6.4 receipt shape (`d4_8_status=BLOCKED` / equivalent governed forms) and also requires no production execution and no physical authorization inference.

Also removes a duplicate helper definition that was overriding the corrected D4.8 gate.

No D6.0-D6.4 source is modified.
