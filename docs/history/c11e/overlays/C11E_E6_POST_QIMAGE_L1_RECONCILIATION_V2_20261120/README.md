# E6 post-QImage L1 reconciliation V2 — correction record

**Date:** 2026-11-20  
**Status before V2 execution:** correction prepared; V2 read-only audit must return 18/18 PASS.

## Root cause of V1 block

The V1 reconciliation reported `v2_7_qt_receipt` blocked because its active-source rehash compared `actual_bytes == expected_bytes` unconditionally. Four rows in the immutable V2.7 runner receipt declare `expected_bytes: null`, while their expected and actual SHA-256 values are identical. Those rows therefore failed only an inapplicable byte-count comparison.

## V2 correction

V2 requires the active file to exist, the source row status to be PASS and SHA-256 to match. If `expected_bytes` is an integer, the byte count must also match exactly. If `expected_bytes` is null, V2 records `NOT_DECLARED_SHA256_ONLY` and does not infer a value. Malformed non-null byte counts fail closed. The source check count remains exactly 23.

## Integrity and authority

No historical receipt, source file, C11-C manifest, D4.8 policy or V2.7 artifact is rewritten. The old V1 blocked receipt remains preserved as incident evidence. The V2 audit is read-only. E6 acceptance remains zero; renderer and media remain OFF; release authority remains NONE.
