# C11-D D6.5 Acceptance Repair V4

Fixes a semantic type mismatch in the D6.2 derivation gates consumed by D6.5.

The real D6.2 receipt may encode:
- derivation_capability = true
- derivation_runtime_activation = false

D6.5 now accepts these boolean forms as the governed equivalents of AVAILABLE/DISABLED.

Also emits failed_core_checks diagnostics when the acceptance is blocked, without changing predecessor artifacts.

Overlay is root-relative and modifies only:
`tools/c11d/d6/full_d6_acceptance.py`
