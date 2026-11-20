# V3 installer regression coverage

The focused V3 suite retains the 62 V2 harness/policy tests and adds ten installer-specific regressions:

- Reproduce the V2 263-character sidecar-temp path.
- Prove the V3 short sidecar temp fits the 240-character budget.
- Require both receipt and sidecar temp files to use short sibling names.
- Enforce final and temp path budgets before payload writes.
- Require receipt directory creation before the first destination write.
- Require both temp files to be written/validated before final moves.
- Verify same-directory receipt/sidecar layout.
- Verify rollback is limited to exact transaction-owned hashes.
- Ensure V3 uses its own receipt root and does not reuse V2.
- Verify the policy/manifest remains the same one-frame TEST_ONLY scope.

The local builder must report 72/72 tests. Windows PowerShell 5.1 AST validation and Windows installation must still be performed on the target.
