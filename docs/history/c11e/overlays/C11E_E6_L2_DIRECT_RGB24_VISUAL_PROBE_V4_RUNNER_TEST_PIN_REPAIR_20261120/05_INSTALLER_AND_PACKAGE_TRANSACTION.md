# V4 installer/package transaction

V4 inherits V3's short sibling receipt temp paths, pre-created receipt directory, <=240 path budgets, 29-member ZIP inventory, all-hash preflight, 24 ADD_ONLY postimages and transaction-owned rollback. The V4 package/installer is a fresh versioned artifact; it does not reinstall, overwrite or remove V3 destinations.

The focused tests consume the extracted root-member installer by explicit environment path. This is not a reason to add the installer itself as a repository destination. PS 5.1 AST and package SHA validation remain installer responsibilities and run before any write.
