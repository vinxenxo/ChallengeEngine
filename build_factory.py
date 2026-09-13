import os
import sys
import json
import subprocess
import argparse
import math
import hashlib
import struct
from pathlib import Path
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# C8-A / FACTORY CONTRACT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

FACTORY_VERSION = "0.11.0"
MANIFEST_VERSION = "1.1"

GIF_FPS = 30
GIF_WIDTH = 540
GIF_HEIGHT = 960

SOURCE_VIDEO_WIDTH = 540
SOURCE_VIDEO_HEIGHT = 960
MASTER_OUTPUT_WIDTH = 1080
MASTER_OUTPUT_HEIGHT = 1920

DECLARATIVE_METADATA_FIELDS = (
    "schema_version",
    "engine_version",
    "mechanic",
    "mechanic_version",
    "video_profile_version",
    "asset_family_version",
)

AUDIO_SYNC_TOLERANCE_SECONDS = 0.05
PCM_PEAK_THRESHOLD = 100
AAC_MAX_VOLUME_THRESHOLD_DB = -90.0


# ============================================================
# WORKSPACE
# ============================================================

def sanitize_workspace(output_dir: Path) -> None:
    """Limpia residuos canónicos directamente situados en la raíz de output."""
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
                    print(f"[WORKSPACE-SANITIZER] Residuo eliminado: {filepath.name}")
                except Exception as exc:
                    print(
                        f"[WORKSPACE-SANITIZER] Advertencia: no se pudo eliminar "
                        f"{filepath.name}: {exc}"
                    )


# ============================================================
# CONFIG
# ============================================================

def read_challenge_id(config_path: Path) -> Optional[str]:
    """Obtiene challenge_id únicamente desde la definición declarativa."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("challenge_id") if isinstance(data, dict) else None
    except Exception as exc:
        print(
            '[ERROR_JSON] '
            f'{{"error":"CONFIG_READ_ERROR",'
            f'"message":"No se pudo leer {config_path.name}: {exc}"}}'
        )
        return None


def read_challenge_definition(config_path: Path) -> Dict[str, Any]:
    """Carga la definición JSON sin completarla ni modificarla."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        raise ValueError(f"No se pudo leer {config_path.name}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"La configuración {config_path.name} no contiene un objeto JSON válido."
        )
    return data


def build_declarative_metadata(challenge_definition: Dict[str, Any]) -> Dict[str, Any]:
    """Construye snapshot exacto de provenance declarativo."""
    return {
        field: challenge_definition[field]
        for field in DECLARATIVE_METADATA_FIELDS
        if field in challenge_definition
    }


def read_rng_version(challenge_definition: Dict[str, Any]) -> Optional[str]:
    """Obtiene generation.rng_version sin defaults."""
    generation = challenge_definition.get("generation")
    if not isinstance(generation, dict) or "rng_version" not in generation:
        return None
    return generation["rng_version"]


# ============================================================
# OUTPUT CLEANUP / HASH / C8-A PROVENANCE
# ============================================================

def cleanup_partial_outputs(output_dir: Path, challenge_id: str) -> None:
    """Elimina todos los artefactos canónicos parciales del challenge."""
    for path in (
        output_dir / f"{challenge_id}_raw.avi",
        output_dir / f"{challenge_id}.mp4",
        output_dir / f"{challenge_id}.gif",
        output_dir / f"{challenge_id}_manifest.json",
        output_dir / "audio_master.pcm",
    ):
        try:
            if path.exists() or path.is_symlink():
                path.unlink()
        except OSError as exc:
            print(f"[WARN_CLEANUP] No se pudo eliminar {path}: {exc}")


def compute_file_sha256(file_path: Path, chunk_size: int = 65536) -> Optional[str]:
    """Calcula SHA-256 del archivo físico."""
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


def require_file_sha256(file_path: Path, context: str) -> str:
    """Calcula SHA-256 de forma estricta (fail-closed)."""
    sha256 = compute_file_sha256(file_path)
    if sha256 is None:
        raise ValueError(
            f"C8-A: no se pudo calcular SHA-256 de {context}: {file_path}"
        )
    return sha256


def compute_bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_provenance_identity_sha256(provenance: Dict[str, Any]) -> str:
    """Calcula la identidad canónica del bloque provenance sin autorreferencia."""
    payload = {
        key: value
        for key, value in provenance.items()
        if key != "provenance_sha256"
    }

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return compute_bytes_sha256(canonical)


def run_git(args: list[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def build_git_provenance() -> Dict[str, Any]:
    commit = run_git(["rev-parse", "HEAD"])
    branch = run_git(["branch", "--show-current"])
    status = run_git(["status", "--porcelain", "--untracked-files=all"])

    if commit is None:
        raise ValueError("C8-A: no se pudo resolver el Git commit HEAD.")

    if status is None:
        raise ValueError("C8-A: no se pudo resolver el estado Git.")

    return {
        "commit": commit,
        "branch": branch or None,
        "dirty": bool(status),
    }


def resolve_res_references(value: Any) -> set[str]:
    """Extrae todos los paths res:// presentes en la definición declarativa."""
    found: set[str] = set()

    if isinstance(value, dict):
        for child in value.values():
            found.update(resolve_res_references(child))

    elif isinstance(value, list):
        for child in value:
            found.update(resolve_res_references(child))

    elif isinstance(value, str) and value.startswith("res://"):
        found.add(value)

    return found


def hash_res_references(
    challenge_definition: Dict[str, Any],
) -> list[Dict[str, str]]:
    result = []

    for res_path in sorted(resolve_res_references(challenge_definition)):
        relative_path = res_path.removeprefix("res://")
        physical_path = PROJECT_ROOT / relative_path

        sha256 = require_file_sha256(physical_path, f"res_reference ({res_path})")

        result.append({
            "path": res_path,
            "sha256": sha256,
        })

    return result


def resolve_unique_profile_file(profile_id: str) -> Optional[Path]:
    matches = sorted(
        path
        for path in (PROJECT_ROOT / "profiles").rglob(f"{profile_id}.json")
        if path.is_file()
    )

    if len(matches) > 1:
        raise ValueError(
            f"C8-A: profile_id ambiguo: {profile_id}. "
            f"Encontrados {len(matches)} archivos."
        )

    return matches[0] if matches else None


def build_profile_provenance(
    challenge_definition: Dict[str, Any],
) -> Dict[str, Any]:
    provenance: Dict[str, Any] = {}

    video_profile_id = challenge_definition.get("video_profile")
    if isinstance(video_profile_id, str):
        video_path = resolve_unique_profile_file(video_profile_id)

        if video_path is None:
            raise ValueError(
                f"C8-A: no se encontró archivo para video_profile "
                f"{video_profile_id!r}."
            )

        provenance["video_profile"] = {
            "id": video_profile_id,
            "path": str(video_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "sha256": require_file_sha256(video_path, "video_profile"),
        }

    return provenance


def build_audio_authoring_provenance(
    challenge_definition: Dict[str, Any],
) -> Dict[str, Any]:
    audio_root = PROJECT_ROOT / "profiles" / "audio"

    result = {
        "assets_catalog": None,
        "profiles": [],
    }

    catalog = audio_root / "audio_assets.json"

    if catalog.is_file():
        result["assets_catalog"] = {
            "path": str(catalog.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "sha256": require_file_sha256(catalog, "audio_assets_catalog"),
        }

    for profile_path in sorted(audio_root.glob("c7_profile_*.json")):
        result["profiles"].append({
            "path": str(profile_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "sha256": require_file_sha256(profile_path, "audio_profile_snapshot"),
        })

    return result


def build_provenance(
    config_path: Path,
    challenge_definition: Dict[str, Any],
) -> Dict[str, Any]:

    git_info = build_git_provenance()

    challenge_hash = require_file_sha256(config_path, "challenge_definition")

    provenance = {
        "git": git_info,
        "challenge_definition": {
            "path": str(config_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "sha256": challenge_hash,
        },
        "referenced_files": hash_res_references(
            challenge_definition
        ),
        "authoring": {
            "video": build_profile_provenance(
                challenge_definition
            ),
            "audio_authoring_snapshot": build_audio_authoring_provenance(
                challenge_definition
            ),
        },
    }

    provenance["provenance_sha256"] = compute_provenance_identity_sha256(
        provenance
    )

    return provenance


# ============================================================
# TIMELINE
# ============================================================

def duration_to_frames(duration_seconds: float, fps: int) -> int:
    """Conversión determinista segundos -> frames."""
    return max(0, math.floor(duration_seconds * float(fps) + 0.5))


def build_timeline_from_definition(video_config: Dict[str, Any]) -> Dict[str, int]:
    """Construye timeline esperado únicamente desde video.* declarativo."""
    if not isinstance(video_config, dict):
        raise ValueError("video debe ser un objeto JSON.")

    if "fps" not in video_config:
        raise ValueError("video.fps obligatorio.")

    expected_fps = video_config["fps"]
    if (
        type(expected_fps) not in (int, float)
        or not math.isfinite(float(expected_fps))
        or float(expected_fps) <= 0.0
    ):
        raise ValueError("video.fps inválido.")

    fps = int(expected_fps)
    hook_frames = duration_to_frames(float(video_config.get("hook_duration", 2.0)), fps)
    game_frames = duration_to_frames(float(video_config.get("game_duration", 7.0)), fps)
    reveal_frames = duration_to_frames(float(video_config.get("reveal_duration", 0.0)), fps)
    cta_frames = duration_to_frames(float(video_config.get("cta_duration", 2.0)), fps)

    total_frames = hook_frames + game_frames + reveal_frames + cta_frames

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

def generate_gif_preview(mp4_path: Path, gif_path: Path) -> None:
    """Genera preview GIF 540x960 a 30fps."""
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
            "[s0]palettegen=stats_mode=diff:max_colors=256[p];"
            "[s1][p]paletteuse=dither=sierra2_4a"
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
            result.stderr.strip() or "FFmpeg no pudo generar el GIF."
        )

    if not gif_path.is_file() or gif_path.stat().st_size <= 0:
        raise RuntimeError(
            "FFmpeg indicó éxito pero el GIF no existe o está vacío."
        )


def run_gif_probe(gif_path: Path) -> Dict[str, Any]:
    """Inspección mínima del GIF."""
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
            return {"error": "FFprobe no devolvió un stream GIF válido."}

        stream = streams[0]
        width = stream.get("width")
        height = stream.get("height")

        if width != GIF_WIDTH:
            return {"error": f"GIF width inválido: {width}; esperado {GIF_WIDTH}."}
        if height != GIF_HEIGHT:
            return {"error": f"GIF height inválido: {height}; esperado {GIF_HEIGHT}."}

        return {
            "width": width,
            "height": height,
            "avg_frame_rate": stream.get("avg_frame_rate"),
            "nb_frames": int(stream["nb_frames"])
            if stream.get("nb_frames") not in (None, "", "N/A")
            else None,
            "duration": float(stream["duration"])
            if stream.get("duration") not in (None, "", "N/A")
            else None,
        }
    except Exception as exc:
        return {"error": str(exc)}


# ============================================================
# VIDEO PROBE
# ============================================================

def run_ffprobe(video_path: Path) -> Dict[str, Any]:
    """Extrae observaciones del stream principal de vídeo RAW."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-count_frames",
        "-show_entries",
        "stream=width,height,codec_name,pix_fmt,r_frame_rate,nb_read_frames,duration",
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
        probe_data = json.loads(result.stdout)
        streams = probe_data.get("streams")

        if not isinstance(streams, list) or not streams:
            return {"error": "FFprobe no devolvió información de stream de vídeo."}

        stream_info = streams[0]
        required_fields = (
            "width",
            "height",
            "codec_name",
            "pix_fmt",
            "duration",
            "nb_read_frames",
            "r_frame_rate",
        )
        missing = [field for field in required_fields if field not in stream_info]
        if missing:
            return {"error": "FFprobe no proporcionó los campos requeridos: " + ", ".join(missing)}

        if stream_info["duration"] in (None, "", "N/A"):
            return {"error": "FFprobe devolvió duration ausente o N/A."}
        if stream_info["nb_read_frames"] in (None, "", "N/A"):
            return {"error": "FFprobe devolvió nb_read_frames ausente o N/A."}
        if stream_info["r_frame_rate"] in (None, ""):
            return {"error": "FFprobe devolvió r_frame_rate ausente."}

        try:
            width = int(stream_info["width"])
            height = int(stream_info["height"])
            duration = float(stream_info["duration"])
            nb_frames = int(stream_info["nb_read_frames"])
        except (TypeError, ValueError) as exc:
            return {"error": f"FFprobe parámetros inválidos: {exc}"}

        if not math.isfinite(duration):
            return {"error": f"FFprobe duration no finita: {duration!r}"}
        if nb_frames < 0:
            return {"error": f"FFprobe nb_read_frames negativo: {nb_frames}"}
        if not isinstance(stream_info["r_frame_rate"], str) or "/" not in stream_info["r_frame_rate"]:
            return {"error": f"FFprobe r_frame_rate inválido: {stream_info['r_frame_rate']!r}"}

        return {
            "width": width,
            "height": height,
            "codec_name": str(stream_info["codec_name"]),
            "pix_fmt": str(stream_info["pix_fmt"]),
            "duration": duration,
            "nb_frames": nb_frames,
            "r_frame_rate": stream_info["r_frame_rate"],
        }
    except subprocess.CalledProcessError as exc:
        return {"error": exc.stderr.strip() or "FFprobe terminó con código de error."}
    except (json.JSONDecodeError, OSError) as exc:
        return {"error": str(exc)}


# ============================================================
# C7-A1.4: AUDIO CONTENT AUDIT
# ============================================================

def analyze_pcm_content(pcm_path: Path) -> Dict[str, Any]:
    """Analiza la señal acústica física en el PCM crudo (s16le)."""
    if not pcm_path.is_file() or pcm_path.stat().st_size == 0:
        return {"valid": False, "error": "PCM ausente o vacío."}

    try:
        with open(pcm_path, "rb") as f:
            raw_data = f.read()

        if len(raw_data) % 2 != 0:
            return {"valid": False, "error": "PCM s16le con número impar de bytes."}

        sample_count = len(raw_data) // 2
        if sample_count == 0:
            return {"valid": False, "error": "PCM sin datos."}

        samples = struct.unpack(f"<{sample_count}h", raw_data)
        peak = max(abs(s) for s in samples)
        non_zero = sum(1 for s in samples if s != 0)
        sum_squares = sum(s * s for s in samples)
        rms = math.sqrt(sum_squares / sample_count)
        is_non_silent = peak > PCM_PEAK_THRESHOLD and non_zero > 0

        return {
            "valid": is_non_silent,
            "total_samples": sample_count,
            "non_zero_samples": non_zero,
            "non_zero_ratio": round(non_zero / float(sample_count), 4),
            "peak_amplitude": peak,
            "peak_normalized": round(peak / 32768.0, 4),
            "rms_amplitude": round(rms, 2),
            "is_silent": not is_non_silent,
        }
    except Exception as exc:
        return {"valid": False, "error": f"Error analizando PCM: {exc}"}


def analyze_mp4_audio_volume(mp4_path: Path) -> Dict[str, Any]:
    """Aplica volumedetect de FFmpeg al MP4 y audita energía del AAC."""
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(mp4_path),
        "-map",
        "0:a:0",
        "-af",
        "volumedetect",
        "-f",
        "null",
        "-",
    ]

    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if res.returncode != 0:
            return {
                "valid": False,
                "error": res.stderr.strip() or "volumedetect terminó con error.",
            }

        mean_vol = None
        max_vol = None

        for line in res.stderr.splitlines():
            if "mean_volume:" in line:
                try:
                    mean_vol = float(
                        line.split("mean_volume:", 1)[1]
                        .replace("dB", "")
                        .strip()
                    )
                except ValueError:
                    pass
            elif "max_volume:" in line:
                try:
                    max_vol = float(
                        line.split("max_volume:", 1)[1]
                        .replace("dB", "")
                        .strip()
                    )
                except ValueError:
                    pass

        if max_vol is None:
            return {
                "valid": False,
                "error": "volumedetect no emitió max_volume.",
            }

        is_non_silent = max_vol > AAC_MAX_VOLUME_THRESHOLD_DB

        return {
            "valid": is_non_silent,
            "mean_volume_db": mean_vol,
            "max_volume_db": max_vol,
            "is_silent": not is_non_silent,
        }
    except Exception as exc:
        return {"valid": False, "error": f"Error ejecutando volumedetect: {exc}"}


# ============================================================
# MASTER MP4 PROBE (C7-A1.3 + C7-A1.4)
# ============================================================

def run_master_probe(
    video_path: Path,
    pcm_path: Path,
    has_audio: bool,
) -> Dict[str, Any]:
    """Audita vídeo, audio/no-audio, A/V sync y contenido acústico."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-count_frames",
        "-show_entries",
        (
            "stream=index,codec_type,width,height,codec_name,pix_fmt,"
            "r_frame_rate,nb_read_frames,duration,sample_rate,channels,channel_layout"
        ),
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
        probe_data = json.loads(result.stdout)
        streams = probe_data.get("streams", [])

        video_stream = None
        audio_stream = None
        audio_stream_count = 0

        for stream in streams:
            if not isinstance(stream, dict):
                continue
            codec_type = stream.get("codec_type")
            if codec_type == "video" and video_stream is None:
                video_stream = stream
            elif codec_type == "audio":
                audio_stream_count += 1
                if audio_stream is None:
                    audio_stream = stream

        if video_stream is None:
            return {"error": "FFprobe no encontró stream de vídeo en el MP4 Master."}

        required_video_fields = (
            "width",
            "height",
            "codec_name",
            "pix_fmt",
            "duration",
            "nb_read_frames",
            "r_frame_rate",
        )
        missing_video = [field for field in required_video_fields if field not in video_stream]
        if missing_video:
            return {
                "error": (
                    "FFprobe no proporcionó campos de vídeo requeridos: "
                    + ", ".join(missing_video)
                )
            }

        try:
            v_width = int(video_stream["width"])
            v_height = int(video_stream["height"])
            v_duration = float(video_stream["duration"])
            v_nb_frames = int(video_stream["nb_read_frames"])
        except (TypeError, ValueError) as exc:
            return {"error": f"FFprobe parámetros de vídeo inválidos: {exc}"}

        video_validation = {
            "valid": True,
            "width": v_width,
            "height": v_height,
            "codec_name": str(video_stream["codec_name"]),
            "pix_fmt": str(video_stream["pix_fmt"]),
            "duration": v_duration,
            "nb_frames": v_nb_frames,
            "r_frame_rate": str(video_stream["r_frame_rate"]),
        }

        if has_audio:
            if audio_stream is None:
                return {
                    "error": (
                        "Audio habilitado pero FFprobe no encontró "
                        "stream de audio a:0 en el MP4 Master."
                    )
                }

            if audio_stream_count != 1:
                return {
                    "error": (
                        f"Audio habilitado pero se encontraron {audio_stream_count} "
                        "streams de audio; esperado exactamente 1."
                    )
                }

            a_codec = str(audio_stream.get("codec_name", ""))
            a_sample_rate_raw = audio_stream.get("sample_rate")
            a_channels_raw = audio_stream.get("channels")
            a_channel_layout = str(audio_stream.get("channel_layout", ""))
            a_duration_raw = audio_stream.get("duration")

            if a_codec != "aac":
                return {"error": f"Master audio codec must be aac; observed {a_codec}."}
            if a_sample_rate_raw in (None, "", "N/A"):
                return {"error": "FFprobe audio sample_rate ausente."}
            if a_channels_raw in (None, "", "N/A"):
                return {"error": "FFprobe audio channels ausente."}
            if a_duration_raw in (None, "", "N/A"):
                return {"error": "FFprobe audio duration ausente o N/A."}

            try:
                a_sample_rate = int(a_sample_rate_raw)
                a_channels = int(a_channels_raw)
                a_duration = float(a_duration_raw)
            except (TypeError, ValueError) as exc:
                return {"error": f"FFprobe parámetros de audio inválidos: {exc}"}

            if a_sample_rate != 44100:
                return {
                    "error": (
                        f"Master audio sample_rate must be 44100; observed {a_sample_rate}."
                    )
                }
            if a_channels != 1:
                return {
                    "error": f"Master audio channels must be 1 (mono); observed {a_channels}."
                }

            audio_validation = {
                "valid": True,
                "codec_name": a_codec,
                "sample_rate": a_sample_rate,
                "channels": a_channels,
                "channel_layout": "mono" if a_channels == 1 else a_channel_layout,
                "duration": a_duration,
            }

            av_diff = abs(v_duration - a_duration)
            av_sync_validation = {
                "valid": av_diff <= AUDIO_SYNC_TOLERANCE_SECONDS,
                "video_duration": v_duration,
                "audio_duration": a_duration,
                "diff": av_diff,
                "tolerance": AUDIO_SYNC_TOLERANCE_SECONDS,
            }

            if not av_sync_validation["valid"]:
                return {
                    "error": (
                        f"A/V sync mismatch: video duration {v_duration}s vs "
                        f"audio duration {a_duration}s (diff {av_diff}s > "
                        f"{AUDIO_SYNC_TOLERANCE_SECONDS}s tolerance)."
                    )
                }

            pcm_analysis = analyze_pcm_content(pcm_path)
            if not pcm_analysis["valid"]:
                return {
                    "error": (
                        "Auditoría física PCM fallida: "
                        f"{pcm_analysis.get('error', 'señal silenciosa')}"
                    )
                }

            aac_analysis = analyze_mp4_audio_volume(video_path)
            if not aac_analysis["valid"]:
                return {
                    "error": (
                        "Auditoría física AAC fallida: "
                        f"{aac_analysis.get('error', 'señal silenciosa')}"
                    )
                }

            audio_content_validation = {
                "valid": True,
                "pcm_signal": pcm_analysis,
                "aac_volume": aac_analysis,
            }

        else:
            if audio_stream_count != 0:
                return {
                    "error": (
                        "Audio deshabilitado pero el MP4 Master contiene "
                        f"{audio_stream_count} stream(s) de audio no autorizado(s)."
                    )
                }

            audio_validation = {
                "valid": True,
                "disabled": True,
                "audio_streams_found": 0,
            }
            av_sync_validation = {
                "valid": True,
                "disabled": True,
            }
            audio_content_validation = {
                "valid": True,
                "disabled": True,
            }

        return {
            "valid": True,
            "video": video_validation,
            "audio": audio_validation,
            "av_sync": av_sync_validation,
            "audio_content": audio_content_validation,
        }

    except subprocess.CalledProcessError as exc:
        return {
            "error": exc.stderr.strip() or "FFprobe Master terminó con código de error."
        }
    except (json.JSONDecodeError, OSError, ValueError) as exc:
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

    config_path = Path(config_path_str).resolve()
    base_output_dir = Path(output_dir_str).resolve()

    if not config_path.exists():
        return {
            "success": False,
            "error": {
                "code": "FILE_NOT_FOUND",
                "message": f"Config file not found: {config_path}",
            },
        }

    try:
        challenge_definition = read_challenge_definition(config_path)
        challenge_id = read_challenge_id(config_path)
        declarative_metadata = build_declarative_metadata(challenge_definition)
        source_rng_version = read_rng_version(challenge_definition)
        timeline_cfg = build_timeline_from_definition(
            challenge_definition.get("video", {})
        )
        provenance = build_provenance(config_path, challenge_definition)
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
                "message": f"challenge_id ausente en {config_path.name}",
            },
        }

    if "mechanic" not in challenge_definition:
        return {
            "success": False,
            "error": {
                "code": "MISSING_MECHANIC",
                "message": f"mechanic ausente en {config_path.name}",
            },
        }

    output_dir = base_output_dir / challenge_id
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_video_path = output_dir / f"{challenge_id}_raw.avi"
    final_video_path = output_dir / f"{challenge_id}.mp4"
    gif_path = output_dir / f"{challenge_id}.gif"
    manifest_path = output_dir / f"{challenge_id}_manifest.json"
    audio_pcm_path = output_dir / "audio_master.pcm"

    fps = timeline_cfg["fps"]
    expected_total_frames = timeline_cfg["total_frames"]

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
            f"--audio-output={audio_pcm_path}",
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

    stdout, stderr = process.communicate()

    telemetry: Optional[Dict[str, Any]] = None
    error_payload: Optional[Dict[str, Any]] = None
    audio_export_info: Optional[Dict[str, Any]] = None

    for line in stdout.splitlines():
        line_clean = line.strip()

        if line_clean.startswith("[TELEMETRY_JSON]"):
            try:
                telemetry = json.loads(
                    line_clean[len("[TELEMETRY_JSON]"):].strip()
                )
            except json.JSONDecodeError:
                pass

        elif line_clean.startswith("[AUDIO_EXPORT_JSON]"):
            try:
                audio_export_info = json.loads(
                    line_clean[len("[AUDIO_EXPORT_JSON]"):].strip()
                )
            except json.JSONDecodeError:
                pass

        elif line_clean.startswith("[ERROR_JSON]"):
            try:
                error_payload = json.loads(
                    line_clean[len("[ERROR_JSON]"):].strip()
                )
            except json.JSONDecodeError:
                pass

    if process.returncode != 0 or error_payload is not None:
        cleanup_partial_outputs(output_dir, challenge_id)

        err_msg = (
            error_payload.get("message", "Godot process failed.")
            if error_payload
            else stderr.strip()
        )

        return {
            "success": False,
            "error": error_payload or {
                "code": "GODOT_EXECUTION_ERROR",
                "message": err_msg,
            },
        }

    if telemetry is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_TELEMETRY",
                "message": "Godot no emitió [TELEMETRY_JSON].",
            },
        }

    # ========================================================
    # C7-A1.1: AUDIO EXPORT GATE — FAIL CLOSED
    # ========================================================

    if audio_export_info is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_AUDIO_EXPORT_JSON",
                "message": (
                    "Godot terminó sin error crítico pero no emitió "
                    "[AUDIO_EXPORT_JSON]. Violación de fail-closed."
                ),
            },
        }

    if not isinstance(audio_export_info, dict):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_AUDIO_EXPORT_JSON",
                "message": "[AUDIO_EXPORT_JSON] debe contener un objeto JSON.",
            },
        }

    if "audio_enabled" not in audio_export_info:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_AUDIO_EXPORT_JSON",
                "message": "[AUDIO_EXPORT_JSON] carece de la clave audio_enabled.",
            },
        }

    audio_enabled_raw = audio_export_info["audio_enabled"]
    if type(audio_enabled_raw) is not bool:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_AUDIO_EXPORT_JSON",
                "message": "audio_enabled debe ser booleano estricto.",
            },
        }

    has_audio = audio_enabled_raw
    audio_hash: Optional[str] = None

    if has_audio:
        if not audio_pcm_path.is_file() or audio_pcm_path.stat().st_size <= 0:
            cleanup_partial_outputs(output_dir, challenge_id)
            return {
                "success": False,
                "error": {
                    "code": "MISSING_AUDIO_PCM",
                    "message": "Audio habilitado pero el archivo PCM no existe o está vacío.",
                },
            }

        audio_hash = compute_file_sha256(audio_pcm_path)
        if not audio_hash:
            cleanup_partial_outputs(output_dir, challenge_id)
            return {
                "success": False,
                "error": {
                    "code": "AUDIO_HASH_FAILED",
                    "message": "No se pudo calcular SHA-256 del PCM canónico.",
                },
            }

    # ========================================================
    # RNG provenance gate
    # ========================================================

    telemetry_rng_version = telemetry.get("rng_version")
    if source_rng_version is None:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_RNG_VERSION",
                "message": "generation.rng_version es obligatorio en Capa 0.",
            },
        }

    if telemetry_rng_version != source_rng_version:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "RNG_VERSION_MISMATCH",
                "message": (
                    f"rng_version mismatch: {source_rng_version} vs "
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
            "declarative_metadata": declarative_metadata,
            "challenge_id": challenge_id,
            "audio_export": audio_export_info,
        }

    # ========================================================
    # 2. RAW GATE
    # ========================================================

    if not raw_video_path.exists() or raw_video_path.stat().st_size <= 0:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_RAW_VIDEO",
                "message": "Godot no generó RAW AVI válido.",
            },
        }

    # ========================================================
    # 3. SOURCE MOVIE GATE
    # ========================================================

    source_probe = run_ffprobe(raw_video_path)
    if "error" in source_probe:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "SOURCE_FFPROBE_ERROR",
                "message": source_probe["error"],
            },
        }

    if (
        source_probe["width"] != SOURCE_VIDEO_WIDTH
        or source_probe["height"] != SOURCE_VIDEO_HEIGHT
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "SOURCE_RESOLUTION_MISMATCH",
                "message": (
                    f"Source movie must be {SOURCE_VIDEO_WIDTH}x{SOURCE_VIDEO_HEIGHT}; "
                    f"observed {source_probe['width']}x{source_probe['height']}."
                ),
            },
        }

    # ========================================================
    # 4. MP4 MASTER — C7-A1.2
    # ========================================================

    if has_audio:
        if not audio_pcm_path.exists() or audio_pcm_path.stat().st_size <= 0:
            cleanup_partial_outputs(output_dir, challenge_id)
            return {
                "success": False,
                "error": {
                    "code": "MISSING_AUDIO_PCM",
                    "message": "Audio habilitado pero el archivo PCM no existe o está vacío.",
                },
            }

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(raw_video_path),
            "-f",
            "s16le",
            "-ar",
            "44100",
            "-ac",
            "1",
            "-i",
            str(audio_pcm_path),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-vf",
            f"scale={MASTER_OUTPUT_WIDTH}:{MASTER_OUTPUT_HEIGHT}:flags=lanczos",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(final_video_path),
        ]
    else:
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(raw_video_path),
            "-map",
            "0:v:0",
            "-vf",
            f"scale={MASTER_OUTPUT_WIDTH}:{MASTER_OUTPUT_HEIGHT}:flags=lanczos",
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
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "FFMPEG_ERROR",
                "message": ffmpeg_proc.stderr.strip(),
            },
        }

    # ========================================================
    # 5. GIF C6-D3
    # ========================================================

    gif_hash: Optional[str] = None
    gif_probe: Optional[Dict[str, Any]] = None

    if not no_gif:
        try:
            generate_gif_preview(final_video_path, gif_path)
            gif_probe = run_gif_probe(gif_path)
            if "error" in gif_probe:
                raise RuntimeError(gif_probe["error"])

            gif_hash = compute_file_sha256(gif_path)
            if not gif_hash:
                raise RuntimeError("No se pudo calcular SHA-256 del GIF.")
        except Exception as exc:
            cleanup_partial_outputs(output_dir, challenge_id)
            return {
                "success": False,
                "error": {
                    "code": "GIF_GENERATION_ERROR",
                    "message": str(exc),
                },
            }

    # ========================================================
    # 6. MASTER MP4 PROBE — C7-A1.3 + C7-A1.4
    # ========================================================

    probe_data = run_master_probe(
        final_video_path,
        audio_pcm_path,
        has_audio,
    )

    if "error" in probe_data:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "FFPROBE_ERROR",
                "message": probe_data["error"],
            },
        }

    v_probe = probe_data["video"]

    if (
        v_probe["width"] != MASTER_OUTPUT_WIDTH
        or v_probe["height"] != MASTER_OUTPUT_HEIGHT
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MASTER_RESOLUTION_MISMATCH",
                "message": (
                    f"Master MP4 must be {MASTER_OUTPUT_WIDTH}x{MASTER_OUTPUT_HEIGHT}; "
                    f"observed {v_probe['width']}x{v_probe['height']}."
                ),
            },
        }

    if v_probe["codec_name"] != "h264":
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MASTER_CODEC_MISMATCH",
                "message": (
                    f"Master codec must be h264; observed {v_probe['codec_name']}."
                ),
            },
        }

    if v_probe["pix_fmt"] not in ("yuv420p", "yuvj420p"):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MASTER_PIXEL_FORMAT_MISMATCH",
                "message": (
                    "Master pixel format must be yuv420p-compatible; "
                    f"observed {v_probe['pix_fmt']}."
                ),
            },
        }

    # ========================================================
    # 7. CONSISTENCY GATE C5-A
    # ========================================================

    expected_fps = challenge_definition["video"]["fps"]
    required_timeline_keys = (
        "total_frames",
        "hook_frames",
        "game_frames",
        "reveal_frames",
        "cta_frames",
    )

    if any(key not in telemetry for key in required_timeline_keys):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "MISSING_TELEMETRY_TIMELINE",
                "message": "Telemetría temporal incompleta.",
            },
        }

    t_total = telemetry["total_frames"]
    t_hook = telemetry["hook_frames"]
    t_game = telemetry["game_frames"]
    t_reveal = telemetry["reveal_frames"]
    t_cta = telemetry["cta_frames"]

    if any(
        type(value) is not int
        for value in (t_total, t_hook, t_game, t_reveal, t_cta)
    ):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "INVALID_TELEMETRY_TIMELINE",
                "message": "Timeline debe ser entero.",
            },
        }

    if t_total != t_hook + t_game + t_reveal + t_cta:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "TIMELINE_INTEGRITY_VIOLATION",
                "message": "Suma de frames incorrecta.",
            },
        }

    if t_total != expected_total_frames:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "TIMELINE_DECLARATIVE_MISMATCH",
                "message": "Telemetría no coincide con video.* declarativo.",
            },
        }

    expected_duration = t_total / float(expected_fps)

    if v_probe["nb_frames"] != t_total:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_FRAME_COUNT_MISMATCH",
                "message": "Frames FFprobe != Telemetría.",
            },
        }

    if not math.isclose(v_probe["duration"], expected_duration, abs_tol=AUDIO_SYNC_TOLERANCE_SECONDS):
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_DURATION_MISMATCH",
                "message": "Duración física errónea.",
            },
        }

    expected_rate = f"{int(expected_fps)}/1"
    if v_probe["r_frame_rate"] != expected_rate:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "ARTIFACT_FRAMERATE_MISMATCH",
                "message": "Framerate erróneo.",
            },
        }

    # ========================================================
    # 8. HASHES
    # ========================================================

    raw_hash = compute_file_sha256(raw_video_path)
    final_hash = compute_file_sha256(final_video_path)

    if not raw_hash or not final_hash:
        cleanup_partial_outputs(output_dir, challenge_id)
        return {
            "success": False,
            "error": {
                "code": "HASH_GENERATION_FAILED",
                "message": "No se pudo calcular SHA-256 de los artefactos.",
            },
        }

    # ========================================================
    # 9. MANIFEST (C8-A Provenance v1.1)
    # ========================================================

    manifest_data = {
        "manifest_version": MANIFEST_VERSION,
        "factory_version": FACTORY_VERSION,
        "challenge_id": challenge_id,
        "provenance": provenance,
        "declarative_metadata": declarative_metadata,
        "telemetry": telemetry,
        "artifacts": {
            "raw_video": raw_video_path.name,
            "raw_video_sha256": raw_hash,
            "final_video": final_video_path.name,
            "final_video_sha256": final_hash,
        },
        "output_contract": {
            "simulation_canvas": [1080, 1920],
            "source_movie": [SOURCE_VIDEO_WIDTH, SOURCE_VIDEO_HEIGHT],
            "master_mp4": [MASTER_OUTPUT_WIDTH, MASTER_OUTPUT_HEIGHT],
            "master_scale_filter": (
                f"scale={MASTER_OUTPUT_WIDTH}:{MASTER_OUTPUT_HEIGHT}:flags=lanczos"
            ),
        },
        "source_validation": source_probe,
        "validation": probe_data,
        "status": "PASS",
    }

    manifest_data["audio_export"] = dict(audio_export_info)
    if has_audio and audio_hash is not None:
        manifest_data["audio_export"]["audio_master_sha256"] = audio_hash

    if not no_gif:
        manifest_data["artifacts"]["preview_gif"] = gif_path.name
        manifest_data["artifacts"]["preview_gif_sha256"] = gif_hash
        manifest_data["gif_validation"] = {
            "valid": True,
            "width": GIF_WIDTH,
            "height": GIF_HEIGHT,
            "fps": GIF_FPS,
            "probe": gif_probe,
        }
    else:
        manifest_data["gif_validation"] = {
            "valid": False,
            "disabled": True,
            "policy_exception": "--no-gif",
        }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "validate_only": False,
        "manifest_path": str(manifest_path),
        "video_path": str(final_video_path),
        "manifest": manifest_data,
    }


# ============================================================
# BATCH WORKER
# ============================================================

def _process_single_challenge(
    cfg_path: Path,
    base_output_dir: Path,
    validate_only: bool,
    no_gif: bool,
) -> tuple[str, Dict[str, Any]]:
    challenge_id = read_challenge_id(cfg_path) or cfg_path.stem
    print(
        "[BATCH-WORKER] Iniciando "
        f"{challenge_id} desde {cfg_path.name}..."
    )

    result = run_factory(
        str(cfg_path),
        str(base_output_dir),
        validate_only,
        no_gif,
    )

    print(
        "[BATCH-WORKER] Finalizado "
        f"{challenge_id} -> {'PASS' if result['success'] else 'FAIL'}"
    )
    return challenge_id, result


# ============================================================
# MANIFEST READ / AUDIT
# ============================================================

def read_unit_manifest(manifest_path: Path) -> Dict[str, Any]:
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_MISSING",
                "message": f"No existe el manifiesto: {manifest_path}",
            },
        }
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_NOT_CERTIFIED",
                "message": f"Error leyendo manifiesto: {exc}",
            },
        }

    if not isinstance(data, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_NOT_CERTIFIED",
                "message": "Manifiesto no es un objeto JSON.",
            },
        }

    return {"valid": True, "manifest": data}


def _validate_artifact_path(challenge_dir: Path, filename: Any) -> Optional[Path]:
    if not isinstance(filename, str) or not filename:
        return None

    artifact_path = challenge_dir / filename
    try:
        artifact_path.resolve().relative_to(challenge_dir.resolve())
    except ValueError:
        return None
    return artifact_path


def audit_unit_manifest(
    cfg_path: Path,
    base_output_dir: Path,
    execution_result: Dict[str, Any],
    require_gif: bool,
) -> Dict[str, Any]:
    """Auditoría física del manifiesto unitario antes de agregarlo al lote."""
    try:
        challenge_definition = read_challenge_definition(cfg_path)
    except ValueError as exc:
        return {
            "valid": False,
            "error": {
                "code": "BATCH_CONFIG_READ_ERROR",
                "message": str(exc),
            },
        }

    challenge_id = challenge_definition.get("challenge_id")
    if not challenge_id:
        return {
            "valid": False,
            "error": {
                "code": "BATCH_CHALLENGE_COVERAGE_MISMATCH",
                "message": "challenge_id ausente.",
            },
        }

    if not execution_result.get("success", False):
        original_error = execution_result.get(
            "error",
            {
                "code": "BATCH_INTEGRITY_GATE_FAILED",
                "message": f"{challenge_id}: ejecución fallida.",
            },
        )
        return {
            "valid": False,
            "error": {
                "code": original_error.get("code", "BATCH_INTEGRITY_GATE_FAILED"),
                "message": (
                    f"{challenge_id}: "
                    f"{original_error.get('message', 'ejecución fallida.')}"
                ),
            },
        }

    challenge_dir = base_output_dir / challenge_id
    manifest_path = challenge_dir / f"{challenge_id}_manifest.json"

    manifest_read = read_unit_manifest(manifest_path)
    if not manifest_read["valid"]:
        return manifest_read

    manifest = manifest_read["manifest"]
    validation = manifest.get("validation")

    if (
        manifest.get("status") != "PASS"
        or not isinstance(validation, dict)
        or validation.get("valid") is not True
    ):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_NOT_CERTIFIED",
                "message": f"{challenge_id}: manifiesto no certificado.",
            },
        }

    if manifest.get("challenge_id") != challenge_id:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_ID_MISMATCH",
                "message": f"{challenge_id}: ID mismatch.",
            },
        }

    # ========================================================
    # C8-A PROVENANCE GATE
    # ========================================================

    provenance = manifest.get("provenance")

    if not isinstance(provenance, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_MISSING",
                "message": f"{challenge_id}: provenance ausente o inválida.",
            },
        }

    required_provenance_keys = {
        "git",
        "challenge_definition",
        "referenced_files",
        "authoring",
        "provenance_sha256",
    }

    missing_provenance_keys = sorted(
        key for key in required_provenance_keys
        if key not in provenance
    )

    if missing_provenance_keys:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_STRUCTURE_INVALID",
                "message": (
                    f"{challenge_id}: faltan claves de provenance: "
                    + ", ".join(missing_provenance_keys)
                ),
            },
        }

    declared_provenance_hash = provenance.get("provenance_sha256")

    if (
        not isinstance(declared_provenance_hash, str)
        or len(declared_provenance_hash) != 64
    ):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_HASH_INVALID",
                "message": (
                    f"{challenge_id}: provenance_sha256 no es "
                    "un SHA-256 hexadecimal válido."
                ),
            },
        }

    computed_provenance_hash = compute_provenance_identity_sha256(
        provenance
    )

    if computed_provenance_hash != declared_provenance_hash:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_HASH_MISMATCH",
                "message": (
                    f"{challenge_id}: provenance_sha256 no coincide "
                    "con el payload canónico."
                ),
            },
        }

    git_provenance = provenance.get("git")
    if not isinstance(git_provenance, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_GIT_INVALID",
                "message": f"{challenge_id}: provenance.git inválido.",
            },
        }

    if not isinstance(git_provenance.get("commit"), str):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_GIT_INVALID",
                "message": f"{challenge_id}: provenance.git.commit inválido.",
            },
        }

    challenge_provenance = provenance.get("challenge_definition")
    if not isinstance(challenge_provenance, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_DEFINITION_INVALID",
                "message": (
                    f"{challenge_id}: provenance.challenge_definition inválida."
                ),
            },
        }

    if (
        challenge_provenance.get("path")
        != str(cfg_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    ):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_DEFINITION_PATH_MISMATCH",
                "message": (
                    f"{challenge_id}: path de challenge_definition no coincide."
                ),
            },
        }

    current_definition_hash = require_file_sha256(
        cfg_path,
        "challenge_definition",
    )

    if challenge_provenance.get("sha256") != current_definition_hash:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_PROVENANCE_DEFINITION_HASH_MISMATCH",
                "message": (
                    f"{challenge_id}: hash de challenge_definition "
                    "no coincide con el archivo actual."
                ),
            },
        }

    declarative_metadata = manifest.get("declarative_metadata")
    if not isinstance(declarative_metadata, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_DECLARATIVE_MISMATCH",
                "message": f"{challenge_id}: declarative_metadata inválido.",
            },
        }

    for field in DECLARATIVE_METADATA_FIELDS:
        if field in challenge_definition:
            if (
                field not in declarative_metadata
                or declarative_metadata[field] != challenge_definition[field]
            ):
                return {
                    "valid": False,
                    "error": {
                        "code": "UNIT_MANIFEST_DECLARATIVE_MISMATCH",
                        "message": (
                            f"{challenge_id}: campo {field} no coincide."
                        ),
                    },
                }

    source_rng_version = read_rng_version(challenge_definition)
    telemetry = manifest.get("telemetry")
    if (
        not isinstance(telemetry, dict)
        or telemetry.get("rng_version") != source_rng_version
    ):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_MANIFEST_DECLARATIVE_MISMATCH",
                "message": f"{challenge_id}: rng_version mismatch.",
            },
        }

    audio_export = manifest.get("audio_export")
    if not isinstance(audio_export, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_AUDIO_EXPORT_MISSING",
                "message": f"{challenge_id}: audio_export ausente.",
            },
        }

    if "audio_enabled" not in audio_export or type(audio_export["audio_enabled"]) is not bool:
        return {
            "valid": False,
            "error": {
                "code": "UNIT_AUDIO_EXPORT_INVALID",
                "message": f"{challenge_id}: audio_export.audio_enabled inválido.",
            },
        }

    audio_enabled = audio_export["audio_enabled"]
    validation_audio = validation.get("audio")
    validation_av_sync = validation.get("av_sync")
    validation_audio_content = validation.get("audio_content")

    if not isinstance(validation_audio, dict) or not isinstance(validation_av_sync, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_AUDIO_VALIDATION_MISSING",
                "message": f"{challenge_id}: bloques de validación audio/av_sync ausentes.",
            },
        }

    if audio_enabled:
        if validation_audio.get("valid") is not True:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AUDIO_VALIDATION_FAILED",
                    "message": f"{challenge_id}: audio no certificado.",
                },
            }
        if validation_av_sync.get("valid") is not True:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AV_SYNC_VALIDATION_FAILED",
                    "message": f"{challenge_id}: A/V sync no certificado.",
                },
            }
        if (
            not isinstance(validation_audio_content, dict)
            or validation_audio_content.get("valid") is not True
        ):
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AUDIO_CONTENT_VALIDATION_FAILED",
                    "message": f"{challenge_id}: contenido acústico no certificado.",
                },
            }

        if "audio_master_sha256" not in audio_export:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AUDIO_HASH_MISSING",
                    "message": f"{challenge_id}: audio_master_sha256 ausente.",
                },
            }
    else:
        if validation_audio.get("disabled") is not True:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AUDIO_OFF_VALIDATION_FAILED",
                    "message": f"{challenge_id}: rama audio-off no certificada como disabled.",
                },
            }
        if validation_audio.get("audio_streams_found") != 0:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AUDIO_OFF_STREAM_PRESENT",
                    "message": f"{challenge_id}: audio-off pero existen streams de audio.",
                },
            }
        if validation_av_sync.get("disabled") is not True:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AV_SYNC_OFF_VALIDATION_FAILED",
                    "message": f"{challenge_id}: A/V sync debe estar disabled en audio-off.",
                },
            }
        if (
            not isinstance(validation_audio_content, dict)
            or validation_audio_content.get("disabled") is not True
        ):
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_AUDIO_CONTENT_OFF_VALIDATION_FAILED",
                    "message": f"{challenge_id}: audio_content debe estar disabled en audio-off.",
                },
            }

    # ========================================================
    # Artifact checks
    # ========================================================

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        return {
            "valid": False,
            "error": {
                "code": "UNIT_ARTIFACT_MISSING",
                "message": f"{challenge_id}: sección artifacts ausente.",
            },
        }

    checks = [
        ("raw_video", "raw_video_sha256"),
        ("final_video", "final_video_sha256"),
    ]

    if require_gif:
        if "preview_gif" not in artifacts or "preview_gif_sha256" not in artifacts:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_GIF_MISSING",
                    "message": f"{challenge_id}: GIF obligatorio y no certificado.",
                },
            }
        checks.append(("preview_gif", "preview_gif_sha256"))

        gif_validation = manifest.get("gif_validation")
        if not isinstance(gif_validation, dict) or gif_validation.get("valid") is not True:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_GIF_NOT_CERTIFIED",
                    "message": f"{challenge_id}: gif_validation no certificado.",
                },
            }

    for file_key, hash_key in checks:
        filename = artifacts.get(file_key)
        declared_hash = artifacts.get(hash_key)

        if (
            not isinstance(filename, str)
            or not filename
            or not isinstance(declared_hash, str)
            or not declared_hash
        ):
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_ARTIFACT_MISSING",
                    "message": f"{challenge_id}: falta declaración de {file_key} o su hash.",
                },
            }

        artifact_path = _validate_artifact_path(challenge_dir, filename)
        if artifact_path is None:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_ARTIFACT_MISSING",
                    "message": f"{challenge_id}: ruta de {file_key} fuera de límites.",
                },
            }

        if not artifact_path.is_file() or artifact_path.stat().st_size <= 0:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_ARTIFACT_MISSING",
                    "message": f"{challenge_id}: artefacto físico ausente: {filename}",
                },
            }

        current_hash = compute_file_sha256(artifact_path)
        if current_hash != declared_hash:
            return {
                "valid": False,
                "error": {
                    "code": "UNIT_ARTIFACT_HASH_MISMATCH",
                    "message": (
                        f"{challenge_id}: el hash SHA-256 de {filename} "
                        "no coincide con el manifiesto."
                    ),
                },
            }

    return {
        "valid": True,
        "challenge_id": challenge_id,
        "manifest": manifest,
        "manifest_path": str(manifest_path),
    }


# ============================================================
# BATCH MANIFEST
# ============================================================

def write_batch_manifest_atomic(
    batch_manifest_path: Path,
    batch_manifest_data: Dict[str, Any],
) -> None:
    temp_path = batch_manifest_path.with_suffix(".json.tmp")

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(batch_manifest_data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())

    temp_path.replace(batch_manifest_path)


# ============================================================
# BATCH — C7-A2
# ============================================================

def run_batch(
    challenges_dir_str: str,
    base_output_dir_str: str,
    validate_only: bool = False,
    no_gif: bool = False,
    workers: int = 1,
) -> Dict[str, Any]:

    challenges_dir = Path(challenges_dir_str).resolve()
    base_output_dir = Path(base_output_dir_str).resolve()

    if not challenges_dir.exists() or not challenges_dir.is_dir():
        return {
            "success": False,
            "error": {
                "code": "DIR_NOT_FOUND",
                "message": "Directorio no encontrado.",
            },
        }

    config_files = sorted(challenges_dir.glob("*CHALLENGE*.json"))

    if not config_files:
        return {
            "success": False,
            "error": {
                "code": "NO_CHALLENGES_FOUND",
                "message": "No hay challenges.",
            },
        }

    base_output_dir.mkdir(parents=True, exist_ok=True)
    sanitize_workspace(base_output_dir)
    batch_manifest_path = base_output_dir / "BATCH_MANIFEST.json"

    # ========================================================
    # Coverage
    # ========================================================

    challenge_ids = []
    for cfg_path in config_files:
        ch_id = read_challenge_id(cfg_path)
        if not ch_id:
            error = {
                "code": "BATCH_CHALLENGE_COVERAGE_MISMATCH",
                "message": f"{cfg_path.name} sin ID válido.",
            }
            batch_data = {
                "manifest_version": MANIFEST_VERSION,
                "factory_version": FACTORY_VERSION,
                "status": "FAILED",
                "summary": {
                    "total": len(config_files),
                    "passed": 0,
                    "failed": len(config_files),
                },
                "challenges": [],
                "errors": [error],
            }
            write_batch_manifest_atomic(batch_manifest_path, batch_data)
            return {
                "success": False,
                "batch_manifest_path": str(batch_manifest_path),
                "summary": batch_data["summary"],
                "batch_manifest": batch_data,
            }
        challenge_ids.append(ch_id)

    if len(challenge_ids) != len(set(challenge_ids)):
        error = {
            "code": "BATCH_CHALLENGE_COVERAGE_MISMATCH",
            "message": "ID duplicados encontrados.",
        }
        batch_data = {
            "manifest_version": MANIFEST_VERSION,
            "factory_version": FACTORY_VERSION,
            "status": "FAILED",
            "summary": {
                "total": len(config_files),
                "passed": 0,
                "failed": len(config_files),
            },
            "challenges": [],
            "errors": [error],
        }
        write_batch_manifest_atomic(batch_manifest_path, batch_data)
        return {
            "success": False,
            "batch_manifest_path": str(batch_manifest_path),
            "summary": batch_data["summary"],
            "batch_manifest": batch_data,
        }

    # ========================================================
    # Workers
    # ========================================================

    raw_results: Dict[str, Dict[str, Any]] = {}

    print(
        "[BATCH] Lanzando lote con "
        f"{len(config_files)} desafíos usando {max(1, workers)} worker(s)..."
    )

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
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

        for future in as_completed(future_to_config):
            cfg_path = future_to_config[future]
            try:
                ch_id, result = future.result()
                raw_results[ch_id] = result
            except Exception as exc:
                ch_id = read_challenge_id(cfg_path) or cfg_path.stem
                raw_results[ch_id] = {
                    "success": False,
                    "error": {
                        "code": "WORKER_CRASH",
                        "message": str(exc),
                    },
                }

    audited_manifests: Dict[str, Dict[str, Any]] = {}
    challenges_results = []
    gate_errors = []

    # ========================================================
    # Validate-only batch
    # ========================================================

    if validate_only:
        for cfg_path in config_files:
            ch_id = read_challenge_id(cfg_path)
            exec_res = raw_results.get(
                ch_id,
                {
                    "success": False,
                    "error": {
                        "code": "MISSING_RESULT",
                        "message": "Sin resultado.",
                    },
                },
            )

            if not exec_res.get("success", False):
                error = exec_res.get(
                    "error",
                    {
                        "code": "BATCH_INTEGRITY_GATE_FAILED",
                        "message": f"{ch_id}: ejecución fallida.",
                    },
                )
                gate_errors.append({"challenge_id": ch_id, **error})
                challenges_results.append({
                    "challenge_id": ch_id,
                    "status": "FAIL",
                    "error": error,
                })
                continue

            telemetry = exec_res.get("telemetry", {})
            declarative = exec_res.get("declarative_metadata", {})
            audio_export = exec_res.get("audio_export", {})

            audited_manifests[ch_id] = {
                "telemetry": telemetry,
                "declarative_metadata": declarative,
                "audio_export": audio_export,
            }

            challenges_results.append({
                "challenge_id": ch_id,
                "status": "PASS",
                "mechanic": declarative.get("mechanic"),
                "rng_version": telemetry.get("rng_version"),
                "godot_version": telemetry.get("godot_version"),
            })

    # ========================================================
    # Artifact-certified batch
    # ========================================================

    else:
        for cfg_path in config_files:
            ch_id = read_challenge_id(cfg_path)
            exec_res = raw_results.get(
                ch_id,
                {
                    "success": False,
                    "error": {
                        "code": "MISSING_RESULT",
                        "message": "Sin resultado.",
                    },
                },
            )

            audit = audit_unit_manifest(
                cfg_path,
                base_output_dir,
                exec_res,
                require_gif=not no_gif,
            )

            if not audit["valid"]:
                error = audit["error"]
                gate_errors.append({"challenge_id": ch_id, **error})
                challenges_results.append({
                    "challenge_id": ch_id,
                    "status": "FAIL",
                    "error": error,
                })
                continue

            manifest = audit["manifest"]
            audited_manifests[ch_id] = manifest
            telemetry = manifest.get("telemetry", {})
            declarative = manifest.get("declarative_metadata", {})
            audio_export = manifest.get("audio_export", {})

            challenge_result = {
                "challenge_id": ch_id,
                "status": "PASS",
                "mechanic": declarative.get("mechanic"),
                "rng_version": telemetry.get("rng_version"),
                "godot_version": telemetry.get("godot_version"),
                "audio_enabled": audio_export.get("audio_enabled"),
                "manifest": f"{ch_id}/{ch_id}_manifest.json",
            }

            if not no_gif:
                challenge_result["preview_gif"] = f"{ch_id}/{ch_id}.gif"

            challenges_results.append(challenge_result)

    # ========================================================
    # Summary + C7-A2 audio aggregation
    # ========================================================

    expected_count = len(config_files)
    passed_count = sum(
        1 for item in challenges_results if item["status"] == "PASS"
    )
    failed_count = expected_count - passed_count

    audio_enabled_count = 0
    audio_disabled_count = 0
    audio_content_valid_count = 0
    av_sync_valid_count = 0

    for manifest in audited_manifests.values():
        audio_export = manifest.get("audio_export", {})
        audio_enabled = audio_export.get("audio_enabled")

        if type(audio_enabled) is not bool:
            continue

        if audio_enabled:
            audio_enabled_count += 1
            validation = manifest.get("validation", {})

            if validation.get("audio_content", {}).get("valid", False):
                audio_content_valid_count += 1

            if validation.get("av_sync", {}).get("valid", False):
                av_sync_valid_count += 1
        else:
            audio_disabled_count += 1

    godot_versions = sorted({
        str(manifest.get("telemetry", {}).get("godot_version"))
        for manifest in audited_manifests.values()
        if manifest.get("telemetry", {}).get("godot_version") is not None
    })

    rng_versions = sorted({
        str(manifest.get("telemetry", {}).get("rng_version"))
        for manifest in audited_manifests.values()
        if manifest.get("telemetry", {}).get("rng_version") is not None
    })

    batch_status = (
        "PASSED"
        if failed_count == 0 and not gate_errors
        else "FAILED"
    )

    audio_summary = {
        "total_challenges": expected_count,
        "audited_challenges": len(audited_manifests),
        "audio_enabled": audio_enabled_count,
        "audio_disabled": audio_disabled_count,
        "audio_content_valid": audio_content_valid_count,
        "av_sync_valid": av_sync_valid_count,
    }

    if not validate_only and batch_status == "PASSED":
        if audio_enabled_count < 1 or audio_disabled_count < 1:
            batch_status = "FAILED"
            gate_errors.append({
                "code": "C7_A2_MIXED_BATCH_REQUIRED",
                "message": (
                    "C7-A2 requiere al menos un challenge audio-on y uno audio-off "
                    "en el mismo lote."
                ),
            })
            audio_summary["mixed_batch"] = False
        else:
            audio_summary["mixed_batch"] = True
    else:
        audio_summary["mixed_batch"] = (
            audio_enabled_count > 0 and audio_disabled_count > 0
        )

    batch_manifest_data = {
        "manifest_version": MANIFEST_VERSION,
        "factory_version": FACTORY_VERSION,
        "godot_versions": godot_versions,
        "rng_versions": rng_versions,
        "status": batch_status,
        "summary": {
            "total": expected_count,
            "passed": passed_count,
            "failed": failed_count,
        },
        "audio_summary": audio_summary,
        "challenges": challenges_results,
    }

    if not no_gif and not validate_only:
        batch_manifest_data["preview_gif_policy"] = {
            "enabled": True,
            "required": True,
            "fps": GIF_FPS,
            "width": GIF_WIDTH,
            "height": GIF_HEIGHT,
            "loop": True,
        }
    elif no_gif:
        batch_manifest_data["preview_gif_policy"] = {
            "enabled": False,
            "required": False,
            "exception": "--no-gif",
        }

    if gate_errors:
        batch_manifest_data["errors"] = gate_errors

    write_batch_manifest_atomic(batch_manifest_path, batch_manifest_data)

    return {
        "success": batch_status == "PASSED",
        "batch_manifest_path": str(batch_manifest_path),
        "summary": batch_manifest_data["summary"],
        "audio_summary": batch_manifest_data["audio_summary"],
        "batch_manifest": batch_manifest_data,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Pause Challenge Engine - Build Factory C8-A "
            "(Provenance & Release Identity)"
        )
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", help="Ruta al archivo JSON unitario")
    group.add_argument("--batch", help="Directorio con archivos *CHALLENGE*.json")

    parser.add_argument("--output", default="./output", help="Directorio raíz de salida")
    parser.add_argument("--validate-only", action="store_true", help="Validación matemática sin vídeo ni GIF")
    parser.add_argument("--workers", type=int, default=1, help="Workers concurrentes")
    parser.add_argument("--no-gif", action="store_true", help="Excepción explícita: desactiva GIF")

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

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result["success"]:
        sys.exit(1)