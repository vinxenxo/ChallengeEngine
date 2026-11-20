# V2 audit semantic contract

## Immutable pin

C11-C manifest: `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953` / 796,318 bytes.
D4.8 V2: `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` / 12,996 bytes. D4.8 remains BLOCKED and unchanged.

## QImage V2.7 receipt

The auditor validates the actual schema, overall status, runtime, nested `qimage_tests`, benchmark, 23 source rows, A3 adjudication, three immutable synthetic fixtures and the no-execution governance envelope. A nested mapping is never compared with a scalar. Any missing, malformed, failed or over-budget field blocks.

## L1 reconciliation V2 receipt

The auditor validates schema/status and 18/18 totals, then independently confirms `phase_state.e6_accepted == 0` and `governance.e6_accepted == 0`. Top-level absence is not treated as a mismatch; a top-level convenience value cannot substitute for the two authoritative nested values. `no_execution_authority_created` must be true and the visual resampler state must remain pending.

## Result policy

Only false-negative schema access is corrected. No historical receipt, source pin, evidence hash, D4.8/C11-C artifact or gate is edited or waived. Pending evidence remains pending; real RGB24 buffers remain absent and L2 remains false.
