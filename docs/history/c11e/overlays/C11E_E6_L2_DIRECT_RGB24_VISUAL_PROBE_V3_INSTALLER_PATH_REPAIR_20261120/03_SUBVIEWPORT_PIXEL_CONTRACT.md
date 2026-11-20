# V3 installation transaction order

1. Parse the installer using Windows PowerShell 5.1 AST.
2. Verify ZIP sidecar and exact package SHA-256.
3. Extract to a fresh system-temp staging directory; never extract over the active checkout.
4. Validate the exact member set, package manifest and every staged byte/hash.
5. Rehash frozen C11-C and D4.8 V2; verify all 20 source dependencies.
6. Preflight all 24 ADD_ONLY destinations and their temporary paths; reject any non-identical collision.
7. Generate a unique receipt ID and calculate final receipt, final sidecar, and short sibling temp paths. Reject path lengths over 240 before writes.
8. Create and verify the transaction's receipt directory, recording each newly created parent for rollback.
9. Write destination files using same-directory temporary paths, flush, rehash, and atomic move.
10. Verify all 24 destination postimages.
11. Write receipt and sidecar to short sibling temp files, parse/validate, and then atomically move both final artifacts.
12. On failure, remove only owned/hash-matching additions and created empty directories. Preserve all pre-existing files.
