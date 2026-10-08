# C11-D D7.2 Authority Fix V1

Incremental overlay for D7.2.

Fixes the authority-layer mismatch between the real D7.1 matrix object and the D7.2 coverage policy.

The validator now requires BOTH:

- matrix.authority == `D7.1`
- matrix.authority_state.matrix_authority == `CANONICAL_D7_1`

A tampered authority such as `D7.0` is still rejected.

No runner, policy, D7.1 source, D6, D5, D4, runtime, or production files are modified.
