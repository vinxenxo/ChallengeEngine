import argparse
import copy
import hashlib
import json
import math
import sys
from collections import OrderedDict


SEMANTIC_UNKNOWN = "UNKNOWN"
SCHEMA_ID = "c11d_production_request"
SCHEMA_VERSION = "1.0"
ALLOWED_MODES = {"REVIEW", "PRODUCTION"}
ALLOWED_REQUEST_ORIGINS = {"GUI", "CLI", "API", "TEST", "UNKNOWN"}

FORBIDDEN_REQUEST_FIELDS = {
    "winning_frame",
    "close_calls",
    "simulation_result",
    "simulation_truth"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, value):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(
            value,
            handle,
            ensure_ascii=False,
            indent=2
        )
        handle.write("\n")


def require_string(value, field):
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")

    if not value.strip():
        raise ValueError(f"{field} must not be empty")

    return value.strip()


def normalize_unknown_string(value, field):
    if value is None:
        return SEMANTIC_UNKNOWN

    if not isinstance(value, str):
        raise ValueError(f"{field} must be string or UNKNOWN")

    if not value.strip():
        return SEMANTIC_UNKNOWN

    return value.strip()


def normalize_integer(value, field, minimum=None):
    if isinstance(value, bool):
        raise ValueError(f"{field} must be integer")

    if isinstance(value, int):
        result = value

    elif isinstance(value, str):
        text = value.strip()

        try:
            result = int(text)
        except ValueError as exc:
            raise ValueError(f"{field} must be integer") from exc

    else:
        raise ValueError(f"{field} must be integer")

    if minimum is not None and result < minimum:
        raise ValueError(f"{field} must be >= {minimum}")

    return result


def normalize_number(value, field, minimum=None):
    if isinstance(value, bool):
        raise ValueError(f"{field} must be number")

    if isinstance(value, (int, float)):
        result = float(value)

    elif isinstance(value, str):
        text = value.strip()

        try:
            result = float(text)
        except ValueError as exc:
            raise ValueError(f"{field} must be number") from exc

    else:
        raise ValueError(f"{field} must be number")

    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")

    if minimum is not None and result < minimum:
        raise ValueError(f"{field} must be >= {minimum}")

    return result


def normalize_bool(value, field):
    if isinstance(value, bool):
        return value

    raise ValueError(f"{field} must be boolean")


def reject_unknown_fields(value, allowed, field):
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be object")
    unknown = sorted(set(value.keys()) - set(allowed))
    if unknown:
        raise ValueError(
            f"Unknown {field} field(s): " + ", ".join(unknown)
        )


def schema_vocabulary(schema):
    challenge_ids = []
    delivery_profiles = []

    fields = schema.get("fields", [])

    for field in fields:
        name = field.get("name")

        if name == "challenge_id":
            challenge_ids = list(field.get("allowed_values", []))

        if name == "delivery_profile_id":
            delivery_profiles = list(field.get("evidence_values", []))

    if not challenge_ids:
        raise ValueError("schema has no Challenge ID vocabulary")

    if not delivery_profiles:
        raise ValueError("schema has no delivery-profile vocabulary")

    return challenge_ids, delivery_profiles


def reject_forbidden_fields(value, path="request"):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_REQUEST_FIELDS:
                raise ValueError(
                    f"Forbidden production-request field: {path}.{key}"
                )
            reject_forbidden_fields(nested, f"{path}.{key}")

    elif isinstance(value, list):
        for index, nested in enumerate(value):
            reject_forbidden_fields(nested, f"{path}[{index}]")


def canonicalize_object(value):
    if isinstance(value, dict):
        return OrderedDict(
            (key, canonicalize_object(value[key]))
            for key in sorted(value)
        )

    if isinstance(value, list):
        return [canonicalize_object(item) for item in value]

    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("personalization values must contain finite numbers")

    return value


def reject_unknown_top_level_fields(request, schema):
    allowed = set(schema.get("canonical_field_order", []))
    if not allowed:
        raise ValueError("schema has no canonical field order")

    unknown = sorted(set(request.keys()) - allowed)
    if unknown:
        raise ValueError(
            "Unknown Production Request field(s): " + ", ".join(unknown)
        )


def normalize_personalization_values(value):
    if not isinstance(value, dict):
        raise ValueError("personalization.values must be object")
    reject_forbidden_fields(value, "personalization.values")
    return canonicalize_object(value)


def normalize_personalization(value):
    if value is None:
        value = {}

    if not isinstance(value, dict):
        raise ValueError("personalization must be object")
    reject_unknown_fields(
        value,
        {"enabled", "profile_id", "values"},
        "personalization"
    )

    enabled = value.get("enabled", False)
    enabled = normalize_bool(enabled, "personalization.enabled")

    profile_id = value.get("profile_id", SEMANTIC_UNKNOWN)
    profile_id = normalize_unknown_string(
        profile_id,
        "personalization.profile_id"
    )

    values = value.get("values", {})
    if values is None:
        values = {}

    values = normalize_personalization_values(values)

    return OrderedDict([
        ("enabled", enabled),
        ("profile_id", profile_id),
        ("values", values)
    ])


def normalize_editorial(value):
    if value is None:
        value = {}

    if not isinstance(value, dict):
        raise ValueError("editorial must be object")
    reject_unknown_fields(
        value,
        {"title", "subtitle", "language", "call_to_action"},
        "editorial"
    )

    return OrderedDict([
        (
            "title",
            normalize_unknown_string(
                value.get("title"),
                "editorial.title"
            )
        ),
        (
            "subtitle",
            normalize_unknown_string(
                value.get("subtitle"),
                "editorial.subtitle"
            )
        ),
        (
            "language",
            normalize_unknown_string(
                value.get("language"),
                "editorial.language"
            )
        ),
        (
            "call_to_action",
            normalize_unknown_string(
                value.get("call_to_action"),
                "editorial.call_to_action"
            )
        )
    ])


def normalize_output(value):
    if value is None:
        value = {}

    if not isinstance(value, dict):
        raise ValueError("output must be object")
    reject_unknown_fields(
        value,
        {"container", "width", "height", "fps", "audio_enabled"},
        "output"
    )

    container = value.get(
        "container",
        SEMANTIC_UNKNOWN
    )
    container = normalize_unknown_string(
        container,
        "output.container"
    )

    width = value.get("width", SEMANTIC_UNKNOWN)
    if width != SEMANTIC_UNKNOWN:
        width = normalize_integer(
            width,
            "output.width",
            minimum=1
        )

    height = value.get("height", SEMANTIC_UNKNOWN)
    if height != SEMANTIC_UNKNOWN:
        height = normalize_integer(
            height,
            "output.height",
            minimum=1
        )

    fps = value.get("fps", SEMANTIC_UNKNOWN)
    if fps != SEMANTIC_UNKNOWN:
        fps = normalize_number(
            fps,
            "output.fps",
            minimum=1
        )

    audio_enabled = value.get(
        "audio_enabled",
        True
    )
    audio_enabled = normalize_bool(
        audio_enabled,
        "output.audio_enabled"
    )

    return OrderedDict([
        ("container", container),
        ("width", width),
        ("height", height),
        ("fps", fps),
        ("audio_enabled", audio_enabled)
    ])


def normalize_provenance(value):
    if value is None:
        value = {}

    if not isinstance(value, dict):
        raise ValueError("provenance must be object")
    reject_unknown_fields(
        value,
        {"source_revision", "request_origin", "parent_request_id"},
        "provenance"
    )

    source_revision = normalize_unknown_string(
        value.get("source_revision"),
        "provenance.source_revision"
    )

    request_origin = value.get(
        "request_origin",
        SEMANTIC_UNKNOWN
    )

    request_origin = normalize_unknown_string(
        request_origin,
        "provenance.request_origin"
    )

    if request_origin not in ALLOWED_REQUEST_ORIGINS:
        raise ValueError(
            "provenance.request_origin must be GUI, CLI, API, TEST or UNKNOWN"
        )

    parent_request_id = normalize_unknown_string(
        value.get("parent_request_id"),
        "provenance.parent_request_id"
    )

    # Interface origin is provenance metadata, not semantic request
    # identity. Normalize it away so GUI and CLI converge.
    canonical_request_origin = SEMANTIC_UNKNOWN

    return OrderedDict([
        ("source_revision", source_revision),
        ("request_origin", canonical_request_origin),
        ("parent_request_id", SEMANTIC_UNKNOWN)
    ])


def normalize_request(raw_request, schema):
    if not isinstance(raw_request, dict):
        raise ValueError("Production Request must be a JSON object")

    reject_forbidden_fields(raw_request)
    reject_unknown_top_level_fields(raw_request, schema)

    if raw_request.get("schema_version", SCHEMA_VERSION) != SCHEMA_VERSION:
        raise ValueError("schema_version must be 1.0")

    request_id = require_string(
        raw_request.get("request_id"),
        "request_id"
    )

    mode = require_string(
        raw_request.get("mode"),
        "mode"
    )

    if mode not in ALLOWED_MODES:
        raise ValueError(
            "mode must be REVIEW or PRODUCTION"
        )

    challenge_id = require_string(
        raw_request.get("challenge_id"),
        "challenge_id"
    )

    challenge_ids, delivery_profiles = schema_vocabulary(schema)

    if challenge_id not in challenge_ids:
        raise ValueError(
            f"Unknown challenge_id: {challenge_id}"
        )

    challenge_version = normalize_unknown_string(
        raw_request.get("challenge_version"),
        "challenge_version"
    )

    seed = normalize_integer(
        raw_request.get("seed"),
        "seed"
    )

    music_seed = normalize_integer(
        raw_request.get("music_seed"),
        "music_seed"
    )

    delivery_profile_id = require_string(
        raw_request.get("delivery_profile_id"),
        "delivery_profile_id"
    )

    if delivery_profile_id not in delivery_profiles:
        raise ValueError(
            f"Unknown delivery_profile_id: {delivery_profile_id}"
        )

    presentation_profile_id = normalize_unknown_string(
        raw_request.get("presentation_profile_id"),
        "presentation_profile_id"
    )

    duration_seconds = normalize_number(
        raw_request.get("duration_seconds"),
        "duration_seconds",
        minimum=0
    )

    variation_index = raw_request.get(
        "variation_index",
        0
    )

    variation_index = normalize_integer(
        variation_index,
        "variation_index",
        minimum=0
    )

    personalization = normalize_personalization(
        raw_request.get("personalization")
    )

    editorial = normalize_editorial(
        raw_request.get("editorial")
    )

    output = normalize_output(
        raw_request.get("output")
    )

    provenance = normalize_provenance(
        raw_request.get("provenance")
    )

    canonical = OrderedDict([
        ("request_id", request_id),
        ("schema_version", SCHEMA_VERSION),
        ("mode", mode),
        ("challenge_id", challenge_id),
        ("challenge_version", challenge_version),
        ("seed", seed),
        ("music_seed", music_seed),
        ("delivery_profile_id", delivery_profile_id),
        ("presentation_profile_id", presentation_profile_id),
        ("duration_seconds", duration_seconds),
        ("variation_index", variation_index),
        ("personalization", personalization),
        ("editorial", editorial),
        ("output", output),
        ("provenance", provenance)
    ])

    return canonical


def canonical_json(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False
    )


def request_hash(value):
    payload = canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_valid_fixture(challenge_id, delivery_profile_id, origin):
    personalization_values = OrderedDict([
        ("player_name", "TEST"),
        ("layout", OrderedDict([
            ("align", "center"),
            ("theme", "dark")
        ]))
    ])

    if origin == "CLI":
        personalization_values = OrderedDict([
            ("layout", OrderedDict([
                ("theme", "dark"),
                ("align", "center")
            ])),
            ("player_name", "TEST")
        ])

    return OrderedDict([
        ("request_id", "D4.2-PARITY-001"),
        ("schema_version", "1.0"),
        ("mode", "PRODUCTION"),
        ("challenge_id", challenge_id),
        ("challenge_version", "UNKNOWN"),
        ("seed", "123456"),
        ("music_seed", "654321"),
        ("delivery_profile_id", delivery_profile_id),
        ("presentation_profile_id", "UNKNOWN"),
        ("duration_seconds", "10"),
        ("variation_index", 0),
        ("personalization", OrderedDict([
            ("enabled", True),
            ("profile_id", "UNKNOWN"),
            ("values", personalization_values)
        ])),
        ("editorial", OrderedDict([
            ("title", "TEST"),
            ("subtitle", "UNKNOWN"),
            ("language", "es"),
            ("call_to_action", "JUEGA")
        ])),
        ("output", OrderedDict([
            ("container", "mp4"),
            ("width", 720),
            ("height", 1280),
            ("fps", 30),
            ("audio_enabled", True)
        ])),
        ("provenance", OrderedDict([
            ("source_revision", "D4.2-TEST"),
            ("request_origin", origin),
            ("parent_request_id", f"PARENT-{origin}")
        ]))
    ])


def build_unknown_fixture(challenge_id, delivery_profile_id):
    return OrderedDict([
        ("request_id", "D4.2-UNKNOWN-001"),
        ("mode", "REVIEW"),
        ("challenge_id", challenge_id),
        ("seed", 1),
        ("music_seed", 2),
        ("delivery_profile_id", delivery_profile_id),
        ("duration_seconds", 0)
    ])


def run_self_test(schema_path):
    schema = load_json(schema_path)

    if schema.get("schema_id") != SCHEMA_ID:
        raise AssertionError("schema_id mismatch")

    if schema.get("schema_version") != SCHEMA_VERSION:
        raise AssertionError("schema_version mismatch")

    if schema.get("runtime_authority") != "NONE":
        raise AssertionError("runtime authority is not NONE")

    challenge_ids, delivery_profiles = schema_vocabulary(schema)

    if len(challenge_ids) != 9:
        raise AssertionError(
            f"Expected 9 Challenge IDs, got {len(challenge_ids)}"
        )

    if len(delivery_profiles) != 5:
        raise AssertionError(
            f"Expected 5 delivery profiles, got {len(delivery_profiles)}"
        )

    challenge_id = challenge_ids[0]
    delivery_profile_id = delivery_profiles[0]

    gui_input = build_valid_fixture(
        challenge_id,
        delivery_profile_id,
        "GUI"
    )

    cli_input = build_valid_fixture(
        challenge_id,
        delivery_profile_id,
        "CLI"
    )

    gui_canonical = normalize_request(gui_input, schema)
    cli_canonical = normalize_request(cli_input, schema)

    gui_json = canonical_json(gui_canonical)
    cli_json = canonical_json(cli_canonical)

    gui_hash = request_hash(gui_canonical)
    cli_hash = request_hash(cli_canonical)

    parity_json = gui_json == cli_json
    parity_hash = gui_hash == cli_hash

    if not parity_json:
        raise AssertionError(
            "GUI and CLI canonical JSON are not identical"
        )

    if not parity_hash:
        raise AssertionError(
            "GUI and CLI canonical hashes are not identical"
        )

    if len(gui_hash) != 64:
        raise AssertionError("SHA-256 length invalid")

    unknown_input = build_unknown_fixture(
        challenge_id,
        delivery_profile_id
    )

    unknown_canonical = normalize_request(
        unknown_input,
        schema
    )

    unknown_defaults = (
        unknown_canonical["schema_version"] == "1.0" and
        unknown_canonical["challenge_version"] == "UNKNOWN" and
        unknown_canonical["presentation_profile_id"] == "UNKNOWN" and
        unknown_canonical["variation_index"] == 0 and
        unknown_canonical["personalization"]["enabled"] is False and
        unknown_canonical["editorial"]["title"] == "UNKNOWN" and
        unknown_canonical["output"]["audio_enabled"] is True and
        unknown_canonical["provenance"]["request_origin"] == "UNKNOWN" and
        unknown_canonical["provenance"]["parent_request_id"] == "UNKNOWN"
    )

    if not unknown_defaults:
        raise AssertionError(
            "UNKNOWN/default normalization failed"
        )

    negative_tests = {}

    try:
        broken = copy.deepcopy(gui_input)
        del broken["music_seed"]
        normalize_request(broken, schema)
        negative_tests["missing_music_seed"] = False
    except ValueError:
        negative_tests["missing_music_seed"] = True

    try:
        broken = copy.deepcopy(gui_input)
        broken["delivery_profile_id"] = "__INVALID_PROFILE__"
        normalize_request(broken, schema)
        negative_tests["invalid_delivery_profile"] = False
    except ValueError:
        negative_tests["invalid_delivery_profile"] = True

    for forbidden_key in (
        "winning_frame",
        "close_calls",
        "simulation_result",
        "simulation_truth"
    ):
        try:
            broken = copy.deepcopy(gui_input)
            broken["personalization"]["values"][forbidden_key] = 123
            normalize_request(broken, schema)
            negative_tests[f"nested_{forbidden_key}_rejected"] = False
        except ValueError:
            negative_tests[f"nested_{forbidden_key}_rejected"] = True

    try:
        broken = copy.deepcopy(gui_input)
        broken["unexpected_field"] = True
        normalize_request(broken, schema)
        negative_tests["unknown_top_level_field_rejected"] = False
    except ValueError:
        negative_tests["unknown_top_level_field_rejected"] = True

    try:
        broken = copy.deepcopy(gui_input)
        broken["duration_seconds"] = "NaN"
        normalize_request(broken, schema)
        negative_tests["non_finite_duration_rejected"] = False
    except ValueError:
        negative_tests["non_finite_duration_rejected"] = True

    try:
        broken = copy.deepcopy(gui_input)
        broken["seed"] = True
        normalize_request(broken, schema)
        negative_tests["boolean_seed_rejected"] = False
    except ValueError:
        negative_tests["boolean_seed_rejected"] = True

    try:
        broken = copy.deepcopy(gui_input)
        broken["mode"] = "INVALID"
        normalize_request(broken, schema)
        negative_tests["invalid_mode"] = False
    except ValueError:
        negative_tests["invalid_mode"] = True

    if not all(negative_tests.values()):
        raise AssertionError(
            "One or more negative validation tests failed"
        )

    return {
        "checkpoint": "C11-D D4.2",
        "result": "PASS",
        "status": "CLOSED",
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "challenge_count": len(challenge_ids),
        "delivery_profile_count": len(delivery_profiles),
        "gui_cli_parity": {
            "canonical_json_equal": parity_json,
            "sha256_equal": parity_hash,
            "sha256": gui_hash
        },
        "unknown_default_normalization": unknown_defaults,
        "negative_tests": negative_tests,
        "semantic_normalization": {
            "interface_origin_removed_from_identity": True,
            "parent_request_id_removed_from_identity": True,
            "request_id_preserved_for_traceability": True
        },
        "seed_isolation": {
            "seed_field_required": True,
            "music_seed_field_required": True,
            "distinct_fields": True,
            "gameplay_rng_consumption": False
        },
        "forbidden_simulation_controls_rejected": all(
            negative_tests.get(f"nested_{key}_rejected", False)
            for key in (
                "winning_frame",
                "close_calls",
                "simulation_result",
                "simulation_truth"
            )
        ),
        "runtime_authority": "NONE",
        "gui_activation": False,
        "cli_production_activation": False,
        "renderer_activation": False,
        "orchestrator_activation": False,
        "next": "D4.3 - Personalization Contract"
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--schema", required=True)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--self-test", action="store_true")
    input_group.add_argument("--input", help="JSON Production Request to normalize")
    parser.add_argument("--output", help="Canonical JSON output path")
    parser.add_argument("--sha256-output", help="Canonical request SHA-256 output path")
    parser.add_argument("--receipt", required=False)
    parser.add_argument("--evidence", required=False)
    parser.add_argument("--parity", required=False)

    args = parser.parse_args()

    schema = load_json(args.schema)

    if args.input:
        if not args.output or not args.sha256_output:
            parser.error("--input requires both --output and --sha256-output")

        raw_request = load_json(args.input)
        canonical = normalize_request(raw_request, schema)
        digest = request_hash(canonical)
        save_json(args.output, canonical)

        with open(args.sha256_output, "w", encoding="ascii", newline="\n") as handle:
            handle.write(digest + "\n")

        print(json.dumps({
            "result": "PASS",
            "canonical_output": args.output,
            "sha256_output": args.sha256_output,
            "request_sha256": digest,
            "runtime_authority": "NONE"
        }, ensure_ascii=False, indent=2))
        return 0

    result = run_self_test(args.schema)

    if args.evidence:
        save_json(
            args.evidence,
            result
        )

    if args.parity:
        save_json(
            args.parity,
            result["gui_cli_parity"]
        )

    if args.receipt:
        save_json(
            args.receipt,
            result
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.2 ERROR: {exc}", file=sys.stderr)
        sys.exit(1)