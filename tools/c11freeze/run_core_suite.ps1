[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
$tests = @(
    "tests/DeterministicLCGStatelessTest.gd",
    "tests/RNGArchitectureTest.gd",
    "tests/PilotMechanicIsolationTest.gd",
    "tests/PilotMechanicDDIHardeningTest.gd",
    "tests/ParkingMechanicV2IsolationTest.gd",
    "tests/mechanics/catch/CatchMechanicIsolationTest.gd",
    "tests/mechanics/catch/CatchPresentationContractTest.gd",
    "tests/mechanics/choose/ChooseMechanicIsolationTest.gd",
    "tests/mechanics/find/FindMechanicIsolationTest.gd",
    "tests/mechanics/hit/HitMechanicIsolationTest.gd"
)
foreach ($test in $tests) {
    Write-Host "[C11FREEZE][CORE] $test"
    godot --headless --path . -s .\$test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "[C11FREEZE] Core suite PASS"
