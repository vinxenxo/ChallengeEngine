# Build and target validation

Build validation verifies package inventory, all manifest member hashes, JSON parseability, Python syntax compilation, 28 focused tests, source pin cardinality, the exact C11-C/D4.8 immutable hashes, and package ZIP CRC.

This environment cannot execute Windows PowerShell 5.1 or the operator's pinned Godot executable. Therefore the package build does not claim target AST or Godot runtime PASS. Those checks occur on the Windows operator machine. The installer itself parses its AST under Windows PowerShell 5.1 before any write. The runner reports each Godot invocation, log hash, and exit code.
