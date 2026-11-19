# C11-E E6 Option C Native Qt Probe V2.5 — extraction and staging path repair

Date: 2026-11-19  
Mode: `ADD_ONLY`; the V2.4 A3 adjudicator, runner, reference producer, tests and V2.4 documentation are retained byte-for-byte.

## Incident: V2.4 never reached its installer

The operator's V2.4 transcript shows `Expand-Archive` failed with `DirectoryNotFoundException` while extracting a deeply nested documentation member. The chosen extraction root was:

`C:\Users\vinxe\Downloads\C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4_A3_LEGACY_FIELD_CONTRACT_FIX_20261119`

The longest V2.4 ZIP member path is 175 characters. Combining that member with the selected root produced a 276-character path. Windows PowerShell 5.1's `Expand-Archive` / .NET Framework extraction path could not create it. Because extraction failed, the subsequent `-File` invocation pointed to an installer that was not present. The resulting process exit `-196608` is downstream of the absent script; it is not evidence that the V2.4 installer body ran or that its transaction failed.

No V2.4 install receipt was emitted. The safe state classification is `V2_4_INSTALLER_NOT_INVOKED_EXTRACTION_FAILED`; do not infer a checkout rollback or partial V2.4 install from this transcript. The V2.4 package SHA remains the pinned reference `cd79f09cf4d9304cad1b555a7772b0f031c3f07d8c9c02d65d7f2da12e82f860`.

## Second latent path defect found by source review

Even if V2.4 were extracted to a short root, its internal staging directory used a long fixed prefix plus a 32-character GUID. With the operator's `%TEMP%` root and the 175-character package member, this could also exceed the legacy path budget. Its destination `.partial.<GUID>` temporary name was appended to the full destination filename, which could exceed the limit for the longest documentation destination.

V2.5 corrects all three path domains before any destination write:

1. **Outer package extraction:** the runbook uses `%TEMP%\c11e25` and measures every expanded path before calling `Expand-Archive`; it refuses extraction if any path exceeds 230 characters.
2. **Installer staging:** the staging directory uses a one-character prefix plus GUID, and the installer calculates the maximum full staging path from every manifest member. It blocks above 250 characters before creating the stage or writing destinations.
3. **Destination write temporaries:** a short `.q<GUID>.tmp` filename is created in the destination's own parent directory, preserving same-volume atomic `File.Move`. Every final and temporary path is budget-checked during the complete preflight, before the first destination write.

The receipt directory and receipt/sidecar `CreateNew` + `Flush(true)` + no-overwrite `File.Move` contract from V2.4 remains intact. Rollback still removes only exact SHA-256-matching postimages owned by the current invocation.

## Payload and adjudicator preservation

The V2.4 A3 V4 adjudicator, original diagnostic generator reference, runner, and 17 focused tests are byte-identical to the V2.4 package. The original producer source remains pinned at `90375a6c21550d67e6aa1f374d5e5c8dcd7c06b630c51b34ad83313fbb7b2fc2`; the adjudicator continues to enforce the field-specific A3 source contract and the exact single-pointer reconstruction. The already-installed V2 QImage payload and 37-test target suite are reused by exact path; they are not repackaged or replaced.

## Installation outcome expected

V2.5 installs the same 11 V2.4 destinations plus seven new V2.5 incident/runbook/ledger/prompt/next-phase-plan documents. Total planned destinations: 18. Existing exact postimages are `SKIP_IDENTICAL`; conflicting postimages block before writes. No file is overwritten.

## Current gate / next phase

The V2.4 Qt runner has still not executed. After successful V2.5 installation:

1. Run the 17 V2.4 focused regressions once.
2. Run the V2.4 runner once under Python 3.13.14 / PySide6 6.11.2 with seven iterations.
3. Require A3 PASS, source closure PASS, QImage 37/37, and P95 <= 33.333 ms.
4. Inspect all three synthetic previews. Geometry approval (720x1280 canvas; 504x896 body at (108,192); black reserved bands/gutters) does not approve resampler quality. The operator must explicitly accept or decline the resampler.
5. Only after that synthetic gate and read-only source closure can a separate scoped successor D4.8 policy and exact E6 TEST_ONLY execution manifest be proposed. A one-selector copied-frame proof is the next L2/L3 gate, followed by six Loop selectors at L4. No Smoke18 media run is implied.

No Godot, FFmpeg, FFprobe, audio, mux, renderer, production dispatch, BatchId or E6 acceptance is enabled. C11-C and D4.8 V2 remain unchanged; `e6_accepted=0`; `release_authority=NONE`.
