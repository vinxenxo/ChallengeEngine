"""Static contract tests for the C11-D D9.8 Universal Editorial Model V1."""
from __future__ import annotations

import copy
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(MODULE_DIR))
import universal_editorial_model as editorial  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejects(call, reason: str) -> None:
    try:
        call()
    except editorial.EditorialModelError:
        NEGATIVES.append(reason)
        return
    raise AssertionError(f"Expected EditorialModelError: {reason}")


NEGATIVES: list[str] = []
model_path = ROOT / editorial.MODEL_REL
schema_path = ROOT / editorial.PRODUCER_SCHEMA_REL
model_hash_before = sha256(model_path)
schema_hash_before = sha256(schema_path)

model = editorial.load_model(ROOT)
catalog = editorial.build_catalog(ROOT)
summary = catalog["inventory_summary"]
assert summary == {
    "challenge_variants": 9,
    "visual_loop_families": 5,
    "visual_loop_concrete_grammars": 27,
    "visual_drill_types": 4,
    "visual_drill_variants": 20,
    "longform_enabled": False,
}, summary
assert model["seed_contract"]["master_seed"] == "NOT_ADOPTED"
assert model["seed_contract"]["gameplay_seed"] == "request.seed"
assert model["seed_contract"]["music_seed"] == "request.music_seed"
assert model["authority"]["runtime_authority"] == "NONE"
assert model["authority"]["renderer_activation"] is False
assert model["authority"]["production_execution"] is False
assert model["authority"]["release_authority"] == "NONE"

# Challenge remains the only content type that currently resolves through the D4 request/plan.
challenge = {"content_type": "challenges", "variant_id": "CHALLENGE_001"}
challenge_node = editorial.resolve_selection(challenge, ROOT)
assert challenge_node["request_plan_compatible"] is True
assert challenge_node["family_id"] == "key"
challenge_values = editorial.resolve_editorial_values(
    challenge,
    profile={
        "global": {"title": " Global title ", "language": " ES "},
        "content_type": {"challenges": {"title": "Challenge title", "subtitle": "Subtitle"}},
        "family": {"challenge-family:key": {"call_to_action": "Play"}},
        "variant": {"challenge:CHALLENGE_001": {"player_name": " Ada "}},
    },
    production_override={"title": " Final title ", "challenge_label": "  One  "},
    project_root=ROOT,
)
assert challenge_values["values"]["title"] == "Final title"
assert challenge_values["values"]["subtitle"] == "Subtitle"
assert challenge_values["values"]["language"] == "es"
assert challenge_values["values"]["call_to_action"] == "Play"
assert challenge_values["values"]["player_name"] == "Ada"
assert challenge_values["values"]["challenge_label"] == "One"
assert challenge_values["request_plan_state"] == "CURRENT_D4_CHALLENGE_PATH"
assert challenge_values["renderer_activation"] is False
assert challenge_values["release_authority"] == "NONE"

# Visual Loop inventory is resolvable editorially but deliberately not yet D4 plan-compatible.
loop = {
    "content_type": "visual_loops",
    "family_id": "c11c_geometric_waves_v1",
    "subtype_id": "harmonic_membrane",
}
loop_node = editorial.resolve_selection(loop, ROOT)
assert loop_node["request_plan_compatible"] is False
loop_values = editorial.resolve_editorial_values(
    loop,
    profile={
        "global": {"language": " ES "},
        "family": {"visual-loop-family:c11c_geometric_waves_v1": {"title": "Waves"}},
        "subtype": {"visual-loop-grammar:c11c_geometric_waves_v1/harmonic_membrane": {"subtitle": "Membrane"}},
    },
    project_root=ROOT,
)
assert loop_values["values"]["title"] == "Waves"
assert loop_values["values"]["subtitle"] == "Membrane"
assert loop_values["values"]["language"] == "es"
assert loop_values["request_plan_state"] == "PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER"

# Visual Drill includes type + explicit declared difficulty tier; telemetry stays read-only.
drill = {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"}
drill_node = editorial.resolve_selection(drill, ROOT)
assert drill_node["difficulty_tier"] == 1
assert drill_node["request_plan_compatible"] is False
assert catalog["content_types"]["visual_drills"]["variant_count"] == 20

# Negative selection and editorial boundary cases.
rejects(lambda: editorial.resolve_selection({"content_type": "bogus", "variant_id": "X"}, ROOT), "unknown content type")
rejects(lambda: editorial.resolve_selection({"content_type": "challenges", "variant_id": "NOT_REAL"}, ROOT), "unknown Challenge variant")
rejects(lambda: editorial.resolve_selection({"content_type": "visual_loops", "family_id": "missing", "subtype_id": "auto"}, ROOT), "unknown Loop family")
rejects(lambda: editorial.resolve_selection({"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "missing"}, ROOT), "unknown Loop grammar")
rejects(lambda: editorial.resolve_selection({"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-99"}, ROOT), "unknown Drill tier")
rejects(lambda: editorial.resolve_selection({"content_type": "longform"}, ROOT), "Longform explicitly disabled")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"seed": "42"}, project_root=ROOT), "gameplay seed not editorial")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"music_seed": "42"}, project_root=ROOT), "music seed not editorial")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"winning_frame": "12"}, project_root=ROOT), "simulation truth not editorial")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"request_hash": "abc"}, project_root=ROOT), "provenance not editorial")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"duration_seconds": "15"}, project_root=ROOT), "telemetry not editorial")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"hook": "Not enabled"}, project_root=ROOT), "reserved editorial field disabled")
rejects(lambda: editorial.resolve_editorial_values(loop, production_override={"player_name": "not for Loop"}, project_root=ROOT), "Challenge-only field rejected on Loop")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"unknown_field": "bad"}, project_root=ROOT), "unknown editorial field")
rejects(lambda: editorial.resolve_editorial_values(challenge, production_override={"title": "x" * 161}, project_root=ROOT), "editorial max length")
rejects(lambda: editorial.resolve_editorial_values(challenge, profile={"global": {"player_name": "scope violation"}}, project_root=ROOT), "Challenge-only field rejected globally")
rejects(lambda: editorial.resolve_editorial_values(challenge, profile={"mystery_layer": {}}, project_root=ROOT), "unknown inheritance layer")
rejects(lambda: editorial.resolve_editorial_values(challenge, profile={"family": {"not-a-canonical-scope": {"title": "x"}}}, project_root=ROOT), "unknown family editorial scope")
rejects(lambda: editorial.resolve_editorial_values(challenge, profile={"content_type": []}, project_root=ROOT), "malformed content-type profile layer")
rejects(lambda: editorial.resolve_editorial_values(challenge, profile={"variant": {"challenge:CHALLENGE_001": {"hook": "disabled"}}}, project_root=ROOT), "reserved field rejected in non-selected profile scope")

bad = copy.deepcopy(model)
bad["authority"]["runtime_authority"] = "EXECUTE"
rejects(lambda: editorial.validate_model_definition(bad), "runtime authority elevation rejected")
bad = copy.deepcopy(model)
bad["seed_contract"]["automatic_seed_generation"] = True
rejects(lambda: editorial.validate_model_definition(bad), "automatic seed generation rejected")
bad = copy.deepcopy(model)
bad["content_types"]["longform"]["enabled_for_selection"] = True
rejects(lambda: editorial.validate_model_definition(bad), "Longform activation rejected by model contract")
bad = copy.deepcopy(model)
bad["data_classes"]["derived_telemetry"]["editable"] = True
rejects(lambda: editorial.validate_model_definition(bad), "telemetry editability elevation rejected")
bad = copy.deepcopy(model)
bad["content_types"]["visual_drills"]["editable_fields"].append("player_name")
rejects(lambda: editorial.validate_model_definition(bad), "invalid field/content-type assignment rejected")

assert sha256(model_path) == model_hash_before, "Model changed while running tests"
assert sha256(schema_path) == schema_hash_before, "Producer inventory changed while running tests"
assert len(NEGATIVES) == 25, (len(NEGATIVES), NEGATIVES)
print(
    "C11-D D9.8 UNIVERSAL EDITORIAL MODEL PASS | "
    f"challenge={summary['challenge_variants']}/9 | "
    f"loops={summary['visual_loop_families']} families/{summary['visual_loop_concrete_grammars']} grammars | "
    f"drills={summary['visual_drill_types']} types/{summary['visual_drill_variants']} tiers | "
    f"negative={len(NEGATIVES)}/25 | longform=EXPLICITLY_DISABLED | "
    "renderer=OFF | production=false | release_authority=NONE"
)
