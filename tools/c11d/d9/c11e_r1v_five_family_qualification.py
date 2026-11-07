#!/usr/bin/env python3
"""C11-E R1V bounded five-family C11-C source qualification and frame identity capture.

This runner is Windows-only by design. It calls only the five pinned C11-C family
PowerShell launchers, with -NoSound and the operator-approved exact silent MP4 encode
branch. It does not call D dispatch, D composition, D3, audio, mux, filters or delivery.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import zipfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO

FROZEN_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
STATIC_AUDIT_SHA256 = "600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92"
R1P_RUN_ID = "E4B_R1P_20261107_032743_5F75045C"
R1P_RECOVERED_ZIP_SHA256 = "d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52"
R1P_REPORT_CANONICAL_SHA256 = "9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41"
OPTION_C_RUN_ID = "OPTION_C_CONTRACT_20261107_151457_1746_A89CEBDA"
OPTION_C_REPORT_SHA256 = "ba76c626d92736c2f139380ec2b93d865015e8ef7e53f2881fdb16b6c4a54246"
OPTION_C_PROCESS_RECEIPT_SHA256 = "db1cc4b8393f84d944391efdd6daa325e0ed9a5aac69ce7b0d7efc9ed9ea9355"
OPTION_C_INSTALL_RECEIPT_SHA256 = "30c6531129a08d3ce347432ddb4d5a26155f92dc89863828398cbfc2a8dfe6a7"
OPTION_C_PACKAGE_MANIFEST_SHA256 = "b34bd464f0e23c8bba592d8620a56801b54c35f75d9140567949c0622447e695"
R1V_V1_PROPOSAL_SHA256 = "e0f9693584e5b7d42c6d67cf2c806ff691dec4644738458bd405cdcbd5d9c4db"
R1V_POLICY_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
C11D_PRODUCTION_POLICY_SHA256 = "cf970424b1b079d80cda41085a700129e094e90c87e48b04122c5acdabebae16"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
EXPECTED_C11C_OVERRIDE_BYTES = (
    b"[display]\r\n\r\n"
    b"window/size/viewport_width=720\r\n"
    b"window/size/viewport_height=1280\r\n"
    b"window/size/window_width_override=720\r\n"
    b"window/size/window_height_override=1280\r\n"
)

SELECTOR_EXPECTATIONS = [
    {
        "receipt_index": 6,
        "receipt_file": f"receipts/06_{R1P_RUN_ID}_06.json",
        "family_id": "c11c_fractal_bloom_v1",
        "internal_family_id": "fractal",
        "grammar_id": "radial_bloom",
        "grammar_index": 0,
        "launcher_sha256": "02e3721c92046f1f69119e5bbc6c69709dd0b97fad7191c08213ecc233930801",
        "prototype_sha256": "b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55",
        "scene_sha256": "806bed600f7550e7aa5c10175359c7ce545581ce206dc73e31c7c265cc398d5e",
        "gameplay_seed": 100006,
        "duration_seconds": 22.0,
        "fps": 30,
        "frame_count_consistency_only": 660,
        "output_prefix": "FractalBloom_v1",
        "source_folder_key": "fractal_bloom",
        "launcher_path": "tools/prototypes/c11c_fractal_bloom_v1/run_prototype.ps1",
        "prototype_path": "tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd",
        "scene_path": "tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.tscn",
    },
    {
        "receipt_index": 1,
        "receipt_file": f"receipts/01_{R1P_RUN_ID}_01.json",
        "family_id": "c11c_geometric_waves_v1",
        "internal_family_id": "geometric",
        "grammar_id": "harmonic_membrane",
        "grammar_index": 0,
        "launcher_sha256": "661bd61df61bc633e4b87cd4b9413c4317c8d4b6068194245aea7d40fcb5c7cd",
        "prototype_sha256": "ab2560cbe7fa42c5cad3b143aa59d1f2a0dc047682f7667983c7c0a0f6dbb61c",
        "scene_sha256": "11e214c6d8bba6003d7ef734477fdfc22cbe8238cae49c98692bd9b7487745fc",
        "gameplay_seed": 100001,
        "duration_seconds": 23.0,
        "fps": 30,
        "frame_count_consistency_only": 690,
        "output_prefix": "GeometricWaves_v1",
        "source_folder_key": "geometric_waves",
        "launcher_path": "tools/prototypes/c11c_geometric_waves_v1/run_prototype.ps1",
        "prototype_path": "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd",
        "scene_path": "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.tscn",
    },
    {
        "receipt_index": 21,
        "receipt_file": f"receipts/21_{R1P_RUN_ID}_21.json",
        "family_id": "c11c_invisible_forces_v1",
        "internal_family_id": "invisible_forces",
        "grammar_id": "dipole_field",
        "grammar_index": 0,
        "launcher_sha256": "88924dd86ebdc9b51a51f354ec22f40beb75cf6daafbe869283fa187568b6f60",
        "prototype_sha256": "a68661a5fdf792aa7fe701afa6fbf1631a2b8215c214032f58ecfe0c69d8374a",
        "scene_sha256": "85401c7c5a45283f90f090a28a1d0bb639d78dec4800e6eb730d60080972cb1c",
        "gameplay_seed": 100021,
        "duration_seconds": 22.0,
        "fps": 30,
        "frame_count_consistency_only": 660,
        "output_prefix": "InvisibleForces_v1",
        "source_folder_key": "invisible_forces",
        "launcher_path": "tools/prototypes/c11c_invisible_forces_v1/run_prototype.ps1",
        "prototype_path": "tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd",
        "scene_path": "tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.tscn",
    },
    {
        "receipt_index": 16,
        "receipt_file": f"receipts/16_{R1P_RUN_ID}_16.json",
        "family_id": "c11c_living_particles_v1",
        "internal_family_id": "living_particles",
        "grammar_id": "swarm",
        "grammar_index": 0,
        "launcher_sha256": "3674fdf778927022d2ebc1d1a96865b441479c5e4e71802e90837d654278a638",
        "prototype_sha256": "835ba0df2c160a259be39bd1977bfac0e6a66f903ce1aa6b4247af7c508ad94a",
        "scene_sha256": "b574dd963ea6556eff08ef1d6924f54e0b027238f98b717dc02e07584f22dfa1",
        "gameplay_seed": 100016,
        "duration_seconds": 20.0,
        "fps": 30,
        "frame_count_consistency_only": 600,
        "output_prefix": "LivingParticles_v1",
        "source_folder_key": "living_particles",
        "launcher_path": "tools/prototypes/c11c_living_particles_v1/run_prototype.ps1",
        "prototype_path": "tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd",
        "scene_path": "tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.tscn",
    },
    {
        "receipt_index": 11,
        "receipt_file": f"receipts/11_{R1P_RUN_ID}_11.json",
        "family_id": "c11c_sacred_symmetry_v1",
        "internal_family_id": "sacred_symmetry",
        "grammar_id": "astrolabe",
        "grammar_index": 0,
        "launcher_sha256": "8eea21f7b72f679d8951410597f0ecf968ac0a6f1ee629a48de965ea62b60b6e",
        "prototype_sha256": "12fdbc13e05df28b26cf95fe1907d150bd41f29196287700153521e9baee336b",
        "scene_sha256": "231e24928f0e4e8287b2fccc8fae4e6deec45eea4dbf4f7ac5cd9bec0676ffa5",
        "gameplay_seed": 100011,
        "duration_seconds": 23.0,
        "fps": 30,
        "frame_count_consistency_only": 690,
        "output_prefix": "SacredSymmetry_v1",
        "source_folder_key": "sacred_symmetry",
        "launcher_path": "tools/prototypes/c11c_sacred_symmetry_v1/run_prototype.ps1",
        "prototype_path": "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd",
        "scene_path": "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.tscn",
    },
]

# Direct runtime dependencies outside the existing 30-file R1P source pin set.
# The transitive Godot scene/prototype dependency graph is pinned as a complete set.
ADDITIONAL_SOURCE_PINS = {
    "project.godot": {"bytes": 868, "sha256": "d20b0f275c58a34881420705bb1990564d719427c550478c434345ced72805d3"},
    "tools/prototypes/c11c_common/C11CMovieCapture.ps1": {"bytes": 1943, "sha256": "916e95ebc01006efb436097df032626e666e3b1d80e2c50490c0eb2a3934ba1b"},
    "tools/prototypes/c11c_common/write_social_metadata.py": {"bytes": 5087, "sha256": "2fe823bde91ad5ac9b074827e9814e52e001a34917ccf51cc603a51170a789d7"},
    "assets/fonts/Inter-Bold.otf": {"bytes": 631880, "sha256": "9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d"},
    "assets/fonts/NotoSansMono-Regular.ttf": {"bytes": 510612, "sha256": "6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f"},
    "core/presentation/C11CVisualEditorialLayer.gd": {"bytes": 19047, "sha256": "f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d"},
    "core/presentation/C11CVisualTypography.gd": {"bytes": 2211, "sha256": "9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633"},
    "core/presentation/UnifiedSocialFrame.gd": {"bytes": 2087, "sha256": "d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba"},
    "core/presentation/UnifiedSocialFrame.tscn": {"bytes": 1471, "sha256": "a89051019ab78bc35757acaa8b46a3b62526432bfa86582f07a66187e80e1b4b"},
    "tools/prototypes/c11c_common/C11CColorBoost.gd": {"bytes": 478, "sha256": "ea585997b03aba00a13c3cb87640a7c626081316b43306093265757dd09c6607"},
    "tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd": {"bytes": 9631, "sha256": "44c4a9a11c334e6e84fcc1413667accac175781787866c3d6b894beeba3ea255"},
    "tools/prototypes/c11c_common/C11CTheme.gd": {"bytes": 255, "sha256": "7e73c62221ca8149a174b4633900b732b67047e0eddd20ee73e9d8f2f83cab64"},
}

# The 20 family-renderer/shader/scene resources not already covered by R1P.
for _k, _v in {
    "tools/prototypes/c11c_fractal_bloom_v1/FractalBloom.gdshader": (10052, "38288d4342afa2196b0e40aad7eddbbc012fab7e7664499ce2b0c302f658ba7c"),
    "tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.tscn": (224, "806bed600f7550e7aa5c10175359c7ce545581ce206dc73e31c7c265cc398d5e"),
    "tools/prototypes/c11c_fractal_bloom_v1/FractalBloomRenderer.gd": (3478, "78102f64829bda24ae56d50b5ad16a69b8674569b22133509e335649f08861f7"),
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader": (10073, "737149389a37d92f1f6947de93d89903aa5429eda23b1c8b261cc1ce3d6e7154"),
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.tscn": (230, "11e214c6d8bba6003d7ef734477fdfc22cbe8238cae49c98692bd9b7487745fc"),
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd": (3918, "4cf42e5e464e9aec86d7dd38caca226c1c451543c17ea87197d9acf8e8659783"),
    "tools/prototypes/c11c_invisible_forces_v1/InvisibleForces.gdshader": (7919, "7bd96b5dc504a7e64a4d1ba75505a71dd89e81accf175992a7299a8730d22f8d"),
    "tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.tscn": (233, "85401c7c5a45283f90f090a28a1d0bb639d78dec4800e6eb730d60080972cb1c"),
    "tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesRenderer.gd": (3069, "82c6a8d6913d462842258480010c44dceab439dc81a65d5517345bf948891c19"),
    "tools/prototypes/c11c_living_particles_v1/LivingParticles.gdshader": (8871, "b1ec5c82d8905617cb78d9a905d1d2194c1a5d54e6b3ee049ad6a6cd6c54305f"),
    "tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.tscn": (233, "b574dd963ea6556eff08ef1d6924f54e0b027238f98b717dc02e07584f22dfa1"),
    "tools/prototypes/c11c_living_particles_v1/LivingParticlesRenderer.gd": (4259, "99d6eada955e37b0273134117441dd4494e196d238277f18b4bbba7ad22b1b4c"),
    "tools/prototypes/c11c_living_particles_v1/LivingParticlesTronRoad.gd": (3849, "6e530a529f902a10bc3b9dacc580fd3c416da085c785c4aea2b2f3ddded91f54"),
    "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetry.gdshader": (11602, "4874060302443196a1c8646a4790670ff61c1b6b04d66d275989ab1bf9551d5d"),
    "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.tscn": (230, "231e24928f0e4e8287b2fccc8fae4e6deec45eea4dbf4f7ac5cd9bec0676ffa5"),
    "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryRenderer.gd": (3205, "4cb914ccdab0f7a4ec2f85670691ea90ac24e045ac1e5a8e696344a702397a26"),
}.items():
    ADDITIONAL_SOURCE_PINS[_k] = {"bytes": _v[0], "sha256": _v[1]}

OPTION_C_SOURCE_PINS = {
    "tools/c11d/d9/c11e_option_c_postcomposition_contract.py": {"bytes": 50143, "sha256": "fcf662bec8e2c7f689d428e7e6beb7d6c932ea441a3015111ef87fd58fbf107a"},
    "definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_DECISION_V1.json": {"bytes": 2342, "sha256": "22cec26baecfb6018a814750cc781143f5fa13f897d3dce708f6e9e074f669ac"},
    "definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_BOUNDARY_V1.json": {"bytes": 3576, "sha256": "795be1da157dd07fd4992d3ec6d7cf091a015eed72d16d86df13085db296098b"},
}

class R1VError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [canonical(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def dump_json(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    path.write_text(raw, encoding="utf-8", newline="\n")
    return sha256_file(path)


def load_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except Exception as exc:
        raise R1VError(f"Invalid JSON ({label}): {exc}") from exc


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise R1VError(f"Required JSON missing: {path}")
    return load_json_bytes(path.read_bytes(), str(path))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise R1VError(message)


def safe_project_file(project_root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative.replace("\\", "/"))
    require(not rel.is_absolute() and ".." not in rel.parts, f"Unsafe relative path: {relative}")
    path = project_root.joinpath(*rel.parts)
    require(path.resolve().is_relative_to(project_root.resolve()), f"Path escapes ProjectRoot: {relative}")
    return path


def verify_file_pin(project_root: Path, relative: str, pin: dict[str, Any]) -> dict[str, Any]:
    path = safe_project_file(project_root, relative)
    require(path.is_file(), f"Pinned source missing: {relative}")
    observed_size = path.stat().st_size
    observed_sha = sha256_file(path)
    require(observed_size == int(pin["bytes"]), f"Pinned source size mismatch: {relative}")
    require(observed_sha == str(pin["sha256"]).lower(), f"Pinned source SHA-256 mismatch: {relative}")
    return {"path": relative, "bytes": observed_size, "sha256": observed_sha}


def verify_source_pins_after_capture(project_root: Path, r1p_archive: Path, policy_path: Path,
                                     approval_path: Path) -> dict[str, Any]:
    """Re-check all authorities/pins after each C11-C launcher execution."""
    r1p = verify_r1p_archive(project_root, r1p_archive)
    option_c = verify_option_c_evidence(project_root)
    policy = verify_approval_policy(project_root, policy_path, approval_path)
    return {
        "r1p_source_pin_count": r1p["r1p_source_pins"],
        "additional_c11c_dependency_pin_count": r1p["additional_c11c_dependency_pins"],
        "option_c_source_pin_count": r1p["option_c_source_pins"],
        "total_source_pin_validations": r1p["total_source_pins_verified"],
        "r1p_recovered_zip_sha256": r1p["recovered_zip_sha256"],
        "option_c_report_sha256": option_c["report_sha256"],
        "r1v_policy_sha256": policy["policy_sha256"],
        "d4_8_production_policy_state": policy["d4_8_production_policy_state"],
    }


def temp_file_state(pattern: str) -> dict[str, str]:
    root = Path(tempfile.gettempdir())
    return {p.name: sha256_file(p) for p in sorted(root.glob(pattern)) if p.is_file()}


def restore_known_c11c_override_state(override_path: Path, existed_before: bool,
                                      original_bytes: bytes | None) -> str:
    """Restore only the exact known temporary C11-C override; never clobber unknown changes."""
    current = override_path.read_bytes() if override_path.exists() else None
    if existed_before:
        if current == original_bytes:
            return "PASS_ORIGINAL_PREIMAGE_PRESENT"
        if current == EXPECTED_C11C_OVERRIDE_BYTES:
            override_path.write_bytes(original_bytes or b"")
            return "RESTORED_EXACT_KNOWN_C11C_TEMPORARY; RUN_MUST_FAIL"
        raise R1VError("override.cfg contains unexpected bytes; left untouched to avoid overwriting external/user changes")
    if current is None:
        return "PASS_ORIGINALLY_ABSENT"
    if current == EXPECTED_C11C_OVERRIDE_BYTES:
        override_path.unlink()
        return "REMOVED_EXACT_KNOWN_C11C_TEMPORARY; RUN_MUST_FAIL"
    raise R1VError("override.cfg appeared with unexpected bytes; left untouched to avoid overwriting external/user changes")


def read_zip_member(archive: zipfile.ZipFile, name: str) -> bytes:
    try:
        return archive.read(name)
    except KeyError as exc:
        raise R1VError(f"R1P archive member missing: {name}") from exc


def sidecar_digest(raw: bytes, label: str) -> str:
    token = raw.decode("ascii").strip().split()[0]
    require(re.fullmatch(r"[0-9a-f]{64}", token) is not None, f"Malformed SHA sidecar: {label}")
    return token


def verify_r1p_archive(project_root: Path, archive_path: Path) -> dict[str, Any]:
    require(archive_path.is_file(), f"R1P recovered ZIP missing: {archive_path}")
    archive_sha = sha256_file(archive_path)
    require(archive_sha == R1P_RECOVERED_ZIP_SHA256,
            f"R1P recovered ZIP SHA mismatch: {archive_sha}")
    try:
        zf = zipfile.ZipFile(archive_path, "r")
    except Exception as exc:
        raise R1VError(f"R1P recovered ZIP cannot open: {exc}") from exc
    with zf:
        require(zf.testzip() is None, "R1P recovered ZIP CRC failure")
        names = [n for n in zf.namelist() if not n.endswith("/")]
        require(len(names) == 72, f"R1P recovered archive member count {len(names)} != 72")
        require(len(names) == len(set(names)), "R1P recovered ZIP contains duplicate entry names")
        require(all("\\" not in n for n in names), "R1P recovered ZIP has non-normalized separators")
        receipt_names = sorted(n for n in names if re.fullmatch(r"receipts/[^/]+\.json", n))
        sidecar_names = sorted(n for n in names if re.fullmatch(r"receipts/[^/]+\.json\.sha256", n))
        require(len(receipt_names) == 27 and len(sidecar_names) == 27,
                f"R1P receipt count mismatch: {len(receipt_names)} receipts / {len(sidecar_names)} sidecars")

        report = load_json_bytes(read_zip_member(zf, "r1p_report.json"), "r1p_report.json")
        report_for_hash = dict(report)
        stored_report_hash = report_for_hash.pop("report_sha256", None)
        observed_report_hash = canonical_sha256(report_for_hash)
        require(stored_report_hash == observed_report_hash == R1P_REPORT_CANONICAL_SHA256,
                "R1P canonical report hash mismatch")
        require(sidecar_digest(read_zip_member(zf, "r1p_report.sha256"), "r1p_report.sha256") == observed_report_hash,
                "R1P report sidecar hash mismatch")
        require(report.get("run_id") == R1P_RUN_ID
                and report.get("status") == "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27"
                and report.get("case_count") == report.get("receipt_count") == report.get("grammar_count") == 27
                and report.get("family_count") == 5,
                "R1P report identity/status/count mismatch")
        require(report.get("scope_limits", {}).get("family_launchers_invoked") is False
                and report.get("scope_limits", {}).get("media_created") is False
                and report.get("scope_limits", {}).get("ffmpeg_invoked") is False,
                "R1P report scope boundary is not parameter-only")

        source_manifest = load_json_bytes(read_zip_member(zf, "source_manifest.json"), "source_manifest.json")
        source_pins = source_manifest.get("source_pins", {})
        require(len(source_pins) == 30 and report.get("source_pins") == source_pins,
                "R1P source pin set is not the accepted 30-file map")
        require(sha256_bytes(read_zip_member(zf, "source_manifest.json")) == report.get("source_manifest_sha256"),
                "R1P source manifest raw SHA mismatch")
        require(source_pins.get("release/C11C_FREEZE_PACKAGE_MANIFEST.json", {}).get("sha256")
                == FROZEN_C11C_MANIFEST_SHA256, "R1P source pins do not bind frozen C11-C")
        require(source_pins.get("tools/c11d/d9/test_c11e_e4b_r1p_family_grammar_static_audit.py", {}).get("sha256")
                == STATIC_AUDIT_SHA256, "R1P static audit pin mismatch")

        prepare = load_json_bytes(read_zip_member(zf, "prepare_report.json"), "prepare_report.json")
        parent_bindings = load_json_bytes(read_zip_member(zf, "parent_bindings.json"), "parent_bindings.json")
        require(prepare.get("status") == "PASS_D9_9_D9_10_PARENT_PREPARATION_27_OF_27"
                and prepare.get("case_count") == prepare.get("explicit_selector_count") == 27
                and len(prepare.get("request_ids", [])) == 27,
                "R1P prepare report is not 27/27")
        require(sha256_bytes(read_zip_member(zf, "parent_bindings.json")) == report.get("parent_bindings_sha256")
                == prepare.get("parent_bindings_sha256"), "R1P parent bindings SHA mismatch")
        parent_by_case = {str(row.get("case_id")): row for row in parent_bindings.get("cases", [])}
        require(len(parent_by_case) == 27, "R1P parent binding set is incomplete or duplicated")

        observed_receipts: dict[int, dict[str, Any]] = {}
        canonical_receipt_hashes: list[str] = []
        observed_case_ids: set[str] = set()
        for receipt_name in receipt_names:
            raw = read_zip_member(zf, receipt_name)
            receipt = load_json_bytes(raw, receipt_name)
            hash_input = dict(receipt)
            stored_hash = hash_input.pop("receipt_sha256", None)
            observed_hash = canonical_sha256(hash_input)
            require(stored_hash == observed_hash, f"Canonical receipt hash mismatch: {receipt_name}")
            sidecar_name = receipt_name + ".sha256"
            require(sidecar_digest(read_zip_member(zf, sidecar_name), sidecar_name) == observed_hash,
                    f"Receipt sidecar mismatch: {receipt_name}")
            require(receipt.get("schema") == "C11E-E4B-R1P-LOOP-FAMILY-PARAMETER-RECEIPT-V1"
                    and receipt.get("status") == "PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT"
                    and receipt.get("run_id") == R1P_RUN_ID,
                    f"R1P receipt schema/status/run mismatch: {receipt_name}")
            case_id = str(receipt.get("case_id", ""))
            require(case_id in prepare["request_ids"] and case_id in parent_by_case and case_id not in observed_case_ids,
                    f"R1P case is not uniquely bound to prepare/D9.9/D9.10: {case_id}")
            observed_case_ids.add(case_id)
            require(receipt.get("request_identity") == parent_by_case[case_id].get("request_identity"),
                    f"R1P D9.9/D9.10 parent identity mismatch: {case_id}")
            require(receipt.get("source_pins") == source_pins,
                    f"R1P global source pins differ from archive manifest: {case_id}")
            require(receipt.get("payload_sha256") == receipt.get("repeat_payload_sha256"),
                    f"R1P deterministic parameter repeat mismatch: {case_id}")
            canonical_text = receipt.get("visual_parameters_canonical_json")
            require(isinstance(canonical_text, str)
                    and sha256_bytes(canonical_text.encode("utf-8")) == receipt.get("visual_parameters_sha256"),
                    f"R1P canonical visual parameter hash mismatch: {case_id}")
            timing = receipt.get("timing", {})
            require(int(timing.get("fps", 0)) == 30
                    and float(timing.get("duration_seconds", 0)) in (20.0, 22.0, 23.0)
                    and int(timing.get("frame_count", 0)) == int(timing["fps"]) * int(timing["duration_seconds"]),
                    f"R1P timing descriptor invalid: {case_id}")
            seed_domains = receipt.get("seed_domains", {})
            require(seed_domains.get("music_seed_consumed_by_visual_parameters") is False
                    and seed_domains.get("visual_parameters_use") == "request.seed"
                    and seed_domains.get("runtime_seed_derivation") is False,
                    f"R1P gameplay/music seed separation invalid: {case_id}")
            governance = receipt.get("governance", {})
            for key, value in {"renderer": "OFF", "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY",
                               "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION",
                               "release_authority": "NONE"}.items():
                require(governance.get(key) == value, f"R1P governance lock drift: {case_id} {key}")
            materialization = receipt.get("materialization", {})
            for key in ("frame_buffers_materialized", "frame_inventory_materialized", "pixel_payload_materialized",
                        "renderer_native_input_emitted", "renderer_instantiated", "prototype_node_instantiated",
                        "launcher_invoked", "audio_or_d3_invoked", "ffmpeg_invoked", "media_created"):
                require(materialization.get(key) is False, f"R1P is no longer parameter-only: {case_id} {key}")
            canonical_receipt_hashes.append(observed_hash)
            observed_receipts[int(receipt["receipt_index"])] = receipt

        require(len(observed_receipts) == 27 and len(observed_case_ids) == 27,
                "R1P selected receipt set incomplete")
        require(canonical_sha256(canonical_receipt_hashes) == report.get("receipt_hash_set_sha256"),
                "R1P aggregate receipt hash-set digest mismatch")

        selected = []
        for expected in SELECTOR_EXPECTATIONS:
            receipt = observed_receipts.get(int(expected["receipt_index"]))
            require(receipt is not None, f"Selected R1P receipt missing: {expected['receipt_index']}")
            selection = receipt.get("selection", {})
            timing = receipt.get("timing", {})
            seed_domains = receipt.get("seed_domains", {})
            require(selection.get("family_id") == expected["family_id"]
                    and selection.get("grammar_id") == expected["grammar_id"]
                    and int(selection.get("grammar_index", -1)) == expected["grammar_index"],
                    f"Selected R1P family/grammar mismatch: {expected['family_id']}")
            require(int(seed_domains.get("gameplay_seed", -1)) == expected["gameplay_seed"],
                    f"Selected R1P gameplay seed mismatch: {expected['family_id']}")
            require(float(timing.get("duration_seconds", 0)) == expected["duration_seconds"]
                    and int(timing.get("fps", 0)) == expected["fps"]
                    and int(timing.get("frame_count", 0)) == expected["frame_count_consistency_only"],
                    f"Selected R1P timing mismatch: {expected['family_id']}")
            # Launcher and prototype are members of the R1P 30-pin set.
            # The family scene is a transitive dependency pinned separately in
            # ADDITIONAL_SOURCE_PINS; do not misclassify it as a missing R1P pin.
            for path_key, hash_key in (("launcher_path", "launcher_sha256"),
                                       ("prototype_path", "prototype_sha256")):
                require(source_pins.get(expected[path_key], {}).get("sha256") == expected[hash_key],
                        f"Selected R1P source pin mismatch: {expected['family_id']} {expected[path_key]}")
            scene_pin = ADDITIONAL_SOURCE_PINS.get(expected["scene_path"], {})
            require(scene_pin.get("sha256") == expected["scene_sha256"],
                    f"Selected transitive scene pin mismatch: {expected['family_id']} {expected['scene_path']}")
            selected.append({
                **expected,
                "r1p_case_id": receipt["case_id"],
                "r1p_receipt_sha256": receipt["receipt_sha256"],
                "r1p_payload_sha256": receipt["payload_sha256"],
                "r1p_request_identity": receipt["request_identity"],
            })

    pin_results = []
    for relative, pin in sorted(source_pins.items()):
        pin_results.append(verify_file_pin(project_root, relative, pin))
    for relative, pin in sorted(ADDITIONAL_SOURCE_PINS.items()):
        require(pin["sha256"] != "__TO_BE_SET__", f"Additional source pin has not been finalized: {relative}")
        pin_results.append(verify_file_pin(project_root, relative, pin))
    for relative, pin in sorted(OPTION_C_SOURCE_PINS.items()):
        pin_results.append(verify_file_pin(project_root, relative, pin))
    frozen_path = safe_project_file(project_root, "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    require(sha256_file(frozen_path) == FROZEN_C11C_MANIFEST_SHA256,
            "Active frozen C11-C manifest SHA mismatch")
    static_audit = safe_project_file(project_root, "tools/c11d/d9/test_c11e_e4b_r1p_family_grammar_static_audit.py")
    require(sha256_file(static_audit) == STATIC_AUDIT_SHA256, "Active accepted static audit SHA mismatch")

    return {
        "r1p_run_id": R1P_RUN_ID,
        "recovered_zip_path": str(archive_path),
        "recovered_zip_sha256": archive_sha,
        "r1p_report_canonical_sha256": observed_report_hash,
        "r1p_source_pins": len(source_pins),
        "additional_c11c_dependency_pins": len(ADDITIONAL_SOURCE_PINS),
        "option_c_source_pins": len(OPTION_C_SOURCE_PINS),
        "total_source_pins_verified": len(pin_results),
        "source_pin_results": pin_results,
        "receipt_count": len(observed_receipts),
        "selected_selectors": selected,
        "parent_bindings": len(parent_by_case),
        "r1p_archive_members": 72,
    }


def verify_approval_policy(project_root: Path, policy_path: Path, approval_path: Path) -> dict[str, Any]:
    policy = load_json(policy_path)
    approval = load_json(approval_path)
    require(policy.get("schema") == "C11E-D4.8-R1V-QUALIFICATION-ONLY-POLICY-V2"
            and policy.get("status") == "APPROVED_BOUNDED_R1V_QUALIFICATION_ONLY"
            and policy.get("execution_authorized") is True
            and policy.get("supersedes") == "C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V1",
            "R1V policy is not explicitly approved or does not supersede the historical V1 proposal")
    old_v1_path = safe_project_file(project_root, "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V1.json")
    old_v1 = load_json(old_v1_path)
    require(sha256_file(old_v1_path) == R1V_V1_PROPOSAL_SHA256
            and old_v1.get("status") == "PROPOSED_NOT_APPROVED"
            and old_v1.get("execution_authorized") is False
            and policy.get("superseded_v1_policy_sha256") == R1V_V1_PROPOSAL_SHA256,
            "Historical R1V V1 proposal changed or is not explicitly superseded")
    require(approval.get("schema") == "C11E-D4.8-R1V-OPERATOR-APPROVAL-RECORD-V1"
            and approval.get("decision") == "APPROVE_EXACT_BOUNDED_R1V_SCOPE",
            "R1V operator approval record is invalid")
    approval_input = dict(approval)
    record_hash = approval_input.pop("approval_record_sha256", None)
    calculated_record_hash = canonical_sha256(approval_input)
    require(record_hash == calculated_record_hash == policy.get("approval", {}).get("approval_record_sha256"),
            "R1V approval record canonical hash mismatch")
    require(policy.get("approval", {}).get("policy_author") == "ChatGPT — technical author"
            and policy.get("approval", {}).get("independent_reviewer") == "Operator (user)"
            and policy.get("approval", {}).get("operator_approver") == "Operator (user)"
            and approval.get("policy_author") == policy.get("approval", {}).get("policy_author")
            and approval.get("independent_reviewer") == policy.get("approval", {}).get("independent_reviewer")
            and approval.get("operator_approver") == policy.get("approval", {}).get("operator_approver"),
            "R1V author/reviewer/operator assignments differ from approval")
    require(approval.get("approval_timestamp") == "2026-11-07T22:45:00+01:00",
            "R1V approval timestamp does not match the recorded operator approval")
    require(approval.get("scope") == policy.get("execution", {}).get("approval_scope"),
            "R1V approval scope differs from the immutable policy scope")
    require(policy.get("scope", {}).get("allowed_selector_count") == 5
            and policy.get("scope", {}).get("repeat_count_per_selector") == 2
            and policy.get("scope", {}).get("total_launcher_invocations") == 10
            and policy.get("scope", {}).get("music_seed_passed_to_visual_launcher") is False,
            "R1V D4.8 qualification-only scope fields are inconsistent")
    require(policy.get("forbidden", {}).get("ffmpeg_encode_filter_or_mux") is False
            and policy.get("forbidden", {}).get("ffmpeg_filter_or_mux") is True
            and policy.get("governance", {}).get("d4_8_r1v_qualification_only") == "AUTHORIZED",
            "R1V bounded silent-encode exception is not isolated from filter/mux prohibition")
    require(approval.get("scope", {}).get("selector_count") == 5
            and approval.get("scope", {}).get("repeat_count_per_selector") == 2
            and approval.get("scope", {}).get("launcher_invocations") == 10,
            "R1V approval scope must remain exactly five selectors × two runs")
    require(approval.get("scope", {}).get("silent_c11c_mp4_encode_only") is True
            and approval.get("scope", {}).get("no_filters_audio_d3_mux_or_d_consumer") is True,
            "R1V approval does not match operator's limited FFmpeg exception")
    require(policy.get("selectors") == [{k: s[k] for k in (
        "receipt_index", "family_id", "grammar_id", "grammar_index", "gameplay_seed", "duration_seconds", "fps",
        "frame_count_consistency_only", "launcher_path", "launcher_sha256", "prototype_path", "prototype_sha256",
        "scene_path", "scene_sha256") } for s in SELECTOR_EXPECTATIONS],
        "R1V policy selector allowlist differs from code-pinned selection")
    require(policy.get("execution", {}).get("selector_count") == 5
            and policy.get("execution", {}).get("repeat_count_per_selector") == 2
            and policy.get("execution", {}).get("launcher_invocations_exact") == 10,
            "R1V policy is not limited to five selectors × two executions")
    forbidden = policy.get("forbidden", {})
    for key in ("d_compositor_dispatch", "d9_10_renderer_consumer_dispatch", "d3_music_engine",
                "pcm_audio_generation", "ffmpeg_filter_or_mux", "longform", "smoke18_or_matrix99",
                "production_delivery", "freeze_or_promotion", "release_authority",
                "c11c_source_mechanics_rng_or_protected_path_modification"):
        require(forbidden.get(key) is True, f"R1V forbidden operation not enforced: {key}")
    require(policy.get("allowances", {}).get("c11c_no_sound_mp4_encode") is True
            and policy.get("allowances", {}).get("ffprobe_read_only") is True
            and policy.get("allowances", {}).get("ffmpeg_decode_only_pipe_to_memory") is True,
            "R1V limited tool allowances are missing")
    require(policy.get("execution", {}).get("launcher_invocations_exact") == 10
            and policy.get("execution", {}).get("prohibited_launcher_switches") == ["-ExportGif", "-KeepAvi", "-NoFooter"]
            and policy.get("execution", {}).get("temp_silent_path_preflight_nonexistent") is True
            and policy.get("execution", {}).get("temp_avi_prefix_preflight_empty") is True
            and policy.get("execution", {}).get("output_tag_includes_unique_run_id") is True,
            "R1V launcher invocation count/switch/temp-path restrictions differ from the approved scope")
    expected_encode = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", "<AVI>", "-an",
                       "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                       "-movflags", "+faststart", "<MP4>"]
    require(policy.get("permitted_native_c11c_encode", {}).get("argv_template") == expected_encode,
            "R1V C11-C silent encoder argv allowlist changed")
    require(policy.get("source_integrity", {}).get("r1p_source_pins") == 30
            and policy.get("source_integrity", {}).get("additional_c11c_transitive_dependency_pins") == len(ADDITIONAL_SOURCE_PINS)
            and policy.get("source_integrity", {}).get("option_c_source_pins") == len(OPTION_C_SOURCE_PINS)
            and policy.get("source_integrity", {}).get("total_source_pins_expected") == 61,
            "R1V transitive source-pin policy is incomplete")
    require(policy.get("governance", {}).get("d_renderer_dispatch") == "OFF"
            and policy.get("governance", {}).get("d4_8_general_production") == "BLOCKED"
            and policy.get("governance", {}).get("d9_10") == "PREPARE_ONLY"
            and policy.get("governance", {}).get("release_authority") == "NONE",
            "R1V policy improperly changes production governance")

    # The C11-D production policy remains unchanged and disabled; this bounded
    # R1V approval is not a general production renderer authorization. Check
    # the exact authoritative fields, not a loose string occurrence.
    require(sha256_file(policy_path) == R1V_POLICY_SHA256,
            "R1V policy raw SHA-256 differs from the approved policy pin")
    d4_policy_path = safe_project_file(project_root, "definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json")
    d4_policy = load_json(d4_policy_path)
    require(sha256_file(d4_policy_path) == C11D_PRODUCTION_POLICY_SHA256,
            "C11-D production activation policy SHA changed")
    require(d4_policy.get("policy_id") == "c11d_production_activation"
            and d4_policy.get("runtime_authority") == "NONE"
            and d4_policy.get("renderer_activation_policy", {}).get("state") == "DISABLED"
            and d4_policy.get("review", {}).get("authorization") is False
            and d4_policy.get("execution", {}).get("renderer_called") is False
            and d4_policy.get("execution", {}).get("production_execution") is False
            and d4_policy.get("execution", {}).get("ffmpeg_production_called") is False
            and d4_policy.get("execution", {}).get("godot_production_called") is False,
            "C11-D production activation policy changed or no longer remains disabled")
    return {
        "policy_path": str(policy_path),
        "policy_sha256": sha256_file(policy_path),
        "approval_path": str(approval_path),
        "approval_record_sha256": record_hash,
        "policy_author": policy["approval"]["policy_author"],
        "independent_reviewer": policy["approval"]["independent_reviewer"],
        "operator_approver": policy["approval"]["operator_approver"],
        "operator_approval_timestamp": approval.get("approval_timestamp"),
        "selector_count": 5,
        "repeat_count": 2,
        "launcher_invocations_authorized": 10,
        "d4_8_production_policy_state": "DISABLED_UNCHANGED",
        "d_renderer_dispatch": "OFF",
    }


def verify_option_c_evidence(project_root: Path) -> dict[str, Any]:
    base = project_root / "artifacts" / "tests" / "c11e" / "option_c_postcomposition_contract" / OPTION_C_RUN_ID
    report_path = base / "option_c_contract_report.json"
    process_path = base / "option_c_contract_process_receipt.json"
    install_path = (project_root / "artifacts" / "tests" / "c11e" / "option_c_postcomposition_install"
                    / "OPTION_C_INSTALL_20261107_151443_95D2C6E9" / "install_receipt.json")
    for p in (report_path, process_path, install_path):
        require(p.is_file(), f"Option C active-checkout evidence missing: {p}")
    report_hash = sha256_file(report_path)
    process_hash = sha256_file(process_path)
    install_hash = sha256_file(install_path)
    require(report_hash == OPTION_C_REPORT_SHA256, "Option C report SHA mismatch")
    require(process_hash == OPTION_C_PROCESS_RECEIPT_SHA256, "Option C process receipt SHA mismatch")
    require(install_hash == OPTION_C_INSTALL_RECEIPT_SHA256, "Option C install receipt SHA mismatch")
    report = load_json(report_path)
    process = load_json(process_path)
    install = load_json(install_path)
    require(report.get("status") == "PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY"
            and report.get("architecture_decision", {}).get("selected_option") == "C"
            and report.get("architecture_decision", {}).get("decision_state") == "OPERATOR_APPROVED_OPTION_C",
            "Option C report status/decision mismatch")
    require(len(report.get("handoffs", [])) == 27
            and all(h.get("status") == "PREPARED_WAITING_FOR_R1V_ACTUAL_SOURCE_EVIDENCE" for h in report["handoffs"]),
            "Option C handoff set is not 27/27 prepare-only")
    gov = report.get("governance", {})
    require(gov.get("renderer") == "OFF" and gov.get("d4_8") == "BLOCKED"
            and gov.get("d9_10") == "PREPARE_ONLY" and gov.get("d9_14") == "BLOCKED"
            and gov.get("d9_16") == "BLOCKED" and gov.get("d9_17") == "BLOCKED_NO_GO"
            and gov.get("d10") == "BLOCKED_FOR_PROMOTION" and gov.get("release_authority") == "NONE"
            and gov.get("media_created") is False and gov.get("launcher_invoked") is False
            and gov.get("godot_invoked") is False and gov.get("ffprobe_invoked") is False
            and gov.get("ffmpeg_invoked") is False and gov.get("compositor_invoked") is False
            and gov.get("audio_or_d3_invoked") is False and gov.get("mux_invoked") is False
            and gov.get("renderer_dispatch_invoked") is False
            and gov.get("c11c_source_mutation") is False,
            "Option C evidence does not preserve governance locks or static-only scope")
    require(process.get("overall_status") == report.get("status")
            and process.get("report_sha256") == report_hash
            and process.get("process_count") == 2,
            "Option C process receipt does not bind report and two captured processes")
    require(install.get("status") == "PASS_ADD_ONLY_INSTALL"
            and install.get("installed_file_count") == 17
            and install.get("package_manifest_sha256") == OPTION_C_PACKAGE_MANIFEST_SHA256
            and install.get("frozen_c11c_manifest_sha256") == FROZEN_C11C_MANIFEST_SHA256,
            "Option C installation evidence is invalid")
    process_logs = []
    for item in process.get("processes", []):
        require(int(item.get("exit_code", -1)) == 0, f"Option C process failed: {item.get('name')}")
        for kind in ("stdout", "stderr"):
            path = Path(item.get(f"{kind}_path", ""))
            # On the active Windows checkout, the captured absolute path is authoritative.
            # A portable evidence-bundle fallback exists only for isolated validation/tests.
            if not path.is_file():
                portable_name = ("unit_tests" if item.get("name") == "OPTION_C_UNIT_TESTS" else "contract")
                path = base / f"{portable_name}.{kind}.log"
            require(path.is_file(), f"Option C captured {kind} log missing: {path}")
            digest = sha256_file(path)
            require(digest == item.get(f"{kind}_sha256"), f"Option C {kind} log SHA mismatch: {item.get('name')}")
            process_logs.append({"name": item.get("name"), "kind": kind, "sha256": digest})
    return {
        "report_sha256": report_hash,
        "process_receipt_sha256": process_hash,
        "install_receipt_sha256": install_hash,
        "handoffs": 27,
        "source_pin_validations": 33,
        "captured_process_logs_verified": len(process_logs),
        "architecture_decision": "OPERATOR_APPROVED_OPTION_C",
    }


def executable_info(name: str, version_args: list[str]) -> dict[str, Any]:
    exe = shutil.which(name)
    require(exe is not None, f"Required executable not found on PATH: {name}")
    path = Path(exe).resolve()
    require(path.is_file(), f"Executable path is not a file: {path}")
    run = subprocess.run([str(path), *version_args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(run.returncode == 0, f"Version probe failed for {name}: exit={run.returncode}")
    output = (run.stdout + run.stderr).decode("utf-8", errors="replace")
    return {
        "command": name,
        "path": str(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "version_exit_code": run.returncode,
        "version_output": output.splitlines()[0] if output.splitlines() else "",
        "version_output_sha256": sha256_bytes(run.stdout + run.stderr),
    }


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        part = stream.read(size - len(chunks))
        if not part:
            break
        chunks.extend(part)
    return bytes(chunks)


def parse_rate(value: str) -> Fraction:
    try:
        return Fraction(value)
    except Exception as exc:
        raise R1VError(f"Invalid rational value: {value}") from exc


def run_command(executable: str, args: list[str], cwd: Path, timeout: int = 1800) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([executable, *args], cwd=str(cwd), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout, check=False)



def validate_c11c_sidecars(authoring: dict[str, Any], manifest: dict[str, Any], selector: dict[str, Any], repeat: str) -> None:
    """Validate the authentic C11-C 2.16.3 sidecar schema (not guessed flat fields)."""
    require(int(authoring.get("seed", -1)) == selector["gameplay_seed"]
            and str(authoring.get("family_id")) == selector["internal_family_id"]
            and str(authoring.get("grammar_id")) == selector["grammar_id"],
            f"C11-C authoring sidecar identity mismatch: {selector['family_id']} {repeat}")
    require(float(authoring.get("duration_seconds", 0)) == selector["duration_seconds"]
            and int(authoring.get("fps", 0)) == selector["fps"]
            and int(authoring.get("frame_count", 0)) == selector["frame_count_consistency_only"],
            f"C11-C authoring timing mismatch: {selector['family_id']} {repeat}")
    require(authoring.get("sound_enabled") is False,
            f"C11-C authoring reports sound enabled: {selector['family_id']} {repeat}")

    visual = manifest.get("visual", {})
    audio = manifest.get("audio", {})
    artifact_policy = manifest.get("artifact_policy", {})
    require(manifest.get("revision") == "2.16.3"
            and manifest.get("family_id") == selector["internal_family_id"]
            and manifest.get("production_id") == selector["family_id"]
            and manifest.get("grammar_id") == selector["grammar_id"]
            and int(manifest.get("seed", -1)) == selector["gameplay_seed"],
            f"C11-C product manifest identity mismatch: {selector['family_id']} {repeat}")
    require(visual.get("canvas") == "720x1280"
            and float(visual.get("duration_seconds", 0)) == selector["duration_seconds"]
            and int(visual.get("fps", 0)) == selector["fps"]
            and int(visual.get("frame_count", 0)) == selector["frame_count_consistency_only"],
            f"C11-C product manifest visual contract mismatch: {selector['family_id']} {repeat}")
    require(audio.get("enabled") is False and audio.get("muxed_into_mp4") is False
            and artifact_policy.get("export_gif") is False
            and artifact_policy.get("keep_avi") is False
            and artifact_policy.get("avi_intermediate") is True,
            f"C11-C product manifest audio/artifact policy mismatch: {selector['family_id']} {repeat}")

def inspect_source_video(project_root: Path, output_root: Path, selector: dict[str, Any], repeat: str,
                         tools: dict[str, Any], job_record: dict[str, Any]) -> dict[str, Any]:
    stem = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job_record['output_tag']}"
    video_path = output_root / f"{stem}.mp4"
    authoring_path = output_root / f"{stem}_authoring.json"
    manifest_path = output_root / f"{stem}_manifest.json"
    godot_log_path = output_root / f"{stem}_godot.log"
    social_path = output_root / f"{stem}_social.txt"
    launcher_probe_path = output_root / f"{stem}_ffprobe.json"
    required_files = (video_path, authoring_path, manifest_path, godot_log_path, social_path, launcher_probe_path)
    for p in required_files:
        require(p.is_file() and p.stat().st_size > 0, f"C11-C launcher output missing/empty: {p}")
    forbidden_output_suffixes = (".gif", ".avi", "_music.wav", "_silent.mp4")
    for p in output_root.iterdir():
        require(not p.name.endswith(forbidden_output_suffixes), f"Forbidden R1V artifact produced: {p.name}")
    require(not list(output_root.glob("*.wav")), "R1V output contains a WAV/audio artifact")

    authoring = load_json(authoring_path)
    manifest = load_json(manifest_path)
    validate_c11c_sidecars(authoring, manifest, selector, repeat)
    launcher_probe = load_json(launcher_probe_path)
    launcher_streams = launcher_probe.get("streams", [])
    require(len(launcher_streams) == 1 and launcher_streams[0].get("codec_type") == "video"
            and int(launcher_streams[0].get("width", 0)) == 720
            and int(launcher_streams[0].get("height", 0)) == 1280
            and launcher_streams[0].get("r_frame_rate") == "30/1"
            and int(launcher_streams[0].get("nb_frames", -1)) == selector["frame_count_consistency_only"],
            f"C11-C launcher's own FFprobe sidecar does not satisfy the silent source contract: {selector['family_id']} {repeat}")
    godot_text = godot_log_path.read_text(encoding="utf-8", errors="replace")
    require("recording movie in" in godot_text.lower() and "720" in godot_text and "1280" in godot_text
            and "30 fps" in godot_text.lower(), f"Godot movie capture log lacks 720x1280@30: {selector['family_id']} {repeat}")
    require(not re.search(r"SCRIPT ERROR|Parse Error|SHADER ERROR|Shader compilation failed|ERROR:", godot_text, re.I),
            f"Godot output contains a prototype error: {selector['family_id']} {repeat}")

    mp4_sha_before = sha256_file(video_path)
    mp4_bytes = video_path.stat().st_size
    require(mp4_bytes > 0, "Silent MP4 source is empty")

    metadata_args = [
        "-v", "error",
        "-show_entries",
        "format=filename,format_name,start_time,duration,size,bit_rate:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,sample_aspect_ratio,display_aspect_ratio,r_frame_rate,avg_frame_rate,time_base,start_pts,start_time,duration,nb_frames,color_range,color_space,color_transfer,color_primaries,chroma_location",
        "-of", "json", str(video_path),
    ]
    metadata = run_command(tools["ffprobe"]["path"], metadata_args, project_root)
    (output_root / f"{stem}_r1v_ffprobe_metadata.stdout.json").write_bytes(metadata.stdout)
    (output_root / f"{stem}_r1v_ffprobe_metadata.stderr.log").write_bytes(metadata.stderr)
    require(metadata.returncode == 0, f"FFprobe metadata exit={metadata.returncode}: {selector['family_id']} {repeat}")
    metadata_json = load_json_bytes(metadata.stdout, f"{stem} FFprobe metadata")
    streams = metadata_json.get("streams", [])
    require(len(streams) == 1 and streams[0].get("codec_type") == "video",
            f"R1V source must contain one video stream and no audio/other streams: {selector['family_id']} {repeat}")
    stream = streams[0]
    require(int(stream.get("width", 0)) == 720 and int(stream.get("height", 0)) == 1280,
            f"R1V source resolution is not 720x1280: {selector['family_id']} {repeat}")
    require(stream.get("r_frame_rate") == "30/1" and stream.get("pix_fmt") == "yuv420p",
            f"R1V source fps/pixel format mismatch: {selector['family_id']} {repeat}")
    require(int(stream.get("nb_frames", -1)) == selector["frame_count_consistency_only"],
            f"FFprobe nb_frames disagrees with R1P timing consistency descriptor: {selector['family_id']} {repeat}")
    duration_actual = float(metadata_json.get("format", {}).get("duration", stream.get("duration", 0)))
    require(abs(duration_actual - selector["duration_seconds"]) <= 0.05,
            f"R1V source duration mismatch: {selector['family_id']} {repeat}")

    frames_args = [
        "-v", "error", "-select_streams", "v:0", "-show_frames",
        "-show_entries",
        "frame=media_type,stream_index,key_frame,pict_type,pts,pts_time,best_effort_timestamp,best_effort_timestamp_time,pkt_dts,pkt_dts_time,pkt_duration,pkt_duration_time,width,height,pix_fmt",
        "-of", "json", str(video_path),
    ]
    frames_proc = run_command(tools["ffprobe"]["path"], frames_args, project_root)
    frames_json_path = output_root / f"{stem}_r1v_ffprobe_frames.json"
    frames_json_path.write_bytes(frames_proc.stdout)
    (output_root / f"{stem}_r1v_ffprobe_frames.stderr.log").write_bytes(frames_proc.stderr)
    require(frames_proc.returncode == 0, f"FFprobe frame metadata exit={frames_proc.returncode}: {selector['family_id']} {repeat}")
    frames_json = load_json_bytes(frames_proc.stdout, f"{stem} FFprobe frames")
    ffprobe_frames = frames_json.get("frames", [])
    require(len(ffprobe_frames) == selector["frame_count_consistency_only"],
            f"Actual FFprobe frame count differs from timing consistency descriptor: {selector['family_id']} {repeat}")

    time_base = parse_rate(str(stream.get("time_base", "")))
    require(time_base > 0, "FFprobe stream time_base must be positive")
    frame_pts = []
    for index, frame in enumerate(ffprobe_frames):
        pts_value = frame.get("best_effort_timestamp", frame.get("pts"))
        require(pts_value is not None, f"Frame {index} has no presentation timestamp")
        pts = int(pts_value)
        pts_time = Fraction(pts) * time_base
        if frame_pts:
            require(pts > frame_pts[-1]["pts"], f"Non-increasing presentation timestamp at frame {index}")
            delta = (pts - frame_pts[-1]["pts"]) * time_base
            require(abs(float(delta) - (1.0 / selector["fps"])) <= 0.00001,
                    f"Non-uniform frame PTS interval at frame {index}: {float(delta)}")
        frame_pts.append({
            "frame_index": index,
            "pts": pts,
            "time_base": f"{time_base.numerator}/{time_base.denominator}",
            "timestamp_seconds_fraction": f"{pts_time.numerator}/{pts_time.denominator}",
            "timestamp_seconds": float(pts_time),
            "pkt_duration": frame.get("pkt_duration"),
            "pkt_duration_time": frame.get("pkt_duration_time"),
            "key_frame": frame.get("key_frame"),
            "pict_type": frame.get("pict_type"),
        })

    raw_frame_size = 720 * 1280 * 3 // 2  # yuv420p: luma + two half-resolution chroma planes
    decode_args = [
        "-v", "error", "-i", str(video_path), "-map", "0:v:0", "-vsync", "0",
        "-pix_fmt", "yuv420p", "-f", "rawvideo", "pipe:1",
    ]
    decode_stderr_path = output_root / f"{stem}_r1v_ffmpeg_decode.stderr.log"
    pixel_hashes = []
    total_bytes = 0
    decoded_stream_hasher = hashlib.sha256()
    decode_start = time.time()
    with decode_stderr_path.open("wb") as decode_stderr:
        proc = subprocess.Popen([tools["ffmpeg"]["path"], *decode_args], cwd=str(project_root),
                                stdout=subprocess.PIPE, stderr=decode_stderr)
        assert proc.stdout is not None
        try:
            index = 0
            while True:
                raw = read_exact(proc.stdout, raw_frame_size)
                if not raw:
                    break
                require(len(raw) == raw_frame_size, f"Truncated decoded pixel frame {index}")
                pixel_hashes.append(sha256_bytes(raw))
                decoded_stream_hasher.update(raw)
                total_bytes += len(raw)
                index += 1
        finally:
            proc.stdout.close()
        decode_exit = proc.wait(timeout=1800)
    require(decode_exit == 0, f"FFmpeg decode-only process failed exit={decode_exit}: {selector['family_id']} {repeat}")
    require(len(pixel_hashes) == len(ffprobe_frames),
            f"Decoded pixel frame count {len(pixel_hashes)} differs from FFprobe frames {len(ffprobe_frames)}")
    require(len(pixel_hashes) == selector["frame_count_consistency_only"],
            f"Decoded pixel count not equal to descriptor: {selector['family_id']} {repeat}")

    frame_records = []
    for pts_record, pixel_hash in zip(frame_pts, pixel_hashes):
        frame_records.append({
            **pts_record,
            "width": 720,
            "height": 1280,
            "pixel_format": "yuv420p",
            "decoded_pixel_sha256": pixel_hash,
        })
    pixel_manifest = {
        "schema": "C11E-R1V-DECODED-PIXEL-HASH-MANIFEST-V1",
        "serialization": "FFMPEG_RAWVIDEO_YUV420P_CONTIGUOUS_PLANES_PER_FRAME; SHA256_PER_FRAME",
        "decoder": {
            "path": tools["ffmpeg"]["path"],
            "executable_sha256": tools["ffmpeg"]["sha256"],
            "version_output": tools["ffmpeg"]["version_output"],
            "arguments": decode_args,
            "exit_code": decode_exit,
            "stderr_sha256": sha256_file(decode_stderr_path),
        },
        "frame_count": len(pixel_hashes),
        "frame_bytes": raw_frame_size,
        "total_decoded_bytes": total_bytes,
        "pixel_format": "yuv420p",
        "global_decoded_stream_sha256": decoded_stream_hasher.hexdigest(),
        "ordered_per_frame_hashes_sha256": sha256_bytes("".join(pixel_hashes).encode("ascii")),
        "per_frame_sha256": pixel_hashes,
    }
    pixel_manifest_path = output_root / f"{stem}_r1v_pixel_hash_manifest.json"
    pixel_manifest_sha = dump_json(pixel_manifest_path, pixel_manifest)
    inventory = {
        "schema": "C11E-R1V-ACTUAL-FRAME-INVENTORY-V1",
        "status": "PASS_MEASURED_SOURCE_FRAME_INVENTORY",
        "r1p_lineage": {
            "run_id": R1P_RUN_ID,
            "case_id": selector["r1p_case_id"],
            "receipt_sha256": selector["r1p_receipt_sha256"],
            "payload_sha256": selector["r1p_payload_sha256"],
            "request_identity": selector["r1p_request_identity"],
        },
        "selector": {k: selector[k] for k in ("family_id", "grammar_id", "grammar_index", "gameplay_seed", "duration_seconds", "fps")},
        "repeat": repeat,
        "source": {
            "video_path": str(video_path),
            "video_path_relative_to_project": video_path.relative_to(project_root).as_posix(),
            "byte_length": mp4_bytes,
            "sha256": mp4_sha_before,
            "sha256_after_read_only_inspection": sha256_file(video_path),
            "immutable_source_bytes_preserved": mp4_sha_before == sha256_file(video_path),
        },
        "metadata": {
            "format": metadata_json.get("format", {}),
            "video_stream": stream,
            "container_probe_stdout_sha256": sha256_bytes(metadata.stdout),
            "frames_probe_stdout_sha256": sha256_bytes(frames_proc.stdout),
            "frames_probe_json_path": str(frames_json_path),
            "frames_probe_json_sha256": sha256_file(frames_json_path),
            "frame_count_measured": len(frame_records),
            "r1p_frame_count_consistency_descriptor": selector["frame_count_consistency_only"],
            "frame_count_matches_descriptor": len(frame_records) == selector["frame_count_consistency_only"],
            "time_base": f"{time_base.numerator}/{time_base.denominator}",
            "start_pts": frame_pts[0]["pts"],
            "start_timestamp_seconds": frame_pts[0]["timestamp_seconds"],
            "last_pts": frame_pts[-1]["pts"],
            "last_timestamp_seconds": frame_pts[-1]["timestamp_seconds"],
            "decoded_duration_seconds": float(Fraction(frame_pts[-1]["pts"] - frame_pts[0]["pts"], 1) * time_base) + 1.0 / selector["fps"],
        },
        "pixel_identity": {
            "pixel_format": "yuv420p",
            "hash_algorithm": "SHA-256",
            "frame_hash_count": len(pixel_hashes),
            "frame_hash_manifest_path": str(pixel_manifest_path),
            "frame_hash_manifest_sha256": pixel_manifest_sha,
            "global_decoded_stream_sha256": pixel_manifest["global_decoded_stream_sha256"],
            "decode_stored_as_frame_files": False,
            "decode_pipe_to_memory": True,
            "filters_applied": False,
        },
        "frame_records": frame_records,
    }
    inventory_path = output_root / f"{stem}_r1v_frame_inventory.json"
    inventory_sha = dump_json(inventory_path, inventory)
    # Recompute the source hash after every read-only operation to prove the original bytes did not change.
    final_video_sha = sha256_file(video_path)
    require(final_video_sha == mp4_sha_before, "C11-C MP4 source bytes changed during R1V read-only inspection")
    return {
        "selector": selector["family_id"],
        "grammar": selector["grammar_id"],
        "repeat": repeat,
        "output_root": str(output_root),
        "video_path": str(video_path),
        "video_sha256": mp4_sha_before,
        "video_bytes": mp4_bytes,
        "frame_count": len(frame_records),
        "frame_inventory_path": str(inventory_path),
        "frame_inventory_sha256": inventory_sha,
        "pixel_manifest_path": str(pixel_manifest_path),
        "pixel_manifest_sha256": pixel_manifest_sha,
        "global_decoded_stream_sha256": pixel_manifest["global_decoded_stream_sha256"],
        "frame_hashes": pixel_hashes,
        "pts": [x["pts"] for x in frame_pts],
        "time_base": f"{time_base.numerator}/{time_base.denominator}",
        "format_metadata": metadata_json.get("format", {}),
        "video_stream": stream,
        "launcher_ffprobe_json_sha256": sha256_file(launcher_probe_path),
        "launcher_godot_log_sha256": sha256_file(godot_log_path),
        "launcher_authoring_sha256": sha256_file(authoring_path),
        "launcher_manifest_sha256": sha256_file(manifest_path),
        "launcher_social_sha256": sha256_file(social_path),
        "decode_exit_code": decode_exit,
        "decode_stderr_sha256": sha256_file(decode_stderr_path),
        "inspection_elapsed_seconds": round(time.time() - decode_start, 3),
    }


def compare_repeats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        by_key.setdefault(row["selector"], {})[row["repeat"]] = row
    comparisons = []
    for selector in SELECTOR_EXPECTATIONS:
        key = selector["family_id"]
        pair = by_key.get(key, {})
        require(set(pair) == {"A", "B"}, f"Missing repeat pair for {key}")
        a, b = pair["A"], pair["B"]
        checks = {
            "frame_count_equal": a["frame_count"] == b["frame_count"],
            "pts_equal": a["pts"] == b["pts"],
            "time_base_equal": a["time_base"] == b["time_base"],
            "pixel_frame_hashes_equal": a["frame_hashes"] == b["frame_hashes"],
            "global_pixel_stream_hash_equal": a["global_decoded_stream_sha256"] == b["global_decoded_stream_sha256"],
            "metadata_geometry_equal": (a["video_stream"].get("width"), a["video_stream"].get("height"),
                                         a["video_stream"].get("pix_fmt"), a["video_stream"].get("r_frame_rate"))
                                        == (b["video_stream"].get("width"), b["video_stream"].get("height"),
                                            b["video_stream"].get("pix_fmt"), b["video_stream"].get("r_frame_rate")),
        }
        passed = all(checks.values())
        comparisons.append({"family_id": key, "grammar_id": selector["grammar_id"], "checks": checks,
                            "deterministic_repeat_pass": passed,
                            "source_mp4_sha256_a": a["video_sha256"],
                            "source_mp4_sha256_b": b["video_sha256"],
                            "source_mp4_byte_identical": a["video_sha256"] == b["video_sha256"]})
        require(passed, f"Deterministic R1V repeat mismatch for {key}: {checks}")
    return {"selector_count": 5, "repeat_pairs": comparisons, "deterministic_repeat_passed": 5}


def _tool_preflight(project_root: Path) -> dict[str, Any]:
    require(sys.platform == "win32", "R1V physical qualification runner may execute only on Windows")
    require(sys.version_info[:2] == (3, 13), f"Python 3.13 required; found {sys.version.split()[0]}")
    python_path = Path(sys.executable).resolve()
    path_python = Path(shutil.which("python") or "").resolve()
    require(path_python.is_file() and os.path.normcase(str(path_python)) == os.path.normcase(str(python_path)),
            f"Python PATH launcher and active interpreter differ: {path_python} != {python_path}")
    ps = executable_info("powershell.exe", ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"])
    require(ps["version_output"].startswith("5.1."), f"Windows PowerShell 5.1 required; found {ps['version_output']}")
    godot = executable_info("godot", ["--version"])
    require(godot["version_output"].startswith("4.7.1"), f"Godot 4.7.1 required; found {godot['version_output']}")
    ffmpeg = executable_info("ffmpeg", ["-version"])
    ffprobe = executable_info("ffprobe", ["-version"])
    python = executable_info("python", ["--version"])
    encoders = subprocess.run([ffmpeg["path"], "-hide_banner", "-encoders"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(encoders.returncode == 0 and b"libx264" in encoders.stdout,
            "FFmpeg libx264 encoder not available")
    return {"powershell": ps, "godot": godot, "ffmpeg": ffmpeg, "ffprobe": ffprobe, "python": python,
            "ffmpeg_libx264_encoder_available": True,
            "ffmpeg_encoders_stdout_sha256": sha256_bytes(encoders.stdout),
            "ffmpeg_encoders_stderr_sha256": sha256_bytes(encoders.stderr)}


def build_launcher_command(powershell_path: str, launcher_path: Path, selector: dict[str, Any],
                           output_root: Path, output_tag: str) -> list[str]:
    """Return the exact permitted C11-C silent qualification invocation."""
    return [
        powershell_path, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(launcher_path),
        "-Seed", str(selector["gameplay_seed"]), "-Grammar", selector["grammar_id"],
        "-Duration", f"{selector['duration_seconds']:.1f}", "-NoSound",
        "-OutputRoot", str(output_root), "-OutputTag", output_tag,
    ]


def run_r1v(project_root: Path, r1p_archive: Path, policy_path: Path, approval_path: Path) -> dict[str, Any]:
    require(project_root.is_dir(), f"ProjectRoot not found: {project_root}")
    project_root = project_root.resolve(strict=True)
    require(sys.version_info[:2] == (3, 13), f"Python 3.13 required; found {sys.version.split()[0]}")

    policy_evidence = verify_approval_policy(project_root, policy_path, approval_path)
    r1p_evidence = verify_r1p_archive(project_root, r1p_archive)
    option_c_evidence = verify_option_c_evidence(project_root)
    tools = _tool_preflight(project_root)

    run_id = "R1V_Q5_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8].upper()
    evidence_parent = project_root / "artifacts" / "tests" / "c11e" / "r1v_five_family_qualification"
    evidence_root = evidence_parent / run_id
    output_parent = evidence_root / "source"
    require(not evidence_root.exists(), f"R1V evidence root collision: {evidence_root}")
    output_roots = []
    temp_silent_paths = []
    jobs = []
    for selector in SELECTOR_EXPECTATIONS:
        for repeat in ("A", "B"):
            tag = f"{run_id}_{selector['source_folder_key'].upper()}_{repeat}"
            output_root = output_parent / selector["source_folder_key"] / repeat
            stem = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{tag}"
            temp_silent = Path(tempfile.gettempdir()) / f"C11C_{stem}_silent.mp4"
            temp_avi_glob = f"{stem}_*.avi"
            jobs.append({"selector": selector, "repeat": repeat, "output_tag": tag,
                         "output_root": output_root, "temp_silent_path": temp_silent,
                         "temp_avi_glob": temp_avi_glob})
            output_roots.append(output_root)
            temp_silent_paths.append(temp_silent)
    for root in output_roots:
        require(not root.exists(), f"R1V output root already exists; refusing to clean or overwrite: {root}")
    for path in temp_silent_paths:
        require(not path.exists(), f"C11-C launcher would delete/overwrite pre-existing temp silent path; refusing: {path}")
    for job in jobs:
        stale_avi = list(Path(tempfile.gettempdir()).glob(job["temp_avi_glob"]))
        require(not stale_avi, f"C11-C launcher temporary AVI pattern already has files; refusing to risk deletion/reuse: {stale_avi}")

    # One global exclusive lock protects the temporary project override from concurrent R1V runs.
    lock_token = sha256_bytes(str(project_root).lower().encode("utf-8"))[:16]
    lock_path = Path(tempfile.gettempdir()) / f"C11E_R1V_{lock_token}.lock"
    lock_fd = None
    try:
        lock_fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise R1VError(f"Another R1V runner holds the project lock: {lock_path}") from exc

    evidence_root.mkdir(parents=True, exist_ok=False)
    (evidence_root / "processes").mkdir()
    (evidence_root / "inventories").mkdir()
    output_parent.mkdir(parents=True, exist_ok=True)
    # Create selector parent folders only. All ten OutputRoot leaves remain nonexistent.
    for selector in SELECTOR_EXPECTATIONS:
        (output_parent / selector["source_folder_key"]).mkdir(parents=True, exist_ok=True)

    override_path = project_root / "override.cfg"
    override_backup_preimage = temp_file_state("C11C_override_backup_*.cfg")
    override_existed = override_path.exists()
    override_bytes = override_path.read_bytes() if override_existed else None
    override_sha = sha256_bytes(override_bytes) if override_bytes is not None else None
    override_evidence = {
        "path": str(override_path),
        "existed_before": override_existed,
        "sha256_before": override_sha,
        "restored_after_each_launcher": True,
        "temporary_write_expected_from_pinned_C11CMovieCapture_helper": True,
        "preexisting_temp_backup_files": override_backup_preimage,
    }
    if override_existed:
        (evidence_root / "override_cfg_preimage.bin").write_bytes(override_bytes or b"")

    run_manifest = {
        "schema": "C11E-R1V-FIVE-FAMILY-QUALIFICATION-RUN-MANIFEST-V1",
        "run_id": run_id,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        "policy": policy_evidence,
        "r1p": r1p_evidence,
        "option_c": option_c_evidence,
        "runtime_executables": tools,
        "scope": {
            "selector_count": 5, "repeat_count_per_selector": 2, "planned_launcher_invocations": 10,
            "allowed_c11c_no_sound_mp4_encode_only": True,
            "ffmpeg_filters": False, "audio_or_d3": False, "mux": False,
            "d_compositor": False, "d9_10_renderer_dispatch": False,
            "ffprobe_read_only": True, "ffmpeg_decode_only_pipe_to_memory": True,
            "music_seed_passed_to_visual_launcher": False,
            "keep_avi": False, "export_gif": False, "no_footer_switch": False,
        },
        "output_roots": [str(x) for x in output_roots],
        "output_root_preflight": "ALL_TEN_NONEXISTENT_BEFORE_FIRST_LAUNCHER",
        "temp_silent_paths": [str(x) for x in temp_silent_paths],
        "temp_silent_path_preflight": "ALL_TEN_NONEXISTENT_BEFORE_FIRST_LAUNCHER; NO_PREEXISTING_TEMP_FILE_DELETION",
        "temp_avi_patterns": [j["temp_avi_glob"] for j in jobs],
        "temp_avi_preflight": "ALL_TEN_PATTERNS_EMPTY_BEFORE_FIRST_LAUNCHER; LAUNCHER_MUST_DELETE_INTERMEDIATE_AVI",
        "output_tag_contains_unique_run_id": True,
        "temporary_override_cfg": override_evidence,
        "source_media_contract": {
            "width": 720, "height": 1280, "fps": 30, "video_codec": "libx264",
            "pixel_format": "yuv420p", "audio_streams": 0,
            "allowed_encode_argv_template": ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", "<AVI>", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "<MP4>"],
        },
        "jobs": [{"family_id": j["selector"]["family_id"], "grammar_id": j["selector"]["grammar_id"],
                  "repeat": j["repeat"], "seed": j["selector"]["gameplay_seed"],
                  "duration_seconds": j["selector"]["duration_seconds"],
                  "output_root": str(j["output_root"]), "output_tag": j["output_tag"]} for j in jobs],
        "governance": {"c11c_source_capture": "AUTHORIZED_R1V_LIMITED_ONLY", "d_renderer_dispatch": "OFF",
                       "d4_8_general_production": "BLOCKED", "d9_10": "PREPARE_ONLY",
                       "d9_14": "BLOCKED", "d9_16": "BLOCKED", "d9_17": "BLOCKED_NO_GO",
                       "d10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE"},
    }
    manifest_hash = dump_json(evidence_root / "r1v_run_manifest.json", run_manifest)
    dump_json(evidence_root / "preflight_report.json", {
        "schema": "C11E-R1V-FIVE-FAMILY-PREFLIGHT-REPORT-V1", "status": "PASS_R1V_PRELAUNCH_PREFLIGHT",
        "run_id": run_id, "policy": policy_evidence, "r1p": r1p_evidence, "option_c": option_c_evidence,
        "runtime_executables": tools, "output_roots": [str(x) for x in output_roots],
        "output_roots_all_nonexistent": True, "source_mutation": False, "launcher_invocations": 0,
    })

    process_records = []
    inventory_rows = []
    failure = None
    try:
        for job_index, job in enumerate(jobs, start=1):
            selector = job["selector"]
            repeat = job["repeat"]
            output_root = job["output_root"]
            require(not output_root.exists(), f"Output root appeared after preflight; refusing: {output_root}")
            require(not job["temp_silent_path"].exists(),
                    f"C11-C launcher temp silent path appeared after preflight; refusing: {job['temp_silent_path']}")
            require(not list(Path(tempfile.gettempdir()).glob(job["temp_avi_glob"])),
                    f"C11-C launcher temp AVI path appeared after preflight; refusing: {job['temp_avi_glob']}")
            launcher_path = safe_project_file(project_root, selector["launcher_path"])
            command = build_launcher_command(tools["powershell"]["path"], launcher_path, selector,
                                             output_root, job["output_tag"])
            log_key = f"{job_index:02d}_{selector['source_folder_key']}_{repeat}"
            stdout_path = evidence_root / "processes" / f"{log_key}.stdout.log"
            stderr_path = evidence_root / "processes" / f"{log_key}.stderr.log"
            start_epoch = time.time()
            start = datetime.now(timezone.utc).isoformat()
            result = subprocess.run(command, cwd=str(project_root), stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=3600, check=False)
            stdout_path.write_bytes(result.stdout)
            stderr_path.write_bytes(result.stderr)
            stdout_sha = sha256_file(stdout_path)
            stderr_sha = sha256_file(stderr_path)
            process_record = {
                "job_index": job_index, "job_id": log_key,
                "family_id": selector["family_id"], "grammar_id": selector["grammar_id"],
                "repeat": repeat, "seed": selector["gameplay_seed"], "duration_seconds": selector["duration_seconds"],
                "executable": tools["powershell"]["path"], "executable_sha256": tools["powershell"]["sha256"],
                "arguments": command[1:], "cwd": str(project_root), "output_root": str(output_root),
                "started_utc": start, "started_epoch": start_epoch,
                "completed_utc": datetime.now(timezone.utc).isoformat(), "completed_epoch": time.time(),
                "exit_code": result.returncode,
                "stdout_path": str(stdout_path), "stdout_sha256": stdout_sha,
                "stderr_path": str(stderr_path), "stderr_sha256": stderr_sha,
            }
            process_records.append(process_record)
            if result.returncode != 0:
                raise R1VError(f"C11-C launcher failed for {selector['family_id']} repeat {repeat}: exit={result.returncode}")

            require(not job["temp_silent_path"].exists(),
                    f"C11-C launcher left or created a temp silent file outside the approved output root: {job['temp_silent_path']}")
            require(not list(Path(tempfile.gettempdir()).glob(job["temp_avi_glob"])),
                    f"C11-C launcher failed to delete its intermediate AVI: {job['temp_avi_glob']}")
            # Ensure this invocation did not leave the helper's uniquely named override backup behind.
            current_backup_state = temp_file_state("C11C_override_backup_*.cfg")
            new_backup_files = sorted(set(current_backup_state) - set(override_backup_preimage))
            require(not new_backup_files,
                    f"C11CMovieCapture left temporary override backup residue: {new_backup_files}")
            require(all(current_backup_state.get(name) == digest for name, digest in override_backup_preimage.items()),
                    "A pre-existing C11CMovieCapture backup file changed during R1V")

            # Ensure every C11-C/Option-C/policy source pin remains unchanged after each launcher.
            post_source_guard = verify_source_pins_after_capture(project_root, r1p_archive, policy_path, approval_path)
            require(post_source_guard["total_source_pin_validations"] == 61,
                    "Post-launch source pin validation count differs from 61")
            process_record["post_launch_source_guard"] = post_source_guard

            # Ensure the MovieCapture temporary override restored the exact user preimage.
            override_result = restore_known_c11c_override_state(override_path, override_existed, override_bytes)
            process_record["override_cfg_post_launcher"] = override_result
            if override_result not in ("PASS_ORIGINAL_PREIMAGE_PRESENT", "PASS_ORIGINALLY_ABSENT"):
                override_evidence["restored_after_each_launcher"] = False
                raise R1VError(f"override.cfg required emergency restoration after {log_key}; run marked FAIL")

            # Sidecars must have been generated by this invocation, not copied from a stale canonical artifact.
            stdout_text = result.stdout.decode("utf-8", errors="replace")
            require("[C11-C-2.16.3] PASS" in stdout_text,
                    f"C11-C launcher did not report its own PASS: {selector['family_id']} {repeat}")
            inspected = inspect_source_video(project_root, output_root, selector, repeat, tools, job)
            for generated_key in ("video_path",):
                generated_path = Path(inspected[generated_key])
                require(generated_path.stat().st_mtime >= start_epoch - 1.0,
                        f"C11-C output appears older than this invocation (stale artifact): {generated_path}")
            for required_name in (f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['output_tag']}_authoring.json",
                                  f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['output_tag']}_manifest.json",
                                  f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['output_tag']}_godot.log",
                                  f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['output_tag']}_social.txt"):
                generated_sidecar = output_root / required_name
                require(generated_sidecar.stat().st_mtime >= start_epoch - 1.0,
                        f"C11-C sidecar appears older than this invocation (stale artifact): {generated_sidecar}")
            inspected["process"] = process_record
            inventory_rows.append(inspected)
            dump_json(evidence_root / "progress.json", {
                "schema": "C11E-R1V-PROGRESS-V1", "run_id": run_id,
                "completed_launcher_invocations": len(process_records),
                "completed_inventories": len(inventory_rows), "last_job": log_key,
                "status": "RUNNING_FAIL_CLOSED_ON_NEXT_ERROR",
            })
    except Exception as exc:
        failure = str(exc)
    finally:
        # Final guard: restore only the exact override preimage observed before the first launch.
        try:
            final_override_result = restore_known_c11c_override_state(override_path, override_existed, override_bytes)
            override_evidence["final_guard_result"] = final_override_result
            if final_override_result not in ("PASS_ORIGINAL_PREIMAGE_PRESENT", "PASS_ORIGINALLY_ABSENT"):
                override_evidence["restored_by_final_guard"] = True
        except Exception as override_exc:
            override_evidence["final_guard_result"] = f"FAIL_PRESERVED_UNKNOWN_STATE: {override_exc}"
            if failure is None:
                failure = str(override_exc)
        override_evidence["temp_backup_files_after"] = temp_file_state("C11C_override_backup_*.cfg")
        if lock_fd is not None:
            os.close(lock_fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass

    post_run_source_guard = None
    try:
        post_run_source_guard = verify_source_pins_after_capture(project_root, r1p_archive, policy_path, approval_path)
        require(post_run_source_guard["total_source_pin_validations"] == 61,
                "Final source pin validation count differs from 61")
        final_backup_state = temp_file_state("C11C_override_backup_*.cfg")
        require(final_backup_state == override_backup_preimage,
                "C11CMovieCapture temporary override backup inventory differs from pre-run state")
        require(all(not p.exists() for p in temp_silent_paths),
                "One or more C11-C temp silent intermediate files remain after R1V")
        require(all(not list(Path(tempfile.gettempdir()).glob(j["temp_avi_glob"])) for j in jobs),
                "One or more C11-C intermediate AVI files remain after R1V")
    except Exception as exc:
        if failure is None:
            failure = str(exc)

    deterministic = None
    if failure is None:
        try:
            deterministic = compare_repeats(inventory_rows)
        except Exception as exc:
            failure = str(exc)

    status = ("PASS_R1V_FIVE_FAMILY_TECHNICAL_CAPTURE_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW"
              if failure is None else "FAIL_R1V_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED")
    report = {
        "schema": "C11E-R1V-FIVE-FAMILY-QUALIFICATION-REPORT-V1",
        "status": status,
        "run_id": run_id,
        "r1v_run_manifest_sha256": manifest_hash,
        "preflight": "PASS_R1V_PRELAUNCH_PREFLIGHT",
        "approval": policy_evidence,
        "r1p": {k: v for k, v in r1p_evidence.items() if k != "source_pin_results"},
        "option_c": option_c_evidence,
        "planned_launcher_invocations": 10,
        "completed_launcher_invocations": len(process_records),
        "completed_frame_inventories": len(inventory_rows),
        "processes": process_records,
        "inventories": [{k: v for k, v in row.items() if k not in ("frame_hashes", "pts", "format_metadata", "video_stream")}
                        for row in inventory_rows],
        "deterministic_repeats": deterministic,
        "override_cfg_integrity": override_evidence,
        "post_run_source_guard": post_run_source_guard,
        "failure": failure,
        "scope": {
            "c11c_source_capture_invoked": bool(process_records),
            "c11c_silent_mp4_encode_allowed_and_used_by_pinned_launcher": bool(inventory_rows),
            "ffmpeg_decode_only_used": bool(inventory_rows),
            "ffprobe_read_only_used": bool(inventory_rows),
            "ffmpeg_filters": False, "audio_or_d3": False, "mux": False,
            "d_compositor": False, "d9_10_renderer_dispatch": False,
            "source_video_bytes_modified": False,
            "music_seed_passed_to_visual_launcher": False,
            "frame_files_spooled_to_disk": False,
        },
        "governance": {
            "c11c_source_capture": "R1V_LIMITED_SCOPE_ONLY",
            "d_renderer_dispatch": "OFF",
            "d4_8_general_production": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
            "release_authority": "NONE",
        },
    }
    report_hash = dump_json(evidence_root / "r1v_report.json", report)
    (evidence_root / "r1v_report.sha256").write_text(f"{report_hash}  r1v_report.json\n", encoding="ascii")
    process_receipt = {
        "schema": "C11E-R1V-FIVE-FAMILY-PROCESS-RECEIPT-V1",
        "run_id": run_id,
        "python_version": sys.version.split()[0],
        "python_executable": sys.executable,
        "python_executable_sha256": sha256_file(Path(sys.executable)),
        "powershell_version": tools["powershell"]["version_output"],
        "r1v_policy_sha256": policy_evidence["policy_sha256"],
        "approval_record_sha256": policy_evidence["approval_record_sha256"],
        "r1p_recovered_zip_sha256": R1P_RECOVERED_ZIP_SHA256,
        "option_c_report_sha256": OPTION_C_REPORT_SHA256,
        "runtime_executable_pins": tools,
        "launcher_process_count": len(process_records),
        "processes": process_records,
        "report_sha256": report_hash,
        "exit_code": 0 if failure is None else 1,
        "status": status,
        "failure": failure,
    }
    process_hash = dump_json(evidence_root / "r1v_process_receipt.json", process_receipt)
    (evidence_root / "r1v_process_receipt.sha256").write_text(f"{process_hash}  r1v_process_receipt.json\n", encoding="ascii")

    # Bundle the immutable source MP4s, measured inventories, logs and receipts for transfer/review.
    bundle_path = evidence_parent / f"{run_id}_EVIDENCE.zip"
    require(not bundle_path.exists(), f"R1V evidence ZIP collision: {bundle_path}")
    with zipfile.ZipFile(bundle_path, "x", compression=zipfile.ZIP_STORED, allowZip64=True) as bundle:
        for path in sorted(evidence_root.rglob("*")):
            if path.is_file():
                bundle.write(path, arcname=path.relative_to(evidence_root).as_posix())
    with zipfile.ZipFile(bundle_path, "r") as bundle:
        require(bundle.testzip() is None, "R1V evidence ZIP CRC failure")
    result = {
        "status": status,
        "run_id": run_id,
        "report_path": str(evidence_root / "r1v_report.json"),
        "report_sha256": report_hash,
        "process_receipt_path": str(evidence_root / "r1v_process_receipt.json"),
        "process_receipt_sha256": process_hash,
        "completed_launcher_invocations": len(process_records),
        "completed_frame_inventories": len(inventory_rows),
        "evidence_zip": str(bundle_path),
        "evidence_zip_sha256": sha256_file(bundle_path),
        "failure": failure,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if failure is not None:
        return result
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--r1p-recovered-zip", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--approval-record", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = run_r1v(args.project_root, args.r1p_recovered_zip, args.policy, args.approval_record)
        return 0 if result["status"].startswith("PASS_") else 1
    except Exception as exc:
        print(json.dumps({"status": "FAIL_R1V_PREFLIGHT_OR_EXECUTION", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
