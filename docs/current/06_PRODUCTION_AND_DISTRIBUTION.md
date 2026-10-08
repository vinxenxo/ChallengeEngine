# Production and Distribution — C11-D D7 FROZEN

C11-C production remains declarative and profile-driven. `c11c-suite` GUI operations delegate to the same canonical commands used from the command line; GUI/CLI parity is a transverse D invariant.

## D7 boundary

D7 defined a 90-case production matrix and catalog plus identity/provenance governance. It did **not** authorize production execution, renderer execution or release execution.

The current D7 governance locks are:

- D4.8 = `BLOCKED`.
- Runtime authority = `NONE`.
- Production execution = `false`.
- Renderer execution = `false`.
- `master_seed=NOT_ADOPTED`.
- Runtime seed derivation disabled.
- Automatic seed generation disabled.
- Cross-domain seed sharing `FORBIDDEN`.

## D8 boundary

D8 will define the media QA and release layer incrementally. Release staging/packaging must acquire explicit authority from its own contracts; it must not be inferred from D7.
