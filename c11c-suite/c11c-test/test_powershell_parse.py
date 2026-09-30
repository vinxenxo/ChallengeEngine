from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXCLUDED_PARTS = {
    ".git", ".godot", ".mono", ".import", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".venv", "venv", "env", "artifacts",
    "legacy", "history"
}


def active_powershell_scripts() -> list[Path]:
    candidates = []
    for path in ROOT.glob("*.ps1"):
        if path.name == "FULL_ACCEPTANCE_C11C_2.19.12_A1_SINGLE.ps1":
            continue
        candidates.append(path)
    for path in ROOT.rglob("run_*.ps1"):
        rel_parts = set(path.relative_to(ROOT).parts)
        if EXCLUDED_PARTS.intersection(rel_parts):
            continue
        candidates.append(path)
    unique = {path.resolve() for path in candidates}
    return sorted(unique)


def build_ps_command(paths: list[Path]) -> str:
    payload = ",".join("'" + str(p).replace("'", "''") + "'" for p in paths)
    return f"""$ErrorActionPreference = 'Stop'\n$paths = @({payload})\n$failed = @()\nforeach ($path in $paths) {{\n    $tokens = $null\n    $errors = $null\n    [System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$errors) | Out-Null\n    if ($errors.Count -gt 0) {{ $failed += $path }}\n}}\nif ($failed.Count -gt 0) {{\n    Write-Host ('C11C_POWERSHELL_PARSE_AUDIT FAIL - ' + ($failed -join '; '))\n    exit 1\n}}\nWrite-Host ('C11C_POWERSHELL_PARSE_AUDIT PASS - ' + $paths.Count + ' script(s) parsed by Windows PowerShell')\nexit 0\n"""


def main() -> int:
    paths = active_powershell_scripts()
    if not paths:
        print("C11C_POWERSHELL_PARSE_AUDIT FAIL - no active PowerShell scripts found")
        return 1
    try:
        proc = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", build_ps_command(paths)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        print(f"C11C_POWERSHELL_PARSE_AUDIT FAIL - Windows PowerShell unavailable: {exc}")
        return 1
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip(), file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
