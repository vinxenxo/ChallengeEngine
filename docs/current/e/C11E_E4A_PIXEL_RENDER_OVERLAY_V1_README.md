# C11-E E4A Pixel Render Overlay V1 — Apply and run

This is a minimal one-source replacement plus two new D-only Python files and add-only documentation. It is not an installer framework.

## Files and operations

- `tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd`: replace only if current SHA-256 is the exact source handoff preimage `8f8e4c9be6170d48319b62512a1e1cdb40c4f126563deb3546dfd302b080179e`; postimage `4cf2c754c9675ebb3952a292a21af71634102cf7d880f71a871ba7d7555ac6ed`.
- `tools/c11d/d9/c11e_e4a_challenge_pixel_review.py`: add-only, SHA-256 `939a12f369df9eaa0dbaf5b06b0635a0d4dc906e14fd7d5bdf9c12b3ec2b97a0`.
- `tools/c11d/d9/test_c11e_e4a_challenge_pixel_review.py`: add-only, SHA-256 `f6adf4a10a55af167d9ac255cbce0c49b521dc87897d0519c0e955650d642fa9`.
- The approved policy JSON is included for completeness; if V33 already installed it, exact hash match is `ALREADY_PRESENT`, not a replacement.
- Six versioned E4A documentation/prompt files are add-only.

The ZIP manifest contains every target path, expected preimage/postimage and source/authority pin. The apply block in the accompanying response extracts to `%TEMP%`, validates the manifest and C11-C frozen manifest, then copies only these listed files. It stops on unknown preimage or an add-only destination conflict.

## Execution

Run from the active checkout with Python 3.13 and Godot 4.7.1 Mono. The driver runs the 23 focused tests and the actual opt-in Godot pixel fixture. It captures Python/Godot stdout/stderr and real exit codes. The runner writes evidence under `artifacts/tests/c11e/e4a_pixel_review/RUN_*`.

Expected bounded result: 18 PNGs at 540×960, 12 comparisons, D1.5 HEADER/FOOTER mapping, HOOK/CTA windows, empty suppression, language metadata-only, Challenge overlay blocked. It explicitly does **not** test gameplay body pixel identity or produce a gameplay MP4.
