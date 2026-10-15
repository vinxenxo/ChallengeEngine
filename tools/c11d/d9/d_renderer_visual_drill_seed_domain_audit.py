from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_SCHEMA_V1.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
# Updated together with the versioned contract/schema in this overlay.
EXPECTED_CONTRACT_SHA256 = "5967a38c227152849a8b2f30ed3dfcea70aac57eca178314fc4a7ee969f17e8c"
EXPECTED_SCHEMA_SHA256 = "e27e72a058e361087328fe8d117688b3ee8b711ba546607e5cfc9b42e9b5c485"
CONTRACT_ID = "C11-D-RENDERER-VISUAL-DRILL-SEED-DOMAIN-AUDIT-V1"
SCHEMA_ID = "urn:c11d:renderer-visual-drill-seed-domain-audit:v1"
STATUS = "PREPARATION_ONLY_VISUAL_DRILL_SEED_DOMAIN_AUDIT_PASS_NOT_RENDERER_INPUT"
ERROR_MARKERS = ("SCRIPT ERROR:", "ERROR:", "C11-D VISUAL DRILL DYNAMIC REQUEST PAYLOAD BINDING V2 FAIL")
SEED_BASE = 12345
SEED_CHANGED = 54321
MUSIC_SEED_BASE = 840001
MUSIC_SEED_CHANGED = 840002


class SeedDomainAuditError(RuntimeError):
    """The Visual Drill seed-domain evidence is incomplete, non-orthogonal, or stale."""


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


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
        raise SeedDomainAuditError("Seed-domain audit contract missing or SHA-256 mismatch")
    if not schema_path.is_file() or _sha_file(schema_path) != EXPECTED_SCHEMA_SHA256:
        raise SeedDomainAuditError("Seed-domain audit report schema missing or SHA-256 mismatch")
    contract = _read_json(contract_path)
    schema = _read_json(schema_path)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise SeedDomainAuditError("Seed-domain audit contract identity/version mismatch")
    if contract.get("status") != "READ_ONLY_SOURCE_PINNED_VISUAL_DRILL_SEED_DOMAIN_AUDIT_NOT_INPUT_ADMISSION":
        raise SeedDomainAuditError("Seed-domain audit contract status is not review-only")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise SeedDomainAuditError("Frozen C11-C reference mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != SCHEMA_ID or schema.get("additionalProperties") is not False:
        raise SeedDomainAuditError("Seed-domain report schema identity/strictness mismatch")
    expected_experiment = {
        "baseline_gameplay_seed": SEED_BASE,
        "changed_gameplay_seed": SEED_CHANGED,
        "baseline_music_seed": MUSIC_SEED_BASE,
        "changed_music_seed": MUSIC_SEED_CHANGED,
        "matrix_variants": ["BASELINE", "GAMEPLAY_SEED_ONLY_CHANGED", "MUSIC_SEED_ONLY_CHANGED"],
        "expected_runtime_invocations": 120,
        "gameplay_seed_change_must_change": ["payload_sha256", "visual_state_sha256", "request_binding_sha256"],
        "music_seed_change_must_preserve": ["payload_sha256", "visual_state_sha256", "visual_drill_authoring_evidence"],
        "music_seed_change_must_change": ["request_binding_sha256"],
        "request_id_and_selector_held_constant_across_each_pair": True,
        "expected_receipt_mode": "CANONICAL_VISUAL_DRILL_V2_RECEIPTS_WITH_INDEPENDENT_REPEAT_EVIDENCE",
    }
    if contract.get("experiment") != expected_experiment:
        raise SeedDomainAuditError("Seed-domain experiment contract changed without runner review")
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) != contract.get("source_pin_count"):
        raise SeedDomainAuditError("Seed-domain source pin count/shape mismatch")
    paths: list[str] = []
    for row in pins:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "role"}:
            raise SeedDomainAuditError("Malformed source pin row")
        rel, expected = row.get("path"), row.get("sha256")
        if not isinstance(rel, str) or not rel or "\\" in rel or rel.startswith("/") or ".." in Path(rel).parts:
            raise SeedDomainAuditError(f"Unsafe source pin path: {rel!r}")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise SeedDomainAuditError(f"Malformed source pin digest for {rel}")
        paths.append(rel)
        source_path = root / rel
        if not source_path.is_file() or _sha_file(source_path) != expected:
            raise SeedDomainAuditError(f"Source pin mismatch: {rel}")
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise SeedDomainAuditError("Source pins must be unique and sorted")
    # Invoke the canonical binder's own contract/lineage validation too.
    v2_contract, input_schema, output_schema, v2_lineage = binder._load_contract_for_mode(root, "visual_drill_v2")
    if len(v2_lineage) != contract.get("v2_source_lineage_count"):
        raise SeedDomainAuditError("Visual Drill V2 source lineage count changed")
    if v2_contract.get("schema") != "C11-D-RENDERER-DYNAMIC-REQUEST-PAYLOAD-BINDING-CONTRACT-V2":
        raise SeedDomainAuditError("Visual Drill V2 canonical binder contract changed")
    if input_schema.get("$id") != contract.get("v2_input_schema_id") or output_schema.get("$id") != contract.get("v2_output_schema_id"):
        raise SeedDomainAuditError("Visual Drill V2 schemas do not match seed audit contract")
    return contract, schema, pins


def _receipt_parts(receipt: Mapping[str, Any], matrix_name: str) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    identity = receipt.get("request_identity")
    evidence = receipt.get("payload_evidence")
    source = receipt.get("source_identity")
    if not all(isinstance(value, Mapping) for value in (identity, evidence, source)):
        raise SeedDomainAuditError(f"{matrix_name} row is not a complete V2 runtime receipt")
    if receipt.get("runtime_verification_status") != "VERIFIED":
        raise SeedDomainAuditError(f"{matrix_name} contains a receipt without runtime verification")
    repeat = receipt.get("runtime_repeat_evidence")
    if not isinstance(repeat, Mapping) or repeat.get("status") != "VERIFIED" or repeat.get("independent_runtime_executions") != 2:
        raise SeedDomainAuditError(f"{matrix_name} lacks independent runtime repeat evidence")
    if evidence.get("exact_selector_payload_materialized") is not True or evidence.get("materialization") != "IN_MEMORY_ONLY":
        raise SeedDomainAuditError(f"{matrix_name} is not an exact in-memory payload receipt")
    return identity, evidence, source


def _selector_key(receipt: Mapping[str, Any], matrix_name: str) -> tuple[str, str]:
    identity = receipt.get("request_identity")
    selection = identity.get("selection") if isinstance(identity, Mapping) else None
    if not isinstance(selection, Mapping):
        raise SeedDomainAuditError(f"{matrix_name} receipt lacks canonical selector identity")
    if selection.get("content_type") != "visual_drills" or selection.get("subtype_id") is not None:
        raise SeedDomainAuditError(f"{matrix_name} contains a non-Visual-Drill selection")
    family, tier = selection.get("family_id"), selection.get("variant_id")
    if not isinstance(family, str) or not isinstance(tier, str):
        raise SeedDomainAuditError(f"{matrix_name} selector fields are malformed")
    return family, tier


def _receipt_map(rows: list[Mapping[str, Any]], matrix_name: str) -> dict[tuple[str, str], Mapping[str, Any]]:
    expected = {
        (family, tier)
        for family in binder.DRILL_V2_FAMILIES
        for tier in binder.DRILL_V2_TIERS
    }
    if len(rows) != 20:
        raise SeedDomainAuditError(f"{matrix_name} matrix must contain 20 receipts, got {len(rows)}")
    mapped: dict[tuple[str, str], Mapping[str, Any]] = {}
    for receipt in rows:
        key = _selector_key(receipt, matrix_name)
        if key not in expected or key in mapped:
            raise SeedDomainAuditError(f"{matrix_name} matrix has unknown/duplicate selector: {key}")
        identity, evidence, source = _receipt_parts(receipt, matrix_name)
        for field in ("request_binding_sha256",):
            value = identity.get(field)
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise SeedDomainAuditError(f"{matrix_name} receipt has malformed request_identity.{field}: {key}")
        for field in ("payload_sha256", "visual_state_sha256"):
            value = evidence.get(field)
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise SeedDomainAuditError(f"{matrix_name} receipt has malformed payload_evidence.{field}: {key}")
        if not isinstance(identity.get("gameplay_seed"), int) or not isinstance(identity.get("music_seed"), int):
            raise SeedDomainAuditError(f"{matrix_name} receipt has malformed seed metadata: {key}")
        authoring = evidence.get("visual_drill_authoring_evidence")
        if not isinstance(authoring, Mapping):
            raise SeedDomainAuditError(f"{matrix_name} receipt lacks Visual Drill authoring evidence: {key}")
        if not isinstance(source.get("request_hash"), str) or not re.fullmatch(r"[0-9a-f]{64}", str(source.get("request_hash"))):
            raise SeedDomainAuditError(f"{matrix_name} receipt has malformed canonical request hash: {key}")
        mapped[key] = receipt
    if set(mapped) != expected:
        raise SeedDomainAuditError(f"{matrix_name} matrix selector coverage is incomplete")
    return mapped


def evaluate_seed_domain_relationships(
    baseline_rows: list[Mapping[str, Any]],
    gameplay_seed_rows: list[Mapping[str, Any]],
    music_seed_rows: list[Mapping[str, Any]],
) -> dict[str, Any]:
    baseline = _receipt_map(baseline_rows, "baseline")
    changed_gameplay = _receipt_map(gameplay_seed_rows, "gameplay-seed-change")
    changed_music = _receipt_map(music_seed_rows, "music-seed-change")
    selector_results: list[dict[str, Any]] = []
    for family in binder.DRILL_V2_FAMILIES:
        for tier in binder.DRILL_V2_TIERS:
            key = (family, tier)
            base, game, music = baseline[key], changed_gameplay[key], changed_music[key]
            for row_name, receipt in (("baseline", base), ("gameplay-seed-change", game), ("music-seed-change", music)):
                if _selector_key(receipt, row_name) != key:
                    raise SeedDomainAuditError(f"Selector drift in {row_name}: expected {key}")
            base_id, base_payload, base_source = _receipt_parts(base, "baseline")
            game_id, game_payload, game_source = _receipt_parts(game, "gameplay-seed-change")
            music_id, music_payload, music_source = _receipt_parts(music, "music-seed-change")
            if base_id["gameplay_seed"] != SEED_BASE or game_id["gameplay_seed"] != SEED_CHANGED:
                raise SeedDomainAuditError(f"Gameplay seed values do not match the declared experiment: {key}")
            if base_id["music_seed"] != MUSIC_SEED_BASE or game_id["music_seed"] != MUSIC_SEED_BASE:
                raise SeedDomainAuditError(f"Gameplay-seed mutation crossed the music seed domain: {key}")
            if music_id["gameplay_seed"] != SEED_BASE or music_id["music_seed"] != MUSIC_SEED_CHANGED:
                raise SeedDomainAuditError(f"Music-seed mutation changed or lost a seed domain: {key}")
            # Each pair must preserve the request and selector identity except for the declared seed.
            invariant_fields = ("request_id", "content_type", "selection", "variation_index", "presentation_profile_id", "delivery_profile_id")
            for field in invariant_fields:
                if base_id.get(field) != game_id.get(field) or base_id.get(field) != music_id.get(field):
                    raise SeedDomainAuditError(f"Request identity field {field} drifted across seed comparison: {key}")
            if game_id["request_binding_sha256"] == base_id["request_binding_sha256"]:
                raise SeedDomainAuditError(f"Gameplay-seed mutation was not retained in request-binding identity: {key}")
            if music_id["request_binding_sha256"] == base_id["request_binding_sha256"]:
                raise SeedDomainAuditError(f"Music-seed mutation was not retained in request-binding identity: {key}")
            if game_payload["visual_state_sha256"] == base_payload["visual_state_sha256"]:
                raise SeedDomainAuditError(f"Gameplay seed did not alter visual-state evidence: {key}")
            if game_payload["payload_sha256"] == base_payload["payload_sha256"]:
                raise SeedDomainAuditError(f"Gameplay seed did not alter the selected visual payload: {key}")
            if music_payload["visual_state_sha256"] != base_payload["visual_state_sha256"]:
                raise SeedDomainAuditError(f"Music-seed mutation leaked into visual-state evidence: {key}")
            if music_payload["payload_sha256"] != base_payload["payload_sha256"]:
                raise SeedDomainAuditError(f"Music-seed mutation leaked into the visual payload: {key}")
            if dict(music_payload["visual_drill_authoring_evidence"]) != dict(base_payload["visual_drill_authoring_evidence"]):
                raise SeedDomainAuditError(f"Music-seed mutation leaked into Visual Drill authoring evidence: {key}")
            selector_results.append({
                "family_id": family,
                "tier": tier,
                "gameplay_seed_sensitivity": "PASS",
                "music_seed_orthogonality": "PASS",
                "baseline_visual_state_sha256": base_payload["visual_state_sha256"],
                "changed_gameplay_visual_state_sha256": game_payload["visual_state_sha256"],
                "baseline_payload_sha256": base_payload["payload_sha256"],
                "changed_gameplay_payload_sha256": game_payload["payload_sha256"],
                "music_seed_payload_sha256": music_payload["payload_sha256"],
                "baseline_request_binding_sha256": base_id["request_binding_sha256"],
                "changed_gameplay_request_binding_sha256": game_id["request_binding_sha256"],
                "changed_music_request_binding_sha256": music_id["request_binding_sha256"],
            })
    report = {
        "schema": SCHEMA_ID,
        "schema_version": "1.0",
        "status": STATUS,
        "scope": "VISUAL_DRILL_FOUR_FAMILIES_X_FIVE_TIERS_ONLY",
        "cases": 20,
        "families_verified": 4,
        "tiers_per_family": 5,
        "gameplay_seed_sensitivity": {"passed": 20, "total": 20},
        "music_seed_orthogonality": {"passed": 20, "total": 20},
        "source_pin_count": None,
        "runtime_invocations": 120,
        "seed_domains_complete_for_candidate_input": False,
        "unclosed_seed_requirements": [
            "automatic-seed and collision/cross-domain behaviour for arbitrary requests",
            "general request-driven seed-domain validation across the full catalog",
        ],
        "per_selector": selector_results,
        "execution_boundary": {
            "runtime": "GODOT_HEADLESS_IN_MEMORY_AUDIT_ONLY",
            "request_input_persisted": False,
            "payload_files_written": False,
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_created": False,
            "output_artifact_path": None,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
        },
    }
    return report


def _run_matrix(
    raws: list[dict[str, Any]], godot: str, timeout: int, root: Path,
    matrix_name: str,
) -> list[dict[str, Any]]:
    try:
        result = binder.run_dynamic_request_matrix(
            godot=godot,
            timeout=timeout,
            project_root=root,
            process_runner=subprocess.run,
            raw_requests=raws,
            mode="visual_drill_v2",
            independent_repeat=True,
        )
    except binder.DynamicRequestPayloadBindingError as exc:
        raise SeedDomainAuditError(f"{matrix_name} Visual Drill V2 runtime matrix failed: {exc}") from exc
    receipts = result.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != 20:
        raise SeedDomainAuditError(f"{matrix_name} binder did not return the required 20 receipts")
    print(f"SEED AUDIT {matrix_name}: receipts=20/20 independent_runtime_repeat=20/20 PASS", file=sys.stderr)
    return receipts

def build_seed_experiment_requests(base_requests: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    baseline = deepcopy(base_requests)
    gameplay_changed = deepcopy(base_requests)
    music_changed = deepcopy(base_requests)
    if len(baseline) != 20:
        raise SeedDomainAuditError(f"Expected 20 baseline Visual Drill requests, got {len(baseline)}")
    for index, (base, game, music) in enumerate(zip(baseline, gameplay_changed, music_changed), start=1):
        for row in (base, game, music):
            selection = row.get("selection")
            if not isinstance(selection, Mapping) or not binder._is_allowed_visual_drill_selection(selection):
                raise SeedDomainAuditError(f"Invalid canonical Visual Drill selector at matrix row {index}")
        if int(base.get("seed", -1)) != SEED_BASE or int(base.get("music_seed", -1)) != MUSIC_SEED_BASE:
            raise SeedDomainAuditError("Canonical base-request seed values drifted from the audit contract")
        game["seed"] = SEED_CHANGED
        music["music_seed"] = MUSIC_SEED_CHANGED
        # Ensure each comparison changes exactly the declared independent field.
        game_diff = {key for key in base if base[key] != game.get(key)}
        music_diff = {key for key in base if base[key] != music.get(key)}
        if game_diff != {"seed"} or music_diff != {"music_seed"}:
            raise SeedDomainAuditError(f"Seed experiment changes unexpected request fields: game={game_diff}, music={music_diff}")
    return baseline, gameplay_changed, music_changed


def run_seed_domain_audit(godot: str, timeout: int = 120, project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, pins = _load_and_validate_contract(root)
    try:
        version = subprocess.run([godot, "--version"], cwd=str(root), capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SeedDomainAuditError(f"Cannot probe configured Godot executable: {exc}") from exc
    version_text = ((version.stdout or "") + "\n" + (version.stderr or "")).strip().splitlines()
    if version.returncode != 0 or not version_text or not version_text[0].strip().startswith("4.7.1"):
        raise SeedDomainAuditError(f"Godot 4.7.1 is required, got: {' | '.join(version_text[:2])}")
    if timeout < 1 or timeout > 600:
        raise SeedDomainAuditError("Timeout must be in 1..600 seconds")
    # The canonical binder performs the accepted V2 per-case independent repeat.
    # Three 20-selector matrices x two runtime executions each = 120 Godot calls.
    base, gameplay_changed, music_changed = build_seed_experiment_requests(binder._visual_drill_matrix_raw_requests())
    baseline_rows = _run_matrix(base, godot, timeout, root, "BASELINE")
    gameplay_rows = _run_matrix(gameplay_changed, godot, timeout, root, "GAMEPLAY_SEED_ONLY_CHANGED")
    music_rows = _run_matrix(music_changed, godot, timeout, root, "MUSIC_SEED_ONLY_CHANGED")
    report = evaluate_seed_domain_relationships(baseline_rows, gameplay_rows, music_rows)
    report["source_pin_count"] = len(pins)
    report["godot_version"] = version_text[0].strip()
    report["frozen_c11c_manifest_sha256"] = EXPECTED_MANIFEST_SHA256
    report["accepted_v2_runtime_log_sha256"] = contract["accepted_baseline_runtime_evidence"]["log_sha256"]
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-pinned Visual Drill V2 seed-domain sensitivity/orthogonality audit; no renderer input or media.")
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE", ""), help="Path to Godot 4.7.1 console executable")
    parser.add_argument("--timeout", type=int, default=120, help="Per-harness timeout in seconds")
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--full-report", action="store_true", help="Print per-selector digest report JSON")
    args = parser.parse_args(argv)
    if not args.godot or not Path(args.godot).is_file():
        print("C11-D VISUAL DRILL SEED DOMAIN AUDIT FAIL | Godot 4.7.1 executable missing/configuration invalid | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 2
    try:
        report = run_seed_domain_audit(args.godot, args.timeout, args.root)
        summary = (
            "C11-D VISUAL DRILL SEED DOMAIN AUDIT PASS"
            f" | cases={report['cases']} | gameplay_seed_sensitivity={report['gameplay_seed_sensitivity']['passed']}/{report['gameplay_seed_sensitivity']['total']}"
            f" | music_seed_orthogonality={report['music_seed_orthogonality']['passed']}/{report['music_seed_orthogonality']['total']}"
            f" | source_pins={report['source_pin_count']}/{report['source_pin_count']} | runtime_invocations={report['runtime_invocations']}"
            " | seed_domains_complete_for_candidate_input=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
        )
        print(summary)
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (SeedDomainAuditError, binder.DynamicRequestPayloadBindingError, OSError, ValueError, TypeError) as exc:
        print(f"C11-D VISUAL DRILL SEED DOMAIN AUDIT FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
