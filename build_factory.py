import os
import sys
import json
import subprocess
import argparse
import math
import glob
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Resolución inmutable del directorio raíz del proyecto y versión oficial de la fábrica.
PROJECT_ROOT = Path(__file__).resolve().parent
FACTORY_VERSION = "0.9.0"
MANIFEST_VERSION = "1.0"

# Metadata declarativa que forma parte del provenance snapshot del manifest.
DECLARATIVE_METADATA_FIELDS = (
    "schema_version",
    "engine_version",
    "mechanic",
    "mechanic_version",
    "video_profile_version",
    "asset_family_version",
)


def sanitize_workspace(output_dir: Path) -> None:
    """Sanea la raíz del directorio de salida eliminando exclusivamente artefactos de desafíos sueltos o residuo."""
    if not output_dir.exists():
        return

    residual_patterns = [
        "CHALLENGE_*_raw.avi",
        "CHALLENGE_*.mp4",
        "CHALLENGE_*_manifest.json",
    ]

    for pattern in residual_patterns:
        for filepath in output_dir.glob(pattern):
            if filepath.is_file():
                try:
                    filepath.unlink()
                    print(f"[WORKSPACE-SANITIZER] Residuo legacy eliminado: {filepath.name}")
                except Exception as e:
                    print(f"[WORKSPACE-SANITIZER] Advertencia: no se pudo eliminar {filepath.name}: {e}")


def read_challenge_id(config_path: Path) -> Optional[str]:
    """Extrae challenge_id únicamente de la definición declarativa; sin fallback inferido."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("challenge_id") if isinstance(data, dict) else None
    except Exception as e:
        print(f"[ERROR_JSON] {{\"error\": \"CONFIG_READ_ERROR\", \"message\": \"No se pudo leer {config_path.name}: {e}\"}}")
        return None


def read_challenge_definition(config_path: Path) -> Dict[str, Any]:
    """Carga la definición declarativa completa sin modificarla ni completarla."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"No se pudo leer {config_path.name}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError(f"La configuración {config_path.name} no contiene un objeto JSON válido.")
    return data


def build_declarative_metadata(challenge_definition: Dict[str, Any]) -> Dict[str, Any]:
    """Construye un snapshot exacto de las claves declarativas de provenance presentes."""
    return {
        field: challenge_definition[field]
        for field in DECLARATIVE_METADATA_FIELDS
        if field in challenge_definition
    }


def read_rng_version(challenge_definition: Dict[str, Any]) -> Optional[str]:
    """Obtiene generation.rng_version sin defaults ni inferencias."""
    generation = challenge_definition.get("generation")
    if not isinstance(generation, dict) or "rng_version" not in generation:
        return None
    return generation["rng_version"]


def cleanup_partial_outputs(output_dir: Path, challenge_id: str) -> None:
    """Elimina artefactos canónicos parciales de la ejecución fallida actual."""
    for path in (
        output_dir / f"{challenge_id}_raw.avi",
        output_dir / f"{challenge_id}.mp4",
        output_dir / f"{challenge_id}_manifest.json",
    ):
        try:
            if path.exists() or path.is_symlink():
                path.unlink()
        except OSError as exc:
            print(f"[WARN_CLEANUP] No se pudo eliminar {path}: {exc}")


def compute_file_sha256(file_path: Path, chunk_size: int = 65536) -> Optional[str]:
    """Calcula el hash SHA-256 de un archivo físico de forma segura y optimizada por bloques."""
    if not file_path.is_file():
        return None
    
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as exc:
        print(f"[WARN_HASH] No se pudo calcular SHA-256 para {file_path.name}: {exc}")
        return None


def run_ffprobe(video_path: Path) -> Dict[str, Any]:
    """Extrae observaciones de FFprobe sin convertir datos ausentes/corruptos en valores válidos."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-count_frames",
        "-show_entries", "stream=r_frame_rate,nb_read_frames,duration",
        "-of", "json",
        str(video_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        probe_data = json.loads(result.stdout)
        streams = probe_data.get("streams")

        if not isinstance(streams, list) or not streams:
            return {"error": "FFprobe no devolvió información de stream de vídeo."}

        stream_info = streams[0]
        if not isinstance(stream_info, dict):
            return {"error": "FFprobe devolvió un stream de vídeo inválido."}

        required_fields = ("duration", "nb_read_frames", "r_frame_rate")
        missing = [field for field in required_fields if field not in stream_info]

        if missing:
            return {"error": "FFprobe no proporcionó los campos requeridos: " + ", ".join(missing)}

        duration_raw = stream_info["duration"]
        frames_raw = stream_info["nb_read_frames"]
        fps_raw = stream_info["r_frame_rate"]

        if duration_raw in (None, "", "N/A"):
            return {"error": "FFprobe devolvió duration ausente o N/A."}
        if frames_raw in (None, "", "N/A"):
            return {"error": "FFprobe devolvió nb_read_frames ausente o N/A."}
        if fps_raw in (None, ""):
            return {"error": "FFprobe devolvió r_frame_rate ausente."}

        try:
            duration = float(duration_raw)
        except (ValueError, TypeError):
            return {"error": f"FFprobe duration inválida: {duration_raw!r}"}

        try:
            nb_frames = int(frames_raw)
        except (ValueError, TypeError):
            return {"error": f"FFprobe nb_read_frames inválido: {frames_raw!r}"}

        if not math.isfinite(duration):
            return {"error": f"FFprobe duration no finita: {duration!r}"}
        if nb_frames < 0:
            return {"error": f"FFprobe nb_read_frames negativo: {nb_frames}"}
        if not isinstance(fps_raw, str) or "/" not in fps_raw:
            return {"error": f"FFprobe r_frame_rate inválido: {fps_raw!r}"}

        return {
            "duration": duration,
            "nb_frames": nb_frames,
            "r_frame_rate": fps_raw,
        }

    except subprocess.CalledProcessError as exc:
        return {"error": exc.stderr.strip() or "FFprobe terminó con código de error."}
    except (json.JSONDecodeError, OSError) as exc:
        return {"error": str(exc)}


def run_factory(config_path_str: str, output_dir_str: str, validate_only: bool = False) -> Dict[str, Any]:
    config_path = Path(config_path_str).resolve()
    base_output_dir = Path(output_dir_str).resolve()
    
    if not config_path.exists():
        return {"success": False, "error": {"code": "FILE_NOT_FOUND", "message": f"Config file not found: {config_path}"}}

    try:
        challenge_definition = read_challenge_definition(config_path)
        challenge_id = read_challenge_id(config_path)
        declarative_metadata = build_declarative_metadata(challenge_definition)
        source_rng_version = read_rng_version(challenge_definition)
    except ValueError as exc:
        return {"success": False, "error": {"code": "CONFIG_READ_ERROR", "message": str(exc)}}

    if not challenge_id:
        return {"success": False, "error": {"code": "MISSING_CHALLENGE_ID", "message": f"challenge_id ausente en {config_path.name}"}}
    if "mechanic" not in challenge_definition:
        return {"success": False, "error": {"code": "MISSING_MECHANIC", "message": f"mechanic ausente en {config_path.name}"}}

    output_dir = base_output_dir / challenge_id
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_video_path = output_dir / f"{challenge_id}_raw.avi"
    final_video_path = output_dir / f"{challenge_id}.mp4"
    manifest_path = output_dir / f"{challenge_id}_manifest.json"

    # --- 1. SIMULACIÓN (GODOT) ---
    cmd = ["godot", "--path", str(PROJECT_ROOT)]
    if validate_only:
        cmd.append("--headless")
    else:
        cmd.extend(["--write-movie", str(raw_video_path), "--fixed-fps", "60", "--quit-after", "660"])
        
    cmd.extend(["--", f"--config={config_path}"])
    if validate_only:
        cmd.append("--validate-only")

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", cwd=str(PROJECT_ROOT)
    )
    stdout, stderr = process.communicate()

    telemetry: Optional[Dict[str, Any]] = None
    error_payload: Optional[Dict[str, Any]] = None

    for line in stdout.splitlines():
        line_clean = line.strip()
        if line_clean.startswith("[TELEMETRY_JSON]"):
            try: telemetry = json.loads(line_clean[len("[TELEMETRY_JSON]"):].strip())
            except json.JSONDecodeError: pass
        elif line_clean.startswith("[ERROR_JSON]"):
            try: error_payload = json.loads(line_clean[len("[ERROR_JSON]"):].strip())
            except json.JSONDecodeError: pass

    if process.returncode != 0 or error_payload is not None:
        cleanup_partial_outputs(output_dir, challenge_id)
        err_msg = error_payload.get("message", "Godot process failed.") if error_payload else stderr.strip()
        return {"success": False, "error": error_payload or {"code": "GODOT_EXECUTION_ERROR", "message": err_msg}}

    if telemetry is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "MISSING_TELEMETRY", "message": "Godot did not emit [TELEMETRY_JSON]."}}

    telemetry_rng_version = telemetry.get("rng_version")
    if source_rng_version is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "MISSING_RNG_VERSION", "message": "generation.rng_version es obligatorio en Capa 0."}}
    if telemetry_rng_version != source_rng_version:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "RNG_VERSION_MISMATCH", "message": f"rng_version mismatch: {source_rng_version} vs {telemetry_rng_version}"}}

    if validate_only:
        return {
            "success": True,
            "validate_only": True,
            "telemetry": telemetry,
            "declarative_metadata": declarative_metadata,
            "challenge_id": challenge_id,
        }

    # --- 2. EMPAQUETADO (FFMPEG) ---
    if not raw_video_path.exists() or raw_video_path.stat().st_size == 0:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "MISSING_RAW_VIDEO", "message": f"Godot no generó RAW AVI válido."}}

    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", str(raw_video_path),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        str(final_video_path)
    ]
    ffmpeg_proc = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if ffmpeg_proc.returncode != 0:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "FFMPEG_ERROR", "message": ffmpeg_proc.stderr.strip()}}

    # --- 3. VALIDACIÓN E2E (FFPROBE) ---
    probe_data = run_ffprobe(final_video_path)
    if "error" in probe_data:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "FFPROBE_ERROR", "message": probe_data["error"]}}

    # C5-A — CONSISTENCY GATE
    video_config = challenge_definition.get("video")
    if not isinstance(video_config, dict) or "fps" not in video_config:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "MISSING_DECLARATIVE_FPS", "message": "video.fps obligatorio."}}

    expected_fps = video_config["fps"]
    if type(expected_fps) not in (int, float) or not math.isfinite(float(expected_fps)) or float(expected_fps) <= 0.0:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "INVALID_DECLARATIVE_FPS", "message": f"video.fps inválido."}}

    required_timeline_keys = ("total_frames", "hook_frames", "game_frames", "cta_frames")
    if any(k not in telemetry for k in required_timeline_keys):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "MISSING_TELEMETRY_TIMELINE", "message": "Telemetría temporal incompleta."}}

    t_total = telemetry["total_frames"]
    t_hook = telemetry["hook_frames"]
    t_game = telemetry["game_frames"]
    t_cta = telemetry["cta_frames"]

    if any(type(x) is not int for x in (t_total, t_hook, t_game, t_cta)):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "INVALID_TELEMETRY_TIMELINE", "message": "Timeline debe ser entero."}}

    if t_total <= 0 or t_hook < 0 or t_game <= 0 or t_cta < 0:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "INVALID_TELEMETRY_TIMELINE", "message": "Timeline fuera de rango."}}

    if t_total != (t_hook + t_game + t_cta):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "TIMELINE_INTEGRITY_VIOLATION", "message": "Suma de frames incorrecta."}}

    expected_duration = t_total / float(expected_fps)

    if probe_data["nb_frames"] != t_total:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "ARTIFACT_FRAME_COUNT_MISMATCH", "message": "Frames FFprobe != Telemetría."}}

    if not math.isclose(probe_data["duration"], expected_duration, abs_tol=0.05):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "ARTIFACT_DURATION_MISMATCH", "message": "Duración física errónea."}}

    expected_rate = f"{int(expected_fps)}/1"
    if probe_data["r_frame_rate"] != expected_rate:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "ARTIFACT_FRAMERATE_MISMATCH", "message": "Framerate erróneo."}}

    probe_data["valid"] = True

    # --- C5-C: CÁLCULO DE HUELLAS CRIPTOGRÁFICAS (SHA-256) ---
    raw_hash = compute_file_sha256(raw_video_path)
    final_hash = compute_file_sha256(final_video_path)

    if not raw_hash or not final_hash:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {"success": False, "error": {"code": "HASH_GENERATION_FAILED", "message": "No se pudo calcular el hash criptográfico SHA-256."}}

    # --- 4. CONSOLIDACIÓN DE MANIFIESTO UNITARIO (C5-B / C5-C) ---
    manifest_data = {
        "manifest_version": MANIFEST_VERSION,
        "factory_version": FACTORY_VERSION,
        "challenge_id": challenge_id,
        "declarative_metadata": declarative_metadata,
        "telemetry": telemetry,
        "artifacts": {
            "raw_video": raw_video_path.name,
            "raw_video_sha256": raw_hash,
            "final_video": final_video_path.name,
            "final_video_sha256": final_hash
        },
        "validation": probe_data,
        "status": "PASS",
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "validate_only": False,
        "manifest_path": str(manifest_path),
        "video_path": str(final_video_path),
        "manifest": manifest_data
    }


def _process_single_challenge(cfg_path: Path, base_output_dir: Path, validate_only: bool) -> tuple[str, Dict[str, Any]]:
    challenge_id = read_challenge_id(cfg_path) or cfg_path.stem
    print(f"[BATCH-WORKER] Iniciando {challenge_id} desde {cfg_path.name}...")
    res = run_factory(str(cfg_path), str(base_output_dir), validate_only)
    print(f"[BATCH-WORKER] Finalizado {challenge_id} -> {'PASS' if res['success'] else 'FAIL'}")
    return challenge_id, res


def read_unit_manifest(manifest_path: Path) -> Dict[str, Any]:
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_MISSING", "message": f"No existe el manifiesto: {manifest_path}"}}
    except (OSError, json.JSONDecodeError) as exc:
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_NOT_CERTIFIED", "message": f"Error leyendo manifiesto: {exc}"}}

    if not isinstance(data, dict):
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_NOT_CERTIFIED", "message": "Manifiesto no es un objeto JSON."}}

    return {"valid": True, "manifest": data}


def audit_unit_manifest(cfg_path: Path, base_output_dir: Path, execution_result: Dict[str, Any]) -> Dict[str, Any]:
    """C5-D + C5-C: Audita la evidencia en disco y comprueba las huellas criptográficas SHA-256."""
    challenge_definition = read_challenge_definition(cfg_path)
    challenge_id = challenge_definition.get("challenge_id")

    if not challenge_id:
        return {"valid": False, "error": {"code": "BATCH_CHALLENGE_COVERAGE_MISMATCH", "message": "challenge_id ausente."}}

    if not execution_result.get("success", False):
        return {"valid": False, "error": {"code": "BATCH_INTEGRITY_GATE_FAILED", "message": f"{challenge_id}: ejecución fallida."}}

    challenge_dir = base_output_dir / challenge_id
    manifest_path = challenge_dir / f"{challenge_id}_manifest.json"

    manifest_read = read_unit_manifest(manifest_path)
    if not manifest_read["valid"]:
        return manifest_read

    manifest = manifest_read["manifest"]

    validation = manifest.get("validation")
    if manifest.get("status") != "PASS" or not isinstance(validation, dict) or validation.get("valid") is not True:
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_NOT_CERTIFIED", "message": f"{challenge_id}: manifiesto no certificado."}}

    if manifest.get("challenge_id") != challenge_id:
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_ID_MISMATCH", "message": f"{challenge_id}: ID mismatch."}}

    declarative_metadata = manifest.get("declarative_metadata")
    if not isinstance(declarative_metadata, dict):
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_DECLARATIVE_MISMATCH", "message": f"{challenge_id}: declarative_metadata inválido."}}

    for field in DECLARATIVE_METADATA_FIELDS:
        if field in challenge_definition:
            if field not in declarative_metadata or declarative_metadata[field] != challenge_definition[field]:
                return {"valid": False, "error": {"code": "UNIT_MANIFEST_DECLARATIVE_MISMATCH", "message": f"{challenge_id}: campo {field} no coincide."}}

    source_rng_version = read_rng_version(challenge_definition)
    telemetry = manifest.get("telemetry")
    if not isinstance(telemetry, dict) or telemetry.get("rng_version") != source_rng_version:
        return {"valid": False, "error": {"code": "UNIT_MANIFEST_DECLARATIVE_MISMATCH", "message": f"{challenge_id}: rng_version mismatch."}}

    # C5-C / C5-D: Verificación de Integridad de Artefactos y Hashes SHA-256 en Disco
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        return {"valid": False, "error": {"code": "UNIT_ARTIFACT_MISSING", "message": f"{challenge_id}: sección artifacts ausente."}}

    checks = [
        ("raw_video", "raw_video_sha256"),
        ("final_video", "final_video_sha256")
    ]

    for file_key, hash_key in checks:
        filename = artifacts.get(file_key)
        declared_hash = artifacts.get(hash_key)

        if not isinstance(filename, str) or not filename or not isinstance(declared_hash, str) or not declared_hash:
            return {"valid": False, "error": {"code": "UNIT_ARTIFACT_MISSING", "message": f"{challenge_id}: falta declaración de {file_key} o su hash."}}

        artifact_path = challenge_dir / filename
        try:
            artifact_path.resolve().relative_to(challenge_dir.resolve())
        except ValueError:
            return {"valid": False, "error": {"code": "UNIT_ARTIFACT_MISSING", "message": f"{challenge_id}: ruta de artefacto fuera de límites."}}

        if not artifact_path.is_file() or artifact_path.stat().st_size <= 0:
            return {"valid": False, "error": {"code": "UNIT_ARTIFACT_MISSING", "message": f"{challenge_id}: artefacto físico ausente: {filename}"}}

        # Recálculo forense del SHA-256 en disco para garantizar que no fue manipulado
        current_hash = compute_file_sha256(artifact_path)
        if current_hash != declared_hash:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_ARTIFACT_HASH_MISMATCH",
                    "message": f"{challenge_id}: el hash SHA-256 de {filename} no coincide con el manifiesto (posible corrupción o manipulación)."
                }
            }

    return {
        "valid": True,
        "challenge_id": challenge_id,
        "manifest": manifest,
        "manifest_path": str(manifest_path),
    }


def write_batch_manifest_atomic(batch_manifest_path: Path, batch_manifest_data: Dict[str, Any]) -> None:
    temp_path = batch_manifest_path.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(batch_manifest_data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    temp_path.replace(batch_manifest_path)


def run_batch(challenges_dir_str: str, base_output_dir_str: str, validate_only: bool = False, workers: int = 1) -> Dict[str, Any]:
    challenges_dir = Path(challenges_dir_str).resolve()
    base_output_dir = Path(base_output_dir_str).resolve()
    
    if not challenges_dir.exists() or not challenges_dir.is_dir():
        return {"success": False, "error": {"code": "DIR_NOT_FOUND", "message": f"Directorio no encontrado."}}

    config_files = sorted(challenges_dir.glob("CHALLENGE_*.json"))
    if not config_files:
        return {"success": False, "error": {"code": "NO_CHALLENGES_FOUND", "message": f"No hay challenges."}}

    base_output_dir.mkdir(parents=True, exist_ok=True)
    sanitize_workspace(base_output_dir)

    batch_manifest_path = base_output_dir / "BATCH_MANIFEST.json"

    # D1 — Cobertura
    challenge_ids = []
    for cfg_path in config_files:
        ch_id = read_challenge_id(cfg_path)
        if not ch_id:
            err = {"code": "BATCH_CHALLENGE_COVERAGE_MISMATCH", "message": f"{cfg_path.name} sin ID válido."}
            batch_data = {"manifest_version": MANIFEST_VERSION, "factory_version": FACTORY_VERSION, "godot_versions": [], "rng_versions": [], "status": "FAILED", "summary": {"total": len(config_files), "passed": 0, "failed": len(config_files)}, "challenges": [], "errors": [err]}
            write_batch_manifest_atomic(batch_manifest_path, batch_data)
            return {"success": False, "batch_manifest_path": str(batch_manifest_path), "summary": batch_data["summary"], "batch_manifest": batch_data}
        challenge_ids.append(ch_id)

    if len(challenge_ids) != len(set(challenge_ids)):
        err = {"code": "BATCH_CHALLENGE_COVERAGE_MISMATCH", "message": "ID duplicados encontrados."}
        batch_data = {"manifest_version": MANIFEST_VERSION, "factory_version": FACTORY_VERSION, "godot_versions": [], "rng_versions": [], "status": "FAILED", "summary": {"total": len(config_files), "passed": 0, "failed": len(config_files)}, "challenges": [], "errors": [err]}
        write_batch_manifest_atomic(batch_manifest_path, batch_data)
        return {"success": False, "batch_manifest_path": str(batch_manifest_path), "summary": batch_data["summary"], "batch_manifest": batch_data}

    raw_results = {}
    print(f"[BATCH] Lanzando lote con {len(config_files)} desafíos usando {workers} worker(s)...")

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        future_to_config = {
            executor.submit(_process_single_challenge, cfg_path, base_output_dir, validate_only): cfg_path 
            for cfg_path in config_files
        }
        for future in as_completed(future_to_config):
            cfg_path = future_to_config[future]
            try:
                ch_id, res = future.result()
                raw_results[ch_id] = res
            except Exception as exc:
                ch_id = read_challenge_id(cfg_path) or cfg_path.stem
                raw_results[ch_id] = {"success": False, "error": {"code": "WORKER_CRASH", "message": str(exc)}}

    audited_manifests = {}
    challenges_results = []
    gate_errors = []

    for cfg_path in config_files:
        ch_id = read_challenge_id(cfg_path)
        exec_res = raw_results.get(ch_id, {"success": False, "error": {"code": "MISSING_RESULT", "message": "Sin resultado."}})
        
        audit = audit_unit_manifest(cfg_path, base_output_dir, exec_res)
        if not audit["valid"]:
            error = audit["error"]
            gate_errors.append({"challenge_id": ch_id, **error})
            challenges_results.append({"challenge_id": ch_id, "status": "FAIL", "error": error})
            continue

        manifest = audit["manifest"]
        audited_manifests[ch_id] = manifest
        telemetry = manifest.get("telemetry", {})
        declarative = manifest.get("declarative_metadata", {})

        ch_res = {
            "challenge_id": ch_id,
            "status": "PASS",
            "mechanic": declarative.get("mechanic"),
            "rng_version": telemetry.get("rng_version"),
            "godot_version": telemetry.get("godot_version"),
        }
        if not validate_only:
            ch_res["manifest"] = f"{ch_id}/{ch_id}_manifest.json"
        challenges_results.append(ch_res)

    expected_count = len(config_files)
    passed_count = sum(1 for item in challenges_results if item["status"] == "PASS")
    failed_count = expected_count - passed_count

    godot_versions = sorted({
        str(m.get("telemetry", {}).get("godot_version"))
        for m in audited_manifests.values()
        if m.get("telemetry", {}).get("godot_version") is not None
    })
    rng_versions = sorted({
        str(m.get("telemetry", {}).get("rng_version"))
        for m in audited_manifests.values()
        if m.get("telemetry", {}).get("rng_version") is not None
    })

    batch_status = "PASSED" if failed_count == 0 and not gate_errors else "FAILED"
    batch_manifest_data = {
        "manifest_version": MANIFEST_VERSION,
        "factory_version": FACTORY_VERSION,
        "godot_versions": godot_versions,
        "rng_versions": rng_versions,
        "status": batch_status,
        "summary": {"total": expected_count, "passed": passed_count, "failed": failed_count},
        "challenges": challenges_results
    }
    if gate_errors:
        batch_manifest_data["errors"] = gate_errors

    write_batch_manifest_atomic(batch_manifest_path, batch_manifest_data)

    return {
        "success": batch_status == "PASSED",
        "batch_manifest_path": str(batch_manifest_path),
        "summary": batch_manifest_data["summary"],
        "batch_manifest": batch_manifest_data
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pause Challenge Engine - Build Factory (C5-C SHA-256)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", help="Ruta al archivo JSON unitario")
    group.add_argument("--batch", help="Directorio con archivos CHALLENGE_*.json")
    
    parser.add_argument("--output", default="./output", help="Directorio raíz de salida")
    parser.add_argument("--validate-only", action="store_true", help="Validación matemática sin vídeo")
    parser.add_argument("--workers", type=int, default=1, help="Workers concurrentes")
    args = parser.parse_args()

    if args.config:
        result = run_factory(args.config, args.output, args.validate_only)
    else:
        result = run_batch(args.batch, args.output, args.validate_only, args.workers)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["success"]:
        sys.exit(1)