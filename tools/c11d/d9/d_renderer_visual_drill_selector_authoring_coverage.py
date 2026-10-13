"""Source-pinned, stdout-only Godot audit of canonical Visual Drill type/tier authoring coverage.

This probes the existing D/C11 authoring adapter only. It is intentionally not a second
request/payload binder and does not assert dynamic-manifest acceptance or renderer readiness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_SCHEMA_V1.json")
HARNESS_REL = Path("tools/c11d/d9/audit_visual_drill_selector_authoring_coverage.gd")
CONTRACT_ID = "C11-D-D9-VISUAL-DRILL-SELECTOR-AUTHORING-COVERAGE-CONTRACT-V1"
REPORT_ID = "C11-D-D9-VISUAL-DRILL-SELECTOR-AUTHORING-COVERAGE-V1"
RUNTIME_ID = "C11-D-D9-VISUAL-DRILL-SELECTOR-AUTHORING-COVERAGE-RUNTIME-V1"
STATUS = "PREPARATION_ONLY_AUTHORIZING_ADAPTER_CAPABILITY_AUDIT_NOT_DYNAMIC_PAYLOAD_BINDING_OR_RENDERER_INPUT"
RUNTIME_STATUS = "PREPARATION_ONLY_AUTHORING_ADAPTER_CAPABILITY_AUDIT_NOT_DYNAMIC_PAYLOAD_BINDING_OR_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT_VERSION = "4.7.1.stable.mono.official.a13da4feb"
EXPECTED_FAMILIES = ["peripheral_scan", "pursuit", "saccade", "tracking"]
EXPECTED_TIERS = [1, 2, 3, 4, 5]
EXPECTED_BOUNDARY = {
    "scope": "AUTHORING_ADAPTER_CAPABILITY_ONLY_NOT_REQUEST_BOUND_PAYLOAD_BINDING",
    "request_bound_payload_manifest_created": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": "OFF",
    "production_execution": False,
    "media_created": False,
    "c11c_source_mutation": False,
    "d4_8": "BLOCKED",
    "release_authority": "NONE",
    "baseline_approval": "MISSING",
    "freeze_eligible": False,
}
RECEIPT_PREFIX = "C11-D VISUAL DRILL AUTHORING COVERAGE RECEIPT="
SUMMARY_PREFIX = "C11-D VISUAL DRILL AUTHORING COVERAGE SUMMARY="

class VisualDrillCoverageError(ValueError):
    """Raised when canonical sources, policy identity, or runtime evidence drift."""

def _root(root: Path | str | None = None) -> Path:
    return Path(root).resolve() if root is not None else ROOT

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("ascii")).hexdigest()

def _sha_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise VisualDrillCoverageError(f"Cannot hash source {path}: {exc}") from exc

def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise VisualDrillCoverageError(f"Cannot parse JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise VisualDrillCoverageError(f"Expected JSON object: {path}")
    return value

def _validate_contract_sources(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise VisualDrillCoverageError("Coverage contract identity/version mismatch")
    if contract.get("status") != STATUS:
        raise VisualDrillCoverageError("Coverage contract may not claim dynamic binding or renderer input")
    if contract.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA:
        raise VisualDrillCoverageError("Frozen C11-C manifest pin mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:visual-drill-selector-authoring-coverage:v1" or schema.get("additionalProperties") is not False:
        raise VisualDrillCoverageError("Coverage report schema identity/strictness mismatch")
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
    except ImportError:
        pass
    except Exception as exc:
        raise VisualDrillCoverageError(f"Coverage schema is invalid: {exc}") from exc
    matrix = contract.get("selector_matrix")
    if matrix != {
        "content_type": "visual_drills",
        "family_ids": EXPECTED_FAMILIES,
        "tiers": EXPECTED_TIERS,
        "expected_selector_count": 20,
        "authoring_domain_family": "visual_drill",
        "request_bound_payload_manifest": "NOT_TESTED_BY_THIS_AUDIT",
    }:
        raise VisualDrillCoverageError("Selector matrix exceeds or differs from the fixed canonical V1 scope")
    if contract.get("governance_locks") != EXPECTED_BOUNDARY:
        raise VisualDrillCoverageError("Coverage contract attempted to change governance boundaries")
    rows = contract.get("source_lineage")
    if not isinstance(rows, list) or len(rows) != 24:
        raise VisualDrillCoverageError("Expected the exact 24-source authoring capability lineage")
    seen: set[str] = set()
    lineage: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise VisualDrillCoverageError("Malformed source lineage row")
        rel, digest = row.get("path"), row.get("sha256")
        if not isinstance(rel, str) or not rel or "\\" in rel or rel.startswith("/") or any(part in ("", ".", "..") for part in rel.split("/")):
            raise VisualDrillCoverageError(f"Unsafe source path: {rel!r}")
        if rel in seen or not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise VisualDrillCoverageError(f"Duplicate path or malformed SHA-256: {rel}")
        if index == 0:
            if rel != "release/C11C_FREEZE_PACKAGE_MANIFEST.json" or digest != EXPECTED_MANIFEST_SHA:
                raise VisualDrillCoverageError("Frozen C11-C manifest must be the first exact source pin")
        elif index > 1 and rel <= lineage[-1]["path"]:
            raise VisualDrillCoverageError("Source pins must be lexicographically sorted after the frozen manifest")
        source_path = root / rel
        actual = _sha_file(source_path)
        if actual != digest:
            raise VisualDrillCoverageError(f"Pinned source drift: {rel}")
        seen.add(rel)
        lineage.append({"path": rel, "sha256": actual})
    required = {
        "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
        "c11c-suite/c11c-producer/producer_schema.json",
        "tools/c11d/d9/universal_editorial_model.py",
        "core/authoring/VisualAuthoringGenerator.gd",
        "core/authoring/VisualAuthoringRequest.gd",
        "core/authoring/VisualAuthoringAssemblyContext.gd",
        "core/authoring/VisualAuthoringRegistry.gd",
        "core/authoring/VisualAuthoringPolicyRegistry.gd",
        "core/authoring/VisualDifficultyResolver.gd",
        "core/authoring/VisualDrillSeedVariation.gd",
        "core/authoring/adapters/VisualDrillAuthoringAdapter.gd",
        HARNESS_REL.as_posix(), Path("tools/c11d/d9/d_renderer_visual_drill_selector_authoring_coverage.py").as_posix(),
        Path("tools/c11d/d9/test_d_renderer_visual_drill_selector_authoring_coverage.py").as_posix(),
        SCHEMA_REL.as_posix(),
    }
    for family in EXPECTED_FAMILIES:
        required.add(f"definitions/visual_drill_{family}_canonical.json")
        required.add(f"profiles/difficulty/visual_drill_{family}.json")
    if seen - {"release/C11C_FREEZE_PACKAGE_MANIFEST.json"} != required:
        raise VisualDrillCoverageError(f"Coverage source-lineage set differs from the exact upstream authoring surface; extra={sorted((seen - {"release/C11C_FREEZE_PACKAGE_MANIFEST.json"})-required)} missing={sorted(required-(seen - {"release/C11C_FREEZE_PACKAGE_MANIFEST.json"}))}")
    return contract, schema, lineage

def _canonical_catalog(root: Path, contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    d9_tools = root / "tools/c11d/d9"
    if str(d9_tools) not in sys.path:
        sys.path.insert(0, str(d9_tools))
    try:
        from universal_editorial_model import build_catalog
        catalog = build_catalog(root)
    except Exception as exc:
        raise VisualDrillCoverageError(f"Canonical D9.8 catalog failed: {exc}") from exc
    drill_info = catalog.get("content_types", {}).get("visual_drills", {})
    raw_families = drill_info.get("families")
    if not isinstance(raw_families, list):
        raise VisualDrillCoverageError("Canonical Visual Drill family inventory is missing")
    actual_families = sorted(str(item.get("id", "")) for item in raw_families if isinstance(item, dict))
    if actual_families != EXPECTED_FAMILIES:
        raise VisualDrillCoverageError(f"Canonical drill family catalog drift: {actual_families}")
    matrix_rows: list[dict[str, Any]] = []
    for family in EXPECTED_FAMILIES:
        raw_family = next((item for item in raw_families if item.get("id") == family), None)
        if not isinstance(raw_family, dict):
            raise VisualDrillCoverageError(f"Canonical selector family missing: {family}")
        selectors = raw_family.get("variants")
        if not isinstance(selectors, list) or [row.get("id") for row in selectors if isinstance(row, dict)] != [f"tier-{tier}" for tier in EXPECTED_TIERS]:
            raise VisualDrillCoverageError(f"Canonical tier selector inventory differs for {family}")
        canonical_rel = f"definitions/visual_drill_{family}_canonical.json"
        policy_rel = f"profiles/difficulty/visual_drill_{family}.json"
        canonical = _read_json(root / canonical_rel)
        policy = _read_json(root / policy_rel)
        if canonical.get("subtype") != family or policy.get("subtype") != family:
            raise VisualDrillCoverageError(f"Canonical/policy subtype identity mismatch: {family}")
        payload = canonical.get("payload", {})
        duration, fps, frames = payload.get("duration"), payload.get("fps"), payload.get("frame_count")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration <= 0 or fps != 30 or frames != round(duration * fps):
            raise VisualDrillCoverageError(f"Canonical timing triplet inconsistent: {family}")
        policy_tiers = policy.get("tiers")
        if not isinstance(policy_tiers, dict) or sorted(policy_tiers) != [str(tier) for tier in EXPECTED_TIERS]:
            raise VisualDrillCoverageError(f"Difficulty policy does not define exact tier 1..5 coverage: {family}")
        for tier in EXPECTED_TIERS:
            matrix_rows.append({
                "selection": {"content_type":"visual_drills", "family_id":family, "subtype_id":None, "variant_id":f"tier-{tier}"},
                "canonical_source_path":canonical_rel,
                "canonical_source_sha256":_sha_file(root / canonical_rel),
                "difficulty_policy_path":policy_rel,
                "difficulty_policy_sha256":_sha_file(root / policy_rel),
                "canonical_duration_seconds":float(duration),
                "fps":30,
                "frame_count":int(frames),
            })
    if len(matrix_rows) != 20:
        raise VisualDrillCoverageError("Canonical selector matrix count is not 20")
    return matrix_rows

def _validate_runtime_receipts(receipts: list[dict[str, Any]], expected_matrix: list[dict[str, Any]], source_lineage_sha256: str) -> dict[str, int]:
    if len(receipts) != 20:
        raise VisualDrillCoverageError(f"Expected 20 selector receipts, received {len(receipts)}")
    expected_by_key = {(r["selection"]["family_id"], r["selection"]["variant_id"]): r for r in expected_matrix}
    seen: set[tuple[str, str]] = set()
    for row in receipts:
        if not isinstance(row, dict):
            raise VisualDrillCoverageError("Runtime receipt must be a JSON object")
        selection = row.get("selection")
        if not isinstance(selection, dict):
            raise VisualDrillCoverageError("Runtime receipt lacks selector identity")
        key = (selection.get("family_id"), selection.get("variant_id"))
        if key not in expected_by_key or key in seen:
            raise VisualDrillCoverageError(f"Unknown or duplicate selector receipt: {key}")
        seen.add(key)
        expected = expected_by_key[key]
        for field in ("selection", "canonical_source_path", "canonical_source_sha256", "difficulty_policy_path", "difficulty_policy_sha256", "canonical_duration_seconds", "fps", "frame_count"):
            if row.get(field) != expected[field]:
                raise VisualDrillCoverageError(f"Runtime receipt disagrees with canonical source at {key}: {field}")
        if row.get("base_seed") != 12345 or row.get("alternate_seed") != 54321:
            raise VisualDrillCoverageError(f"Unexpected seed pair in receipt: {key}")
        digest_fields = ("payload_sha256", "repeat_payload_sha256", "alternate_seed_payload_sha256", "visual_state_sha256", "repeat_visual_state_sha256", "alternate_seed_visual_state_sha256")
        for field in digest_fields:
            if not isinstance(row.get(field), str) or re.fullmatch(r"[0-9a-f]{64}", row[field]) is None:
                raise VisualDrillCoverageError(f"Malformed runtime digest {field}: {key}")
        if row["payload_sha256"] != row["repeat_payload_sha256"] or row["visual_state_sha256"] != row["repeat_visual_state_sha256"] or row["payload_sha256"] == row["alternate_seed_payload_sha256"] or row["visual_state_sha256"] == row["alternate_seed_visual_state_sha256"]:
            raise VisualDrillCoverageError(f"Determinism or seed-variation evidence failed: {key}")
        for field in ("deterministic_repeat_pass", "visual_seed_change_observed", "selection_identity_matches", "policy_tier_resolved"):
            if row.get(field) is not True:
                raise VisualDrillCoverageError(f"Runtime receipt did not pass {field}: {key}")
    if seen != set(expected_by_key):
        raise VisualDrillCoverageError("Runtime receipt matrix is incomplete")
    return {"cases":20,"families":4,"deterministic_repeat":20,"visual_seed_change":20,"identity_match":20,"policy_tier_resolved":20}

def _build_report(contract: Mapping[str, Any], lineage: list[dict[str, str]], matrix: list[dict[str, Any]], receipts: list[dict[str, Any]], schema: Mapping[str, Any]) -> dict[str, Any]:
    stats = _validate_runtime_receipts(receipts, matrix, _sha_json(lineage))
    rows = []
    for expected in matrix:
        key = (expected["selection"]["family_id"], expected["selection"]["variant_id"])
        found = next(row for row in receipts if (row["selection"]["family_id"], row["selection"]["variant_id"]) == key)
        rows.append({**expected, **{k:found[k] for k in (
            "base_seed","alternate_seed","payload_sha256","repeat_payload_sha256","alternate_seed_payload_sha256",
            "visual_state_sha256","repeat_visual_state_sha256","alternate_seed_visual_state_sha256",
            "deterministic_repeat_pass","visual_seed_change_observed","selection_identity_matches","policy_tier_resolved")}})
    report: dict[str, Any] = {
        "schema":REPORT_ID,
        "schema_version":"1.0",
        "status":RUNTIME_STATUS,
        "frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA,
        "source_lineage":lineage,
        "source_lineage_sha256":_sha_json(lineage),
        "catalog_summary":{
            "content_type":"visual_drills","family_count":4,"selector_count":20,
            "family_ids":EXPECTED_FAMILIES,"tiers":EXPECTED_TIERS,
            "authoring_adapter_coverage":"20_OF_20_VERIFIED_BY_REAL_GODOT_RUNTIME",
            "dynamic_request_payload_binding":"NOT_COVERED_BY_THIS_AUDIT",
            "renderer_input_emitted":False,
        },
        "coverage_matrix":rows,
        "governance":dict(EXPECTED_BOUNDARY),
    }
    report["report_sha256"] = _sha_json(report)
    try:
        import jsonschema
        jsonschema.Draft202012Validator(schema).validate(report)
    except ImportError:
        required = set(schema.get("required", []))
        if required - set(report):
            raise VisualDrillCoverageError("Report failed schema fallback")
    except Exception as exc:
        detail = getattr(exc, "message", str(exc))
        raise VisualDrillCoverageError(f"Coverage report schema validation failed: {detail}") from exc
    if report["report_sha256"] != _sha_json({k:v for k,v in report.items() if k != "report_sha256"}):
        raise VisualDrillCoverageError("Report self-hash mismatch")
    return report

def run_coverage_audit(godot: str, timeout: int = 120, project_root: Path | str | None = None, process_runner: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, lineage = _validate_contract_sources(root)
    matrix = _canonical_catalog(root, contract)
    if not godot or not Path(godot).is_file():
        raise VisualDrillCoverageError("Godot 4.7.1 executable is missing")
    try:
        completed = process_runner([godot,"--version"],cwd=str(root),text=True,capture_output=True,timeout=min(timeout,30),check=False)
        version = str(getattr(completed,"stdout","") or "").strip()
        if int(getattr(completed,"returncode",-1)) != 0 or version != EXPECTED_GODOT_VERSION:
            raise VisualDrillCoverageError(f"Godot version mismatch: {version!r}")
        command = [godot,"--headless","--path",str(root),"--script","res://"+HARNESS_REL.as_posix()]
        completed = process_runner(command,cwd=str(root),text=True,capture_output=True,timeout=timeout,check=False)
    except VisualDrillCoverageError:
        raise
    except Exception as exc:
        raise VisualDrillCoverageError(f"Godot authoring coverage harness invocation failed: {exc}") from exc
    stdout = str(getattr(completed,"stdout","") or "")
    stderr = str(getattr(completed,"stderr","") or "")
    combined = stdout + "\n" + stderr
    if int(getattr(completed,"returncode",-1)) != 0:
        raise VisualDrillCoverageError(f"Godot harness failed: {combined[-5000:]}")
    if any(marker in combined for marker in ("SCRIPT ERROR:","Parse Error:","Invalid call.","VISUAL DRILL SELECTOR AUTHORING COVERAGE FAIL")):
        raise VisualDrillCoverageError(f"Godot harness emitted an error marker: {combined[-5000:]}")
    receipt_lines = [line[len(RECEIPT_PREFIX):] for line in combined.splitlines() if line.startswith(RECEIPT_PREFIX)]
    summary_lines = [line[len(SUMMARY_PREFIX):] for line in combined.splitlines() if line.startswith(SUMMARY_PREFIX)]
    pass_lines = [line for line in combined.splitlines() if line.startswith("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE PASS")]
    if len(receipt_lines) != 20 or len(summary_lines) != 1 or len(pass_lines) != 1:
        raise VisualDrillCoverageError(f"Expected 20 selector receipts, one summary and one PASS line. Receipts={len(receipt_lines)} summaries={len(summary_lines)} pass_lines={len(pass_lines)}")
    try:
        receipts = [json.loads(row) for row in receipt_lines]
        runtime_summary = json.loads(summary_lines[0])
    except json.JSONDecodeError as exc:
        raise VisualDrillCoverageError("Godot stdout receipt/summary is invalid JSON") from exc
    expected_runtime = {
        "schema":RUNTIME_ID,"schema_version":"1.0","status":RUNTIME_STATUS,
        "frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA,"source_lineage_sha256":_sha_json(lineage),
        "family_count":4,"selector_count":20,"deterministic_repeat":20,"visual_seed_change":20,
        "identity_match":20,"policy_tier_resolved":20,"governance":EXPECTED_BOUNDARY,
    }
    if runtime_summary != expected_runtime:
        raise VisualDrillCoverageError("Godot runtime summary contradicts expected coverage/governance")
    report = _build_report(contract,lineage,matrix,receipts,schema)
    return report

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE", ""), help="Godot 4.7.1 Mono executable")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout in seconds for the single 20-selector Godot harness")
    parser.add_argument("--root", default=str(ROOT), help="Project root; default is this checkout")
    parser.add_argument("--contract-only", action="store_true", help="Validate pins, canonical selector matrix and schema without Godot runtime (not acceptance)")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    try:
        contract,schema,lineage = _validate_contract_sources(root)
        matrix = _canonical_catalog(root,contract)
        if args.contract_only:
            print(f"C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE CONTRACT PASS | source_pins={len(lineage)}/{len(lineage)} | canonical_selectors={len(matrix)}/20 | authoring_runtime=NOT_RUN | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
            return 0
        report = run_coverage_audit(args.godot,args.timeout,root,subprocess.run)
        for row in report["coverage_matrix"]:
            print("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE VERIFIED=" + json.dumps(row,ensure_ascii=True,sort_keys=True,separators=(",",":")))
        print("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE REPORT=" + json.dumps(report,ensure_ascii=True,sort_keys=True,separators=(",",":")))
        print("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE PASS | families=4/4 | selectors=20/20 | deterministic_repeat=20/20 | visual_seed_change=20/20 | identity=20/20 | policy_tier=20/20 | source_pins=%d/%d | report_sha256=%s | dynamic_request_manifest=NOT_TESTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % (len(lineage),len(lineage),report["report_sha256"]))
        return 0
    except Exception as exc:
        print(f"C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE",file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
