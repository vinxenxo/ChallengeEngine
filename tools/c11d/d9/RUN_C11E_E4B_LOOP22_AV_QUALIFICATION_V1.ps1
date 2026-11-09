[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$ProjectRoot,
 [string]$R1PArchive = "artifacts/tests/c11e/e4b_r1p/E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip"
)
$ErrorActionPreference = 'Stop'
$minimumPS = [version]'5.1'
if ($PSVersionTable.PSVersion -lt $minimumPS) { throw "Windows PowerShell 5.1 required; found $($PSVersionTable.PSVersion)" }
$root = [IO.Path]::GetFullPath($ProjectRoot)
$runner = Join-Path $root 'tools\c11d\d9\c11e_e4b_loop22_av_qualification_v1.py'
$tests = Join-Path $root 'tools\c11d\d9\test_c11e_e4b_loop22_av_qualification_v1.py'
foreach ($p in @($runner,$tests)) { if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Required Loop22 file missing: $p" } }
$py = Get-Command py.exe -ErrorAction SilentlyContinue
if ($null -eq $py) { throw 'py.exe launcher not found; install Python 3.13 and py.exe' }
$version = & $py.Source -3.13 -c "import sys; print('.'.join(map(str,sys.version_info[:3])))"
if ($LASTEXITCODE -ne 0 -or -not $version.StartsWith('3.13.')) { throw "Python 3.13 unavailable: $version" }
$python = & $py.Source -3.13 -c "import sys; print(sys.executable)"
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $python -PathType Leaf)) { throw 'Could not resolve Python 3.13 executable' }
$env:PATH = (Split-Path -Parent $python) + ';' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
# AST-parse only. No Python bytecode is emitted; no Git calls are made.
$astCode = "import ast,pathlib,sys; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8'),filename=p) for p in sys.argv[1:]]; print('AST_PARSE=PASS')"
$astOut = & $python -c $astCode $runner $tests
if ($LASTEXITCODE -ne 0 -or ($astOut -join "`n") -notmatch 'AST_PARSE=PASS') { throw "Python AST parse failed: $astOut" }
$archive = if ([IO.Path]::IsPathRooted($R1PArchive)) { $R1PArchive } else { Join-Path $root $R1PArchive }
$testOut = & $python $tests --project-root $root --r1p-recovered-zip $archive 2>&1
$testOut | ForEach-Object { Write-Host $_ }
if ($LASTEXITCODE -ne 0) { throw 'Loop22 focused tests failed; no media qualification was started' }
$match = [regex]::Match(($testOut -join "`n"), 'Ran\s+(\d+)\s+tests')
if (-not $match.Success -or [int]$match.Groups[1].Value -ne 24) { throw 'Loop22 focused test count mismatch; expected exactly 24' }
Write-Host 'LOOP22_FOCUSED_TESTS=PASS_24_OF_24'
Write-Host 'LOOP22_MEDIA_PRELAUNCH=STARTING_AFTER_PASS'
& $python $runner --project-root $root --r1p-recovered-zip $archive
if ($LASTEXITCODE -ne 0) { throw "Loop22 qualification runner failed with exit code $LASTEXITCODE" }
