$ErrorActionPreference = 'Stop'
$path = Join-Path $PSScriptRoot '..\..\core\presentation\rendering\PeripheralScanRenderer.gd'
$path = [System.IO.Path]::GetFullPath($path)
if (-not (Test-Path -LiteralPath $path)) { throw "PeripheralScanRenderer.gd not found: $path" }
$content = Get-Content -LiteralPath $path -Raw
if ($content -match '(?m)^var _environment\s*:') {
    Write-Host '[C11C 2.9.1] _environment already declared; no change needed.'
    exit 0
}
$needle = 'var _frame_state: Dictionary = {}'
if (-not $content.Contains($needle)) { throw 'Expected insertion anchor not found.' }
$content = $content.Replace($needle, "$needle`r`nvar _environment: Node2D = Node2D.new()")
Set-Content -LiteralPath $path -Value $content -NoNewline
Write-Host '[C11C 2.9.1] _environment declaration inserted.'
