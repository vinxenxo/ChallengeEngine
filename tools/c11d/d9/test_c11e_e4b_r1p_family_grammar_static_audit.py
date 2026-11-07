#!/usr/bin/env python3
"""Read-only C11-E E4B-R1P family grammar/source mapping audit.

This utility checks that the explicit Loop selector order in producer_schema.json
matches both C11CVariationProfile.gd and the corresponding family prototype's
GRAMMAR_IDS array. It does not import project code, invoke Godot/PowerShell,
instantiate prototypes/renderers, write files, or create media.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_REL = Path("c11c-suite/c11c-producer/producer_schema.json")
VARIATION_REL = Path("tools/prototypes/c11c_common/C11CVariationProfile.gd")
PALETTE_REL = Path("tools/prototypes/c11c_common/C11CPaletteBank.gd")
DURATION_REL = Path("tools/prototypes/c11c_common/C11CVisualLoopDuration.gd")

FAMILY_FUNCTIONS = {
    "geometric": "_geometric",
    "fractal": "_fractal",
    "sacred_symmetry": "_sacred",
    "living_particles": "_living",
    "invisible_forces": "_invisible",
}
EXPECTED_FAMILIES = {
    "c11c_geometric_waves_v1": ("geometric", 5),
    "c11c_fractal_bloom_v1": ("fractal", 5),
    "c11c_sacred_symmetry_v1": ("sacred_symmetry", 5),
    "c11c_living_particles_v1": ("living_particles", 5),
    "c11c_invisible_forces_v1": ("invisible_forces", 7),
}


class AuditError(RuntimeError):
    """Raised when a source contract does not match."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(root: Path, relative: Path) -> tuple[Path, str]:
    path = root / relative
    if not path.is_file():
        raise AuditError(f"Required source file is missing: {relative.as_posix()}")
    try:
        return path, path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise AuditError(f"Cannot read {relative.as_posix()}: {exc}") from exc


def extract_string_array(source: str, pattern: str, label: str) -> list[str]:
    match = re.search(pattern, source, flags=re.DOTALL)
    if not match:
        raise AuditError(f"Cannot locate {label} string array")
    values = re.findall(r'"([A-Za-z0-9_]+)"', match.group(1))
    if not values:
        raise AuditError(f"{label} string array is empty")
    return values


def extract_profile_grammars(profile_source: str, function_name: str, internal_id: str) -> list[str]:
    function_pattern = rf"static\s+func\s+{re.escape(function_name)}\s*\("
    function_match = re.search(function_pattern, profile_source)
    if not function_match:
        raise AuditError(f"Variation profile function not found for {internal_id}: {function_name}")
    start = function_match.start()
    next_function = re.search(r"\nstatic\s+func\s+", profile_source[function_match.end():])
    end = function_match.end() + next_function.start() if next_function else len(profile_source)
    block = profile_source[start:end]
    return extract_string_array(
        block,
        r"var\s+grammar_modes(?:\s*:\s*[^=\n]+)?\s*=\s*(\[[\s\S]*?\])",
        f"{internal_id} variation-profile grammar_modes",
    )


def extract_prototype_grammars(prototype_source: str, prototype_path: str) -> list[str]:
    return extract_string_array(
        prototype_source,
        r"const\s+GRAMMAR_IDS(?:\s*:\s*[^=\n]+)?\s*=\s*(\[[\s\S]*?\])",
        f"{prototype_path} GRAMMAR_IDS",
    )


def run_audit(project_root: Path) -> dict[str, Any]:
    root = project_root.resolve(strict=True)
    schema_path, schema_text = read_text(root, SCHEMA_REL)
    variation_path, variation_text = read_text(root, VARIATION_REL)
    palette_path, palette_text = read_text(root, PALETTE_REL)
    duration_path, duration_text = read_text(root, DURATION_REL)

    try:
        schema = json.loads(schema_text)
    except json.JSONDecodeError as exc:
        raise AuditError(f"Invalid producer schema JSON: {exc}") from exc
    families = schema.get("families") if isinstance(schema, dict) else None
    if not isinstance(families, dict):
        raise AuditError("producer_schema.json does not contain a families object")
    if set(families) != set(EXPECTED_FAMILIES):
        raise AuditError(
            "Loop family set mismatch: "
            f"expected {sorted(EXPECTED_FAMILIES)}, got {sorted(families)}"
        )

    # API guards used by the subsequent parameter-only stage.
    if not re.search(r"static\s+func\s+build\s*\(family_id:\s*String,\s*seed_value:\s*int\)", variation_text):
        raise AuditError("C11CVariationProfile.build(family_id, seed_value) API signature changed")
    if not re.search(r"static\s+func\s+palette\s*\(family_id:\s*String,\s*palette_index:\s*int,\s*seed_value:\s*int\s*=\s*0\)", palette_text):
        raise AuditError("C11CPaletteBank.palette(family_id, palette_index, seed_value) API signature changed")
    if not re.search(r"const\s+FPS:\s*int\s*=\s*30", duration_text):
        raise AuditError("C11CVisualLoopDuration FPS is not the expected 30")
    if not re.search(r"static\s+func\s+policy_seconds_for_cycles\s*\(loop_cycles:\s*int\)", duration_text):
        raise AuditError("C11CVisualLoopDuration.policy_seconds_for_cycles API is missing")
    if not all(value in duration_text for value in ("return 20.0", "return 22.0", "return 23.0")):
        raise AuditError("C11CVisualLoopDuration 20/22/23-second cycle policy changed")

    family_results: list[dict[str, Any]] = []
    total = 0
    for family_id in sorted(EXPECTED_FAMILIES):
        expected_internal, expected_count = EXPECTED_FAMILIES[family_id]
        family = families[family_id]
        if not isinstance(family, dict):
            raise AuditError(f"Family record is not an object: {family_id}")
        internal = family.get("internal")
        if internal != expected_internal:
            raise AuditError(f"Family {family_id} internal ID changed: {internal!r}")

        raw_grammars = family.get("grammars")
        if not isinstance(raw_grammars, list) or not raw_grammars:
            raise AuditError(f"Family {family_id} has no grammar list")
        if not all(isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str) for item in raw_grammars):
            raise AuditError(f"Family {family_id} has malformed grammar entries")
        if raw_grammars[0][0] != "auto":
            raise AuditError(f"Family {family_id} no longer declares auto as its first grammar entry")
        schema_grammars = [item[0] for item in raw_grammars if item[0] != "auto"]
        if len(schema_grammars) != expected_count or len(set(schema_grammars)) != expected_count:
            raise AuditError(f"Family {family_id} explicit grammar count/uniqueness mismatch")

        function_name = FAMILY_FUNCTIONS[internal]
        profile_grammars = extract_profile_grammars(variation_text, function_name, internal)
        if profile_grammars != schema_grammars:
            raise AuditError(
                f"Family {family_id} schema/profile order mismatch: "
                f"schema={schema_grammars}, profile={profile_grammars}"
            )

        launcher = family.get("prototype")
        if not isinstance(launcher, str) or not launcher.endswith("/run_prototype.ps1"):
            raise AuditError(f"Family {family_id} canonical launcher path is malformed")
        prototype_dir = (root / launcher).parent
        if not prototype_dir.is_dir():
            raise AuditError(f"Family {family_id} prototype directory is missing: {prototype_dir}")
        prototype_candidates = sorted(prototype_dir.glob("*Prototype.gd"))
        if len(prototype_candidates) != 1:
            raise AuditError(
                f"Family {family_id} must contain exactly one *Prototype.gd; "
                f"found {len(prototype_candidates)}"
            )
        prototype_path = prototype_candidates[0]
        try:
            prototype_text = prototype_path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            raise AuditError(f"Cannot read prototype {prototype_path}: {exc}") from exc
        prototype_grammars = extract_prototype_grammars(prototype_text, prototype_path.relative_to(root).as_posix())
        if prototype_grammars != schema_grammars:
            raise AuditError(
                f"Family {family_id} schema/prototype order mismatch: "
                f"schema={schema_grammars}, prototype={prototype_grammars}"
            )
        if not re.search(r"_apply_grammar_override", prototype_text):
            raise AuditError(f"Family {family_id} prototype has no _apply_grammar_override hook")

        launcher_path, launcher_text = read_text(root, Path(launcher.replace("/", "/")))
        # Match the parameter contract used by the existing family-stage builder.
        header_end = launcher_text.find("$ErrorActionPreference")
        launcher_header = launcher_text[:header_end if header_end >= 0 else min(len(launcher_text), 12000)]
        missing = [p for p in ("$Seed", "$Grammar", "$NoSound", "$OutputRoot", "$OutputTag") if p.lower() not in launcher_header.lower()]
        if missing:
            raise AuditError(f"Family {family_id} launcher parameter contract missing: {missing}")

        selectors = [
            {"grammar_id": grammar, "grammar_index": index}
            for index, grammar in enumerate(schema_grammars)
        ]
        family_results.append({
            "family_id": family_id,
            "internal_family_id": internal,
            "grammar_count": len(schema_grammars),
            "selectors": selectors,
            "prototype_path": prototype_path.relative_to(root).as_posix(),
            "launcher_path": launcher_path.relative_to(root).as_posix(),
            "prototype_sha256": sha256_file(prototype_path),
            "launcher_sha256": sha256_file(launcher_path),
            "mapping": "PASS_SCHEMA_PROFILE_PROTOTYPE_EXACT_ORDER",
        })
        total += len(schema_grammars)

    if total != 27:
        raise AuditError(f"Expected exactly 27 explicit selectors across five families; got {total}")

    source_pins = {}
    for label, path in (
        ("producer_schema", schema_path),
        ("variation_profile", variation_path),
        ("palette_bank", palette_path),
        ("visual_loop_duration", duration_path),
    ):
        source_pins[label] = {"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path)}

    return {
        "schema": "C11E-E4B-R1P-STATIC-FAMILY-GRAMMAR-AUDIT-V1",
        "status": "PASS_STATIC_SOURCE_MAPPING",
        "scope": "READ_ONLY_SCHEMA_PROFILE_PROTOTYPE_AND_LAUNCHER_CONTRACT",
        "project_root": str(root),
        "family_count": len(family_results),
        "explicit_selector_count": total,
        "families": family_results,
        "shared_source_pins": source_pins,
        "governance": {
            "repository_files_written": False,
            "godot_invoked": False,
            "prototype_nodes_instantiated": False,
            "renderer_instantiated": False,
            "shader_created": False,
            "launchers_invoked": False,
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "frame_buffers_created": False,
            "pixels_created": False,
            "audio_or_d3_invoked": False,
            "ffmpeg_invoked": False,
            "media_created": False,
            "release_authority": "NONE",
        },
    }


def main() -> int:
    script_path = Path(__file__).resolve()
    default_root = script_path.parents[3] if len(script_path.parents) > 3 else Path.cwd()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=default_root,
                        help="Project root; defaults to the repository root derived from this script path")
    args = parser.parse_args()
    try:
        report = run_audit(args.project_root)
    except (AuditError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL_STATIC_SOURCE_MAPPING", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
