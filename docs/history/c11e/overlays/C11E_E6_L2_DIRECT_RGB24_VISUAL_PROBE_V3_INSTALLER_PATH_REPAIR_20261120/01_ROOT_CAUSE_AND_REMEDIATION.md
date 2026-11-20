# E6 L2 Direct RGB24 Visual Probe V3 — V2 installer failure

## Operator result

V2 completed PS 5.1 AST, package/member/destination checks, immutable C11-C/D4.8 pins, 20 source pins and ADD_ONLY preflight. It then failed writing the receipt sidecar temporary file. The exception was `DirectoryNotFoundException` at `WriteAllText($sideTmp,...)`. The subsequent focused-test directory and V2 runner were absent, so no Godot capture process ran under V2.

## Root cause

V2 built the sidecar temporary path by appending `.tmp.` plus a 32-character GUID to the final sidecar path. The final sidecar path was 226 characters. The temporary path therefore became 263 characters, beyond the classic .NET Framework/Windows path limit used by Windows PowerShell 5.1. .NET surfaced the failure as `DirectoryNotFoundException`; the parent receipt directory itself was not the underlying issue.

## Transaction result

V2's catch block is designed to remove only transaction-owned files whose hashes still match their package postimages, remove temporary/partial receipt files, and remove transaction-created empty directories. The target checkout should still be checked for unexpected leftovers before the next transaction. V3 installs to new versioned destinations and does not overwrite V1/V2 artifacts.
