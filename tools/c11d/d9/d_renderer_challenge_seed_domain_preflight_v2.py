from __future__ import annotations

"""Source-pinned Challenge seed-domain planner preflight; no Godot/payload execution."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402
import universal_editorial_model as editorial  # noqa: E402
import universal_producer as planner  # noqa: E402

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2_SCHEMA.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2_REPORT_SCHEMA.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_CONTRACT_SHA256 = "fc09a92e1f16afd4409a6a161385d1c3bca7925bb7e9d43249944fcc6d195799"
EXPECTED_SCHEMA_SHA256 = "86dc601bd29e1eee4d9c123d77e9a133ccacc5f97ef0718ee27d115f0b3db695"
EXPECTED_REPORT_SCHEMA_SHA256 = "2aac148bea46253312dfb84ee2b2e23c78893b43ba2bd3e518a3569e18ea9086"
CONTRACT_ID = "C11-D-D9-CHALLENGE-SEED-DOMAIN-PREFLIGHT-CONTRACT-V2"
SCHEMA_ID = "urn:c11d:challenge-seed-domain-preflight:v2"
REPORT_SCHEMA_ID = "urn:c11d:challenge-seed-domain-preflight-report:v2"
STATUS = "PREPARATION_ONLY_CANONICAL_CHALLENGE_PLANNING_PREFLIGHT_NO_PAYLOAD_MATERIALIZATION_NOT_INPUT_ADMISSION"
REPORT_PREFIX = "C11D_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2_REPORT="
SEED_VARIANTS = {
    "BASELINE": {"seed": 12345, "music_seed": 840001},
    "GAMEPLAY_SEED_ONLY_CHANGED": {"seed": 54321, "music_seed": 840001},
    "MUSIC_SEED_ONLY_CHANGED": {"seed": 12345, "music_seed": 840002},
}
CHALLENGE_IDS = tuple(f"CHALLENGE_{i:03d}" for i in range(1, 10))
EXPECTED_PIN_PATHS = tuple(sorted((
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json",
    "tools/c11d/d9/universal_producer.py",
    "tools/c11d/d9/universal_editorial_model.py",
    "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py",
    "definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json",
    "profiles/delivery/c11c_video_delivery_profiles.json",
    "c11c-suite/c11c-producer/c11d_gui_request.py",
    *(f"challenges/{cid}.json" for cid in CHALLENGE_IDS),
)))
PIN_ROLES = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "IMMUTABLE_C11C_MANIFEST",
    "tools/c11d/d9/universal_producer.py": "CANONICAL_D9_9_UNIVERSAL_PLANNER",
    "tools/c11d/d9/universal_editorial_model.py": "CANONICAL_UNIVERSAL_EDITORIAL_SELECTOR_RESOLVER",
    "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py": "CANONICAL_V1_BASE_REQUEST_HELPER_ONLY_SELECTOR_MATRIX_NOT_INVOLVED",
    "definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json": "CANONICAL_D9_9_REQUEST_SCHEMA",
    "profiles/delivery/c11c_video_delivery_profiles.json": "CANONICAL_DELIVERY_PROFILE_REGISTRY",
    "c11c-suite/c11c-producer/c11d_gui_request.py": "CANONICAL_D4_CHALLENGE_GUI_CLI_PARITY_ADAPTER",
}
for _cid in CHALLENGE_IDS:
    PIN_ROLES[f"challenges/{_cid}.json"] = "CANONICAL_CHALLENGE_DEFINITION_" + _cid

class PreflightError(RuntimeError):
    """Canonical Challenge planning matrix is stale, incomplete or non-deterministic."""


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_json(value: Any) -> str:
    return _sha_bytes(_canonical(value).encode("utf-8"))


def _sha_file(path: Path) -> str:
    if not path.is_file():
        raise PreflightError(f"Pinned source missing: {path}")
    return _sha_bytes(path.read_bytes())


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreflightError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PreflightError(f"Expected JSON object: {path}")
    return value


def _load_and_validate_contract(root: Path):
    contract_path = root / CONTRACT_REL
    schema_path = root / SCHEMA_REL
    report_schema_path = root / REPORT_SCHEMA_REL
    if _sha_file(contract_path) != EXPECTED_CONTRACT_SHA256:
        raise PreflightError("Challenge seed-domain preflight contract SHA-256 mismatch")
    if _sha_file(schema_path) != EXPECTED_SCHEMA_SHA256:
        raise PreflightError("Challenge seed-domain preflight schema SHA-256 mismatch")
    if _sha_file(report_schema_path) != EXPECTED_REPORT_SCHEMA_SHA256:
        raise PreflightError("Challenge seed-domain preflight report schema SHA-256 mismatch")
    if _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise PreflightError("Frozen C11-C manifest SHA-256 mismatch")

    contract = _read_json(contract_path)
    schema = _read_json(schema_path)
    report_schema = _read_json(report_schema_path)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "2.0" or contract.get("status") != STATUS:
        raise PreflightError("Challenge preflight contract identity/status mismatch")
    if contract.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise PreflightError("Contract frozen C11-C reference mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != SCHEMA_ID or schema.get("additionalProperties") is not False:
        raise PreflightError("Contract schema must be strict Draft 2020-12")
    if report_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or report_schema.get("$id") != REPORT_SCHEMA_ID or report_schema.get("additionalProperties") is not False:
        raise PreflightError("Report schema must be strict Draft 2020-12")

    try:
        import jsonschema  # type: ignore
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator.check_schema(report_schema)
        jsonschema.Draft202012Validator(schema).validate(contract)
    except ImportError:
        required = set(schema.get("required", []))
        if required - set(contract):
            raise PreflightError("Contract schema fallback rejected missing fields")
    except Exception as exc:
        raise PreflightError(f"Contract/report JSON schema invalid: {getattr(exc, 'message', str(exc))}") from exc

    if contract.get("contract_schema_sha256") != EXPECTED_SCHEMA_SHA256 or contract.get("report_schema_sha256") != EXPECTED_REPORT_SCHEMA_SHA256:
        raise PreflightError("Contract schema pins do not match")
    expected_approvals = {
        "challenge_seed_domain_preflight_approved": False,
        "challenge_visual_payload_seed_audit_approved": False,
        "seed_domains_complete_for_candidate_input": False,
        "automatic_seed_generation_approved": False,
        "master_seed_adopted": False,
        "candidate_input_admissible": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approvals:
        raise PreflightError("Challenge preflight governance lock changed")
    if contract.get("seed_variants") != [
        {"variant_id": key, **value} for key, value in SEED_VARIANTS.items()
    ]:
        raise PreflightError("Seed variants/order changed without contract review")
    if contract.get("challenge_ids") != list(CHALLENGE_IDS) or contract.get("expected_plan_calls") != 54:
        raise PreflightError("Challenge inventory or 9x3x2 planning cardinality mismatch")

    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) != len(EXPECTED_PIN_PATHS):
        raise PreflightError("Source pin count/shape mismatch")
    seen = []
    lineage = []
    for row in pins:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "role"}:
            raise PreflightError("Malformed source pin row")
        rel, expected, role = row.get("path"), row.get("sha256"), row.get("role")
        if rel not in PIN_ROLES or role != PIN_ROLES[rel]:
            raise PreflightError(f"Unapproved source pin or role: {rel!r}")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise PreflightError(f"Malformed SHA-256 in source pin: {rel}")
        if _sha_file(root / rel) != expected:
            raise PreflightError(f"Source pin mismatch: {rel}")
        seen.append(rel)
        lineage.append({"path": rel, "sha256": expected, "role": role})
    if seen != list(EXPECTED_PIN_PATHS):
        raise PreflightError("Source pins must be unique, complete and lexicographically ordered")

    # Confirm selector/family/mechanic pairs against the canonical editorial catalog and the source JSONs.
    catalog = editorial.build_catalog(root)
    variants = {
        v["id"]: {"family_id": family["id"], "mechanic": v.get("mechanic")}
        for family in catalog["content_types"]["challenges"]["families"]
        for v in family["variants"]
    }
    declared = contract.get("selector_matrix")
    if not isinstance(declared, list) or len(declared) != 9:
        raise PreflightError("Selector matrix must contain the nine canonical Challenge definitions")
    expected_matrix = []
    for cid in CHALLENGE_IDS:
        source = _read_json(root / "challenges" / f"{cid}.json")
        if source.get("challenge_id") != cid:
            raise PreflightError(f"Challenge file identity mismatch: {cid}")
        family_id = variants.get(cid, {}).get("family_id")
        mechanic = variants.get(cid, {}).get("mechanic")
        if not family_id or mechanic != source.get("mechanic"):
            raise PreflightError(f"Canonical catalog/source mechanic mismatch: {cid}")
        expected_matrix.append({
            "challenge_id": cid,
            "family_id": family_id,
            "mechanic": mechanic,
            "source_path": f"challenges/{cid}.json",
            "source_sha256": _sha_file(root / "challenges" / f"{cid}.json"),
        })
    if declared != expected_matrix:
        raise PreflightError("Contract selector matrix drifted from the live canonical Challenge catalog")
    return contract, schema, report_schema, lineage, expected_matrix


def _selection_for(root: Path, challenge_id: str, family_id: str | None = None, subtype_id: Any = None) -> dict[str, Any]:
    source = _read_json(root / "challenges" / f"{challenge_id}.json")
    resolved = editorial.resolve_selection({
        "content_type": "challenges",
        "family_id": family_id,
        "subtype_id": subtype_id,
        "variant_id": challenge_id,
    }, root)
    return {k: resolved.get(k) for k in ("content_type", "family_id", "subtype_id", "variant_id")}


def _build_raw_request(selection: Mapping[str, Any], request_id: str) -> dict[str, Any]:
    # Reuse the canonical request-envelope constructor; this preflight intentionally stops before its V1 selector gate.
    return binder._base_request(dict(selection), request_id)


def _duration_review(source: Mapping[str, Any], challenge_id: str) -> dict[str, Any]:
    video = source.get("video", {})
    if not isinstance(video, Mapping):
        video = {}
    keys = ("hook_duration", "game_duration", "reveal_duration", "cta_duration")
    components = {key: float(video.get(key, 0.0)) for key in keys}
    component_sum = sum(components.values())
    explicit_total = video.get("total_duration")
    if explicit_total is not None and (isinstance(explicit_total, bool) or not isinstance(explicit_total, (int, float))):
        raise PreflightError(f"Malformed video.total_duration for {challenge_id}")
    explicit_total_value = float(explicit_total) if explicit_total is not None else None
    matches = None if explicit_total_value is None else math.isclose(explicit_total_value, component_sum, rel_tol=0.0, abs_tol=1e-9)
    return {
        "challenge_id": challenge_id,
        "fps": video.get("fps"),
        "hook_duration": components["hook_duration"],
        "game_duration": components["game_duration"],
        "reveal_duration": components["reveal_duration"],
        "cta_duration": components["cta_duration"],
        "component_sum_duration_seconds": component_sum,
        "explicit_total_duration_seconds": explicit_total_value,
        "explicit_total_matches_component_sum": matches,
        "duration_conflict": matches is False,
        "timebase_approval": "NOT_EVALUATED_BY_PLANNER_PREFLIGHT",
    }


def _validate_negative_cases(root: Path) -> list[dict[str, str]]:
    cases: list[tuple[str, Any]] = []
    cases.append(("unknown_challenge_id", lambda: _selection_for(root, "CHALLENGE_010")))
    cases.append(("family_conflicts_with_mechanic", lambda: _selection_for(root, "CHALLENGE_001", "parking_v2")))
    cases.append(("challenge_subtype_not_declared", lambda: _selection_for(root, "CHALLENGE_001", None, "illegal-subtype")))

    def bool_seed_case():
        sel = _selection_for(root, "CHALLENGE_001")
        raw = _build_raw_request(sel, "C11D-PREFLIGHT-NEGATIVE-BOOL-SEED")
        raw["seed"] = True
        return planner.evaluate_universal_request(raw, root)
    cases.append(("boolean_gameplay_seed", bool_seed_case))

    def zero_music_seed_case():
        sel = _selection_for(root, "CHALLENGE_001")
        raw = _build_raw_request(sel, "C11D-PREFLIGHT-NEGATIVE-ZERO-MUSIC-SEED")
        raw["music_seed"] = 0
        return planner.evaluate_universal_request(raw, root)
    cases.append(("zero_music_seed", zero_music_seed_case))

    results = []
    for label, func in cases:
        rejected = False
        try:
            func()
        except Exception:
            rejected = True
        if not rejected:
            raise PreflightError(f"Fail-closed negative unexpectedly accepted: {label}")
        results.append({"case": label, "result": "REJECTED_AS_REQUIRED"})
    return results


def evaluate_challenge_seed_preflight(root_value: Path | str | None = None) -> dict[str, Any]:
    root = Path(root_value).resolve() if root_value is not None else ROOT
    contract, schema, report_schema, lineage, matrix = _load_and_validate_contract(root)
    by_id = {row["challenge_id"]: row for row in matrix}
    cases: list[dict[str, Any]] = []
    planner_calls = 0
    planned_by_challenge: dict[str, dict[str, dict[str, Any]]] = {}

    for challenge_id in CHALLENGE_IDS:
        selector = by_id[challenge_id]
        selected = _selection_for(root, challenge_id, selector["family_id"])
        if selected["family_id"] != selector["family_id"] or selected["variant_id"] != challenge_id:
            raise PreflightError(f"Canonical selector resolution mismatch: {challenge_id}")
        request_id = f"C11D-CHALLENGE-SEED-PREFLIGHT-{challenge_id}"
        base = _build_raw_request(selected, request_id)
        variants: dict[str, dict[str, Any]] = {}
        for variant_id, seed_pair in SEED_VARIANTS.items():
            raw = copy.deepcopy(base)
            raw["seed"] = seed_pair["seed"]
            raw["music_seed"] = seed_pair["music_seed"]
            diff = {k for k in base if base[k] != raw.get(k)}
            expected_diff = set()
            if seed_pair["seed"] != 12345:
                expected_diff.add("seed")
            if seed_pair["music_seed"] != 840001:
                expected_diff.add("music_seed")
            if diff != expected_diff:
                raise PreflightError(f"Seed variant changed non-seed request fields: {challenge_id}/{variant_id}")
            repeats: list[dict[str, Any]] = []
            for repeat_index in (1, 2):
                try:
                    result = planner.evaluate_universal_request(copy.deepcopy(raw), root)
                except Exception as exc:
                    raise PreflightError(f"Canonical D9.9 planner rejected {challenge_id}/{variant_id}/repeat-{repeat_index}: {exc}") from exc
                planner_calls += 1
                if result.get("status") != "PLANNED":
                    raise PreflightError(f"Canonical request plan did not reach PLANNED: {challenge_id}/{variant_id}")
                selection_result = result.get("plan", {}).get("selection", {})
                canonical_request = result.get("canonical_request", {})
                d4 = result.get("d4_evidence")
                if selection_result.get("content_type") != "challenges" or selection_result.get("family_id") != selector["family_id"] or selection_result.get("variant_id") != challenge_id or selection_result.get("subtype_id") is not None:
                    raise PreflightError(f"Canonical plan selector identity mismatch: {challenge_id}/{variant_id}")
                if canonical_request.get("seed") != seed_pair["seed"] or canonical_request.get("music_seed") != seed_pair["music_seed"]:
                    raise PreflightError(f"Canonical plan changed a declared seed field: {challenge_id}/{variant_id}")
                if not isinstance(d4, Mapping) or d4.get("status") != "PASS" or d4.get("parity", {}).get("status") != "PASS":
                    raise PreflightError(f"Canonical D4 GUI/CLI parity evidence missing: {challenge_id}/{variant_id}")
                hashes = {key: result.get(key) for key in ("request_hash", "plan_hash", "editorial_hash")}
                for key, value in hashes.items():
                    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                        raise PreflightError(f"Malformed {key}: {challenge_id}/{variant_id}")
                repeats.append({
                    "repeat_index": repeat_index,
                    "request_hash": hashes["request_hash"],
                    "plan_hash": hashes["plan_hash"],
                    "editorial_hash": hashes["editorial_hash"],
                    "canonical_request_seed": canonical_request.get("seed"),
                    "canonical_request_music_seed": canonical_request.get("music_seed"),
                    "d4_parity_status": d4.get("parity", {}).get("status"),
                })
            if repeats[0] != {**repeats[1], "repeat_index": 1}:
                # Compare the evidence fields explicitly; the repeat index is intentionally distinct.
                for key in ("request_hash", "plan_hash", "editorial_hash", "canonical_request_seed", "canonical_request_music_seed", "d4_parity_status"):
                    if repeats[0][key] != repeats[1][key]:
                        raise PreflightError(f"Canonical plan repeat drifted in {key}: {challenge_id}/{variant_id}")
            variant_record = {
                "variant_id": variant_id,
                "gameplay_seed": seed_pair["seed"],
                "music_seed": seed_pair["music_seed"],
                "repeat_1": repeats[0],
                "repeat_2": repeats[1],
                "repeat_stable": True,
            }
            variants[variant_id] = variant_record
            cases.append({
                "challenge_id": challenge_id,
                "family_id": selector["family_id"],
                "mechanic": selector["mechanic"],
                "variant_id": variant_id,
                "gameplay_seed": seed_pair["seed"],
                "music_seed": seed_pair["music_seed"],
                "request_hash": repeats[0]["request_hash"],
                "request_hash_repeat_2": repeats[1]["request_hash"],
                "plan_hash": repeats[0]["plan_hash"],
                "plan_hash_repeat_2": repeats[1]["plan_hash"],
                "editorial_hash": repeats[0]["editorial_hash"],
                "editorial_hash_repeat_2": repeats[1]["editorial_hash"],
                "repeat_stable": True,
                "canonical_plan_status": "PLANNED",
                "canonical_d4_parity_status": "PASS",
            })
        planned_by_challenge[challenge_id] = variants

    if planner_calls != 54 or len(cases) != 27:
        raise PreflightError(f"Planning matrix cardinality mismatch: calls={planner_calls}, cases={len(cases)}")

    sensitivity = []
    timing_review = []
    for challenge_id in CHALLENGE_IDS:
        rows = planned_by_challenge[challenge_id]
        base = rows["BASELINE"]["repeat_1"]
        game = rows["GAMEPLAY_SEED_ONLY_CHANGED"]["repeat_1"]
        music = rows["MUSIC_SEED_ONLY_CHANGED"]["repeat_1"]
        for key in ("request_hash", "plan_hash"):
            if base[key] == game[key]:
                raise PreflightError(f"Gameplay seed did not change canonical {key}: {challenge_id}")
            if base[key] == music[key]:
                raise PreflightError(f"Music seed did not change canonical {key}: {challenge_id}")
        for variant_id, variant_record in rows.items():
            if variant_record["repeat_1"]["editorial_hash"] != base["editorial_hash"]:
                raise PreflightError(f"Seed mutation leaked into editorial identity: {challenge_id}/{variant_id}")
        source = _read_json(root / "challenges" / f"{challenge_id}.json")
        time_review = _duration_review(source, challenge_id)
        timing_review.append(time_review)
        sensitivity.append({
            "challenge_id": challenge_id,
            "family_id": by_id[challenge_id]["family_id"],
            "gameplay_seed_changes_request_and_plan_identity": True,
            "music_seed_changes_request_and_plan_identity": True,
            "editorial_identity_preserved_across_seed_variants": True,
            "canonical_planning_only": True,
            "visual_payload_sensitivity": "NOT_TESTED",
            "timebase_approved": False,
        })

    negative_cases = _validate_negative_cases(root)
    timing_conflicts = [row["challenge_id"] for row in timing_review if row["duration_conflict"]]
    if timing_conflicts != ["CHALLENGE_008", "CHALLENGE_009"]:
        raise PreflightError(f"Source duration conflict set changed; expected CHALLENGE_008/009, got {timing_conflicts}")

    source_lineage_sha = _sha_json(lineage)
    report: dict[str, Any] = {
        "schema": REPORT_SCHEMA_ID,
        "schema_version": "2.0",
        "status": STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "source_pin_count": len(lineage),
        "source_lineage": lineage,
        "source_lineage_sha256": source_lineage_sha,
        "selector_matrix": matrix,
        "cases": cases,
        "summary": {
            "selectors": "9/9",
            "seed_variant_cases": "27/27",
            "repeat_consistency_checks": "27/27",
            "request_hash_repeat_matches": "27/27",
            "plan_hash_repeat_matches": "27/27",
            "request_identity_seed_sensitivity": "9/9",
            "plan_identity_seed_sensitivity": "9/9",
            "editorial_identity_invariance": "9/9",
            "negative_cases": "5/5",
            "planner_invocations": 54,
            "godot_invocations": 0,
            "payload_materialized": False,
            "challenge_visual_payload_seed_sensitivity": "NOT_TESTED",
            "timebase_conflicts": len(timing_conflicts),
        },
        "seed_sensitivity": sensitivity,
        "timing_review": timing_review,
        "negative_cases": negative_cases,
        "unclosed_requirements": [
            "The accepted V1 dynamic request-to-payload binder and Godot harness remain explicitly pinned to CHALLENGE_004 / parking_v2.",
            "This preflight proves canonical request/plan sensitivity only; it does not materialize Challenge visual payloads or prove gameplay_seed visual sensitivity.",
            "CHALLENGE_008 and CHALLENGE_009 declare total_duration=11 seconds while hook+game+reveal+CTA components sum to 12 seconds; timebase policy must resolve this before timeline/payload acceptance.",
            "Challenge-specific mechanics, visual snapshots, asset whitelists, source timebases and payload schemas must be explicitly covered by an additive V2 materializer using shared canonical planner/bridge/adapter internals.",
            "Automatic/default seed behavior, equal-domain collision policy, and arbitrary cross-domain requests remain unproven; master_seed remains not adopted.",
            "Candidate I/O admission, shared presentation policy approval, D4.8, renderer approval, media creation, release authority, freeze and cutover remain blocked.",
        ],
        "governance": {
            "planner_only": True,
            "godot_invocations": 0,
            "payload_materialized": False,
            "payload_files_written": False,
            "renderer_input_emitted": False,
            "renderer": "OFF",
            "media_created": False,
            "candidate_input_admissible": False,
            "seed_domains_complete_for_candidate_input": False,
            "automatic_seed_generation": False,
            "master_seed_adopted": False,
            "D4.8": "BLOCKED",
            "D9.10": "PREPARE_ONLY",
            "D9.17": "BLOCKED_NO_GO",
            "D10": "BLOCKED",
            "release_authority": "NONE",
        },
    }
    report["audit_sha256"] = _sha_json(report)
    _validate_report(report, report_schema)
    return report


def _validate_report(report: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    try:
        import jsonschema  # type: ignore
        jsonschema.Draft202012Validator(schema).validate(dict(report))
    except ImportError:
        must = set(schema.get("required", []))
        if must - set(report):
            raise PreflightError("Report schema fallback rejected missing fields")
    except Exception as exc:
        raise PreflightError(f"Report schema validation failed: {getattr(exc, 'message', str(exc))}") from exc
    audit_sha = report.get("audit_sha256")
    without = {k: v for k, v in report.items() if k != "audit_sha256"}
    if audit_sha is not None and audit_sha != _sha_json(without):
        raise PreflightError("Report audit_sha256 mismatch")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-pinned Challenge planner seed preflight; no Godot or payload creation.")
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--full-report", action="store_true", help="Print compact canonical JSON report to stdout")
    args = parser.parse_args(argv)
    try:
        report = evaluate_challenge_seed_preflight(args.root)
        summary = (
            "C11-D CHALLENGE SEED DOMAIN PLANNER PREFLIGHT V2 PASS"
            f" | selectors={report['summary']['selectors']}"
            f" | seed_variant_cases={report['summary']['seed_variant_cases']}"
            f" | repeat_consistency_checks={report['summary']['repeat_consistency_checks']}"
            f" | request_identity_seed_sensitivity={report['summary']['request_identity_seed_sensitivity']}"
            f" | plan_identity_seed_sensitivity={report['summary']['plan_identity_seed_sensitivity']}"
            f" | editorial_identity_invariance={report['summary']['editorial_identity_invariance']}"
            f" | negative_cases={report['summary']['negative_cases']}"
            f" | planner_invocations={report['summary']['planner_invocations']}"
            " | godot_invocations=0 | payload_materialized=false | challenge_visual_payload_seed_sensitivity=NOT_TESTED"
            f" | timebase_conflicts={report['summary']['timebase_conflicts']}"
            " | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
        )
        print(summary)
        if args.full_report:
            print(REPORT_PREFIX + _canonical(report))
        return 0
    except (PreflightError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"C11-D CHALLENGE SEED DOMAIN PLANNER PREFLIGHT V2 FAIL | {exc} | godot_invocations=0 | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
