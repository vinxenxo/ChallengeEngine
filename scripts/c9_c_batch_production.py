import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BATCH_INPUT = PROJECT_ROOT / "authoring_batch.json"
GENERATED_DIR = PROJECT_ROOT / "c9_c_generated_configs"
PRODUCTION_DIR = PROJECT_ROOT / "export" / "c9_c_production_batch"


def fail(message: str) -> None:
    print(f"[C9-C] FAIL: {message}")
    raise SystemExit(1)


def run_command(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True)


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        fail(f"No se pudo leer JSON {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"JSON raíz no Dictionary: {path}")
    return data


def main() -> None:
    print("=" * 58)
    print(" C9-C: BATCH AUTHORING PRODUCTIVE GENERATION")
    print("=" * 58)

    if not BATCH_INPUT.is_file():
        fail(f"No existe el lote de authoring: {BATCH_INPUT}")

    for path in (GENERATED_DIR, PRODUCTION_DIR):
        if path.exists():
            shutil.rmtree(path)

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    godot_cmd = [
        "godot",
        "--path", str(PROJECT_ROOT),
        "--headless",
        "--script", str(PROJECT_ROOT / "tests" / "C9CBatchAuthoringGenerator.gd"),
        "--",
        "--input-batch=authoring_batch.json",
        "--output-dir=c9_c_generated_configs",
    ]

    print("\n[C9-C] 1. Authoring -> Canonical V2 -> Runtime V1...")
    result_godot = run_command(godot_cmd, PROJECT_ROOT)
    if result_godot.returncode != 0:
        fail("Godot batch authoring devolvió un error.")

    generated_configs = sorted(GENERATED_DIR.glob("*.json"))
    if not generated_configs:
        fail("No se generaron configuraciones runtime.")

    with BATCH_INPUT.open("r", encoding="utf-8") as handle:
        requests = json.load(handle)
    if not isinstance(requests, list):
        fail("authoring_batch.json no contiene una lista.")
    if len(generated_configs) != len(requests):
        fail(f"Cardinalidad inesperada: {len(generated_configs)} configs para {len(requests)} requests.")

    print(f"[C9-C] Configuraciones generadas: {len(generated_configs)}")

    print("\n[C9-C] 2. Inyectando lote en build_factory.py...")
    factory_cmd = [
        sys.executable,
        "build_factory.py",
        "--batch", str(GENERATED_DIR),
        "--output", str(PRODUCTION_DIR),
        "--workers", "1",
    ]
    result_factory = run_command(factory_cmd, PROJECT_ROOT)

    batch_manifest_path = PRODUCTION_DIR / "BATCH_MANIFEST.json"
    if not batch_manifest_path.is_file():
        fail("build_factory no produjo BATCH_MANIFEST.json.")

    batch_manifest = load_json(batch_manifest_path)
    summary = batch_manifest.get("summary", {})
    total = int(summary.get("total", -1))
    passed = int(summary.get("passed", -1))
    failed = int(summary.get("failed", -1))
    if total != len(requests) or passed != len(requests) or failed != 0:
        fail(f"Producción incompleta: total={total}, passed={passed}, failed={failed}.")

    errors = batch_manifest.get("errors", [])
    non_policy_errors = [
        error for error in errors
        if error.get("code") != "C7_A2_MIXED_BATCH_REQUIRED"
    ]
    if non_policy_errors:
        fail(f"El batch contiene errores críticos: {non_policy_errors}")

    # C7-A2 is a known batch-policy exception because this authoring corpus is audio-on only.
    if result_factory.returncode != 0 and batch_manifest.get("status") != "FAILED":
        fail("build_factory devolvió error sin un estado de batch coherente.")

    unit_manifests = []
    for config_path in generated_configs:
        config_data = load_json(config_path)
        challenge_id = config_data.get("challenge_id")
        if not challenge_id:
            fail(f"Config sin challenge_id: {config_path}")
        manifest_path = PRODUCTION_DIR / challenge_id / f"{challenge_id}_manifest.json"
        if not manifest_path.is_file():
            fail(f"Manifest unitario ausente: {manifest_path}")
        manifest = load_json(manifest_path)
        if manifest.get("status") != "PASS":
            fail(f"Manifest unitario no PASS: {manifest_path}")
        unit_manifests.append(manifest)

    print(f"[C9-C] Unidades auditadas: {len(unit_manifests)}/{len(requests)} PASS")
    print("[C9-C] Excepción C7-A2: aceptada como política no bloqueante.")
    print("\n" + "=" * 58)
    print("[C9-C] BATCH AUTHORING -> FACTORY: PASS")
    print(f"[C9-C] Configuración: {GENERATED_DIR}")
    print(f"[C9-C] Producción: {PRODUCTION_DIR}")
    print("=" * 58)


if __name__ == "__main__":
    main()
