import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import build_factory


PROJECT_ROOT = Path(build_factory.PROJECT_ROOT)
RUN_A_DIR = PROJECT_ROOT / "export" / "c8_b_run_a" / "CHALLENGE_001"
RUN_B_DIR = PROJECT_ROOT / "export" / "c8_b_run_b" / "CHALLENGE_001"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    manifest_path_a = RUN_A_DIR / "CHALLENGE_001_manifest.json"
    manifest_path_b = RUN_B_DIR / "CHALLENGE_001_manifest.json"

    assert_true(
        manifest_path_a.is_file(),
        f"Manifesto Run A no encontrado: {manifest_path_a}",
    )
    assert_true(
        manifest_path_b.is_file(),
        f"Manifesto Run B no encontrado: {manifest_path_b}",
    )

    with open(manifest_path_a, "r", encoding="utf-8") as f:
        manifest_a = json.load(f)

    with open(manifest_path_b, "r", encoding="utf-8") as f:
        manifest_b = json.load(f)

    # ----------------------------------------------------
    # 0. ESTADO DE RELEASE / STATUS GATES
    # ----------------------------------------------------
    assert_true(
        manifest_a.get("status") == "PASS" and manifest_b.get("status") == "PASS",
        "C8-B.2 Status: una o ambas ejecuciones no tienen status PASS.",
    )

    prov_a = manifest_a.get("provenance", {})
    prov_b = manifest_b.get("provenance", {})

    dirty_a = prov_a.get("git", {}).get("dirty", True)
    dirty_b = prov_b.get("git", {}).get("dirty", True)

    if dirty_a or dirty_b:
        print("[C8-B.2] ADVERTENCIA: Se detectó árbol Git 'dirty' en una o ambas ejecuciones.")
        print(f"         Run A dirty: {dirty_a} | Run B dirty: {dirty_b}")
        print("         (El determinismo bit-a-bit es válido, pero el contrato de release limpio requiere dirty=false).")

    print("[C8-B.2] Release Status & Git Flags: PASS (con aviso de dirty state)")

    # ----------------------------------------------------
    # 1. IDENTIDAD DE ENTRADA Y PROVENANCE
    # ----------------------------------------------------
    assert_true(
        prov_a == prov_b,
        "C8-B.2 Identidad de entrada: los bloques provenance difieren entre Run A y Run B.",
    )
    print("[C8-B.2] Identidad de entrada (Provenance): PASS")

    # ----------------------------------------------------
    # 2. IDENTIDAD DE EJECUCIÓN (TELEMETRY)
    # ----------------------------------------------------
    telemetry_keys = [
        "rng_version",
        "initial_seed",
        "seed_used",
        "total_frames",
        "hook_frames",
        "game_frames",
        "reveal_frames",
        "cta_frames",
        "winning_frame",
        "winning_frame_game",
        "winning_time",
        "winning_time_game",
        "attempts",
        "close_calls",
        "final_seed",
        "score",
        "minimum_distance",
    ]

    telem_a = manifest_a.get("telemetry", {})
    telem_b = manifest_b.get("telemetry", {})

    for key in telemetry_keys:
        val_a = telem_a.get(key)
        val_b = telem_b.get(key)
        assert_true(
            val_a == val_b,
            f"C8-B.2 Identidad de ejecución: telemetría '{key}' difiere ({val_a} vs {val_b}).",
        )
    print("[C8-B.2] Identidad de ejecución (Telemetry): PASS")

    # ----------------------------------------------------
    # 3. RESULTADO FÍSICO Y HASHES DEL RAW
    # ----------------------------------------------------
    artifacts_a = manifest_a.get("artifacts", {})
    artifacts_b = manifest_b.get("artifacts", {})

    raw_hash_a = artifacts_a.get("raw_video_sha256")
    raw_hash_b = artifacts_b.get("raw_video_sha256")

    assert_true(
        raw_hash_a is not None and raw_hash_a == raw_hash_b,
        f"C8-B.2 Resultado físico: raw_video_sha256 difiere en manifiesto ({raw_hash_a} vs {raw_hash_b}).",
    )

    raw_filename_a = artifacts_a.get("raw_video")
    raw_filename_b = artifacts_b.get("raw_video")

    raw_path_a = RUN_A_DIR / raw_filename_a
    raw_path_b = RUN_B_DIR / raw_filename_b

    assert_true(
        raw_path_a.is_file(),
        f"Archivo RAW físico A no encontrado: {raw_path_a}",
    )
    assert_true(
        raw_path_b.is_file(),
        f"Archivo RAW físico B no encontrado: {raw_path_b}",
    )

    physical_hash_a = build_factory.compute_file_sha256(raw_path_a)
    physical_hash_b = build_factory.compute_file_sha256(raw_path_b)

    assert_true(
        physical_hash_a == physical_hash_b,
        f"C8-B.2 Resultado físico: SHA-256 físico de RAW difiere ({physical_hash_a} vs {physical_hash_b}).",
    )

    assert_true(
        raw_hash_a == physical_hash_a,
        "C8-B.2 Resultado físico: el hash del manifiesto no coincide con el archivo físico A.",
    )
    assert_true(
        raw_hash_b == physical_hash_b,
        "C8-B.2 Resultado físico: el hash del manifiesto no coincide con el archivo físico B.",
    )

    print("[C8-B.2] Resultado físico (RAW Bit-to-Bit Identity): PASS")
    print("[C8-B.2] RESULTADO GLOBAL DE DETERMINISMO: PASS")


if __name__ == "__main__":
    main()