import argparse
import hashlib
import json
import sys
from collections import OrderedDict

SCHEMA_ID = "c11d_production_request"
SCHEMA_VERSION = "1.0"
PLAN_ID = "c11d_production_plan"
PLAN_VERSION = "1.0"
FORBIDDEN_FIELDS = {
    "winning_frame",
    "close_calls",
    "simulation_result",
    "simulation_truth",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, value):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def canonical_json(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    )


def sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def profile_registry(registry):
    profiles = registry.get("profiles", [])
    result = OrderedDict()
    for profile in profiles:
        profile_id = profile.get("profile_id")
        if profile_id:
            result[str(profile_id)] = profile
    return result


def delivery_profiles(schema):
    result = []
    for field in schema.get("fields", []):
        if field.get("name") == "delivery_profile_id":
            values = field.get("evidence_values", [])
            result.extend(str(value) for value in values)
    return sorted(set(result))


def validate_canonical_request(request, schema):
    if not isinstance(request, dict):
        raise ValueError("Canonical Production Request must be an object")

    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in request:
            raise ValueError(f"Forbidden simulation control: {forbidden}")

    if request.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Production Request schema_version must be 1.0")

    if not request.get("request_id"):
        raise ValueError("request_id is required")

    if request.get("mode") not in {"REVIEW", "PRODUCTION"}:
        raise ValueError("mode must be REVIEW or PRODUCTION")

    challenge_values = []
    for field in schema.get("fields", []):
        if field.get("name") == "challenge_id":
            challenge_values = field.get("allowed_values", [])

    challenge_id = request.get("challenge_id")
    if challenge_values and challenge_id not in challenge_values:
        raise ValueError(f"Unknown challenge_id: {challenge_id}")

    known_delivery = delivery_profiles(schema)
    delivery_id = request.get("delivery_profile_id")
    if known_delivery and delivery_id not in known_delivery:
        raise ValueError(f"Unknown delivery_profile_id: {delivery_id}")

    seed = request.get("seed")
    music_seed = request.get("music_seed")
    if seed is None or music_seed is None:
        raise ValueError("seed and music_seed are both required")

    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be integer")

    if not isinstance(music_seed, int) or isinstance(music_seed, bool):
        raise ValueError("music_seed must be integer")

    if "provenance" not in request:
        raise ValueError("provenance is required in canonical request")

    return True


def build_plan(request, schema, personalization_registry):
    validate_canonical_request(request, schema)

    personal_profiles = profile_registry(personalization_registry)
    personalization = request.get("personalization", {})
    personalization_enabled = bool(personalization.get("enabled", False))
    personalization_profile = personalization.get("profile_id", "UNKNOWN")

    if personalization_enabled:
        if personalization_profile == "UNKNOWN":
            raise ValueError(
                "Enabled personalization requires an explicit profile_id"
            )
        if personalization_profile not in personal_profiles:
            raise ValueError(
                f"Unknown personalization profile: {personalization_profile}"
            )

    # One canonical sequence. These are PLAN steps, not renderer calls.
    steps = [
        OrderedDict([
            ("step_id", "request_validation"),
            ("type", "VALIDATION"),
            ("authority", "CANONICAL"),
        ]),
        OrderedDict([
            ("step_id", "challenge_resolution"),
            ("type", "RESOLVE_CHALLENGE"),
            ("authority", "DECLARATIVE"),
            ("challenge_id", request["challenge_id"]),
        ]),
        OrderedDict([
            ("step_id", "delivery_profile_resolution"),
            ("type", "RESOLVE_DELIVERY_PROFILE"),
            ("authority", "REUSABLE_PROFILE"),
            ("delivery_profile_id", request["delivery_profile_id"]),
        ]),
        OrderedDict([
            ("step_id", "personalization_resolution"),
            ("type", "RESOLVE_PERSONALIZATION"),
            ("authority", "D4.3_RESOLVER"),
            ("enabled", personalization_enabled),
            ("profile_id", personalization_profile),
        ]),
        OrderedDict([
            ("step_id", "music_request"),
            ("type", "MUSIC_PLAN"),
            ("authority", "C11D_MUSIC_ENGINE_V5"),
            ("music_seed", request["music_seed"]),
            ("gameplay_rng_consumption", False),
        ]),
        OrderedDict([
            ("step_id", "production_plan"),
            ("type", "DELIVERY_PLAN"),
            ("authority", "CANONICAL_ORCHESTRATOR"),
            ("mode", request["mode"]),
        ]),
        OrderedDict([
            ("step_id", "artifact_provenance"),
            ("type", "PROVENANCE_PLAN"),
            ("authority", "CANONICAL"),
        ]),
    ]

    plan = OrderedDict([
        ("plan_id", PLAN_ID),
        ("plan_version", PLAN_VERSION),
        ("request_id", request["request_id"]),
        ("schema_id", SCHEMA_ID),
        ("schema_version", SCHEMA_VERSION),
        ("mode", request["mode"]),
        ("challenge_id", request["challenge_id"]),
        ("challenge_version", request.get("challenge_version", "UNKNOWN")),
        ("seed", request["seed"]),
        ("music_seed", request["music_seed"]),
        ("delivery_profile_id", request["delivery_profile_id"]),
        ("presentation_profile_id", request.get("presentation_profile_id", "UNKNOWN")),
        ("duration_seconds", request["duration_seconds"]),
        ("variation_index", request.get("variation_index", 0)),
        ("personalization", personalization),
        ("editorial", request.get("editorial", {})),
        ("output", request.get("output", {})),
        ("steps", steps),
        ("runtime_authority", "NONE"),
        ("simulation_truth_mutation", False),
        ("winning_frame_mutation", False),
        ("close_calls_mutation", False),
        ("gameplay_rng_consumption", False),
        ("structural_rng_consumption", False),
        ("renderer_activation", False),
        ("gui_activation", False),
        ("cli_production_activation", False),
        ("orchestrator_execution", False),
    ])

    plan_hash = sha256(plan)

    return plan, plan_hash


def make_fixture(challenge_id, delivery_profile_id, origin):
    return OrderedDict([
        ("request_id", "D4.4-ORCHESTRATOR-001"),
        ("schema_version", "1.0"),
        ("mode", "PRODUCTION"),
        ("challenge_id", challenge_id),
        ("challenge_version", "UNKNOWN"),
        ("seed", 123456),
        ("music_seed", 654321),
        ("delivery_profile_id", delivery_profile_id),
        ("presentation_profile_id", "UNKNOWN"),
        ("duration_seconds", 10.0),
        ("variation_index", 0),
        ("personalization", OrderedDict([
            ("enabled", True),
            ("profile_id", "editorial_text_v1"),
            ("values", OrderedDict([
                ("player_name", "TEST"),
                ("challenge_label", "UNKNOWN"),
            ])),
        ])),
        ("editorial", OrderedDict([
            ("title", "TEST"),
            ("subtitle", "UNKNOWN"),
            ("language", "es"),
            ("call_to_action", "JUEGA"),
        ])),
        ("output", OrderedDict([
            ("container", "mp4"),
            ("width", 720),
            ("height", 1280),
            ("fps", 30),
            ("audio_enabled", True),
        ])),
        ("provenance", OrderedDict([
            ("source_revision", "D4.4-TEST"),
            ("request_origin", origin),
            ("parent_request_id", "PARENT-TEST"),
        ])),
    ])


def run_self_test(schema_path, personalization_registry_path):
    schema = load_json(schema_path)
    personalization_registry = load_json(personalization_registry_path)

    if schema.get("schema_id") != SCHEMA_ID:
        raise AssertionError("schema_id mismatch")

    if schema.get("schema_version") != SCHEMA_VERSION:
        raise AssertionError("schema_version mismatch")

    if schema.get("runtime_authority") != "NONE":
        raise AssertionError("schema runtime authority must be NONE")

    challenge_values = []
    for field in schema.get("fields", []):
        if field.get("name") == "challenge_id":
            challenge_values = list(field.get("allowed_values", []))

    delivery_values = delivery_profiles(schema)

    if len(challenge_values) != 9:
        raise AssertionError(
            f"Expected 9 Challenge IDs, got {len(challenge_values)}"
        )

    if len(delivery_values) != 5:
        raise AssertionError(
            f"Expected 5 delivery profiles, got {len(delivery_values)}"
        )

    personal_profiles = profile_registry(personalization_registry)

    if "none_v1" not in personal_profiles:
        raise AssertionError("none_v1 missing from personalization registry")

    if "editorial_text_v1" not in personal_profiles:
        raise AssertionError("editorial_text_v1 missing from personalization registry")

    challenge_id = challenge_values[0]
    delivery_id = delivery_values[0]

    gui_request = make_fixture(challenge_id, delivery_id, "GUI")
    cli_request = make_fixture(challenge_id, delivery_id, "CLI")

    gui_plan, gui_hash = build_plan(
        gui_request,
        schema,
        personalization_registry,
    )

    cli_plan, cli_hash = build_plan(
        cli_request,
        schema,
        personalization_registry,
    )

    plan_json_equal = canonical_json(gui_plan) == canonical_json(cli_plan)
    plan_hash_equal = gui_hash == cli_hash

    if not plan_json_equal:
        raise AssertionError("GUI/CLI canonical Production Plan differs")

    if not plan_hash_equal:
        raise AssertionError("GUI/CLI Production Plan SHA-256 differs")

    if len(gui_hash) != 64:
        raise AssertionError("Production Plan SHA-256 has invalid length")

    # Personalization change must alter the plan but never alter either seed.
    changed = make_fixture(challenge_id, delivery_id, "GUI")
    changed["personalization"]["values"]["player_name"] = "OTHER"

    changed_plan, changed_hash = build_plan(
        changed,
        schema,
        personalization_registry,
    )

    personalization_plan_changed = changed_hash != gui_hash
    seeds_preserved = (
        changed_plan["seed"] == gui_plan["seed"] and
        changed_plan["music_seed"] == gui_plan["music_seed"]
    )

    if not personalization_plan_changed:
        raise AssertionError("Personalization change did not alter Production Plan identity")

    if not seeds_preserved:
        raise AssertionError("Personalization changed seed values")

    # Runtime boundary tests.
    boundary_pass = (
        gui_plan["runtime_authority"] == "NONE" and
        gui_plan["simulation_truth_mutation"] is False and
        gui_plan["winning_frame_mutation"] is False and
        gui_plan["close_calls_mutation"] is False and
        gui_plan["gameplay_rng_consumption"] is False and
        gui_plan["structural_rng_consumption"] is False and
        gui_plan["renderer_activation"] is False and
        gui_plan["gui_activation"] is False and
        gui_plan["cli_production_activation"] is False and
        gui_plan["orchestrator_execution"] is False
    )

    if not boundary_pass:
        raise AssertionError("Runtime boundary protection failed")

    # Forbidden simulation controls must be rejected.
    rejected = {}
    for field_name in ["winning_frame", "close_calls", "simulation_result"]:
        invalid = make_fixture(challenge_id, delivery_id, "TEST")
        invalid[field_name] = 1
        try:
            build_plan(invalid, schema, personalization_registry)
            rejected[field_name] = False
        except ValueError:
            rejected[field_name] = True

    if not all(rejected.values()):
        raise AssertionError("Forbidden simulation control acceptance detected")

    return OrderedDict([
        ("checkpoint", "C11-D D4.4"),
        ("result", "PASS"),
        ("status", "CLOSED"),
        ("plan_id", PLAN_ID),
        ("plan_version", PLAN_VERSION),
        ("challenge_count", len(challenge_values)),
        ("delivery_profile_count", len(delivery_values)),
        ("personalization_profile_count", len(personal_profiles)),
        ("gui_cli_plan_parity", OrderedDict([
            ("canonical_plan_equal", plan_json_equal),
            ("sha256_equal", plan_hash_equal),
            ("sha256", gui_hash),
        ])),
        ("personalization_isolation", OrderedDict([
            ("plan_hash_changes", personalization_plan_changed),
            ("seed_identical", seeds_preserved),
            ("music_seed_identical", seeds_preserved),
        ])),
        ("forbidden_simulation_controls_rejected", rejected),
        ("runtime_boundary", OrderedDict([
            ("runtime_authority", "NONE"),
            ("simulation_truth_mutation", False),
            ("winning_frame_mutation", False),
            ("close_calls_mutation", False),
            ("gameplay_rng_consumption", False),
            ("structural_rng_consumption", False),
            ("renderer_activation", False),
            ("gui_activation", False),
            ("cli_production_activation", False),
            ("orchestrator_execution", False),
        ])),
        ("example_plan", gui_plan),
        ("next", "D4.5 - CLI Adapter"),
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True)
    parser.add_argument("--personalization-registry", required=True)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--parity", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    result = run_self_test(
        args.schema,
        args.personalization_registry,
    )

    save_json(args.evidence, result)
    save_json(args.parity, result["gui_cli_plan_parity"])
    save_json(args.plan, result["example_plan"])
    save_json(args.receipt, result)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.4 ERROR: {exc}", file=sys.stderr)
        sys.exit(1)