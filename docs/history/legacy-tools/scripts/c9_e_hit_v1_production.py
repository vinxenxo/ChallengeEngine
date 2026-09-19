import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = PROJECT_ROOT / "hit_v1"
GENERATED_CONFIG = WORK_DIR / "hit_v1_generated.json"
PRODUCTION_DIR = WORK_DIR / "production"


def main() -> int:
    WORK_DIR.mkdir(exist_ok=True)
    if GENERATED_CONFIG.exists():
        GENERATED_CONFIG.unlink()
    if PRODUCTION_DIR.exists():
        shutil.rmtree(PRODUCTION_DIR)

    godot_cmd = [
        "godot", "--headless", "--path", str(PROJECT_ROOT),
        "--script", str(PROJECT_ROOT / "tests" / "C9EHitAuthoringProductiveTest.gd"), "--",
        f"--output-config={GENERATED_CONFIG}",
    ]
    print("[C9-E] Generación authoring:", " ".join(godot_cmd))
    result = subprocess.run(godot_cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("[C9-E] FAIL: authoring generation returned non-zero exit code.")
        return 1

    if not GENERATED_CONFIG.is_file():
        print("[C9-E] FAIL: generated Runtime V1 config not found.")
        return 1

    print("[C9-E] Producción build_factory...")
    factory_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "build_factory.py"),
        "--config", str(GENERATED_CONFIG),
        "--output", str(PRODUCTION_DIR),
    ]
    result_factory = subprocess.run(factory_cmd, cwd=PROJECT_ROOT, text=True)
    if result_factory.returncode != 0:
        print("[C9-E] FAIL: build_factory returned non-zero exit code.")
        return 1

    manifest_files = list(PRODUCTION_DIR.glob("*/" + "*_manifest.json"))
    if len(manifest_files) != 1:
        print(f"[C9-E] FAIL: expected exactly 1 manifest, found {len(manifest_files)}")
        return 1

    manifest = json.loads(manifest_files[0].read_text(encoding="utf-8"))
    if manifest.get("status") != "PASS":
        print("[C9-E] FAIL: production manifest is not PASS.")
        return 1

    print("[C9-E] GENERATED_CONFIG: PASS")
    print("[C9-E] AUTHORING -> RUNTIME -> FACTORY: PASS")
    print("[C9-E] RESULTADO GLOBAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
