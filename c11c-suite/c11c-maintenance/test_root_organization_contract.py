from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'c11c-suite' / 'c11c-maintenance' / 'organize_repository_root.ps1'
BAT = ROOT / 'c11c-suite' / 'c11c-maintenance' / 'organize_repository_root.bat'
MAIN = ROOT / 'c11c-suite' / 'c11c-maintenance' / 'main.py'

assert SCRIPT.exists()
assert BAT.exists()
text = SCRIPT.read_text(encoding='utf-8-sig')
assert '[switch]$Apply' in text
assert "project.godot" in text and "untouched_roots" in text
assert "build_factory.py" in text and "release_gate.py" in text
assert "GeneradorMaestro.gd" in text and "Main.tscn" in text
assert 'c11c-suite/c11c-maintenance/organize_repository_root.ps1' in MAIN.read_text(encoding='utf-8-sig') or 'root_organize_dry' in MAIN.read_text(encoding='utf-8-sig')
print('C11C_ROOT_ORGANIZATION_CONTRACT PASS')
