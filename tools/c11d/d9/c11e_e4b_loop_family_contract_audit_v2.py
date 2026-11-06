from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import c11e_e4b_loop_family_contract_audit as legacy

SCHEMA = "C11E-E4B-LOOP-FAMILY-CONTRACT-AUDIT-V2"
STATUS = "PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY"

class AuditV2Error(RuntimeError):
    pass


def count_mp4_presence(selectors: Sequence[Mapping[str, Any]]) -> int:
    """Count file-presence observations; this is never a visual-acceptance gate."""
    if not isinstance(selectors, (list, tuple)):
        raise AuditV2Error("Historical selector coverage must be a sequence")
    count = 0
    for index, row in enumerate(selectors):
        if not isinstance(row, Mapping):
            raise AuditV2Error(f"Malformed historical selector row: {index}")
        value = row.get("mp4_present_in_project_root")
        if type(value) is not bool:
            raise AuditV2Error(f"MP4 presence must be an explicit boolean: row {index}")
        count += int(value)
    return count


def validate_mp4_presence_observation(coverage: Mapping[str, Any]) -> int:
    selectors = coverage.get("selectors")
    count = count_mp4_presence(selectors)
    declared = coverage.get("mp4_present_in_project_root_count")
    if type(declared) is not int or declared != count:
        raise AuditV2Error("MP4 presence summary does not match per-selector file observations")
    selector_count = coverage.get("selector_count")
    if type(selector_count) is not int or selector_count != len(selectors):
        raise AuditV2Error("Historical selector count does not match selector rows")
    if not 0 <= count <= selector_count:
        raise AuditV2Error("MP4 presence count is outside the observed selector range")
    if coverage.get("visual_review_performed") is not False:
        raise AuditV2Error("File presence must not be represented as visual review")
    return count


def build_report(project_root: str | Path) -> dict[str, Any]:
    report = legacy.build_report(project_root)
    old_report_hash = report.get("report_sha256")
    report["schema"] = SCHEMA
    report["audit_target"] = "ACTIVE_CHECKOUT_PROJECT_ROOT"
    report["source_snapshot_sha256"] = report.pop("project_snapshot_sha256", None)
    report["legacy_v1_report_sha256"] = old_report_hash
    coverage = report["historical_product_coverage"]
    for row in coverage.get("selectors", []):
        if "mp4_present_in_snapshot" in row:
            row["mp4_present_in_project_root"] = row.pop("mp4_present_in_snapshot")
    old_count = coverage.pop("mp4_present_in_snapshot_count", None)
    coverage["mp4_present_in_project_root_count"] = count_mp4_presence(coverage.get("selectors", []))
    if old_count != coverage["mp4_present_in_project_root_count"]:
        raise AuditV2Error("Legacy MP4 count and per-selector file observations disagree")
    coverage["evidence_scope"] = "HISTORICAL_MANIFEST_AUTHORING_AND_ACTIVE_CHECKOUT_FILE_EXISTENCE_ONLY_NO_MP4_VISUAL_REVIEW"
    coverage["visual_review_performed"] = False
    report["report_sha256"] = legacy.canonical_hash(report)
    validate_mp4_presence_observation(coverage)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-E E4B Loop active-checkout audit with observational MP4 inventory")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    report = build_report(args.project_root)
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(raw)
    Path(str(output) + ".sha256").write_text(legacy.sha256_bytes(raw) + "  " + output.name + "\n", encoding="ascii")
    coverage = report["historical_product_coverage"]
    print("C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT=" + report["status"])
    print("DECISIONS=" + str(report["operator_decisions"]["decision_count"]) + "/5")
    print("FAMILIES=" + str(report["family_interface_audit"]["family_count"]) + "; GRAMMARS=" + str(report["family_interface_audit"]["grammar_count"]))
    print("HISTORICAL_MANIFEST_AUTHORING=" + coverage["manifest_authoring_pairs"])
    print("MP4_FILES_PRESENT_IN_ACTIVE_CHECKOUT=" + str(coverage["mp4_present_in_project_root_count"]) + "/" + str(coverage["selector_count"]) + "; VISUAL_REVIEW=NOT_PERFORMED")
    print("D98_COMPATIBILITY=" + report["d98_d99_semantics"]["d98_request_plan_compatibility_metadata"] + "; D99=PLAN_ONLY")
    print("RENDERER=OFF; MEDIA=FALSE; D4.8=BLOCKED; RELEASE_AUTHORITY=NONE")
    print("REPORT_SHA256=" + legacy.sha256_bytes(raw))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (legacy.AuditError, AuditV2Error) as exc:
        print("C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT=FAIL")
        print("ERROR=" + str(exc))
        raise SystemExit(2)
