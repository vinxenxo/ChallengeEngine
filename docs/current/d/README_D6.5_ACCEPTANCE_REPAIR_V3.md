# D6.5 Acceptance Repair V3

Fixes a representation mismatch: D6.4 stores `d4_8_blocked` as boolean `true`, while D6.5 V2 compared it to the string `BLOCKED`. No functional source is changed.

Apply as a root-relative overlay over the current D6.5 V2 state. Run the existing D6.5 parser check and runner twice.
