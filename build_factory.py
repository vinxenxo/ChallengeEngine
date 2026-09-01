import os
import sys
import json
import subprocess
import argparse
import math
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# C6-D3 / FACTORY CONTRACT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

FACTORY_VERSION = "0.10.0"
MANIFEST_VERSION = "1.0"

# GIF de preview: obligatorio salvo --no-gif explícito.
GIF_FPS = 30
GIF_WIDTH = 540
GIF_HEIGHT = 960

DECLARATIVE_METADATA_FIELDS = (
    "schema_version",
    "engine_version",
    "mechanic",
    "mechanic_version",
    "video_profile_version",
    "asset_family_version",
)


# ============================================================
# WORKSPACE
# ============================================================

def sanitize_workspace(output_dir: Path) -> None:
    """
    Limpia únicamente residuos canónicos directamente situados
    en la raíz de output.

    No toca carpetas CHALLENGE_* porque contienen los artefactos
    certificados de cada desafío y se gestionan individualmente.
    """
    if not output_dir.exists():
        return

    residual_patterns = [
        "CHALLENGE_*_raw.avi",
        "CHALLENGE_*.mp4",
        "CHALLENGE_*.gif",
        "CHALLENGE_*_manifest.json",
    ]

    for pattern in residual_patterns:
        for filepath in output_dir.glob(pattern):
            if filepath.is_file():
                try:
                    filepath.unlink()
                    print(
                        "[WORKSPACE-SANITIZER] "
                        f"Residuo eliminado: {filepath.name}"
                    )
                except Exception as exc:
                    print(
                        "[WORKSPACE-SANITIZER] "
                        f"Advertencia: no se pudo eliminar "
                        f"{filepath.name}: {exc}"
                    )


# ============================================================
# CONFIG
# ============================================================

def read_challenge_id(
    config_path: Path
) -> Optional[str]:
    """Obtiene challenge_id únicamente desde la definición declarativa."""
    try:
        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        return (
            data.get("challenge_id")
            if isinstance(data, dict)
            else None
        )

    except Exception as exc:
        print(
            '[ERROR_JSON] '
            f'{{"error":"CONFIG_READ_ERROR",'
            f'"message":"No se pudo leer '
            f'{config_path.name}: {exc}"}}'
        )
        return None


def read_challenge_definition(
    config_path: Path
) -> Dict[str, Any]:
    """Carga la definición JSON sin completarla ni modificarla."""
    try:
        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

    except Exception as exc:
        raise ValueError(
            f"No se pudo leer {config_path.name}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"La configuración {config_path.name} "
            "no contiene un objeto JSON válido."
        )

    return data


def build_declarative_metadata(
    challenge_definition: Dict[str, Any]
) -> Dict[str, Any]:
    """Construye snapshot exacto de provenance declarativo."""
    return {
        field: challenge_definition[field]
        for field in DECLARATIVE_METADATA_FIELDS
        if field in challenge_definition
    }


def read_rng_version(
    challenge_definition: Dict[str, Any]
) -> Optional[str]:
    """Obtiene generation.rng_version sin defaults."""
    generation = challenge_definition.get("generation")

    if (
        not isinstance(generation, dict)
        or "rng_version" not in generation
    ):
        return None

    return generation["rng_version"]


# ============================================================
# OUTPUT CLEANUP / HASH
# ============================================================

def cleanup_partial_outputs(
    output_dir: Path,
    challenge_id: str
) -> None:
    """Elimina todos los artefactos canónicos parciales del challenge."""
    for path in (
        output_dir / f"{challenge_id}_raw.avi",
        output_dir / f"{challenge_id}.mp4",
        output_dir / f"{challenge_id}.gif",
        output_dir / f"{challenge_id}_manifest.json",
    ):
        try:
            if path.exists() or path.is_symlink():
                path.unlink()
        except OSError as exc:
            print(
                "[WARN_CLEANUP] "
                f"No se pudo eliminar {path}: {exc}"
            )


def compute_file_sha256(
    file_path: Path,
    chunk_size: int = 65536
) -> Optional[str]:
    """Calcula SHA-256 del archivo físico."""
    if not file_path.is_file():
        return None

    sha256_hash = hashlib.sha256()

    try:
        with open(
            file_path,
            "rb"
        ) as f:
            for byte_block in iter(
                lambda: f.read(chunk_size),
                b""
            ):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    except Exception as exc:
        print(
            "[WARN_HASH] "
            f"No se pudo calcular SHA-256 para "
            f"{file_path.name}: {exc}"
        )
        return None


# ============================================================
# TIMELINE
# ============================================================

def duration_to_frames(
    duration_seconds: float,
    fps: int
) -> int:
    """
    Conversión determinista segundos -> frames.
    Mantiene la política histórica de la factoría.
    """
    return max(
        0,
        math.floor(
            duration_seconds * float(fps) + 0.5
        )
    )


def build_timeline_from_definition(
    video_config: Dict[str, Any]
) -> Dict[str, int]:
    """Construye timeline esperado únicamente desde video.* declarativo."""
    if not isinstance(video_config, dict):
        raise ValueError(
            "video debe ser un objeto JSON."
        )

    if "fps" not in video_config:
        raise ValueError(
            "video.fps obligatorio."
        )

    expected_fps = video_config["fps"]

    if (
        type(expected_fps) not in (int, float)
        or not math.isfinite(float(expected_fps))
        or float(expected_fps) <= 0.0
    ):
        raise ValueError(
            "video.fps inválido."
        )

    fps = int(expected_fps)

    hook_frames = duration_to_frames(
        float(
            video_config.get(
                "hook_duration",
                2.0
            )
        ),
        fps
    )

    game_frames = duration_to_frames(
        float(
            video_config.get(
                "game_duration",
                7.0
            )
        ),
        fps
    )

    reveal_frames = duration_to_frames(
        float(
            video_config.get(
                "reveal_duration",
                0.0
            )
        ),
        fps
    )

    cta_frames = duration_to_frames(
        float(
            video_config.get(
                "cta_duration",
                2.0
            )
        ),
        fps
    )

    total_frames = (
        hook_frames
        + game_frames
        + reveal_frames
        + cta_frames
    )

    return {
        "fps": fps,
        "hook_frames": hook_frames,
        "game_frames": game_frames,
        "reveal_frames": reveal_frames,
        "cta_frames": cta_frames,
        "total_frames": total_frames,
    }


# ============================================================
# GIF
# ============================================================

def generate_gif_preview(
    mp4_path: Path,
    gif_path: Path
) -> None:
    """
    Genera preview GIF 540x960 a 30fps.
    Palette adaptativa en dos pasos para preservar calidad.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(mp4_path),
        "-vf",
        (
            "fps=30,"
            "scale=540:960:flags=lanczos,"
            "split[s0][s1];"
            "[s0]palettegen="
            "stats_mode=diff:"
            "max_colors=256[p];"
            "[s1][p]paletteuse="
            "dither=sierra2_4a"
        ),
        "-loop",
        "0",
        str(gif_path),
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or "FFmpeg no pudo generar el GIF."
        )

    if (
        not gif_path.is_file()
        or gif_path.stat().st_size <= 0
    ):
        raise RuntimeError(
            "FFmpeg indicó éxito pero el GIF "
            "no existe o está vacío."
        )


def run_gif_probe(
    gif_path: Path
) -> Dict[str, Any]:
    """
    Inspección mínima del GIF para certificar que existe como
    stream GIF válido y que mantiene 540x960.
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,avg_frame_rate,nb_frames,duration",
        "-of",
        "json",
        str(gif_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        probe = json.loads(result.stdout)
        streams = probe.get("streams")

        if (
            not isinstance(streams, list)
            or not streams
            or not isinstance(streams[0], dict)
        ):
            return {
                "error": (
                    "FFprobe no devolvió un stream GIF válido."
                )
            }

        stream = streams[0]

        width = stream.get("width")
        height = stream.get("height")
        frame_rate = stream.get("avg_frame_rate")
        nb_frames = stream.get("nb_frames")
        duration = stream.get("duration")

        if width != GIF_WIDTH:
            return {
                "error": (
                    f"GIF width inválido: {width}; "
                    f"esperado {GIF_WIDTH}."
                )
            }

        if height != GIF_HEIGHT:
            return {
                "error": (
                    f"GIF height inválido: {height}; "
                    f"esperado {GIF_HEIGHT}."
                )
            }

        return {
            "width": width,
            "height": height,
            "avg_frame_rate": frame_rate,
            "nb_frames": (
                int(nb_frames)
                if nb_frames not in (None, "", "N/A")
                else None
            ),
            "duration": (
                float(duration)
                if duration not in (None, "", "N/A")
                else None
            ),
        }

    except subprocess.CalledProcessError as exc:
        return {
            "error": (
                exc.stderr.strip()
                or "FFprobe GIF terminó con error."
            )
        }

    except (
        json.JSONDecodeError,
        OSError,
        ValueError,
    ) as exc:
        return {"error": str(exc)}


# ============================================================
# VIDEO PROBE
# ============================================================

def run_ffprobe(
    video_path: Path
) -> Dict[str, Any]:
    """Extrae observaciones del stream principal de vídeo."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-count_frames",
        "-show_entries",
        "stream=r_frame_rate,nb_read_frames,duration",
        "-of",
        "json",
        str(video_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        probe_data = json.loads(
            result.stdout
        )

        streams = probe_data.get("streams")

        if (
            not isinstance(streams, list)
            or not streams
        ):
            return {
                "error": (
                    "FFprobe no devolvió "
                    "información de stream de vídeo."
                )
            }

        stream_info = streams[0]

        if not isinstance(
            stream_info,
            dict
        ):
            return {
                "error": (
                    "FFprobe devolvió un stream "
                    "de vídeo inválido."
                )
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
                    "FFprobe no proporcionó los campos "
                    "requeridos: "
                    + ", ".join(missing)
                )
            }

        duration_raw = stream_info["duration"]
        frames_raw = stream_info["nb_read_frames"]
        fps_raw = stream_info["r_frame_rate"]

        if duration_raw in (
            None,
            "",
            "N/A",
        ):
            return {
                "error": (
                    "FFprobe devolvió duration "
                    "ausente o N/A."
                )
            }

        if frames_raw in (
            None,
            "",
            "N/A",
        ):
            return {
                "error": (
                    "FFprobe devolvió nb_read_frames "
                    "ausente o N/A."
                )
            }

        if fps_raw in (
            None,
            "",
        ):
            return {
                "error": (
                    "FFprobe devolvió r_frame_rate "
                    "ausente."
                )
            }

        try:
            duration = float(
                duration_raw
            )
        except (
            ValueError,
            TypeError,
        ):
            return {
                "error": (
                    "FFprobe duration inválida: "
                    f"{duration_raw!r}"
                )
            }

        try:
            nb_frames = int(
                frames_raw
            )
        except (
            ValueError,
            TypeError,
        ):
            return {
                "error": (
                    "FFprobe nb_read_frames "
                    f"inválido: {frames_raw!r}"
                )
            }

        if not math.isfinite(
            duration
        ):
            return {
                "error": (
                    "FFprobe duration no finita: "
                    f"{duration!r}"
                )
            }

        if nb_frames < 0:
            return {
                "error": (
                    "FFprobe nb_read_frames negativo: "
                    f"{nb_frames}"
                )
            }

        if (
            not isinstance(
                fps_raw,
                str
            )
            or "/"
            not in fps_raw
        ):
            return {
                "error": (
                    "FFprobe r_frame_rate inválido: "
                    f"{fps_raw!r}"
                )
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

    except (
        json.JSONDecodeError,
        OSError,
    ) as exc:
        return {"error": str(exc)}


# ============================================================
# FACTORY
# ============================================================

def run_factory(
    config_path_str: str,
    output_dir_str: str,
    validate_only: bool = False,
    no_gif: bool = False,
) -> Dict[str, Any]:

    config_path = Path(
        config_path_str
    ).resolve()

    base_output_dir = Path(
        output_dir_str
    ).resolve()

    if not config_path.exists():
        return {
            "success": False,
            "error": {
                "code": "FILE_NOT_FOUND",
                "message": (
                    "Config file not found: "
                    f"{config_path}"
                ),
            },
        }

    try:
        challenge_definition = (
            read_challenge_definition(
                config_path
            )
        )

        challenge_id = (
            read_challenge_id(
                config_path
            )
        )

        declarative_metadata = (
            build_declarative_metadata(
                challenge_definition
            )
        )

        source_rng_version = (
            read_rng_version(
                challenge_definition
            )
        )

        timeline_cfg = (
            build_timeline_from_definition(
                challenge_definition.get(
                    "video",
                    {}
                )
            )
        )

    except ValueError as exc:
        return {
            "success": False,
            "error": {
                "code": "CONFIG_READ_ERROR",
                "message": str(exc),
            },
        }

    if not challenge_id:
        return {
            "success": False,
            "error": {
                "code": "MISSING_CHALLENGE_ID",
                "message": (
                    "challenge_id ausente en "
                    f"{config_path.name}"
                ),
            },
        }

    if "mechanic" not in challenge_definition:
        return {
            "success": False,
            "error": {
                "code": "MISSING_MECHANIC",
                "message": (
                    "mechanic ausente en "
                    f"{config_path.name}"
                ),
            },
        }

    output_dir = (
        base_output_dir
        / challenge_id
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    raw_video_path = (
        output_dir
        / f"{challenge_id}_raw.avi"
    )

    final_video_path = (
        output_dir
        / f"{challenge_id}.mp4"
    )

    gif_path = (
        output_dir
        / f"{challenge_id}.gif"
    )

    manifest_path = (
        output_dir
        / f"{challenge_id}_manifest.json"
    )

    fps = timeline_cfg["fps"]
    expected_total_frames = (
        timeline_cfg["total_frames"]
    )

    # ========================================================
    # 1. GODOT
    # ========================================================

    cmd = [
        "godot",
        "--path",
        str(PROJECT_ROOT),
    ]

    if validate_only:
        cmd.append("--headless")
    else:
        cmd.extend(
            [
                "--write-movie",
                str(raw_video_path),
                "--fixed-fps",
                str(fps),
                "--quit-after",
                str(expected_total_frames),
            ]
        )

    cmd.extend(
        [
            "--",
            f"--config={config_path}",
        ]
    )

    if validate_only:
        cmd.append("--validate-only")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=str(PROJECT_ROOT),
    )

    stdout, stderr = (
        process.communicate()
    )

    telemetry: Optional[
        Dict[str, Any]
    ] = None

    error_payload: Optional[
        Dict[str, Any]
    ] = None

    for line in stdout.splitlines():
        line_clean = line.strip()

        if line_clean.startswith(
            "[TELEMETRY_JSON]"
        ):
            try:
                telemetry = json.loads(
                    line_clean[
                        len("[TELEMETRY_JSON]") :
                    ].strip()
                )
            except json.JSONDecodeError:
                pass

        elif line_clean.startswith(
            "[ERROR_JSON]"
        ):
            try:
                error_payload = json.loads(
                    line_clean[
                        len("[ERROR_JSON]") :
                    ].strip()
                )
            except json.JSONDecodeError:
                pass

    if (
        process.returncode != 0
        or error_payload is not None
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        err_msg = (
            error_payload.get(
                "message",
                "Godot process failed."
            )
            if error_payload
            else stderr.strip()
        )

        return {
            "success": False,
            "error": (
                error_payload
                or {
                    "code":
                        "GODOT_EXECUTION_ERROR",
                    "message": err_msg,
                }
            ),
        }

    if telemetry is None:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code": "MISSING_TELEMETRY",
                "message": (
                    "Godot did not emit "
                    "[TELEMETRY_JSON]."
                ),
            },
        }

    # ========================================================
    # RNG provenance gate
    # ========================================================

    telemetry_rng_version = telemetry.get(
        "rng_version"
    )

    if source_rng_version is None:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "MISSING_RNG_VERSION",
                "message": (
                    "generation.rng_version "
                    "es obligatorio en Capa 0."
                ),
            },
        }

    if (
        telemetry_rng_version
        != source_rng_version
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "RNG_VERSION_MISMATCH",
                "message": (
                    "rng_version mismatch: "
                    f"{source_rng_version} vs "
                    f"{telemetry_rng_version}"
                ),
            },
        }

    # ========================================================
    # Validate-only
    # ========================================================

    if validate_only:
        return {
            "success": True,
            "validate_only": True,
            "telemetry": telemetry,
            "declarative_metadata":
                declarative_metadata,
            "challenge_id":
                challenge_id,
        }

    # ========================================================
    # 2. RAW GATE
    # ========================================================

    if (
        not raw_video_path.exists()
        or raw_video_path.stat().st_size <= 0
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "MISSING_RAW_VIDEO",
                "message":
                    "Godot no generó RAW AVI válido.",
            },
        }

    # ========================================================
    # 3. MP4
    # ========================================================

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(raw_video_path),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        str(final_video_path),
    ]

    ffmpeg_proc = subprocess.run(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if ffmpeg_proc.returncode != 0:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "FFMPEG_ERROR",
                "message":
                    ffmpeg_proc.stderr.strip(),
            },
        }

    # ========================================================
    # 4. GIF C6-D3
    # ========================================================

    gif_hash: Optional[str] = None
    gif_probe: Optional[
        Dict[str, Any]
    ] = None

    if not no_gif:
        try:
            generate_gif_preview(
                final_video_path,
                gif_path
            )

            gif_probe = run_gif_probe(
                gif_path
            )

            if "error" in gif_probe:
                raise RuntimeError(
                    gif_probe["error"]
                )

            gif_hash = (
                compute_file_sha256(
                    gif_path
                )
            )

            if not gif_hash:
                raise RuntimeError(
                    "No se pudo calcular "
                    "SHA-256 del GIF."
                )

        except Exception as exc:
            cleanup_partial_outputs(
                output_dir,
                challenge_id
            )

            return {
                "success": False,
                "error": {
                    "code":
                        "GIF_GENERATION_ERROR",
                    "message":
                        str(exc),
                },
            }

    # ========================================================
    # 5. FFPROBE MP4
    # ========================================================

    probe_data = run_ffprobe(
        final_video_path
    )

    if "error" in probe_data:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "FFPROBE_ERROR",
                "message":
                    probe_data["error"],
            },
        }

    # ========================================================
    # 6. CONSISTENCY GATE C5-A
    # ========================================================

    expected_fps = (
        challenge_definition[
            "video"
        ]["fps"]
    )

    required_timeline_keys = (
        "total_frames",
        "hook_frames",
        "game_frames",
        "reveal_frames",
        "cta_frames",
    )

    if any(
        key not in telemetry
        for key in required_timeline_keys
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "MISSING_TELEMETRY_TIMELINE",
                "message":
                    "Telemetría temporal incompleta.",
            },
        }

    t_total = telemetry[
        "total_frames"
    ]

    t_hook = telemetry[
        "hook_frames"
    ]

    t_game = telemetry[
        "game_frames"
    ]

    t_reveal = telemetry[
        "reveal_frames"
    ]

    t_cta = telemetry[
        "cta_frames"
    ]

    if any(
        type(value) is not int
        for value in (
            t_total,
            t_hook,
            t_game,
            t_reveal,
            t_cta,
        )
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "INVALID_TELEMETRY_TIMELINE",
                "message":
                    "Timeline debe ser entero.",
            },
        }

    if t_total != (
        t_hook
        + t_game
        + t_reveal
        + t_cta
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "TIMELINE_INTEGRITY_VIOLATION",
                "message":
                    "Suma de frames incorrecta.",
            },
        }

    if t_total != expected_total_frames:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "TIMELINE_DECLARATIVE_MISMATCH",
                "message": (
                    "Telemetría no coincide con "
                    "video.* declarativo."
                ),
            },
        }

    expected_duration = (
        t_total
        / float(expected_fps)
    )

    if probe_data[
        "nb_frames"
    ] != t_total:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "ARTIFACT_FRAME_COUNT_MISMATCH",
                "message":
                    "Frames FFprobe != Telemetría.",
            },
        }

    if not math.isclose(
        probe_data["duration"],
        expected_duration,
        abs_tol=0.05,
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "ARTIFACT_DURATION_MISMATCH",
                "message":
                    "Duración física errónea.",
            },
        }

    expected_rate = (
        f"{int(expected_fps)}/1"
    )

    if probe_data[
        "r_frame_rate"
    ] != expected_rate:
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "ARTIFACT_FRAMERATE_MISMATCH",
                "message":
                    "Framerate erróneo.",
            },
        }

    probe_data["valid"] = True

    # ========================================================
    # 7. HASHES
    # ========================================================

    raw_hash = compute_file_sha256(
        raw_video_path
    )

    final_hash = compute_file_sha256(
        final_video_path
    )

    if (
        not raw_hash
        or not final_hash
    ):
        cleanup_partial_outputs(
            output_dir,
            challenge_id
        )

        return {
            "success": False,
            "error": {
                "code":
                    "HASH_GENERATION_FAILED",
                "message": (
                    "No se pudo calcular "
                    "SHA-256 de los artefactos."
                ),
            },
        }

    # ========================================================
    # 8. MANIFEST
    # ========================================================

    manifest_data = {
        "manifest_version":
            MANIFEST_VERSION,

        "factory_version":
            FACTORY_VERSION,

        "challenge_id":
            challenge_id,

        "declarative_metadata":
            declarative_metadata,

        "telemetry":
            telemetry,

        "artifacts": {
            "raw_video":
                raw_video_path.name,

            "raw_video_sha256":
                raw_hash,

            "final_video":
                final_video_path.name,

            "final_video_sha256":
                final_hash,
        },

        "validation":
            probe_data,

        "status":
            "PASS",
    }

    if not no_gif:
        manifest_data[
            "artifacts"
        ][
            "preview_gif"
        ] = gif_path.name

        manifest_data[
            "artifacts"
        ][
            "preview_gif_sha256"
        ] = gif_hash

        manifest_data[
            "gif_validation"
        ] = {
            "valid": True,
            "width": GIF_WIDTH,
            "height": GIF_HEIGHT,
            "fps": GIF_FPS,
            "probe": gif_probe,
        }

    else:
        manifest_data[
            "gif_validation"
        ] = {
            "valid": False,
            "disabled":
                True,
            "policy_exception":
                "--no-gif",
        }

    with open(
        manifest_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            manifest_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    return {
        "success": True,
        "validate_only": False,
        "manifest_path":
            str(manifest_path),
        "video_path":
            str(final_video_path),
        "manifest":
            manifest_data,
    }


# ============================================================
# BATCH WORKER
# ============================================================

def _process_single_challenge(
    cfg_path: Path,
    base_output_dir: Path,
    validate_only: bool,
    no_gif: bool
) -> tuple[
    str,
    Dict[str, Any]
]:
    challenge_id = (
        read_challenge_id(
            cfg_path
        )
        or cfg_path.stem
    )

    print(
        "[BATCH-WORKER] Iniciando "
        f"{challenge_id} desde "
        f"{cfg_path.name}..."
    )

    result = run_factory(
        str(cfg_path),
        str(base_output_dir),
        validate_only,
        no_gif,
    )

    print(
        "[BATCH-WORKER] Finalizado "
        f"{challenge_id} -> "
        f"{'PASS' if result['success'] else 'FAIL'}"
    )

    return (
        challenge_id,
        result
    )


# ============================================================
# MANIFEST READ / AUDIT
# ============================================================

def read_unit_manifest(
    manifest_path: Path
) -> Dict[str, Any]:
    try:
        with open(
            manifest_path,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

    except FileNotFoundError:
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_MISSING",
                "message":
                    f"No existe el manifiesto: "
                    f"{manifest_path}",
            },
        }

    except (
        OSError,
        json.JSONDecodeError,
    ) as exc:
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_NOT_CERTIFIED",
                "message":
                    f"Error leyendo manifiesto: "
                    f"{exc}",
            },
        }

    if not isinstance(
        data,
        dict
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_NOT_CERTIFIED",
                "message":
                    "Manifiesto no es un objeto JSON.",
            },
        }

    return {
        "valid": True,
        "manifest": data
    }


def _validate_artifact_path(
    challenge_dir: Path,
    filename: Any,
) -> Optional[Path]:
    if (
        not isinstance(
            filename,
            str
        )
        or not filename
    ):
        return None

    artifact_path = (
        challenge_dir
        / filename
    )

    try:
        artifact_path.resolve().relative_to(
            challenge_dir.resolve()
        )
    except ValueError:
        return None

    return artifact_path


def audit_unit_manifest(
    cfg_path: Path,
    base_output_dir: Path,
    execution_result: Dict[str, Any],
    require_gif: bool,
) -> Dict[str, Any]:
    """
    Auditoría C5-C/C5-D + C6-D3.

    La auditoría física vuelve a calcular SHA-256 y, cuando GIF
    está habilitado, exige que el GIF exista y esté certificado.
    """
    challenge_definition = (
        read_challenge_definition(
            cfg_path
        )
    )

    challenge_id = (
        challenge_definition.get(
            "challenge_id"
        )
    )

    if not challenge_id:
        return {
            "valid": False,
            "error": {
                "code":
                    "BATCH_CHALLENGE_COVERAGE_MISMATCH",
                "message":
                    "challenge_id ausente.",
            },
        }

    if not execution_result.get(
        "success",
        False
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "BATCH_INTEGRITY_GATE_FAILED",
                "message":
                    f"{challenge_id}: ejecución fallida.",
            },
        }

    challenge_dir = (
        base_output_dir
        / challenge_id
    )

    manifest_path = (
        challenge_dir
        / f"{challenge_id}_manifest.json"
    )

    manifest_read = read_unit_manifest(
        manifest_path
    )

    if not manifest_read["valid"]:
        return manifest_read

    manifest = manifest_read[
        "manifest"
    ]

    validation = manifest.get(
        "validation"
    )

    if (
        manifest.get(
            "status"
        ) != "PASS"
        or not isinstance(
            validation,
            dict
        )
        or validation.get(
            "valid"
        ) is not True
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_NOT_CERTIFIED",
                "message":
                    f"{challenge_id}: "
                    "manifiesto no certificado.",
            },
        }

    if (
        manifest.get(
            "challenge_id"
        )
        != challenge_id
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_ID_MISMATCH",
                "message":
                    f"{challenge_id}: ID mismatch.",
            },
        }

    declarative_metadata = (
        manifest.get(
            "declarative_metadata"
        )
    )

    if not isinstance(
        declarative_metadata,
        dict
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_DECLARATIVE_MISMATCH",
                "message":
                    f"{challenge_id}: "
                    "declarative_metadata inválido.",
            },
        }

    for field in (
        DECLARATIVE_METADATA_FIELDS
    ):
        if field in challenge_definition:
            if (
                field
                not in declarative_metadata
                or declarative_metadata[field]
                != challenge_definition[field]
            ):
                return {
                    "valid": False,
                    "error": {
                        "code":
                            "UNIT_MANIFEST_DECLARATIVE_MISMATCH",
                        "message":
                            f"{challenge_id}: "
                            f"campo {field} no coincide.",
                    },
                }

    source_rng_version = (
        read_rng_version(
            challenge_definition
        )
    )

    telemetry = manifest.get(
        "telemetry"
    )

    if (
        not isinstance(
            telemetry,
            dict
        )
        or telemetry.get(
            "rng_version"
        )
        != source_rng_version
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_MANIFEST_DECLARATIVE_MISMATCH",
                "message":
                    f"{challenge_id}: "
                    "rng_version mismatch.",
            },
        }

    # ========================================================
    # Artifact checks
    # ========================================================

    artifacts = manifest.get(
        "artifacts"
    )

    if not isinstance(
        artifacts,
        dict
    ):
        return {
            "valid": False,
            "error": {
                "code":
                    "UNIT_ARTIFACT_MISSING",
                "message":
                    f"{challenge_id}: "
                    "sección artifacts ausente.",
            },
        }

    checks = [
        (
            "raw_video",
            "raw_video_sha256"
        ),
        (
            "final_video",
            "final_video_sha256"
        ),
    ]

    # C6-D3: GIF obligatorio por defecto.
    if require_gif:
        if (
            "preview_gif"
            not in artifacts
            or "preview_gif_sha256"
            not in artifacts
        ):
            return {
                "valid": False,
                "error": {
                    "code":
                        "UNIT_GIF_MISSING",
                    "message":
                        f"{challenge_id}: "
                        "GIF de previsualización "
                        "obligatorio y no certificado.",
                },
            }

        checks.append(
            (
                "preview_gif",
                "preview_gif_sha256"
            )
        )

        gif_validation = manifest.get(
            "gif_validation"
        )

        if (
            not isinstance(
                gif_validation,
                dict
            )
            or gif_validation.get(
                "valid"
            ) is not True
        ):
            return {
                "valid": False,
                "error": {
                    "code":
                        "UNIT_GIF_NOT_CERTIFIED",
                    "message":
                        f"{challenge_id}: "
                        "gif_validation no certificado.",
                },
            }

    for file_key, hash_key in checks:

        filename = artifacts.get(
            file_key
        )

        declared_hash = artifacts.get(
            hash_key
        )

        if (
            not isinstance(
                filename,
                str
            )
            or not filename
            or not isinstance(
                declared_hash,
                str
            )
            or not declared_hash
        ):
            return {
                "valid": False,
                "error": {
                    "code":
                        "UNIT_ARTIFACT_MISSING",
                    "message":
                        f"{challenge_id}: falta "
                        f"declaración de {file_key} "
                        "o su hash.",
                },
            }

        artifact_path = (
            _validate_artifact_path(
                challenge_dir,
                filename,
            )
        )

        if artifact_path is None:
            return {
                "valid": False,
                "error": {
                    "code":
                        "UNIT_ARTIFACT_MISSING",
                    "message":
                        f"{challenge_id}: ruta de "
                        f"{file_key} fuera de límites.",
                },
            }

        if (
            not artifact_path.is_file()
            or artifact_path.stat().st_size <= 0
        ):
            return {
                "valid": False,
                "error": {
                    "code":
                        "UNIT_ARTIFACT_MISSING",
                    "message":
                        f"{challenge_id}: artefacto físico "
                        f"ausente: {filename}",
                },
            }

        current_hash = (
            compute_file_sha256(
                artifact_path
            )
        )

        if current_hash != declared_hash:
            return {
                "valid": False,
                "error": {
                    "code":
                        "UNIT_ARTIFACT_HASH_MISMATCH",
                    "message":
                        f"{challenge_id}: el hash SHA-256 "
                        f"de {filename} no coincide "
                        "con el manifiesto.",
                },
            }

    return {
        "valid": True,
        "challenge_id": challenge_id,
        "manifest": manifest,
        "manifest_path":
            str(manifest_path),
    }


# ============================================================
# BATCH MANIFEST
# ============================================================

def write_batch_manifest_atomic(
    batch_manifest_path: Path,
    batch_manifest_data: Dict[str, Any]
) -> None:

    temp_path = (
        batch_manifest_path.with_suffix(
            ".json.tmp"
        )
    )

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            batch_manifest_data,
            f,
            indent=2,
            ensure_ascii=False
        )

        f.flush()
        os.fsync(
            f.fileno()
        )

    temp_path.replace(
        batch_manifest_path
    )


# ============================================================
# BATCH
# ============================================================

def run_batch(
    challenges_dir_str: str,
    base_output_dir_str: str,
    validate_only: bool = False,
    no_gif: bool = False,
    workers: int = 1
) -> Dict[str, Any]:

    challenges_dir = Path(
        challenges_dir_str
    ).resolve()

    base_output_dir = Path(
        base_output_dir_str
    ).resolve()

    if (
        not challenges_dir.exists()
        or not challenges_dir.is_dir()
    ):
        return {
            "success": False,
            "error": {
                "code":
                    "DIR_NOT_FOUND",
                "message":
                    "Directorio no encontrado.",
            },
        }

    config_files = sorted(
        challenges_dir.glob(
            "CHALLENGE_*.json"
        )
    )

    if not config_files:
        return {
            "success": False,
            "error": {
                "code":
                    "NO_CHALLENGES_FOUND",
                "message":
                    "No hay challenges.",
            },
        }

    base_output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    sanitize_workspace(
        base_output_dir
    )

    batch_manifest_path = (
        base_output_dir
        / "BATCH_MANIFEST.json"
    )

    # ========================================================
    # D1 coverage
    # ========================================================

    challenge_ids = []

    for cfg_path in config_files:
        ch_id = read_challenge_id(
            cfg_path
        )

        if not ch_id:
            err = {
                "code":
                    "BATCH_CHALLENGE_COVERAGE_MISMATCH",
                "message":
                    f"{cfg_path.name} sin ID válido.",
            }

            batch_data = {
                "manifest_version":
                    MANIFEST_VERSION,
                "factory_version":
                    FACTORY_VERSION,
                "godot_versions": [],
                "rng_versions": [],
                "status":
                    "FAILED",
                "summary": {
                    "total":
                        len(config_files),
                    "passed":
                        0,
                    "failed":
                        len(config_files),
                },
                "challenges": [],
                "errors": [err],
            }

            write_batch_manifest_atomic(
                batch_manifest_path,
                batch_data
            )

            return {
                "success": False,
                "batch_manifest_path":
                    str(batch_manifest_path),
                "summary":
                    batch_data["summary"],
                "batch_manifest":
                    batch_data,
            }

        challenge_ids.append(
            ch_id
        )

    if len(challenge_ids) != len(
        set(challenge_ids)
    ):
        err = {
            "code":
                "BATCH_CHALLENGE_COVERAGE_MISMATCH",
            "message":
                "ID duplicados encontrados.",
        }

        batch_data = {
            "manifest_version":
                MANIFEST_VERSION,
            "factory_version":
                FACTORY_VERSION,
            "godot_versions": [],
            "rng_versions": [],
            "status":
                "FAILED",
            "summary": {
                "total":
                    len(config_files),
                "passed":
                    0,
                "failed":
                    len(config_files),
            },
            "challenges": [],
            "errors": [err],
        }

        write_batch_manifest_atomic(
            batch_manifest_path,
            batch_data
        )

        return {
            "success": False,
            "batch_manifest_path":
                str(batch_manifest_path),
            "summary":
                batch_data["summary"],
            "batch_manifest":
                batch_data,
        }

    # ========================================================
    # Workers
    # ========================================================

    raw_results: Dict[
        str,
        Dict[str, Any]
    ] = {}

    print(
        "[BATCH] Lanzando lote con "
        f"{len(config_files)} desafíos usando "
        f"{max(1, workers)} worker(s)..."
    )

    with ThreadPoolExecutor(
        max_workers=max(
            1,
            workers
        )
    ) as executor:

        future_to_config = {
            executor.submit(
                _process_single_challenge,
                cfg_path,
                base_output_dir,
                validate_only,
                no_gif,
            ): cfg_path
            for cfg_path in config_files
        }

        for future in as_completed(
            future_to_config
        ):

            cfg_path = future_to_config[
                future
            ]

            try:
                ch_id, result = (
                    future.result()
                )

                raw_results[
                    ch_id
                ] = result

            except Exception as exc:
                ch_id = (
                    read_challenge_id(
                        cfg_path
                    )
                    or cfg_path.stem
                )

                raw_results[
                    ch_id
                ] = {
                    "success": False,
                    "error": {
                        "code":
                            "WORKER_CRASH",
                        "message":
                            str(exc),
                    },
                }

    audited_manifests = {}
    challenges_results = []
    gate_errors = []

    # ========================================================
    # Validate-only batch
    # ========================================================

    if validate_only:

        for cfg_path in config_files:

            ch_id = read_challenge_id(
                cfg_path
            )

            exec_res = raw_results.get(
                ch_id,
                {
                    "success":
                        False,
                    "error": {
                        "code":
                            "MISSING_RESULT",
                        "message":
                            "Sin resultado.",
                    },
                }
            )

            if not exec_res.get(
                "success",
                False
            ):
                error = exec_res.get(
                    "error",
                    {
                        "code":
                            "BATCH_INTEGRITY_GATE_FAILED",
                        "message":
                            f"{ch_id}: "
                            "ejecución fallida.",
                    }
                )

                gate_errors.append(
                    {
                        "challenge_id":
                            ch_id,
                        **error,
                    }
                )

                challenges_results.append(
                    {
                        "challenge_id":
                            ch_id,
                        "status":
                            "FAIL",
                        "error":
                            error,
                    }
                )

                continue

            telemetry = exec_res.get(
                "telemetry",
                {}
            )

            declarative = (
                exec_res.get(
                    "declarative_metadata",
                    {}
                )
            )

            audited_manifests[
                ch_id
            ] = {
                "telemetry":
                    telemetry,
                "declarative_metadata":
                    declarative,
            }

            challenges_results.append(
                {
                    "challenge_id":
                        ch_id,
                    "status":
                        "PASS",
                    "mechanic":
                        declarative.get(
                            "mechanic"
                        ),
                    "rng_version":
                        telemetry.get(
                            "rng_version"
                        ),
                    "godot_version":
                        telemetry.get(
                            "godot_version"
                        ),
                }
            )

    # ========================================================
    # Artifact-certified batch
    # ========================================================

    else:

        for cfg_path in config_files:

            ch_id = read_challenge_id(
                cfg_path
            )

            exec_res = raw_results.get(
                ch_id,
                {
                    "success":
                        False,
                    "error": {
                        "code":
                            "MISSING_RESULT",
                        "message":
                            "Sin resultado.",
                    },
                }
            )

            audit = audit_unit_manifest(
                cfg_path,
                base_output_dir,
                exec_res,
                require_gif=not no_gif,
            )

            if not audit["valid"]:

                error = audit["error"]

                gate_errors.append(
                    {
                        "challenge_id":
                            ch_id,
                        **error,
                    }
                )

                challenges_results.append(
                    {
                        "challenge_id":
                            ch_id,
                        "status":
                            "FAIL",
                        "error":
                            error,
                    }
                )

                continue

            manifest = audit[
                "manifest"
            ]

            audited_manifests[
                ch_id
            ] = manifest

            telemetry = manifest.get(
                "telemetry",
                {}
            )

            declarative = manifest.get(
                "declarative_metadata",
                {}
            )

            challenge_result = {
                "challenge_id":
                    ch_id,
                "status":
                    "PASS",
                "mechanic":
                    declarative.get(
                        "mechanic"
                    ),
                "rng_version":
                    telemetry.get(
                        "rng_version"
                    ),
                "godot_version":
                    telemetry.get(
                        "godot_version"
                    ),
                "manifest":
                    f"{ch_id}/"
                    f"{ch_id}_manifest.json",
            }

            if not no_gif:
                challenge_result[
                    "preview_gif"
                ] = (
                    f"{ch_id}/"
                    f"{ch_id}.gif"
                )

            challenges_results.append(
                challenge_result
            )

    # ========================================================
    # Summary
    # ========================================================

    expected_count = len(
        config_files
    )

    passed_count = sum(
        1
        for item
        in challenges_results
        if item["status"] == "PASS"
    )

    failed_count = (
        expected_count
        - passed_count
    )

    godot_versions = sorted(
        {
            str(
                manifest
                .get(
                    "telemetry",
                    {}
                )
                .get(
                    "godot_version"
                )
            )
            for manifest
            in audited_manifests.values()
            if manifest
            .get(
                "telemetry",
                {}
            )
            .get(
                "godot_version"
            )
            is not None
        }
    )

    rng_versions = sorted(
        {
            str(
                manifest
                .get(
                    "telemetry",
                    {}
                )
                .get(
                    "rng_version"
                )
            )
            for manifest
            in audited_manifests.values()
            if manifest
            .get(
                "telemetry",
                {}
            )
            .get(
                "rng_version"
            )
            is not None
        }
    )

    batch_status = (
        "PASSED"
        if (
            failed_count == 0
            and not gate_errors
        )
        else
        "FAILED"
    )

    batch_manifest_data = {
        "manifest_version":
            MANIFEST_VERSION,

        "factory_version":
            FACTORY_VERSION,

        "godot_versions":
            godot_versions,

        "rng_versions":
            rng_versions,

        "status":
            batch_status,

        "summary": {
            "total":
                expected_count,
            "passed":
                passed_count,
            "failed":
                failed_count,
        },

        "challenges":
            challenges_results,
    }

    if not no_gif and not validate_only:
        batch_manifest_data[
            "preview_gif_policy"
        ] = {
            "enabled": True,
            "required": True,
            "fps": GIF_FPS,
            "width": GIF_WIDTH,
            "height": GIF_HEIGHT,
            "loop": True,
        }
    elif no_gif:
        batch_manifest_data[
            "preview_gif_policy"
        ] = {
            "enabled": False,
            "required": False,
            "exception":
                "--no-gif",
        }

    if gate_errors:
        batch_manifest_data[
            "errors"
        ] = gate_errors

    write_batch_manifest_atomic(
        batch_manifest_path,
        batch_manifest_data
    )

    return {
        "success":
            batch_status == "PASSED",

        "batch_manifest_path":
            str(batch_manifest_path),

        "summary":
            batch_manifest_data[
                "summary"
            ],

        "batch_manifest":
            batch_manifest_data,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Pause Challenge Engine - "
            "Build Factory C6-D3 "
            "(GIF + SHA-256)"
        )
    )

    group = (
        parser
        .add_mutually_exclusive_group(
            required=True
        )
    )

    group.add_argument(
        "--config",
        help=(
            "Ruta al archivo JSON "
            "unitario"
        )
    )

    group.add_argument(
        "--batch",
        help=(
            "Directorio con archivos "
            "CHALLENGE_*.json"
        )
    )

    parser.add_argument(
        "--output",
        default="./output",
        help=(
            "Directorio raíz "
            "de salida"
        )
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help=(
            "Validación matemática "
            "sin vídeo ni GIF"
        )
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Workers concurrentes"
    )

    parser.add_argument(
        "--no-gif",
        action="store_true",
        help=(
            "Excepción explícita: "
            "desactiva generación y "
            "certificación del GIF"
        )
    )

    args = parser.parse_args()

    if args.config:

        result = run_factory(
            args.config,
            args.output,
            args.validate_only,
            args.no_gif,
        )

    else:

        result = run_batch(
            args.batch,
            args.output,
            args.validate_only,
            args.no_gif,
            args.workers,
        )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )

    if not result["success"]:
        sys.exit(1)
