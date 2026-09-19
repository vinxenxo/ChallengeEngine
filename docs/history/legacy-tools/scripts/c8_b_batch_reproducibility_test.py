import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import build_factory


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="C8-B.3 Batch Reproducibility Cross-Run Verifier"
    )
    parser.add_argument("batch_a", help="Ruta al directorio raíz del Lote A externo")
    parser.add_argument("batch_b", help="Ruta al directorio raíz del Lote B externo")
    args = parser.parse_args()

    root_a = Path(args.batch_a).resolve()
    root_b = Path(args.batch_b).resolve()

    batch_manifest_a = root_a / "BATCH_MANIFEST.json"
    batch_manifest_b = root_b / "BATCH_MANIFEST.json"

    assert_true(
        batch_manifest_a.is_file(),
        f"BATCH_MANIFEST.json no encontrado en Lote A: {batch_manifest_a}",
    )
    assert_true(
        batch_manifest_b.is_file(),
        f"BATCH_MANIFEST.json no encontrado en Lote B: {batch_manifest_b}",
    )

    with open(batch_manifest_a, "r", encoding="utf-8") as f:
        data_a = json.load(f)
    with open(batch_manifest_b, "r", encoding="utf-8") as f:
        data_b = json.load(f)

    # Validar éxito de producción del corpus
    summary_a = data_a.get("summary", {})
    summary_b = data_b.get("summary", {})

    assert_true(
        summary_a.get("failed") == 0 and summary_a.get("passed") == summary_a.get("total"),
        f"Lote A no tiene éxito de producción completo: {summary_a}",
    )
    assert_true(
        summary_b.get("failed") == 0 and summary_b.get("passed") == summary_b.get("total"),
        f"Lote B no tiene éxito de producción completo: {summary_b}",
    )

    challenges_a = {
        item["challenge_id"]: item
        for item in data_a.get("challenges", [])
        if item.get("status") == "PASS"
    }
    challenges_b = {
        item["challenge_id"]: item
        for item in data_b.get("challenges", [])
        if item.get("status") == "PASS"
    }

    ids_a = set(challenges_a.keys())
    ids_b = set(challenges_b.keys())

    assert_true(
        ids_a == ids_b,
        f"Corpus PASS difiere entre lotes: A={sorted(ids_a)} B={sorted(ids_b)}.",
    )

    common_ids = sorted(ids_a)
    assert_true(
        len(common_ids) > 0,
        "No se encontraron desafíos PASS en el corpus.",
    )

    print(f"[C8-B.3] Iniciando auditoría cruzada de {len(common_ids)} desafíos...")

    for ch_id in common_ids:
        dir_a = root_a / ch_id
        dir_b = root_b / ch_id

        manifest_path_a = dir_a / f"{ch_id}_manifest.json"
        manifest_path_b = dir_b / f"{ch_id}_manifest.json"

        assert_true(
            manifest_path_a.is_file(),
            f"[{ch_id}] Manifiesto unitario ausente en Lote A: {manifest_path_a}",
        )
        assert_true(
            manifest_path_b.is_file(),
            f"[{ch_id}] Manifiesto unitario ausente en Lote B: {manifest_path_b}",
        )

        with open(manifest_path_a, "r", encoding="utf-8") as f:
            ma = json.load(f)
        with open(manifest_path_b, "r", encoding="utf-8") as f:
            mb = json.load(f)

        # 1. Validación de paridad exacta en el bloque provenance entre ambos lotes
        prov_a = ma.get("provenance", {})
        prov_b = mb.get("provenance", {})
        assert_true(
            prov_a == prov_b,
            f"[{ch_id}] Discrepancia en el bloque provenance entre lotes.",
        )

        # 2. Validación de Telemetría Clave
        telem_a = ma.get("telemetry", {})
        telem_b = mb.get("telemetry", {})
        telemetry_keys = [
            "rng_version",
            "initial_seed",
            "seed_used",
            "total_frames",
            "winning_frame",
            "score",
            "minimum_distance",
        ]
        for key in telemetry_keys:
            val_a = telem_a.get(key)
            val_b = telem_b.get(key)
            assert_true(
                val_a == val_b,
                f"[{ch_id}] Discrepancia en telemetría '{key}' ({val_a} vs {val_b}).",
            )

        # 3. Validación Física del RAW Bit-to-Bit
        art_a = ma.get("artifacts", {})
        art_b = mb.get("artifacts", {})
        raw_hash_a = art_a.get("raw_video_sha256")
        raw_hash_b = art_b.get("raw_video_sha256")

        assert_true(
            raw_hash_a is not None and raw_hash_a == raw_hash_b,
            f"[{ch_id}] Hash SHA-256 del RAW difiere en manifiesto.",
        )

        raw_path_a = dir_a / art_a.get("raw_video")
        raw_path_b = dir_b / art_b.get("raw_video")

        assert_true(
            raw_path_a.is_file(),
            f"[{ch_id}] Archivo RAW físico A no encontrado: {raw_path_a}",
        )
        assert_true(
            raw_path_b.is_file(),
            f"[{ch_id}] Archivo RAW físico B no encontrado: {raw_path_b}",
        )

        physical_hash_a = build_factory.compute_file_sha256(raw_path_a)
        physical_hash_b = build_factory.compute_file_sha256(raw_path_b)

        assert_true(
            physical_hash_a == physical_hash_b,
            f"[{ch_id}] Discrepancia en el hash SHA-256 físico del archivo RAW.",
        )

        print(f"  -> [{ch_id}] Paridad verificada: PASS")

    print("[C8-B.3] RESULTADO GLOBAL DE REPRODUCIBILIDAD EN LOTE: PASS")


if __name__ == "__main__":
    main()