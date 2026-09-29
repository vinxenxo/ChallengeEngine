from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIRS = [ROOT / "c11c-suite", ROOT / "tools" / "qa" / "c11", ROOT / "tools" / "prototypes" / "c11c_bulk"]
EXCLUDED_PARTS = {"c11c-studio", ".godot", "__pycache__"}


def collect_scripts() -> list[Path]:
    return sorted(
        {
            p
            for base in TARGET_DIRS
            if base.exists()
            for p in base.rglob("*.ps1")
            if not EXCLUDED_PARTS.intersection(p.parts)
        }
    )


def parse_one(path: Path) -> tuple[bool, str]:
    # PowerShell 5.1 does not bind parameters placed after a -Command string
    # the way this audit runner previously assumed. The old form therefore
    # handed an empty path to Parser.ParseFile and produced a false FAIL for
    # every script. Pass the target through an environment variable instead.
    command = r'''$Path = $env:C11C_PARSE_TARGET
if([string]::IsNullOrWhiteSpace($Path)){ Write-Error 'C11C_PARSE_TARGET is empty'; exit 2 }
$tokens=$null
$errors=$null
try {
    [System.Management.Automation.Language.Parser]::ParseFile($Path,[ref]$tokens,[ref]$errors)|Out-Null
} catch {
    Write-Error $_.Exception.Message
    exit 2
}
if($errors.Count -eq 0){ exit 0 }
$errors|ForEach-Object{$_.Message}
exit 1
'''
    env = os.environ.copy()
    env["C11C_PARSE_TARGET"] = str(path.resolve())
    try:
        cp = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                command,
            ],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return False, "powershell.exe not found"
    detail = (cp.stdout + cp.stderr).strip()
    return cp.returncode == 0, detail


def main() -> int:
    scripts = collect_scripts()
    failures = []
    for path in scripts:
        ok, detail = parse_one(path)
        if not ok:
            failures.append((path, detail))
    if failures:
        print(f"C11C_POWERSHELL_PARSE_AUDIT FAIL - {len(failures)} script(s)")
        for path, detail in failures:
            print(f" - {path.relative_to(ROOT)}")
            if detail:
                print(detail)
        return 1
    print(f"C11C_POWERSHELL_PARSE_AUDIT PASS - {len(scripts)} script(s) parsed by Windows PowerShell")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
