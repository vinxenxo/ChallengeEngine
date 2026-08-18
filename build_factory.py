import os
import sys
import json
import subprocess
import argparse
from typing import Dict, Any, Optional

def run_factory(config_path: str, output_dir: str, validate_only: bool = False) -> Dict[str, Any]:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    os.makedirs(output_dir, exist_ok=True)

    # Invocación de Godot en modo Headless
    cmd = [
        "godot",
        "--headless",
        "--path", ".",
        "--",
        f"--config={config_path}"
    ]
    if validate_only:
        cmd.append("--validate-only")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    stdout, stderr = process.communicate()

    telemetry: Optional[Dict[str, Any]] = None
    error_payload: Optional[Dict[str, Any]] = None

    for line in stdout.splitlines():
        line_clean = line.strip()
        if line_clean.startswith("[TELEMETRY_JSON]"):
            json_str = line_clean[len("[TELEMETRY_JSON]"):].strip()
            telemetry = json.loads(json_str)
        elif line_clean.startswith("[ERROR_JSON]"):
            json_str = line_clean[len("[ERROR_JSON]"):].strip()
            error_payload = json.loads(json_str)

    if process.returncode != 0 or error_payload is not None:
        err_msg = error_payload.get("message", "Godot process failed.") if error_payload else stderr
        return {
            "success": False,
            "error": error_payload or {"code": "GODOT_EXECUTION_ERROR", "message": err_msg}
        }

    if telemetry is None:
        return {
            "success": False,
            "error": {"code": "MISSING_TELEMETRY", "message": "Godot did not emit [TELEMETRY_JSON]."}
        }

    # Python consume los datos directamente emitidos por VideoTimeline
    if validate_only:
        return {
            "success": True,
            "validate_only": True,
            "telemetry": telemetry
        }

    # Generación de Manifest
    manifest_path = os.path.join(output_dir, f"{telemetry.get('challenge_id', 'CHALLENGE')}_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "validate_only": False,
        "manifest_path": manifest_path,
        "telemetry": telemetry
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pause Challenge Engine - Build Factory")
    parser.add_argument("--config", required=True, help="Path to challenge JSON config")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--validate-only", action="store_true", help="Run simulation validation without rendering")
    args = parser.parse_args()

    result = run_factory(args.config, args.output, args.validate_only)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["success"]:
        sys.exit(1)