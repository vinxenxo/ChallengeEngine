import os
import sys
import json
import subprocess
import argparse
import math
import glob
from pathlib import Path
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Resolución inmutable del directorio raíz del proyecto y versión oficial de la fábrica.
PROJECT_ROOT = Path(__file__).resolve().parent
FACTORY_VERSION = "0.9.0"
MANIFEST_VERSION = "1.0"

# Metadata declarativa que forma parte del provenance snapshot del manifest.
# La factoría COPIA SOLO claves que existan realmente en Capa 0; nunca infiere valores.
DECLARATIVE_METADATA_FIELDS = (
    "schema_version",
    "engine_version",
    "mechanic",
    "mechanic_version",
    "video_profile_version",
    "asset_family_version",
)


def sanitize_workspace(output_dir: Path) -> None:
    """
    Sanea la raíz del directorio de salida eliminando exclusivamente artefactos de desafíos
    sueltos o residuo (R11/R12) antes de publicar el lote de producción.
    Respeta la política de limpieza 0.9.0 sin tocar subcarpetas canónicas ni archivos desconocidos.
    """
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
            return {
                "error": "FFprobe no devolvió información de stream de vídeo."
            }

        stream_info = streams[0]

        if not isinstance(stream_info, dict):
            return {
                "error": "FFprobe devolvió un stream de vídeo inválido."
            }

        required_fields = (
            "duration",
            "nb_read_frames",
            "r_frame_rate",
        )

        missing = [
            field
            for field in required_fields
            if field not in stream_info
        ]

        if missing:
            return {
                "error": (
                    "FFprobe no proporcionó los campos requeridos: "
                    + ", ".join(missing)
                )
            }

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
        except (ValueError, TypeError) as exc:
            return {
                "error": f"FFprobe duration inválida: {duration_raw!r}"
            }

        try:
            nb_frames = int(frames_raw)
        except (ValueError, TypeError):
            return {
                "error": f"FFprobe nb_read_frames inválido: {frames_raw!r}"
            }

        if not math.isfinite(duration):
            return {
                "error": f"FFprobe duration no finita: {duration!r}"
            }

        if nb_frames < 0:
            return {
                "error": f"FFprobe nb_read_frames negativo: {nb_frames}"
            }

        if not isinstance(fps_raw, str) or "/" not in fps_raw:
            return {
                "error": f"FFprobe r_frame_rate inválido: {fps_raw!r}"
            }

        return {
            "duration": duration,
            "nb_frames": nb_frames,
            "r_frame_rate": fps_raw,
        }

    except subprocess.CalledProcessError as exc:
        return {
            "error": (
                exc.stderr.strip()
                or "FFprobe terminó con código de error."
            )
        }
    except (json.JSONDecodeError, OSError) as exc:
        return {
            "error": str(exc)
        }


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

    # Contract 0.9.0: todos los artefactos de un challenge viven en su directorio dedicado.
    output_dir = base_output_dir / challenge_id
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_video_path = output_dir / f"{challenge_id}_raw.avi"
    final_video_path = output_dir / f"{challenge_id}.mp4"
    manifest_path = output_dir / f"{challenge_id}_manifest.json"

    # --- 1. SIMULACIÓN (GODOT) ---
    cmd = [
        "godot",
        "--path", str(PROJECT_ROOT)
    ]
    
    if validate_only:
        cmd.append("--headless")
    else:
        cmd.extend([
            "--write-movie", str(raw_video_path),
            "--fixed-fps", "60",
            "--quit-after", "660"
        ])
        
    cmd.extend([
        "--",
        f"--config={config_path}"
    ])
    
    if validate_only:
        cmd.append("--validate-only")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=str(PROJECT_ROOT)
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
        return {
            "success": False,
            "error": error_payload or {"code": "GODOT_EXECUTION_ERROR", "message": err_msg}
        }

    if telemetry is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {"code": "MISSING_TELEMETRY", "message": "Godot did not emit [TELEMETRY_JSON]."}
        }

    telemetry_rng_version = telemetry.get("rng_version")
    if source_rng_version is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_RNG_VERSION",
                "message": "generation.rng_version es obligatorio en Capa 0 bajo el contrato 0.9.0."
            }
        }
    if telemetry_rng_version != source_rng_version:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "RNG_VERSION_MISMATCH",
                "message": f"rng_version de Capa 0 ({source_rng_version}) no coincide con telemetry ({telemetry_rng_version})."
            }
        }

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
        return {
            "success": False,
            "error": {"code": "MISSING_RAW_VIDEO", "message": f"Godot no generó un RAW AVI válido: {raw_video_path.name}"}
        }

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(final_video_path)
    ]

    ffmpeg_proc = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if ffmpeg_proc.returncode != 0:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {"code": "FFMPEG_ERROR", "message": ffmpeg_proc.stderr.strip()}
        }

    # --- 3. VALIDACIÓN E2E (FFPROBE) ---
    probe_data = run_ffprobe(final_video_path)
    if "error" in probe_data:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {"code": "FFPROBE_ERROR", "message": probe_data["error"]}
        }

    # ---------------------------------------------------------
    # C5-A — RUNTIME ↔ ARTIFACT CONSISTENCY GATE
    # ---------------------------------------------------------

    video_config = challenge_definition.get("video")

    if not isinstance(video_config, dict) or "fps" not in video_config:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_DECLARATIVE_FPS",
                "message": "video.fps es obligatorio para validar el artefacto."
            }
        }

    expected_fps = video_config["fps"]

    # A0 — Declarative FPS válido
    if (
        type(expected_fps) not in (int, float)
        or not math.isfinite(float(expected_fps))
        or float(expected_fps) <= 0.0
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_DECLARATIVE_FPS",
                "message": f"video.fps inválido: {expected_fps!r}"
            }
        }

    # C5-A exige enteros físicos para la línea temporal.
    required_timeline_keys = (
        "total_frames",
        "hook_frames",
        "game_frames",
        "cta_frames",
    )

    missing_timeline = [
        key
        for key in required_timeline_keys
        if key not in telemetry
    ]

    if missing_timeline:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_TELEMETRY_TIMELINE",
                "message": (
                    "Telemetría temporal incompleta. "
                    f"Faltan: {', '.join(missing_timeline)}"
                )
            }
        }

    t_total = telemetry["total_frames"]
    t_hook = telemetry["hook_frames"]
    t_game = telemetry["game_frames"]
    t_cta = telemetry["cta_frames"]

    # A5 — Telemetría temporal válida
    if (
        type(t_total) is not int
        or type(t_hook) is not int
        or type(t_game) is not int
        or type(t_cta) is not int
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_TELEMETRY_TIMELINE",
                "message": "Los campos de timeline deben ser enteros."
            }
        }

    if (
        t_total <= 0
        or t_hook < 0
        or t_game <= 0
        or t_cta < 0
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_TELEMETRY_TIMELINE",
                "message": (
                    "Valores de timeline fuera de rango: "
                    f"total={t_total}, hook={t_hook}, "
                    f"game={t_game}, cta={t_cta}"
                )
            }
        }

    # A1 — Integridad interna del timeline
    timeline_sum = t_hook + t_game + t_cta

    if t_total != timeline_sum:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "TIMELINE_INTEGRITY_VIOLATION",
                "message": (
                    f"total_frames ({t_total}) != "
                    f"hook ({t_hook}) + "
                    f"game ({t_game}) + "
                    f"cta ({t_cta})"
                )
            }
        }

    expected_duration = t_total / float(expected_fps)

    # A2 — Conteo físico
    if probe_data["nb_frames"] != t_total:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_FRAME_COUNT_MISMATCH",
                "message": (
                    f"FFprobe nb_frames ({probe_data['nb_frames']}) != "
                    f"Telemetry total_frames ({t_total})"
                )
            }
        }

    # A3 — Duración física
    if not math.isclose(
        probe_data["duration"],
        expected_duration,
        abs_tol=0.05
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_DURATION_MISMATCH",
                "message": (
                    f"FFprobe duration ({probe_data['duration']}) != "
                    f"expected duration ({expected_duration}) "
                    f"within tolerance 0.05s"
                )
            }
        }

    # A4 — Framerate físico
    expected_rate = f"{int(expected_fps)}/1"

    if probe_data["r_frame_rate"] != expected_rate:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_FRAMERATE_MISMATCH",
                "message": (
                    f"FFprobe r_frame_rate ({probe_data['r_frame_rate']}) != "
                    f"expected ({expected_rate})"
                )
            }
        }

    probe_data["valid"] = True

    # --- 4. CONSOLIDACIÓN DE MANIFIESTO UNITARIO (Contract 0.9.0) ---
    manifest_data = {
        "manifest_version": MANIFEST_VERSION,
        "factory_version": FACTORY_VERSION,
        "challenge_id": challenge_id,
        "declarative_metadata": declarative_metadata,
        "telemetry": telemetry,
        "artifacts": {
            "raw_video": raw_video_path.name,
            "final_video": final_video_path.name
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
    """Helper interno para procesar un desafío de forma aislada (ejecutable por worker)."""
    challenge_id = read_challenge_id(cfg_path) or cfg_path.stem

    print(f"[BATCH-WORKER] Iniciando {challenge_id} desde {cfg_path.name}...")
    res = run_factory(str(cfg_path), str(base_output_dir), validate_only)
    print(f"[BATCH-WORKER] Finalizado {challenge_id} -> {'PASS' if res['success'] else 'FAIL'}")

    return challenge_id, res


def run_batch(challenges_dir_str: str, base_output_dir_str: str, validate_only: bool = False, workers: int = 1) -> Dict[str, Any]:
    """Ejecuta el procesamiento por lotes de forma concurrente controlada (Workers) y orden determinista."""
    challenges_dir = Path(challenges_dir_str).resolve()
    base_output_dir = Path(base_output_dir_str).resolve()
    
    if not challenges_dir.exists() or not challenges_dir.is_dir():
        return {
            "success": False,
            "error": {"code": "DIR_NOT_FOUND", "message": f"El directorio de desafíos no existe: {challenges_dir}"}
        }

    config_files = sorted(challenges_dir.glob("CHALLENGE_*.json"))
    
    if not config_files:
        return {
            "success": False,
            "error": {"code": "NO_CHALLENGES_FOUND", "message": f"No se encontraron archivos CHALLENGE_*.json en {challenges_dir}"}
        }

    base_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Contract 0.9.0: Saneamiento de la raíz de salida antes de volcar la producción del lote
    sanitize_workspace(base_output_dir)

    batch_manifest_path = base_output_dir / "BATCH_MANIFEST.json"
    raw_results: Dict[str, Dict[str, Any]] = {}

    print(f"[BATCH] Lanzando lote con {len(config_files)} desafíos usando {workers} worker(s)...")

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        future_to_config = {
            executor.submit(_process_single_challenge, cfg_path, base_output_dir, validate_only): cfg_path 
            for cfg_path in config_files
        }

        for future in as_completed(future_to_config):
            try:
                ch_id, res = future.result()
                raw_results[ch_id] = res
            except Exception as exc:
                cfg_path = future_to_config[future]
                ch_id = read_challenge_id(cfg_path) or cfg_path.stem
                raw_results[ch_id] = {
                    "success": False,
                    "error": {"code": "WORKER_CRASH", "message": str(exc)}
                }

    passed_count = 0
    failed_count = 0
    challenges_results = []

    for cfg_path in config_files:
        challenge_id = read_challenge_id(cfg_path)
        res = raw_results.get(challenge_id, {"success": False, "error": {"code": "MISSING_RESULT", "message": "No se registró resultado."}})
        
        if res["success"]:
            passed_count += 1
            manifest_info = res.get("manifest", {})
            telemetry_info = manifest_info.get("telemetry", res.get("telemetry", {}))
            declarative_info = manifest_info.get("declarative_metadata", res.get("declarative_metadata", {}))
            challenge_result = {
                "challenge_id": challenge_id,
                "status": "PASS",
                "mechanic": declarative_info.get("mechanic"),
                "rng_version": telemetry_info.get("rng_version"),
                "godot_version": telemetry_info.get("godot_version"),
            }
            if not validate_only:
                challenge_result["manifest"] = f"{challenge_id}/{challenge_id}_manifest.json"
            challenges_results.append(challenge_result)
        else:
            failed_count += 1
            err_info = res.get("error", {"code": "UNKNOWN_ERROR", "message": "Error desconocido en factoría"})
            challenges_results.append({
                "challenge_id": challenge_id,
                "status": "FAIL",
                "error": err_info
            })

    # Extracción dinámica y consolidada de versiones del lote
    godot_versions = sorted({
        str(telemetry.get("godot_version"))
        for res in raw_results.values()
        if res.get("success")
        for telemetry in [res.get("manifest", {}).get("telemetry", res.get("telemetry", {}))]
        if telemetry.get("godot_version") is not None
    })

    rng_versions = sorted({
        str(telemetry.get("rng_version"))
        for res in raw_results.values()
        if res.get("success")
        for telemetry in [res.get("manifest", {}).get("telemetry", res.get("telemetry", {}))]
        if telemetry.get("rng_version") is not None
    })

    batch_status = "PASSED" if failed_count == 0 else "FAILED"
    batch_manifest_data = {
        "manifest_version": MANIFEST_VERSION,
        "factory_version": FACTORY_VERSION,
        "godot_versions": godot_versions,
        "rng_versions": rng_versions,
        "status": batch_status,
        "summary": {
            "total": len(config_files),
            "passed": passed_count,
            "failed": failed_count
        },
        "challenges": challenges_results
    }

    with open(batch_manifest_path, "w", encoding="utf-8") as f:
        json.dump(batch_manifest_data, f, indent=2, ensure_ascii=False)

    return {
        "success": (failed_count == 0),
        "batch_manifest_path": str(batch_manifest_path),
        "summary": batch_manifest_data["summary"],
        "batch_manifest": batch_manifest_data
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pause Challenge Engine - Build Factory (Batch, Parallel & Unit)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", help="Ruta al archivo JSON unitario de configuración del challenge")
    group.add_argument("--batch", help="Directorio que contiene los archivos CHALLENGE_*.json para procesamiento por lotes")
    
    parser.add_argument("--output", default="./output", help="Directorio raíz de salida de los artefactos")
    parser.add_argument("--validate-only", action="store_true", help="Ejecutar validación matemática sin empaquetar video")
    parser.add_argument("--workers", type=int, default=1, help="Número de hilos/procesos concurrentes para el modo batch (default: 1)")
    args = parser.parse_args()

    if args.config:
        result = run_factory(args.config, args.output, args.validate_only)
    else:
        result = run_batch(args.batch, args.output, args.validate_only, args.workers)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if not result["success"]:
        sys.exit(1)