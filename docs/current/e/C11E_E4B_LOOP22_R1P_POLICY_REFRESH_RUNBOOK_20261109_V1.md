# E4B Loop22 R1P Projection / Policy Fingerprint Refresh — V1

## Purpose

A bounded read-only stage between the accepted R1V pilot and any D-only Loop consumer or 44-output A/V execution. It reconciles the accepted 27 R1P receipts to the active 22-selector complement and captures the five current policy hashes from the active checkout.

## Exact inputs

- Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
- Frozen C11-C manifest: SHA-256 `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953`, 796,318 bytes.
- V7 installer receipt: SHA-256 `917ea340f345956c40e0fa9e60ba9be2721ca920b8cee867ceffe4bdbca3e15b`.
- R1V closeout receipt: SHA-256 `a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a`.
- Active-source audit report: SHA-256 `3d5102aa7eca0a4eb50d2532f66459823446855c4ab6c62ae4fccd1e2f817667`.
- R1P archive: SHA-256 `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52`, CRC clean.

## What it proves

1. Canonical R1P report self-hash and sidecar are valid.
2. All 27 receipts have valid canonical `receipt_sha256` and sidecar; the aggregate receipt-hash-set value matches.
3. Source manifest contains exactly 30 pins; all 30 resolve and hash/size-match the active checkout.
4. The 27 rows split into the five accepted pilot selector identities plus precisely 22 remaining selectors; every planned profile, pair of seeds, cycle count, duration, FPS and frame count matches the active V7 source audit.
5. Request identities are present, `request.seed` and `request.music_seed` remain separate, and R1P did not instantiate prototype nodes or produce renderer-native payload/media.
6. Five current proposal fingerprints (A.1/A.3/E4B_LOOP/B.1/D.1) are taken directly from active source bytes.

## Policy decision semantics

The generated docket uses current SHA values and requires a decision plus explicit full-hash confirmation for each proposal. The broad instruction to continue does not count as approval of any policy fingerprint.

Visual consumer implementation gate: A.1 + A.3 + E4B_LOOP.
A/V delivery gate: B.1 + D.1.

After decisions are recorded in a D-owned, versioned record and covered by focused positive/negative tests, a separate scoped implementation amendment can be prepared. A distinct AV execution amendment is required before any captures/audio/mux for the 22 selectors.

## Outputs and safety

Only creates a new folder under `artifacts/tests/c11e/e4b_loop22_r1p_policy_refresh/`. No existing evidence or source is changed. No Git, Godot, launchers, tests other than the eight new focused tests, music, FFmpeg/FFprobe, renderer, dispatch or media.
