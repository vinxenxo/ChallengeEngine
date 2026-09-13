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
        # 4. Provenance tampering gate (audit_unit_manifest)
        # ----------------------------------------------------
        source_unit_dir = PROJECT_ROOT / "export" / "c8_a_unit_001" / "CHALLENGE_001"
        if source_unit_dir.exists():
            audit_temp_base = temp_root / "audit_output"
            audit_challenge_dir = audit_temp_base / "CHALLENGE_001"
            audit_challenge_dir.mkdir(parents=True, exist_ok=True)

            for item in source_unit_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, audit_challenge_dir / item.name)

            manifest_copy_path = audit_challenge_dir / "CHALLENGE_001_manifest.json"
            manifest_data = json.loads(manifest_copy_path.read_text(encoding="utf-8"))

            manifest_data["provenance"]["provenance_sha256"] = "0" * 64
            manifest_copy_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")

            fake_exec_result = {"success": True}
            audit_res = build_factory.audit_unit_manifest(
                PROJECT_ROOT / "challenges_c7" / "CHALLENGE_001.json",
                audit_temp_base,
                fake_exec_result,
                require_gif=True,
            )

            assert_true(
                not audit_res["valid"] and audit_res["error"]["code"] == "UNIT_PROVENANCE_HASH_MISMATCH",
                "C8-A.5 tamper provenance: el auditor no rechazó el hash corrupto.",
            )
            print("[C8-A.5-TEST] Provenance tampering gate: PASS")

        # ----------------------------------------------------
        # 5. Definition hash tampering gate (audit_unit_manifest)
        # ----------------------------------------------------
        if source_unit_dir.exists():
            for item in source_unit_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, audit_challenge_dir / item.name)

            manifest_copy_path = audit_challenge_dir / "CHALLENGE_001_manifest.json"
            manifest_data = json.loads(manifest_copy_path.read_text(encoding="utf-8"))

            manifest_data["provenance"]["challenge_definition"]["sha256"] = "0" * 64

            manifest_data["provenance"]["provenance_sha256"] = (
                build_factory.compute_provenance_identity_sha256(
                    manifest_data["provenance"]
                )
            )

            manifest_copy_path.write_text(
                json.dumps(
                    manifest_data,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            fake_exec_result = {"success": True}
            audit_res = build_factory.audit_unit_manifest(
                PROJECT_ROOT / "challenges_c7" / "CHALLENGE_001.json",
                audit_temp_base,
                fake_exec_result,
                require_gif=True,
            )

            assert_true(
                not audit_res["valid"] and audit_res["error"]["code"] == "UNIT_PROVENANCE_DEFINITION_HASH_MISMATCH",
                "C8-A.5 tamper definition hash: el auditor no rechazó el hash de definición corrupto.",
            )
            print("[C8-A.5-TEST] Definition hash tampering gate: PASS")

        print("[C8-A.5-TEST] RESULTADO GLOBAL: PASS")


if __name__ == "__main__":
    main()