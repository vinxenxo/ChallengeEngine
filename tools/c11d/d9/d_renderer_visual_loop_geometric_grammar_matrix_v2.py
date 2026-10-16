"""Read-only Godot probe for five frozen geometric Visual Loop grammar parameter mappings.

This V2 extends parameter-mapping evidence only. It deliberately does not claim canonical
D9.9 request admission, exact selector payload admission, renderer input, or media output.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

sys.dont_write_bytecode = True
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - depends on environment
    raise RuntimeError("jsonschema is required for the Visual Loop geometric grammar matrix contract") from exc

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parents[2]
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_V2.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_CONTRACT_SCHEMA_V2.json")
INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_INPUT_SCHEMA_V2.json")
PROBE_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_OUTPUT_SCHEMA_V2.json")
AUDIT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_AUDIT_SCHEMA_V2.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
HARNESS_REL = Path("tools/c11d/d9/probe_visual_loop_geometric_grammar_matrix_v2.gd")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT_VERSION = "4.7.1.stable.mono.official.a13da4feb"
INPUT_SCHEMA_ID = "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-MATRIX-INPUT-V2"
PROBE_SCHEMA_ID = "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-MATRIX-PROBE-V2"
RECEIPT_SCHEMA_ID = "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-MATRIX-AUDIT-V2"
PROBE_PREFIX = "C11D_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_PROBE="
RECEIPT_PREFIX = "C11D_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_AUDIT="
STYLE_KEYS = (
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width",
    "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread",
    "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale",
    "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale",
)
GRAMMAR_MATRIX = (
    {"grammar_id": "harmonic_membrane", "grammar_index": 0, "shader_branch": "field_harmonic_membrane"},
    {"grammar_id": "interference_plane", "grammar_index": 1, "shader_branch": "field_interference_plane"},
    {"grammar_id": "parametric_ribbon", "grammar_index": 2, "shader_branch": "field_parametric_ribbon"},
    {"grammar_id": "lattice_wave", "grammar_index": 3, "shader_branch": "field_lattice_wave"},
    {"grammar_id": "orbital_wave", "grammar_index": 4, "shader_branch": "field_orbital_wave"},
)
SEEDS = (1, 12345, 54321, 2147483646)
BOUNDARY = {
    "mode": "GODOT_HEADLESS_IN_MEMORY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_ONLY",
    "canonical_request_chain_admitted": False,
    "canonical_selector_matrix_modified": False,
    "renderer_native_input_emitted": False,
    "renderer_instance_created": False,
    "renderer_dispatch_invoked": False,
    "shader_executed": False,
    "payload_files_written": False,
    "receipt_files_written": False,
    "media_created": False,
    "c11c_source_mutation": False,
    "renderer": "OFF",
    "d4_8": "BLOCKED",
    "release_authority": "NONE",
    "d9_14": "BLOCKED_AS_REQUIRED",
    "d9_16": "BLOCKED_AS_REQUIRED",
    "d9_17": "BLOCKED_NO_GO",
    "d10": "BLOCKED",
}


class GrammarMatrixAuditError(ValueError):
    """The grammar matrix audit failed closed."""


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _sha_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise GrammarMatrixAuditError(f"Required source is missing/unreadable: {path}: {exc}") from exc


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise GrammarMatrixAuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GrammarMatrixAuditError(f"JSON root must be an object: {path}")
    return value


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _root(value: str | Path | None = None) -> Path:
    return Path(value).resolve() if value is not None else ROOT_DEFAULT.resolve()


def load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root / CONTRACT_REL)
    contract_schema = _read_json(root / CONTRACT_SCHEMA_REL)
    input_schema = _read_json(root / INPUT_SCHEMA_REL)
    probe_schema = _read_json(root / PROBE_SCHEMA_REL)
    audit_schema = _read_json(root / AUDIT_SCHEMA_REL)
    for schema in (contract_schema, input_schema, probe_schema, audit_schema):
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise GrammarMatrixAuditError("All matrix schemas must use JSON Schema Draft 2020-12")
        Draft202012Validator.check_schema(schema)
    try:
        Draft202012Validator(contract_schema).validate(contract)
    except Exception as exc:
        raise GrammarMatrixAuditError(f"Contract schema rejection: {getattr(exc, 'message', str(exc))}") from exc

    if contract.get("schema") != "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-MATRIX-CONTRACT-V2":
        raise GrammarMatrixAuditError("Contract schema identity mismatch")
    if contract.get("schema_version") != "2.0":
        raise GrammarMatrixAuditError("Contract version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_NOT_CANONICAL_REQUEST_BINDING_NOT_RENDERER_INPUT":
        raise GrammarMatrixAuditError("Contract status is not preparation-only")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise GrammarMatrixAuditError("Contract C11-C manifest pin mismatch")
    if _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise GrammarMatrixAuditError("Active frozen C11-C manifest SHA-256 mismatch")
    scope = contract.get("scope", {})
    if scope.get("grammar_matrix") != list(GRAMMAR_MATRIX) or scope.get("seed_values") != list(SEEDS):
        raise GrammarMatrixAuditError("Contract is not the exact pinned five-grammar × four-seed matrix")
    if scope.get("expected_case_count") != len(GRAMMAR_MATRIX) * len(SEEDS):
        raise GrammarMatrixAuditError("Contract expected case count mismatch")
    if contract.get("execution_boundary") != BOUNDARY:
        raise GrammarMatrixAuditError("Contract execution/governance boundary changed")
    expected_approvals = {
        "geometric_grammar_parameter_matrix_approved": False,
        "canonical_request_selector_matrix_approved": False,
        "exact_selector_payload_approved": False,
        "editorial_visual_consumption_approved": False,
        "presentation_geometry_approved": False,
        "temporal_alignment_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approvals:
        raise GrammarMatrixAuditError("Contract attempted to self-promote an approval/freeze gate")

    lineage_raw = contract.get("source_lineage")
    if not isinstance(lineage_raw, list) or len(lineage_raw) != 12:
        raise GrammarMatrixAuditError("Exactly twelve pinned source-lineage entries are required")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, row in enumerate(lineage_raw):
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise GrammarMatrixAuditError("Malformed source-lineage entry")
        rel, expected = row["path"], row["sha256"]
        path = Path(rel) if isinstance(rel, str) else Path("invalid")
        if (not isinstance(rel, str) or path.is_absolute() or ".." in path.parts or "\\" in rel
                or rel in seen or not _is_sha(expected)):
            raise GrammarMatrixAuditError("Unsafe, duplicated, or malformed source-lineage entry")
        actual = _sha_file(root / path)
        if actual != expected:
            raise GrammarMatrixAuditError(f"Pinned source drift: {rel}")
        if index == 0 and (rel != MANIFEST_REL.as_posix() or expected != EXPECTED_MANIFEST_SHA256):
            raise GrammarMatrixAuditError("Frozen C11-C manifest must be the first source pin")
        seen.add(rel)
        lineage.append({"path": rel, "sha256": actual})
    expected_paths = {
        MANIFEST_REL.as_posix(),
        "c11c-suite/c11c-producer/producer_schema.json",
        "tools/prototypes/c11c_common/C11CVariationProfile.gd",
        "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd",
        "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd",
        "tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader",
        CONTRACT_SCHEMA_REL.as_posix(), INPUT_SCHEMA_REL.as_posix(), PROBE_SCHEMA_REL.as_posix(), AUDIT_SCHEMA_REL.as_posix(), HARNESS_REL.as_posix(),
        Path(__file__).resolve().relative_to(root).as_posix(),
    }
    if seen != expected_paths:
        raise GrammarMatrixAuditError("Source lineage path set is incomplete or includes an unexpected source")
    return contract, contract_schema, input_schema, probe_schema, audit_schema, lineage


def build_input(root: Path, contract: Mapping[str, Any]) -> dict[str, Any]:
    value = {
        "schema": INPUT_SCHEMA_ID,
        "schema_version": "2.0",
        "contract_sha256": _sha_file(root / CONTRACT_REL),
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "grammar_matrix": [dict(row) for row in GRAMMAR_MATRIX],
        "seeds": list(SEEDS),
    }
    try:
        Draft202012Validator(_read_json(root / INPUT_SCHEMA_REL)).validate(value)
    except Exception as exc:
        raise GrammarMatrixAuditError(f"Probe input does not satisfy the strict schema: {getattr(exc, 'message', str(exc))}") from exc
    return value


def validate_probe_report(report: Mapping[str, Any], probe_input: Mapping[str, Any], output_schema: Mapping[str, Any]) -> dict[str, Any]:
    if report.get("schema") != PROBE_SCHEMA_ID or report.get("schema_version") != "2.0":
        raise GrammarMatrixAuditError("Godot probe report identity/version mismatch")
    if report.get("status") != "PREPARATION_ONLY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_NOT_CANONICAL_REQUEST_BINDING_NOT_RENDERER_INPUT":
        raise GrammarMatrixAuditError("Godot report status is not preparation-only")
    if report.get("contract_sha256") != probe_input.get("contract_sha256"):
        raise GrammarMatrixAuditError("Godot report does not bind the current contract")
    if report.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise GrammarMatrixAuditError("Godot report C11-C manifest pin mismatch")
    if report.get("selection_family") != {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1"}:
        raise GrammarMatrixAuditError("Godot report family identity mismatch")
    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) != 20:
        raise GrammarMatrixAuditError("Godot report must contain exactly 20 grammar/seed cases")
    expected = {(row["grammar_id"], row["grammar_index"], row["shader_branch"], seed)
                for row in GRAMMAR_MATRIX for seed in SEEDS}
    seen: set[tuple[str, int, str, int]] = set()
    style_hashes_by_grammar: dict[str, set[str]] = {row["grammar_id"]: set() for row in GRAMMAR_MATRIX}
    for row in cases:
        if not isinstance(row, Mapping):
            raise GrammarMatrixAuditError("Malformed case row")
        key = (row.get("grammar_id"), row.get("grammar_index"), row.get("shader_branch"), row.get("gameplay_seed"))
        if key not in expected or key in seen:
            raise GrammarMatrixAuditError(f"Unknown or duplicate grammar/seed case: {key}")
        seen.add(key)
        if row.get("seed_profile_grammar_before_override") not in style_hashes_by_grammar:
            raise GrammarMatrixAuditError("Seed-derived profile grammar was not a known frozen geometry grammar")
        if row.get("style_parameter_count") != len(STYLE_KEYS):
            raise GrammarMatrixAuditError("A case did not emit exactly 20 style parameters")
        style = row.get("style_parameters")
        repeat_style = row.get("repeat_style_parameters")
        if not isinstance(style, Mapping) or not isinstance(repeat_style, Mapping):
            raise GrammarMatrixAuditError("Projected style parameter values are missing")
        if set(style) != set(STYLE_KEYS) or set(repeat_style) != set(STYLE_KEYS):
            raise GrammarMatrixAuditError("Projected style object must contain exactly the 20 pinned keys")
        for key in STYLE_KEYS:
            value = style[key]
            repeat_value = repeat_style[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or isinstance(repeat_value, bool) or not isinstance(repeat_value, (int, float)):
                raise GrammarMatrixAuditError(f"Non-numeric projected style value: {key}")
        if dict(style) != dict(repeat_style):
            raise GrammarMatrixAuditError(f"Independent repeat style values differ for {key}")
        if _sha_json(dict(style)) != row.get("style_sha256"):
            raise GrammarMatrixAuditError(f"Style parameter digest does not bind the values for {key}")
        for digest_key in ("style_sha256", "repeat_style_sha256", "parameter_instance_sha256", "repeat_parameter_instance_sha256"):
            if not _is_sha(row.get(digest_key)):
                raise GrammarMatrixAuditError(f"Malformed {digest_key} in case {key}")
        if row["style_sha256"] != row["repeat_style_sha256"] or row["parameter_instance_sha256"] != row["repeat_parameter_instance_sha256"]:
            raise GrammarMatrixAuditError(f"Independent in-process repeat digest mismatch for {key}")
        instance_core = {
            "schema": "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-PARAMETER-INSTANCE-V2",
            "schema_version": "2.0",
            "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": row["grammar_id"], "variant_id": None},
            "grammar_id": row["grammar_id"],
            "grammar_index": row["grammar_index"],
            "shader_branch": row["shader_branch"],
            "shader_uniform": "grammar_mode",
            "gameplay_seed": row["gameplay_seed"],
            "style_parameter_count": 20,
            "style_parameters": dict(style),
        }
        if _sha_json(instance_core) != row["parameter_instance_sha256"]:
            raise GrammarMatrixAuditError(f"Parameter-instance digest does not bind the case values for {key}")
        if row.get("deterministic_repeat") is not True:
            raise GrammarMatrixAuditError(f"Case lacks deterministic repeat proof: {key}")
        style_hashes_by_grammar[str(row["grammar_id"])].add(str(row["style_sha256"]))
    if seen != expected:
        raise GrammarMatrixAuditError("One or more expected grammar/seed cases are missing")
    if any(len(style_hashes_by_grammar[row["grammar_id"]]) < 2 for row in GRAMMAR_MATRIX):
        raise GrammarMatrixAuditError("Gameplay seed did not produce varying style evidence for every grammar")
    checks_expected = {
        "case_count": 20,
        "expected_case_count": 20,
        "all_five_grammar_indices_bound": True,
        "style_parameters_per_case": 20,
        "same_seed_repeat_deterministic": True,
        "gameplay_seed_variation_per_grammar": True,
        "profile_copy_only": True,
        "source_checks_passed": True,
    }
    if report.get("grammar_count") != 5 or report.get("seed_values") != list(SEEDS) or report.get("checks") != checks_expected:
        raise GrammarMatrixAuditError("Godot summary checks do not match the exact expected matrix")
    if report.get("execution_boundary") != BOUNDARY:
        raise GrammarMatrixAuditError("Godot report attempted to alter governance/execution boundary")
    try:
        Draft202012Validator(output_schema).validate(dict(report))
    except Exception as exc:
        raise GrammarMatrixAuditError(f"Godot report failed strict output schema: {getattr(exc, 'message', str(exc))}") from exc
    return dict(report)


def invoke_probe(root: Path, godot: str, timeout: int, process_runner: Callable[..., Any] = subprocess.run) -> tuple[dict[str, Any], str, str]:
    contract, _, input_schema, probe_schema, audit_schema, lineage = load_contract(root)
    probe_input = build_input(root, contract)
    encoded = base64.b64encode(_canonical(probe_input).encode("utf-8")).decode("ascii")
    command = [godot, "--headless", "--path", str(root), "--script", "res://" + HARNESS_REL.as_posix(), "--", encoded]
    try:
        completed = process_runner(command, cwd=str(root), text=True, capture_output=True, timeout=timeout, check=False)
    except Exception as exc:
        raise GrammarMatrixAuditError(f"Godot matrix probe invocation failed: {exc}") from exc
    stdout = str(getattr(completed, "stdout", "") or "")
    stderr = str(getattr(completed, "stderr", "") or "")
    combined = stdout + "\n" + stderr
    returncode = int(getattr(completed, "returncode", -1))
    if returncode != 0 or any(marker in combined for marker in ("SCRIPT ERROR:", "ERROR:", "GRAMMAR MATRIX V2 FAIL")):
        raise GrammarMatrixAuditError(f"Godot matrix probe failed (exit={returncode}): {combined[-5000:]}")
    rows = [line[len(PROBE_PREFIX):] for line in combined.splitlines() if line.startswith(PROBE_PREFIX)]
    if len(rows) != 1:
        raise GrammarMatrixAuditError(f"Expected exactly one Godot probe report; got {len(rows)}")
    try:
        parsed = json.loads(rows[0])
    except json.JSONDecodeError as exc:
        raise GrammarMatrixAuditError("Godot matrix report is not valid JSON") from exc
    if not isinstance(parsed, dict):
        raise GrammarMatrixAuditError("Godot matrix report root must be an object")
    report = validate_probe_report(parsed, probe_input, probe_schema)
    return report, stdout, stderr


def build_receipt(root: Path, contract: Mapping[str, Any], lineage: list[dict[str, str]], godot_version: str,
                  probe_report: Mapping[str, Any]) -> dict[str, Any]:
    cases = list(probe_report["cases"])
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA_ID,
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_NOT_CANONICAL_REQUEST_BINDING_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "contract_sha256": _sha_file(root / CONTRACT_REL),
        "godot_version": godot_version,
        "source_lineage_sha256": _sha_json(lineage),
        "source_pin_count": len(lineage),
        "godot_probe_sha256": _sha_json(dict(probe_report)),
        "scope": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "grammars": [dict(row) for row in GRAMMAR_MATRIX], "seed_values": list(SEEDS)},
        "matrix": {"grammars": 5, "seed_values_per_grammar": 4, "cases": len(cases), "expected_cases": 20, "style_parameters_per_case": 20, "deterministic_repeat_checks": 20, "distinct_seed_style_hashes_per_grammar_min": 2},
        "cases": cases,
        "findings": {
            "five_geometric_grammar_parameter_mappings_probed": True,
            "gameplay_seed_changes_style_per_grammar": True,
            "same_seed_repeats_deterministic": True,
            "frozen_c11c_sources_read_only": True,
            "canonical_request_chain_admitted": False,
            "canonical_selector_matrix_modified": False,
            "exact_selector_payload_materialized": False,
            "candidate_input_admissible": False,
            "video_render_ready": False,
        },
        "execution_boundary": dict(BOUNDARY),
    }
    receipt["audit_sha256"] = _sha_json(receipt)
    return receipt


def _validate_receipt(receipt: Mapping[str, Any], root: Path, audit_schema: Mapping[str, Any]) -> bool:
    expected_hash = _sha_json({k: v for k, v in receipt.items() if k != "audit_sha256"})
    if receipt.get("audit_sha256") != expected_hash:
        raise GrammarMatrixAuditError("Final audit SHA-256 does not match receipt content")
    if receipt.get("execution_boundary") != BOUNDARY:
        raise GrammarMatrixAuditError("Final receipt execution/governance boundary mismatch")
    if receipt.get("findings", {}).get("canonical_request_chain_admitted") is not False or receipt.get("findings", {}).get("exact_selector_payload_materialized") is not False:
        raise GrammarMatrixAuditError("Receipt overstated canonical request or payload admission")
    try:
        Draft202012Validator(audit_schema).validate(dict(receipt))
    except Exception as exc:
        raise GrammarMatrixAuditError(f"Final audit receipt failed strict schema: {getattr(exc, 'message', str(exc))}") from exc
    return True


def run_audit(godot: str, timeout: int = 120, project_root: str | Path | None = None,
              process_runner: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    root = _root(project_root)
    contract, _, _, _, audit_schema, lineage = load_contract(root)
    version_result = process_runner([godot, "--version"], cwd=str(root), text=True, capture_output=True, timeout=min(timeout, 30), check=False)
    version = (str(getattr(version_result, "stdout", "") or "") + str(getattr(version_result, "stderr", "") or "")).strip()
    if int(getattr(version_result, "returncode", -1)) != 0 or version != EXPECTED_GODOT_VERSION:
        raise GrammarMatrixAuditError(f"Expected exact Godot version {EXPECTED_GODOT_VERSION}, got {version!r}")
    probe, _, _ = invoke_probe(root, godot, timeout, process_runner)
    receipt = build_receipt(root, contract, lineage, version, probe)
    _validate_receipt(receipt, root, audit_schema)
    return receipt


def _resolve_godot(explicit: str | None) -> str | None:
    candidates = [explicit, os.environ.get("C11D_GODOT_EXECUTABLE")]
    for command in ("godot.exe", "godot"):
        found = shutil.which(command)
        if found:
            candidates.append(found)
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE", ""), help="Godot 4.7.1 executable path")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout for each Godot process, in seconds")
    parser.add_argument("--root", default=str(ROOT_DEFAULT), help="Repository root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    godot = _resolve_godot(args.godot)
    if not godot:
        print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 FAIL | Godot executable not found; pass --godot or set C11D_GODOT_EXECUTABLE | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 2
    if not root.is_dir() or not (root / "project.godot").is_file():
        print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 FAIL | project root lacks project.godot | renderer=OFF | media_created=false")
        return 2
    if args.timeout < 1 or args.timeout > 600:
        print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 FAIL | timeout must be 1..600 | renderer=OFF | media_created=false")
        return 2
    try:
        receipt = run_audit(godot, args.timeout, root, subprocess.run)
        print(RECEIPT_PREFIX + _canonical(receipt))
        print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 AUDIT PASS | grammars=5/5 | seed_cases=20/20 | style_parameters=20/20_per_case | deterministic_repeats=20/20 | source_pins=12/12 | canonical_request_admission=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 0
    except Exception as exc:
        print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 AUDIT FAIL | %s | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
