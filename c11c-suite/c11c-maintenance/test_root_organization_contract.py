from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'c11c-suite' / 'c11c-maintenance' / 'organize_repository_root.ps1'
BAT = ROOT / 'c11c-suite' / 'c11c-maintenance' / 'organize_repository_root.bat'
MAIN = ROOT / 'c11c-suite' / 'c11c-maintenance' / 'main.py'

assert SCRIPT.exists()
assert BAT.exists()
text = SCRIPT.read_text(encoding='utf-8-sig')
assert '[switch]$Apply' in text
assert 'root_conflicts' in text
assert "CHANGELOG_C11-C_2.19.12.md" in text and "root_changelogs/CHANGELOG_C11-C_2.19.12.md" in text
assert 'ARCHIVED_CONFLICT' in text
assert 'WOULD_ARCHIVE_CONFLICT' in text
assert "project.godot" in text and "untouched_roots" in text
assert "build_factory.py" in text and "release_gate.py" in text
assert "GeneradorMaestro.gd" in text and "Main.tscn" in text
main_text = MAIN.read_text(encoding='utf-8-sig')
assert 'root_organize_dry' in main_text
assert 'root_organize_apply' in main_text
assert 'create_c11c_freeze_zip.ps1' in main_text
assert 'FREEZE C11-C · DRY RUN' in main_text
assert 'clean_c11c_artifacts.ps1' in main_text
assert 'run_freeze_package.bat' in (ROOT / 'c11c-suite' / 'c11c-maintenance' / 'run_freeze_package.bat').read_text(encoding='utf-8-sig') or (ROOT / 'c11c-suite' / 'c11c-maintenance' / 'run_freeze_package.bat').exists()
print('C11C_ROOT_ORGANIZATION_CONTRACT PASS')
