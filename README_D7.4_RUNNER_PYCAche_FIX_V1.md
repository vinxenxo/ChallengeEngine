# C11-D D7.4 Runner PYTHONBYTECODE Fix V1

This overlay changes only the D7.4 runner.

It preserves the existing D7.4 functional checks and the D7.2 receipt-field repair, and adds:

- `PYTHONDONTWRITEBYTECODE=1` for the runner process;
- no mutation of Python `__pycache__` files during the mutation-guarded execution.

The mutation guard remains strict for all repository files outside `artifacts/tests/c11d_d7/d7_4/`.
