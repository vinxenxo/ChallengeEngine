"""Explicit, receipt-driven projection of C11-D records for the existing Catalog GUI.

This module does not discover products by arbitrary filename, render media, authorize
release, or mutate canonical artifacts. Only these governed sources are projected:
- D7.3 canonical catalog guarded by D7.3/D7.4 receipts and validation.
- D9.4 acceptance manifest with explicit media path/hash rows.
- D9.5.1 Producer GUI receipts with the complete saved request/plan evidence bundle.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

CATALOG_INTEGRATION_VERSION = "0.2.0"
D7_CATALOG = Path("artifacts/tests/c11d_d7/d7_3/d7_3_canonical_catalog.json")
D7_VALIDATION = Path("artifacts/tests/c11d_d7/d7_3/d7_3_catalog_validation.json")
D7_RECEIPT = Path("artifacts/tests/c11d_d7/d7_3/d7_3_catalog_receipt.json")
D7_IDENTITY_RECEIPT = Path("artifacts/tests/c11d_d7/d7_4/d7_4_identity_receipt.json")
D8_RECEIPT = Path("artifacts/tests/c11d_d8/d8_7/d8_7_receipt.json")
D8_SCOPE = Path("definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json")
D94_RECEIPT = Path("artifacts/tests/c11d_d9/d9_4/evidence/d9_4_receipt.json")
D94_MANIFEST = Path("artifacts/tests/c11d_d9/d9_4/evidence/d9_4_acceptance_manifest.json")
PRODUCER_GUI_ROOT = Path("artifacts/tests/c11d_d9/producer_gui")
EXPECTED_D94_MEDIA = {"D9.1_VIDEO", "D9.2_AV", "D9.3_REPEAT_A", "D9.3_REPEAT_B", "D9.3_NEGATIVE"}
PLAN_FILES = (
    "request.json",
    "canonical_request.json",
    "resolved_personalization.json",
    "production_plan.json",
    "gui_cli_parity.json",
    "producer_gui_receipt.json",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError):
        return False


def _safe_project_path(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    # On Windows pathlib understands native absolute paths. On non-Windows audit
    # hosts we accept only relative repository paths; Windows absolute paths are
    # deliberately not remapped heuristically to avoid filename inference.
    value = raw.strip()
    candidate = Path(value)
    if candidate.is_absolute():
        if not _inside(root, candidate):
            return None
        return candidate.resolve()
    candidate = (root / Path(value.replace("\\", os.sep))).resolve()
    if not _inside(root, candidate):
        return None
    return candidate


def _relative(root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _add_issue(issues: list[dict[str, str]], source: str, code: str, message: str) -> None:
    issues.append({"source": source, "code": code, "message": message})


def _read_receipt(root: Path, rel: Path, *, checkpoint: str | None = None,
                  result: str = "PASS", status: str = "CLOSED") -> tuple[dict[str, Any] | None, str | None]:
    path = root / rel
    if not path.is_file():
        return None, "missing"
    try:
        data = _load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"invalid JSON: {exc}"
    if not isinstance(data, dict):
        return None, "receipt is not a JSON object"
    if checkpoint and data.get("checkpoint") != checkpoint:
        return None, f"checkpoint must be {checkpoint}"
    if data.get("result") != result or data.get("status") != status:
        return None, f"expected {result}/{status}"
    if data.get("release_authority", "NONE") != "NONE":
        return None, "release_authority must remain NONE"
    return data, None


def _seed_display(bindings: Any) -> tuple[str, str]:
    if not isinstance(bindings, dict):
        return "NOT_RESOLVED", "NOT_RESOLVED"
    game = bindings.get("GAMEPLAY", {})
    music = bindings.get("MUSIC", {})
    def render(item: Any, fallback: str) -> str:
        if not isinstance(item, dict):
            return fallback
        # D7 records seed authority and source fields, not necessarily concrete
        # runtime seed values; preserve that distinction in the display.
        value = item.get("value", item.get("seed"))
        if value is not None:
            return str(value)
        return str(item.get("source_field") or fallback)
    return render(game, "request.seed"), render(music, "request.music_seed")


def _load_d7_intents(root: Path, records: list[dict[str, Any]], issues: list[dict[str, str]]) -> str:
    paths = (D7_CATALOG, D7_VALIDATION, D7_RECEIPT, D7_IDENTITY_RECEIPT)
    if not all((root / p).is_file() for p in paths):
        _add_issue(issues, "D7.3/D7.4", "EVIDENCE_NOT_PRESENT", "Canonical D7.3/D7.4 outputs are not all present; no canonical intent rows projected.")
        return "NOT_PRESENT"
    try:
        catalog = _load_json(root / D7_CATALOG)
        validation = _load_json(root / D7_VALIDATION)
        receipt = _load_json(root / D7_RECEIPT)
        identity_receipt = _load_json(root / D7_IDENTITY_RECEIPT)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _add_issue(issues, "D7.3/D7.4", "INVALID_EVIDENCE", str(exc))
        return "INVALID"
    if not isinstance(catalog, dict) or catalog.get("authority") != "D7.3" or catalog.get("status") != "CANONICAL":
        _add_issue(issues, "D7.3", "AUTHORITY_MISMATCH", "Catalog must have authority D7.3 and CANONICAL status.")
        return "INVALID"
    if validation.get("result") != "PASS" or receipt.get("result") != "PASS" or receipt.get("status") != "CLOSED":
        _add_issue(issues, "D7.3", "VALIDATION_NOT_CLOSED", "D7.3 catalog/validation receipt is not PASS/CLOSED.")
        return "INVALID"
    if identity_receipt.get("result") != "PASS" or identity_receipt.get("status") != "CLOSED":
        _add_issue(issues, "D7.4", "IDENTITY_NOT_CLOSED", "D7.4 identity/provenance receipt is not PASS/CLOSED.")
        return "INVALID"
    if catalog.get("authority_state", {}).get("runtime_authority") != "NONE":
        _add_issue(issues, "D7.3", "RUNTIME_AUTHORITY_FORBIDDEN", "Canonical catalog runtime authority must remain NONE.")
        return "INVALID"
    if catalog.get("authority_state", {}).get("production_execution") is not False or catalog.get("authority_state", {}).get("renderer_execution") is not False:
        _add_issue(issues, "D7.3", "EXECUTION_AUTHORITY_FORBIDDEN", "Canonical catalog must remain plan-only.")
        return "INVALID"
    items = catalog.get("items")
    if not isinstance(items, list) or len(items) != 90 or len({str(i.get("catalog_key")) for i in items if isinstance(i, dict)}) != 90:
        _add_issue(issues, "D7.3", "CATALOG_COVERAGE_INVALID", "Canonical catalog must contain 90 unique catalog items.")
        return "INVALID"
    for item in items:
        if not isinstance(item, dict):
            _add_issue(issues, "D7.3", "INVALID_ITEM", "Catalog contains a non-object item.")
            continue
        game_seed, music_seed = _seed_display(item.get("seed_bindings"))
        records.append({
            "record_type": "CANONICAL_INTENT",
            "record_id": str(item.get("catalog_item_id") or item.get("catalog_key") or "UNKNOWN"),
            "challenge_id": str(item.get("challenge_id") or "UNKNOWN"),
            "challenge_version": str(item.get("challenge_version") or "UNKNOWN"),
            "status": "PLAN_ONLY",
            "gameplay_seed": game_seed,
            "music_seed": music_seed,
            "delivery_profile_id": str(item.get("delivery_profile_id") or "UNKNOWN"),
            "presentation_profile_id": "NOT_BOUND_BY_D7_CATALOG",
            "personalization_profile": str(item.get("personalization_profile") or "none_v1"),
            "request_hash": None,
            "personalization_hash": None,
            "plan_hash": None,
            "identity_hash": str(item.get("identity_hash") or ""),
            "media_path": None,
            "media_sha256": None,
            "media_bytes": None,
            "media_eligibility": "NO_MEDIA_CREATED",
            "release_authority": "NONE",
            "execution": "DECLARATIVE INTENT ONLY",
            "evidence_path": D7_CATALOG.as_posix(),
            "evidence_paths": [D7_CATALOG.as_posix(), D7_VALIDATION.as_posix(), D7_RECEIPT.as_posix(), D7_IDENTITY_RECEIPT.as_posix()],
            "provenance": item.get("provenance", {}),
            "reproduction_command": None,
            "source_status": "PASS/CLOSED",
            "search_text": " ".join(str(v) for v in (item.get("catalog_key"), item.get("challenge_id"), item.get("delivery_profile_id"), item.get("mode"), item.get("catalog_item_id"))).lower(),
        })
    return "PASS/CLOSED"


def _receipt_map(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for label, rel in (
        ("D9.1", Path("artifacts/tests/c11d_d9/d9_1/evidence/d9_1_receipt.json")),
        ("D9.2", Path("artifacts/tests/c11d_d9/d9_2/evidence/d9_2_receipt.json")),
        ("D9.3", Path("artifacts/tests/c11d_d9/d9_3/evidence/d9_3_receipt.json")),
    ):
        try:
            path = root / rel
            if path.is_file():
                item = _load_json(path)
                if isinstance(item, dict):
                    out[label] = item
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
    return out


def _load_d8_release_scope(root: Path, issues: list[dict[str, str]]) -> str:
    receipt, receipt_error = _read_receipt(root, D8_RECEIPT, checkpoint="D8.7", result="PASS_NO_MEDIA", status="CLOSED")
    if receipt_error or receipt is None:
        _add_issue(issues, "D8.7", "RELEASE_SCOPE_NOT_CONFIRMED", "D8.7 must remain PASS_NO_MEDIA/CLOSED before pilot media can be shown as non-release evidence.")
        return "INVALID"
    scope_path = root / D8_SCOPE
    if not scope_path.is_file():
        _add_issue(issues, "D8", "MEDIA_SCOPE_MISSING", "Canonical D8 media scope file is missing.")
        return "INVALID"
    try:
        scope = _load_json(scope_path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _add_issue(issues, "D8", "MEDIA_SCOPE_INVALID", str(exc))
        return "INVALID"
    if not isinstance(scope, dict) or scope.get("scope_mode") != "EXPLICIT_REGISTRY_ONLY":
        _add_issue(issues, "D8", "MEDIA_SCOPE_MODE_INVALID", "D8 media scope must use EXPLICIT_REGISTRY_ONLY.")
        return "INVALID"
    registry = scope.get("registry")
    if not isinstance(registry, list) or registry or int(scope.get("candidate_count", -1)) != 0:
        _add_issue(issues, "D8", "MEDIA_SCOPE_NOT_EMPTY", "D8 registry/candidate count must remain empty for the current PASS_NO_MEDIA checkpoint.")
        return "INVALID"
    if scope.get("release_authority") != "NONE" or scope.get("production_execution") is not False or scope.get("renderer_execution") is not False or scope.get("runtime_authority") != "NONE":
        _add_issue(issues, "D8", "MEDIA_SCOPE_AUTHORITY_INVALID", "D8 media scope must not authorize execution or release.")
        return "INVALID"
    if int(receipt.get("scope_candidate_count", -1)) != 0 or receipt.get("release_authority") != "NONE" or receipt.get("d8_control_plane") != "ACCEPTED":
        _add_issue(issues, "D8.7", "RECEIPT_SCOPE_MISMATCH", "D8.7 receipt must record accepted control plane, zero candidates and no release authority.")
        return "INVALID"
    return "PASS_NO_MEDIA/CLOSED"


def _load_d94_media(root: Path, records: list[dict[str, Any]], issues: list[dict[str, str]], d8_scope_valid: bool) -> str:
    receipt, receipt_error = _read_receipt(root, D94_RECEIPT, checkpoint="D9.4")
    manifest_path = root / D94_MANIFEST
    if receipt_error == "missing" and not manifest_path.is_file():
        _add_issue(issues, "D9.4", "EVIDENCE_NOT_PRESENT", "D9.4 acceptance manifest is not present; no pilot media rows projected.")
        return "NOT_PRESENT"
    if receipt_error or receipt is None:
        _add_issue(issues, "D9.4", "RECEIPT_INVALID", receipt_error or "invalid receipt")
        return "INVALID"
    if not manifest_path.is_file():
        _add_issue(issues, "D9.4", "MANIFEST_MISSING", "D9.4 manifest referenced by the catalog policy is missing.")
        return "INVALID"
    if not d8_scope_valid:
        _add_issue(issues, "D9.4", "D8_RELEASE_GATE_BLOCKED", "Pilot media is not projected because the canonical D8.7 empty-scope/no-release gate did not validate.")
        return "BLOCKED_BY_D8_SCOPE"
    try:
        manifest = _load_json(manifest_path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _add_issue(issues, "D9.4", "MANIFEST_INVALID", str(exc))
        return "INVALID"
    if not isinstance(manifest, dict) or manifest.get("checkpoint") != "D9.4" or manifest.get("result") != "PASS" or manifest.get("d9_status") not in ("CLOSED", "ACTIVE"):
        _add_issue(issues, "D9.4", "MANIFEST_NOT_ACCEPTED", "D9.4 manifest identity/result is invalid.")
        return "INVALID"
    if manifest.get("release_authority") != "NONE" or manifest.get("production_execution") is not False or manifest.get("renderer_execution") is not False:
        _add_issue(issues, "D9.4", "AUTHORITY_BOUNDARY", "D9.4 manifest must remain non-release and non-executing.")
        return "INVALID"
    media = manifest.get("media")
    if not isinstance(media, list):
        _add_issue(issues, "D9.4", "MEDIA_LIST_MISSING", "D9.4 manifest must have an explicit media list.")
        return "INVALID"
    names = {str(m.get("name")) for m in media if isinstance(m, dict)}
    if names != EXPECTED_D94_MEDIA:
        _add_issue(issues, "D9.4", "MEDIA_INVENTORY_MISMATCH", f"Expected exact media identifiers {sorted(EXPECTED_D94_MEDIA)}; found {sorted(names)}.")
        return "INVALID"
    receipts = _receipt_map(root)
    for entry in media:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name"))
        source = "D9.1" if name == "D9.1_VIDEO" else "D9.2" if name == "D9.2_AV" else "D9.3"
        media_path = _safe_project_path(root, entry.get("path"))
        if media_path is None or not media_path.is_file():
            _add_issue(issues, "D9.4", "MEDIA_PATH_MISSING_OR_OUTSIDE_ROOT", f"{name}: path is missing, invalid or outside project root.")
            continue
        actual_hash = _sha256(media_path)
        expected_hash = str(entry.get("sha256") or "").lower()
        actual_bytes = media_path.stat().st_size
        if len(expected_hash) != 64 or actual_hash != expected_hash or (entry.get("bytes") is not None and int(entry["bytes"]) != actual_bytes):
            _add_issue(issues, "D9.4", "MEDIA_HASH_OR_SIZE_MISMATCH", f"{name}: physical file does not match explicit D9.4 manifest.")
            continue
        source_receipt = receipts.get(source, {})
        profile = str(source_receipt.get("delivery_profile_id") or "REVIEW_720")
        records.append({
            "record_type": "PILOT_MEDIA",
            "record_id": name,
            "challenge_id": str(source_receipt.get("challenge_id") or manifest.get("challenge_id") or "CHALLENGE_001"),
            "challenge_version": str(source_receipt.get("challenge_version") or "UNKNOWN"),
            "status": "VALIDATED_PILOT",
            "gameplay_seed": str(source_receipt.get("seed", "UNKNOWN")),
            "music_seed": str(source_receipt.get("music_seed", "UNKNOWN")),
            "delivery_profile_id": profile,
            "presentation_profile_id": str(source_receipt.get("presentation_profile_id") or "social_default_v1"),
            "personalization_profile": "NOT_APPLIED_BY_D9.1-D9.3",
            "request_hash": None,
            "personalization_hash": None,
            "plan_hash": str(source_receipt.get("d4_plan_sha256") or ""),
            "identity_hash": None,
            "media_path": _relative(root, media_path),
            "media_sha256": actual_hash,
            "media_bytes": actual_bytes,
            "media_eligibility": "NOT_REGISTERED_FOR_D8_RELEASE",
            "release_authority": "NONE",
            "execution": "PILOT VALIDATION ONLY; NOT A RELEASE PRODUCT",
            "evidence_path": D94_MANIFEST.as_posix(),
            "evidence_paths": [D94_RECEIPT.as_posix(), D94_MANIFEST.as_posix(), f"artifacts/tests/c11d_d9/{source.lower().replace('.', '_')}/evidence/{source.lower().replace('.', '_')}_receipt.json"],
            "provenance": {"d9_checkpoint": source, "d9_4_acceptance_manifest": D94_MANIFEST.as_posix(), "sha256_verified": True},
            "reproduction_command": None,
            "source_status": "PASS/PILOT_COMPLETE",
            "search_text": " ".join(str(v) for v in (name, source_receipt.get("challenge_id", "CHALLENGE_001"), profile, entry.get("path"))).lower(),
        })
    return "PASS/CLOSED" if not any(i["source"] == "D9.4" and i["code"] in {"MEDIA_PATH_MISSING_OR_OUTSIDE_ROOT", "MEDIA_HASH_OR_SIZE_MISMATCH", "MEDIA_INVENTORY_MISMATCH", "MANIFEST_NOT_ACCEPTED", "AUTHORITY_BOUNDARY"} for i in issues) else "PARTIAL/INVALID_MEDIA"


def _load_producer_plans(root: Path, records: list[dict[str, Any]], issues: list[dict[str, str]]) -> str:
    base = root / PRODUCER_GUI_ROOT
    if not base.is_dir():
        _add_issue(issues, "D9.5.1", "NO_GUI_PLAN_RECORDS", "No persisted Producer GUI plan records are present yet.")
        return "NOT_PRESENT"
    found = 0
    invalid = 0
    for receipt_path in sorted(base.glob("*/producer_gui_receipt.json")):
        found += 1
        folder = receipt_path.parent
        rel_folder = _relative(root, folder)
        try:
            receipt = _load_json(receipt_path)
            if not isinstance(receipt, dict):
                raise ValueError("receipt is not an object")
            if receipt.get("schema") != "C11-D-D9.5.1-PRODUCER-GUI-RECEIPT-V1":
                raise ValueError("unsupported receipt schema")
            if receipt.get("phase") != "D9.5.1" or receipt.get("result") != "PASS_PLAN_ONLY" or receipt.get("status") != "PLANNED":
                raise ValueError("receipt is not PASS_PLAN_ONLY/PLANNED")
            if receipt.get("renderer_execution") is not False or receipt.get("production_execution") is not False or receipt.get("release_authority") != "NONE" or receipt.get("d4_8") != "BLOCKED":
                raise ValueError("authority boundary invalid")
            if receipt.get("gui_cli_parity") != "PASS":
                raise ValueError("GUI/CLI parity is not PASS")
            docs: dict[str, Any] = {}
            for filename in PLAN_FILES:
                p = folder / filename
                if not p.is_file():
                    raise ValueError(f"missing companion evidence: {filename}")
                docs[filename] = _load_json(p)
            request = docs["request.json"]
            canonical = docs["canonical_request.json"]
            personalization = docs["resolved_personalization.json"]
            plan = docs["production_plan.json"]
            parity = docs["gui_cli_parity.json"]
            if str(request.get("request_id")) != str(receipt.get("request_id")):
                raise ValueError("request_id does not match receipt")
            if str(request.get("request_id")) != folder.name:
                raise ValueError("request_id does not match evidence directory identity")
            if parity.get("status") != "PASS" or parity.get("gui_plan_hash") != receipt.get("plan_hash"):
                raise ValueError("parity/plan hash does not match receipt")
            if personalization.get("profile_id") is None:
                raise ValueError("resolved personalization profile missing")
            guard = plan
            for key in ("renderer_activation", "gui_activation", "orchestrator_execution", "simulation_truth_mutation", "winning_frame_mutation", "close_calls_mutation", "gameplay_rng_consumption", "structural_rng_consumption"):
                if guard.get(key) is not False:
                    raise ValueError(f"plan guard {key} must be false")
            if guard.get("runtime_authority") != "NONE":
                raise ValueError("plan runtime_authority must remain NONE")
            if receipt.get("plan_hash") != parity.get("gui_plan_hash") or receipt.get("request_hash") != parity.get("gui_request_hash"):
                raise ValueError("request/plan hash mismatch")
            command = (
                'python .\\tools\\c11d\\d4\\production_cli.py '
                f'--request ".\\{(folder / "request.json").relative_to(root).as_posix().replace("/", chr(92))}" '
                f'--output ".\\{(folder / "production_plan_cli_replay.json").relative_to(root).as_posix().replace("/", chr(92))}"'
            )
            rel_files = [f"{rel_folder}/{name}" for name in PLAN_FILES]
            records.append({
                "record_type": "PRODUCER_PLAN",
                "record_id": str(receipt["request_id"]),
                "challenge_id": str(request.get("challenge_id") or canonical.get("challenge_id") or "UNKNOWN"),
                "challenge_version": str(request.get("challenge_version") or canonical.get("challenge_version") or "UNKNOWN"),
                "status": "PLAN_ONLY",
                "gameplay_seed": str(request.get("seed", "UNKNOWN")),
                "music_seed": str(request.get("music_seed", "UNKNOWN")),
                "delivery_profile_id": str(request.get("delivery_profile_id") or "UNKNOWN"),
                "presentation_profile_id": str(request.get("presentation_profile_id") or "UNKNOWN"),
                "personalization_profile": str(personalization.get("profile_id") or "UNKNOWN"),
                "request_hash": str(receipt.get("request_hash") or ""),
                "personalization_hash": str(receipt.get("personalization_hash") or ""),
                "plan_hash": str(receipt.get("plan_hash") or ""),
                "identity_hash": None,
                "media_path": None,
                "media_sha256": None,
                "media_bytes": None,
                "media_eligibility": "NO_MEDIA_CREATED",
                "release_authority": "NONE",
                "execution": "PLAN ONLY; D4.8 BLOCKED",
                "evidence_path": rel_folder,
                "evidence_paths": rel_files,
                "provenance": {"request_origin": "GUI", "canonical_cli_adapter": "tools/c11d/d4/production_cli.py", "gui_cli_parity": "PASS"},
                "reproduction_command": command,
                "source_status": "PASS_PLAN_ONLY/PLANNED",
                "search_text": " ".join(str(v) for v in (receipt.get("request_id"), request.get("challenge_id"), request.get("delivery_profile_id"), personalization.get("profile_id"))).lower(),
            })
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
            invalid += 1
            _add_issue(issues, "D9.5.1", "PLAN_RECORD_INVALID", f"{rel_folder or receipt_path.name}: {exc}")
    if found == 0:
        _add_issue(issues, "D9.5.1", "NO_GUI_PLAN_RECORDS", "No Producer GUI receipts found; catalog remains usable.")
        return "NOT_PRESENT"
    return "PASS" if invalid == 0 else "PARTIAL/INVALID"


def build_catalog_data(project_root: Path) -> dict[str, Any]:
    root = Path(project_root).resolve()
    records: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    d8_scope_status = _load_d8_release_scope(root, issues)
    status = {
        "D8_release_scope": d8_scope_status,
        "D7_canonical_intents": _load_d7_intents(root, records, issues),
        "D9_4_pilot_media": _load_d94_media(root, records, issues, d8_scope_valid=(d8_scope_status == "PASS_NO_MEDIA/CLOSED")),
        "D9_5_1_producer_plans": _load_producer_plans(root, records, issues),
    }
    records.sort(key=lambda x: (x["record_type"], x["challenge_id"], x["record_id"]))
    return {
        "schema": "C11-D-D9.6-CATALOG-PROJECTION-V1",
        "catalog_version": CATALOG_INTEGRATION_VERSION,
        "project_root": str(root),
        "records": records,
        "issues": issues,
        "source_status": status,
        "summary": {
            "record_count": len(records),
            "canonical_intents": sum(r["record_type"] == "CANONICAL_INTENT" for r in records),
            "producer_plans": sum(r["record_type"] == "PRODUCER_PLAN" for r in records),
            "pilot_media": sum(r["record_type"] == "PILOT_MEDIA" for r in records),
            "release_products": 0,
            "release_authority": "NONE",
        },
    }
