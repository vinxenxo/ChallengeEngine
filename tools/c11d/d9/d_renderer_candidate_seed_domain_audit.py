from __future__ import annotations

"""Read-only cross-type seed-domain audit for pinned Challenge and Visual Loop selectors."""
from collections.abc import Callable, Mapping
from copy import deepcopy
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402
import d_renderer_visual_drill_seed_domain_audit as drill_audit  # noqa: E402

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_SCHEMA_V1.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_CONTRACT_SHA256 = "e51be5340d26896f28fc94ae33416a1c93fbbcd5dd27916b661edbebd7616d69"
EXPECTED_SCHEMA_SHA256 = "ba22ca15028c82bfafdaca4f4d10f08d4e554405f9869247bb2d32e28922575c"
CONTRACT_ID = "C11-D-RENDERER-CANDIDATE-SEED-DOMAIN-AUDIT-V1"
SCHEMA_ID = "urn:c11d:renderer-candidate-seed-domain-audit:v1"
STATUS = "PREPARATION_ONLY_CROSS_TYPE_SEED_DOMAIN_AUDIT_NOT_INPUT_ADMISSION"
SEED_BASE = 12345
SEED_CHANGED = 54321
MUSIC_SEED_BASE = 840001
MUSIC_SEED_CHANGED = 840002
VARIANTS = ("BASELINE", "GAMEPLAY_SEED_ONLY_CHANGED", "MUSIC_SEED_ONLY_CHANGED")
CONTENT_TYPES = ("challenges", "visual_loops")
VARIANT_SEEDS = {
    "BASELINE": (SEED_BASE, MUSIC_SEED_BASE),
    "GAMEPLAY_SEED_ONLY_CHANGED": (SEED_CHANGED, MUSIC_SEED_BASE),
    "MUSIC_SEED_ONLY_CHANGED": (SEED_BASE, MUSIC_SEED_CHANGED),
}
EXPECTED_SELECTOR_SCOPE = {
    "challenges": {
        "selection": {"content_type": "challenges", "family_id": "parking_v2", "subtype_id": None, "variant_id": "CHALLENGE_004"},
        "payload_scope": "CHALLENGE_RUNTIME_VISUAL_PAYLOAD_SOURCE_TIMEBASE",
    },
    "visual_loops": {
        "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane", "variant_id": None},
        "payload_scope": "VISUAL_LOOP_SELECTOR_PAYLOAD_HARMONIC_MEMBRANE_V1",
    },
}
# This audit composes with (but does not alter) the accepted V1/V2 binders.
PIN_ROLES = {
    "challenges/CHALLENGE_004.json": "PINNED_CHALLENGE_DEFINITION",
    "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_SCHEMA_V1.json": "V1_BINDING_OUTPUT_SCHEMA",
    "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json": "V1_BINDING_CONTRACT",
    "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_INPUT_SCHEMA_V1.json": "V1_BINDING_INPUT_SCHEMA",
    "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json": "ACCEPTED_VISUAL_DRILL_V2_CONTRACT",
    "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_SCHEMA_V1.json": "ACCEPTED_VISUAL_DRILL_SEED_AUDIT_SCHEMA",
    "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_V1.json": "ACCEPTED_VISUAL_DRILL_SEED_AUDIT_CONTRACT",
    "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_BINDING_AUDIT_V1.json": "PINNED_LOOP_GRAMMAR_AUDIT_CONTRACT",
    "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INSTANCE_V1.json": "PINNED_LOOP_PARAMETER_INSTANCE_CONTRACT",
    "definitions/visual_loop_geometric_canonical.json": "PINNED_LOOP_CANONICAL_DEFINITION",
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "IMMUTABLE_C11C_MANIFEST",
    "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py": "CANONICAL_V1_BINDER_IMPLEMENTATION",
    "tools/c11d/d9/d_renderer_visual_drill_seed_domain_audit.py": "ACCEPTED_VISUAL_DRILL_SEED_AUDIT_RUNNER",
    "tools/c11d/d9/materialize_dynamic_request_payload_in_memory.gd": "CANONICAL_V1_GODOT_HARNESS",
    "tools/c11d/d9/materialize_visual_drill_dynamic_request_payload_in_memory_v2.gd": "ACCEPTED_VISUAL_DRILL_V2_GODOT_HARNESS",
    "tools/c11d/d9/test_d_renderer_dynamic_request_payload_binding.py": "CANONICAL_V1_BINDER_REGRESSION",
    "tools/c11d/d9/test_d_renderer_dynamic_request_payload_binding_visual_drill_v2.py": "ACCEPTED_VISUAL_DRILL_V2_REGRESSION",
    "tools/c11d/d9/test_d_renderer_visual_drill_seed_domain_audit.py": "ACCEPTED_VISUAL_DRILL_SEED_AUDIT_REGRESSION",
}
PINNED_PATHS = tuple(sorted(PIN_ROLES))
IDENTITY_FIELDS = ("request_id", "content_type", "selection", "variation_index", "presentation_profile_id", "delivery_profile_id")
REPEAT_FIELDS = ("request_hash", "request_binding_sha256", "payload_sha256", "visual_state_sha256", "grammar_parameter_evidence")
GOVERNANCE_BOUNDARY = {
    "runtime": "GODOT_HEADLESS_IN_MEMORY_CROSS_TYPE_AUDIT_ONLY",
    "request_input_persisted": False,
    "payload_files_written": False,
    "receipt_files_written": False,
    "renderer_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": False,
    "production_execution": False,
    "media_created": False,
    "output_artifact_path": None,
    "c11c_source_mutation": False,
    "d4_8": "BLOCKED",
    "release_authority": "NONE",
}


class SeedDomainAuditError(RuntimeError):
    """The cross-type seed audit is stale, incomplete, non-orthogonal, or unsafe."""


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _sha_json(value: Any) -> str:
    return _sha_bytes(_canonical(value).encode("utf-8"))


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SeedDomainAuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SeedDomainAuditError(f"Expected JSON object at {path}")
    return value


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT


def _load_and_validate_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract_path = root / CONTRACT_REL
    schema_path = root / SCHEMA_REL
    if not contract_path.is_file() or _sha_file(contract_path) != EXPECTED_CONTRACT_SHA256:
        raise SeedDomainAuditError("Cross-type seed audit contract missing or SHA-256 mismatch")
    if not schema_path.is_file() or _sha_file(schema_path) != EXPECTED_SCHEMA_SHA256:
        raise SeedDomainAuditError("Cross-type seed audit report schema missing or SHA-256 mismatch")
    contract = _read_json(contract_path)
    schema = _read_json(schema_path)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise SeedDomainAuditError("Cross-type seed audit contract identity/version mismatch")
    if contract.get("status") != "READ_ONLY_SOURCE_PINNED_CHALLENGE_VISUAL_LOOP_SEED_AUDIT_NOT_INPUT_ADMISSION":
        raise SeedDomainAuditError("Cross-type seed audit is not in read-only review status")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise SeedDomainAuditError("Frozen C11-C reference mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != SCHEMA_ID or schema.get("additionalProperties") is not False:
        raise SeedDomainAuditError("Cross-type report schema identity/strictness mismatch")
    expected_experiment = {
        "content_types": list(CONTENT_TYPES),
        "selectors": EXPECTED_SELECTOR_SCOPE,
        "baseline_gameplay_seed": SEED_BASE,
        "changed_gameplay_seed": SEED_CHANGED,
        "baseline_music_seed": MUSIC_SEED_BASE,
        "changed_music_seed": MUSIC_SEED_CHANGED,
        "variants": {k: {"gameplay_seed": v[0], "music_seed": v[1]} for k, v in VARIANT_SEEDS.items()},
        "identity_fields_held_constant": list(IDENTITY_FIELDS),
        "gameplay_seed_change_must_change": ["request_binding_sha256", "payload_sha256", "visual_state_sha256"],
        "music_seed_change_must_preserve": ["payload_sha256", "visual_state_sha256", "grammar_parameter_evidence"],
        "music_seed_change_must_change": ["request_binding_sha256"],
        "repeat_must_preserve": list(REPEAT_FIELDS),
        "independent_runtime_executions_per_variant": 2,
        "expected_runtime_invocations": 12,
        "receipt_mode": "CANONICAL_V1_REQUEST_SCOPED_RECEIPTS_WITH_SEPARATE_INDEPENDENT_PROCESS_REPEATS",
    }
    if contract.get("experiment") != expected_experiment:
        raise SeedDomainAuditError("Cross-type seed experiment contract changed without runner review")
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) != contract.get("source_pin_count"):
        raise SeedDomainAuditError("Cross-type source pin count/shape mismatch")
    if len(pins) != len(PINNED_PATHS):
        raise SeedDomainAuditError(f"Cross-type source pin count must be {len(PINNED_PATHS)}")
    verified: list[dict[str, str]] = []
    seen: list[str] = []
    for row in pins:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "role"}:
            raise SeedDomainAuditError("Malformed cross-type source pin row")
        rel, expected = row.get("path"), row.get("sha256")
        if not isinstance(rel, str) or rel not in PIN_ROLES:
            raise SeedDomainAuditError(f"Unapproved source pin path: {rel!r}")
        if row.get("role") != PIN_ROLES[rel]:
            raise SeedDomainAuditError(f"Source pin role mismatch: {rel}")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise SeedDomainAuditError(f"Malformed source digest for {rel}")
        if not (root / rel).is_file() or _sha_file(root / rel) != expected:
            raise SeedDomainAuditError(f"Source pin mismatch: {rel}")
        verified.append({"path": rel, "sha256": expected, "role": row["role"]})
        seen.append(rel)
    if seen != list(PINNED_PATHS):
        raise SeedDomainAuditError("Cross-type source pins must be unique, sorted and complete")
    if _sha_file(root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json") != EXPECTED_MANIFEST_SHA256:
        raise SeedDomainAuditError("Frozen C11-C manifest SHA-256 mismatch")
    # Re-run both canonical binders' source-closure checks; this audit never substitutes for them.
    binder._load_contract(root)
    drill_contract, _, _ = drill_audit._load_and_validate_contract(root)
    if drill_contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise SeedDomainAuditError("Accepted Visual Drill V2 seed audit reference drifted")
    for content_type in CONTENT_TYPES:
        if binder.EXPECTED_SELECTIONS.get(content_type) != EXPECTED_SELECTOR_SCOPE[content_type]["selection"]:
            raise SeedDomainAuditError(f"Canonical V1 selector scope changed for {content_type}")
    return contract, schema, verified


def _receipt_sections(receipt: Mapping[str, Any], label: str) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    identity, evidence, source = receipt.get("request_identity"), receipt.get("payload_evidence"), receipt.get("source_identity")
    if not all(isinstance(part, Mapping) for part in (identity, evidence, source)):
        raise SeedDomainAuditError(f"{label} is missing canonical receipt identity/evidence sections")
    readiness, boundary = receipt.get("readiness"), receipt.get("execution_boundary")
    if not isinstance(readiness, Mapping) or readiness.get("candidate_input_admissible") is not False or readiness.get("video_render_ready") is not False:
        raise SeedDomainAuditError(f"{label} must remain inadmissible and not render-ready")
    if boundary != binder.EXPECTED_BOUNDARY:
        raise SeedDomainAuditError(f"{label} crossed the canonical V1 execution boundary")
    if receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise SeedDomainAuditError(f"{label} does not retain the immutable C11-C manifest")
    if evidence.get("exact_selector_payload_materialized") is not True or evidence.get("materialization") != "IN_MEMORY_ONLY":
        raise SeedDomainAuditError(f"{label} does not prove exact in-memory selector payload materialization")
    for field in ("payload_sha256", "visual_state_sha256"):
        if not isinstance(evidence.get(field), str) or not re.fullmatch(r"[0-9a-f]{64}", str(evidence[field])):
            raise SeedDomainAuditError(f"{label} has malformed {field}")
    if not isinstance(identity.get("request_binding_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", str(identity["request_binding_sha256"])):
        raise SeedDomainAuditError(f"{label} has malformed request binding identity")
    if not isinstance(source.get("request_hash"), str) or not re.fullmatch(r"[0-9a-f]{64}", str(source["request_hash"])):
        raise SeedDomainAuditError(f"{label} has malformed canonical request hash")
    return identity, evidence, source


def _assert_receipt_pair_stable(first: Mapping[str, Any], repeat: Mapping[str, Any], label: str) -> None:
    first_id, first_evidence, first_source = _receipt_sections(first, f"{label}/run-1")
    repeat_id, repeat_evidence, repeat_source = _receipt_sections(repeat, f"{label}/run-2")
    for field in REPEAT_FIELDS:
        if field == "request_hash":
            left, right = first_source.get(field), repeat_source.get(field)
        elif field == "request_binding_sha256":
            left, right = first_id.get(field), repeat_id.get(field)
        else:
            left, right = first_evidence.get(field), repeat_evidence.get(field)
        if left != right:
            raise SeedDomainAuditError(f"Independent repeat drifted in {field}: {label}")


def evaluate_seed_domain_relationships(
    matrix: Mapping[str, Mapping[str, list[Mapping[str, Any]]]],
    source_pin_count: int,
) -> dict[str, Any]:
    if set(matrix) != set(CONTENT_TYPES):
        raise SeedDomainAuditError("Cross-type matrix must include exactly the Challenge and Visual Loop selectors")
    selector_rows: list[dict[str, Any]] = []
    repeat_checks = 0
    for content_type in CONTENT_TYPES:
        variants = matrix[content_type]
        if not isinstance(variants, Mapping) or set(variants) != set(VARIANTS):
            raise SeedDomainAuditError(f"Variant matrix incomplete for {content_type}")
        receipts_by_variant: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
        expected_selection = EXPECTED_SELECTOR_SCOPE[content_type]["selection"]
        expected_scope = EXPECTED_SELECTOR_SCOPE[content_type]["payload_scope"]
        for variant in VARIANTS:
            rows = variants[variant]
            if not isinstance(rows, list) or len(rows) != 2:
                raise SeedDomainAuditError(f"{content_type}/{variant} must contain two independent runtime receipts")
            first, repeat = rows
            _assert_receipt_pair_stable(first, repeat, f"{content_type}/{variant}")
            first_id, first_evidence, _ = _receipt_sections(first, f"{content_type}/{variant}/run-1")
            repeat_id, repeat_evidence, _ = _receipt_sections(repeat, f"{content_type}/{variant}/run-2")
            for identity, evidence, label in ((first_id, first_evidence, "run-1"), (repeat_id, repeat_evidence, "run-2")):
                if identity.get("content_type") != content_type or identity.get("selection") != expected_selection:
                    raise SeedDomainAuditError(f"Canonical selector drift in {content_type}/{variant}/{label}")
                expected_seed, expected_music = VARIANT_SEEDS[variant]
                if identity.get("gameplay_seed") != expected_seed or identity.get("music_seed") != expected_music:
                    raise SeedDomainAuditError(f"Seed domain mismatch in {content_type}/{variant}/{label}")
                if evidence.get("payload_scope") != expected_scope:
                    raise SeedDomainAuditError(f"Payload scope mismatch in {content_type}/{variant}/{label}")
            if any(first_id.get(field) != repeat_id.get(field) for field in IDENTITY_FIELDS):
                raise SeedDomainAuditError(f"Identity fields drifted across independent repeats: {content_type}/{variant}")
            receipts_by_variant[variant] = (first, repeat)
            repeat_checks += 1

        base, base_repeat = receipts_by_variant["BASELINE"]
        game, game_repeat = receipts_by_variant["GAMEPLAY_SEED_ONLY_CHANGED"]
        music, music_repeat = receipts_by_variant["MUSIC_SEED_ONLY_CHANGED"]
        base_id, base_evidence, _ = _receipt_sections(base, f"{content_type}/baseline")
        game_id, game_evidence, _ = _receipt_sections(game, f"{content_type}/gameplay-changed")
        music_id, music_evidence, _ = _receipt_sections(music, f"{content_type}/music-changed")
        for field in IDENTITY_FIELDS:
            if base_id.get(field) != game_id.get(field) or base_id.get(field) != music_id.get(field):
                raise SeedDomainAuditError(f"Identity field {field} drifted across seed experiment: {content_type}")
        if game_id["request_binding_sha256"] == base_id["request_binding_sha256"]:
            raise SeedDomainAuditError(f"Gameplay seed not captured in request binding: {content_type}")
        if music_id["request_binding_sha256"] == base_id["request_binding_sha256"]:
            raise SeedDomainAuditError(f"Music seed not captured in request binding: {content_type}")
        for field in ("payload_sha256", "visual_state_sha256"):
            if game_evidence[field] == base_evidence[field]:
                raise SeedDomainAuditError(f"Gameplay seed did not alter {field}: {content_type}")
            if music_evidence[field] != base_evidence[field]:
                raise SeedDomainAuditError(f"Music seed leaked into {field}: {content_type}")
        if music_evidence.get("grammar_parameter_evidence") != base_evidence.get("grammar_parameter_evidence"):
            raise SeedDomainAuditError(f"Music seed leaked into grammar-parameter evidence: {content_type}")
        if content_type == "visual_loops":
            grammar = base_evidence.get("grammar_parameter_evidence")
            if not isinstance(grammar, Mapping) or grammar.get("grammar_id") != "harmonic_membrane" or not isinstance(grammar.get("parameter_instance_sha256"), str):
                raise SeedDomainAuditError("Visual Loop audit did not return the explicitly pinned harmonic_membrane instance")
        elif base_evidence.get("grammar_parameter_evidence") is not None:
            raise SeedDomainAuditError("Challenge receipt unexpectedly contains Visual Loop grammar evidence")
        selector_rows.append({
            "content_type": content_type,
            "selection": deepcopy(expected_selection),
            "payload_scope": expected_scope,
            "gameplay_seed_sensitivity": "PASS",
            "music_seed_orthogonality": "PASS",
            "independent_repeats": "PASS",
            "baseline_payload_sha256": base_evidence["payload_sha256"],
            "gameplay_changed_payload_sha256": game_evidence["payload_sha256"],
            "music_changed_payload_sha256": music_evidence["payload_sha256"],
            "baseline_visual_state_sha256": base_evidence["visual_state_sha256"],
            "gameplay_changed_visual_state_sha256": game_evidence["visual_state_sha256"],
            "baseline_request_binding_sha256": base_id["request_binding_sha256"],
            "gameplay_changed_request_binding_sha256": game_id["request_binding_sha256"],
            "music_changed_request_binding_sha256": music_id["request_binding_sha256"],
        })
    report: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "schema_version": "1.0",
        "status": STATUS,
        "scope": "CHALLENGE_PARKING_V2_SINGLE_SELECTOR_AND_VISUAL_LOOP_HARMONIC_MEMBRANE_SINGLE_SELECTOR_ONLY",
        "selectors": len(selector_rows),
        "matrix_variants_per_selector": 3,
        "gameplay_seed_sensitivity": {"passed": len(selector_rows), "total": len(CONTENT_TYPES)},
        "music_seed_orthogonality": {"passed": len(selector_rows), "total": len(CONTENT_TYPES)},
        "independent_repeat_checks": {"passed": repeat_checks, "total": 6},
        "source_pin_count": source_pin_count,
        "runtime_invocations": 12,
        "godot_version": None,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "accepted_visual_drill_seed_audit_contract_sha256": None,
        "seed_domains_complete_for_candidate_input": False,
        "unclosed_requirements": [
            "Visual Loop grammars beyond harmonic_membrane remain outside the canonical selector matrix.",
            "Challenge selectors beyond parking_v2/CHALLENGE_004 remain outside this cross-type matrix.",
            "Automatic/default seed, collision, and arbitrary-request cross-domain behavior remain unproven.",
            "Visual Drill seed coverage is covered by its separate V2 matrix and is not replaced by this audit.",
            "No renderer input admission, renderer activation, production execution, or media creation is established.",
        ],
        "per_selector": selector_rows,
        "execution_boundary": deepcopy(GOVERNANCE_BOUNDARY),
    }
    return report


def _build_experiment_requests() -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for content_type in CONTENT_TYPES:
        selection = EXPECTED_SELECTOR_SCOPE[content_type]["selection"]
        request_id = f"C11D-CROSS-SEED-{content_type.upper()}"
        base = binder._base_request(selection, request_id)
        rows: dict[str, dict[str, Any]] = {}
        for variant, (game_seed, music_seed) in VARIANT_SEEDS.items():
            row = deepcopy(base)
            row["seed"] = game_seed
            row["music_seed"] = music_seed
            rows[variant] = row
        if rows["BASELINE"]["request_id"] != rows["GAMEPLAY_SEED_ONLY_CHANGED"]["request_id"] or rows["BASELINE"]["request_id"] != rows["MUSIC_SEED_ONLY_CHANGED"]["request_id"]:
            raise SeedDomainAuditError(f"Request ID drifted in planned matrix: {content_type}")
        if rows["BASELINE"]["selection"] != rows["GAMEPLAY_SEED_ONLY_CHANGED"]["selection"] or rows["BASELINE"]["selection"] != rows["MUSIC_SEED_ONLY_CHANGED"]["selection"]:
            raise SeedDomainAuditError(f"Selector drifted in planned matrix: {content_type}")
        if {k for k in rows["BASELINE"] if rows["BASELINE"][k] != rows["GAMEPLAY_SEED_ONLY_CHANGED"].get(k)} != {"seed"}:
            raise SeedDomainAuditError(f"Gameplay variant changed fields outside the gameplay seed: {content_type}")
        if {k for k in rows["BASELINE"] if rows["BASELINE"][k] != rows["MUSIC_SEED_ONLY_CHANGED"].get(k)} != {"music_seed"}:
            raise SeedDomainAuditError(f"Music variant changed fields outside the music seed: {content_type}")
        result[content_type] = rows
    return result


def _collect_receipts(
    godot: str,
    timeout: int,
    root: Path,
    process_runner: Callable[..., Any] = subprocess.run,
) -> dict[str, dict[str, list[Mapping[str, Any]]]]:
    planned = _build_experiment_requests()
    matrix: dict[str, dict[str, list[Mapping[str, Any]]]] = {}
    for content_type in CONTENT_TYPES:
        matrix[content_type] = {}
        for variant in VARIANTS:
            independent_receipts: list[Mapping[str, Any]] = []
            for run_no in (1, 2):
                result = binder.run_dynamic_request_matrix(
                    godot=godot,
                    timeout=timeout,
                    project_root=root,
                    process_runner=process_runner,
                    raw_requests=[deepcopy(planned[content_type][variant])],
                    mode="v1",
                    independent_repeat=False,
                )
                receipts = result.get("receipts")
                if not isinstance(receipts, list) or len(receipts) != 1:
                    raise SeedDomainAuditError(f"{content_type}/{variant}/run-{run_no} did not return exactly one canonical receipt")
                independent_receipts.append(receipts[0])
                print(f"CROSS-SEED {content_type}/{variant}/run-{run_no}: canonical V1 receipt PASS", file=sys.stderr)
            matrix[content_type][variant] = independent_receipts
    return matrix


def run_cross_type_seed_domain_audit(
    godot: str,
    timeout: int = 120,
    project_root: Path | str | None = None,
    process_runner: Callable[..., Any] = subprocess.run,
    version_probe: Callable[..., Any] = subprocess.run,
) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, pins = _load_and_validate_contract(root)
    if timeout < 1 or timeout > 600:
        raise SeedDomainAuditError("Timeout must be in 1..600 seconds")
    try:
        version = version_probe([godot, "--version"], cwd=str(root), capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SeedDomainAuditError(f"Cannot probe configured Godot executable: {exc}") from exc
    version_lines = ((getattr(version, "stdout", "") or "") + "\n" + (getattr(version, "stderr", "") or "")).strip().splitlines()
    if getattr(version, "returncode", -1) != 0 or not version_lines or not version_lines[0].strip().startswith("4.7.1"):
        raise SeedDomainAuditError(f"Godot 4.7.1 is required, got: {' | '.join(version_lines[:2])}")
    matrix = _collect_receipts(godot, timeout, root, process_runner)
    report = evaluate_seed_domain_relationships(matrix, len(pins))
    report["godot_version"] = version_lines[0].strip()
    report["accepted_visual_drill_seed_audit_contract_sha256"] = _sha_file(root / drill_audit.CONTRACT_REL)
    report["audit_sha256"] = _sha_json(report)
    _validate_report_schema(report, schema)
    return report


def _validate_report_schema(report: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        required = set(schema.get("required", []))
        if required - set(report):
            raise SeedDomainAuditError("Report schema fallback rejected missing fields")
    else:
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(dict(report)), key=lambda err: list(err.path))
        if errors:
            raise SeedDomainAuditError("Report schema validation failed: " + "; ".join(error.message for error in errors[:5]))
    if report.get("audit_sha256") != _sha_json({k: v for k, v in report.items() if k != "audit_sha256"}):
        raise SeedDomainAuditError("Report audit SHA-256 mismatch")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-pinned Challenge/Visual Loop seed-domain audit; no renderer input or media.")
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE", ""), help="Path to Godot 4.7.1 console executable")
    parser.add_argument("--timeout", type=int, default=120, help="Per-harness timeout in seconds")
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--full-report", action="store_true", help="Print the per-selector digest report to stdout only")
    args = parser.parse_args(argv)
    if not args.godot or not Path(args.godot).is_file():
        print("C11-D CROSS-TYPE SEED DOMAIN AUDIT FAIL | Godot 4.7.1 executable missing/configuration invalid | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 2
    try:
        report = run_cross_type_seed_domain_audit(args.godot, args.timeout, args.root)
        summary = (
            "C11-D CROSS-TYPE SEED DOMAIN AUDIT PASS"
            f" | selectors={report['selectors']}"
            f" | gameplay_seed_sensitivity={report['gameplay_seed_sensitivity']['passed']}/{report['gameplay_seed_sensitivity']['total']}"
            f" | music_seed_orthogonality={report['music_seed_orthogonality']['passed']}/{report['music_seed_orthogonality']['total']}"
            f" | independent_repeats={report['independent_repeat_checks']['passed']}/{report['independent_repeat_checks']['total']}"
            f" | source_pins={report['source_pin_count']}/{report['source_pin_count']}"
            f" | runtime_invocations={report['runtime_invocations']}"
            " | seed_domains_complete_for_candidate_input=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
        )
        print(summary)
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (SeedDomainAuditError, binder.DynamicRequestPayloadBindingError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"C11-D CROSS-TYPE SEED DOMAIN AUDIT FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
