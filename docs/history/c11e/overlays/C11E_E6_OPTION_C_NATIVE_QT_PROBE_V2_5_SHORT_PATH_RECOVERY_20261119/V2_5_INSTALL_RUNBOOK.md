# V2.5 short-path recovery — install and run

## Why this revision exists

V2.4's ZIP is structurally valid, but the operator extracted it under a long `Downloads` directory. The longest ZIP member is 175 characters; the resulting absolute extraction path reached 276 characters and `Expand-Archive` failed before the installer was invoked. V2.4 also used a long internal staging prefix and appended GUID temporary names to full destination filenames. V2.5 fixes outer extraction, internal staging and destination temporary paths. It retains V2.4 A3/Python payload bytes unchanged.

## Verify and extract to a short path (Windows PowerShell 5.1)

Do **not** extract to the long V2.4 directory under Downloads. The following block verifies the ZIP and preflights every absolute extraction path before `Expand-Archive` can write anything.

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Downloads = Join-Path $env:USERPROFILE 'Downloads'
$PackageZip = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_5_SHORT_PATH_RECOVERY.zip'
$Sidecar = "$PackageZip.sha256"
$PackageRoot = Join-Path $env:TEMP 'c11e25'

if (Test-Path -LiteralPath $PackageRoot) { throw "USE_FRESH_PACKAGE_DIRECTORY:$PackageRoot" }
$ExpectedSha = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualSha = (Get-FileHash -LiteralPath $PackageZip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha -ne $ExpectedSha) { throw "PACKAGE_SHA256_MISMATCH:$ActualSha" }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::OpenRead($PackageZip)
try {
    $maxExtractPath = 0
    foreach ($entry in $zip.Entries) {
        $target = Join-Path $PackageRoot ($entry.FullName.Replace('/', [IO.Path]::DirectorySeparatorChar))
        if ($target.Length -gt 230) { throw "OUTER_EXTRACTION_PATH_BUDGET_EXCEEDED:$($target.Length):$target" }
        if ($target.Length -gt $maxExtractPath) { $maxExtractPath = $target.Length }
    }
}
finally { $zip.Dispose() }
Write-Host ("OUTER_EXTRACTION_PATH_BUDGET=PASS; MAX=230; ACTUAL={0}" -f $maxExtractPath)

Expand-Archive -LiteralPath $PackageZip -DestinationPath $PackageRoot
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_5_SHORT_PATH_RECOVERY.ps1'
if (-not (Test-Path -LiteralPath $Installer -PathType Leaf)) { throw 'V2_5_INSTALLER_MISSING_AFTER_EXTRACT' }

& (Join-Path $PSHOME 'powershell.exe') `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File $Installer `
    -ProjectRoot $ProjectRoot `
    -PackageZip $PackageZip `
    -ExpectedPackageZipSha256 $ExpectedSha

$InstallExit = $LASTEXITCODE
if ($InstallExit -ne 0) { throw "E6_OPTION_C_QT_V2_5_INSTALL_BLOCKED:$InstallExit; preserve output and receipt" }
```

Expected installer signals include:

```text
POWERSHELL_5_1_AST_PARSE=PASS/INSTALLER
FROZEN_C11C_MANIFEST=PASS
D4_8_V2=PASS/UNCHANGED
INSTALL_STAGE_PATH_BUDGET=PASS; MAX=250; ACTUAL=<value>
PACKAGE_MEMBERS=20/20 PASS
INSTALL_WRITE_PATH_BUDGET=PASS; DEST_MAX=<value>; TEMP_MAX=<value>
INSTALL_STATUS=PASS_ADD_ONLY
INSTALL_FILES=18/18 VERIFIED
```

`ADD` and `SKIP_IDENTICAL` are computed from the live checkout. The installer performs full collision preflight before any destination write and never overwrites a mismatch.

## Run the V2.4 focused tests and native Qt probe

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$TestDir = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_4\tests'
$PreviousProjectRoot = $env:C11E_PROJECT_ROOT
try {
    $env:C11E_PROJECT_ROOT = $ProjectRoot
    & $PythonExe -m unittest discover -s $TestDir -p 'test_*.py' -v
    $TestExit = $LASTEXITCODE
}
finally {
    if ($null -eq $PreviousProjectRoot) { Remove-Item Env:\C11E_PROJECT_ROOT -ErrorAction SilentlyContinue }
    else { $env:C11E_PROJECT_ROOT = $PreviousProjectRoot }
}
if ($TestExit -ne 0) { throw "V2_4_REGRESSION_TESTS_BLOCKED:$TestExit" }

$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_4\RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4.py'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'V2_4_RUNNER_MISSING_AFTER_INSTALL' }
& $PythonExe $Runner --project-root $ProjectRoot --iterations 7
$RunnerExit = $LASTEXITCODE
if ($RunnerExit -ne 0) { throw "OPTION_C_NATIVE_QT_PROBE_V2_4_BLOCKED:$RunnerExit; preserve receipt and sidecar" }
```

Do not rerun V2.1/V2.2/V2.3. Preserve all historical receipts. The 17 V2.4 tests are the A3/source and path-loader focused suite; the runner then executes the already-installed 37 QImage target tests and seven benchmark iterations only after all preflights pass.

## Acceptance and next gates

- QImage stage: A3 source/lineage pass, source closure pass, 37/37 QImage, native P95 <=33.333 ms.
- Visual review: inspect all three synthetic preview images and the actual resampling result. Geometry approval is not resampler approval. No automatic promotion from this runner.
- Source closure: pin the exact existing C frame source/ordered stream, exact RGB24 bytes, dimensions/stride/colour contract, selector identity and D9.9/D9.10/R1P metadata. Do not invent a decoder or infer a source path.
- L2: after a separately approved successor policy and exact TEST_ONLY execution manifest, one copied real frame only at the existing D seam; original C source stays read-only.
- L3: negative controls, pixel/geometry proof and human review.
- L4: only then widen the same consumer to six Loop selectors; do not start Smoke18 media before its separate authorization.

No Godot/FFmpeg/FFprobe/audio/mux/renderer/dispatch. E6 remains accepted 0; D4.8 V2 remains blocked and unchanged; `release_authority=NONE`.
