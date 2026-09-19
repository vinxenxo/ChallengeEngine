from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTHORING_TEST = PROJECT_ROOT / "tests" / "C9BParkingV2ProductiveGenerationTest.gd"
BUILD_FACTORY = PROJECT_ROOT / "build_factory.py"


def run_command(cmd: list[str], label: str) -> subprocess.CompletedProcess[str]:
    print(f"[C9-B] {label}: {' '.join(str(x) for x in cmd)}")
    return subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def extract_json_object(output: str) -> dict:
    decoder = json.JSONDecoder()
    start = output.find("{")
    while start >= 0:
        try:
            value, _ = decoder.raw_decode(output[start:])
            if isinstance(value, dict):
                return value
        except json.JSONDecodeError:
            pass
        start = output.find("{", start + 1)
    raise RuntimeError("build_factory.py no emitió un JSON de resultado interpretable.")


def main() -> int:
    parser = argparse.ArgumentParser(description="C9-B parking_v2 authoring -> production integration")
    parser.add_argument(
        "output_root",
        help="Directorio externo donde se escribirán config generada y artefactos de producción",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    generated_config = output_root / "parking_v2_generated.json"
    production_output = output_root / "production"

    # 1. Godot authoring -> runtime V1 production projection.
    authoring_cmd = [
        "godot",
        "--headless",
        "--path",
        str(PROJECT_ROOT),
        "--script",
        str(AUTHORING_TEST),
        "--",
        f"--output-config={generated_config}",
    ]
    authoring_result = run_command(authoring_cmd, "Generación authoring")
    print(authoring_result.stdout)
    if authoring_result.returncode != 0:
        print("[C9-B] FAIL: authoring generation returned non-zero exit code.", file=sys.stderr)
        return 1

    if not generated_config.is_file():
        print(f"[C9-B] FAIL: generated config not found: {generated_config}", file=sys.stderr)
        return 1

    # 2. Production factory consumes the generated definition.
    factory_cmd = [
        sys.executable,
        str(BUILD_FACTORY),
        "--config",
        str(generated_config),
        "--output",
        str(production_output),
    ]
    factory_result = run_command(factory_cmd, "Producción build_factory")
    print(factory_result.stdout)
    if factory_result.returncode != 0:
        print("[C9-B] FAIL: build_factory returned non-zero exit code.", file=sys.stderr)
        return 1

    result = extract_json_object(factory_result.stdout)
    if result.get("success") is not True:
        print(f"[C9-B] FAIL: build_factory success != true: {result}", file=sys.stderr)
        return 1

    manifest_path = Path(result.get("manifest_path", ""))
    if not manifest_path.is_file():
        print(f"[C9-B] FAIL: manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "PASS":
        print(f"[C9-B] FAIL: production manifest status != PASS: {manifest.get('status')}", file=sys.stderr)
        return 1

    telemetry = manifest.get("telemetry", {})
    audio_export = manifest.get("audio_export", {})
    if telemetry.get("rng_version") != "2.0":
        print(f"[C9-B] FAIL: unexpected runtime rng_version: {telemetry.get('rng_version')}", file=sys.stderr)
        return 1
    if audio_export.get("audio_enabled") is not True:
        print("[C9-B] FAIL: generated parking_v2 challenge did not produce audio_enabled=true.", file=sys.stderr)
        return 1

    print("[C9-B] GENERATED CONFIG: PASS")
    print("[C9-B] AUTHORING -> RUNTIME -> FACTORY: PASS")
    print("[C9-B] RESULTADO GLOBAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
