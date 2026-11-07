# E4B R1V Actual Frame Inventory — V7

R1V is operator-authorized within the bounded scope but remains NOT RUN. V2/V3 installer and wrapper failures occurred before any launcher; they produced no R1V media.

V4 separates responsibilities to remove redundant preflight: the installer performs PowerShell-only checks/copy and never invokes Python; wrapper V3 resolves direct Python 3.13 and runs the 32-test active-checkout suite once before capture. Do not run the test file separately.

After the single wrapper preflight passes, it performs ten source launches (five selectors A/B) and records: MP4 SHA, read-only FFprobe metadata, decoded frame order/PTS, dimensions/pixel format, per-frame pixel SHA-256, deterministic A/B comparison, source/runtime pins and stdout/stderr hashes. FFmpeg decode streams raw pixels to an in-memory hasher; no derived video is written. No AVI retention, GIF, audio, D composition, filters, D3 or mux.

Technical capture PASS is not visual acceptance. Operator visual review is required before expanding to the remaining 22 selectors.
