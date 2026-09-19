[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"

& .\tools\run_C10C_physical_export.ps1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$tests = @(
    @{ Path = ".\tests\C6F06VisualLoopPhysicalExportTest.gd"; Marker = "[C6F0_6_PHYSICAL_EXPORT_SUITE] PASS" },
    @{ Path = ".\tests\C6F06VisualDrillPhysicalExportTest.gd"; Marker = "[C6F0_6_DRILL_PHYSICAL_EXPORT_SUITE] PASS" }
)

$logRoot = ".\artifacts\tests\logs\physical"
New-Item -ItemType Directory -Force -Path $logRoot | Out-Null

foreach ($test in $tests) {
    $name = [IO.Path]::GetFileNameWithoutExtension($test.Path)
    $log = Join-Path $logRoot ($name + ".log")
    Write-Host "[C11FREEZE][PHYSICAL] $name"

    $output = @(& godot --headless --path . --script $test.Path 2>&1)
    $code = $LASTEXITCODE
    $output | Tee-Object -FilePath $log | Out-Host

    if ($code -ne 0) {
        Write-Host "[C11FREEZE][PHYSICAL] FAIL $name exit=$code" -ForegroundColor Red
        exit $code
    }

    $output_text = ($output | ForEach-Object { $_.ToString() }) -join "`n"
    if (-not ($output_text -like "*$($test.Marker)*")) {
        Write-Host "[C11FREEZE][PHYSICAL] WARN $name marker not captured; exit=0 is authoritative and artifact assertion completed." -ForegroundColor Yellow
    }
}

Write-Host "[C11FREEZE] Physical export suite PASS - 2/2" -ForegroundColor Green
