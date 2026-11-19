#!/usr/bin/env python3
"""E6 Challenge family editorial binding: PREPARE_ONLY, no media execution."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INPUTS_REL = Path("definitions/c11e/test_only/C11E_E6_CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY_INPUTS_V1.json")
INPUTS_SHA256 = "9750c12f08bdbb55505e4f800699003be73a360f36941c946495cc9323dae95a"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
EXPECTED_SELECTORS = ("CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007")
EXPECTED_VARIANTS = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
EXPECTED_FIELDS = ("title", "subtitle", "player_name", "challenge_label", "call_to_action", "language")
RENDERABLE_FIELDS = ("title", "subtitle", "call_to_action")
EXPECTED_REGIONS = {"title": "HEADER", "subtitle": "HEADER", "player_name": "CHALLENGE_OVERLAY", "challenge_label": "CHALLENGE_OVERLAY", "call_to_action": "FOOTER", "language": None}
EXPECTED_WINDOWS = {"title": ["HOOK"], "subtitle": ["HOOK"], "player_name": ["HOOK", "GAME"], "challenge_label": ["HOOK", "GAME"], "call_to_action": ["CTA"], "language": []}
READY = "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
OMITTED = "OMITTED_EMPTY"
BLOCKED = "BLOCKED_GEOMETRY_UNRESOLVED"
METADATA = "METADATA_ONLY"

class BindingError(RuntimeError):
    pass

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BindingError(f"JSON_READ_FAILED:{path}:{type(exc).__name__}:{exc}") from exc

def verify_sidecar(path: Path, expected_sha: str) -> None:
    sidecar = Path(str(path) + ".sha256")
    if not sidecar.is_file():
        raise BindingError(f"SIDECAR_MISSING:{sidecar}")
    text = sidecar.read_text(encoding="ascii").strip()
    match = re.fullmatch(r"([0-9a-fA-F]{64})(?:\s+.+)?", text)
    if not match or match.group(1).lower() != expected_sha.lower():
        raise BindingError(f"SIDECAR_MISMATCH:{sidecar}")

def verify_pin(root: Path, pin: dict[str, Any]) -> None:
    rel = str(pin.get("path", ""))
    if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts or "\\" in rel or ":" in rel:
        raise BindingError(f"UNSAFE_PIN_PATH:{rel}")
    path = root / Path(rel)
    if not path.is_file():
        raise BindingError(f"PIN_FILE_MISSING:{rel}")
    size = path.stat().st_size
    digest = sha256_file(path)
    if size != int(pin["bytes"]) or digest != str(pin["sha256"]).lower():
        raise BindingError(f"SOURCE_PIN_MISMATCH:{rel}:bytes={size}:sha256={digest}")

def phase_index(envelope: dict[str, Any]) -> dict[str, dict[str, Any]]:
    timebase = envelope.get("source_timebase")
    if not isinstance(timebase, dict) or int(timebase.get("fps", -1)) != 60 or int(timebase.get("total_frames", -1)) <= 0:
        raise BindingError("SOURCE_TIMEBASE_INVALID")
    total = int(timebase["total_frames"])
    rows = envelope.get("source_phase_ranges")
    if not isinstance(rows, list) or len(rows) != 4:
        raise BindingError("SOURCE_PHASE_RANGE_SET_INVALID")
    result: dict[str, dict[str, Any]] = {}
    cursor = 0
    for row in rows:
        if not isinstance(row, dict):
            raise BindingError("SOURCE_PHASE_RANGE_ROW_INVALID")
        phase = str(row.get("phase", ""))
        start = int(row.get("start_frame", -1))
        end = int(row.get("end_frame", -1))
        if phase not in ("HOOK", "GAME", "REVEAL", "CTA") or phase in result:
            raise BindingError(f"SOURCE_PHASE_NAME_INVALID:{phase}")
        if start != cursor or end < start or end > total or str(row.get("timebase", "")) != "SOURCE_FPS_HALF_OPEN":
            raise BindingError(f"SOURCE_PHASE_RANGE_INVALID:{phase}:{start}:{end}:{cursor}")
        result[phase] = row
        cursor = end
    if set(result) != {"HOOK", "GAME", "REVEAL", "CTA"} or cursor != total:
        raise BindingError("SOURCE_PHASE_COVERAGE_INVALID")
    return result

def expected_field_ranges(field_name: str, phase_rows: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for phase in EXPECTED_WINDOWS[field_name]:
        source = phase_rows[phase]
        rows.append({
            "phase": phase,
            "start_frame": int(source["start_frame"]),
            "end_frame": int(source["end_frame"]),
            "timebase": "SOURCE_FPS_HALF_OPEN",
        })
    return rows

def bind_envelope(envelope: dict[str, Any], editorial: dict[str, str], policy_sha: str, layout_sha: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind test copy only inside non-empty approved phase intervals; zero-width means suppress."""
    result = copy.deepcopy(envelope)
    if result.get("schema") != "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1" or result.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise BindingError("ENVELOPE_SCHEMA_OR_STATUS_INVALID")
    if result.get("content_type") != "challenges":
        raise BindingError("ENVELOPE_NOT_CHALLENGE")
    if result.get("policy_sha256") != policy_sha or result.get("layout_contract_sha256") != layout_sha:
        raise BindingError("ENVELOPE_POLICY_OR_LAYOUT_PIN_MISMATCH")
    phases = phase_index(result)
    rows = result.get("fields")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_FIELDS):
        raise BindingError("ENVELOPE_FIELD_SET_INVALID")
    by_name: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise BindingError("ENVELOPE_FIELD_ROW_INVALID")
        name = str(row.get("field", ""))
        if name not in EXPECTED_FIELDS or name in by_name:
            raise BindingError(f"ENVELOPE_FIELD_NAME_INVALID:{name}")
        by_name[name] = row
    if set(by_name) != set(EXPECTED_FIELDS):
        raise BindingError("ENVELOPE_FIELD_ALLOWLIST_MISMATCH")

    visible: list[str] = []
    suppressed: list[str] = []
    for name in RENDERABLE_FIELDS:
        row = by_name[name]
        expected_windows = EXPECTED_WINDOWS[name]
        if row.get("region") != EXPECTED_REGIONS[name] or row.get("source_phase_windows") != expected_windows:
            raise BindingError(f"FIELD_POLICY_WINDOW_MISMATCH:{name}")
        if row.get("policy_sha256") != policy_sha or row.get("layout_contract_sha256") != layout_sha:
            raise BindingError(f"FIELD_POLICY_PIN_MISMATCH:{name}")
        expected_ranges = expected_field_ranges(name, phases)
        if row.get("source_frame_ranges") != expected_ranges:
            raise BindingError(f"FIELD_SOURCE_RANGE_MISMATCH:{name}")
        value = str(editorial.get(name, "")).strip()
        if not value:
            raise BindingError(f"TEST_FIXTURE_VALUE_EMPTY:{name}")
        # A zero-length canonical interval is a deliberate no-display instruction.
        # Do not move it to GAME, CTA, or any other phase.
        active_frames = sum(int(item["end_frame"]) - int(item["start_frame"]) for item in expected_ranges)
        if active_frames == 0:
            row["disposition"] = OMITTED
            row["effective_value"] = ""
            row["value_sha256"] = EMPTY_SHA256
            suppressed.append(name)
        else:
            row["disposition"] = READY
            row["effective_value"] = value
            row["value_sha256"] = sha256_bytes(value.encode("utf-8"))
            visible.append(name)

    # Identity/metadata fields are not part of the synthetic visual fixture.
    for name in ("player_name", "challenge_label"):
        row = by_name[name]
        if row.get("source_phase_windows") != EXPECTED_WINDOWS[name] or row.get("region") != EXPECTED_REGIONS[name]:
            raise BindingError(f"BLOCKED_IDENTITY_FIELD_POLICY_MISMATCH:{name}")
        if str(row.get("effective_value", "")) not in ("", "UNKNOWN"):
            raise BindingError(f"IDENTITY_FIELD_MUST_REMAIN_UNKNOWN:{name}")
        if row.get("disposition") not in (OMITTED, BLOCKED):
            raise BindingError(f"IDENTITY_FIELD_DISPOSITION_INVALID:{name}")
    language = by_name["language"]
    if language.get("disposition") not in (OMITTED, METADATA) or str(language.get("effective_value", "")) not in ("", "UNKNOWN", "es"):
        raise BindingError("LANGUAGE_FIELD_MUST_REMAIN_NON_VISUAL")

    return result, {
        "visible_fields": visible,
        "suppressed_zero_window_fields": suppressed,
        "hook_frames": int(phases["HOOK"]["end_frame"]) - int(phases["HOOK"]["start_frame"]),
        "cta_frames": int(phases["CTA"]["end_frame"]) - int(phases["CTA"]["start_frame"]),
    }

def validate_seed_isolation(seed_rows: dict[str, dict[str, int]]) -> None:
    if set(seed_rows) != set(EXPECTED_VARIANTS):
        raise BindingError("SEED_VARIANT_SET_INVALID")
    a = seed_rows["A"]
    b = seed_rows["B_REPEAT"]
    c = seed_rows["C_CHANGED_MUSIC_SEED"]
    if a["gameplay"] != b["gameplay"] or a["gameplay"] != c["gameplay"]:
        raise BindingError("GAMEPLAY_SEED_NOT_HELD_ACROSS_A_B_C")
    if a["music"] != b["music"]:
        raise BindingError("A_B_MUSIC_SEED_NOT_REPEATABLE")
    if c["music"] == a["music"]:
        raise BindingError("C_MUSIC_SEED_NOT_CHANGED")

def _verify_predecessor(root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    path = root / str(entry["path"])
    if not path.is_file():
        raise BindingError(f"PREDECESSOR_MISSING:{entry['path']}")
    actual_bytes = path.stat().st_size
    actual_sha = sha256_file(path)
    if actual_bytes != int(entry["bytes"]) or actual_sha != entry["sha256"]:
        raise BindingError(f"PREDECESSOR_PIN_MISMATCH:{entry['path']}")
    if entry.get("sidecar_required", False):
        verify_sidecar(path, actual_sha)
    return {"path": entry["path"], "bytes": actual_bytes, "sha256": actual_sha, "sidecar": "PASS" if entry.get("sidecar_required", False) else "NOT_REQUIRED"}

def run(project_root: Path, output_parent: Path) -> dict[str, Any]:
    root = project_root.resolve(strict=True)
    inputs_path = root / INPUTS_REL
    if not inputs_path.is_file():
        raise BindingError(f"INPUTS_MANIFEST_MISSING:{INPUTS_REL}")
    inputs_raw = inputs_path.read_bytes()
    if sha256_bytes(inputs_raw) != INPUTS_SHA256:
        raise BindingError("INPUTS_MANIFEST_SHA256_MISMATCH")
    inputs = json.loads(inputs_raw.decode("utf-8"))
    sidecar = Path(str(inputs_path) + ".sha256")
    verify_sidecar(inputs_path, INPUTS_SHA256)
    if inputs.get("schema") != "C11E-E6-CHALLENGE-EDITORIAL-BINDING-PREPARE-ONLY-INPUTS-V1":
        raise BindingError("INPUTS_SCHEMA_INVALID")

    pinned: list[dict[str, Any]] = []
    for group in ("policy_and_layout_pins", "protected_governance_pins", "runtime_consumer_pins", "predecessor_evidence", "canonical_e1_source_pins"):
        for pin in inputs.get(group, []):
            pinned.append(verify_pin(root, pin))
    # Receipt/plan artifacts that had predecessor sidecars are explicitly rechecked.
    predecessor_checks = []
    for entry in inputs.get("predecessor_evidence", []):
        sidecar_required = str(entry["path"]).endswith((
            "E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_AUDIT_RECEIPT_V1.json",
            "E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_PLAN_V1.json",
            "E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json",
            "E6_CHALLENGE_PREPARE_ONLY_PLAN_V1.json",
            "INPUT_MANIFEST_PINNED_V1.json",
        ))
        predecessor_checks.append(_verify_predecessor(root, {**entry, "sidecar_required": sidecar_required}))

    fixture = load_json(root / "definitions/c11e/test_only/C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.json")
    family_plan_path = root / "artifacts/tests/c11e/e6_smoke18_family_editorial_fixture/E6FAMEDITORIAL_20261118T215606Z_36DB17BC/E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_PLAN_V1.json"
    family_receipt_path = root / "artifacts/tests/c11e/e6_smoke18_family_editorial_fixture/E6FAMEDITORIAL_20261118T215606Z_36DB17BC/E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_AUDIT_RECEIPT_V1.json"
    challenge_plan_path = root / "artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator/E6CHPREP_20261118T202841Z_37C6AE0E/E6_CHALLENGE_PREPARE_ONLY_PLAN_V1.json"
    challenge_receipt_path = root / "artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator/E6CHPREP_20261118T202841Z_37C6AE0E/E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json"
    family_plan = load_json(family_plan_path)
    family_receipt = load_json(family_receipt_path)
    challenge_plan = load_json(challenge_plan_path)
    challenge_receipt = load_json(challenge_receipt_path)
    if fixture.get("status") != "OPERATOR_SCOPE_APPROVED_TEST_ONLY_COPY_CANDIDATES_PREPARE_ONLY":
        raise BindingError("FAMILY_FIXTURE_STATUS_INVALID")
    if family_plan.get("status") != "PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN":
        raise BindingError("FAMILY_EDITORIAL_PLAN_NOT_PREPARE_ONLY_PASS")
    if family_receipt.get("status") != "PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN":
        raise BindingError("FAMILY_EDITORIAL_RECEIPT_NOT_PREPARE_ONLY_PASS")
    if challenge_receipt.get("status") != "PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD":
        raise BindingError("CHALLENGE_PREPARE_ONLY_RECEIPT_STATUS_INVALID")
    if challenge_plan.get("status") != "PREPARED_ONLY_NOT_FROZEN_NOT_E6_ACCEPTED":
        raise BindingError("CHALLENGE_PREPARE_ONLY_PLAN_STATUS_INVALID")
    if int(family_plan.get("top_level_rows_actual", -1)) != 18 or int(family_plan.get("editorial_targets_actual", -1)) != 30:
        raise BindingError("FAMILY_EDITORIAL_COVERAGE_COUNT_INVALID")
    if int(family_receipt.get("top_level_rows", -1)) != 18 or int(family_receipt.get("editorial_targets", -1)) != 30:
        raise BindingError("FAMILY_EDITORIAL_RECEIPT_COUNTS_INVALID")
    if int(challenge_receipt.get("counts", {}).get("e1_intents", -1)) != 18 or int(challenge_receipt.get("counts", {}).get("d_envelopes", -1)) != 18:
        raise BindingError("CHALLENGE_PREPARE_ONLY_RECEIPT_COUNTS_INVALID")
    music_fixture = challenge_receipt.get("music_fixture", {})
    if music_fixture.get("profile_id") != "challenge_8bit_v1" or music_fixture.get("authority") != "PROPOSAL_ONLY_NOT_AUTHORIZED" or music_fixture.get("tempo_bpm_sent_to_e1") is not False or music_fixture.get("duration_seconds_sent_to_e1") is not False:
        raise BindingError("CHALLENGE_MUSIC_FIXTURE_AUTHORITY_INVALID")
    if challenge_receipt.get("governance", {}).get("d4_8") != "BLOCKED" or challenge_receipt.get("governance", {}).get("renderer") != "OFF" or challenge_receipt.get("governance", {}).get("release_authority") != "NONE":
        raise BindingError("CHALLENGE_PREDECESSOR_GOVERNANCE_INVALID")

    challenge_values = fixture.get("family_fixtures", {}).get("challenge", {})
    if {k: challenge_values.get(k) for k in RENDERABLE_FIELDS} != inputs.get("fixture_values"):
        raise BindingError("CHALLENGE_FIXTURE_VALUES_DIFFER_FROM_PINNED_INPUTS")
    policy_sha = inputs["policy_and_layout_pins"][0]["sha256"]
    layout_sha = inputs["policy_and_layout_pins"][1]["sha256"]

    family_rows = {str(row.get("selector")): row for row in family_plan.get("rows", []) if row.get("family") == "challenge"}
    if set(family_rows) != set(EXPECTED_SELECTORS) or len(family_rows) != 6:
        raise BindingError("FAMILY_PLAN_CHALLENGE_SELECTOR_SET_INVALID")
    challenge_groups = {str(row.get("selector")): row for row in challenge_plan.get("challenge_groups", [])}
    if set(challenge_groups) != set(EXPECTED_SELECTORS) or len(challenge_groups) != 6:
        raise BindingError("CHALLENGE_PLAN_SELECTOR_SET_INVALID")
    envelope_rows = {(str(x.get("selector")), str(x.get("variant"))): x for x in challenge_plan.get("d_envelopes", [])}
    intent_rows = {(str(x.get("selector")), str(x.get("variant"))): x for x in challenge_plan.get("e1_intents", [])}
    if len(envelope_rows) != 18 or len(intent_rows) != 18:
        raise BindingError("CHALLENGE_PLAN_PROBE_RECORD_COUNTS_INVALID")

    # Each base E1/Envelope input is linked to its challenge plan hashes and sidecars.
    expected_probe_count = 0
    observed_e1_pins: dict[str, dict[str, Any]] = {}
    output_records = []
    groups_report = []
    visible_total = 0
    suppressed_total = 0
    for selector in EXPECTED_SELECTORS:
        group = challenge_groups[selector]
        family_row = family_rows[selector]
        editorial = family_row.get("editorial", {})
        if editorial != inputs["fixture_values"]:
            raise BindingError(f"FAMILY_ROW_EDITORIAL_MISMATCH:{selector}")
        family_targets = {str(t.get("variant")): t for t in family_row.get("targets", [])}
        if set(family_targets) != set(EXPECTED_VARIANTS):
            raise BindingError(f"FAMILY_ROW_TARGET_VARIANTS_INVALID:{selector}")
        group_probe_rows = {str(p.get("variant")): p for p in group.get("probes", [])}
        if set(group_probe_rows) != set(EXPECTED_VARIANTS):
            raise BindingError(f"CHALLENGE_GROUP_PROBE_VARIANTS_INVALID:{selector}")
        selector_report = {"selector": selector, "phase_frames": {}, "targets": []}
        selector_seeds: dict[str, dict[str, int]] = {}

        for variant in EXPECTED_VARIANTS:
            expected_probe_count += 1
            key = (selector, variant)
            plan_env = envelope_rows[key]
            plan_intent = intent_rows[key]
            base_env_rel = str(plan_env["relative_path"])
            base_intent_rel = str(plan_intent["relative_path"])
            expected_env = inputs["challenge_probe_inputs"][expected_probe_count - 1]
            if expected_env["selector"] != selector or expected_env["variant"] != variant:
                # Lookup exact input row rather than relying on package array order.
                expected_env = next((x for x in inputs["challenge_probe_inputs"] if x["selector"] == selector and x["variant"] == variant), None)
            if expected_env is None:
                raise BindingError(f"PINNED_PROBE_INPUT_NOT_FOUND:{selector}:{variant}")
            env_path = root / expected_env["envelope_path"]
            intent_path = root / expected_env["intent_path"]
            if base_env_rel != Path(expected_env["envelope_path"]).relative_to(Path("artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator/E6CHPREP_20261118T202841Z_37C6AE0E")).as_posix() or base_intent_rel != Path(expected_env["intent_path"]).relative_to(Path("artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator/E6CHPREP_20261118T202841Z_37C6AE0E")).as_posix():
                raise BindingError(f"CHALLENGE_PLAN_PATH_LINKAGE_INVALID:{selector}:{variant}")
            env_sha = sha256_file(env_path) if env_path.is_file() else ""
            intent_sha = sha256_file(intent_path) if intent_path.is_file() else ""
            if env_sha != expected_env["envelope_sha256"] or env_path.stat().st_size != int(expected_env["envelope_bytes"]):
                raise BindingError(f"CHALLENGE_ENVELOPE_PIN_MISMATCH:{selector}:{variant}")
            if intent_sha != expected_env["intent_sha256"] or intent_path.stat().st_size != int(expected_env["intent_bytes"]):
                raise BindingError(f"CHALLENGE_INTENT_PIN_MISMATCH:{selector}:{variant}")
            verify_sidecar(env_path, env_sha)
            verify_sidecar(intent_path, intent_sha)
            if env_sha != str(plan_env.get("envelope_sha256", "")) or intent_sha != str(plan_intent.get("intent_sha256", "")):
                raise BindingError(f"CHALLENGE_PLAN_HASH_LINKAGE_INVALID:{selector}:{variant}")
            if str(plan_env.get("scenario_id", "")) != str(family_row.get("scenario_id", "")) or str(plan_intent.get("scenario_id", "")) != str(family_row.get("scenario_id", "")):
                raise BindingError(f"CHALLENGE_SCENARIO_ID_LINKAGE_INVALID:{selector}:{variant}")
            if str(plan_env.get("request_id", "")) != str(base_env_rel.split("/")[-1].replace("_D_ENVELOPE.json", "")) and not str(plan_env.get("request_id", "")).endswith(f"-{selector}-{variant}"):
                raise BindingError(f"CHALLENGE_ENVELOPE_REQUEST_ID_LINKAGE_INVALID:{selector}:{variant}")
            if intent_sha != str(group_probe_rows[variant].get("intent_sha256", "")) or env_sha != str(group_probe_rows[variant].get("envelope_sha256", "")):
                raise BindingError(f"CHALLENGE_GROUP_HASH_LINKAGE_INVALID:{selector}:{variant}")

            base_envelope = load_json(env_path)
            intent = load_json(intent_path)
            if base_envelope.get("e1_intent") != intent:
                raise BindingError(f"ENVELOPE_EMBEDDED_INTENT_MISMATCH:{selector}:{variant}")
            for source_pin in intent.get("source_identity", {}).get("source_pins", []):
                source_path = str(source_pin.get("path", ""))
                row_pin = {"path": source_path, "bytes": int(source_pin.get("bytes", -1)), "sha256": str(source_pin.get("sha256", "")).lower()}
                existing_pin = observed_e1_pins.get(source_path)
                if existing_pin is not None and existing_pin != row_pin:
                    raise BindingError(f"E1_SOURCE_PIN_UNION_CONFLICT:{source_path}")
                observed_e1_pins[source_path] = row_pin
            if base_envelope.get("challenge_id") != selector or intent.get("request", {}).get("selection", {}).get("variant_id") != selector:
                raise BindingError(f"CHALLENGE_SELECTOR_IDENTITY_MISMATCH:{selector}:{variant}")
            if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED" or intent.get("request_origin") != "TEST":
                raise BindingError(f"E1_INTENT_BOUNDARY_INVALID:{selector}:{variant}")
            e1_editorial = intent.get("editorial", {})
            if any(e1_editorial.get(field) != "UNKNOWN" for field in ("title", "subtitle", "call_to_action", "player_name", "challenge_label")):
                raise BindingError(f"E1_CANONICAL_EDITORIAL_FIELDS_NOT_UNKNOWN:{selector}:{variant}")
            if intent.get("music_contract", {}).get("engine_request", {}).get("tempo_bpm") is not None or intent.get("music_contract", {}).get("engine_request", {}).get("duration_seconds") is not None:
                raise BindingError(f"E1_MUSIC_UNRESOLVED_FIELDS_CHANGED:{selector}:{variant}")
            seed_domains = intent.get("seed_domains", {})
            gameplay_seed = seed_domains.get("gameplay", {}).get("value")
            music_seed = seed_domains.get("music", {}).get("value")
            if not isinstance(gameplay_seed, int) or not isinstance(music_seed, int):
                raise BindingError(f"E1_SEED_DOMAIN_VALUE_INVALID:{selector}:{variant}")
            selector_seeds[variant] = {"gameplay": gameplay_seed, "music": music_seed}
            if int(plan_intent.get("gameplay_seed", -1)) != gameplay_seed or int(plan_intent.get("music_seed", -1)) != music_seed:
                raise BindingError(f"CHALLENGE_PLAN_SEED_LINKAGE_INVALID:{selector}:{variant}")
            phase_rows = phase_index(base_envelope)
            group_phases = group.get("phase_ranges", [])
            if group_phases != base_envelope.get("source_phase_ranges"):
                raise BindingError(f"CHALLENGE_GROUP_PHASE_MAP_MISMATCH:{selector}:{variant}")
            if int(group.get("source_timebase", {}).get("frames", -1)) != int(base_envelope.get("source_timebase", {}).get("total_frames", -2)) or int(group.get("source_timebase", {}).get("fps", -1)) != int(base_envelope.get("source_timebase", {}).get("fps", -2)):
                raise BindingError(f"CHALLENGE_GROUP_TIMEBASE_MISMATCH:{selector}:{variant}")
            if int(intent.get("source_identity", {}).get("c11c_manifest", {}).get("bytes", -1)) != 796318 or intent.get("source_identity", {}).get("c11c_manifest", {}).get("sha256") != "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953":
                raise BindingError(f"C11C_MANIFEST_IDENTITY_MISMATCH:{selector}:{variant}")
            if intent.get("execution_boundary", {}).get("d4_8") != "BLOCKED" or intent.get("execution_boundary", {}).get("release_authority") != "NONE":
                raise BindingError(f"E1_GOVERNANCE_BOUNDARY_INVALID:{selector}:{variant}")

            derived, field_summary = bind_envelope(base_envelope, editorial, policy_sha, layout_sha)
            if derived["e1_intent"] != intent:
                raise BindingError(f"DERIVED_E1_INTENT_MUTATED:{selector}:{variant}")
            if derived["source_phase_ranges"] != base_envelope["source_phase_ranges"] or derived["source_timebase"] != base_envelope["source_timebase"]:
                raise BindingError(f"DERIVED_SOURCE_TIMEBASE_MUTATED:{selector}:{variant}")
            if derived["intent_hash"] != base_envelope["intent_hash"]:
                raise BindingError(f"DERIVED_INTENT_HASH_MUTATED:{selector}:{variant}")

            filename = f"{selector}_{variant}_E6_BOUND_D_ENVELOPE_V1.json"
            output_rel = f"envelopes/{filename}"
            out_dir_placeholder = output_rel
            out_bytes = (json.dumps(derived, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
            output_records.append({
                "selector": selector, "variant": variant,
                "scenario_id": str(family_row.get("scenario_id", "")),
                "target_id": str(family_targets[variant].get("target_id", "")),
                "source_envelope_path": expected_env["envelope_path"],
                "source_envelope_sha256": env_sha,
                "source_intent_path": expected_env["intent_path"],
                "source_intent_sha256": intent_sha,
                "output_relative_path": output_rel,
                "output_bytes": len(out_bytes),
                "output_sha256": sha256_bytes(out_bytes),
                "visible_fields": field_summary["visible_fields"],
                "suppressed_zero_window_fields": field_summary["suppressed_zero_window_fields"],
                "hook_frames": field_summary["hook_frames"],
                "cta_frames": field_summary["cta_frames"],
                "_bytes": out_bytes,
            })
            visible_total += len(field_summary["visible_fields"])
            suppressed_total += len(field_summary["suppressed_zero_window_fields"])
            selector_report["phase_frames"] = {"HOOK":field_summary["hook_frames"],"CTA":field_summary["cta_frames"]}
            selector_report["targets"].append({
                "variant":variant, "visible_fields":field_summary["visible_fields"],
                "suppressed_zero_window_fields":field_summary["suppressed_zero_window_fields"],
                "output_relative_path":output_rel,
                "output_sha256":sha256_bytes(out_bytes),
            })
        validate_seed_isolation(selector_seeds)
        selector_report["seed_isolation"] = {
            "gameplay_seed_shared_A_B_C": selector_seeds["A"]["gameplay"],
            "music_seed_A_B_repeat": selector_seeds["A"]["music"],
            "music_seed_C_changed": selector_seeds["C_CHANGED_MUSIC_SEED"]["music"],
        }
        groups_report.append(selector_report)

    if expected_probe_count != 18 or len(output_records) != 18:
        raise BindingError("OUTPUT_PROBE_COUNT_INVALID")
    expected_e1_pins = {str(x["path"]): {"path": str(x["path"]), "bytes": int(x["bytes"]), "sha256": str(x["sha256"]).lower()} for x in inputs.get("canonical_e1_source_pins", [])}
    if observed_e1_pins != expected_e1_pins or len(observed_e1_pins) != 17:
        raise BindingError(f"E1_SOURCE_PIN_UNION_MISMATCH:{len(observed_e1_pins)}:{len(expected_e1_pins)}")
    if visible_total != 27 or suppressed_total != 27:
        raise BindingError(f"VISIBLE_SUPPRESSED_COUNTS_INVALID:{visible_total}:{suppressed_total}")

    governance = inputs["governance"]
    if governance["d4_8"] != "BLOCKED" or governance["renderer"] != "OFF" or governance["release_authority"] != "NONE" or governance["e6_test_only_execution_authorized"] is not False:
        raise BindingError("GOVERNANCE_INPUTS_NOT_HELD")

    output_parent_resolved = output_parent.resolve()
    if not output_parent_resolved.is_relative_to(root):
        raise BindingError("OUTPUT_PARENT_OUTSIDE_PROJECT_ROOT")
    cursor = output_parent_resolved
    while cursor != root:
        if cursor.exists() and cursor.is_symlink():
            raise BindingError(f"OUTPUT_PARENT_REPARSE_OR_SYMLINK:{cursor}")
        cursor = cursor.parent
        if root not in cursor.parents and cursor != root:
            raise BindingError("OUTPUT_PARENT_ANCESTOR_ESCAPE")
    if root.is_symlink():
        raise BindingError("PROJECT_ROOT_IS_SYMLINK")
    output_parent_resolved.mkdir(parents=True, exist_ok=True)
    output_parent = output_parent_resolved
    run_id = "E6CHEDITORIALBIND_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper()
    output_root = output_parent / run_id
    output_root.mkdir(parents=False, exist_ok=False)
    (output_root / "envelopes").mkdir()
    written = []
    for record in output_records:
        out_path = output_root / record["output_relative_path"]
        write_new(out_path, record["_bytes"])
        sidecar_text = f"{record['output_sha256']}  {out_path.name}\n".encode("ascii")
        write_new(Path(str(out_path) + ".sha256"), sidecar_text)
        written.append({k:v for k,v in record.items() if k != "_bytes"})

    binding_manifest = {
        "schema":"C11E-E6-CHALLENGE-EDITORIAL-BINDING-MANIFEST-V1",
        "schema_version":"1.0",
        "status":"PASS_PREPARE_ONLY_18_CHALLENGE_ENVELOPES_27_VISIBLE_27_SUPPRESSED",
        "run_id":run_id,
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "source_inputs_sha256":INPUTS_SHA256,
        "family_fixture_sha256":inputs["predecessor_evidence"][0]["sha256"],
        "family_plan_sha256":inputs["predecessor_evidence"][2]["sha256"],
        "challenge_prepare_receipt_sha256":inputs["predecessor_evidence"][3]["sha256"],
        "challenge_prepare_plan_sha256":inputs["predecessor_evidence"][4]["sha256"],
        "counts":{"selectors":6,"nested_probes":18,"bound_envelopes":18,"editorial_slots":54,"visible_slots":27,"intentionally_suppressed_zero_window_slots":27},
        "phase_policy":{
            "title_subtitle_window":"HOOK only",
            "call_to_action_window":"CTA only",
            "zero_duration":"OMITTED_EMPTY; zero-width [start_frame,end_frame) has no frames",
            "fallback":"FORBIDDEN; no migration to GAME or another phase",
            "phase_boundaries_mutated":False,
        },
        "selectors":groups_report,
        "outputs":written,
        "predecessor_checks":predecessor_checks,
        "source_pin_count":len(pinned),
        "governance":{
            "e1":"PREPARE_ONLY","d4_8":"BLOCKED","renderer":"OFF",
            "production_dispatch":False,"production_media":False,"release_authority":"NONE",
            "e6_accepted_scenarios":0,"e6_test_only_execution_authorized":False,"matrix_frozen":False,
            "godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,
            "audio_generated":False,"mux_invoked":False,"media_created":False,"batch_id_consumed":False,
        },
        "limitations":[
            "This is a D-envelope binding/preparation artifact, not live consumer readback.",
            "The 27 suppressed fields are intentionally absent because their canonical HOOK/CTA window has zero frames.",
            "No zero-duration field is moved into GAME or any other phase.",
            "The original E1 intents, source D envelopes, canonical Challenge definitions, E4A policy, D1.5 layout, C11-C and D4.8 V2 remain unmodified.",
            "Godot, FFmpeg, FFprobe, renderer, audio, mux, media and production dispatch are not invoked.",
        ],
    }
    manifest_path = output_root / "E6_CHALLENGE_EDITORIAL_BINDING_MANIFEST_V1.json"
    manifest_bytes = (json.dumps(binding_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_new(manifest_path, manifest_bytes)
    manifest_sha = sha256_bytes(manifest_bytes)
    write_new(Path(str(manifest_path)+".sha256"), f"{manifest_sha}  {manifest_path.name}\n".encode("ascii"))
    receipt = {
        "schema":"C11E-E6-CHALLENGE-EDITORIAL-BINDING-RECEIPT-V1",
        "schema_version":"1.0",
        "status":binding_manifest["status"],
        "run_id":run_id,
        "manifest_path":str(manifest_path.relative_to(root)) if manifest_path.is_relative_to(root) else str(manifest_path),
        "manifest_sha256":manifest_sha,
        "output_envelopes":18,
        "visible_field_slots":27,
        "suppressed_zero_window_field_slots":27,
        "runtime_editorial_readback":"NOT_PROVEN",
        "governance":binding_manifest["governance"],
    }
    receipt_path=output_root/"E6_CHALLENGE_EDITORIAL_BINDING_RECEIPT_V1.json"
    receipt_bytes=(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode("utf-8")
    write_new(receipt_path,receipt_bytes)
    receipt_sha=sha256_bytes(receipt_bytes)
    write_new(Path(str(receipt_path)+".sha256"),f"{receipt_sha}  {receipt_path.name}\n".encode("ascii"))
    print("CHALLENGE_SELECTORS=6/6")
    print("NESTED_PROBES=18/18")
    print("BOUND_D_ENVELOPES=18/18")
    print("EDITORIAL_FIELD_SLOTS=54; VISIBLE=27; ZERO_WINDOW_SUPPRESSED=27")
    print("ZERO_WINDOW_POLICY=OMIT_NO_PHASE_FALLBACK")
    print("SOURCE_PINS=PASS/%d" % len(pinned))
    print("PREDECESSOR_RECEIPTS_AND_SIDECARS=PASS/%d" % len(predecessor_checks))
    print("RUNTIME_EDITORIAL_READBACK=NOT_PROVEN")
    print("GODOT=NOT_INVOKED; FFMPEG=NOT_INVOKED; FFPROBE=NOT_INVOKED")
    print("D4_8=BLOCKED; RENDERER=OFF; E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; RELEASE_AUTHORITY=NONE")
    print("BINDING_MANIFEST=%s" % manifest_path)
    print("BINDING_MANIFEST_SHA256=%s" % manifest_sha)
    print("BINDING_RECEIPT=%s" % receipt_path)
    print("BINDING_RECEIPT_SHA256=%s" % receipt_sha)
    print("BINDING_PREPARE_ONLY=PASS")
    return receipt

def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-root",required=True)
    parser.add_argument("--output-parent",default="artifacts/tests/c11e/e6_challenge_editorial_binding_prepare_only")
    args=parser.parse_args()
    try:
        run(Path(args.project_root), Path(args.project_root)/Path(args.output_parent))
    except Exception as exc:
        print(f"CHALLENGE_EDITORIAL_BINDING_FAILED={type(exc).__name__}:{exc}",file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
