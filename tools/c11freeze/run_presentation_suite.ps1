[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
$tests = Get-ChildItem .\tests -Filter "C6*.gd" -File | Where-Object { $_.Name -notin @("C6F06VisualDrillPhysicalExportTest.gd", "C6F06VisualLoopPhysicalExportTest.gd") } | Sort-Object Name
foreach ($test in $tests) {
    Write-Host "[C11FREEZE][PRESENTATION] $($test.Name)"
    godot --headless --path . -s $test.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "[C11FREEZE] Presentation suite PASS"
