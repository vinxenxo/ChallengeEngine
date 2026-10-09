from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from test_universal_producer import _raw  # noqa: E402
from test_editorial_render_bridge import _representative_selections  # noqa: E402
from cross_suite_lifecycle import (  # noqa: E402
    CrossSuiteLifecycleError,
    build_lifecycle_receipt,
    canonical_json,
    sha256,
    validate_lifecycle_receipt,
)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _module(name: str, rel: str):
    path = ROOT / rel
    key = f"_d913_test_{name}"
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot load {rel}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


def _seed_evidence(request: dict[str, Any], run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    producer = _module("producer_backend", "tools/c11d/d9/universal_producer.py")
    bridge_backend = _module("bridge_backend", "tools/c11d/d9/editorial_render_bridge.py")
    result = producer.evaluate_universal_request(request, ROOT)
    bridge = bridge_backend.build_bridge_planning_record(result, ROOT)
    request_path = run_dir / "request.json"
    _write_json(request_path, request)
    cli_script = ROOT / "tools/c11d/d9/universal_producer_cli.py"
    cli = subprocess.run(
        [sys.executable, str(cli_script), "--request", str(request_path), "--print-json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=45,
    )
    if cli.returncode != 0:
        raise AssertionError("Canonical universal Producer CLI failed: " + cli.stdout + "\n" + cli.stderr)
    cli_result = json.loads(cli.stdout)
    parity_checks = {
        "canonical_request_equal": result["canonical_request"] == cli_result["canonical_request"],
        "request_hash_equal": result["request_hash"] == cli_result["request_hash"],
        "editorial_hash_equal": result["editorial_hash"] == cli_result["editorial_hash"],
        "plan_equal": result["plan"] == cli_result["plan"],
        "plan_hash_equal": result["plan_hash"] == cli_result["plan_hash"],
        "bridge_planning_record_equal": bridge == cli_result.get("bridge_planning_record"),
    }
    if not all(parity_checks.values()):
        raise AssertionError(f"GUI/CLI semantic parity failed: {parity_checks}")
    parity = {
        "schema": "C11-D-D9.10-UNIVERSAL-GUI-CLI-BRIDGE-PARITY-V1",
        "status": "PASS",
        "content_type": result["canonical_request"]["selection"]["content_type"],
        "selection": result["canonical_request"]["selection"],
        "checks": parity_checks,
        "gui_request_hash": result["request_hash"],
        "cli_request_hash": cli_result["request_hash"],
        "gui_plan_hash": result["plan_hash"],
        "cli_plan_hash": cli_result["plan_hash"],
        "bridge_record_hash": bridge["record_hash"],
        "cli_bridge_record_hash": cli_result["bridge_planning_record"]["record_hash"],
        "renderer_input_emitted": False,
        "renderer": False,
        "production_execution": False,
        "release_authority": "NONE",
    }
    _write_json(run_dir / "canonical_request.json", result["canonical_request"])
    _write_json(run_dir / "editorial_resolution.json", result["editorial_resolution"])
    _write_json(run_dir / "universal_plan.json", result["plan"])
    _write_json(run_dir / "editorial_render_bridge_plan.json", bridge)
    _write_json(run_dir / "d4_subplan_evidence.json", result.get("d4_evidence") or {"status": "NOT_APPLICABLE"})
    _write_json(run_dir / "gui_cli_parity.json", parity)
    receipt = {
        "schema": "C11-D-D9.10-PRODUCER-BRIDGE-PLANNING-RECEIPT-V1",
        "phase": "D9.10",
        "result": "PASS_BRIDGE_PLANNING_ONLY",
        "status": result["status"],
        "request_id": request["request_id"],
        "request_hash": result["request_hash"],
        "editorial_hash": result["editorial_hash"],
        "plan_hash": result["plan_hash"],
        "bridge_record_hash": bridge["record_hash"],
        "gui_cli_parity": "PASS",
        "content_type": result["canonical_request"]["selection"]["content_type"],
        "selection": result["canonical_request"]["selection"],
        "renderer_execution": False,
        "production_execution": False,
        "release_authority": "NONE",
        "d4_8": "BLOCKED",
        "evidence_root": str(run_dir.relative_to(ROOT)).replace("/", "\\"),
    }
    _write_json(run_dir / "producer_universal_receipt.json", receipt)
    return result, bridge


def _reseal(receipt: dict[str, Any]) -> dict[str, Any]:
    item = copy.deepcopy(receipt)
    item.pop("receipt_sha256", None)
    item["receipt_sha256"] = sha256(item)
    return item


def _must_reject(label: str, receipt: dict[str, Any], *, reseal: bool = True) -> None:
    candidate = _reseal(receipt) if reseal else copy.deepcopy(receipt)
    try:
        validate_lifecycle_receipt(candidate, ROOT, verify_current=True)
    except (CrossSuiteLifecycleError, ValueError, KeyError, TypeError, OSError):
        return
    raise AssertionError(f"D9.13 negative case accepted: {label}")


def run_checks() -> dict[str, int]:
    config_module = _module("config_backend", "c11c-suite/c11c-config/c11d_config.py")
    rows, config_errors = config_module.validate_c11d_contracts(ROOT)
    assert not config_errors, config_errors
    assert any(row.get("id") == "D9_CROSS_SUITE_LIFECYCLE" for row in rows)
    manifest_path = ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    assert manifest_path.is_file(), "Historical C11-C freeze manifest is required and read-only"
    historical_hash_before = __import__("hashlib").sha256(manifest_path.read_bytes()).hexdigest()

    selections = _representative_selections()
    assert set(selections) == {"challenges", "visual_loops", "visual_drills"}
    base = ROOT / "artifacts/tests/c11d_d9/producer_universal"
    test_prefix = "D913-TEST-" + uuid.uuid4().hex[:10].upper()
    run_dirs: list[Path] = []
    life_ids: list[str] = []
    parity_cases = catalog_cases = maintenance_cases = 0
    all_negatives = 0
    try:
        for index, (content_type, selection) in enumerate(selections.items(), start=1):
            request_id = f"{test_prefix}-{content_type.upper()}"
            run_dir = base / request_id
            assert not run_dir.exists(), f"Refusing to overwrite existing evidence: {run_dir}"
            run_dir.mkdir(parents=True, exist_ok=False)
            run_dirs.append(run_dir)
            request = _raw(selection, request_id)
            result, bridge = _seed_evidence(request, run_dir)
            receipt = build_lifecycle_receipt(request, ROOT, run_dir)
            _write_json(run_dir / "cross_suite_lifecycle_receipt.json", receipt)
            validated = validate_lifecycle_receipt(receipt, ROOT, verify_current=True)
            assert validated["status"] == "PASS" and validated["stages"] == 5
            assert receipt["identity"]["gameplay_seed"] == 12345
            assert receipt["identity"]["music_seed"] == 840001
            assert receipt["identity"]["request_hash"] == result["request_hash"]
            assert receipt["identity"]["plan_hash"] == result["plan_hash"]
            assert receipt["identity"]["bridge_record_hash"] == bridge["record_hash"]
            assert len({stage["lifecycle_id"] for stage in receipt["stages"]}) == 1
            assert len({stage["identity_sha256"] for stage in receipt["stages"]}) == 1
            assert len({stage["binding_sha256"] for stage in receipt["stages"]}) == 1
            assert [stage["surface"] for stage in receipt["stages"]] == ["c11c-config", "c11c-producer", "c11c-test", "c11c-catalog", "c11c-maintenance"]
            assert receipt["governance"]["renderer_activation"] is False
            assert receipt["governance"]["production_execution"] is False
            assert receipt["media_created"] is False and receipt["release_authority"] == "NONE"
            life_ids.append(receipt["lifecycle_id"])
            parity_cases += 1

            catalog_backend = _module("catalog_backend", "c11c-suite/c11c-catalog/c11d_catalog.py")
            catalog_data = catalog_backend.build_catalog_data(ROOT)
            catalog_records = [row for row in catalog_data["records"] if row.get("lifecycle_id") == receipt["lifecycle_id"]]
            assert len(catalog_records) == 1, {"id": receipt["lifecycle_id"], "issues": catalog_data["issues"]}
            projected = catalog_records[0]
            assert projected["record_type"] == "CROSS_SUITE_LIFECYCLE_INTENT"
            assert projected["media_path"] is None and projected["media_sha256"] is None
            assert projected["release_authority"] == "NONE"
            catalog_cases += 1

            maintenance = _module("maintenance_backend", "tools/c11d/d9/maintenance.py")
            rel_receipt = (run_dir / "cross_suite_lifecycle_receipt.json").relative_to(ROOT).as_posix()
            audit = maintenance.audit_cross_suite_lifecycle(ROOT, rel_receipt)
            assert audit["status"] == "PASS" and audit["side_effects"]["files_moved"] is False
            assert audit["side_effects"]["files_deleted"] is False and audit["side_effects"]["media_created"] is False
            maintenance_cases += 1

            if index == 1:
                # Malformed seal, stage order, identity hash, cross-stage hash/value drift,
                # media/release overclaim, seed-source substitution, unsafe evidence path,
                # and changed current contracts must all fail closed.
                m = copy.deepcopy(receipt); m["receipt_sha256"] = "0" * 64
                _must_reject("receipt checksum", m, reseal=False); all_negatives += 1
                m = copy.deepcopy(receipt); m["stages"][0], m["stages"][1] = m["stages"][1], m["stages"][0]
                _must_reject("stage reorder", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["identity"]["music_seed"] += 1
                _must_reject("identity hash drift", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["identity"]["music_seed"] += 1
                m["identity_sha256"] = sha256(m["identity"])
                binding = {key: m["identity"][key] for key in ("gameplay_seed", "music_seed", "delivery_profile_id", "resolved_delivery_profile_id", "presentation_profile_id", "audio_enabled", "personalization_enabled")}
                m["binding_sha256"] = sha256(binding)
                for stage in m["stages"]:
                    stage["identity_sha256"] = m["identity_sha256"]
                    stage["binding_sha256"] = m["binding_sha256"]
                _must_reject("resealed cross-domain seed substitution", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["stages"][1]["identity_sha256"] = "0" * 64
                _must_reject("stage identity drift", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["stages"][1]["evidence"]["music_seed_source"] = "canonical_request.seed"
                _must_reject("music seed source substitution", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["media_created"] = True
                _must_reject("media overclaim", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["release_authority"] = "AUTHORIZED"
                _must_reject("release overclaim", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["stages"][3]["evidence"]["projection_sha256"] = "0" * 64
                _must_reject("catalog projection hash drift", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["evidence"]["producer_evidence_directory"] = "artifacts/tests/../../release"
                _must_reject("evidence path traversal", m); all_negatives += 1
                m = copy.deepcopy(receipt); m["stages"][4]["evidence"]["side_effects"]["files_deleted"] = True
                _must_reject("maintenance side-effect overclaim", m); all_negatives += 1
                bad_request = copy.deepcopy(request); bad_request["selection"] = {"content_type": "longform", "family_id": "any", "variant_id": "longform"}
                try:
                    _module("producer_negative", "tools/c11d/d9/universal_producer.py").evaluate_universal_request(bad_request, ROOT)
                except Exception:
                    pass
                else:
                    raise AssertionError("Unsupported Longform request was accepted")
                all_negatives += 1
        assert len(set(life_ids)) == 3, "Each distinct request must have a distinct lifecycle identity"
    finally:
        for path in run_dirs:
            shutil.rmtree(path, ignore_errors=True)

    historical_hash_after = __import__("hashlib").sha256(manifest_path.read_bytes()).hexdigest()
    assert historical_hash_after == historical_hash_before, "D9.13 must not mutate historical C11-C manifest"
    assert parity_cases == catalog_cases == maintenance_cases == 3
    assert all_negatives == 12
    return {"content_types": 3, "stages": 5, "parity": parity_cases, "catalog": catalog_cases, "maintenance": maintenance_cases, "negative": all_negatives}


if __name__ == "__main__":
    counts = run_checks()
    print(
        "C11-D D9.13 CROSS-SUITE LIFECYCLE PASS | "
        f"content_types={counts['content_types']}/3 | stages={counts['stages']}/5 | "
        f"identity_continuity=PASS | GUI/CLI parity={counts['parity']}/3 | "
        f"catalog_projection={counts['catalog']}/3 | maintenance_audit={counts['maintenance']}/3 | "
        f"negative={counts['negative']}/{counts['negative']} | renderer=OFF | media_created=false | release_authority=NONE"
    )
