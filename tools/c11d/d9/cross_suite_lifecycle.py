"""D9.13 shared cross-suite lifecycle receipt builder and validator.

The module composes existing canonical suite backends; it does not duplicate request
normalization, editorial resolution, QA, catalog eligibility, or maintenance policy.
Every stage remains plan-only. No media or release artifact is created by this module.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT_REL = Path("definitions/c11d/d9/D9_13_CROSS_SUITE_LIFECYCLE_V1.json")
RECEIPT_SCHEMA = "C11-D-D9.13-CROSS-SUITE-LIFECYCLE-RECEIPT-V1"
RECEIPT_ROOT = Path("artifacts/tests/c11d_d9/producer_universal")
EXPECTED_SURFACES = ["c11c-config", "c11c-producer", "c11c-test", "c11c-catalog", "c11c-maintenance"]
EXPECTED_VERSIONS = {
    "c11c-config": "0.2.0", "c11c-producer": "0.11.1", "c11c-test": "0.2.0",
    "c11c-catalog": "0.2.0", "c11c-maintenance": "0.2.0",
}
GOVERNANCE = {
    "renderer_activation": False,
    "renderer_input_emitted": False,
    "production_execution": False,
    "media_output_created": False,
    "d4_8": "BLOCKED",
    "runtime_authority": "NONE",
    "release_authority": "NONE",
    "c11c_frozen_reference_mutation": "FORBIDDEN",
}


class CrossSuiteLifecycleError(ValueError):
    """Raised when a D9.13 hand-off breaks canonical identity or governance."""


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise CrossSuiteLifecycleError(f"Cannot read canonical JSON {path}: {exc}") from exc


def _load_module(name: str, path: Path):
    key = f"_c11d_d913_{name}"
    if key in sys.modules:
        return sys.modules[key]
    if not path.is_file():
        raise CrossSuiteLifecycleError(f"Required canonical surface module missing: {path}")
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise CrossSuiteLifecycleError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(key, None)
        raise
    return module


def _root(path: Path | str | None = None) -> Path:
    return Path(path).resolve() if path is not None else ROOT.resolve()


def _inside(base: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(base.resolve())
        return True
    except (ValueError, OSError):
        return False


def _require_plan_evidence(root: Path, evidence_dir: Path, request: Mapping[str, Any]) -> dict[str, Any]:
    evidence_root = (root / RECEIPT_ROOT).resolve()
    folder = Path(evidence_dir).resolve()
    if not _inside(evidence_root, folder):
        raise CrossSuiteLifecycleError("Producer evidence must be under the canonical D9 universal evidence root")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,160}", request_id):
        raise CrossSuiteLifecycleError("request_id is invalid")
    if folder.name != request_id:
        raise CrossSuiteLifecycleError("request_id must match the persisted Producer evidence directory")

    required = (
        "request.json", "canonical_request.json", "editorial_resolution.json", "universal_plan.json",
        "editorial_render_bridge_plan.json", "d4_subplan_evidence.json", "gui_cli_parity.json",
        "producer_universal_receipt.json",
    )
    docs: dict[str, Any] = {}
    for name in required:
        path = folder / name
        if not path.is_file() or path.is_symlink():
            raise CrossSuiteLifecycleError(f"Producer evidence missing or unsafe: {name}")
        docs[name] = _read_json(path)
    if docs["request.json"] != dict(request):
        raise CrossSuiteLifecycleError("Persisted raw request differs from current request source")
    if docs["producer_universal_receipt.json"].get("request_id") != request_id:
        raise CrossSuiteLifecycleError("Producer receipt request_id mismatch")
    return docs


def _config_stage(root: Path, identity: dict[str, Any], lifecycle_id: str, identity_sha256: str) -> dict[str, Any]:
    config = _load_module("config", root / "c11c-suite/c11c-config/c11d_config.py")
    rows, errors = config.validate_c11d_contracts(root)
    if errors:
        raise CrossSuiteLifecycleError("Config canonical registry invalid: " + "; ".join(errors))
    contracts = [
        {"id": row["id"], "path": row["path"], "sha256": row["sha256"]}
        for row in rows
    ]
    if not contracts or any(len(row["sha256"]) != 64 for row in contracts):
        raise CrossSuiteLifecycleError("Config registry has missing contract hashes")
    versions = _read_json(root / "c11c-suite/c11c-config/BUILD_MANIFEST.json")
    if versions.get("version") != EXPECTED_VERSIONS["c11c-config"]:
        raise CrossSuiteLifecycleError("Config 0.2.0 version identity mismatch")
    delivery_path = root / "profiles/delivery/c11c_video_delivery_profiles.json"
    evidence = {
        "config_registry_sha256": sha256(contracts),
        "registry_count": len(contracts),
        "contract_hashes": contracts,
        "delivery_profile_registry_sha256": sha256_file(delivery_path),
        "profile_bindings": {
            "delivery_profile_id": identity["delivery_profile_id"],
            "resolved_delivery_profile_id": identity["resolved_delivery_profile_id"],
            "presentation_profile_id": identity["presentation_profile_id"],
            "personalization_enabled": identity["personalization_enabled"],
        },
        "profile_bindings_sha256": sha256({
            key: identity[key] for key in (
                "delivery_profile_id", "resolved_delivery_profile_id", "presentation_profile_id", "personalization_enabled"
            )
        }),
        "canonical_contracts_access": "READ_ONLY",
    }
    return _stage("c11c-config", lifecycle_id, identity_sha256, "PASS_READ_ONLY_CONFIG_BINDINGS", evidence)


def _test_stage(root: Path, identity: dict[str, Any], lifecycle_id: str, identity_sha256: str) -> dict[str, Any]:
    manifest_path = root / "c11c-suite/c11c-test/BUILD_MANIFEST.json"
    manifest = _read_json(manifest_path)
    if manifest.get("suite_id") != "c11c-test" or manifest.get("version") != EXPECTED_VERSIONS["c11c-test"]:
        raise CrossSuiteLifecycleError("Test version identity mismatch")
    contract_test = root / "c11c-suite/c11c-test/test_d9_test_integration.py"
    tester = _load_module("test_contract", contract_test)
    counts = tester.run_checks()
    route_path = root / "c11c-suite/c11c-test/main.py"
    route_count = counts.get("all_routes")
    if route_count is None or counts.get("surfaces") != 5:
        raise CrossSuiteLifecycleError("Test route registry did not certify all five surfaces")
    evidence = {
        "build_manifest_sha256": sha256_file(manifest_path),
        "integration_contract_sha256": sha256_file(contract_test),
        "route_source_sha256": sha256_file(route_path),
        "registered_route_count": int(route_count),
        "canonical_surface_count": counts["surfaces"],
        "negative_acceptance_reference": "tools/c11d/d9/test_d9_negative_acceptance.py",
        "gui_cli_parity_reference": "tools/c11d/d9/test_d9_gui_cli_parity.py",
        "plan_identity_validation": "PASS",
        "media_qa": "NOT_APPLICABLE_NO_MEDIA_CREATED",
        "no_media": True,
    }
    return _stage("c11c-test", lifecycle_id, identity_sha256, "PASS_PLAN_ONLY_QA_CONTRACT", evidence)


def _stage(surface: str, lifecycle_id: str, identity_sha256: str, status: str, evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "surface": surface,
        "version": EXPECTED_VERSIONS[surface],
        "lifecycle_id": lifecycle_id,
        "identity_sha256": identity_sha256,
        "binding_sha256": None,
        "status": status,
        "evidence": evidence,
    }


def build_catalog_projection(identity: Mapping[str, Any], lifecycle_id: str, identity_sha256: str, evidence_path: str, project_root: Path | str | None = None) -> dict[str, Any]:
    """Call the existing Catalog backend's read-only D9.13 plan projection adapter."""
    root = _root(project_root)
    module = _load_module("catalog", root / "c11c-suite/c11c-catalog/c11d_catalog.py")
    return module.project_cross_suite_lifecycle_intent(dict(identity), lifecycle_id, identity_sha256, evidence_path)


def build_lifecycle_receipt(
    raw_request: Mapping[str, Any],
    project_root: Path | str | None = None,
    evidence_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Build a sealed lifecycle receipt from the Producer GUI's persisted evidence bundle."""
    root = _root(project_root)
    if evidence_dir is None:
        raise CrossSuiteLifecycleError("evidence_dir is required; lifecycle receipts must bind to persisted Producer evidence")
    docs = _require_plan_evidence(root, Path(evidence_dir), raw_request)

    producer = _load_module("producer", root / "tools/c11d/d9/universal_producer.py")
    bridge_module = _load_module("bridge", root / "tools/c11d/d9/editorial_render_bridge.py")
    result = producer.evaluate_universal_request(raw_request, root)
    bridge = bridge_module.build_bridge_planning_record(result, root)
    parity = docs["gui_cli_parity.json"]
    parity_checks = parity.get("checks") if isinstance(parity, dict) else None
    expected_parity_checks = {
        "canonical_request_equal", "request_hash_equal", "editorial_hash_equal", "plan_equal", "plan_hash_equal", "bridge_planning_record_equal"
    }
    if parity.get("status") != "PASS" or not isinstance(parity_checks, dict) or set(parity_checks) != expected_parity_checks or not all(parity_checks.values()):
        raise CrossSuiteLifecycleError("Persisted GUI/CLI parity receipt is not a complete PASS")
    if docs["canonical_request.json"] != result["canonical_request"]:
        raise CrossSuiteLifecycleError("Persisted canonical request does not match the canonical Producer backend")
    if docs["universal_plan.json"] != result["plan"]:
        raise CrossSuiteLifecycleError("Persisted plan differs from canonical Producer plan")
    if docs["editorial_render_bridge_plan.json"] != bridge:
        raise CrossSuiteLifecycleError("Persisted bridge record differs from canonical bridge backend")
    if docs["producer_universal_receipt.json"].get("request_hash") != result["request_hash"] or docs["producer_universal_receipt.json"].get("plan_hash") != result["plan_hash"]:
        raise CrossSuiteLifecycleError("Persisted Producer receipt identity mismatch")
    if docs["producer_universal_receipt.json"].get("bridge_record_hash") != bridge.get("record_hash"):
        raise CrossSuiteLifecycleError("Persisted Producer bridge hash mismatch")
    for name, expected in (("request_hash", result["request_hash"]), ("editorial_hash", result["editorial_hash"]), ("plan_hash", result["plan_hash"])):
        if docs["producer_universal_receipt.json"].get(name) != expected:
            raise CrossSuiteLifecycleError(f"Persisted Producer receipt {name} mismatch")
    if parity.get("bridge_record_hash") != bridge.get("record_hash") or parity.get("gui_plan_hash") != result["plan_hash"]:
        raise CrossSuiteLifecycleError("Persisted GUI/CLI parity receipt does not bind to the canonical plan and bridge")

    plan = result["plan"]
    canonical_request = result["canonical_request"]
    identity = {
        "request_id": str(canonical_request["request_id"]),
        "content_type": str(plan["selection"]["content_type"]),
        "selection": _canonical(plan["selection"]),
        "request_hash": str(result["request_hash"]),
        "editorial_hash": str(result["editorial_hash"]),
        "plan_hash": str(result["plan_hash"]),
        "bridge_record_hash": str(bridge["record_hash"]),
        "gameplay_seed": int(canonical_request["seed"]),
        "music_seed": int(canonical_request["music_seed"]),
        "delivery_profile_id": str(canonical_request["delivery_profile_id"]),
        "resolved_delivery_profile_id": str(canonical_request["resolved_delivery_profile_id"]),
        "presentation_profile_id": str(canonical_request["presentation_profile_id"]),
        "audio_enabled": bool(canonical_request["audio_enabled"]),
        "personalization_enabled": bool(canonical_request["personalization_enabled"]),
    }
    identity_sha256 = sha256(identity)
    lifecycle_id = "D9L13-" + sha256({"request_hash": identity["request_hash"], "plan_hash": identity["plan_hash"], "bridge_record_hash": identity["bridge_record_hash"]})[:24].upper()
    binding_payload = {key: identity[key] for key in (
        "gameplay_seed", "music_seed", "delivery_profile_id", "resolved_delivery_profile_id",
        "presentation_profile_id", "audio_enabled", "personalization_enabled"
    )}
    binding_sha256 = sha256(binding_payload)

    contract = _read_json(root / CONTRACT_REL)
    if contract.get("schema") != "C11-D-D9.13-CROSS-SUITE-LIFECYCLE-CONTRACT-V1" or contract.get("checkpoint") != "D9.13":
        raise CrossSuiteLifecycleError("D9.13 canonical contract identity mismatch")
    contract_stages = _config_stage(root, identity, lifecycle_id, identity_sha256)
    producer_manifest = _read_json(root / "c11c-suite/c11c-producer/BUILD_MANIFEST.json")
    if producer_manifest.get("version") != EXPECTED_VERSIONS["c11c-producer"]:
        raise CrossSuiteLifecycleError("Producer version identity mismatch")
    producer_stage = _stage("c11c-producer", lifecycle_id, identity_sha256, "PASS_CANONICAL_PLAN_ONLY", {
        "persisted_evidence_directory": Path(evidence_dir).resolve().relative_to(root).as_posix(),
        "producer_manifest_sha256": sha256_file(root / "c11c-suite/c11c-producer/BUILD_MANIFEST.json"),
        "request_hash": identity["request_hash"], "editorial_hash": identity["editorial_hash"],
        "plan_hash": identity["plan_hash"], "bridge_record_hash": identity["bridge_record_hash"],
        "source_revision": canonical_request.get("source_revision"),
        "gameplay_seed": identity["gameplay_seed"], "music_seed": identity["music_seed"],
        "delivery_profile_id": identity["delivery_profile_id"],
        "resolved_delivery_profile_id": identity["resolved_delivery_profile_id"],
        "presentation_profile_id": identity["presentation_profile_id"],
        "audio_enabled": identity["audio_enabled"], "personalization_enabled": identity["personalization_enabled"],
        "content_type": identity["content_type"], "selection": identity["selection"],
        "gameplay_seed_source": "canonical_request.seed", "music_seed_source": "canonical_request.music_seed",
        "cross_domain_seed_sharing": "FORBIDDEN", "automatic_seed_generation": False, "runtime_seed_derivation": False,
    })
    test_stage = _test_stage(root, identity, lifecycle_id, identity_sha256)
    projection = build_catalog_projection(identity, lifecycle_id, identity_sha256, (Path(evidence_dir).resolve().relative_to(root) / "cross_suite_lifecycle_receipt.json").as_posix(), root)
    catalog_manifest = _read_json(root / "c11c-suite/c11c-catalog/BUILD_MANIFEST.json")
    if catalog_manifest.get("version") != EXPECTED_VERSIONS["c11c-catalog"]:
        raise CrossSuiteLifecycleError("Catalog version identity mismatch")
    catalog_stage = _stage("c11c-catalog", lifecycle_id, identity_sha256, "PASS_READ_ONLY_IDENTITY_PROJECTION", {
        "catalog_manifest_sha256": sha256_file(root / "c11c-suite/c11c-catalog/BUILD_MANIFEST.json"),
        "projection_schema": projection["schema"],
        "projection_sha256": sha256(projection),
        "record_type": projection["record_type"],
        "media_created": False, "media_path": None, "media_sha256": None,
        "release_authority": "NONE",
    })

    maintenance = _load_module("maintenance", root / "tools/c11d/d9/maintenance.py")
    maintenance_plan = maintenance.build_plan(root)
    if maintenance_plan.get("status") != "PASS":
        raise CrossSuiteLifecycleError("Maintenance read-only plan is not PASS: " + "; ".join(maintenance_plan.get("errors", [])))
    policy_path = root / "definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json"
    manifest_path = root / str(maintenance_plan.get("historical_manifest", {}).get("path") or "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    maintenance_manifest = _read_json(root / "c11c-suite/c11c-maintenance/BUILD_MANIFEST.json")
    if maintenance_manifest.get("version") != EXPECTED_VERSIONS["c11c-maintenance"]:
        raise CrossSuiteLifecycleError("Maintenance version identity mismatch")
    maintenance_stage = _stage("c11c-maintenance", lifecycle_id, identity_sha256, "PASS_READ_ONLY_MAINTENANCE_AUDIT", {
        "maintenance_manifest_sha256": sha256_file(root / "c11c-suite/c11c-maintenance/BUILD_MANIFEST.json"),
        "maintenance_policy_sha256": sha256_file(policy_path),
        "historical_c11c_manifest_path": maintenance_plan["historical_manifest"]["path"],
        "historical_c11c_manifest_sha256": sha256_file(manifest_path),
        "maintenance_plan_status": maintenance_plan["status"],
        "registered_surface_count": maintenance_plan["registered_surface_count"],
        "freeze_ready": False,
        "side_effects": {"files_moved": False, "files_deleted": False, "manifest_rewritten": False, "archive_created": False},
    })

    stages = [contract_stages, producer_stage, test_stage, catalog_stage, maintenance_stage]
    for stage in stages:
        stage["binding_sha256"] = binding_sha256
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "schema_version": "1.0",
        "checkpoint": "D9.13",
        "status": "PASS_PLAN_ONLY",
        "lifecycle_id": lifecycle_id,
        "identity_sha256": identity_sha256,
        "identity": identity,
        "binding_sha256": binding_sha256,
        "stages": stages,
        "governance": dict(GOVERNANCE),
        "media_created": False,
        "media_path": None,
        "media_sha256": None,
        "release_authority": "NONE",
        "evidence": {
            "producer_evidence_directory": Path(evidence_dir).resolve().relative_to(root).as_posix(),
            "producer_gui_cli_parity": "PASS",
            "catalog_projection_sha256": sha256(projection),
            "maintenance_is_dry_run": True,
        },
    }
    receipt["receipt_sha256"] = sha256(receipt)
    validate_lifecycle_receipt(receipt, root, verify_current=True)
    return receipt


def validate_lifecycle_receipt(receipt: Mapping[str, Any], project_root: Path | str | None = None, *, verify_current: bool = True) -> dict[str, Any]:
    """Validate checksum, exact stage order, identity binding and optionally current contracts."""
    root = _root(project_root)
    if not isinstance(receipt, Mapping):
        raise CrossSuiteLifecycleError("Lifecycle receipt must be an object")
    data = dict(receipt)
    if data.get("schema") != RECEIPT_SCHEMA or data.get("schema_version") != "1.0" or data.get("checkpoint") != "D9.13":
        raise CrossSuiteLifecycleError("Unsupported D9.13 lifecycle receipt schema/checkpoint")
    expected_hash = data.get("receipt_sha256")
    payload = {key: value for key, value in data.items() if key != "receipt_sha256"}
    if not isinstance(expected_hash, str) or sha256(payload) != expected_hash:
        raise CrossSuiteLifecycleError("Lifecycle receipt checksum mismatch")
    if data.get("status") != "PASS_PLAN_ONLY":
        raise CrossSuiteLifecycleError("Lifecycle receipt is not PASS_PLAN_ONLY")
    identity = data.get("identity")
    if not isinstance(identity, Mapping):
        raise CrossSuiteLifecycleError("Lifecycle identity payload missing")
    identity_hash = sha256(identity)
    if identity_hash != data.get("identity_sha256"):
        raise CrossSuiteLifecycleError("Lifecycle identity hash mismatch")
    lifecycle_id = "D9L13-" + sha256({"request_hash": identity.get("request_hash"), "plan_hash": identity.get("plan_hash"), "bridge_record_hash": identity.get("bridge_record_hash")})[:24].upper()
    if lifecycle_id != data.get("lifecycle_id"):
        raise CrossSuiteLifecycleError("Lifecycle ID does not match canonical request/plan/bridge hashes")
    stages = data.get("stages")
    if not isinstance(stages, list) or [row.get("surface") for row in stages if isinstance(row, Mapping)] != EXPECTED_SURFACES or len(stages) != 5:
        raise CrossSuiteLifecycleError("Lifecycle stages must be exactly Config → Producer → Test → Catalog → Maintenance")
    for stage in stages:
        if not isinstance(stage, Mapping):
            raise CrossSuiteLifecycleError("Lifecycle stage must be an object")
        if stage.get("lifecycle_id") != lifecycle_id or stage.get("identity_sha256") != identity_hash or stage.get("binding_sha256") != data.get("binding_sha256"):
            raise CrossSuiteLifecycleError(f"Identity or seed/profile binding drift at {stage.get('surface')}")
        if stage.get("version") != EXPECTED_VERSIONS.get(str(stage.get("surface"))) or not str(stage.get("status", "")).startswith("PASS"):
            raise CrossSuiteLifecycleError(f"Stage not accepted or version mismatch: {stage.get('surface')}")
    binding = {key: identity.get(key) for key in (
        "gameplay_seed", "music_seed", "delivery_profile_id", "resolved_delivery_profile_id",
        "presentation_profile_id", "audio_enabled", "personalization_enabled"
    )}
    if sha256(binding) != data.get("binding_sha256"):
        raise CrossSuiteLifecycleError("Gameplay/music seed or profile binding hash mismatch")
    producer_stage = stages[1]["evidence"]
    for key in ("request_hash", "editorial_hash", "plan_hash", "bridge_record_hash"):
        if producer_stage.get(key) != identity.get(key):
            raise CrossSuiteLifecycleError(f"Producer stage changed canonical identity field: {key}")
    if producer_stage.get("gameplay_seed_source") != "canonical_request.seed" or producer_stage.get("music_seed_source") != "canonical_request.music_seed":
        raise CrossSuiteLifecycleError("Seed source reinterpretation is forbidden")
    if producer_stage.get("cross_domain_seed_sharing") != "FORBIDDEN" or producer_stage.get("automatic_seed_generation") is not False or producer_stage.get("runtime_seed_derivation") is not False:
        raise CrossSuiteLifecycleError("Seed governance drifted across lifecycle")
    if data.get("governance") != GOVERNANCE:
        raise CrossSuiteLifecycleError("D9.13 governance invariants must remain locked")
    if data.get("media_created") is not False or data.get("media_path") is not None or data.get("media_sha256") is not None or data.get("release_authority") != "NONE":
        raise CrossSuiteLifecycleError("Plan-only lifecycle receipt may not claim media or release authority")
    if stages[2]["evidence"].get("media_qa") != "NOT_APPLICABLE_NO_MEDIA_CREATED" or stages[2]["evidence"].get("no_media") is not True:
        raise CrossSuiteLifecycleError("Test stage must not imply physical media QA without media")
    cat_evidence = stages[3]["evidence"]
    if cat_evidence.get("media_created") is not False or cat_evidence.get("media_path") is not None or cat_evidence.get("media_sha256") is not None or cat_evidence.get("release_authority") != "NONE":
        raise CrossSuiteLifecycleError("Catalog projection claims media/release state not present in this plan-only lifecycle")
    maintenance_evidence = stages[4]["evidence"]
    if maintenance_evidence.get("maintenance_plan_status") != "PASS" or maintenance_evidence.get("freeze_ready") is not False:
        raise CrossSuiteLifecycleError("Maintenance must be a PASS dry-run, never a freeze authorization")
    if maintenance_evidence.get("side_effects") != {"files_moved": False, "files_deleted": False, "manifest_rewritten": False, "archive_created": False}:
        raise CrossSuiteLifecycleError("Maintenance lifecycle audit must remain read-only")

    if verify_current:
        contract = _read_json(root / CONTRACT_REL)
        if contract.get("schema") != "C11-D-D9.13-CROSS-SUITE-LIFECYCLE-CONTRACT-V1":
            raise CrossSuiteLifecycleError("Current D9.13 contract missing or mismatched")
        config = _load_module("config", root / "c11c-suite/c11c-config/c11d_config.py")
        rows, errors = config.validate_c11d_contracts(root)
        if errors:
            raise CrossSuiteLifecycleError("Current Config registry invalid: " + "; ".join(errors))
        current_contracts = [{"id": row["id"], "path": row["path"], "sha256": row["sha256"]} for row in rows]
        if sha256(current_contracts) != stages[0]["evidence"].get("config_registry_sha256"):
            raise CrossSuiteLifecycleError("Config contract set changed after lifecycle receipt generation")
        if sha256_file(root / "profiles/delivery/c11c_video_delivery_profiles.json") != stages[0]["evidence"].get("delivery_profile_registry_sha256"):
            raise CrossSuiteLifecycleError("Delivery profile registry changed after lifecycle receipt generation")
        test_manifest = root / "c11c-suite/c11c-test/BUILD_MANIFEST.json"
        if sha256_file(test_manifest) != stages[2]["evidence"].get("build_manifest_sha256"):
            raise CrossSuiteLifecycleError("Test route manifest changed after lifecycle receipt generation")
        policy_path = root / "definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json"
        manifest_path = root / str(maintenance_evidence.get("historical_c11c_manifest_path"))
        if not manifest_path.is_file() or sha256_file(manifest_path) != maintenance_evidence.get("historical_c11c_manifest_sha256"):
            raise CrossSuiteLifecycleError("Historical C11-C freeze manifest changed or missing")
        if sha256_file(policy_path) != maintenance_evidence.get("maintenance_policy_sha256"):
            raise CrossSuiteLifecycleError("Maintenance policy changed after lifecycle receipt generation")
        evidence_dir_rel = data.get("evidence", {}).get("producer_evidence_directory")
        if not isinstance(evidence_dir_rel, str):
            raise CrossSuiteLifecycleError("Producer evidence directory binding is missing")
        evidence_dir = (root / evidence_dir_rel).resolve()
        docs = _require_plan_evidence(root, evidence_dir, _read_json(evidence_dir / "request.json"))
        producer = _load_module("producer", root / "tools/c11d/d9/universal_producer.py")
        bridge_module = _load_module("bridge", root / "tools/c11d/d9/editorial_render_bridge.py")
        replay = producer.evaluate_universal_request(docs["request.json"], root)
        replay_bridge = bridge_module.build_bridge_planning_record(replay, root)
        expected_identity = {
            "request_id": str(replay["canonical_request"]["request_id"]),
            "content_type": str(replay["plan"]["selection"]["content_type"]),
            "selection": _canonical(replay["plan"]["selection"]),
            "request_hash": str(replay["request_hash"]),
            "editorial_hash": str(replay["editorial_hash"]),
            "plan_hash": str(replay["plan_hash"]),
            "bridge_record_hash": str(replay_bridge["record_hash"]),
            "gameplay_seed": int(replay["canonical_request"]["seed"]),
            "music_seed": int(replay["canonical_request"]["music_seed"]),
            "delivery_profile_id": str(replay["canonical_request"]["delivery_profile_id"]),
            "resolved_delivery_profile_id": str(replay["canonical_request"]["resolved_delivery_profile_id"]),
            "presentation_profile_id": str(replay["canonical_request"]["presentation_profile_id"]),
            "audio_enabled": bool(replay["canonical_request"]["audio_enabled"]),
            "personalization_enabled": bool(replay["canonical_request"]["personalization_enabled"]),
        }
        if _canonical(expected_identity) != _canonical(identity):
            raise CrossSuiteLifecycleError("Persisted Producer request no longer resolves to the sealed cross-suite identity")
        if docs["canonical_request.json"] != replay["canonical_request"] or docs["universal_plan.json"] != replay["plan"] or docs["editorial_render_bridge_plan.json"] != replay_bridge:
            raise CrossSuiteLifecycleError("Persisted Producer request/plan/bridge no longer reproduces byte-semantic identity")
        projection = build_catalog_projection(identity, lifecycle_id, identity_hash, (evidence_dir_rel.rstrip("/") + "/cross_suite_lifecycle_receipt.json"), root)
        if sha256(projection) != cat_evidence.get("projection_sha256") or sha256(projection) != data.get("evidence", {}).get("catalog_projection_sha256"):
            raise CrossSuiteLifecycleError("Catalog projection no longer matches the shared lifecycle identity")
    return {"status": "PASS", "lifecycle_id": lifecycle_id, "identity_sha256": identity_hash, "stages": len(stages), "media_created": False, "release_authority": "NONE"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="D9.13 cross-suite lifecycle validator (plan-only; no media)")
    parser.add_argument("--receipt", required=True, help="Repository-relative persisted cross_suite_lifecycle_receipt.json")
    parser.add_argument("--root", default=None, help="Project root (defaults to repository root)")
    args = parser.parse_args(argv)
    root = _root(args.root)
    try:
        rel = args.receipt.replace("\\", "/")
        if not rel.startswith(RECEIPT_ROOT.as_posix() + "/") or not rel.endswith("/cross_suite_lifecycle_receipt.json"):
            raise CrossSuiteLifecycleError("Receipt path must be within the canonical Producer universal evidence root")
        if "/../" in f"/{rel}/" or rel.startswith("/") or ":" in rel:
            raise CrossSuiteLifecycleError("Absolute and traversal paths are forbidden")
        path = root / rel
        if path.is_symlink() or not path.is_file() or not _inside(root / RECEIPT_ROOT, path):
            raise CrossSuiteLifecycleError("Lifecycle receipt missing or unsafe")
        receipt = _read_json(path)
        checked = validate_lifecycle_receipt(receipt, root, verify_current=True)
        maintenance = _load_module("maintenance", root / "tools/c11d/d9/maintenance.py")
        plan = maintenance.build_plan(root)
        if plan.get("status") != "PASS":
            raise CrossSuiteLifecycleError("Current Maintenance plan is not PASS")
        current_manifest = plan["historical_manifest"].get("sha256")
        if current_manifest != receipt["stages"][4]["evidence"].get("historical_c11c_manifest_sha256"):
            raise CrossSuiteLifecycleError("Maintenance observed a different C11-C historical manifest hash")
        result = {"schema": "C11-D-D9.13-LIFECYCLE-AUDIT-V1", **checked, "operation": "READ_ONLY_AUDIT", "side_effects": {"files_written": False, "files_moved": False, "files_deleted": False, "manifest_rewritten": False, "media_created": False}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": "C11-D-D9.13-LIFECYCLE-AUDIT-V1", "status": "BLOCKED", "errors": [str(exc)], "side_effects": {"files_written": False, "files_moved": False, "files_deleted": False, "manifest_rewritten": False, "media_created": False}}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
