from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
DECISION_REL = Path("docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json")
PINS_REL = Path("tools/c11d/d9/C11E_E4B_LOOP_FAMILY_CONTRACT_SOURCE_PINS_V1.json")
SCHEMA_REL = Path("c11c-suite/c11c-producer/producer_schema.json")
VARIATION_REL = Path("tools/prototypes/c11c_common/C11CVariationProfile.gd")
MUSIC_REGISTRY_REL = Path("profiles/presentation/c11c_visual_music_profiles.json")
READINESS_REPORT_REL = Path("artifacts/tests/c11e/e4b_loop_policy_readiness/20261106T215629Z-495EAB8C/C11E_E4B_LOOP_POLICY_READINESS_REPORT_V1.json")
GUI_MATRIX_REL = Path("artifacts/tests/c11e/e4b_loop_family_matrix/E4B_LOOP_GUI_20261106T211920Z_F9377504/matrix_report.json")
CLI_MATRIX_REL = Path("artifacts/tests/c11e/e4b_loop_family_matrix/CLI_20261106T212054Z-DE8364C4/matrix_report.json")
IDENTITY_FIELDS = (
    "canonical_request_hash", "editorial_hash", "plan_hash", "bridge_hash",
    "adapter_envelope_hash", "e1_request_hash", "e1_plan_hash", "e1_intent_hash",
    "music_profile_id_from_frozen_c11c_profile_registry",
)
SCENARIOS = ("BASELINE", "GAMEPLAY_SEED_ONLY_CHANGED", "MUSIC_SEED_ONLY_CHANGED")

class AuditError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.is_file():
        raise AuditError(f"Missing required source: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value: Any, hash_key: str = "report_sha256") -> str:
    unsigned = dict(value)
    unsigned.pop(hash_key, None)
    raw = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha256_bytes(raw)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise AuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise AuditError(f"JSON root must be an object: {path}")
    return data


def _extract_balanced(source: str, marker: str, opening: str = "(") -> str:
    start = source.find(marker)
    if start < 0:
        raise AuditError(f"GDScript/PowerShell marker not found: {marker}")
    i = start + len(marker)
    closing = {"(": ")", "[": "]", "{": "}"}[opening]
    depth = 1
    quote = None
    escaped = False
    body_start = i
    while i < len(source):
        char = source[i]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        else:
            if char in ("'", '"'):
                quote = char
            elif char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return source[body_start:i]
        i += 1
    raise AuditError(f"Unclosed balanced expression after {marker}")


def _split_top_level(value: str) -> list[str]:
    parts: list[str] = []
    start = 0
    stack: list[str] = []
    quote = None
    escaped = False
    pairs = {")": "(", "]": "[", "}": "{"}
    for index, char in enumerate(value):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
        elif char in "([{" :
            stack.append(char)
        elif char in ")]}":
            if not stack or stack[-1] != pairs[char]:
                raise AuditError("Unbalanced nested expression while splitting arguments")
            stack.pop()
        elif char == "," and not stack:
            parts.append(value[start:index].strip())
            start = index + 1
    tail = value[start:].strip()
    if tail:
        parts.append(tail)
    elif value.strip():
        raise AuditError("Unexpected empty final argument")
    return parts


def _function_body(source: str, signature_prefix: str) -> str:
    pos = source.find(signature_prefix)
    if pos < 0:
        raise AuditError(f"Missing required function: {signature_prefix}")
    body_start = source.find("\n", source.find(":", pos))
    if body_start < 0:
        raise AuditError(f"Malformed function body: {signature_prefix}")
    body_start += 1
    next_fn = re.search(r"\n(?:static )?func\s+", source[body_start:])
    end = body_start + next_fn.start() if next_fn else len(source)
    return source[body_start:end]


def _return_dict_keys(function_body: str, function_name: str) -> set[str]:
    marker = "return {"
    pos = function_body.find(marker)
    if pos < 0:
        raise AuditError(f"{function_name} does not return a dictionary")
    body = _extract_balanced(function_body[pos:], "return {", opening="{")
    return set(re.findall(r"[\"']([a-zA-Z0-9_]+)[\"']\s*:", body))


def _validate_decisions(root: Path) -> dict[str, Any]:
    record = read_json(root / DECISION_REL)
    if record.get("schema") != "C11E-E4B-OPERATOR-POLICY-DECISION-RECORD-V1" or record.get("schema_version") != "1.0":
        raise AuditError("Operator decision record identity/version mismatch")
    if record.get("decision_source") != "EXPLICIT_OPERATOR_MESSAGE_IN_CONVERSATION":
        raise AuditError("Decision record does not identify the explicit operator instruction")
    expected = {
        "A.1_SHARED_PRESENTATION_REGIONS": ("definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json", "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a"),
        "A.3_LOOP_DRILL_EDITORIAL_WINDOWS": ("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"),
        "E4B_LOOP_COMPOSITION": ("definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json", "9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da"),
        "B.1_UNIFIED_DELIVERY_TIMEBASE": ("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json", "41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85"),
        "D.1_AUDIO_MUSIC_DELIVERY_ENVELOPE": ("definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json", "3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23"),
    }
    rows = record.get("decisions")
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise AuditError("Exactly five current-hash decisions are required")
    decisions: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise AuditError("Malformed decision row")
        key = row.get("decision_id")
        if key in decisions:
            raise AuditError(f"Duplicate decision: {key}")
        decisions[key] = row
    if set(decisions) != set(expected):
        raise AuditError("Decision IDs do not match the five authorized decision groups")
    for key, (rel, sha) in expected.items():
        row = decisions[key]
        if row.get("proposal_path") != rel or row.get("proposal_sha256") != sha or row.get("decision") != "APPROVE_AS_PROPOSED":
            raise AuditError(f"Decision does not approve the exact current hash: {key}")
        if sha256_file(root / rel) != sha:
            raise AuditError(f"Current proposal SHA-256 drift: {rel}")
    boundary = record.get("scope_boundary", {})
    required_false = (
        "renderer_native_input_emission_authorized", "renderer_activation_authorized",
        "production_dispatch_authorized", "media_creation_authorized",
        "audio_asset_selection_authorized", "audio_generation_authorized",
        "audio_payload_materialization_authorized", "release_promotion_authorized",
    )
    if any(boundary.get(key) is not False for key in required_false):
        raise AuditError("Operator design decisions were incorrectly expanded into execution or release authority")
    if boundary.get("d4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        raise AuditError("Permanent governance boundary drift")
    if record.get("policy_proposal_files_mutated") is not False:
        raise AuditError("The historical proposal JSON files must remain unmodified")
    return {"record_id": record.get("record_id"), "decision_count": len(rows), "decision": "APPROVE_AS_PROPOSED", "sha256_by_group": {k: expected[k][1] for k in expected}, "execution_authority_granted": False}


def _validate_policy_boundaries(root: Path) -> dict[str, Any]:
    proposals = {
        "A.1": "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json",
        "A.3": "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json",
        "LOOP_COMPOSITION": "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json",
        "B.1": "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json",
        "D.1": "definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json",
    }
    observed = {}
    for label, rel in proposals.items():
        data = read_json(root / rel)
        observed[label] = {"status": data.get("status"), "sha256": sha256_file(root / rel)}
        if label == "LOOP_COMPOSITION":
            gates = data.get("approval_gates", {})
            if gates.get("renderer_native_input_emitted") is not False or gates.get("renderer_activation") is not False or gates.get("production_dispatch") is not False or gates.get("media_created") is not False:
                raise AuditError("Loop composition proposal boundary flags were changed")
        elif label == "D.1":
            policy = data.get("policy", {})
            forbidden = ("OUT_OF_SCOPE_NOT_SELECTED_NOT_EMITTED", "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED")
            if policy.get("music_asset_policy") != forbidden[0] or policy.get("mixing_policy") != forbidden[1]:
                raise AuditError("D.1 music-selection/mixing exclusions changed")
            if data.get("execution_boundary", {}).get("audio_samples_emitted") is not False:
                raise AuditError("D.1 cannot emit audio samples")
        if data.get("status") not in ("PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT", "PROPOSAL_ONLY_NOT_RENDERER_INPUT"):
            raise AuditError(f"Proposal status must remain review-only: {label}")
    return observed


def _validate_matrix_evidence(root: Path) -> dict[str, Any]:
    gui = read_json(root / GUI_MATRIX_REL)
    cli = read_json(root / CLI_MATRIX_REL)
    gui_hash = sha256_file(root / GUI_MATRIX_REL)
    cli_hash = sha256_file(root / CLI_MATRIX_REL)
    for report, label in ((gui, "GUI"), (cli, "CLI")):
        if report.get("schema") != "C11E-E4B-LOOP-FAMILY-MATRIX-RECEIPT-V1" or report.get("status") != "PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY":
            raise AuditError(f"{label} matrix evidence status mismatch")
        if canonical_hash(report) != report.get("report_sha256"):
            raise AuditError(f"{label} matrix report internal self-hash mismatch")
        if len(report.get("cases", [])) != 81 or len(report.get("seed_domain_relations", [])) != 27:
            raise AuditError(f"{label} matrix row count mismatch")
        governance = report.get("governance", {})
        for key in ("renderer_input_emitted", "renderer_dispatch_invoked", "production_execution", "media_created", "godot_invoked", "c11c_family_visual_generators_invoked", "c11c_family_music_generator_invoked", "d3_v5_invoked", "ffmpeg_invoked", "c11c_baseline_modified"):
            if governance.get(key) is not False:
                raise AuditError(f"{label} matrix governance flag is not false: {key}")
        if governance.get("d4_8") != "BLOCKED" or governance.get("release_authority") != "NONE":
            raise AuditError(f"{label} matrix governance boundary mismatch")
    gui_cases = {(c["family_id"], c["subtype_id"], c["scenario"]): c for c in gui["cases"]}
    cli_cases = {(c["family_id"], c["subtype_id"], c["scenario"]): c for c in cli["cases"]}
    if set(gui_cases) != set(cli_cases) or len(gui_cases) != 81:
        raise AuditError("GUI/CLI case key set mismatch")
    equal = 0
    for key in gui_cases:
        a, b = gui_cases[key], cli_cases[key]
        if a.get("d9_plan_kind") != "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY" or b.get("d9_plan_kind") != "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY":
            raise AuditError("Matrix case is not plan-only")
        if a.get("e1_editorial_consumer_status") != "NOT_CONSUMED_E1" or b.get("e1_editorial_consumer_status") != "NOT_CONSUMED_E1":
            raise AuditError("Matrix E1 editorial state unexpectedly changed")
        if a.get("e1_adapter_status") != "NOT_CONNECTED_E1" or b.get("e1_adapter_status") != "NOT_CONNECTED_E1":
            raise AuditError("Matrix family adapter state unexpectedly changed")
        if a.get("music_engine_invoked") is not False or b.get("music_engine_invoked") is not False:
            raise AuditError("Matrix unexpectedly invoked family music")
        for field in IDENTITY_FIELDS:
            if a.get(field) != b.get(field):
                raise AuditError(f"GUI/CLI identity mismatch {key} field={field}")
        equal += 1
    readiness = read_json(root / READINESS_REPORT_REL)
    if readiness.get("status") != "PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED" or readiness.get("stale_packet_v1_hash_count") != 3:
        raise AuditError("Prior Windows policy readiness receipt does not match accepted state")
    return {
        "gui_report_sha256": gui_hash, "cli_report_sha256": cli_hash,
        "gui_cases": len(gui_cases), "cli_cases": len(cli_cases),
        "canonical_identity_fields": len(IDENTITY_FIELDS),
        "gui_cli_canonical_identity_equal": f"{equal}/{len(IDENTITY_FIELDS)}_CASES_X_9_FIELDS",
        "readiness_report_status": readiness["status"],
        "readiness_report_raw_sha256": sha256_file(root / READINESS_REPORT_REL),
        "matrix_is_plan_only": True,
    }


def _family_files(root: Path, family_id: str, prototype_rel: str) -> tuple[Path, Path]:
    family_dir = root / "tools" / "prototypes" / family_id
    protos = list(family_dir.glob("*Prototype.gd"))
    renderers = list(family_dir.glob("*Renderer.gd"))
    if len(protos) != 1 or len(renderers) != 1:
        raise AuditError(f"Expected one prototype and one renderer for {family_id}")
    if (root / Path(prototype_rel)).resolve() != (family_dir / "run_prototype.ps1").resolve():
        raise AuditError(f"Producer schema launcher path mismatch for {family_id}")
    return protos[0], renderers[0]


def _validate_family_interfaces(root: Path) -> dict[str, Any]:
    schema = read_json(root / SCHEMA_REL)
    variation_source = (root / VARIATION_REL).read_text(encoding="utf-8-sig")
    variation_hash = sha256_file(root / VARIATION_REL)
    music_registry = read_json(root / MUSIC_REGISTRY_REL)
    families = schema.get("families", {})
    if len(families) != 5:
        raise AuditError("Producer schema family count is not five")
    builder_suffix = {
        "geometric": "geometric", "fractal": "fractal", "sacred_symmetry": "sacred",
        "living_particles": "living", "invisible_forces": "invisible",
    }
    rows: list[dict[str, Any]] = []
    total_grammars = 0
    for family_id, config in families.items():
        internal = config.get("internal")
        if internal not in builder_suffix:
            raise AuditError(f"Unknown C11C internal family id: {internal}")
        prototype, renderer = _family_files(root, family_id, config.get("prototype", ""))
        proto_text = prototype.read_text(encoding="utf-8-sig")
        renderer_text = renderer.read_text(encoding="utf-8-sig")
        builder_name = "_" + builder_suffix[internal]
        builder_body = _function_body(variation_source, f"static func {builder_name}(")
        profile_keys = _return_dict_keys(builder_body, builder_name)
        grammar_match = re.search(r"const GRAMMAR_IDS\s*:\s*Array\[String\]\s*=\s*\[(.*?)\]", proto_text, re.S)
        if not grammar_match:
            raise AuditError(f"Prototype grammar IDs not found: {prototype}")
        prototype_grammars = re.findall(r"[\"']([a-z0-9_]+)[\"']", grammar_match.group(1))
        schema_grammars = [str(item[0]) for item in config.get("grammars", []) if isinstance(item, list) and item and item[0] != "auto"]
        if prototype_grammars != schema_grammars:
            raise AuditError(f"Producer schema vs C11C prototype grammar mismatch: {family_id}")
        total_grammars += len(prototype_grammars)
        if f'VariationProfileClass.build("{internal}", _seed)' not in proto_text:
            raise AuditError(f"Prototype does not bind requested gameplay seed to C11C family variation profile: {family_id}")
        if "func _apply_grammar_override()" not in proto_text or "requested == technical_id" not in proto_text:
            raise AuditError(f"Prototype grammar override contract is missing: {family_id}")
        if "C11C_VISUAL_GRAMMAR" not in proto_text or "C11C_SEED" not in proto_text:
            raise AuditError(f"Prototype selector/seed environment contract is missing: {family_id}")
        # C11C style arguments are family-specific. Match arity and each referenced profile key.
        call_args = _split_top_level(_extract_balanced(proto_text, "_renderer.set_style("))
        signature_args = _split_top_level(_extract_balanced(renderer_text, "func set_style("))
        if len(call_args) != len(signature_args):
            raise AuditError(f"C11C renderer style call/signature arity mismatch: {family_id}")
        style_pos = proto_text.find("_renderer.set_style(")
        prefix = proto_text[:style_pos]
        variation_refs = set(re.findall(r'_variation\["([a-z0-9_]+)"\]', prefix))
        missing = sorted(variation_refs - profile_keys)
        if missing:
            raise AuditError(f"Prototype requests missing family variation fields {family_id}: {missing}")
        # Verify launcher is a test-isolatable, silent, exact grammar entry point.
        launcher_path = root / config["prototype"]
        launcher_text = launcher_path.read_text(encoding="utf-8-sig")
        header = launcher_text[:launcher_text.find("$ErrorActionPreference")]
        for param in ("$Seed", "$Grammar", "$NoSound", "$OutputRoot", "$OutputTag"):
            if param.lower() not in header.lower():
                raise AuditError(f"Family launcher lacks {param}: {family_id}")
        # Existing C11-C audio still consumes the visual seed from the family launcher.
        if "C11CSafeAmbient.py" not in launcher_text or re.search(r"\$AudioScript\s+\$Audio\s+\$Seed\s+\$loopCycles", launcher_text) is None:
            raise AuditError(f"C11C family audio seed path drift: {family_id}")
        music = music_registry.get("bindings", {}).get(f"visual_loop/{internal}")
        if not isinstance(music, dict):
            raise AuditError(f"C11C FAMILY_MUSIC_V4 profile binding missing: {internal}")
        profile_id = music.get("profile")
        known_profiles = {p.get("id") for p in music_registry.get("profiles", []) if isinstance(p, dict)}
        if profile_id not in known_profiles or music.get("music_semantic_inputs") != ["seed", "visual_grammar"]:
            raise AuditError(f"C11C family music profile/semantic inputs mismatch: {internal}")
        rows.append({
            "family_id": family_id, "internal_id": internal,
            "prototype_path": prototype.relative_to(root).as_posix(),
            "renderer_path": renderer.relative_to(root).as_posix(),
            "launcher_path": config["prototype"],
            "grammar_ids": prototype_grammars,
            "grammar_count": len(prototype_grammars),
            "variation_profile_builder": builder_name,
            "variation_profile_fields_referenced": len(variation_refs),
            "renderer_set_style_parameter_count": len(signature_args),
            "launcher_contract": ["Seed", "Grammar", "NoSound", "OutputRoot", "OutputTag"],
            "family_music_profile_id": profile_id,
            "music_semantic_inputs_in_C11C_registry": music.get("music_semantic_inputs"),
            "existing_launcher_music_uses_visual_seed": True,
            "D_route_requirement": "C11C_VISUAL_NO_SOUND; MUSIC_ASSET_GENERATION_NOT_AUTHORIZED_BY_D1",
        })
    if total_grammars != 27:
        raise AuditError(f"Expected 27 concrete C11C grammar selectors, observed {total_grammars}")
    return {"family_count": len(rows), "grammar_count": total_grammars, "families": rows, "variation_profile_sha256": variation_hash}


def _validate_historical_products(root: Path, family_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_family: dict[str, dict[str, dict[str, Any]]] = {}
    for family in family_rows:
        by_family[family["family_id"]] = {g: None for g in family["grammar_ids"]}
    base = root / "artifacts" / "production" / "audiovisual"
    for family_id, grammar_map in by_family.items():
        family_dir = base / family_id
        if not family_dir.is_dir():
            raise AuditError(f"Missing historical C11C audiovisual product root: {family_id}")
        for manifest_path in sorted(family_dir.glob("*/production_manifest.json")):
            try:
                manifest = read_json(manifest_path)
            except AuditError:
                continue
            grammar = manifest.get("grammar_id")
            if grammar not in grammar_map or manifest.get("delivery_profile") != "REVIEW_720":
                continue
            if manifest.get("schema") != "C11-C-PRODUCTION-PRODUCT-V3" or str(manifest.get("revision")) != "2.19.12" or manifest.get("status") != "FINAL_PRODUCT":
                continue
            file_names = manifest.get("files", [])
            author_name = next((n for n in file_names if isinstance(n, str) and n.endswith("_authoring.json")), None)
            if not author_name:
                continue
            author_path = manifest_path.parent / author_name
            if not author_path.is_file():
                continue
            author = read_json(author_path)
            if author.get("seed") != manifest.get("seed") or author.get("grammar_id") != grammar:
                continue
            if author.get("frame_count") != manifest.get("frames") or int(round(float(author.get("duration_seconds", 0)) * float(author.get("fps", 0)))) != manifest.get("frames"):
                continue
            if manifest.get("fps") != 30 or manifest.get("frames") != int(round(float(manifest.get("duration_seconds", 0)) * 30)):
                continue
            if grammar_map[grammar] is None:
                mp4_name = next((n for n in file_names if isinstance(n, str) and n.lower().endswith(".mp4")), None)
                mp4_exists = bool(mp4_name and (manifest_path.parent / mp4_name).is_file())
                grammar_map[grammar] = {
                    "product_id": manifest.get("product_id"),
                    "seed": manifest.get("seed"),
                    "grammar_id": grammar,
                    "delivery_profile": "REVIEW_720",
                    "fps": manifest.get("fps"),
                    "duration_seconds": manifest.get("duration_seconds"),
                    "frames": manifest.get("frames"),
                    "sound_enabled": manifest.get("sound_enabled"),
                    "manifest_path": manifest_path.relative_to(root).as_posix(),
                    "manifest_sha256": sha256_file(manifest_path),
                    "authoring_path": author_path.relative_to(root).as_posix(),
                    "authoring_sha256": sha256_file(author_path),
                    "mp4_listed_in_manifest": bool(mp4_name),
                    "mp4_present_in_snapshot": mp4_exists,
                }
    coverage = []
    for family_id, grammar_map in by_family.items():
        missing = sorted(g for g,v in grammar_map.items() if v is None)
        if missing:
            raise AuditError(f"Historical C11C manifest/authoring evidence missing for {family_id}: {missing}")
        for grammar in sorted(grammar_map):
            coverage.append({"family_id": family_id, **grammar_map[grammar]})
    if len(coverage) != 27:
        raise AuditError("Historical C11C product coverage was not exactly 27/27")
    return {
        "selector_count": len(coverage),
        "manifest_authoring_pairs": "27/27",
        "all_review_720_30fps": all(x["delivery_profile"] == "REVIEW_720" and x["fps"] == 30 for x in coverage),
        "all_frames_match_duration": all(x["frames"] == round(x["duration_seconds"] * x["fps"]) for x in coverage),
        "mp4_present_in_snapshot_count": sum(1 for x in coverage if x["mp4_present_in_snapshot"]),
        "evidence_scope": "HISTORICAL_PRODUCT_MANIFEST_AND_AUTHORING_METADATA_ONLY_NO_MP4_VISUAL_REVIEW",
        "selectors": coverage,
    }


def build_report(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root).resolve()
    pins = read_json(root / PINS_REL).get("source_pins")
    if not isinstance(pins, list) or not pins:
        raise AuditError("Source pin list is missing or empty")
    pin_results = []
    for item in pins:
        rel, expected = item.get("path"), item.get("sha256")
        if not isinstance(rel, str) or not isinstance(expected, str) or len(expected) != 64:
            raise AuditError("Malformed source pin row")
        actual = sha256_file(root / Path(*Path(rel).parts))
        if actual != expected:
            raise AuditError(f"Source pin mismatch: {rel}")
        pin_results.append({"path": rel, "sha256": actual})
    decision_result = _validate_decisions(root)
    policy_result = _validate_policy_boundaries(root)
    matrix_result = _validate_matrix_evidence(root)
    family_result = _validate_family_interfaces(root)
    product_result = _validate_historical_products(root, family_result["families"])
    d98_model = read_json(root / "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
    loop_d98 = d98_model.get("content_types", {}).get("visual_loops", {})
    if loop_d98.get("model_state") != "ACTIVE_MODEL_ONLY" or loop_d98.get("request_plan_compatibility") != "PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER":
        raise AuditError("D9.8 source metadata drift; reconcile manually before any next implementation")
    c11c_manifest_sha = sha256_file(root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    report = {
        "schema": "C11E-E4B-LOOP-FAMILY-CONTRACT-AUDIT-V1",
        "status": "PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY",
        "project_snapshot_sha256": "4746c2787c85a06caf46b0e9b961ea1ccc81a51516e727406c2799a3487272e4",
        "frozen_c11c_manifest_sha256": c11c_manifest_sha,
        "source_pin_count": len(pin_results),
        "source_pins": pin_results,
        "operator_decisions": decision_result,
        "policy_proposal_states_preserved": policy_result,
        "matrix_evidence": matrix_result,
        "d98_d99_semantics": {
            "d98_model_state": loop_d98.get("model_state"),
            "d98_request_plan_compatibility_metadata": loop_d98.get("request_plan_compatibility"),
            "d99_capability_evidenced": "PLAN_ONLY_27_SELECTORS_81_CASES",
            "d4_executable_compatibility": "NOT_PROVEN",
            "metadata_source_mutated": False,
        },
        "family_interface_audit": family_result,
        "historical_product_coverage": product_result,
        "audio_seed_boundary": {
            "default_c11c_launchers_use_visual_seed_for_existing_audio": True,
            "d_visual_invocation_requirement": "NO_SOUND_FOR_VISUAL_STAGE",
            "d1_audio_generation_or_materialization_authorized": False,
            "music_seed_domain": "request.music_seed",
            "d3_v5_for_visual_loop": False,
        },
        "governance": {
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "production_execution": False,
            "media_created": False,
            "godot_invoked": False,
            "c11c_family_visual_generators_invoked": False,
            "c11c_family_music_generator_invoked": False,
            "d3_v5_invoked": False,
            "ffmpeg_invoked": False,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
            "release_authority": "NONE",
        },
    }
    report["report_sha256"] = canonical_hash(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only C11-E E4B Loop family source-contract audit")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    report = build_report(args.project_root)
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(raw)
    output.with_suffix(".sha256").write_text(sha256_bytes(raw) + "  " + output.name + "\n", encoding="ascii")
    print("C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT=" + report["status"])
    print("DECISIONS=" + str(report["operator_decisions"]["decision_count"]) + "/5")
    print("FAMILIES=" + str(report["family_interface_audit"]["family_count"]) + "; GRAMMARS=" + str(report["family_interface_audit"]["grammar_count"]))
    print("STYLE_SIGNATURES=5/5; HISTORICAL_PRODUCT_MANIFEST_AUTHORING=27/27")
    print("MP4_VISUAL_EVIDENCE_IN_SNAPSHOT=" + str(report["historical_product_coverage"]["mp4_present_in_snapshot_count"]) + "/27")
    print("D98_COMPATIBILITY=" + report["d98_d99_semantics"]["d98_request_plan_compatibility_metadata"] + "; D99=PLAN_ONLY")
    print("RENDERER=OFF; MEDIA=FALSE; D4.8=BLOCKED; RELEASE_AUTHORITY=NONE")
    print("REPORT_SHA256=" + sha256_bytes(raw))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as exc:
        print("C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT=FAIL")
        print("ERROR=" + str(exc))
        raise SystemExit(2)
