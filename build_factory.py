import os
import sys
import json
import subprocess
import argparse
import math
from pathlib import Path
from typing import Dict, Any, Optional

# Resolución inmutable del directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent

def read_challenge_id(config_path: Path) -> str:
    """Extrae el challenge_id directamente del JSON declarativo (Capa 0)."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("challenge_id", data.get("id", config_path.stem))
    except Exception as e:
        print(f"[ERROR_JSON] {{\"error\": \"CONFIG_READ_ERROR\", \"message\": \"No se pudo leer {config_path.name}: {e}\"}}")
        sys.exit(1)

def run_ffprobe(video_path: Path) -> Dict[str, Any]:
    """Extrae métricas exactas y maneja excepciones o valores 'N/A' de forma segura."""
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
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        probe_data = json.loads(result.stdout)
        stream_info = probe_data.get("streams", [{}])[0]
        
        def safe_float(val, default=0.0):
            try: return float(val)
            except (ValueError, TypeError): return default

        def safe_int(val, default=0):
            try: return int(val)
            except (ValueError, TypeError): return default

        return {
            "duration": safe_float(stream_info.get("duration", 0.0)),
            "nb_frames": safe_int(stream_info.get("nb_read_frames", 0)),
            "r_frame_rate": stream_info.get("r_frame_rate", "")
        }
    except Exception as e:
        return {"error": str(e)}

def run_factory(config_path_str: str, output_dir_str: str, validate_only: bool = False) -> Dict[str, Any]:
    config_path = Path(config_path_str).resolve()
    output_dir = Path(output_dir_str).resolve()
    
    if not config_path.exists():
        return {"success": False, "error": {"code": "FILE_NOT_FOUND", "message": f"Config file not found: {config_path}"}}

    output_dir.mkdir(parents=True, exist_ok=True)
    challenge_id = read_challenge_id(config_path)
    
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
        err_msg = error_payload.get("message", "Godot process failed.") if error_payload else stderr.strip()
        return {
            "success": False,
            "error": error_payload or {"code": "GODOT_EXECUTION_ERROR", "message": err_msg}
        }

    if telemetry is None:
        return {
            "success": False,
            "error": {"code": "MISSING_TELEMETRY", "message": "Godot did not emit [TELEMETRY_JSON]."}
        }

    if validate_only:
        return {
            "success": True,
            "validate_only": True,
            "telemetry": telemetry
        }

    # --- 2. EMPAQUETADO (FFMPEG) ---
    if not raw_video_path.exists():
        return {
            "success": False,
            "error": {"code": "MISSING_RAW_VIDEO", "message": f"Godot no generó: {raw_video_path.name}"}
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
        return {
            "success": False,
            "error": {"code": "FFMPEG_ERROR", "message": ffmpeg_proc.stderr.strip()}
        }

    # --- 3. VALIDACIÓN E2E (FFPROBE) ---
    probe_data = run_ffprobe(final_video_path)
    if "error" in probe_data:
        return {
            "success": False,
            "error": {"code": "FFPROBE_ERROR", "message": probe_data["error"]}
        }

    valid_duration = math.isclose(probe_data["duration"], 11.0, abs_tol=0.05)
    valid_frames = probe_data["nb_frames"] == 660
    valid_fps = probe_data["r_frame_rate"] == "60/1"
    
    probe_data["valid"] = valid_duration and valid_frames and valid_fps

    # --- 4. CONSOLIDACIÓN DE MANIFIESTO ---
    manifest_data = {
        "challenge_id": challenge_id,
        "telemetry": telemetry,
        "artifacts": {
            "raw_video": raw_video_path.name,
            "final_video": final_video_path.name
        },
        "validation": probe_data
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    if not probe_data["valid"]:
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_VALIDATION_FAILED",
                "message": "Las métricas extraídas no cumplen el contrato E2E.",
                "details": probe_data
            }
        }

    return {
        "success": True,
        "validate_only": False,
        "manifest_path": str(manifest_path),
        "video_path": str(final_video_path),
        "manifest": manifest_data
    }

def run_batch(challenges_dir_str: str, base_output_dir_str: str, validate_only: bool = False) -> Dict[str, Any]:
    """Ejecuta el procesamiento secuencial y determinista por lotes de desafíos."""
    challenges_dir = Path(challenges_dir_str).resolve()
    base_output_dir = Path(base_output_dir_str).resolve()
    
    if not challenges_dir.exists() or not challenges_dir.is_dir():
        return {
            "success": False,
            "error": {"code": "DIR_NOT_FOUND", "message": f"El directorio de desafíos no existe: {challenges_dir}"}
        }

    # Descubrimiento determinista ordenado alfabéticamente
    config_files = sorted(challenges_dir.glob("CHALLENGE_*.json"))
    
    if not config_files:
        return {
            "success": False,
            "error": {"code": "NO_CHALLENGES_FOUND", "message": f"No se encontraron archivos CHALLENGE_*.json en {challenges_dir}"}
        }

    base_output_dir.mkdir(parents=True, exist_ok=True)
    batch_manifest_path = base_output_dir / "BATCH_MANIFEST.json"

    passed_count = 0
    failed_count = 0
    challenges_results = []

    for cfg_path in config_files:
        # Aislamiento de salida por subdirectorio para cada desafío
        challenge_id = read_challenge_id(cfg_path)
        sub_output_dir = base_output_dir / challenge_id
        
        print(f"[BATCH] Procesando {challenge_id} desde {cfg_path.name}...")
        res = run_factory(str(cfg_path), str(sub_output_dir), validate_only)
        
        if res["success"]:
            passed_count += 1
            rel_manifest = f"{challenge_id}/{challenge_id}_manifest.json"
            challenges_results.append({
                "challenge_id": challenge_id,
                "status": "PASS",
                "manifest": rel_manifest
            })
            print(f"[BATCH] -> {challenge_id}: PASS")
        else:
            failed_count += 1
            err_info = res.get("error", {"code": "UNKNOWN_ERROR", "message": "Error desconocido en factoría"})
            challenges_results.append({
                "challenge_id": challenge_id,
                "status": "FAIL",
                "error": err_info
            })
            print(f"[BATCH] -> {challenge_id}: FAIL [{err_info.get('code')}] {err_info.get('message')}")

    batch_status = "PASSED" if failed_count == 0 else "FAILED"
    batch_manifest_data = {
        "factory_version": "0.5.0",
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
    parser = argparse.ArgumentParser(description="Pause Challenge Engine - Build Factory (Batch & Unit)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", help="Ruta al archivo JSON unitario de configuración del challenge")
    group.add_argument("--batch", help="Directorio que contiene los archivos CHALLENGE_*.json para procesamiento por lotes")
    
    parser.add_argument("--output", default="./output", help="Directorio raíz de salida de los artefactos")
    parser.add_argument("--validate-only", action="store_true", help="Ejecutar validación matemática sin empaquetar video")
    args = parser.parse_args()

    if args.config:
        result = run_factory(args.config, args.output, args.validate_only)
    else:
        result = run_batch(args.batch, args.output, args.validate_only)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if not result["success"]:
        sys.exit(1)