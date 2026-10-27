# C11-D Editorial Payload Provenance Join — Checkpoint V3

Status: PREPARATION_ONLY_IN_MEMORY_PROVENANCE_JOIN_NOT_RENDERER_INPUT

## V3 correction

The integrated V2 runner rejected the corrected challenge payload hash before runtime materialization because EXPECTED_JOIN_OBSERVATIONS still contained the old challenge SHA-256. V3 updates the contract identity and the runner expected-observation table to the same SHA-256 reported by the in-memory Challenge harness.

## Exact challenge hash evidence

- Superseded expected value: `7fe2bcf47b7127ee44c6c9d3a9aeea5bf54fb78ca28ca09757a99058e86b4809`
- Observed runtime value: `7fe2bcf47b7127ee44c6c9d9a3a9eea5bf54fb78c28ca09757a99058e86b4809`
- V2 remains unchanged. Its contract SHA-256 is `9b22e8dcc8f3cc90d09d220a81f89f6daca2f8f0a708219ab2a04579e5525bca`.

## Preserved deterministic evidence

- Prior in-memory receipt SHA-256: `fac949ee4a0498016808e859bd325e68b77586fd7589cb6d744bf11e7fed7e3e`.
- Prior in-memory trace SHA-256: `5f6eee0a8c8fe7b9d9259354b1eb9f4dd64d9f367ccce00aea969ad76edc5c67`.
- The receipt remains in-memory only; no persistent receipt is written.

## Unresolved policy and execution boundary

- `effective_delivery_frame_count` remains unresolved.
- Editorial payload consumption remains not proven.
- Visibility windows remain unevaluated.
- `renderer=OFF`.
- `media_created=false`.
- `candidate_input_admissible=false`.
- `approved_bindings=0`.
- `D4.8=BLOCKED`.
- `D10=BLOCKED_FOR_PROMOTION`.
- `release_authority=NONE`.

This is a diagnostic version only. It does not authorize renderer-native input, media creation, delivery-timebase policy, visual field consumption, baseline promotion or release.
