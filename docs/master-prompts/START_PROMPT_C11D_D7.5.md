# START PROMPT — C11-D D7.5

Execute `D7.5 — Full D7 Acceptance` against the real repository.

Require D7.0, D7.1, D7.2, D7.3 and D7.4 PASS/CLOSED. Validate the canonical 90-case chain, authorities, identity/provenance, seed governance, D4.8 BLOCKED, runtime NONE, production false, renderer false, C11-C build hash, deterministic evidence and mutation guard.

Do not modify C11-C simulation, mechanics, RNG, presentation, renderer, or protected temporal semantics. Do not create or modify `release/`.

Run `tools/c11d/d7/run_d7_5_full_acceptance.ps1` twice. Close only after two clean PASS/CLOSED runs.
