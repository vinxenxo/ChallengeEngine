# Installer transaction design

The installer is PowerShell 5.1 AST-checked, self-hash-independent, and validates the package ZIP hash, full member manifest, each member byte count/SHA-256, C11-C frozen manifest, D4.8 V2 pin, and all 24 destination preimages before the first write.

All destinations are ADD_ONLY. An existing byte-identical file is skipped; an existing non-identical file blocks the whole transaction. Each new destination is written to a unique same-directory temporary file, flushed and rehashed, then atomically moved into place. Postimages are rehashed. On failure, rollback deletes only files created by this installer and only when their bytes still match the package postimage. Historical receipts are never changed.

The installer reads ZIP destinations directly from the temporary extraction root (no synthetic `payload\` prefix), then creates its own receipt and sidecar under a unique artifact directory. It does not run the Python tests or the visual probe. The operator runs the 28 focused manifest tests and then invokes the one-shot runner separately.
