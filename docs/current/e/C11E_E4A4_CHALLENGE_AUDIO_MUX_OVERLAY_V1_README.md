# E4A.4 Challenge audio/mux overlay V1

This is an add-only overlay for the bounded E4A.4 A/V test. It adds one runner, one focused test module and versioned authority/roadmap/plan/prompt documents. It replaces no existing source file and does not modify E1, E3, D3 V5, C11-C or GUI code.

## Download and run

Save these files in `%USERPROFILE%\Downloads`:

- `C11E_E4A4_CHALLENGE_AUDIO_MUX_OVERLAY_V1.zip`
- `RUN_C11E_E4A4_FROM_DOWNLOADS_V1.ps1`

Then run once from PowerShell 5.1:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\RUN_C11E_E4A4_FROM_DOWNLOADS_V1.ps1"
```

The runner verifies package SHA/CRC, all live source pins and all destination states before copying. It applies only new files, skips only exact already-present postimages, runs 42 focused tests, then executes the E4A.4 A/V test with a finite timeout and heartbeat. Logs, test transcript, exit codes and hashes are retained under Documents. A failed test or source mismatch stops before D3 rendering.

The E4A.4 Python runner independently revalidates E4A.2/E4A.3 input evidence and all live E1/D9/D3/E3 pins. It creates fresh test-only output under `artifacts/tests/c11e/e4a_audio_mux_review`. It does not dispatch any production system or renderer.

## Expected final console markers

`E4A4_EVIDENCE_DIR=...`, `E4A4_RECEIPT_SHA256=...`, `E4A4_ZIP=...`, `E4A4_ZIP_SHA256=...`, and `C11E_E4A4_CHALLENGE_AUDIO_MUX=PASS_ISOLATED_TEST_ONLY`.

Upload the named run ZIP to the Library for independent inspection. The MP4s contain the unmodified normalized C11-C review video plus audio. They do not contain E4A.3 D-overlay pixels. Operator listening/synchronization review remains a separate acceptance item.
