from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "tools" / "prototypes" / "c11c_bulk" / "clean_c11c_artifacts.ps1"
RESET = ROOT / "tools" / "prototypes" / "c11c_bulk" / "reset_c11c_artifacts.ps1"
FREEZE = ROOT / "tools" / "maintenance" / "create_c11c_freeze_zip.ps1"
BAT = ROOT / "c11c-suite" / "c11c-maintenance" / "run_freeze_package.bat"
CONSOLIDATOR = ROOT / "tools" / "maintenance" / "consolidate_c11c_2_19_documentation.ps1"
ORGANIZER = ROOT / "c11c-suite" / "c11c-maintenance" / "organize_repository_root.ps1"

clean = CLEAN.read_text(encoding="utf-8-sig")
reset = RESET.read_text(encoding="utf-8-sig")
freeze = FREEZE.read_text(encoding="utf-8-sig")
bat = BAT.read_text(encoding="utf-8-sig")
obsolete_gui_tree = "c11c-" + "studio"

for name in (
    "c11c_geometric_waves_v1",
    "c11c_fractal_bloom_v1",
    "c11c_sacred_symmetry_v1",
    "c11c_living_particles_v1",
    "c11c_invisible_forces_v1",
    "c11c_bulk_multiseed",
):
    assert name in clean
for name in ("legacy", "qa", "regression", "releases", "production", "tests"):
    assert name in clean
for ext in (".mp4", ".gif", ".avi", ".wav", ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".mov", ".mkv", ".webm"):
    assert ext in clean

assert "explicit destructive C11-C reset" in reset
assert "-Recurse -Force" in reset

for token in ("'artifacts'", "'c11c-maintenace'", "'__pycache__'", "'*.pyc'", "'*.zip'", "C11-C-FROZEN-PACKAGE-V2"):
    assert token in freeze, token
assert "'" + obsolete_gui_tree + "'" in freeze
assert "[switch]$DryRun" in freeze

consolidator_bytes = CONSOLIDATOR.read_bytes()
assert not consolidator_bytes.startswith(b'\xef\xbb\xbf\xef\xbb\xbf'), 'Documentation consolidator must not contain a duplicate UTF-8 BOM.'
assert 'if(-not $DryRun)' in CONSOLIDATOR.read_text(encoding='utf-8-sig')
assert 'WOULD_ARCHIVE_CONFLICT' in ORGANIZER.read_text(encoding='utf-8-sig')
assert 'ARCHIVED_CONFLICT' in ORGANIZER.read_text(encoding='utf-8-sig')
assert "-DryRun" not in bat

print("C11C_CLEANUP_FREEZE_TOOLING_CONTRACT PASS")
