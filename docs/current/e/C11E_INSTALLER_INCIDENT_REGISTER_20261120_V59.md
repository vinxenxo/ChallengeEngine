# C11-E installer and audit incident register — V59

## Closed
- V1 L1 reconciliation false negative: four historic records had matching SHA-256 but `expected_bytes=null`; V2 changed byte length to optional only when undeclared while keeping SHA mandatory. V2 audit passed 18/18.
- L1 docs V3: PS 5.1 AST PASS; 16/16 ADD_ONLY destinations verified.

## Active watch
- Loop source closure V1 is read-only. Missing source MP4 files are pending, never PASS. Any mismatch in SHA-256/bytes, selector identity, frame count, PTS, sidecar or source pins blocks.
- QImage RGB24 input not yet materialized from historical YUV420P; colorimetry not declared; do not infer conversion.

No incident permits weakening C11-C/D4.8 pins or enabling media execution.
