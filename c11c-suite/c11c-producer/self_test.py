from __future__ import annotations

import hashlib
import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path(__import__("os").environ.get("C11C_PROJECT_ROOT", ROOT.parents[1])).resolve()

py_compile.compile(str(ROOT / "main.py"), doraise=True)
py_compile.compile(str(ROOT / "preflight.py"), doraise=True)
py_compile.compile(str(ROOT / "c11d_gui_request.py"), doraise=True)
py_compile.compile(str(ROOT / "test_d9_producer_integration.py"), doraise=True)
D9_DIR = PROJECT / "tools" / "c11d" / "d9"
for d9_file in ("universal_producer.py", "universal_producer_cli.py", "test_universal_producer.py"):
    py_compile.compile(str(D9_DIR / d9_file), doraise=True)

schema = json.loads((ROOT / "producer_schema.json").read_text(encoding="utf-8"))
build_manifest = json.loads((ROOT / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
assert build_manifest["version"] == "0.11.0"
assert build_manifest["backend_logic_modified"] is False

assert schema["producer_version"] == "0.11.0"
assert [x[0] for x in schema.get("video_types", [])] == ["challenges", "visual_loops", "visual_drills"]
assert set(schema["drills"]) == {"tracking", "saccade", "pursuit", "peripheral_scan"}
assert len(schema["families"]) == 5

profile_path = PROJECT / "profiles" / "delivery" / "c11c_video_delivery_profiles.json"
assert profile_path.exists(), profile_path
profiles = json.loads(profile_path.read_text(encoding="utf-8"))
expected_profiles = {"MASTER_1080", "REVIEW_720", "MIN_540", "META_REELS_FINAL_V1", "LONGFORM_1080"}
assert set(profiles["profiles"]) == expected_profiles
assert profiles["standard_default"] == "MASTER_1080"
assert profiles["profiles"]["MASTER_1080"]["width"] == 1080
assert profiles["profiles"]["MASTER_1080"]["height"] == 1920
assert profiles["profiles"]["MASTER_1080"]["audio_sample_rate_hz"] == 48000
assert profiles["profiles"]["MASTER_1080"]["audio_channels"] == 2
assert profiles["profiles"]["MASTER_1080"]["fps"] == 30
assert profiles["profiles"]["MASTER_1080"]["encoder"] == "libx264"
assert profiles["profiles"]["MASTER_1080"]["gop_frames"] == 90

challenge_root = PROJECT / "challenges"
challenge_paths = sorted(challenge_root.glob("CHALLENGE_[0-9][0-9][0-9].json"))
assert len(challenge_paths) == 9, challenge_paths
assert any(op[0] == "REVIEW_CHALLENGES" for op in schema.get("batch_operations", []))
assert (ROOT / "test_producer_gui_contract.py").exists()
assert (ROOT / "c11d_gui_request.py").exists()
assert (ROOT / "test_d9_producer_integration.py").exists()
assert build_manifest["d_request_tab"] is True
assert build_manifest["d9_universal_editorial_tab"] is True
assert build_manifest["d9_universal_request_adapter"] == "tools/c11d/d9/universal_producer.py"
assert build_manifest["d9_universal_cli_adapter"] == "tools/c11d/d9/universal_producer_cli.py"
assert build_manifest["d9_universal_gui_cli_parity"] is True
assert build_manifest["d9_universal_plan_only"] is True
assert build_manifest["d9_universal_renderer_activation"] is False
assert build_manifest["d9_universal_production_execution"] is False
assert build_manifest["d9_universal_release_authority"] == "NONE"
assert build_manifest["d_request_runtime_execution"] is False
assert build_manifest["d_request_renderer_activation"] is False
drill_runtime = (ROOT / "run_visual_drill_production.ps1").read_text(encoding="utf-8-sig")
assert ("ProcessStartInfo" in drill_runtime) or ("Start-Process" in drill_runtime)
assert "generator_stdout.log" in drill_runtime
assert "run_c11c_challenge_bulk_qa.ps1" in (ROOT / "main.py").read_text(encoding="utf-8")
assert "run_c11a1_challenge_bulk_qa.ps1" not in (ROOT / "main.py").read_text(encoding="utf-8")

phase_keys = ("hook_duration", "game_duration", "reveal_duration", "cta_duration")
expected_frames = {
    "CHALLENGE_001": 540,
    "CHALLENGE_002": 600,
    "CHALLENGE_003": 720,
    "CHALLENGE_004": 900,
    "CHALLENGE_005": 420,
    "CHALLENGE_006": 540,
    "CHALLENGE_007": 600,
    "CHALLENGE_008": 720,
    "CHALLENGE_009": 720,
}
for path in challenge_paths:
    data = json.loads(path.read_text(encoding="utf-8"))
    cid = data["challenge_id"]
    video = data["video"]
    fps = int(video["fps"])
    total_s = sum(float(video.get(k, 0.0)) for k in phase_keys)
    frames = round(total_s * fps)
    assert frames == expected_frames[cid], (cid, frames, expected_frames[cid])
    assert float(video["game_duration"]) > 0
    assert 24 <= fps <= 60

challenge_launcher = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_challenge_production.ps1"
assert challenge_launcher.exists()
challenge_text = challenge_launcher.read_text(encoding="utf-8-sig")
for token in ("MASTER_1080", "REVIEW_720", "MIN_540", "META_REELS_FINAL_V1", "LONGFORM_1080", "$hookFrames", "$gameFrames", "$revealFrames", "$ctaFrames"):
    assert token in challenge_text, token

loop_launcher = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_production.ps1"
drill_launcher = ROOT / "run_visual_drill_production.ps1"
assert loop_launcher.exists() and drill_launcher.exists()
loop_text = loop_launcher.read_text(encoding="utf-8-sig")
drill_text = drill_launcher.read_text(encoding="utf-8-sig")
assert "DeliveryProfile" in loop_text
assert "Resolve-DeliveryProfileData" in loop_text
assert "DeliveryProfile" in drill_text
assert "Resolve-DeliveryProfileData" in drill_text
assert "-ar 48000" in drill_text
assert "c11c_video_delivery_profiles.json" in loop_text
assert "c11c_video_delivery_profiles.json" in drill_text
assert "scale=${deliveryWidth}:${deliveryHeight}:flags=lanczos" in loop_text
assert "deliveryProfileData.width" in loop_text
assert "encoder" in loop_text and "gop_frames" in loop_text
assert "scale=${deliveryWidth}:${deliveryHeight}:flags=lanczos" in drill_text
assert "function Wait-ForStableFile" in drill_text
assert "'--write-movie',$avi" in drill_text
assert "-i $avi -an" in drill_text
assert "Wait-ForStableFile -Path $avi" in drill_text
assert "Start-Process -FilePath $godotExecutable" in drill_text
assert "@('--path','.'" in drill_text
assert "'--resolution'" not in drill_text
assert "KeepAvi" not in drill_text
assert "temporary_avi" in drill_text
assert "profiles\\presentation\\c11c_visual_hooks.json" in drill_text
assert ".content.hook" not in drill_text
assert "revision='2.19.1'" in drill_text, "Visual Drill product manifest revision must remain 2.19.1"
assert "revision='2.19.12'" in loop_text, "Visual Loop product manifest revision must be 2.19.12"
assert "$TrackingGameplayDurationSeconds=21.0" in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_visual_drill_review.ps1").read_text(encoding="utf-8-sig")
assert "TRACKING_GAMEPLAY_SECONDS: float = 21.0" in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "C11CVisualDrillReviewEnvelopeGenerator.gd").read_text(encoding="utf-8")
assert "DEFAULT_GAMEPLAY_SECONDS: float = 17.0" in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "C11CVisualDrillReviewEnvelopeGenerator.gd").read_text(encoding="utf-8")
assert "if not output_root.is_absolute_path():" in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "C11CVisualDrillReviewEnvelopeGenerator.gd").read_text(encoding="utf-8")
assert "New-C11CReviewWorkerPool" in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_art_direction_batch_v4.ps1").read_text(encoding="utf-8-sig")
assert "WorkerRoot" in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_art_direction_batch_v4.ps1").read_text(encoding="utf-8-sig")
assert "Mutex" not in (PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_art_direction_batch_v4.ps1").read_text(encoding="utf-8-sig")
main_text = (ROOT / "main.py").read_text(encoding="utf-8")
assert "CHALLENGES = load_challenge_catalog()" in main_text
assert "-OutputRoot" in main_text
assert "recipe.delivery" in main_text
assert "QSlider" in main_text
assert "ALEATORIO" in main_text
assert "Banner" not in main_text
assert "type_info" not in main_text
assert "PONER TODO EN ALEATORIO" not in main_text
assert "QTableWidget::item:selected" in main_text
assert "_recipe_already_produced" in main_text
assert "YA PRODUCIDO" in main_text

backend_source = PROJECT / schema["backend_profile_source"]
assert backend_source.exists()
actual_hash = hashlib.sha256(backend_source.read_bytes()).hexdigest()
assert actual_hash == schema["backend_profile_sha256"], (schema["backend_profile_sha256"], actual_hash)

from test_d9_producer_integration import run_checks
_d9_counts = run_checks()
assert _d9_counts == {"core_cases": 90, "personalization_cases": 12, "negative_cases": 4}
print("C11-D D9.5.1 Challenge integration subtest PASS | core=90 | personalization=12 | negative=4")


# D9.9 universal editor: every live selector resolves, and separate CLI process shares the same adapter.
d9_universal = subprocess.run([sys.executable, str(D9_DIR / "test_universal_producer.py")], cwd=str(PROJECT), capture_output=True, text=True, encoding="utf-8", timeout=120)
assert d9_universal.returncode == 0, d9_universal.stdout + "\n" + d9_universal.stderr
assert "challenge=9/9" in d9_universal.stdout and "drill_variants=20/20" in d9_universal.stdout and "GUI/CLI parity=3/3" in d9_universal.stdout and "negative=20/20" in d9_universal.stdout
print("C11-C Producer 0.11.0 self-test PASS | D9.5.1 Challenge + D9.9 universal matrix / plan-only / GUI-CLI backend parity")
