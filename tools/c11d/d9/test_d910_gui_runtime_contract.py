"""Static, dependency-free contract checks for the optional D9.10 Qt runtime runner."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "tools/c11d/d9/test_d910_gui_runtime_acceptance.py"
CAPTURE = ROOT / "tools/c11d/d9/capture_d910_acceptance.py"
SUITE = ROOT / "c11c-suite/self_test.py"
CHECKPOINT = ROOT / "docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md"

runtime = RUNTIME.read_text(encoding="utf-8")
capture = CAPTURE.read_text(encoding="utf-8")
suite = SUITE.read_text(encoding="utf-8")
checkpoint = CHECKPOINT.read_text(encoding="utf-8")

for token in (
    "QT_QPA_PLATFORM",
    "offscreen",
    "MainWindow()",
    "d9_validate.click()",
    "challenges",
    "visual_loops",
    "visual_drills",
    "editorial_override_propagated",
    "d_render_adapter_envelope.json",
    "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED",
    '"renderer_dispatch_invoked": False',
    '"renderer_input_emitted": False',
    '"media_output_created": False',
    '"d4_8": "BLOCKED"',
    '"release_authority": "NONE"',
    '"screenshots_required": False',
):
    assert token in runtime, token

for token in ("--include-qt-gui-runtime", "test_d910_gui_runtime_acceptance.py", "qt_gui_runtime_exercised", "qt_gui_runtime={"):
    assert token in capture, token
assert "test_d910_gui_runtime_contract.py" in suite
assert "D9.10 automated Qt GUI runtime" in checkpoint

for forbidden in ("run_c11c_challenge_production.ps1", "run_prototype.ps1", "run_visual_drill_production.ps1", "godot.exe", "ffmpeg.exe"):
    assert forbidden.lower() not in runtime.lower(), f"Runtime test must never launch production tooling: {forbidden}"

manifest = json.loads((ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
assert manifest, "Historical C11-C manifest must remain present/readable"

print("C11-D D9.10 QT GUI RUNTIME HARNESS CONTRACT PASS | content_types=3/3 | static_contract=PASS | screenshots=NOT_REQUIRED | production=FORBIDDEN")
