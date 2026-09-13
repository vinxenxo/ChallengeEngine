import sys
import json
import argparse
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


import build_factory

RELEASE_GATE_VERSION = "2.2.0"


def compute_file_sha256(file_path: Path, chunk_size: int = 65536) -> Optional[str]:
    if not file_path.is_file():
        return None
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None


def run_release_gate(release_dir_str: str) -> Dict[str, Any]:
    release_dir = Path(release_dir_str).resolve()
    if not release_dir.exists() or not release_dir.is_dir():
        return {
            "success": False,
            "error": {
                "code": "RELEASE_DIR_NOT_FOUND",
                "message": f"Directorio de release no encontrado: {release_dir}",
            },
        }

    batch_manifest_path = release_dir / "BATCH_MANIFEST.json"
    if not batch_manifest_path.is_file():
        return {
            "success": False,
            "error": {
                "code": "BATCH_MANIFEST_MISSING",
                "message": f"No se encontró BATCH_MANIFEST.json en {release_dir}",
            },
        }

    try:
        with open(batch_manifest_path, "r", encoding="utf-8") as f:
            batch_data = json.load(f)
    except Exception as exc:
        return {
            "success": False,
            "error": {
                "code": "BATCH_MANIFEST_PARSE_ERROR",
                "message": f"Error leyendo BATCH_MANIFEST.json: {exc}",
            },
        }

    # ========================================================
    # GESTIÓN DE BATCH STATUS Y POLÍTICA C7-A2
    # ========================================================
    batch_status = batch_data.get("status")
    batch_errors = batch_data.get("errors", [])
    
    c7_a2_policy_failed = False
    other_batch_errors = []
    for err in batch_errors:
        if err.get("code") == "C7_A2_MIXED_BATCH_REQUIRED":
            c7_a2_policy_failed = True
        else:
            other_batch_errors.append(err)

    if batch_status == "FAILED" and other_batch_errors:
        return {
            "success": False,
            "error": {
                "code": "BATCH_MANIFEST_CRITICAL_FAILURE",
                "message": f"BATCH_MANIFEST indica FAILED por errores críticos: {other_batch_errors}",
            },
        }

    challenges = batch_data.get("challenges", [])
    if not isinstance(challenges, list) or not challenges:
        return {
            "success": False,
            "error": {
                "code": "EMPTY_CHALLENGE_CORPUS",
                "message": "El batch manifest no contiene desafíos.",
            },
        }

    audited_units = []
    gate_errors = []
    corpus_commit: Optional[str] = None
    all_units_clean = True

    for item in challenges:
        ch_id = item.get("challenge_id")
        if not ch_id:
            gate_errors.append({"code": "INVALID_CHALLENGE_ENTRY", "message": "Entrada sin challenge_id en batch."})
            continue

        ch_dir = release_dir / ch_id
        if not ch_dir.is_dir():
            gate_errors.append({"challenge_id": ch_id, "code": "CHALLENGE_DIR_MISSING", "message": f"Directorio del desafío ausente en disco: {ch_id}."})
            continue

        manifest_path = ch_dir / f"{ch_id}_manifest.json"
        if not manifest_path.is_file():
            gate_errors.append({"challenge_id": ch_id, "code": "UNIT_MANIFEST_MISSING", "message": f"Manifiesto unitario ausente para {ch_id}."})
            continue

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                unit_manifest = json.load(f)
        except Exception as exc:
            gate_errors.append({"challenge_id": ch_id, "code": "UNIT_MANIFEST_PARSE_ERROR", "message": f"Error leyendo manifiesto de {ch_id}: {exc}"})
            continue

        # 1. Verificar Status PASS
        if unit_manifest.get("status") != "PASS":
            gate_errors.append({"challenge_id": ch_id, "code": "UNIT_STATUS_NOT_PASS", "message": f"El manifiesto de {ch_id} no está en estado PASS."})
            continue

        # 2. Verificar Procedencia Canónica y Hash Identity
        provenance = unit_manifest.get("provenance", {})
        if not isinstance(provenance, dict) or "provenance_sha256" not in provenance:
            gate_errors.append({"challenge_id": ch_id, "code": "PROVENANCE_MISSING", "message": f"Bloque provenance ausente o incompleto en {ch_id}."})
            continue

        declared_prov_hash = provenance.get("provenance_sha256")
        computed_prov_hash = build_factory.compute_provenance_identity_sha256(provenance)
        if computed_prov_hash != declared_prov_hash:
            gate_errors.append({"challenge_id": ch_id, "code": "PROVENANCE_HASH_MISMATCH", "message": f"provenance_sha256 corrupto o alterado en {ch_id}."})
            continue

        git_info = provenance.get("git", {})
        commit = git_info.get("commit")
        dirty = git_info.get("dirty")

        # Validación estricta del commit Git
        if not isinstance(commit, str) or not commit:
            all_units_clean = False
            gate_errors.append({
                "challenge_id": ch_id,
                "code": "INVALID_GIT_COMMIT",
                "message": f"Commit Git ausente o inválido en {ch_id}.",
            })
            continue

        if corpus_commit is None:
            corpus_commit = commit
        elif corpus_commit != commit:
            gate_errors.append({"challenge_id": ch_id, "code": "CORPUS_COMMIT_MISMATCH", "message": f"Inconsistencia de commit Git en {ch_id} ({commit} vs {corpus_commit})."})
            continue

        # Validación estricta del estado dirty (solo se acepta booleano exacto False)
        if dirty is not False:
            all_units_clean = False
            gate_errors.append({
                "challenge_id": ch_id,
                "code": "CORPUS_DIRTY_STATE",
                "message": f"El desafío {ch_id} no contiene dirty=false en su provenance (dirty={dirty!r}).",
            })
            continue

        # 3. Verificar Integridad Física de Artefactos (RAW, MP4, GIF y PCM)
        artifacts = unit_manifest.get("artifacts", {})
        audio_export = unit_manifest.get("audio_export", {})
        
        allowed_files = {
            f"{ch_id}_manifest.json",
            f"{ch_id}_raw.avi",
            f"{ch_id}.mp4",
        }

        artifact_checks = [
            ("raw_video", "raw_video_sha256"),
            ("final_video", "final_video_sha256"),
            ("preview_gif", "preview_gif_sha256"),
        ]

        for art_key, hash_key in artifact_checks:
            filename = artifacts.get(art_key)
            declared_hash = artifacts.get(hash_key)
            if not filename or not declared_hash:
                continue

            allowed_files.add(filename)
            art_path = ch_dir / filename
            if not art_path.is_file():
                gate_errors.append({"challenge_id": ch_id, "code": "PHYSICAL_ARTIFACT_MISSING", "message": f"Artefacto físico ausente: {filename} en {ch_id}."})
                continue

            current_hash = compute_file_sha256(art_path)
            if current_hash != declared_hash:
                gate_errors.append({"challenge_id": ch_id, "code": "PHYSICAL_ARTIFACT_HASH_MISMATCH", "message": f"Hash físico de {filename} no coincide con el manifiesto en {ch_id}."})
                continue

        # Chequeo Específico de PCM (Audio Master)
        audio_enabled = audio_export.get("audio_enabled", False)
        pcm_sha256_val = None
        if audio_enabled:
            pcm_filename = "audio_master.pcm"
            pcm_declared_hash = audio_export.get("audio_master_sha256")
            
            allowed_files.add(pcm_filename)
            pcm_path = ch_dir / pcm_filename
            
            if not pcm_path.is_file():
                gate_errors.append({"challenge_id": ch_id, "code": "PHYSICAL_PCM_MISSING", "message": f"Archivo PCM canónico ausente: {pcm_filename} en {ch_id}."})
            else:
                current_pcm_hash = compute_file_sha256(pcm_path)
                if current_pcm_hash != pcm_declared_hash:
                    gate_errors.append({"challenge_id": ch_id, "code": "PHYSICAL_PCM_HASH_MISMATCH", "message": f"Hash SHA-256 de audio_master.pcm no coincide con audio_master_sha256 en {ch_id}."})
                else:
                    pcm_sha256_val = current_pcm_hash

        # DETECCIÓN DE ARTEFACTOS HUÉRFANOS
        disk_files = {p.name for p in ch_dir.iterdir() if p.is_file()}
        orphan_files = disk_files - allowed_files
        if orphan_files:
            gate_errors.append({
                "challenge_id": ch_id,
                "code": "ORPHAN_ARTIFACTS_DETECTED",
                "message": f"Archivos huérfanos no declarados encontrados en {ch_id}: {sorted(list(orphan_files))}"
            })

        audited_units.append({
            "challenge_id": ch_id,
            "mechanic": unit_manifest.get("declarative_metadata", {}).get("mechanic"),
            "provenance_sha256": declared_prov_hash,
            "raw_video_sha256": artifacts.get("raw_video_sha256"),
            "final_video_sha256": artifacts.get("final_video_sha256"),
            "preview_gif_sha256": artifacts.get("preview_gif_sha256"),
            "pcm_sha256": pcm_sha256_val,
        })

    # ========================================================
    # CÁLCULO DEL HASH RAÍZ CRIPTOGRÁFICO DEL CORPUS COMPLETO
    # ========================================================
    sorted_audited_units = sorted(audited_units, key=lambda x: x["challenge_id"])
    corpus_payload = json.dumps(
        sorted_audited_units,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    corpus_root_sha256 = hashlib.sha256(corpus_payload).hexdigest()

    release_status = "CERTIFIED" if not gate_errors and len(audited_units) == len(challenges) else "FAILED"
    release_clean = (release_status == "CERTIFIED" and all_units_clean)

    release_manifest_data = {
        "release_gate_version": RELEASE_GATE_VERSION,
        "factory_version": build_factory.FACTORY_VERSION,
        "manifest_version": build_factory.MANIFEST_VERSION,
        "release_status": release_status,
        "git_release_identity": {
            "commit": corpus_commit,
            "release_clean": release_clean,
        },
        "batch_policy_evaluation": {
            "batch_manifest_status": batch_status,
            "c7_a2_mixed_batch_policy_exception": c7_a2_policy_failed,
            "blocking": False if c7_a2_policy_failed else True,
        },
        "corpus_identity": {
            "corpus_root_sha256": corpus_root_sha256,
            "total_declared": len(challenges),
            "successfully_audited": len(audited_units),
        },
        "summary": {
            "total_declared": len(challenges),
            "successfully_audited": len(audited_units),
            "failed_checks": len(gate_errors),
        },
        "audited_corpus": audited_units,
    }

    if gate_errors:
        release_manifest_data["errors"] = gate_errors

    release_manifest_path = release_dir / "RELEASE_MANIFEST.json"
    with open(release_manifest_path, "w", encoding="utf-8") as f:
        json.dump(release_manifest_data, f, indent=2, ensure_ascii=False)

    return {
        "success": release_status == "CERTIFIED",
        "release_manifest_path": str(release_manifest_path),
        "release_manifest": release_manifest_data,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pause Challenge Engine - Release Gate Auditor")
    parser.add_argument("release_dir", help="Directorio raíz del lote de producción externo a auditar")
    args = parser.parse_args()

    result = run_release_gate(release_dir_str=args.release_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result["success"]:
        sys.exit(1)