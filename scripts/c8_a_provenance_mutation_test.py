import sys
from pathlib import Path

# Agregar el directorio raíz al path para permitir la importación de build_factory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import shutil
import tempfile

import build_factory


PROJECT_ROOT = Path(build_factory.PROJECT_ROOT)
SOURCE_CONFIG = PROJECT_ROOT / "challenges_c7" / "CHALLENGE_001.json"
SOURCE_ASSET = PROJECT_ROOT / "assets" / "c6" / "garage_background.svg"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    with tempfile.TemporaryDirectory(
        prefix="c8a_provenance_",
        dir=PROJECT_ROOT / "tests",
    ) as temp_dir:

        temp_root = Path(temp_dir)

        # ----------------------------------------------------
        # Base challenge copy
        # ----------------------------------------------------
        config_a = temp_root / "challenge_a.json"

        challenge = build_factory.read_challenge_definition(
            SOURCE_CONFIG
        )

        config_a.write_text(
            json.dumps(
                challenge,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        provenance_a1 = build_factory.build_provenance(
            config_a,
            challenge,
        )

        provenance_a2 = build_factory.build_provenance(
            config_a,
            challenge,
        )

        # 1. Determinismo
        assert_true(
            provenance_a1["provenance_sha256"]
            == provenance_a2["provenance_sha256"],
            "C8-A.5 determinismo: hashes distintos para la misma entrada.",
        )

        # ----------------------------------------------------
        # 2. Sensibilidad declarativa
        # ----------------------------------------------------
        challenge_b = json.loads(
            config_a.read_text(encoding="utf-8")
        )

        challenge_b["theme"] = (
            str(challenge_b.get("theme", "generic")) + "_MUTATED"
        )

        config_b = temp_root / "challenge_b.json"

        config_b.write_text(
            json.dumps(
                challenge_b,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        provenance_b = build_factory.build_provenance(
            config_b,
            challenge_b,
        )

        assert_true(
            provenance_a1["challenge_definition"]["sha256"]
            != provenance_b["challenge_definition"]["sha256"],
            "C8-A.5 declarative: challenge_definition.sha256 no cambió.",
        )

        assert_true(
            provenance_a1["provenance_sha256"]
            != provenance_b["provenance_sha256"],
            "C8-A.5 declarative: provenance_sha256 no cambió.",
        )

        # ----------------------------------------------------
        # 3. Sensibilidad de asset res://
        # ----------------------------------------------------
        asset_copy = temp_root / "garage_background.svg"
        shutil.copy2(SOURCE_ASSET, asset_copy)

        asset_res_path = (
            f"res://{asset_copy.relative_to(PROJECT_ROOT).as_posix()}"
        )

        challenge_asset = json.loads(
            config_a.read_text(encoding="utf-8")
        )

        challenge_asset["provenance_test_asset"] = asset_res_path

        config_c = temp_root / "challenge_c.json"

        config_c.write_text(
            json.dumps(
                challenge_asset,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        provenance_c1 = build_factory.build_provenance(
            config_c,
            challenge_asset,
        )

        original_asset_hash = next(
            item["sha256"]
            for item in provenance_c1["referenced_files"]
            if item["path"] == asset_res_path
        )

        asset_bytes = asset_copy.read_bytes()
        asset_copy.write_bytes(
            asset_bytes + b"\n<!-- C8-A5 MUTATION -->\n"
        )

        provenance_c2 = build_factory.build_provenance(
            config_c,
            challenge_asset,
        )

        mutated_asset_hash = next(
            item["sha256"]
            for item in provenance_c2["referenced_files"]
            if item["path"] == asset_res_path
        )

        assert_true(
            original_asset_hash != mutated_asset_hash,
            "C8-A.5 asset: hash del asset no cambió tras mutación.",
        )

        assert_true(
            provenance_c1["provenance_sha256"]
            != provenance_c2["provenance_sha256"],
            "C8-A.5 asset: provenance_sha256 no propagó la mutación.",
        )

        print("[C8-A.5-TEST] Determinismo: PASS")
        print("[C8-A.5-TEST] Sensibilidad declarativa: PASS")
        print("[C8-A.5-TEST] Sensibilidad asset: PASS")

        # ----------------------------------------------------
        # Preparación de entorno autocontenido para auditoría (validate-only / mock artefactos)
        # ----------------------------------------------------
        audit_temp_base = temp_root / "audit_output"
        audit_challenge_dir = audit_temp_base / "CHALLENGE_001"
        audit_challenge_dir.mkdir(parents=True, exist_ok=True)

        # Generar manifiesto base canónico mínimo autocontenido utilizando build_provenance real
        base_provenance = build_factory.build_provenance(SOURCE_CONFIG, challenge)
        
        # Crear archivos de artefactos dummy requeridos por el auditor físico
        dummy_raw_video = audit_challenge_dir / "CHALLENGE_001_raw.avi"
        dummy_raw_video.write_bytes(b"DUMMY_RAW_AVI")
        dummy_raw_hash = build_factory.compute_file_sha256(dummy_raw_video)

        dummy_final_video = audit_challenge_dir / "CHALLENGE_001.mp4"
        dummy_final_video.write_bytes(b"DUMMY_FINAL_MP4")
        dummy_final_hash = build_factory.compute_file_sha256(dummy_final_video)

        dummy_gif = audit_challenge_dir / "CHALLENGE_001.gif"
        dummy_gif.write_bytes(b"DUMMY_GIF")
        dummy_gif_hash = build_factory.compute_file_sha256(dummy_gif)

        synthetic_manifest = {
            "manifest_version": build_factory.MANIFEST_VERSION,
            "factory_version": build_factory.FACTORY_VERSION,
            "challenge_id": "CHALLENGE_001",
            "provenance": base_provenance,
            "declarative_metadata": build_factory.build_declarative_metadata(challenge),
            "telemetry": {
                "rng_version": build_factory.read_rng_version(challenge),
                "godot_version": "4.7.1-stable (mock)",
                "total_frames": 540,
                "hook_frames": 0,
                "game_frames": 420,
                "reveal_frames": 0,
                "cta_frames": 120,
            },
            "artifacts": {
                "raw_video": dummy_raw_video.name,
                "raw_video_sha256": dummy_raw_hash,
                "final_video": dummy_final_video.name,
                "final_video_sha256": dummy_final_hash,
                "preview_gif": dummy_gif.name,
                "preview_gif_sha256": dummy_gif_hash,
            },
            "validation": {
                "valid": True,
                "video": {"valid": True, "width": 1080, "height": 1920, "codec_name": "h264", "pix_fmt": "yuv420p", "duration": 9.0, "nb_frames": 540, "r_frame_rate": "60/1"},
                "audio": {"valid": True, "codec_name": "aac", "sample_rate": 44100, "channels": 1, "channel_layout": "mono", "duration": 9.0},
                "av_sync": {"valid": True, "video_duration": 9.0, "audio_duration": 9.0, "diff": 0.0, "tolerance": 0.05},
                "audio_content": {
                    "valid": True,
                    "pcm_signal": {"valid": True, "total_samples": 396900, "non_zero_samples": 1000, "non_zero_ratio": 0.01, "peak_amplitude": 10000, "peak_normalized": 0.3, "rms_amplitude": 1000.0, "is_silent": False},
                    "aac_volume": {"valid": True, "mean_volume_db": -20.0, "max_volume_db": -3.0, "is_silent": False}
                }
            },
            "audio_export": {
                "audio_enabled": True,
                "audio_master_sha256": "0" * 64
            },
            "gif_validation": {
                "valid": True,
                "width": 540,
                "height": 960,
                "fps": 30
            },
            "status": "PASS"
        }

        manifest_copy_path = audit_challenge_dir / "CHALLENGE_001_manifest.json"

        # ----------------------------------------------------
        # 4. Provenance tampering gate (audit_unit_manifest)
        # ----------------------------------------------------
        tampered_provenance_manifest = json.loads(json.dumps(synthetic_manifest))
        tampered_provenance_manifest["provenance"]["provenance_sha256"] = "0" * 64
        manifest_copy_path.write_text(json.dumps(tampered_provenance_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

        audit_res_1 = build_factory.audit_unit_manifest(
            SOURCE_CONFIG,
            audit_temp_base,
            {"success": True},
            require_gif=True,
        )

        assert_true(
            not audit_res_1["valid"] and audit_res_1["error"]["code"] == "UNIT_PROVENANCE_HASH_MISMATCH",
            "C8-A.5 tamper provenance: el auditor no rechazó el hash corrupto.",
        )
        print("[C8-A.5-TEST] Provenance tampering gate: PASS")

        # ----------------------------------------------------
        # 5. Definition hash tampering gate (audit_unit_manifest)
        # ----------------------------------------------------
        tampered_def_manifest = json.loads(json.dumps(synthetic_manifest))
        tampered_def_manifest["provenance"]["challenge_definition"]["sha256"] = "0" * 64
        tampered_def_manifest["provenance"]["provenance_sha256"] = (
            build_factory.compute_provenance_identity_sha256(
                tampered_def_manifest["provenance"]
            )
        )
        manifest_copy_path.write_text(json.dumps(tampered_def_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

        audit_res_2 = build_factory.audit_unit_manifest(
            SOURCE_CONFIG,
            audit_temp_base,
            {"success": True},
            require_gif=True,
        )

        assert_true(
            not audit_res_2["valid"] and audit_res_2["error"]["code"] == "UNIT_PROVENANCE_DEFINITION_HASH_MISMATCH",
            "C8-A.5 tamper definition hash: el auditor no rechazó el hash de definición corrupto.",
        )
        print("[C8-A.5-TEST] Definition hash tampering gate: PASS")

        print("[C8-A.5-TEST] RESULTADO GLOBAL: PASS")


if __name__ == "__main__":
    main()