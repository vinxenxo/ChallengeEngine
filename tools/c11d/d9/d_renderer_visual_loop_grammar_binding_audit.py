"""C11-D read-only source-pinned audit of the geometric Visual Loop grammar path.

The Godot probe evaluates only C11CVariationProfile values in memory. It does not
instantiate the prototype renderer, create a shader/material, emit renderer input,
write a receipt or media, or change source files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - environment contract
    raise RuntimeError("jsonschema is required for D9.12 audit contract validation") from exc

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_BINDING_AUDIT_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_BINDING_AUDIT_SCHEMA_V1.json")
RECEIPT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_BINDING_RECEIPT_SCHEMA_V1.json")
HARNESS_REL = Path("tools/c11d/d9/probe_visual_loop_grammar_binding_in_memory.gd")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT_VERSION = "4.7.1.stable.mono.official.a13da4feb"
RECEIPT_PREFIX = "C11D_GRAMMAR_PROBE_RECEIPT="

EXPECTED_GRAMMARS = [
    "harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"
]
EXPECTED_STYLE_ORDER = [
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow_strength",
    "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude",
    "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength",
    "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]
EXPECTED_STYLE_ARGUMENT_ORDER = [
    "grammar_mode", "palette_mode", "morph_value", "wave_frequency", "line_width", "glow_strength",
    "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude",
    "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength",
    "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]
EXPECTED_PROFILE_INPUT_ORDER = [
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow",
    "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude",
    "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength",
    "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]
PROTECTED_C11C_PATHS = {
    "tools/prototypes/c11c_common/C11CVariationProfile.gd",
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd",
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd",
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader",
    "tools/prototypes/c11c_geometric_waves_v1/definition.json",
}


class GrammarAuditError(RuntimeError):
    pass


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    try:
        return _sha256_bytes(path.read_bytes())
    except OSError as exc:
        raise GrammarAuditError(f"Cannot read pinned source {path}: {exc}") from exc


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GrammarAuditError(f"Cannot load JSON {path}: {exc}") from exc


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GrammarAuditError(message)


def load_and_validate_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract_path = root / CONTRACT_REL
    schema_path = root / CONTRACT_SCHEMA_REL
    receipt_schema_path = root / RECEIPT_SCHEMA_REL
    contract = _load_json(contract_path)
    schema = _load_json(schema_path)
    receipt_schema = _load_json(receipt_schema_path)

    _require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "Audit schema must be Draft 2020-12")
    _require(receipt_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "Receipt schema must be Draft 2020-12")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(receipt_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(contract), key=lambda e: list(e.absolute_path))
    if errors:
        first = errors[0]
        where = "/".join(str(v) for v in first.absolute_path) or "<root>"
        raise GrammarAuditError(f"Audit contract schema rejected {where}: {first.message}")

    _require(contract.get("governance", {}).get("frozen_c11c_manifest_sha256") == EXPECTED_MANIFEST_SHA256,
             "Frozen C11-C manifest identity changed")
    lineage = contract.get("source_lineage")
    _require(isinstance(lineage, list) and len(lineage) == 13, "Exactly 13 pinned sources are required")
    seen: set[str] = set()
    for index, row in enumerate(lineage):
        _require(isinstance(row, dict) and set(row) == {"path", "sha256"}, "Malformed source-lineage row")
        rel = row["path"]
        _require(isinstance(rel, str) and rel and not Path(rel).is_absolute() and ".." not in Path(rel).parts and "\\" not in rel,
                 f"Unsafe source path: {rel!r}")
        _require(rel not in seen, f"Duplicate source path: {rel}")
        seen.add(rel)
        actual = _sha256_file(root / rel)
        _require(actual == row["sha256"], f"Pinned source drift: {rel}")
        if index == 0:
            _require(rel == MANIFEST_REL.as_posix() and actual == EXPECTED_MANIFEST_SHA256,
                     "Frozen C11-C manifest must be the first exact source pin")

    manifest = _load_json(root / MANIFEST_REL)
    manifest_map = {str(row.get("path")): str(row.get("sha256")) for row in manifest.get("source_files", []) if isinstance(row, dict)}
    for rel in PROTECTED_C11C_PATHS:
        row = next((r for r in lineage if r["path"] == rel), None)
        _require(row is not None, f"Protected C11-C source is not pinned: {rel}")
        _require(manifest_map.get(rel) == row["sha256"], f"C11-C source pin does not match frozen manifest: {rel}")

    _static_source_audit(root, contract)
    return contract, schema, receipt_schema


def _quoted_ids(source: str, pattern: str, label: str) -> list[str]:
    match = re.search(pattern, source, flags=re.S | re.M)
    _require(match is not None, f"Could not parse {label} from pinned source")
    return re.findall(r'"([a-z_]+)"', match.group(1))


def _static_source_audit(root: Path, contract: Mapping[str, Any]) -> dict[str, bool]:
    producer = _load_json(root / "c11c-suite/c11c-producer/producer_schema.json")
    family = producer.get("families", {}).get("c11c_geometric_waves_v1", {})
    producer_grammars = [str(row[0]) for row in family.get("grammars", []) if isinstance(row, list) and row and row[0] != "auto"]
    _require(producer_grammars == EXPECTED_GRAMMARS, "Producer schema grammar inventory or order changed")

    proto_rel = root / "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd"
    proto = proto_rel.read_text(encoding="utf-8-sig")
    proto_grammars = _quoted_ids(proto, r"const\s+GRAMMAR_IDS:\s*Array\[String\]\s*=\s*\[(.*?)\]", "prototype grammar IDs")
    _require(proto_grammars == EXPECTED_GRAMMARS, "Prototype grammar IDs/order differs from Producer registry")
    for required in (
        'OS.get_environment("C11C_VISUAL_GRAMMAR")',
        '_variation["grammar_mode"] = index',
        '_variation["grammar_name"] = technical_id',
        'requested == technical_id or requested == artistic_id',
    ):
        _require(required in proto, f"Prototype override path missing: {required}")

    profile = (root / "tools/prototypes/c11c_common/C11CVariationProfile.gd").read_text(encoding="utf-8-sig")
    geometric_start = profile.find("static func _geometric")
    fractal_start = profile.find("static func _fractal", geometric_start + 1)
    _require(geometric_start >= 0 and fractal_start > geometric_start, "Cannot isolate geometric variation profile")
    geometric = profile[geometric_start:fractal_start]
    profile_grammars = _quoted_ids(geometric, r"var\s+grammar_modes:\s*Array\[String\]\s*=\s*\[(.*?)\]", "geometric profile grammar IDs")
    _require(profile_grammars == EXPECTED_GRAMMARS, "Seed-derived profile grammar order differs from prototype selector inventory")
    _require('var grammar_index: int = _index(seed_value, 11, grammar_modes.size())' in geometric,
             "Expected seed-derived grammar selection path changed; refresh the audit before proceeding")
    geometric_profile_keys = set(re.findall(r'^\s*"([a-z_]+)"\s*:', geometric, flags=re.M))
    missing_profile_fields = sorted(set(EXPECTED_PROFILE_INPUT_ORDER) - geometric_profile_keys)
    _require(not missing_profile_fields,
             f"Pinned C11-C geometric profile is missing probe input fields: {missing_profile_fields}")

    renderer = (root / "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd").read_text(encoding="utf-8-sig")
    signature = re.search(r"func\s+set_style\s*\((.*?)\)\s*->\s*void\s*:", renderer, flags=re.S)
    _require(signature is not None, "Cannot parse frozen GeometricWavesRenderer.set_style signature")
    style_order = re.findall(r"^\s*([a-z_]+)\s*:\s*(?:int|float)\s*,?\s*$", signature.group(1), flags=re.M)
    _require(style_order == EXPECTED_STYLE_ARGUMENT_ORDER, "Renderer style signature order differs from its pinned argument-order contract")
    _require(contract["grammar_binding"]["renderer_style_argument_order"] == EXPECTED_STYLE_ARGUMENT_ORDER, "Contract renderer style argument order mismatch")
    _require(contract["grammar_binding"]["style_parameter_order"] == EXPECTED_STYLE_ORDER, "Contract shader parameter projection order mismatch")
    _require('_material.set_shader_parameter("grammar_mode", clampi(grammar_mode, 0, 4))' in renderer,
             "Renderer no longer maps selected grammar index to the shader uniform")
    _require('_material.set_shader_parameter("wave_frequency", max(wave_frequency, 5.0))' in renderer,
             "Renderer style setter parameter projection drifted")

    shader = (root / "tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader").read_text(encoding="utf-8-sig")
    _require("uniform int grammar_mode = 0;" in shader, "Shader grammar uniform declaration changed")
    _require("if (grammar_mode == 0)" in shader and "return field_harmonic_membrane(q, local_phase, layer);" in shader,
             "Shader index 0 is not visibly bound to harmonic_membrane function")
    for grammar_name in EXPECTED_GRAMMARS:
        _require(f"field_{grammar_name}" in shader, f"Shader function for grammar missing: {grammar_name}")

    authoring = (root / "core/authoring/VisualAuthoringGenerator.gd").read_text(encoding="utf-8-sig")
    adapter = (root / "core/authoring/adapters/VisualLoopAuthoringAdapter.gd").read_text(encoding="utf-8-sig")
    _require('payload_result = LoopAdapter.build_payload(request, resolved)' in authoring,
             "Visual Loop authoring route changed; refresh scope audit")
    _require('"generator": request.subtype' in adapter and '"grammar_mode"' not in adapter,
             "Visual Loop family authoring adapter no longer exhibits the pinned family-level limitation")

    dynamic_contract = _load_json(root / "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json")
    loop_scope = dynamic_contract.get("supported_selector_matrix", {}).get("visual_loops", {})
    _require(loop_scope.get("exact_selector_payload_materialized") is False,
             "Prior dynamic request contract must continue to disclose the unresolved exact Loop payload")
    _require(loop_scope.get("payload_scope") == "VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED",
             "Prior dynamic request scope was changed unexpectedly")
    dynamic_harness = (root / "tools/c11d/d9/materialize_dynamic_request_payload_in_memory.gd").read_text(encoding="utf-8-sig")
    _require('"payload_scope":"VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED"' in dynamic_harness and
             '"exact_selector_payload_materialized":false' in dynamic_harness,
             "Existing dynamic probe no longer preserves unresolved grammar-instance status")

    binding = contract.get("grammar_binding", {})
    _require(binding.get("prototype_grammar_ids") == EXPECTED_GRAMMARS, "Contract prototype grammar order drift")
    _require(binding.get("style_parameter_order") == EXPECTED_STYLE_ORDER, "Contract shader parameter projection order drift")
    _require(binding.get("renderer_style_argument_order") == EXPECTED_STYLE_ARGUMENT_ORDER, "Contract renderer argument order drift")
    harness = (root / HARNESS_REL).read_text(encoding="utf-8-sig")
    projected_keys = _quoted_ids(harness, r"const\s+STYLE_KEYS:\s*Array\[String\]\s*=\s*\[(.*?)\]", "probe style parameter keys")
    _require(projected_keys == EXPECTED_STYLE_ORDER, "Godot probe shader-parameter projection order drift")
    profile_input_keys = _quoted_ids(harness, r"const\s+PROFILE_INPUT_KEYS:\s*Array\[String\]\s*=\s*\[(.*?)\]", "probe source-profile input keys")
    _require(profile_input_keys == EXPECTED_PROFILE_INPUT_ORDER, "Godot probe C11-C profile input field order drift")
    _require('"glow_strength": clamp(float(value["glow"]), 0.0, 1.0)' in harness,
             "C11-C profile `glow` must map explicitly to renderer output `glow_strength`")
    _require("for key: String in PROFILE_INPUT_KEYS:" in harness and "for key: String in STYLE_KEYS:" not in harness,
             "Probe must validate source profile keys independently of renderer output keys")
    seed_match = re.search(r"const\s+SEEDS:\s*Array\[int\]\s*=\s*\[(.*?)\]", harness, flags=re.S | re.M)
    _require(seed_match is not None, "Could not parse pinned runtime seed set")
    probe_seeds = [int(v) for v in re.findall(r"\d+", seed_match.group(1))]
    _require(probe_seeds == binding.get("runtime_seed_set"), "Godot probe seed set differs from its contract")
    return {
        "producer_registry": True,
        "prototype_override": True,
        "seed_profile": True,
        "profile_input_fields": True,
        "renderer_style_signature": True,
        "shader_branch": True,
        "family_envelope_gap": True,
        "governance_locked": True,
    }


def validate_runtime_receipt(receipt: Mapping[str, Any], contract: Mapping[str, Any], receipt_schema: Mapping[str, Any]) -> None:
    errors = sorted(Draft202012Validator(receipt_schema).iter_errors(dict(receipt)), key=lambda e: list(e.absolute_path))
    if errors:
        first = errors[0]
        where = "/".join(str(v) for v in first.absolute_path) or "<root>"
        raise GrammarAuditError(f"Godot probe receipt rejected at {where}: {first.message}")
    expected_binding = contract["grammar_binding"]
    _require(receipt["mapping"]["grammar_ids"] == expected_binding["prototype_grammar_ids"], "Runtime receipt grammar inventory drift")
    _require(receipt["mapping"]["selected_grammar_index"] == expected_binding["selected_grammar_index"], "Runtime selected grammar index drift")
    _require(receipt["mapping"]["style_parameter_count"] == expected_binding["style_parameter_count"], "Runtime style parameter count drift")
    cases = receipt["seed_cases"]
    expected_seeds = expected_binding["runtime_seed_set"]
    _require([case["seed"] for case in cases] == expected_seeds, "Runtime seed matrix/order mismatch")
    digests: set[str] = set()
    for case in cases:
        _require(case["bound_grammar_id"] == expected_binding["selected_grammar_id"], "Selected grammar varies from canonical selector")
        _require(case["bound_grammar_index"] == expected_binding["selected_grammar_index"], "Selected grammar index varies from canonical selector")
        _require(case["style_parameter_count"] == len(expected_binding["style_parameter_order"]), "Style parameter evidence count mismatch")
        _require(case["deterministic_repeat"] is True and case["style_sha256"] == case["repeat_style_sha256"],
                 "Same-seed style projection is non-deterministic")
        _require(re.fullmatch(r"[0-9a-f]{64}", case["style_sha256"]) is not None, "Malformed style digest")
        digests.add(case["style_sha256"])
    _require(len(digests) >= 2, "Seed changes did not change visual style evidence")
    for key in (
        "prototype_override_source_pinned", "renderer_set_style_source_pinned", "shader_branch_source_pinned",
        "family_envelope_grammar_gap_remains", "seed_profile_changes_style_parameters", "selected_grammar_is_seed_independent"
    ):
        _require(receipt["findings"][key] is True, f"Runtime finding is not proven: {key}")
    _require(receipt["findings"]["exact_selector_payload_materialized"] is False,
             "Probe may not claim exact grammar payload materialization")
    boundary = receipt["execution_boundary"]
    for key in ("renderer_native_input_emitted", "renderer_instance_created", "renderer_dispatch_invoked", "shader_executed", "media_created", "disk_writes", "c11c_source_mutation", "candidate_input_admissible"):
        _require(boundary[key] is False, f"Forbidden operation/authority reported: {key}")
    _require(boundary["renderer"] == "OFF" and boundary["d4_8"] == "BLOCKED" and boundary["release_authority"] == "NONE",
             "Governance status was relaxed")


def run_godot_probe(root: Path, godot: str, timeout: int) -> dict[str, Any]:
    version = subprocess.run([godot, "--version"], cwd=root, text=True, capture_output=True, timeout=min(timeout, 30), check=False)
    actual_version = (version.stdout or version.stderr).strip()
    _require(version.returncode == 0 and actual_version == EXPECTED_GODOT_VERSION,
             f"Godot version must be {EXPECTED_GODOT_VERSION}; got {actual_version!r}")
    command = [godot, "--headless", "--path", str(root), "--script", f"res://{HARNESS_REL.as_posix()}"]
    try:
        process = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise GrammarAuditError(f"Godot grammar probe timed out after {timeout}s") from exc
    output = "\n".join(part for part in (process.stdout, process.stderr) if part)
    if process.returncode != 0:
        raise GrammarAuditError(f"Godot grammar probe failed (exit={process.returncode}):\n{output[-12000:]}")
    receipt_lines = [line.split(RECEIPT_PREFIX, 1)[1].strip() for line in output.splitlines() if RECEIPT_PREFIX in line]
    _require(len(receipt_lines) == 1, f"Expected exactly one stdout receipt from Godot; found {len(receipt_lines)}")
    try:
        receipt = json.loads(receipt_lines[0])
    except json.JSONDecodeError as exc:
        raise GrammarAuditError(f"Godot receipt JSON is malformed: {exc}") from exc
    contract, _, receipt_schema = load_and_validate_contract(root)
    validate_runtime_receipt(receipt, contract, receipt_schema)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", required=True, help="Absolute path to Godot 4.7.1 console executable")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)
    if args.timeout < 10 or args.timeout > 600:
        parser.error("--timeout must be between 10 and 600 seconds")
    root = Path(__file__).resolve().parents[3]
    try:
        contract, _, receipt_schema = load_and_validate_contract(root)
        receipt = run_godot_probe(root, args.godot, args.timeout)
        validate_runtime_receipt(receipt, contract, receipt_schema)
    except GrammarAuditError as exc:
        print(f"C11-D VISUAL LOOP GRAMMAR BINDING AUDIT FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE", file=sys.stderr)
        return 1
    print(
        "C11-D VISUAL LOOP GRAMMAR BINDING AUDIT PASS | "
        f"source_pins={len(contract['source_lineage'])}/{len(contract['source_lineage'])} | "
        f"runtime_seeds={len(receipt['seed_cases'])}/{len(contract['grammar_binding']['runtime_seed_set'])} | "
        "selector_to_prototype_grammar=PASS | style_parameters=20/20 | "
        "selected_grammar_seed_independent=true | family_envelope_grammar_gap=OPEN | "
        "exact_selector_payload_materialized=false | candidate_input_admissible=false | "
        "renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
