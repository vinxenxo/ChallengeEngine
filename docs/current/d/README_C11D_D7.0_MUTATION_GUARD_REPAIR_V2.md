# C11-D D7.0 Mutation Guard Repair V2

Fixes recursive discovery of D7.0's own generated evidence.

The D7.0 audit output tree:
`artifacts/tests/c11d_d7/d7_0/`

is now excluded both from repository snapshots and from token-based source discovery.

This keeps the first and second audit passes semantically identical while preserving the strict mutation guard outside the permitted evidence tree.
