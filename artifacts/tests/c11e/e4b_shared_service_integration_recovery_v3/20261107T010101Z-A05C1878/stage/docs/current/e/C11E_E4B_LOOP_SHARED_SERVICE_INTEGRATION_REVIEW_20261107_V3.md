# E4B Loop Shared Service Integration Review — V3

## V2 implementation

The V2 overlay contains six exact source postimages and fifteen add-only files. Its service change routes Loop family preparation through the existing shared E1 service; GUI and CLI retain one service boundary. The 25 service tests exercise the 27 canonical Loop grammars, parity, deterministic behavior, invalid/tampered input and governance controls. D9.8 is updated to distinguish D9.9 plan compatibility from D4 executable compatibility.

## V2 installation exception

The operator observed `ArgumentException: Los tipos de argumentos no coinciden` after `BACKUP_PATH_PREFLIGHT`. The V2 script performs staging, six backups, 15 add-only writes and six source patches inside a `try` block. It then constructs the receipt outside the transaction with direct `@()` conversion of `New-Object` generic lists. This matches the PowerShell 5.1 bug documented at issue #27558. Therefore the likely outcome is a complete install without an install receipt. V3 must confirm this from live hashes; it does not trust the console line alone.

## V3 acceptance

V3 recovery succeeds only after exact checks:
- six V2 source postimages;
- fifteen V2 add-only destination hashes and byte counts;
- six `b/01.bak` through `b/06.bak` backups matching V2 preimage hashes;
- C11-C frozen manifest;
- V3 tooling/docs add-only preflight.

V3 itself makes no production source changes. Its runner uses arrays rather than `@()` around `New-Object Generic.List[object]` and executes the 25 E service tests, D9.8 tests, Python 3.13 syntax compile and separate live diagnostics.

## Not yet accepted

No request-scoped payload has been rendered; no D-only pixel consumer is accepted; no visual or audio acceptance is claimed. E4B remains `PASS_TEST_ONLY_SHARED_SERVICE_PREPARATION` until the real consumer and downstream gates are completed.
