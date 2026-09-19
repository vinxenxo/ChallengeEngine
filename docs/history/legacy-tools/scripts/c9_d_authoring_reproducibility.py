import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATOR = PROJECT_ROOT / "tests" / "C9CBatchAuthoringGenerator.gd"
DEFAULT_INPUT = PROJECT_ROOT / "authoring_batch.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    print(f"[C9-D] FAIL: {message}")
    raise SystemExit(1)


def run_generator(input_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rel_input = input_path.relative_to(PROJECT_ROOT).as_posix()
    try:
        rel_output = output_dir.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        fail("El generador GDScript requiere output-dir dentro del repositorio.")

    cmd = [
        "godot",
        "--path",
        str(PROJECT_ROOT),
        "--headless",
        "--script",
        str(GENERATOR),
        "--",
        f"--input-batch={rel_input}",
        f"--output-dir={rel_output}",
    ]
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), text=True)
    if result.returncode != 0:
        fail(f"Godot batch generator devolvió {result.returncode}.")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="C9-D Authoring Reproducibility")
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="authoring_batch.json relativo al proyecto",
    )
    args = parser.parse_args()

    input_path = (PROJECT_ROOT / args.input).resolve()
    if not input_path.is_file():
        fail(f"No existe authoring batch: {input_path}")

    input_hash = sha256_file(input_path)
    with tempfile.TemporaryDirectory(prefix="c9d_authoring_", dir=str(PROJECT_ROOT)) as temp_root:
        temp_root_path = Path(temp_root)
        run_a = temp_root_path / "run_a"
        run_b = temp_root_path / "run_b"

        print("==========================================================")
        print(" C9-D: AUTHORING REPRODUCIBILITY")
        print("==========================================================")
        print(f"[C9-D] Input SHA-256: {input_hash}")

        run_generator(input_path, run_a)
        run_generator(input_path, run_b)

        files_a = sorted(run_a.glob("*.json"))
        files_b = sorted(run_b.glob("*.json"))
        if not files_a or not files_b:
            fail("Una de las ejecuciones no generó configuraciones JSON.")
        if [p.name for p in files_a] != [p.name for p in files_b]:
            fail(
                "El conjunto de archivos generado difiere: "
                f"A={[p.name for p in files_a]} B={[p.name for p in files_b]}"
            )

        print(f"[C9-D] Configuraciones A/B: {len(files_a)}/{len(files_b)}")

        for file_a in files_a:
            file_b = run_b / file_a.name
            hash_a = sha256_file(file_a)
            hash_b = sha256_file(file_b)
            if hash_a != hash_b:
                fail(f"SHA-256 de configuración difiere en {file_a.name}: {hash_a} != {hash_b}")

            json_a = load_json(file_a)
            json_b = load_json(file_b)
            if json_a != json_b:
                fail(f"Semántica JSON difiere en {file_a.name} aunque el hash coincidiera.")

            print(f"  -> [{file_a.stem}] SHA-256 idéntico: PASS")

        print("[C9-D] RESULTADO GLOBAL DE REPRODUCIBILIDAD DE AUTHORING: PASS")


if __name__ == "__main__":
    main()
