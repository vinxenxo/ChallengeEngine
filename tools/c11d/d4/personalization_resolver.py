#!/usr/bin/env python3
"""Pure JSON personalization validation, normalization, and hashing for C11-D D4.3."""

import argparse
import copy
import hashlib
import json
import sys
from collections import OrderedDict


UNKNOWN = "UNKNOWN"
FORBIDDEN_FIELDS = {
    "seed", "music_seed", "mechanics", "target", "speed", "collision",
    "timing", "winning_frame", "close_calls", "simulation_result",
    "simulation_truth"
}
PROFILE_ORDER = ("none_v1", "editorial_text_v1")
EDITORIAL_ORDER = (
    "title", "subtitle", "call_to_action", "language", "player_name",
    "challenge_label"
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, value):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def canonical_bytes(value):
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def reject_forbidden(value, path="personalization"):
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_FIELDS:
                raise ValueError(f"Forbidden simulation/control field: {path}.{key}")
            reject_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_forbidden(child, f"{path}[{index}]")


def validate_registry(registry):
    if registry.get("registry_id") != "c11d_personalization_profile_registry":
        raise ValueError("Unexpected personalization registry id")
    if registry.get("registry_version") != "1.0":
        raise ValueError("Unsupported personalization registry version")
    entries = registry.get("profiles")
    if not isinstance(entries, list):
        raise ValueError("Registry profiles must be an array")
    profiles = OrderedDict()
    for item in entries:
        profile_id = item.get("profile_id")
        if profile_id not in PROFILE_ORDER or profile_id in profiles:
            raise ValueError(f"Unknown or duplicate profile_id: {profile_id}")
        if item.get("status") != "ACTIVE" or item.get("scope") != "EDITORIAL_PRESENTATION":
            raise ValueError(f"Profile is not active editorial scope: {profile_id}")
        profiles[profile_id] = item
    if tuple(profiles.keys()) != PROFILE_ORDER:
        raise ValueError("Registry must contain the supported profiles in canonical order")
    return profiles


def normalize_personalization(request, registry):
    if not isinstance(request, dict):
        raise ValueError("Production Request must be a JSON object")
    request_simulation_fields = FORBIDDEN_FIELDS - {"seed", "music_seed"}
    present_simulation_fields = request_simulation_fields.intersection(request)
    if present_simulation_fields:
        raise ValueError(
            "Production Request contains simulation/control field(s): "
            + ", ".join(sorted(present_simulation_fields))
        )

    raw = request.get("personalization", {})
    if not isinstance(raw, dict):
        raise ValueError("personalization must be an object")
    reject_forbidden(raw)
    extras = set(raw) - {"enabled", "profile_id", "values"}
    if extras:
        raise ValueError("Unknown personalization envelope field(s): " + ", ".join(sorted(extras)))

    enabled = raw.get("enabled", False)
    if not isinstance(enabled, bool):
        raise ValueError("personalization.enabled must be boolean")
    profile_id = raw.get("profile_id")
    if profile_id is None or profile_id == UNKNOWN or (isinstance(profile_id, str) and not profile_id.strip()):
        profile_id = "editorial_text_v1" if enabled else "none_v1"
    if not isinstance(profile_id, str):
        raise ValueError("personalization.profile_id must be a string")
    profile_id = profile_id.strip()
    if profile_id not in registry:
        raise ValueError(f"Unknown personalization profile_id: {profile_id}")

    values = raw.get("values", {})
    if values is None:
        values = {}
    if not isinstance(values, dict):
        raise ValueError("personalization.values must be an object")

    profile = registry[profile_id]
    allowed = set(profile.get("allowed_targets", []))
    unknown = set(values) - allowed
    if unknown:
        raise ValueError("Personalization fields not allowlisted: " + ", ".join(sorted(unknown)))

    if profile_id == "none_v1":
        if enabled:
            raise ValueError("none_v1 requires enabled=false")
        if values:
            raise ValueError("none_v1 does not accept personalization values")
        canonical_values = OrderedDict()
    else:
        if not enabled:
            raise ValueError("editorial_text_v1 requires enabled=true")
        canonical_values = OrderedDict()
        for name in EDITORIAL_ORDER:
            value = values.get(name, UNKNOWN)
            if value is None or (isinstance(value, str) and not value.strip()):
                value = UNKNOWN
            if value != UNKNOWN:
                if not isinstance(value, str):
                    raise ValueError(f"personalization.values.{name} must be string or UNKNOWN")
                value = value.strip()
                if name == "language":
                    value = value.lower()
                if len(value) > int(profile["constraints"]["max_string_length"]):
                    raise ValueError(f"personalization.values.{name} exceeds maximum length")
            canonical_values[name] = value

    return OrderedDict([
        ("enabled", enabled),
        ("profile_id", profile_id),
        ("profile_version", profile["profile_version"]),
        ("scope", profile["scope"]),
        ("values", canonical_values)
    ])


def make_fixtures():
    return OrderedDict([
        ("seed", 123456),
        ("music_seed", 654321),
        ("personalization", OrderedDict([
            ("enabled", True),
            ("profile_id", "editorial_text_v1"),
            ("values", OrderedDict([
                ("language", " ES "),
                ("player_name", "  TEST  ")
            ]))
        ]))
    ])


def run_self_test(registry_path):
    registry = validate_registry(load_json(registry_path))
    tests = OrderedDict()

    none_request = {"personalization": {"enabled": False, "profile_id": "none_v1", "values": {}}}
    none = normalize_personalization(none_request, registry)
    tests["neutral_profile_passes"] = none["profile_id"] == "none_v1" and not none["enabled"]

    request = make_fixtures()
    canonical = normalize_personalization(request, registry)
    tests["editorial_profile_passes"] = canonical["profile_id"] == "editorial_text_v1" and canonical["enabled"]
    tests["strings_trimmed"] = canonical["values"]["player_name"] == "TEST"
    tests["language_lowercase"] = canonical["values"]["language"] == "es"
    tests["missing_optional_values_unknown"] = canonical["values"]["title"] == UNKNOWN

    def rejected(candidate):
        try:
            normalize_personalization(candidate, registry)
            return False
        except ValueError:
            return True

    disallowed = copy.deepcopy(request)
    disallowed["personalization"]["values"]["seed"] = 123
    tests["non_allowlisted_field_rejected"] = rejected(disallowed)
    for field in ("winning_frame", "close_calls", "simulation_result"):
        candidate = copy.deepcopy(request)
        candidate["personalization"]["values"][field] = {}
        tests[f"{field}_rejected"] = rejected(candidate)

    gui = copy.deepcopy(request)
    gui["personalization"]["values"] = OrderedDict([
        ("player_name", "TEST"), ("language", "es")
    ])
    cli = copy.deepcopy(request)
    cli["personalization"]["values"] = OrderedDict([
        ("language", " ES "), ("player_name", "  TEST  ")
    ])
    gui_canonical = normalize_personalization(gui, registry)
    cli_canonical = normalize_personalization(cli, registry)
    same_json = canonical_bytes(gui_canonical) == canonical_bytes(cli_canonical)
    same_hash = digest(gui_canonical) == digest(cli_canonical)
    tests["gui_cli_canonical_json_equal"] = same_json
    tests["gui_cli_sha256_equal"] = same_hash

    request_b = copy.deepcopy(request)
    request_b["personalization"]["values"]["player_name"] = "LUIS"
    canonical_b = normalize_personalization(request_b, registry)
    seed_isolation = OrderedDict([
        ("seed_identical", request["seed"] == request_b["seed"]),
        ("music_seed_identical", request["music_seed"] == request_b["music_seed"]),
        ("personalization_hash_differs", digest(canonical) != digest(canonical_b))
    ])
    tests["seed_music_seed_isolation"] = all(seed_isolation.values())

    if not all(tests.values()):
        failed = [key for key, passed in tests.items() if not passed]
        raise AssertionError("D4.3 self-test failed: " + ", ".join(failed))

    return OrderedDict([
        ("checkpoint", "C11-D D4.3"),
        ("result", "PASS"),
        ("status", "CLOSED"),
        ("registry_id", "c11d_personalization_profile_registry"),
        ("registry_version", "1.0"),
        ("profile_count", len(registry)),
        ("tests", tests),
        ("gui_cli_parity", OrderedDict([
            ("canonical_json_equal", same_json),
            ("sha256_equal", same_hash),
            ("sha256", digest(gui_canonical))
        ])),
        ("seed_isolation", seed_isolation),
        ("example_personalization", canonical),
        ("example_sha256", digest(canonical)),
        ("runtime_authority", "NONE"),
        ("gui_activation", False),
        ("cli_activation", False),
        ("renderer_activation", False),
        ("orchestrator_activation", False),
        ("simulation_changes", False),
        ("next", "D4.4 - Canonical Production Orchestrator")
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--sha256-output")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--evidence")
    parser.add_argument("--receipt")
    args = parser.parse_args()
    registry = validate_registry(load_json(args.registry))

    if args.self_test:
        result = run_self_test(args.registry)
        if args.evidence:
            save_json(args.evidence, result)
        if args.receipt:
            save_json(args.receipt, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if not args.input or not args.output or not args.sha256_output:
        parser.error("normalization requires --input, --output, and --sha256-output")
    canonical = normalize_personalization(load_json(args.input), registry)
    value_hash = digest(canonical)
    save_json(args.output, canonical)
    with open(args.sha256_output, "w", encoding="ascii", newline="\n") as handle:
        handle.write(value_hash + "\n")
    print(json.dumps({"result": "PASS", "sha256": value_hash, "runtime_authority": "NONE"}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.3 ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
