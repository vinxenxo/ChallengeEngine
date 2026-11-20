# V3 receipt temp path repair

V3 keeps the final receipt and sidecar filenames unchanged in the versioned V3 receipt directory, but no longer derives temporary names by appending to those long final filenames.

- Receipt temp: `r.<32-hex-guid>.tmp` inside the receipt directory.
- Sidecar temp: `s.<32-hex-guid>.tmp` inside the same receipt directory.
- Final receipt and final sidecar each have a checked path budget of 240 characters.
- Both temporary paths are checked against the same budget before any payload writes.
- The directory is created and verified before the first payload destination is written.
- Both temp files are written and validated before final same-directory atomic moves.
- On any failure, rollback deletes only transaction-owned additions with exact matching SHA-256 postimages and then removes empty transaction-created directories.

The actual operator-reported V2 layout is covered by a regression test: 226-character final sidecar plus `.tmp.` and a 32-character GUID equals 263 characters.
