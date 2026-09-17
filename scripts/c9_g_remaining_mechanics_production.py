import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_BATCH = PROJECT_ROOT / "authoring_remaining_c9_batch.json"
GENERATED_DIR = PROJECT_ROOT / "c9_g_generated_configs"
PRODUCTION_DIR = PROJECT_ROOT / "export" / "c9_g_remaining_production"
EXPECTED_MECHANICS = {"key", "pilot", "find_v1", "choose_v1", "count_v1"}


def fail(message: str) -> None:
    print(f"[C9-G] FAIL: {message}")
    raise SystemExit(1)


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        fail(f"No se pudo leer {path}: {exc}")


def main() -> None:
    print("=" * 64)
    print(" C9-G: REMAINING MECHANICS AUTHORING -> FACTORY")
    print("=" * 64)

    if not INPUT_BATCH.is_file():
        fail(f"No existe {INPUT_BATCH}")

    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)
    if PRODUCTION_DIR.exists():
        shutil.rmtree(PRODUCTION_DIR)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    requests = load_json(INPUT_BATCH)
    if not isinstance(requests, list) or len(requests) != 5:
        fail(f"Se esperaban exactamente 5 requests, obtenido: {type(requests).__name__}/{len(requests) if isinstance(requests, list) else 'n/a'}")

    mechanics = {str(item.get("mechanic", "")) for item in requests if isinstance(item, dict)}
    if mechanics != EXPECTED_MECHANICS:
        fail(f"Corpus C9-G inesperado: {sorted(mechanics)}")

    godot_cmd = [
        "godot", "--headless", "--path", str(PROJECT_ROOT),
        "--script", str(PROJECT_ROOT / "tests" / "C9GRemainingMechanicsProductive.gd"), "--",
        f"--input-batch={INPUT_BATCH.name}",
        f"--output-dir={GENERATED_DIR.name}",
    ]
    print("\n[C9-G] 1. Authoring -> Canonical V2 -> Runtime V1...")
    godot_result = subprocess.run(godot_cmd, cwd=PROJECT_ROOT, text=True)
    if godot_result.returncode != 0:
        fail("Godot authoring batch returned non-zero exit code.")

    generated = sorted(GENERATED_DIR.glob("CHALLENGE_*.json"))
    if len(generated) != 5:
        fail(f"Se esperaban 5 configuraciones runtime, encontradas {len(generated)}")

    print(f"[C9-G] Configuraciones generadas: {len(generated)}/5")

    factory_cmd = [
        sys.executable, str(PROJECT_ROOT / "build_factory.py"),
        "--batch", str(GENERATED_DIR), "--output", str(PRODUCTION_DIR), "--workers", "1",
    ]
    print("\n[C9-G] 2. Producción build_factory...")
    factory_result = subprocess.run(factory_cmd, cwd=PROJECT_ROOT, text=True)

    batch_manifest_path = PRODUCTION_DIR / "BATCH_MANIFEST.json"
    if not batch_manifest_path.is_file():
        fail("build_factory no produjo BATCH_MANIFEST.json")

    batch_manifest = load_json(batch_manifest_path)
    summary = batch_manifest.get("summary", {})
    if int(summary.get("total", -1)) != 5 or int(summary.get("passed", -1)) != 5 or int(summary.get("failed", -1)) != 0:
        fail(f"Producción incompleta: {summary}")

    non_policy_errors = [
        error for error in batch_manifest.get("errors", [])
        if error.get("code") != "C7_A2_MIXED_BATCH_REQUIRED"
    ]
    if non_policy_errors:
        fail(f"Errores críticos en batch: {non_policy_errors}")
    if factory_result.returncode != 0 and batch_manifest.get("status") != "FAILED":
        fail("build_factory falló sin el estado de política esperado.")

    audited = 0
    for config_path in generated:
        config = load_json(config_path)
        challenge_id = config.get("challenge_id")
        if not challenge_id:
            fail(f"Config sin challenge_id: {config_path}")
        manifest_path = PRODUCTION_DIR / challenge_id / f"{challenge_id}_manifest.json"
        if not manifest_path.is_file():
            fail(f"Manifest ausente: {manifest_path}")
        manifest = load_json(manifest_path)
        if manifest.get("status") != "PASS":
            fail(f"Manifest no PASS: {manifest_path}")
        audited += 1
        print(f"  -> [{config.get('mechanic')}] {challenge_id}: PASS")

    print(f"[C9-G] Unidades auditadas: {audited}/5 PASS")
    print("[C9-G] Excepción C7-A2: aceptada como política no bloqueante.")
    print("\n" + "=" * 64)
    print("[C9-G] RESULTADO GLOBAL: REMAINING 5 MECHANICS PASS")
    print(f"[C9-G] Configuración: {GENERATED_DIR}")
    print(f"[C9-G] Producción: {PRODUCTION_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
