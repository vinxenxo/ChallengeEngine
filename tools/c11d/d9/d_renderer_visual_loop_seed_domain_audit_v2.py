"""Preparation-only seed-domain audit for the five exact-selector Geometric Waves V2 payloads.

Reuses the canonical D9.9 request planner, existing request-scoped parameter binder V2,
and exact-selector payload V2. It tests explicit seeds only and never admits renderer input.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

from jsonschema import Draft202012Validator

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_SCHEMA.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_REPORT_SCHEMA.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
IMPLEMENTATION_REL = Path("tools/c11d/d9/d_renderer_visual_loop_seed_domain_audit_v2.py")
EXPECTED_C11C = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT = "4.7.1.stable.mono.official.a13da4feb"

EXACT_RUNNER_REL = Path("tools/c11d/d9/d_renderer_visual_loop_exact_selector_payload_v2.py")
PARAMETER_RUNNER_REL = Path("tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py")
V1_BINDING_REL = Path("tools/c11d/d9/d_renderer_request_scoped_payload_binding.py")
MATRIX_RUNNER_REL = Path("tools/c11d/d9/d_renderer_visual_loop_request_scoped_binding_matrix_v2.py")
REFERENCE_CARRIER_REL = Path("tools/c11d/d9/d_renderer_visual_loop_timing_review_request_bound_reference_carrier.py")

GRAMMAR_MATRIX = (
    ("harmonic_membrane", 0, "field_harmonic_membrane"),
    ("interference_plane", 1, "field_interference_plane"),
    ("parametric_ribbon", 2, "field_parametric_ribbon"),
    ("lattice_wave", 3, "field_lattice_wave"),
    ("orbital_wave", 4, "field_orbital_wave"),
)
VARIANT_ROWS = (
    {"variant_id": "BASELINE", "gameplay_seed": 12345, "music_seed": 840001},
    {"variant_id": "GAMEPLAY_SEED_ONLY_CHANGED", "gameplay_seed": 54321, "music_seed": 840001},
    {"variant_id": "MUSIC_SEED_ONLY_CHANGED", "gameplay_seed": 12345, "music_seed": 840002},
)
REPEAT_COUNT = 2

BOUNDARY = {
    "request_input_persisted": False,
    "payload_file_written": False,
    "receipt_file_written": False,
    "renderer_instance_created": False,
    "shader_material_created": False,
    "shader_executed": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": False,
    "media_created": False,
    "c11c_source_mutation": False,
    "candidate_input_admissible": False,
    "renderer": "OFF",
    "D4.8": "BLOCKED",
    "D9.10": "PREPARE_ONLY",
    "D9.17": "BLOCKED_NO_GO",
    "D10": "BLOCKED",
    "release_authority": "NONE",
}

STATUS = "PREPARATION_ONLY_EXPLICIT_SEED_DOMAIN_V2_FOR_FIVE_GEOMETRIC_SELECTORS_NOT_INPUT_ADMISSION"
INPUT_SCHEMA_ID = "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-INPUT-V2"
PARENT_RECEIPT_SCHEMA = "C11-D-D9-VISUAL-LOOP-SEED-DOMAIN-VARIANT-PARENT-RECEIPT-V2"

class SeedDomainAuditError(ValueError):
    """The source-pinned seed audit failed closed."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def file_sha(path: Path) -> str:
    if not path.is_file():
        raise SeedDomainAuditError(f"Required pinned source is missing: {path}")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise SeedDomainAuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SeedDomainAuditError(f"Expected a JSON object at {path}")
    return value


def load_module(path: Path, name: str):
    if not path.is_file():
        raise SeedDomainAuditError(f"Required canonical parent implementation missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SeedDomainAuditError(f"Cannot load parent module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    parent = str(path.parent)
    if parent in sys.path:
        sys.path.remove(parent)
    sys.path.insert(0, parent)
    spec.loader.exec_module(module)
    return module


def _root(value: str | Path | None = None) -> Path:
    return Path(value).resolve() if value is not None else Path(__file__).resolve().parents[3]


def _validate_boundary(value: Any, label: str) -> None:
    if value != BOUNDARY:
        raise SeedDomainAuditError(f"{label} execution/governance boundary mismatch")


def _load_contract(root: Path):
    contract_path = root / CONTRACT_REL
    schema_path = root / CONTRACT_SCHEMA_REL
    report_schema_path = root / REPORT_SCHEMA_REL
    contract = read_json(contract_path)
    schema = read_json(schema_path)
    report_schema = read_json(report_schema_path)

    for name, candidate in (("contract", schema), ("report", report_schema)):
        if candidate.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or candidate.get("additionalProperties") is not False:
            raise SeedDomainAuditError(f"{name} schema must be strict JSON Schema Draft 2020-12")
        Draft202012Validator.check_schema(candidate)

    if file_sha(schema_path) != contract.get("contract_schema_sha256"):
        raise SeedDomainAuditError("Seed audit contract-schema hash mismatch")
    if file_sha(report_schema_path) != contract.get("report_schema_sha256"):
        raise SeedDomainAuditError("Seed audit report-schema hash mismatch")
    try:
        Draft202012Validator(schema).validate(contract)
    except Exception as exc:
        raise SeedDomainAuditError(f"Seed audit contract schema rejected contract: {getattr(exc, 'message', str(exc))}") from exc

    if contract.get("schema") != "C11-D-D9-VISUAL-LOOP-SEED-DOMAIN-AUDIT-CONTRACT-V2" or contract.get("schema_version") != "2.0":
        raise SeedDomainAuditError("Seed audit contract identity/version mismatch")
    if contract.get("status") != STATUS:
        raise SeedDomainAuditError("Seed audit contract attempted self-promotion")
    if file_sha(root / MANIFEST_REL) != EXPECTED_C11C or contract.get("authority", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_C11C:
        raise SeedDomainAuditError("Frozen C11-C manifest mismatch")
    _validate_boundary(contract.get("execution_boundary"), "Contract")

    implementation = contract.get("implementation", {})
    if implementation.get("path") != IMPLEMENTATION_REL.as_posix() or implementation.get("sha256") != file_sha(root / IMPLEMENTATION_REL):
        raise SeedDomainAuditError("Seed audit implementation path/hash mismatch")

    expected_approvals = {
        "explicit_seed_domain_audit_v2_approved": False,
        "seed_domains_complete_for_candidate_input": False,
        "automatic_seed_generation_approved": False,
        "master_seed_adopted": False,
        "canonical_v1_mutated": False,
        "exact_selector_payload_v2_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approvals:
        raise SeedDomainAuditError("Approval/admission lock changed in seed audit contract")

    if contract.get("scope", {}).get("grammar_matrix") != [
        {"grammar_id": g, "grammar_index": i, "shader_branch": b} for g, i, b in GRAMMAR_MATRIX
    ]:
        raise SeedDomainAuditError("Exact five-selector matrix/order changed")
    if contract.get("scope", {}).get("seed_variants") != list(VARIANT_ROWS) or contract.get("scope", {}).get("independent_repeats_per_variant") != REPEAT_COUNT:
        raise SeedDomainAuditError("Seed variants or repeat count differ from the approved bounded experiment")
    if contract.get("scope", {}).get("expected_seed_variant_count") != 15 or contract.get("scope", {}).get("expected_full_chain_repeat_count") != 30 or contract.get("scope", {}).get("expected_godot_probe_invocations") != 60:
        raise SeedDomainAuditError("Seed matrix coverage/invocation cardinality mismatch")

    lineage = contract.get("source_lineage")
    if not isinstance(lineage, list) or len(lineage) < 60 or lineage[0] != {"path": MANIFEST_REL.as_posix(), "sha256": EXPECTED_C11C}:
        raise SeedDomainAuditError("Seed audit source lineage must contain the frozen manifest first and the full accepted V2 source set")
    seen: set[str] = set()
    for index, row in enumerate(lineage):
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise SeedDomainAuditError("Malformed seed audit source-lineage row")
        rel, expected = row["path"], row["sha256"]
        path = Path(rel)
        if not isinstance(rel, str) or path.is_absolute() or ".." in path.parts or "\\" in rel or rel in seen:
            raise SeedDomainAuditError(f"Unsafe/duplicate seed audit source pin: {rel!r}")
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise SeedDomainAuditError(f"Malformed SHA-256 for source pin {rel}")
        actual = file_sha(root / rel)
        if actual != expected:
            raise SeedDomainAuditError(f"Pinned source drift: {rel}; expected={expected}; actual={actual}")
        seen.add(rel)

    # The exact-selector parent owns the authoritative lineage list; do not fork or reduce it.
    exact_mod = load_module(root / EXACT_RUNNER_REL, "_c11d_seed_audit_parent_exact_payload_v2")
    exact_contract, _exact_schema, exact_input_schema, _exact_report_schema, exact_pins = exact_mod._load_contract(root)
    if lineage != exact_pins:
        raise SeedDomainAuditError("Seed audit source lineage diverges from the accepted exact-selector V2 lineage")
    if exact_contract.get("status") != "PREPARATION_ONLY_IN_MEMORY_EXACT_SELECTOR_VISUAL_PAYLOADS_NOT_RENDERER_INPUT_NOT_APPROVED":
        raise SeedDomainAuditError("Exact-selector V2 parent status/governance changed")

    parameter_mod = load_module(root / PARAMETER_RUNNER_REL, "_c11d_seed_audit_parent_parameter_binding_v2")
    parameter_contract, _parameter_schema, parameter_input_schema, _parameter_report_schema, _parameter_pins = parameter_mod._load_contract(root)
    if parameter_contract.get("status") != "PREPARATION_ONLY_REQUEST_BOUND_GRAMMAR_PARAMETER_INSTANCES_5_OF_5_NOT_EXACT_VISUAL_PAYLOAD_NOT_APPROVED":
        raise SeedDomainAuditError("Request-scoped parameter binder V2 parent status changed")

    return contract, schema, report_schema, lineage, exact_mod, exact_contract, exact_input_schema, parameter_mod, parameter_contract, parameter_input_schema


def _build_canonical_variant_request(root: Path, grammar: str, gameplay_seed: int, music_seed: int):
    """Run the existing D9.9 planner/bridge/adapter for one explicit seed pair."""
    d9_dir = root / "tools/c11d/d9"
    if str(d9_dir) in sys.path:
        sys.path.remove(str(d9_dir))
    sys.path.insert(0, str(d9_dir))
    try:
        from universal_producer import evaluate_universal_request, REQUEST_SCHEMA_ID
        from editorial_render_bridge import build_bridge_planning_record
        from d_render_adapter import prepare_d_only_adapter_envelope
    except Exception as exc:
        raise SeedDomainAuditError(f"Cannot import canonical D9.9 request-chain services: {exc}") from exc

    request_id = "D-GRAMMAR-CHAIN-GAP-" + grammar.upper()
    raw = {
        "schema": REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": grammar, "variant_id": None},
        "seed": gameplay_seed,
        "music_seed": music_seed,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {"title": "Prueba editorial · título", "subtitle": "Subtítulo de revisión", "call_to_action": "Continuar", "language": "es"},
        "provenance": {"source_revision": "C11D-D9.9-DYNAMIC-REQUEST-V1", "request_origin": "TEST"},
    }
    result = evaluate_universal_request(raw, root)
    if result.get("status") != "PLANNED":
        raise SeedDomainAuditError(f"Canonical D9.9 request did not reach PLANNED for {grammar}/{gameplay_seed}/{music_seed}")
    canonical_request = result.get("canonical_request", {})
    selection = result.get("plan", {}).get("selection", {})
    expected_selection = {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": grammar, "variant_id": None}
    observed_selection = {key: selection.get(key) for key in expected_selection}
    if observed_selection != expected_selection:
        raise SeedDomainAuditError(f"Canonical planner changed selector for {grammar}: {observed_selection}")
    if canonical_request.get("request_id") != request_id or canonical_request.get("seed") != gameplay_seed or canonical_request.get("music_seed") != music_seed:
        raise SeedDomainAuditError(f"Canonical request lost request ID or explicit seed pair for {grammar}")
    bridge = build_bridge_planning_record(result, root)
    envelope = prepare_d_only_adapter_envelope(result, bridge, root)
    if not isinstance(bridge.get("record_hash"), str) or not isinstance(envelope.get("envelope_hash"), str):
        raise SeedDomainAuditError(f"Canonical bridge/adapter did not provide their stable identity hashes for {grammar}")
    return result, bridge, envelope


def _build_seeded_chain(root: Path, grammar: str, gameplay_seed: int, music_seed: int, carrier_report: Mapping[str, Any], parameter_mod):
    result, bridge, envelope = _build_canonical_variant_request(root, grammar, gameplay_seed, music_seed)
    request = result["canonical_request"]
    selection = result["plan"]["selection"]

    relation = next((item for item in carrier_report.get("relations", []) if item.get("selector", {}).get("grammar_id") == grammar), None)
    if not isinstance(relation, Mapping):
        raise SeedDomainAuditError(f"Selector metadata reference missing for {grammar}")
    ref = relation.get("reference_identity", {})
    locks = relation.get("locks", {})
    if (ref.get("reference_count") != 9 or ref.get("source_envelope_request_bound") is not False or
            locks.get("policy_values_consumed") is not False or locks.get("candidate_input_admissible") is not False):
        raise SeedDomainAuditError(f"Selector policy reference is not metadata-only for {grammar}")

    # Reuse the existing V1 source-binding core in memory with the same narrow geometric-family mapping.
    binder = load_module(root / V1_BINDING_REL, "_c11d_seed_audit_existing_v1_binding_core")
    v1_contract, v1_schema, v1_lineage = binder._load_contract(root)
    extended = copy.deepcopy(v1_contract)
    extended["representative_source_matrix"]["visual_loops"] = {
        "required_selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1"},
        "payload_source_path": "definitions/visual_loop_geometric_canonical.json",
    }
    source_binding = binder._build_core(result, bridge, envelope, root, extended, v1_schema, v1_lineage, False)
    readiness = source_binding.get("readiness", {})
    if readiness.get("request_scoped_visual_payload_instance_bound") is not False or readiness.get("video_render_ready") is not False:
        raise SeedDomainAuditError(f"Existing V1 core escalated readiness for {grammar}")

    request_input = {
        "schema": "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1",
        "schema_version": "1.0",
        "request_id": request["request_id"],
        "request_hash": result["request_hash"],
        "selection": {
            "content_type": selection["content_type"],
            "family_id": selection["family_id"],
            "subtype_id": selection["subtype_id"],
            "variant_id": selection.get("variant_id"),
        },
        "seed": request["seed"],
        "music_seed": request["music_seed"],
        "variation_index": request["variation_index"],
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
    }
    canonical_chain = {
        "plan_hash": result["plan_hash"],
        "editorial_hash": result["editorial_hash"],
        "bridge_record_hash": bridge["record_hash"],
        "adapter_envelope_hash": envelope["envelope_hash"],
        "source_binding_sha256": source_binding["binding_sha256"],
    }
    timing_reference = {
        "carrier_report_sha256": carrier_report["report_sha256"],
        "selector_envelope_sha256": ref["selector_envelope_sha256"],
        "shared_policy_reference_set_sha256": ref["shared_reference_set_sha256"],
        "policy_reference_count": int(ref["reference_count"]),
        "policy_values_consumed": False,
    }
    request_identity = {
        "request_id": request["request_id"],
        "request_hash": result["request_hash"],
        "selection": request_input["selection"],
        "gameplay_seed": int(request["seed"]),
        "music_seed": int(request["music_seed"]),
        "variation_index": int(request["variation_index"]),
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
    }
    return result, request_input, canonical_chain, timing_reference, request_identity


def _variant_parent_receipt(root: Path, case_receipt: Mapping[str, Any], variant_id: str, lineage: list[dict[str, str]]) -> dict[str, Any]:
    body = {
        "schema": PARENT_RECEIPT_SCHEMA,
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_SINGLE_REQUEST_PARAMETER_BINDING_RECEIPT_NOT_INPUT_ADMISSION",
        "frozen_c11c_manifest_sha256": EXPECTED_C11C,
        "seed_variant_id": variant_id,
        "request_identity": copy.deepcopy(case_receipt["request_identity"]),
        "canonical_chain": copy.deepcopy(case_receipt["canonical_chain"]),
        "timing_review_reference": copy.deepcopy(case_receipt["timing_review_reference"]),
        "request_parameter_binding_sha256": case_receipt["request_parameter_binding_sha256"],
        "parameter_instance_sha256": case_receipt["parameter_instance"]["parameter_instance_sha256"],
        "style_parameters_sha256": case_receipt["parameter_instance"]["style_parameters_sha256"],
        "source_lineage_sha256": digest(lineage),
        "readiness": {"exact_selector_visual_payload_materialized": False, "candidate_input_admissible": False, "video_render_ready": False},
        "governance": {"renderer": "OFF", "media_created": False, "D4.8": "BLOCKED", "release_authority": "NONE"},
    }
    parent_sha = digest(body)
    return {**body, "report_sha256": parent_sha}


def _build_one(root: Path, godot: str, timeout: float, contract: Mapping[str, Any], lineage: list[dict[str, str]],
               exact_mod, exact_contract: Mapping[str, Any], exact_input_schema: Mapping[str, Any],
               parameter_mod, parameter_contract: Mapping[str, Any], parameter_input_schema: Mapping[str, Any],
               carrier_report: Mapping[str, Any], grammar: str, variant: Mapping[str, Any], process_runner: Callable[..., Any]) -> dict[str, Any]:
    result, request_input, chain, timing_reference, request_identity = _build_seeded_chain(
        root, grammar, int(variant["gameplay_seed"]), int(variant["music_seed"]), carrier_report, parameter_mod
    )
    parent_parameter_probe = parameter_mod._run_one(
        root, godot, timeout, parameter_contract, parameter_input_schema,
        request_input, chain, timing_reference, process_runner,
    )
    case_receipt = parameter_mod._case_receipt(parent_parameter_probe, chain, timing_reference)
    if case_receipt.get("request_identity") != request_identity:
        raise SeedDomainAuditError(f"Parent parameter receipt identity mismatch for {grammar}/{variant['variant_id']}")

    parent_record = _variant_parent_receipt(root, case_receipt, str(variant["variant_id"]), lineage)
    probe_input = {
        "schema": INPUT_SCHEMA_ID,
        "schema_version": "2.0",
        "contract_sha256": file_sha(root / exact_mod.CONTRACT_REL),
        "frozen_c11c_manifest_sha256": EXPECTED_C11C,
        "parent_binding_report_sha256": parent_record["report_sha256"],
        "request_identity": request_identity,
        "canonical_chain": chain,
        "timing_review_reference": timing_reference,
        "request_parameter_binding_sha256": case_receipt["request_parameter_binding_sha256"],
        "parameter_instance": copy.deepcopy(case_receipt["parameter_instance"]),
    }
    payload_probe = exact_mod._run_probe(root, godot, timeout, exact_contract, exact_input_schema, probe_input, process_runner)
    if payload_probe.get("parent_request_parameter_binding_sha256") != case_receipt["request_parameter_binding_sha256"]:
        raise SeedDomainAuditError(f"Exact payload detached from request parameter binding for {grammar}/{variant['variant_id']}")
    if payload_probe.get("request_identity") != request_identity or payload_probe.get("canonical_chain") != chain:
        raise SeedDomainAuditError(f"Exact payload detached from canonical request chain for {grammar}/{variant['variant_id']}")

    return {
        "grammar_id": grammar,
        "variant_id": variant["variant_id"],
        "repeat_index": 1,
        "gameplay_seed": int(variant["gameplay_seed"]),
        "music_seed": int(variant["music_seed"]),
        "request_id": request_identity["request_id"],
        "request_hash": request_identity["request_hash"],
        "plan_hash": chain["plan_hash"],
        "editorial_hash": chain["editorial_hash"],
        "bridge_record_hash": chain["bridge_record_hash"],
        "adapter_envelope_hash": chain["adapter_envelope_hash"],
        "source_binding_sha256": chain["source_binding_sha256"],
        "request_parameter_binding_sha256": case_receipt["request_parameter_binding_sha256"],
        "style_parameters_sha256": case_receipt["parameter_instance"]["style_parameters_sha256"],
        "parameter_instance_sha256": case_receipt["parameter_instance"]["parameter_instance_sha256"],
        "parent_binding_receipt_sha256": parent_record["report_sha256"],
        "authoring_envelope_sha256": payload_probe["authoring_envelope_sha256"],
        "family_variation_recipe_sha256": payload_probe["family_variation_recipe_sha256"],
        "resolved_palette_sha256": payload_probe["resolved_palette_sha256"],
        "visual_spec_sha256": payload_probe["visual_spec_sha256"],
        "payload_instance_sha256": payload_probe["payload_instance_sha256"],
        "selector_policy_envelope_sha256": timing_reference["selector_envelope_sha256"],
        "shared_policy_reference_set_sha256": timing_reference["shared_policy_reference_set_sha256"],
        "policy_reference_count": timing_reference["policy_reference_count"],
        "policy_values_consumed": False,
        "source_pins_verified": True,
        "canonical_request_planned": result.get("status") == "PLANNED",
        "parameter_instance_bound_in_memory": True,
        "exact_selector_payload_materialized_in_memory": payload_probe.get("exact_selector_visual_payload_materialized") is True,
        "deterministic_repeat_pass": payload_probe.get("deterministic_repeat_pass") is True,
        "renderer_input_emitted": False,
        "payload_file_written": False,
        "candidate_input_admissible": False,
        "renderer": "OFF",
        "media_created": False,
        "D4.8": "BLOCKED",
        "release_authority": "NONE",
    }


def _repeat_projection(case: Mapping[str, Any]) -> dict[str, Any]:
    fields = (
        "grammar_id", "variant_id", "gameplay_seed", "music_seed", "request_id", "request_hash", "plan_hash",
        "editorial_hash", "bridge_record_hash", "adapter_envelope_hash", "source_binding_sha256",
        "request_parameter_binding_sha256", "style_parameters_sha256", "parameter_instance_sha256",
        "parent_binding_receipt_sha256", "authoring_envelope_sha256", "family_variation_recipe_sha256",
        "resolved_palette_sha256", "visual_spec_sha256", "payload_instance_sha256",
        "selector_policy_envelope_sha256", "shared_policy_reference_set_sha256", "policy_reference_count",
        "policy_values_consumed", "source_pins_verified", "canonical_request_planned",
        "parameter_instance_bound_in_memory", "exact_selector_payload_materialized_in_memory",
        "deterministic_repeat_pass", "renderer_input_emitted", "payload_file_written", "candidate_input_admissible",
        "renderer", "media_created", "D4.8", "release_authority",
    )
    return {key: case.get(key) for key in fields}


def evaluate_seed_domain_relationships(cases: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Pure, strict comparison of the full seed matrix; no process or filesystem access."""
    if not isinstance(cases, list) or len(cases) != 30:
        raise SeedDomainAuditError("Seed matrix must contain exactly 30 independent full-chain receipts")
    grammar_ids = [row[0] for row in GRAMMAR_MATRIX]
    variant_ids = [str(row["variant_id"]) for row in VARIANT_ROWS]
    matrix: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for case in cases:
        if not isinstance(case, Mapping):
            raise SeedDomainAuditError("Seed matrix receipt must be an object")
        grammar, variant_id = case.get("grammar_id"), case.get("variant_id")
        if grammar not in grammar_ids or variant_id not in variant_ids:
            raise SeedDomainAuditError("Unknown selector or seed variant in runtime evidence")
        key = (str(grammar), str(variant_id))
        matrix.setdefault(key, []).append(case)
    if len(matrix) != 15 or any(len(rows) != REPEAT_COUNT for rows in matrix.values()):
        raise SeedDomainAuditError("Each of the 15 selector/seed variants must have two independent full-chain receipts")

    expected_seeds = {row["variant_id"]: (row["gameplay_seed"], row["music_seed"]) for row in VARIANT_ROWS}
    repeat_pairs = 0
    by_grammar: dict[str, dict[str, Mapping[str, Any]]] = {}
    for grammar in grammar_ids:
        by_grammar[grammar] = {}
        for variant_id in variant_ids:
            rows = sorted(matrix[(grammar, variant_id)], key=lambda row: int(row.get("repeat_index", -1)))
            if [row.get("repeat_index") for row in rows] != [1, 2]:
                raise SeedDomainAuditError(f"Repeat indices must be 1,2 for {grammar}/{variant_id}")
            expected_gameplay, expected_music = expected_seeds[variant_id]
            for row in rows:
                if (row.get("gameplay_seed"), row.get("music_seed")) != (expected_gameplay, expected_music):
                    raise SeedDomainAuditError(f"Seed values drifted in {grammar}/{variant_id}")
                if row.get("canonical_request_planned") is not True or row.get("source_pins_verified") is not True:
                    raise SeedDomainAuditError(f"Canonical request/source-pin evidence missing for {grammar}/{variant_id}")
                if row.get("parameter_instance_bound_in_memory") is not True or row.get("exact_selector_payload_materialized_in_memory") is not True:
                    raise SeedDomainAuditError(f"Full request-bound payload chain not proven for {grammar}/{variant_id}")
                if row.get("deterministic_repeat_pass") is not True or row.get("policy_values_consumed") is not False:
                    raise SeedDomainAuditError(f"Repeat determinism or metadata-only policy boundary failed for {grammar}/{variant_id}")
                if row.get("renderer_input_emitted") is not False or row.get("payload_file_written") is not False or row.get("candidate_input_admissible") is not False:
                    raise SeedDomainAuditError(f"Seed audit crossed the preparation-only boundary for {grammar}/{variant_id}")
                if row.get("renderer") != "OFF" or row.get("media_created") is not False or row.get("D4.8") != "BLOCKED" or row.get("release_authority") != "NONE":
                    raise SeedDomainAuditError(f"Governance lock changed for {grammar}/{variant_id}")
                for key in ("request_hash", "plan_hash", "request_parameter_binding_sha256", "style_parameters_sha256", "parameter_instance_sha256", "parent_binding_receipt_sha256", "authoring_envelope_sha256", "family_variation_recipe_sha256", "resolved_palette_sha256", "visual_spec_sha256", "payload_instance_sha256", "selector_policy_envelope_sha256", "shared_policy_reference_set_sha256"):
                    if not isinstance(row.get(key), str) or re.fullmatch(r"[0-9a-f]{64}", row[key]) is None:
                        raise SeedDomainAuditError(f"Malformed {key} for {grammar}/{variant_id}")
                if row.get("policy_reference_count") != 9:
                    raise SeedDomainAuditError(f"Policy reference count changed for {grammar}/{variant_id}")
            if _repeat_projection(rows[0]) != _repeat_projection(rows[1]):
                raise SeedDomainAuditError(f"Independent full-chain repeats drifted for {grammar}/{variant_id}")
            by_grammar[grammar][variant_id] = rows[0]
            repeat_pairs += 1

    request_hashes = [case["request_hash"] for case in by_grammar.values() for case in case.values()]
    plan_hashes = [case["plan_hash"] for case in by_grammar.values() for case in case.values()]
    parameter_hashes = [case["parameter_instance_sha256"] for case in by_grammar.values() for case in case.values()]
    payload_hashes = [case["payload_instance_sha256"] for case in by_grammar.values() for case in case.values()]
    if any(len(set(values)) != 15 for values in (request_hashes, plan_hashes, parameter_hashes, payload_hashes)):
        raise SeedDomainAuditError("Each selector/seed variant must have unique request, plan, parameter and full payload identity")

    gameplay_checks = 0
    music_checks = 0
    for grammar in grammar_ids:
        baseline = by_grammar[grammar]["BASELINE"]
        gameplay = by_grammar[grammar]["GAMEPLAY_SEED_ONLY_CHANGED"]
        music = by_grammar[grammar]["MUSIC_SEED_ONLY_CHANGED"]

        if baseline["request_hash"] == gameplay["request_hash"] or baseline["plan_hash"] == gameplay["plan_hash"]:
            raise SeedDomainAuditError(f"Gameplay seed mutation failed to change canonical request/plan identity: {grammar}")
        for field in ("style_parameters_sha256", "family_variation_recipe_sha256", "resolved_palette_sha256", "visual_spec_sha256", "payload_instance_sha256"):
            if baseline[field] == gameplay[field]:
                raise SeedDomainAuditError(f"Gameplay seed mutation did not change {field}: {grammar}")
        gameplay_checks += 1

        if baseline["request_hash"] == music["request_hash"] or baseline["plan_hash"] == music["plan_hash"]:
            raise SeedDomainAuditError(f"Music seed mutation failed to change canonical request/plan identity: {grammar}")
        if baseline["request_parameter_binding_sha256"] == music["request_parameter_binding_sha256"] or baseline["parameter_instance_sha256"] == music["parameter_instance_sha256"] or baseline["payload_instance_sha256"] == music["payload_instance_sha256"]:
            raise SeedDomainAuditError(f"Music seed mutation failed to change request-bound identity: {grammar}")
        for field in ("style_parameters_sha256", "authoring_envelope_sha256", "family_variation_recipe_sha256", "resolved_palette_sha256", "visual_spec_sha256"):
            if baseline[field] != music[field]:
                raise SeedDomainAuditError(f"Music seed leaked into visual content field {field}: {grammar}")
        music_checks += 1

    distinct_policy_sets = {case["shared_policy_reference_set_sha256"] for case in by_grammar.values() for case in case.values()}
    if len(distinct_policy_sets) != 1:
        raise SeedDomainAuditError("Shared metadata-only policy reference set changed across explicit seed variants")

    return {
        "selectors": "5/5",
        "seed_variant_chains": "15/15",
        "independent_repeat_pairs": f"{repeat_pairs}/15",
        "request_hash_variants": "15/15",
        "plan_hash_variants": "15/15",
        "parameter_instance_hash_variants": "15/15",
        "full_payload_hash_variants": "15/15",
        "gameplay_seed_sensitivity": f"{gameplay_checks}/5",
        "music_seed_orthogonality": f"{music_checks}/5",
        "seed_variant_policy_reference_pairs": "135/135",
        "policy_values_consumed": False,
        "runtime_parameter_binding_invocations": 30,
        "runtime_exact_payload_invocations": 30,
        "runtime_invocations": 60,
        "candidate_input_admissible": False,
        "automatic_seed_generation": False,
        "master_seed_adopted": False,
        "seed_domains_complete_for_candidate_input": False,
    }


def build_report(project_root: str | Path | None = None, godot: str | None = None, timeout: float = 120,
                 process_runner: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    root = _root(project_root)
    if not godot or not Path(godot).is_file():
        raise SeedDomainAuditError("An explicit Godot 4.7.1 console executable path is required")

    contract, _schema, report_schema, lineage, exact_mod, exact_contract, exact_input_schema, parameter_mod, parameter_contract, parameter_input_schema = _load_contract(root)
    try:
        version = process_runner([godot, "--version"], cwd=str(root), text=True, capture_output=True, timeout=min(timeout, 30), check=False)
    except Exception as exc:
        raise SeedDomainAuditError(f"Cannot invoke Godot console executable: {exc}") from exc
    version_text = (str(getattr(version, "stdout", "") or "") + "\n" + str(getattr(version, "stderr", "") or "").strip()).strip()
    if int(getattr(version, "returncode", -1)) != 0 or EXPECTED_GODOT not in version_text:
        raise SeedDomainAuditError(f"Expected Godot {EXPECTED_GODOT}; actual version output: {version_text!r}")

    carrier_mod = load_module(root / REFERENCE_CARRIER_REL, "_c11d_seed_audit_request_bound_reference_carrier")
    carrier_report = carrier_mod.build_report(root)
    carrier_summary = carrier_report.get("summary", {})
    if (carrier_summary.get("request_identity_joins") != "5/5" or carrier_summary.get("policy_reference_pairs") != "45/45" or
            carrier_summary.get("approvals_granted") != 0 or carrier_summary.get("candidate_input_admissible") is not False):
        raise SeedDomainAuditError("Canonical reference carrier is not in its fixed metadata-only state")
    if digest({key: value for key, value in carrier_report.items() if key != "report_sha256"}) != carrier_report.get("report_sha256"):
        raise SeedDomainAuditError("Request/reference carrier report self-hash mismatch")

    cases: list[dict[str, Any]] = []
    for grammar, _index, _branch in GRAMMAR_MATRIX:
        for variant in VARIANT_ROWS:
            repeats: list[dict[str, Any]] = []
            for repeat_index in (1, 2):
                record = _build_one(
                    root, godot, timeout, contract, lineage, exact_mod, exact_contract,
                    exact_input_schema, parameter_mod, parameter_contract,
                    parameter_input_schema, carrier_report, grammar, variant, process_runner,
                )
                record["repeat_index"] = repeat_index
                repeats.append(record)
            if _repeat_projection(repeats[0]) != _repeat_projection(repeats[1]):
                raise SeedDomainAuditError(f"Independent request/parameter/payload process repeats drifted for {grammar}/{variant['variant_id']}")
            cases.extend(repeats)

    summary = evaluate_seed_domain_relationships(cases)
    report = {
        "schema": "C11-D-D9-VISUAL-LOOP-SEED-DOMAIN-AUDIT-REPORT-V2",
        "schema_version": "2.0",
        "status": STATUS,
        "contract_sha256": file_sha(root / CONTRACT_REL),
        "contract_schema_sha256": file_sha(root / CONTRACT_SCHEMA_REL),
        "report_schema_sha256": file_sha(root / REPORT_SCHEMA_REL),
        "implementation_sha256": file_sha(root / IMPLEMENTATION_REL),
        "source_lineage": lineage,
        "source_lineage_sha256": digest(lineage),
        "reference_carrier_report_sha256": carrier_report["report_sha256"],
        "godot_version": EXPECTED_GODOT,
        "cases": cases,
        "summary": summary,
        "governance": {
            "approval_assertions_checked": 19,
            "approvals_granted": 0,
            "explicit_seed_domain_audit_v2_approved": False,
            "seed_domains_complete_for_candidate_input": False,
            "automatic_seed_generation": False,
            "master_seed_adopted": False,
            "canonical_v1_mutated": False,
            "exact_selector_payload_v2_approved": False,
            "candidate_io_contract_complete": False,
            "renderer_baseline_approved": False,
            "renderer_baseline_frozen": False,
            "d4_8_authorized": False,
            "request_input_persisted": False,
            "payload_file_written": False,
            "receipt_file_written": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "shader_executed": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "candidate_input_admissible": False,
            "renderer": "OFF",
            "D4.8": "BLOCKED",
            "D9.10": "PREPARE_ONLY",
            "D9.17": "BLOCKED_NO_GO",
            "D10": "BLOCKED",
            "release_authority": "NONE",
        },
        "execution_boundary": dict(BOUNDARY),
    }
    report["report_sha256"] = digest(report)
    try:
        Draft202012Validator(report_schema).validate(report)
    except Exception as exc:
        raise SeedDomainAuditError(f"Seed audit report schema rejected report: {getattr(exc, 'message', str(exc))}") from exc
    if digest({key: value for key, value in report.items() if key != "report_sha256"}) != report["report_sha256"]:
        raise SeedDomainAuditError("Seed audit report self-hash mismatch")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--godot", required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--full-report", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = build_report(args.root, args.godot, args.timeout)
        s = report["summary"]
        print(
            "C11-D VISUAL LOOP SEED DOMAIN AUDIT V2 PASS | selectors=" + s["selectors"] +
            " | seed_variant_chains=" + s["seed_variant_chains"] +
            " | independent_repeat_pairs=" + s["independent_repeat_pairs"] +
            " | request_hash_variants=" + s["request_hash_variants"] +
            " | plan_hash_variants=" + s["plan_hash_variants"] +
            " | parameter_instance_hash_variants=" + s["parameter_instance_hash_variants"] +
            " | full_payload_hash_variants=" + s["full_payload_hash_variants"] +
            " | gameplay_seed_sensitivity=" + s["gameplay_seed_sensitivity"] +
            " | music_seed_orthogonality=" + s["music_seed_orthogonality"] +
            " | seed_variant_policy_reference_pairs=" + s["seed_variant_policy_reference_pairs"] +
            " | policy_values_consumed=false | runtime_parameter_binding_invocations=30 | runtime_exact_payload_invocations=30 | runtime_invocations=60" +
            " | automatic_seed_generation=false | master_seed_adopted=false | seed_domains_complete_for_candidate_input=false" +
            " | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
        )
        print("C11D_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_REPORT=" + canonical(report))
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print("C11-D VISUAL LOOP SEED DOMAIN AUDIT V2 FAIL | " + str(exc) + " | seed_domains_complete_for_candidate_input=false | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
