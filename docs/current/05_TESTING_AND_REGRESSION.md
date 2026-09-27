# Testing and Regression — Current

## Mandatory gate

```powershell
python .\tests\run_all.py
```

Every discovered `*Test.gd` requires an explicit entry in `KNOWN_SUITES` and an explicit PASS marker. Missing registration is a fatal error.

When a suite fails, `run_all.py` re-runs that suite with `--verbose` and stores the complete diagnostic log in `artifacts/tests/logs/verbose/`.

## C11-C focused contracts

Run the focused C11-C tests when changing visual tooling, then run the full suite. Physical production success does not replace logical regression.

## Producer

`c11c-producer/self_test.py` validates Python syntax, schema alignment, backend hash compatibility and required launchers. Windows/Godot runtime validation remains the final proof.
