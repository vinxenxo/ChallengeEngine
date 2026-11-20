# L3 V1 — source immutability and output transaction

The runner verifies C11-C and D4.8 pins, the self-pinned L3 source manifest (16 evidence rows), all 20 nested V5 source pins and the QImage module, and all V4/V5 receipts, four exact sidecars and pixel artifacts before and after the audit. The V4 and V5 install receipts must each prove 24/24 ADD_ONLY with frozen C11-C/D4.8 pins and no source mutation. It writes only a new unique L3 report/receipt directory.

The installer is ADD_ONLY: 24 declared destinations, complete package-member verification, full collision preflight before writes, PowerShell 5.1 AST validation, short same-directory temp files, postimage SHA/byte verification and rollback limited to transaction-owned postimages.
