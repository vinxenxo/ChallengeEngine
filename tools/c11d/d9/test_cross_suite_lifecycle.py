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
    _validate_persisted_gui_cli_parity_receipt,
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
    adapter_backend = _module("adapter_backend", "tools/c11d/d9/d_render_adapter.py")
    adapter = adapter_backend.prepare_d_only_adapter_envelope(result, bridge, ROOT)
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
        "d_only_adapter_envelope_equal": adapter == cli_result.get("d_only_adapter_envelope"),
    }
    if not all(parity_checks.values()):
        raise AssertionError(f"GUI/CLI semantic parity failed: {parity_checks}")
    parity = {
        "schema": "C11-D-D9.10-UNIVERSAL-GUI-CLI-ADAPTER-PARITY-V1",
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
        "d_only_adapter_envelope_hash": adapter["envelope_hash"],
        "cli_d_only_adapter_envelope_hash": cli_result["d_only_adapter_envelope"]["envelope_hash"],
        "d_only_adapter_prepare_invoked": True,
        "renderer_input_emitted": False,
        "renderer": False,
        "production_execution": False,
        "release_authority": "NONE",
    }
    _write_json(run_dir / "canonical_request.json", result["canonical_request"])
    _write_json(run_dir / "editorial_resolution.json", result["editorial_resolution"])
    _write_json(run_dir / "universal_plan.json", result["plan"])
    _write_json(run_dir / "editorial_render_bridge_plan.json", bridge)
    _write_json(run_dir / "d_render_adapter_envelope.json", adapter)
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
        "d_only_adapter_envelope_hash": adapter["envelope_hash"],
        "d_only_adapter_status": adapter["status"],
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


def run_parity_receipt_contract_regressions() -> int:
    """Exercise the persisted parity schema regression independently of Qt/runtime artifacts."""
    adapter_hash = "3" * 64
    valid = {
        "schema": "C11-D-D9.10-UNIVERSAL-GUI-CLI-ADAPTER-PARITY-V1",
        "status": "PASS",
        "checks": {
            "canonical_request_equal": True,
            "request_hash_equal": True,
            "editorial_hash_equal": True,
            "plan_equal": True,
            "plan_hash_equal": True,
            "bridge_planning_record_equal": True,
            "d_only_adapter_envelope_equal": True,
        },
        "gui_plan_hash": "1" * 64,
        "bridge_record_hash": "2" * 64,
        "d_only_adapter_envelope_hash": adapter_hash,
        "cli_d_only_adapter_envelope_hash": adapter_hash,
    }
    producer_receipt = {"d_only_adapter_envelope_hash": adapter_hash}
    _validate_persisted_gui_cli_parity_receipt(
        valid, producer_receipt, expected_plan_hash="1" * 64, expected_bridge_record_hash="2" * 64
    )

    negatives = 0
    def must_reject(label: str, parity: dict[str, Any], receipt: dict[str, Any] = producer_receipt) -> None:
        nonlocal negatives
        try:
            _validate_persisted_gui_cli_parity_receipt(
                parity, receipt, expected_plan_hash="1" * 64, expected_bridge_record_hash="2" * 64
            )
        except CrossSuiteLifecycleError:
            negatives += 1
            return
        raise AssertionError(f"D9.13 accepted invalid persisted parity receipt: {label}")

    missing_adapter_check = copy.deepcopy(valid)
    missing_adapter_check["checks"].pop("d_only_adapter_envelope_equal")
    must_reject("missing D9.10 adapter parity check", missing_adapter_check)

    false_adapter_check = copy.deepcopy(valid)
    false_adapter_check["checks"]["d_only_adapter_envelope_equal"] = False
    must_reject("false D9.10 adapter parity check", false_adapter_check)

    mismatched_cli_hash = copy.deepcopy(valid)
    mismatched_cli_hash["cli_d_only_adapter_envelope_hash"] = "4" * 64
    must_reject("GUI/CLI adapter envelope hash mismatch", mismatched_cli_hash)

    mismatched_producer_hash = {"d_only_adapter_envelope_hash": "5" * 64}
    must_reject("Producer receipt adapter hash mismatch", copy.deepcopy(valid), mismatched_producer_hash)
    return negatives


def run_checks() -> dict[str, int]:
    parity_receipt_regressions = run_parity_receipt_contract_regressions()
    assert parity_receipt_regressions == 4
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
                # Regression for the D9.10 Qt failure: the Producer GUI now persists
                # seven parity checks, including D-only adapter envelope parity. A
                # missing or false adapter check must still fail closed.
                parity_path = run_dir / "gui_cli_parity.json"
                valid_parity = json.loads(parity_path.read_text(encoding="utf-8"))
                for label, mutation in (
                    ("persisted adapter parity check missing", lambda candidate: candidate["checks"].pop("d_only_adapter_envelope_equal")),
                    ("persisted adapter parity check false", lambda candidate: candidate["checks"].__setitem__("d_only_adapter_envelope_equal", False)),
                ):
                    candidate = copy.deepcopy(valid_parity)
                    mutation(candidate)
                    _write_json(parity_path, candidate)
                    try:
                        build_lifecycle_receipt(request, ROOT, run_dir)
                    except CrossSuiteLifecycleError as exc:
                        if str(exc) != "Persisted GUI/CLI parity receipt is not a complete PASS":
                            raise AssertionError(
                                f"{label} was rejected by the wrong guard: {exc}"
                            ) from exc
                        all_negatives += 1
                    else:
                        raise AssertionError(f"D9.13 accepted incomplete adapter parity evidence: {label}")
                    finally:
                        _write_json(parity_path, valid_parity)

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
    assert all_negatives == 14
    return {"content_types": 3, "stages": 5, "parity": parity_cases, "catalog": catalog_cases, "maintenance": maintenance_cases, "negative": all_negatives, "parity_receipt_regressions": parity_receipt_regressions}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parity-contract-only", action="store_true", help="run the focused D9.10/D9.13 persisted parity receipt regression checks")
    args = parser.parse_args()
    if args.parity_contract_only:
        negatives = run_parity_receipt_contract_regressions()
        assert negatives == 4
        print(f"C11-D D9.10/D9.13 PERSISTED PARITY RECEIPT REGRESSION PASS | positive=1/1 | negative={negatives}/{negatives}")
        raise SystemExit(0)
    counts = run_checks()
    print(
        "C11-D D9.13 CROSS-SUITE LIFECYCLE PASS | "
        f"content_types={counts['content_types']}/3 | stages={counts['stages']}/5 | "
        f"identity_continuity=PASS | GUI/CLI parity={counts['parity']}/3 | "
        f"catalog_projection={counts['catalog']}/3 | maintenance_audit={counts['maintenance']}/3 | "
        f"negative={counts['negative']}/{counts['negative']} | persisted_parity_regression={counts['parity_receipt_regressions']}/{counts['parity_receipt_regressions']} | renderer=OFF | media_created=false | release_authority=NONE"
    )
