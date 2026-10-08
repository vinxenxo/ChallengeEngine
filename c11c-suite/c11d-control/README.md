# C11-D Control Center — D9.5.0 foundation

This is the first integrated C11-D operator surface inside the canonical `c11c-suite`.

It does not duplicate the backend. It discovers D-state from receipts and launches canonical D runners through the same subprocess model already used by the Suite.

Current scope:
- D4–D9 status visibility;
- canonical runner access for D4–D9;
- governance visibility (`D4.8 BLOCKED`, `release_authority=NONE`, D10 gate);
- links to Test, Producer, Catalog, Maintenance and Config;
- explicit integration matrix showing what is already operable and what remains for native GUI completion.

D10 must remain blocked until the full D branch has passed real GUI acceptance.
