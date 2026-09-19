[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
$tests = @(
    "tests/C11B0UnifiedSocialFrameContractTest.gd",
    "tests/C11B02PresentationFramingContractTest.gd",
    "tests/C11B1SocialUIIntegrationContractTest.gd"
)
foreach ($test in $tests) {
    Write-Host "[C11FREEZE] $test"
    godot --headless --path . -s .\$test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "[C11FREEZE] C11 contract suite PASS"
