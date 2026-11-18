from __future__ import annotations

"""D9 E6 Challenge PREPARE_ONLY orchestration.

Reads every selector, gameplay/music seed, profile, and timebase from the
pinned external input manifest. Calls only the existing E1 shared service
and the existing E6 plan-only envelope builder. It never dispatches, renders,
starts a media process, or reserves a BatchId.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

PINS_REL = "definitions/c11d/production/C11E_E6_CHALLENGE_PREPARE_ONLY_SOURCE_PINS_V1.json"
PINS_SHA256 = "3b2333b2ae02158f27363577069dba519bff3975714d1cd95e569728425a09b6"
MANIFEST_SCHEMA = "C11E-E6-CHALLENGE-PREPARE-ONLY-INPUT-MANIFEST-V1"
RECEIPT_SCHEMA = "C11E-E6-CHALLENGE-PREPARE-ONLY-ORCHESTRATOR-RECEIPT-V1"
OUTPUT_REL = "artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator"
RUN_ID_PATTERN = re.compile(r"^E6CHPREP_[0-9]{8}T[0-9]{6}Z_[A-F0-9]{8}$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_PROBES = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
PHASE_FIELDS = (("HOOK", "hook_duration"), ("GAME", "game_duration"), ("REVEAL", "reveal_duration"), ("CTA", "cta_duration"))


class OrchestratorError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise OrchestratorError(f"INVALID_JSON:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise OrchestratorError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def safe_project_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise OrchestratorError(f"UNSAFE_RELATIVE_PATH:{relative!r}")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise OrchestratorError(f"PATH_TRAVERSAL_REJECTED:{relative!r}")
    target = root.joinpath(*pure.parts)
    root_resolved = root.resolve(strict=True)
    target_resolved = target.resolve(strict=False)
    try:
        target_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise OrchestratorError(f"PATH_OUTSIDE_PROJECT_ROOT:{relative!r}") from exc
    cursor = root
    for part in pure.parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise OrchestratorError(f"SYMLINK_PATH_REJECTED:{relative!r}")
    return target


def _require_exact_keys(value: Mapping[str, Any], keys: set[str], label: str) -> None:
    if set(value) != keys:
        missing = sorted(keys - set(value))
        extra = sorted(set(value) - keys)
        raise OrchestratorError(f"{label}_KEY_SET_MISMATCH:missing={missing}:extra={extra}")


def _require_int(value: Any, label: str, minimum: int = 1, maximum: int = 2147483646) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise OrchestratorError(f"{label}_MUST_BE_EXPLICIT_INTEGER_IN_RANGE")
    return value


def _require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA_PATTERN.fullmatch(value):
        raise OrchestratorError(f"{label}_MUST_BE_LOWERCASE_SHA256")
    return value


def verify_pin_rows(root: Path, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256", "role"}:
            raise OrchestratorError("SOURCE_PIN_ROW_SCHEMA_INVALID")
        path = safe_project_path(root, row["path"])
        expected = _require_sha(row["sha256"], f"PIN:{row['path']}")
        if not path.is_file():
            raise OrchestratorError(f"PINNED_FILE_MISSING:{row['path']}")
        actual_bytes = path.stat().st_size
        expected_bytes = row["bytes"]
        if expected_bytes is not None and actual_bytes != expected_bytes:
            raise OrchestratorError(f"PINNED_FILE_SIZE_MISMATCH:{row['path']}:{actual_bytes}:{expected_bytes}")
        actual_sha = sha256_file(path)
        if actual_sha != expected:
            raise OrchestratorError(f"PINNED_FILE_SHA256_MISMATCH:{row['path']}:{actual_sha}:{expected}")
        result.append({"path": row["path"], "bytes": actual_bytes, "sha256": actual_sha, "role": row["role"], "status": "PASS"})
    return result


def verify_pins_document(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pins_path = safe_project_path(root, PINS_REL)
    if not pins_path.is_file():
        raise OrchestratorError("SOURCE_PIN_DOCUMENT_MISSING")
    actual_pin_doc_sha = sha256_file(pins_path)
    if actual_pin_doc_sha != PINS_SHA256:
        raise OrchestratorError(f"SOURCE_PIN_DOCUMENT_SHA256_MISMATCH:{actual_pin_doc_sha}")
    pins = load_json_object(pins_path)
    if pins.get("schema") != "C11E-E6-CHALLENGE-PREPARE-ONLY-SOURCE-PINS-V1":
        raise OrchestratorError("SOURCE_PIN_DOCUMENT_SCHEMA_MISMATCH")
    rows = pins.get("checkout_files")
    evidence = pins.get("upstream_evidence_files")
    if not isinstance(rows, list) or not isinstance(evidence, list):
        raise OrchestratorError("SOURCE_PIN_DOCUMENT_ROWS_MISSING")
    checked = verify_pin_rows(root, rows + evidence)
    return pins, checked


def verify_upstream_evidence(root: Path, pins: Mapping[str, Any]) -> dict[str, Any]:
    evidence = {row["path"]: row for row in pins["upstream_evidence_files"]}
    result: dict[str, Any] = {}
    requal_rel = next(path for path in evidence if "e6_smoke18_reuse_requalification" in path)
    requal = load_json_object(safe_project_path(root, requal_rel))
    if requal.get("status") != "PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE":
        raise OrchestratorError("UPSTREAM_REQUALIFICATION_STATUS_NOT_PASS")
    if requal.get("check_count") != 21 or requal.get("passed_checks") != 21 or requal.get("failed_checks") != 0:
        raise OrchestratorError("UPSTREAM_REQUALIFICATION_CHECK_COUNT_MISMATCH")
    summary = requal.get("candidate_summary", {})
    if summary.get("reconciled_reuse_candidates") != 13 or summary.get("e6_accepted") != 0 or summary.get("fresh_challenge_av_required") != 5:
        raise OrchestratorError("UPSTREAM_REQUALIFICATION_CANDIDATE_SUMMARY_MISMATCH")
    governance = requal.get("governance", {})
    if governance.get("d4_8") != "BLOCKED" or governance.get("d4_8_overridden") is not False or governance.get("renderer") != "OFF" or governance.get("release_authority") != "NONE":
        raise OrchestratorError("UPSTREAM_REQUALIFICATION_GOVERNANCE_MISMATCH")
    result["reuse_requalification"] = {"path": requal_rel, "sha256": evidence[requal_rel]["sha256"], "status": requal["status"]}

    plan_receipt_rel = next(path for path in evidence if path.endswith("E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json"))
    plan_receipt = load_json_object(safe_project_path(root, plan_receipt_rel))
    if plan_receipt.get("status") != "PASS_D9_MULTISELECTOR_CAPTURE_GROUP_PLAN_READY_EXECUTION_HELD":
        raise OrchestratorError("UPSTREAM_D9_PLAN_STATUS_NOT_PASS")
    if plan_receipt.get("linked_e1_intents") != 18 or plan_receipt.get("linked_d_envelopes") != 18 or plan_receipt.get("selected_challenge_groups") != 6:
        raise OrchestratorError("UPSTREAM_D9_PLAN_COUNTS_MISMATCH")
    if plan_receipt.get("execution", {}).get("processes_started") is not False or plan_receipt.get("execution", {}).get("batch_id_consumed") is not False:
        raise OrchestratorError("UPSTREAM_D9_PLAN_EXECUTION_BOUNDARY_MISMATCH")
    result["prior_d9_multiselector_plan"] = {"path": plan_receipt_rel, "sha256": evidence[plan_receipt_rel]["sha256"], "status": plan_receipt["status"]}

    contract_rel = next(path for path in evidence if path.endswith("E6_CHALLENGE_CONSUMER_CONTRACT_PREFLIGHT_RECEIPT_V1.json"))
    contract = load_json_object(safe_project_path(root, contract_rel))
    if contract.get("status") != "PASS_STATIC_CONSUMER_CONTRACT_18_OF_18_EXECUTION_HELD":
        raise OrchestratorError("UPSTREAM_CONSUMER_CONTRACT_STATUS_NOT_PASS")
    if contract.get("e1_intents", {}).get("passed") != 18 or contract.get("d_envelopes", {}).get("passed") != 18:
        raise OrchestratorError("UPSTREAM_CONSUMER_CONTRACT_COUNTS_MISMATCH")
    result["consumer_contract"] = {"path": contract_rel, "sha256": evidence[contract_rel]["sha256"], "status": contract["status"]}

    audit_rel = next(path for path in evidence if path.endswith("E6_SMOKE18_READONLY_AUDIT_RECEIPT_V2.json"))
    audit = load_json_object(safe_project_path(root, audit_rel))
    if audit.get("status") != "PASS_AUDIT_READ_ONLY_EVIDENCE_RECONCILED_EXECUTION_HELD":
        raise OrchestratorError("UPSTREAM_SMOKE18_AUDIT_STATUS_NOT_PASS")
    result["smoke18_readonly_audit"] = {"path": audit_rel, "sha256": evidence[audit_rel]["sha256"], "status": audit["status"]}
    return result


def _decimal_frames(duration: Any, fps: int, label: str) -> int:
    try:
        count = Decimal(str(duration)) * Decimal(fps)
    except Exception as exc:
        raise OrchestratorError(f"INVALID_TIMEBASE_DURATION:{label}") from exc
    if count < 0:
        raise OrchestratorError(f"NEGATIVE_TIMEBASE_DURATION:{label}")
    return int(count.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def validate_manifest(manifest: Mapping[str, Any]) -> None:
    _require_exact_keys(manifest, {"schema", "schema_version", "status", "selection", "request_template", "music_fixture", "scenario_groups", "execution_boundary"}, "MANIFEST")
    if manifest.get("schema") != MANIFEST_SCHEMA or manifest.get("schema_version") != "1.0":
        raise OrchestratorError("INPUT_MANIFEST_IDENTITY_MISMATCH")
    if manifest.get("status") != "DRAFT_PLAN_ONLY_NOT_FROZEN_NOT_EXECUTION_AUTHORITY":
        raise OrchestratorError("INPUT_MANIFEST_STATUS_MUST_REMAIN_DRAFT")

    selection = manifest.get("selection")
    if not isinstance(selection, Mapping):
        raise OrchestratorError("SELECTION_OBJECT_REQUIRED")
    _require_exact_keys(selection, {"decision", "candidate_selectors", "excluded_selectors", "expected_group_count", "expected_probe_count", "probe_variants", "probe_rows_are_subruns_not_additional_smoke18_scenarios"}, "SELECTION")
    if selection.get("decision") != "PROPOSAL_NOT_FROZEN":
        raise OrchestratorError("SELECTOR_SET_MUST_REMAIN_PROPOSAL_NOT_FROZEN")
    candidates = selection.get("candidate_selectors")
    if not isinstance(candidates, list) or len(candidates) != 7 or len(set(candidates)) != 7:
        raise OrchestratorError("CANDIDATE_SELECTOR_POOL_MUST_BE_EXPLICIT_SEVEN")
    if any(not isinstance(item, str) or not re.fullmatch(r"CHALLENGE_[0-9]{3}", item) for item in candidates):
        raise OrchestratorError("CANDIDATE_SELECTOR_FORMAT_INVALID")
    if selection.get("expected_group_count") != 6 or selection.get("expected_probe_count") != 18:
        raise OrchestratorError("MANIFEST_COUNTS_MUST_BE_SIX_GROUPS_EIGHTEEN_PROBES")
    if selection.get("probe_variants") != list(EXPECTED_PROBES) or selection.get("probe_rows_are_subruns_not_additional_smoke18_scenarios") is not True:
        raise OrchestratorError("PROBE_VARIANT_COUNTING_CONTRACT_MISMATCH")

    excluded = selection.get("excluded_selectors")
    if not isinstance(excluded, list) or not all(isinstance(x, Mapping) and isinstance(x.get("selector"), str) and isinstance(x.get("reason"), str) and x.get("reason") for x in excluded):
        raise OrchestratorError("EXCLUDED_SELECTOR_REASONS_MUST_BE_EXPLICIT")

    template = manifest.get("request_template")
    if not isinstance(template, Mapping):
        raise OrchestratorError("REQUEST_TEMPLATE_REQUIRED")
    _require_exact_keys(template, {"mode", "content_type", "delivery_profile_id", "presentation_profile_id", "variation_index", "audio_enabled", "personalization_enabled", "editorial_profile", "production_override", "presentation_options", "provenance"}, "REQUEST_TEMPLATE")
    required_strings = ("mode", "content_type", "delivery_profile_id", "presentation_profile_id")
    if any(not isinstance(template.get(key), str) or not template[key].strip() for key in required_strings):
        raise OrchestratorError("REQUEST_TEMPLATE_STRING_FIELD_MISSING")
    if template["content_type"] != "challenges":
        raise OrchestratorError("CHALLENGE_CONTENT_TYPE_REQUIRED")
    if template["mode"] != "REVIEW":
        raise OrchestratorError("PREPARE_ONLY_MODE_MUST_BE_REVIEW")
    _require_int(template.get("variation_index"), "variation_index", 0, 1000000)
    if type(template.get("audio_enabled")) is not bool or type(template.get("personalization_enabled")) is not bool:
        raise OrchestratorError("REQUEST_TEMPLATE_BOOLEAN_FIELD_MISSING")
    if not isinstance(template.get("editorial_profile"), Mapping) or not isinstance(template.get("production_override"), Mapping):
        raise OrchestratorError("EDITORIAL_PROFILE_AND_OVERRIDE_MUST_BE_OBJECTS")
    if template["editorial_profile"] or template["production_override"]:
        raise OrchestratorError("PREPARE_ONLY_MANIFEST_MUST_NOT_INJECT_EDITORIAL_OVERRIDES")
    options = template.get("presentation_options")
    if not isinstance(options, Mapping) or set(options) != {"show_hook_countdown"} or type(options.get("show_hook_countdown")) is not bool:
        raise OrchestratorError("PRESENTATION_OPTIONS_MUST_BE_EXPLICIT_BOOLEAN")
    provenance = template.get("provenance")
    if not isinstance(provenance, Mapping) or set(provenance) != {"source_revision", "request_origin"}:
        raise OrchestratorError("PROVENANCE_MUST_BE_EXPLICIT")
    if provenance.get("request_origin") != "TEST" or not isinstance(provenance.get("source_revision"), str) or not provenance["source_revision"]:
        raise OrchestratorError("PREPARE_ONLY_TEST_PROVENANCE_REQUIRED")

    music_fixture = manifest.get("music_fixture")
    if not isinstance(music_fixture, Mapping):
        raise OrchestratorError("MUSIC_FIXTURE_METADATA_REQUIRED")
    _require_exact_keys(music_fixture, {"profile_id", "profile_version", "tempo_bpm_proposal", "variation_index", "authority", "tempo_bpm_sent_to_e1", "duration_seconds_sent_to_e1", "e1_unresolved_parameters"}, "MUSIC_FIXTURE")
    if not isinstance(music_fixture.get("profile_id"), str) or not music_fixture["profile_id"] or not isinstance(music_fixture.get("profile_version"), str) or not music_fixture["profile_version"]:
        raise OrchestratorError("MUSIC_FIXTURE_PROFILE_MUST_BE_EXPLICIT")
    _require_int(music_fixture.get("tempo_bpm_proposal"), "tempo_bpm_proposal", 1, 400)
    _require_int(music_fixture.get("variation_index"), "music_fixture_variation_index", 0, 1000000)
    if music_fixture.get("authority") != "PROPOSAL_ONLY_NOT_AUTHORIZED" or music_fixture.get("tempo_bpm_sent_to_e1") is not False or music_fixture.get("duration_seconds_sent_to_e1") is not False:
        raise OrchestratorError("MUSIC_FIXTURE_AUTHORITY_OR_PARAMETER_BOUNDARY_INVALID")
    if music_fixture.get("e1_unresolved_parameters") != ["tempo_bpm", "duration_seconds"]:
        raise OrchestratorError("E1_MUSIC_PARAMETERS_MUST_REMAIN_UNRESOLVED")
    if music_fixture["variation_index"] != template["variation_index"]:
        raise OrchestratorError("MUSIC_FIXTURE_VARIATION_MISMATCH")

    groups = manifest.get("scenario_groups")
    if not isinstance(groups, list) or len(groups) != 6:
        raise OrchestratorError("EXACTLY_SIX_SCENARIO_GROUPS_REQUIRED")
    selectors: list[str] = []
    gameplay_seeds: list[int] = []
    mechanics: list[str] = []
    probe_count = 0
    for index, group in enumerate(groups):
        if not isinstance(group, Mapping):
            raise OrchestratorError(f"SCENARIO_GROUP_{index}_MUST_BE_OBJECT")
        _require_exact_keys(group, {"scenario_id", "selector", "canonical_definition_path", "canonical_definition_sha256", "mechanic", "gameplay_seed", "source_timebase", "music_seed_authority", "probes"}, f"SCENARIO_GROUP_{index}")
        selector = group.get("selector")
        if not isinstance(selector, str) or selector not in candidates or not re.fullmatch(r"CHALLENGE_[0-9]{3}", selector):
            raise OrchestratorError(f"UNKNOWN_OR_UNAPPROVED_SELECTOR:{selector!r}")
        if group.get("scenario_id") != f"E6-CH-{selector[-3:]}" or group.get("canonical_definition_path") != f"challenges/{selector}.json":
            raise OrchestratorError(f"CANONICAL_DEFINITION_PATH_OR_SCENARIO_ID_MISMATCH:{selector}")
        _require_sha(group.get("canonical_definition_sha256"), f"DEFINITION:{selector}")
        if not isinstance(group.get("mechanic"), str) or not group["mechanic"].strip():
            raise OrchestratorError(f"MECHANIC_MUST_BE_EXPLICIT:{selector}")
        gameplay = _require_int(group.get("gameplay_seed"), f"GAMEPLAY_SEED:{selector}")
        if group.get("music_seed_authority") != "PROPOSAL_ONLY_NOT_AUTHORIZED":
            raise OrchestratorError(f"MUSIC_SEED_AUTHORITY_NOT_PROPOSAL_ONLY:{selector}")
        timebase = group.get("source_timebase")
        if not isinstance(timebase, Mapping):
            raise OrchestratorError(f"SOURCE_TIMEBASE_REQUIRED:{selector}")
        _require_exact_keys(timebase, {"fps", "duration_seconds", "frames"}, f"TIMEBASE:{selector}")
        fps = _require_int(timebase.get("fps"), f"FPS:{selector}", 1, 240)
        frames = _require_int(timebase.get("frames"), f"FRAMES:{selector}", 1, 1000000)
        try:
            duration = Decimal(str(timebase.get("duration_seconds")))
        except Exception as exc:
            raise OrchestratorError(f"DURATION_SECONDS_INVALID:{selector}") from exc
        if duration <= 0 or not duration.is_finite() or _decimal_frames(duration, fps, selector) != frames:
            raise OrchestratorError(f"DECLARED_TIMEBASE_ARITHMETIC_MISMATCH:{selector}")
        probes = group.get("probes")
        if not isinstance(probes, list) or len(probes) != 3:
            raise OrchestratorError(f"EXACTLY_THREE_PROBES_REQUIRED:{selector}")
        observed_labels = []
        observed_music = []
        for probe in probes:
            if not isinstance(probe, Mapping):
                raise OrchestratorError(f"PROBE_MUST_BE_OBJECT:{selector}")
            _require_exact_keys(probe, {"variant", "music_seed", "music_seed_status"}, f"PROBE:{selector}")
            label = probe.get("variant")
            if label not in EXPECTED_PROBES:
                raise OrchestratorError(f"UNKNOWN_PROBE_VARIANT:{selector}:{label!r}")
            seed = _require_int(probe.get("music_seed"), f"MUSIC_SEED:{selector}:{label}")
            if probe.get("music_seed_status") != "PROPOSAL_ONLY_NOT_AUTHORIZED":
                raise OrchestratorError(f"MUSIC_SEED_NOT_EXPLICITLY_PROPOSAL_ONLY:{selector}:{label}")
            observed_labels.append(label)
            observed_music.append(seed)
        if tuple(observed_labels) != EXPECTED_PROBES:
            raise OrchestratorError(f"PROBE_ORDER_OR_IDENTITY_MISMATCH:{selector}")
        if observed_music[0] != observed_music[1] or observed_music[0] == observed_music[2]:
            raise OrchestratorError(f"A_B_C_MUSIC_SEED_RELATION_INVALID:{selector}")
        selectors.append(selector)
        gameplay_seeds.append(gameplay)
        mechanics.append(group["mechanic"])
        probe_count += len(probes)
    if len(set(selectors)) != 6:
        raise OrchestratorError("DUPLICATE_CHALLENGE_SELECTOR")
    if len(set(gameplay_seeds)) != 6:
        raise OrchestratorError("GAMEPLAY_SEEDS_MUST_BE_DISTINCT_ACROSS_SIX_GROUPS")
    if len(set(mechanics)) != 6:
        raise OrchestratorError("MECHANICS_MUST_BE_DISTINCT_ACROSS_SIX_GROUPS")
    if probe_count != 18:
        raise OrchestratorError("EXACTLY_EIGHTEEN_CHALLENGE_PROBES_REQUIRED")

    boundary = manifest.get("execution_boundary")
    required_boundary = {
        "mode": "PREPARE_ONLY", "dispatch_authorized": False, "renderer_activation": False,
        "production_execution": False, "media_authorized": False, "godot_invoked": False,
        "ffmpeg_invoked": False, "ffprobe_invoked": False, "audio_generated": False,
        "mux_invoked": False, "batch_id_consumed": False, "release_authority": "NONE", "d4_8": "BLOCKED"
    }
    if not isinstance(boundary, Mapping) or dict(boundary) != required_boundary:
        raise OrchestratorError("EXECUTION_BOUNDARY_MUST_BE_EXACT_PREPARE_ONLY")


def validate_definition_against_group(root: Path, group: Mapping[str, Any], producer_schema: Mapping[str, Any], pin_map: Mapping[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    selector = group["selector"]
    relative = group["canonical_definition_path"]
    expected_sha = _require_sha(group["canonical_definition_sha256"], f"DEFINITION:{selector}")
    if pin_map.get(relative) != expected_sha:
        raise OrchestratorError(f"MANIFEST_DEFINITION_HASH_DOES_NOT_MATCH_SOURCE_PIN:{selector}")
    path = safe_project_path(root, relative)
    actual_sha = sha256_file(path)
    if actual_sha != expected_sha:
        raise OrchestratorError(f"CANONICAL_DEFINITION_HASH_MISMATCH:{selector}:{actual_sha}")
    definition = load_json_object(path)
    if definition.get("challenge_id") != selector:
        raise OrchestratorError(f"CANONICAL_DEFINITION_IDENTITY_MISMATCH:{selector}")
    if definition.get("mechanic") != group["mechanic"]:
        raise OrchestratorError(f"CANONICAL_DEFINITION_MECHANIC_MISMATCH:{selector}")
    if definition.get("generation", {}).get("seed") != group["gameplay_seed"]:
        raise OrchestratorError(f"CANONICAL_GAMEPLAY_SEED_MISMATCH:{selector}")
    video = definition.get("video")
    if not isinstance(video, Mapping):
        raise OrchestratorError(f"CANONICAL_VIDEO_BLOCK_MISSING:{selector}")
    fps = video.get("fps")
    if isinstance(fps, bool) or not isinstance(fps, int):
        raise OrchestratorError(f"CANONICAL_FPS_INVALID:{selector}")
    durations = []
    phase_ranges = []
    cursor = 0
    total = Decimal("0")
    for phase, field in PHASE_FIELDS:
        if field not in video:
            raise OrchestratorError(f"CANONICAL_PHASE_DURATION_MISSING:{selector}:{field}")
        value = video[field]
        phase_seconds = Decimal(str(value))
        if not phase_seconds.is_finite() or phase_seconds < 0:
            raise OrchestratorError(f"CANONICAL_PHASE_DURATION_NONFINITE_OR_NEGATIVE:{selector}:{field}")
        count = _decimal_frames(value, fps, f"{selector}.{field}")
        phase_ranges.append({"phase": phase, "start_frame": cursor, "end_frame": cursor + count, "timebase": "SOURCE_FPS_HALF_OPEN"})
        durations.append({"phase": phase, "duration_seconds": float(phase_seconds), "frames": count})
        cursor += count
        total += phase_seconds
    tb = group["source_timebase"]
    if fps != tb["fps"] or cursor != tb["frames"] or total != Decimal(str(tb["duration_seconds"])):
        raise OrchestratorError(f"CANONICAL_TIMEBASE_MISMATCH:{selector}")
    if _decimal_frames(total, fps, selector) != cursor:
        raise OrchestratorError(f"CANONICAL_PHASE_SUM_FRAME_MISMATCH:{selector}")
    schema_rows = {str(row.get("id")): row for row in producer_schema.get("challenges", []) if isinstance(row, Mapping)}
    schema_row = schema_rows.get(selector)
    if not isinstance(schema_row, Mapping):
        raise OrchestratorError(f"PRODUCER_SCHEMA_CHALLENGE_ROW_MISSING:{selector}")
    if schema_row.get("mechanic") != group["mechanic"] or schema_row.get("default_seed") != group["gameplay_seed"] or schema_row.get("fps") != fps:
        raise OrchestratorError(f"PRODUCER_SCHEMA_IDENTITY_MISMATCH:{selector}")
    if Decimal(str(schema_row.get("duration_seconds"))) != total:
        raise OrchestratorError(f"PRODUCER_SCHEMA_DURATION_MISMATCH:{selector}")
    return definition, phase_ranges


def import_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError(f"MODULE_LOAD_FAILED:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def validate_e1_and_envelope(intent: Mapping[str, Any], envelope: Mapping[str, Any], service_validation: Mapping[str, Any], group: Mapping[str, Any], probe: Mapping[str, Any], template: Mapping[str, Any], phase_ranges: list[dict[str, Any]], plan_builder: Any) -> None:
    selector = group["selector"]
    gameplay_seed = group["gameplay_seed"]
    music_seed = probe["music_seed"]
    plan_builder.validate_e1_intent(intent, selector, gameplay_seed, music_seed, service_validation)
    if intent.get("delivery", {}).get("requested_profile_id") != template["delivery_profile_id"]:
        raise OrchestratorError(f"E1_DELIVERY_PROFILE_MISMATCH:{selector}")
    if intent.get("delivery", {}).get("presentation_profile_id") != template["presentation_profile_id"]:
        raise OrchestratorError(f"E1_PRESENTATION_PROFILE_MISMATCH:{selector}")
    if intent.get("delivery", {}).get("audio_enabled") is not template["audio_enabled"]:
        raise OrchestratorError(f"E1_AUDIO_FLAG_MISMATCH:{selector}")
    music = intent.get("music_contract", {})
    fixture = getattr(plan_builder, "_e6_expected_music_fixture", None)
    del fixture  # no global fixture/default is consulted; explicit manifest is checked by caller.
    if music.get("engine_request", {}).get("music_seed") != music_seed:
        raise OrchestratorError(f"E1_MUSIC_SEED_BINDING_MISMATCH:{selector}")
    if music.get("unresolved_engine_parameters") != ["tempo_bpm", "duration_seconds"]:
        raise OrchestratorError(f"E1_MUSIC_PARAMETER_BOUNDARY_MISMATCH:{selector}")
    if music.get("engine_request", {}).get("tempo_bpm") is not None or music.get("engine_request", {}).get("duration_seconds") is not None:
        raise OrchestratorError(f"E1_MUSIC_ENGINE_PARAMETERS_MUST_REMAIN_NULL:{selector}")
    request = intent.get("request", {})
    if request.get("presentation_options") != template["presentation_options"]:
        raise OrchestratorError(f"E1_PRESENTATION_OPTIONS_NOT_FROM_MANIFEST:{selector}")
    if envelope.get("challenge_id") != selector:
        raise OrchestratorError(f"D_ENVELOPE_SELECTOR_MISMATCH:{selector}")
    if envelope.get("intent_hash") != intent.get("identity", {}).get("intent_hash"):
        raise OrchestratorError(f"D_ENVELOPE_INTENT_HASH_MISMATCH:{selector}")
    if envelope.get("source_timebase") != {"fps": group["source_timebase"]["fps"], "total_frames": group["source_timebase"]["frames"], "kind": "SOURCE_FRAME_INDEX"}:
        raise OrchestratorError(f"D_ENVELOPE_TIMEBASE_MISMATCH:{selector}")
    if envelope.get("source_phase_ranges") != phase_ranges:
        raise OrchestratorError(f"D_ENVELOPE_PHASE_RANGES_MISMATCH:{selector}")
    boundary = envelope.get("governance", {})
    if boundary.get("production_dispatch") is not False or boundary.get("media_created") is not False or boundary.get("renderer_input_emitted") is not False or boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED":
        raise OrchestratorError(f"D_ENVELOPE_GOVERNANCE_BOUNDARY_MISMATCH:{selector}")


def write_exclusive(path: Path, content: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(content)
            handle.flush()
    except FileExistsError as exc:
        raise OrchestratorError(f"OUTPUT_COLLISION_NO_OVERWRITE:{path}") from exc
    return sha256_file(path)


def write_json_exclusive(path: Path, value: Any) -> str:
    payload = canonical_json_bytes(value)
    digest = write_exclusive(path, payload)
    sidecar = path.with_suffix(path.suffix + ".sha256")
    write_exclusive(sidecar, f"{digest}  {path.name}\n".encode("ascii"))
    return digest


def run_orchestrator(project_root: Path, run_id: str) -> dict[str, Any]:
    root = project_root.resolve(strict=True)
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise OrchestratorError("RUN_ID_FORMAT_INVALID; THIS IS AN EVIDENCE_RUN_ID_NOT_A_BATCH_ID")

    pins_doc, pins_pre = verify_pins_document(root)
    upstream = verify_upstream_evidence(root, pins_doc)
    manifest_path = safe_project_path(root, pins_doc["input_manifest_path"])
    if sha256_file(manifest_path) != pins_doc["input_manifest_sha256"]:
        raise OrchestratorError("INPUT_MANIFEST_SHA256_MISMATCH")
    manifest = load_json_object(manifest_path)
    validate_manifest(manifest)

    source_pin_map = {row["path"]: row["sha256"] for row in pins_doc["checkout_files"]}
    producer_schema_path = safe_project_path(root, "c11c-suite/c11c-producer/producer_schema.json")
    producer_schema = load_json_object(producer_schema_path)
    if producer_schema.get("challenge_timing_policy") != "phase_sum_only; legacy total_duration is ignored":
        raise OrchestratorError("PRODUCER_SCHEMA_TIMING_POLICY_MISMATCH")

    prepared_groups: list[dict[str, Any]] = []
    for group in manifest["scenario_groups"]:
        definition, phase_ranges = validate_definition_against_group(root, group, producer_schema, source_pin_map)
        prepared_groups.append({"group": group, "definition": definition, "phase_ranges": phase_ranges})

    service_path = safe_project_path(root, "c11c-suite/c11c-producer/c11e_production_service.py")
    helper_path = safe_project_path(root, "tools/c11d/d9/c11e_e6_challenge_plan_only_v1.py")
    service = import_from_path("c11e_e6_prepare_only_service_v1", service_path)
    resolver = service._load_d9_resolver(root)
    plan_builder = import_from_path("c11e_e6_prepare_only_existing_plan_builder_v1", helper_path)

    output_root = safe_project_path(root, OUTPUT_REL)
    run_dir = output_root / run_id
    if run_dir.exists():
        raise OrchestratorError(f"OUTPUT_RUN_DIRECTORY_ALREADY_EXISTS:{run_dir}")

    e1_records: list[dict[str, Any]] = []
    envelope_records: list[dict[str, Any]] = []
    group_records: list[dict[str, Any]] = []
    outputs: list[tuple[str, dict[str, Any], str]] = []
    template = manifest["request_template"]
    fixture = manifest["music_fixture"]

    for prepared_group in prepared_groups:
        group = prepared_group["group"]
        definition = prepared_group["definition"]
        phase_ranges = prepared_group["phase_ranges"]
        selector = group["selector"]
        group_intents: list[dict[str, Any]] = []
        for probe in group["probes"]:
            request_id = f"{run_id}-{selector}-{probe['variant']}"
            raw_request = {
                "schema": resolver.REQUEST_SCHEMA_ID,
                "schema_version": "1.0",
                "request_id": request_id,
                "mode": template["mode"],
                "selection": {
                    "content_type": template["content_type"],
                    "family_id": group["mechanic"],
                    "variant_id": selector,
                },
                "seed": group["gameplay_seed"],
                "music_seed": probe["music_seed"],
                "delivery_profile_id": template["delivery_profile_id"],
                "presentation_profile_id": template["presentation_profile_id"],
                "variation_index": template["variation_index"],
                "audio_enabled": template["audio_enabled"],
                "personalization_enabled": template["personalization_enabled"],
                "editorial_profile": dict(template["editorial_profile"]),
                "production_override": dict(template["production_override"]),
                "presentation_options": dict(template["presentation_options"]),
                "provenance": dict(template["provenance"]),
            }
            prepared = service.prepare_c11e_production_intent(
                raw_request, root, request_origin=template["provenance"]["request_origin"], resolver_module=resolver
            )
            intent = prepared.get("intent")
            if not isinstance(intent, Mapping):
                raise OrchestratorError(f"E1_INTENT_NOT_RETURNED:{selector}:{probe['variant']}")
            service_validation = service.validate_c11e_production_intent(intent, root)
            if service_validation.get("status") != "PASS_E1_PREPARATION_ONLY" or service_validation.get("valid") is not True:
                raise OrchestratorError(f"E1_SERVICE_VALIDATION_FAILED:{selector}:{probe['variant']}")
            music_contract = intent.get("music_contract", {})
            engine = music_contract.get("engine", {})
            style_profile = music_contract.get("style_profile", {})
            if style_profile.get("profile_id") != fixture["profile_id"] or style_profile.get("profile_version") != fixture["profile_version"]:
                raise OrchestratorError(f"E1_MUSIC_PROFILE_IDENTITY_DIFFERS_FROM_EXPLICIT_FIXTURE:{selector}")
            if music_contract.get("engine_invoked") is not False or music_contract.get("audio_created") is not False or music_contract.get("dispatchable") is not False:
                raise OrchestratorError(f"E1_MUSIC_EXECUTION_BOUNDARY_CROSSED:{selector}")
            envelope = plan_builder.build_envelope(root, intent, definition)
            plan_builder.validate_envelope_static(envelope, selector, group["source_timebase"]["frames"], group["source_timebase"]["fps"])
            validate_e1_and_envelope(intent, envelope, service_validation, group, probe, template, phase_ranges, plan_builder)

            stem = f"{selector}_{probe['variant']}"
            intent_rel = f"intents/{stem}_E1_INTENT.json"
            envelope_rel = f"envelopes/{stem}_D_ENVELOPE.json"
            intent_sha = sha256_bytes(canonical_json_bytes(dict(intent)))
            envelope_sha = sha256_bytes(canonical_json_bytes(envelope))
            outputs.append((intent_rel, dict(intent), intent_sha))
            outputs.append((envelope_rel, envelope, envelope_sha))
            e1_row = {
                "selector": selector, "scenario_id": group["scenario_id"], "variant": probe["variant"],
                "request_id": request_id, "gameplay_seed": group["gameplay_seed"], "music_seed": probe["music_seed"],
                "music_seed_authority": probe["music_seed_status"], "validation_status": service_validation["status"],
                "intent_sha256": intent_sha, "relative_path": intent_rel,
                "unresolved_music_parameters": music_contract.get("unresolved_engine_parameters"),
            }
            envelope_row = {
                "selector": selector, "scenario_id": group["scenario_id"], "variant": probe["variant"],
                "request_id": request_id, "intent_hash": envelope["intent_hash"],
                "envelope_sha256": envelope_sha, "relative_path": envelope_rel,
                "source_fps": envelope["source_timebase"]["fps"], "source_frames": envelope["source_timebase"]["total_frames"],
                "static_validation": "PASS_SCHEMA_IDENTITY_TIMEBASE_PHASES_GOVERNANCE",
            }
            e1_records.append(e1_row)
            envelope_records.append(envelope_row)
            group_intents.append({"variant": probe["variant"], "intent_sha256": intent_sha, "envelope_sha256": envelope_sha})
        group_records.append({
            "scenario_id": group["scenario_id"], "selector": selector, "mechanic": group["mechanic"],
            "canonical_definition_path": group["canonical_definition_path"],
            "canonical_definition_sha256": group["canonical_definition_sha256"],
            "gameplay_seed": group["gameplay_seed"], "source_timebase": dict(group["source_timebase"]),
            "phase_ranges": phase_ranges, "probes": group_intents,
            "scenario_status": "PREPARED_ONLY_NOT_E6_ACCEPTED",
        })

    if len(e1_records) != 18 or len(envelope_records) != 18 or len(group_records) != 6:
        raise OrchestratorError("PREPARE_ONLY_OUTPUT_COUNTS_INVALID")

    # All validation is complete before the first evidence write.
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "intents").mkdir()
    (run_dir / "envelopes").mkdir()
    input_copy_rel = "INPUT_MANIFEST_PINNED_V1.json"
    shutil_copy_bytes = manifest_path.read_bytes()
    input_copy_path = run_dir / input_copy_rel
    input_copy_sha = write_exclusive(input_copy_path, shutil_copy_bytes)
    if input_copy_sha != pins_doc["input_manifest_sha256"]:
        raise OrchestratorError("COPIED_INPUT_MANIFEST_HASH_MISMATCH")
    write_exclusive(
        input_copy_path.with_suffix(input_copy_path.suffix + ".sha256"),
        f"{input_copy_sha}  {input_copy_path.name}\n".encode("ascii"),
    )

    file_outputs: list[dict[str, Any]] = []
    for relative, value, expected_sha in outputs:
        full = run_dir / relative
        actual_sha = write_json_exclusive(full, value)
        if actual_sha != expected_sha:
            raise OrchestratorError(f"OUTPUT_POSTWRITE_HASH_MISMATCH:{relative}")
        file_outputs.append({"path": f"{OUTPUT_REL}/{run_id}/{relative}", "sha256": actual_sha, "bytes": full.stat().st_size})

    pins_post = verify_pin_rows(root, pins_doc["checkout_files"] + pins_doc["upstream_evidence_files"])
    if [(x["path"], x["sha256"], x["bytes"]) for x in pins_pre] != [(x["path"], x["sha256"], x["bytes"]) for x in pins_post]:
        raise OrchestratorError("SOURCE_PINS_CHANGED_DURING_PREPARATION")

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "schema_version": "1.0",
        "status": "PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD",
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "scope": "E6_CHALLENGE_SIX_SELECTOR_D9_PREPARE_ONLY_ORCHESTRATOR",
        "input_manifest": {
            "path": pins_doc["input_manifest_path"],
            "sha256": pins_doc["input_manifest_sha256"],
            "copy_path": f"{OUTPUT_REL}/{run_id}/{input_copy_rel}",
            "copy_sha256": input_copy_sha,
            "copy_sidecar": f"{OUTPUT_REL}/{run_id}/{input_copy_rel}.sha256",
            "status": manifest["status"],
            "selection_decision": manifest["selection"]["decision"],
        },
        "source_pin_document": {"path": PINS_REL, "sha256": PINS_SHA256, "checkout_pins": len(pins_doc["checkout_files"]), "upstream_evidence_pins": len(pins_doc["upstream_evidence_files"]), "pre_post_equal": True},
        "source_pins_pre": pins_pre,
        "source_pins_post": pins_post,
        "upstream_evidence": upstream,
        "counts": {"challenge_scenario_groups": 6, "challenge_probe_subruns": 18, "e1_intents": len(e1_records), "d_envelopes": len(envelope_records), "smoke18_top_level_scenarios": 6},
        "challenge_groups": group_records,
        "e1_intents": {"expected": 18, "passed": 18, "rows": e1_records},
        "d_envelopes": {"expected": 18, "passed": 18, "validation": "EXISTING_PLAN_ONLY_BUILDER_STATIC_SCHEMA_IDENTITY_TIMEBASE_PHASES_GOVERNANCE", "rows": envelope_records},
        "music_fixture": {"profile_id": fixture["profile_id"], "profile_version": fixture["profile_version"], "tempo_bpm_proposal": fixture["tempo_bpm_proposal"], "authority": fixture["authority"], "tempo_bpm_sent_to_e1": False, "duration_seconds_sent_to_e1": False, "e1_unresolved_parameters": ["tempo_bpm", "duration_seconds"]},
        "written_evidence_files": file_outputs,
        "execution": {"mode": "PREPARE_ONLY", "e6_test_only_authorized": False, "godot_invoked": False, "renderer_invoked": False, "ffmpeg_invoked": False, "ffprobe_invoked": False, "audio_generated": False, "mux_invoked": False, "media_created": False, "production_dispatch": False, "batch_id_consumed": False, "runtime_commands_emitted": False, "release_authority": "NONE"},
        "governance": {"e1": "PREPARE_ONLY", "d4_8": "BLOCKED", "d4_8_overridden": False, "renderer": "OFF", "production_dispatch": False, "production_media": False, "e6_accepted_scenarios": 0, "e6_matrix_frozen": False, "release_authority": "NONE", "git_checks": "SKIPPED", "commits": "OPERATOR_MANAGED", "source_file_pins": "ENFORCED"},
        "limitations": ["This receipt proves E1 preparation and static D envelopes only; it does not prove Godot runtime or media output.", "The selector set remains a proposal and is not frozen by this overlay.", "Music seeds and tempo are proposal-only; E1 tempo_bpm and duration_seconds remain null.", "D4.8 conflict is unchanged; no media execution authority is granted."],
    }
    receipt_path = run_dir / "E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json"
    receipt_sha = write_json_exclusive(receipt_path, receipt)
    plan = {
        "schema": "C11E-E6-CHALLENGE-PREPARE-ONLY-PLAN-V1",
        "status": "PREPARED_ONLY_NOT_FROZEN_NOT_E6_ACCEPTED",
        "run_id": run_id,
        "receipt_sha256": receipt_sha,
        "challenge_groups": group_records,
        "e1_intents": e1_records,
        "d_envelopes": envelope_records,
        "execution": receipt["execution"],
        "governance": receipt["governance"],
    }
    plan_sha = write_json_exclusive(run_dir / "E6_CHALLENGE_PREPARE_ONLY_PLAN_V1.json", plan)

    print("E6_CHALLENGE_PREPARE_ONLY_STATUS=PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD")
    print(f"E6_CHALLENGE_PREPARE_ONLY_RUN_ID={run_id}")
    print("E6_CHALLENGE_GROUPS=6/6")
    print("E6_CHALLENGE_PROBE_SUBRUNS=18/18")
    print("E6_E1_INTENTS=18/18_PASS_E1_PREPARATION_ONLY")
    print("E6_D_ENVELOPES=18/18_PASS_STATIC_SCHEMA_IDENTITY_TIMEBASE")
    print("E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; MUSIC_FIXTURES=PROPOSAL_ONLY_NOT_AUTHORIZED")
    print("D4_8=BLOCKED; RENDERER=OFF; RELEASE_AUTHORITY=NONE")
    print("GODOT=NOT_INVOKED; FFMPEG=NOT_INVOKED; FFPROBE=NOT_INVOKED; AUDIO=NOT_GENERATED; MUX=NOT_INVOKED; BATCH_ID=NOT_CONSUMED")
    print(f"RECEIPT_RELATIVE_PATH={OUTPUT_REL}/{run_id}/{receipt_path.name}")
    print(f"RECEIPT_SHA256={receipt_sha}")
    print(f"PLAN_SHA256={plan_sha}")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    try:
        run_orchestrator(Path(args.project_root), args.run_id)
    except Exception as exc:
        print(f"E6_CHALLENGE_PREPARE_ONLY_STATUS=BLOCKED:{type(exc).__name__}:{exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
