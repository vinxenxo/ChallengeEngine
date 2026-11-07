from __future__ import annotations

"""Prepare/validate 27 request-bound C11-C Loop family parameter payloads.

R1P is parameter materialization only. It does not instantiate prototypes or
renderers, invoke family launchers, create frame buffers/pixels/media, or grant
D4.8 / dispatch / release authority.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

# This runner is read-only against source paths; prevent import-time .pyc writes.
sys.dont_write_bytecode = True

SCHEMA = "C11E-E4B-R1P-LOOP-PARAMETER-PAYLOAD-RUN-V1"
INPUT_SCHEMA = "C11E-E4B-R1P-GODOT-INPUT-V1"
GODOT_PREFIX = "C11E_E4B_R1P_RESULT="
EXPECTED_C11C_MANIFEST = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"

# Exact source pins established from V80 and the successful live-checkout R1P
# schema/profile/prototype/launcher audit supplied by the operator.
EXPECTED_PINS: dict[str, str] = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": EXPECTED_C11C_MANIFEST,
    "c11c-suite/c11c-producer/producer_schema.json": "564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0",
    "tools/prototypes/c11c_common/C11CVariationProfile.gd": "f7df994d8842183275bc331decd75762a153f3100248c7cc8b590e34c1347e2d",
    "tools/prototypes/c11c_common/C11CPaletteBank.gd": "6b64d99afb148b0dc5b0f8e27b50558e9b77df4d2fdff98d52495d81d53fdd14",
    "tools/prototypes/c11c_common/C11CEditorialColors.gd": "46326fbd732d514b5bfa2d964b99bdd14f2933dd01ec65689749bf40fda32632",
    "tools/prototypes/c11c_common/C11CVisualLoopDuration.gd": "4ea0b0decbd3a22ade42023e819a74872f312b63facc1163dc73a7c656fdbaf8",
    "tools/prototypes/c11c_common/TechnobabbleGenerator.gd": "f2fbef4ee4b8b07d1b4ebe7781bc5d987e37c43a5f5eb317397a377288890c9f",
    "tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd": "b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55",
    "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd": "ab2560cbe7fa42c5cad3b143aa59d1f2a0dc047682f7667983c7c0a0f6dbb61c",
    "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd": "12fdbc13e05df28b26cf95fe1907d150bd41f29196287700153521e9baee336b",
    "tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd": "835ba0df2c160a259be39bd1977bfac0e6a66f903ce1aa6b4247af7c508ad94a",
    "tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd": "a68661a5fdf792aa7fe701afa6fbf1631a2b8215c214032f58ecfe0c69d8374a",
    "tools/prototypes/c11c_fractal_bloom_v1/run_prototype.ps1": "02e3721c92046f1f69119e5bbc6c69709dd0b97fad7191c08213ecc233930801",
    "tools/prototypes/c11c_geometric_waves_v1/run_prototype.ps1": "661bd61df61bc633e4b87cd4b9413c4317c8d4b6068194245aea7d40fcb5c7cd",
    "tools/prototypes/c11c_sacred_symmetry_v1/run_prototype.ps1": "8eea21f7b72f679d8951410597f0ecf968ac0a6f1ee629a48de965ea62b60b6e",
    "tools/prototypes/c11c_living_particles_v1/run_prototype.ps1": "3674fdf778927022d2ebc1d1a96865b441479c5e4e71802e90837d654278a638",
    "tools/prototypes/c11c_invisible_forces_v1/run_prototype.ps1": "88924dd86ebdc9b51a51f354ec22f40beb75cf6daafbe869283fa187568b6f60",
    "tools/c11d/d9/test_c11e_e4b_r1p_family_grammar_static_audit.py": "600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92",
    "tools/c11d/d9/universal_producer.py": "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1",
    "tools/c11d/d9/editorial_render_bridge.py": "fe9d40052b0f4ff6f1c862c010ae7b3b13070b6ce935be6d62f9dcaec63a644a",
    "tools/c11d/d9/d_render_adapter.py": "222742677cd498368429a3ec0dcdd922c44197bb5ada3638081138fb77c31bf1",
    "tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py": "bfbfa0cc108f00b78003e5480c86af1ee5ca63772d24a7792f8cdb6953b6af5d",
    "profiles/presentation/c11c_visual_music_profiles.json": "b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58",
    "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json": "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a",
    "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json": "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc",
    "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json": "9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da",
    "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json": "41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85",
    "definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json": "3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23",
    "definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json": "5726310b48e9a85540d48b1e78784571ba04c3f900a5c09add35b49ce5575504",
    "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json": "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb",
}

FAMILY_INTERNALS = {
    "c11c_fractal_bloom_v1": ("fractal", "tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd"),
    "c11c_geometric_waves_v1": ("geometric", "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd"),
    "c11c_sacred_symmetry_v1": ("sacred_symmetry", "tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd"),
    "c11c_living_particles_v1": ("living_particles", "tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd"),
    "c11c_invisible_forces_v1": ("invisible_forces", "tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd"),
}


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): canonical(value[k]) for k in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [canonical(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    path.write_text(raw, encoding="utf-8", newline="\n")


def load_module(name: str, path: Path):
    key = "_c11e_r1p_" + name
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


def check_source_pins(root: Path) -> dict[str, dict[str, Any]]:
    observed: dict[str, dict[str, Any]] = {}
    mismatches: list[str] = []
    for relative, expected in EXPECTED_PINS.items():
        path = root / Path(*relative.split("/"))
        if not path.is_file():
            mismatches.append(f"MISSING:{relative}")
            continue
        data = path.read_bytes()
        digest = sha256_bytes(data)
        observed[relative] = {"bytes": len(data), "sha256": digest}
        if digest != expected:
            mismatches.append(f"SHA256:{relative}:expected={expected}:actual={digest}")
    if mismatches:
        raise RuntimeError("Source pin preflight failed: " + " | ".join(mismatches))
    return observed


def audit_prototype_runtime_contracts(root: Path, schema: dict[str, Any]) -> None:
    for family_id, (internal, prototype_rel) in FAMILY_INTERNALS.items():
        prototype = (root / prototype_rel).read_text(encoding="utf-8-sig")
        required = [
            f'VariationProfileClass.build("{internal}", _seed)',
            "_apply_grammar_override()",
            f'C11CVisualLoopDurationClass.resolve(int(_variation["loop_cycles"]), DEFAULT_LOOP_DURATION)',
            f'PaletteBankClass.palette("{internal}", int(_variation["palette_mode"]))',
            f'EditorialColorsClass.palette("{internal}", _palette)',
            f'TechnobabbleGeneratorClass.generate_geek_text("{internal}", _seed, _variation)',
            "const DEFAULT_LOOP_DURATION := 0.0",
            "const FPS := C11CVisualLoopDurationClass.FPS",
            'OS.get_environment("C11C_VISUAL_GRAMMAR")',
            '_variation["grammar_mode"] = index',
            '_variation["grammar_name"] = technical_id',
        ]
        missing = [token for token in required if token not in prototype]
        if missing:
            raise RuntimeError(f"Prototype runtime contract drift {family_id}: {missing}")
        ordered_calls = [
            f'VariationProfileClass.build("{internal}", _seed)',
            "_apply_grammar_override()",
            f'C11CVisualLoopDurationClass.resolve(int(_variation["loop_cycles"]), DEFAULT_LOOP_DURATION)',
            f'PaletteBankClass.palette("{internal}", int(_variation["palette_mode"]))',
            f'EditorialColorsClass.palette("{internal}", _palette)',
            f'TechnobabbleGeneratorClass.generate_geek_text("{internal}", _seed, _variation)',
        ]
        positions = [prototype.find(token) for token in ordered_calls]
        if any(pos < 0 for pos in positions) or positions != sorted(positions):
            raise RuntimeError(f"Prototype helper call order drift {family_id}: {positions}")
        family = schema.get("families", {}).get(family_id)
        if not isinstance(family, dict) or family.get("internal") != internal:
            raise RuntimeError(f"Producer schema internal-family mismatch: {family_id}")


def build_parent_bindings(root: Path, run_id: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    d9_dir = root / "tools" / "c11d" / "d9"
    if str(d9_dir) not in sys.path:
        sys.path.insert(0, str(d9_dir))
    import universal_producer
    import editorial_render_bridge
    import c11e_e4b_loop_family_stage_contract as family_contract

    schema_path = root / "c11c-suite" / "c11c-producer" / "producer_schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    audit = load_module("static_audit", d9_dir / "test_c11e_e4b_r1p_family_grammar_static_audit.py")
    audit_report = audit.run_audit(root)
    if audit_report.get("status") != "PASS_STATIC_SOURCE_MAPPING" or audit_report.get("explicit_selector_count") != 27 or audit_report.get("family_count") != 5:
        raise RuntimeError("Live R1P static source mapping audit did not pass 5 families / 27 selectors")
    audit_prototype_runtime_contracts(root, schema)

    parent_rows: list[dict[str, Any]] = []
    godot_cases: list[dict[str, Any]] = []
    serial = 0
    for family_id, family in schema.get("families", {}).items():
        if family_id not in FAMILY_INTERNALS:
            raise RuntimeError(f"Unexpected family in producer schema: {family_id}")
        internal = FAMILY_INTERNALS[family_id][0]
        grammar_rows = family.get("grammars", [])
        explicit = [row[0] for row in grammar_rows if isinstance(row, list) and row and row[0] != "auto"]
        if len(explicit) != (7 if family_id == "c11c_invisible_forces_v1" else 5):
            raise RuntimeError(f"Unexpected explicit grammar count for {family_id}: {len(explicit)}")
        for grammar_index, grammar_id in enumerate(explicit):
            serial += 1
            request_id = f"{run_id}_{serial:02d}"
            gameplay_seed = 100000 + serial
            music_seed = 500000 + serial
            raw = {
                "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
                "schema_version": "1.0",
                "request_id": request_id,
                "mode": "REVIEW",
                "selection": {
                    "content_type": "visual_loops",
                    "family_id": family_id,
                    "subtype_id": grammar_id,
                },
                "seed": gameplay_seed,
                "music_seed": music_seed,
                "delivery_profile_id": "REVIEW_720",
                "presentation_profile_id": "UNKNOWN",
                "variation_index": 0,
                "audio_enabled": True,
                "personalization_enabled": True,
                "editorial_profile": {},
                "production_override": {
                    "title": f"Loop title {serial:02d}",
                    "subtitle": "UNKNOWN",
                    "call_to_action": "Continue",
                    "language": "en",
                },
                "provenance": {"request_origin": "TEST"},
            }
            planned = universal_producer.evaluate_universal_request(raw, root)
            if planned.get("status") != "PLANNED":
                raise RuntimeError(f"D9.9 request did not plan: {request_id}")
            bridge = editorial_render_bridge.build_bridge_planning_record(planned, root)
            contract = family_contract.build_loop_family_stage_contract(planned, bridge, root)
            family_contract.validate_loop_family_stage_contract(contract)
            if contract["content_identity"].get("grammar_id") != grammar_id:
                raise RuntimeError(f"D9.10 family contract grammar mismatch: {request_id}")
            if contract["family_visual_stage"].get("music_seed_passed_to_visual_launcher") is not False:
                raise RuntimeError(f"music_seed leaked into visual launcher contract: {request_id}")
            if contract["governance"].get("launcher_invoked") is not False or contract["governance"].get("godot_invoked") is not False:
                raise RuntimeError(f"family stage contract crossed execution boundary: {request_id}")
            if gameplay_seed == music_seed:
                raise RuntimeError(f"Seed domains must differ: {request_id}")

            canonical_request = planned["canonical_request"]
            family_music_profile_id = contract["family_visual_stage"].get("frozen_c11c_music_profile_id")
            if not isinstance(family_music_profile_id, str) or not family_music_profile_id.strip():
                raise RuntimeError(f"Missing frozen C11-C family music-profile identity: {request_id}")
            identity = {
                "request_id": request_id,
                "request_hash": planned["request_hash"],
                "plan_hash": planned["plan_hash"],
                "editorial_hash": planned["editorial_hash"],
                "bridge_record_hash": bridge["record_hash"],
                "adapter_envelope_hash": contract["request_identity"]["d_only_adapter_envelope_hash"],
                "family_stage_contract_sha256": contract["contract_sha256"],
            }
            family_audit = next(row for row in audit_report["families"] if row["family_id"] == family_id)
            local_pins = {
                "prototype": {"path": family_audit["prototype_path"], **{
                    k: family_audit[k] for k in ("prototype_sha256",)
                }},
                "launcher": {"path": family_audit["launcher_path"], "sha256": family_audit["launcher_sha256"]},
            }
            godot_cases.append({
                "case_id": request_id,
                "family_id": family_id,
                "internal_family_id": internal,
                "grammar_id": grammar_id,
                "grammar_index": grammar_index,
                "gameplay_seed": canonical_request["seed"],
                "music_seed": canonical_request["music_seed"],
                "request_identity": identity,
                "source_pins": local_pins,
                "family_music_profile_id": family_music_profile_id,
            })
            parent_rows.append({
                "case_id": request_id,
                "raw_request": raw,
                "d9_9_result": planned,
                "d9_10_bridge_record": bridge,
                "d_only_family_stage_contract": contract,
                "request_identity": identity,
            })

    if serial != 27:
        raise RuntimeError(f"Expected 27 canonical D9.9/D9.10 family contracts, got {serial}")
    if len({row["request_identity"]["request_hash"] for row in godot_cases}) != 27:
        raise RuntimeError("Canonical request hashes are not unique")
    seed_pairs = {(row["gameplay_seed"], row["music_seed"]) for row in godot_cases}
    if len(seed_pairs) != 27 or any(a == b for a, b in seed_pairs):
        raise RuntimeError("27 independent gameplay/music seed pairs were not established")

    source_pins = check_source_pins(root)
    return (
        {"schema": INPUT_SCHEMA, "schema_version": "1.0", "run_id": run_id,
         "source_pins": source_pins, "static_audit": audit_report, "cases": godot_cases},
        {"schema": "C11E-E4B-R1P-PARENT-BINDINGS-V1", "run_id": run_id, "cases": parent_rows},
        {"schema": "C11E-E4B-R1P-SOURCE-MANIFEST-V1", "run_id": run_id,
         "source_pins": source_pins, "static_audit": audit_report},
    )


def prepare(args: argparse.Namespace) -> int:
    root = args.project_root.resolve()
    work = args.work_dir.resolve()
    if not root.is_dir():
        raise RuntimeError(f"Project root does not exist: {root}")
    work.mkdir(parents=True, exist_ok=False)
    input_data, parent_data, source_manifest = build_parent_bindings(root, args.run_id)
    write_json(work / "r1p_godot_input.json", input_data)
    write_json(work / "r1p_parent_bindings.json", parent_data)
    write_json(work / "r1p_source_manifest.json", source_manifest)
    report = {
        "schema": "C11E-E4B-R1P-PREPARE-REPORT-V1",
        "status": "PASS_D9_9_D9_10_PARENT_PREPARATION_27_OF_27",
        "run_id": args.run_id,
        "project_root": str(root),
        "case_count": len(input_data["cases"]),
        "family_count": input_data["static_audit"]["family_count"],
        "explicit_selector_count": input_data["static_audit"]["explicit_selector_count"],
        "seed_relation_count": len({(c["gameplay_seed"], c["music_seed"]) for c in input_data["cases"]}),
        "request_ids": [c["case_id"] for c in input_data["cases"]],
        "godot_input_sha256": sha256_file(work / "r1p_godot_input.json"),
        "parent_bindings_sha256": sha256_file(work / "r1p_parent_bindings.json"),
        "source_manifest_sha256": sha256_file(work / "r1p_source_manifest.json"),
        "governance": {
            "renderer_dispatch_invoked": False, "launcher_invoked": False,
            "prototype_node_instantiated": False, "media_created": False,
            "release_authority": "NONE", "D4.8": "BLOCKED",
        },
    }
    write_json(work / "r1p_prepare_report.json", report)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


def sha256_canonical_object(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def extract_godot_result(stdout_path: Path) -> dict[str, Any]:
    text = stdout_path.read_text(encoding="utf-8-sig", errors="replace")
    hits = [line[len(GODOT_PREFIX):] for line in text.splitlines() if line.startswith(GODOT_PREFIX)]
    if len(hits) != 1:
        raise RuntimeError(f"Godot stdout must contain exactly one {GODOT_PREFIX!r} line; found {len(hits)}")
    value = json.loads(hits[0])
    if not isinstance(value, dict):
        raise RuntimeError("Godot result is not a JSON object")
    return value


def finalize(args: argparse.Namespace) -> int:
    root = args.project_root.resolve()
    work = args.work_dir.resolve()
    output = args.output_dir.resolve()
    if output.exists():
        raise RuntimeError(f"Output directory already exists; overwrite is forbidden: {output}")
    input_path = work / "r1p_godot_input.json"
    parent_path = work / "r1p_parent_bindings.json"
    input_data = json.loads(input_path.read_text(encoding="utf-8"))
    parent_data = json.loads(parent_path.read_text(encoding="utf-8"))
    prepare_report = json.loads((work / "r1p_prepare_report.json").read_text(encoding="utf-8"))
    source_manifest_path = work / "r1p_source_manifest.json"
    if prepare_report.get("status") != "PASS_D9_9_D9_10_PARENT_PREPARATION_27_OF_27" or prepare_report.get("run_id") != input_data.get("run_id") or parent_data.get("run_id") != input_data.get("run_id"):
        raise RuntimeError("R1P preparation report/parent run identity is invalid")
    if sha256_file(source_manifest_path) != prepare_report.get("source_manifest_sha256"):
        raise RuntimeError("Prepared source manifest hash changed after D9.9/D9.10 preparation")
    if sha256_file(input_path) != prepare_report.get("godot_input_sha256"):
        raise RuntimeError("Prepared Godot input hash changed after D9.9/D9.10 preparation")
    if sha256_file(parent_path) != prepare_report.get("parent_bindings_sha256"):
        raise RuntimeError("Parent D9.9/D9.10 binding archive hash changed after preparation")
    current_pins = check_source_pins(root)
    if current_pins != input_data.get("source_pins"):
        raise RuntimeError("Active checkout source pins changed during R1P execution")
    d9_dir = root / "tools" / "c11d" / "d9"
    if str(d9_dir) not in sys.path:
        sys.path.insert(0, str(d9_dir))
    import editorial_render_bridge
    import c11e_e4b_loop_family_stage_contract as family_contract
    godot = extract_godot_result(args.godot_stdout)
    if args.godot_exit_code != 0:
        raise RuntimeError(f"Godot exited non-zero: {args.godot_exit_code}")
    if not re.match(r"^4\.7\.1(?:\.|$)", args.godot_version.strip()):
        raise RuntimeError(f"Godot version mismatch; expected 4.7.1, observed {args.godot_version!r}")
    if godot.get("schema") != "C11E-E4B-R1P-GODOT-RESULT-V1" or godot.get("status") != "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27":
        raise RuntimeError("Godot materializer did not return R1P PASS")
    if godot.get("run_id") != input_data.get("run_id"):
        raise RuntimeError("Godot result run_id differs from prepared parent bindings")
    if godot.get("case_count") != 27 or godot.get("family_count") != 5 or godot.get("grammar_count") != 27:
        raise RuntimeError("Godot result summary counts do not match 5 families / 27 selectors")
    top_governance = godot.get("governance", {})
    for forbidden_flag in ("renderer_instantiated", "prototype_nodes_instantiated", "shader_created", "frame_buffers_created", "pixels_created", "renderer_input_emitted", "renderer_dispatch_invoked", "launchers_invoked", "audio_or_d3_invoked", "ffmpeg_invoked", "media_created", "godot_checkout_files_written"):
        if top_governance.get(forbidden_flag) is not False:
            raise RuntimeError(f"Godot top-level governance flag is not false: {forbidden_flag}")
    actual_cases = godot.get("cases")
    expected_cases = input_data.get("cases")
    if not isinstance(actual_cases, list) or len(actual_cases) != 27 or not isinstance(expected_cases, list) or len(expected_cases) != 27:
        raise RuntimeError("R1P result/input must contain exactly 27 cases")
    if args.godot_stderr.exists():
        stderr_text = args.godot_stderr.read_text(encoding="utf-8-sig", errors="replace")
        fatal = re.findall(r"(?im)^.*(?:SCRIPT ERROR|Parse Error|ERROR:|Assertion failed).*$", stderr_text)
        if fatal:
            raise RuntimeError("Godot stderr contains fatal diagnostics: " + " | ".join(fatal[:8]))

    expected_by_id = {row["case_id"]: row for row in expected_cases}
    parent_by_id = {row["case_id"]: row for row in parent_data["cases"]}
    if len(expected_by_id) != 27 or len(parent_by_id) != 27:
        raise RuntimeError("Duplicate or missing case identities in preparation inputs")
    for case_id, parent in parent_by_id.items():
        planned = parent["d9_9_result"]
        bridge = parent["d9_10_bridge_record"]
        contract = parent["d_only_family_stage_contract"]
        if planned.get("status") != "PLANNED":
            raise RuntimeError(f"Stored D9.9 parent is not PLANNED: {case_id}")
        if planned.get("request_hash") != editorial_render_bridge.sha256(planned["canonical_request"]):
            raise RuntimeError(f"Stored D9.9 request hash mismatch: {case_id}")
        if planned.get("plan_hash") != editorial_render_bridge.sha256(planned["plan"]):
            raise RuntimeError(f"Stored D9.9 plan hash mismatch: {case_id}")
        expected_editorial_hash = editorial_render_bridge.sha256({"selection": planned["plan"].get("selection"), "editorial": planned["plan"].get("editorial")})
        if planned.get("editorial_hash") != expected_editorial_hash:
            raise RuntimeError(f"Stored D9.9 editorial hash mismatch: {case_id}")
        if bridge.get("record_hash") != editorial_render_bridge.sha256({k: v for k, v in bridge.items() if k != "record_hash"}):
            raise RuntimeError(f"Stored D9.10 bridge record hash mismatch: {case_id}")
        if not family_contract.validate_loop_family_stage_contract(contract):
            raise RuntimeError(f"Stored family-stage contract validation failed: {case_id}")
        canonical_request = planned["canonical_request"]
        selection = canonical_request.get("selection", {})
        if selection.get("family_id") != expected_by_id[case_id]["family_id"] or selection.get("subtype_id") != expected_by_id[case_id]["grammar_id"]:
            raise RuntimeError(f"Stored D9.9 canonical selection differs from R1P selector: {case_id}")
        if canonical_request.get("seed") != expected_by_id[case_id]["gameplay_seed"] or canonical_request.get("music_seed") != expected_by_id[case_id]["music_seed"]:
            raise RuntimeError(f"Stored D9.9 canonical seed domains differ from R1P input: {case_id}")
        actual_identity = {
            "request_id": canonical_request.get("request_id"),
            "request_hash": planned.get("request_hash"),
            "plan_hash": planned.get("plan_hash"),
            "editorial_hash": planned.get("editorial_hash"),
            "bridge_record_hash": bridge.get("record_hash"),
            "adapter_envelope_hash": contract.get("request_identity", {}).get("d_only_adapter_envelope_hash"),
            "family_stage_contract_sha256": contract.get("contract_sha256"),
        }
        if parent.get("request_identity") != actual_identity:
            raise RuntimeError(f"Stored parent request identity does not match recomputed D9.9/D9.10 hashes: {case_id}")
        if parent.get("request_identity") != expected_by_id[case_id].get("request_identity"):
            raise RuntimeError(f"Stored parent request identity differs from Godot input: {case_id}")
    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for observed in actual_cases:
        case_id = observed.get("case_id")
        if case_id not in expected_by_id or case_id in seen:
            raise RuntimeError(f"Unexpected or duplicate Godot case: {case_id!r}")
        seen.add(case_id)
        expected = expected_by_id[case_id]
        payload = observed.get("payload")
        canonical_text = observed.get("payload_canonical_json")
        payload_sha = observed.get("payload_sha256")
        repeat_sha = observed.get("repeat_payload_sha256")
        if not isinstance(payload, dict) or not isinstance(canonical_text, str):
            raise RuntimeError(f"Missing payload/canonical bytes: {case_id}")
        if sha256_bytes(canonical_text.encode("utf-8")) != payload_sha or payload_sha != repeat_sha:
            raise RuntimeError(f"Canonical/repeat payload hash mismatch: {case_id}")
        if json.loads(canonical_text) != payload:
            raise RuntimeError(f"Canonical JSON bytes disagree with payload object: {case_id}")
        if observed.get("deterministic_repeat_pass") is not True:
            raise RuntimeError(f"Independent deterministic replay failed: {case_id}")
        if payload.get("request_binding", {}).get("request_identity") != expected["request_identity"]:
            raise RuntimeError(f"D9.9/D9.10 request identity mismatch: {case_id}")
        if payload.get("selection") != {
            "content_type": "visual_loops", "family_id": expected["family_id"],
            "grammar_id": expected["grammar_id"], "grammar_index": expected["grammar_index"],
        }:
            raise RuntimeError(f"Family/grammar selector mismatch: {case_id}")
        seeds = payload.get("seed_domains", {})
        if seeds.get("gameplay_seed") != expected["gameplay_seed"] or seeds.get("music_seed") != expected["music_seed"]:
            raise RuntimeError(f"Seed domain identity mismatch: {case_id}")
        if seeds.get("visual_parameters_use") != "request.seed" or seeds.get("music_seed_consumed_by_visual_parameters") is not False:
            raise RuntimeError(f"Visual/music seed isolation mismatch: {case_id}")
        visual = payload.get("visual_parameters", {})
        variation = visual.get("variation_recipe", {})
        palette = visual.get("palette", {})
        timing = payload.get("timing", {})
        if variation.get("family") != expected["internal_family_id"] or variation.get("grammar_mode") != expected["grammar_index"] or variation.get("grammar_name") != expected["grammar_id"]:
            raise RuntimeError(f"C11C variation recipe grammar mismatch: {case_id}")
        if not palette or not isinstance(palette.get("name"), str):
            raise RuntimeError(f"C11C palette missing/invalid: {case_id}")
        fps = timing.get("fps")
        duration = timing.get("duration_seconds")
        frames = timing.get("frame_count")
        if fps != 30 or duration not in (20.0, 22.0, 23.0) or frames != int(duration * fps):
            raise RuntimeError(f"C11C duration/timebase policy mismatch: {case_id}")
        visual_canonical_text = payload.get("visual_parameters_canonical_json")
        if not isinstance(visual_canonical_text, str) or sha256_bytes(visual_canonical_text.encode("utf-8")) != payload.get("visual_parameters_sha256"):
            raise RuntimeError(f"Visual parameter block canonical-byte hash mismatch: {case_id}")
        if json.loads(visual_canonical_text) != visual:
            raise RuntimeError(f"Visual parameter canonical JSON disagrees with object: {case_id}")
        if variation.get("loop_cycles") != timing.get("loop_cycles"):
            raise RuntimeError(f"Variation/timing loop-cycle binding mismatch: {case_id}")
        if timing.get("source") != "C11CVisualLoopDuration.resolve(loop_cycles, DEFAULT_LOOP_DURATION=0.0)":
            raise RuntimeError(f"Duration policy source mismatch: {case_id}")
        colors = visual.get("editorial_text_colors", {})
        required_color_keys = {"header_math", "header_hook", "footer_geek", "footer_data", "footer_palette", "footer_signature", "rule"}
        if not isinstance(colors, dict) or set(colors) != required_color_keys or any(not re.fullmatch(r"[0-9A-F]{6}", str(v)) for v in colors.values()):
            raise RuntimeError(f"C11C editorial text-color contract missing/invalid: {case_id}")
        babble = visual.get("technobabble", {})
        if not isinstance(babble.get("generated_text"), str) or not babble["generated_text"].strip():
            raise RuntimeError(f"Technobabble generation missing: {case_id}")
        if babble.get("display_text") != babble["generated_text"].upper():
            raise RuntimeError(f"Technobabble display capitalization mismatch: {case_id}")
        if payload.get("request_binding", {}).get("request_id") != case_id:
            raise RuntimeError(f"Payload request_id binding mismatch: {case_id}")
        if payload.get("request_binding", {}).get("family_music_profile_id") != parent_by_id[case_id]["d_only_family_stage_contract"]["family_visual_stage"]["frozen_c11c_music_profile_id"]:
            raise RuntimeError(f"Family music profile binding mismatch: {case_id}")
        if seeds.get("automatic_seed_generation") is not False or seeds.get("runtime_seed_derivation") is not False:
            raise RuntimeError(f"Seed generation policy drift: {case_id}")
        materialization_governance = payload.get("governance", {})
        for forbidden_flag in ("renderer_instantiated", "prototype_node_instantiated", "frame_buffers_created", "frame_inventory_materialized", "pixels_created", "renderer_native_input_emitted", "renderer_dispatch_invoked", "launchers_invoked", "audio_or_d3_invoked", "ffmpeg_invoked", "media_created", "godot_checkout_files_written"):
            if materialization_governance.get(forbidden_flag) is not False:
                raise RuntimeError(f"R1P forbidden action flag is not false ({forbidden_flag}): {case_id}")
        if materialization_governance.get("parameter_payload_materialized_in_memory") is not True:
            raise RuntimeError(f"R1P parameter materialization flag missing: {case_id}")
        if observed.get("source_pins") != expected["source_pins"]:
            raise RuntimeError(f"Case-local prototype/launcher source pins mismatch: {case_id}")
        if observed.get("governance", {}).get("renderer_instantiated") is not False or observed.get("governance", {}).get("pixels_created") is not False or observed.get("governance", {}).get("media_created") is not False:
            raise RuntimeError(f"R1P execution boundary changed: {case_id}")
        validated.append(observed)

    if len(seen) != 27:
        raise RuntimeError(f"Missing cases: expected 27, got {len(seen)}")
    output.mkdir(parents=True, exist_ok=False)
    receipts_dir = output / "receipts"
    receipts_dir.mkdir()
    parent_archive = output / "parent_bindings.json"
    source_manifest = output / "source_manifest.json"
    shutil.copy2(work / "r1p_parent_bindings.json", parent_archive)
    shutil.copy2(work / "r1p_godot_input.json", output / "godot_input.json")
    shutil.copy2(work / "r1p_source_manifest.json", source_manifest)
    shutil.copy2(work / "r1p_prepare_report.json", output / "prepare_report.json")
    shutil.copy2(args.godot_stdout, output / "godot_stdout.log")
    shutil.copy2(args.godot_stderr, output / "godot_stderr.log")
    shutil.copy2(args.python_prepare_stdout, output / "python_prepare_stdout.log")
    shutil.copy2(args.python_prepare_stderr, output / "python_prepare_stderr.log")

    receipt_hashes: list[str] = []
    for index, observed in enumerate(validated, start=1):
        payload = observed["payload"]
        row = expected_by_id[observed["case_id"]]
        receipt = {
            "schema": "C11E-E4B-R1P-LOOP-FAMILY-PARAMETER-RECEIPT-V1",
            "status": "PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT",
            "run_id": input_data["run_id"],
            "receipt_index": index,
            "case_id": observed["case_id"],
            "request_identity": row["request_identity"],
            "selection": payload["selection"],
            "seed_domains": payload["seed_domains"],
            "family_music_profile_id": row["family_music_profile_id"],
            "payload_sha256": observed["payload_sha256"],
            "repeat_payload_sha256": observed["repeat_payload_sha256"],
            "visual_parameters_sha256": payload["visual_parameters_sha256"],
            "visual_parameters_canonical_json": payload["visual_parameters_canonical_json"],
            "visual_parameters": payload["visual_parameters"],
            "timing": payload["timing"],
            "source_pins": input_data["source_pins"],
            "case_source_pins": row["source_pins"],
            "materialization": {
                "parameter_payload_materialized_in_memory": True,
                "deterministic_repeat_pass": True,
                "frame_buffers_materialized": False,
                "frame_inventory_materialized": False,
                "pixel_payload_materialized": False,
                "renderer_native_input_emitted": False,
                "renderer_instantiated": False,
                "prototype_node_instantiated": False,
                "launcher_invoked": False,
                "audio_or_d3_invoked": False,
                "ffmpeg_invoked": False,
                "media_created": False,
            },
            "governance": {
                "renderer": "OFF",
                "D4.8": "BLOCKED",
                "D9.10": "PREPARE_ONLY",
                "D9.17": "BLOCKED_NO_GO",
                "D10": "BLOCKED_FOR_PROMOTION",
                "release_authority": "NONE",
            },
        }
        receipt["receipt_sha256"] = sha256_canonical_object(receipt)
        name = f"{index:02d}_{observed['case_id']}.json"
        path = receipts_dir / name
        write_json(path, receipt)
        sidecar = receipts_dir / (name + ".sha256")
        sidecar.write_text(receipt["receipt_sha256"] + "  " + name + "\n", encoding="ascii")
        receipt_hashes.append(receipt["receipt_sha256"])

    all_receipt_digest = sha256_canonical_object(receipt_hashes)
    process_evidence = {
        "python_prepare_exit_code": args.python_prepare_exit_code,
        "python_prepare_stdout_sha256": sha256_file(args.python_prepare_stdout),
        "python_prepare_stderr_sha256": sha256_file(args.python_prepare_stderr),
        "godot_version": args.godot_version,
        "godot_exit_code": args.godot_exit_code,
        "godot_stdout_sha256": sha256_file(args.godot_stdout),
        "godot_stderr_sha256": sha256_file(args.godot_stderr),
    }
    report = {
        "schema": SCHEMA,
        "status": "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27",
        "scope": "REQUEST_SCOPED_C11C_FAMILY_PARAMETER_PAYLOADS_ONLY",
        "run_id": input_data["run_id"],
        "case_count": 27,
        "family_count": 5,
        "grammar_count": 27,
        "receipt_count": len(receipt_hashes),
        "receipt_hash_set_sha256": all_receipt_digest,
        "families": input_data["static_audit"]["families"],
        "source_pins": input_data["source_pins"],
        "parent_bindings_sha256": sha256_file(parent_archive),
        "source_manifest_sha256": sha256_file(source_manifest),
        "process_evidence": process_evidence,
        "scope_limits": {
            "parameter_payload_materialized_in_memory": True,
            "actual_c11c_frame_buffers_created": False,
            "evidence_artifacts_written": True,
            "active_checkout_source_files_written": False,
            "frame_inventory_materialized": False,
            "pixels_created": False,
            "renderer_native_input_emitted": False,
            "prototype_nodes_instantiated": False,
            "family_launchers_invoked": False,
            "audio_or_d3_invoked": False,
            "ffmpeg_invoked": False,
            "media_created": False,
        },
        "governance": {
            "renderer": "OFF", "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY",
            "D9.14": "BLOCKED", "D9.16": "BLOCKED", "D9.17": "BLOCKED_NO_GO",
            "D10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE",
        },
    }
    report["report_sha256"] = sha256_canonical_object(report)
    report_path = output / "r1p_report.json"
    write_json(report_path, report)
    report_sidecar = output / "r1p_report.sha256"
    report_sidecar.write_text(report["report_sha256"] + "  r1p_report.json\n", encoding="ascii")

    # Re-open every evidence record and verify the persisted bytes/sidecars.
    persisted_hashes: list[str] = []
    persisted_receipts = sorted(receipts_dir.glob("*.json"))
    persisted_sidecars = sorted(receipts_dir.glob("*.json.sha256"))
    if len(persisted_receipts) != 27 or len(persisted_sidecars) != 27:
        raise RuntimeError("Persisted receipt/sidecar counts do not equal 27/27")
    for receipt_path in persisted_receipts:
        stored = json.loads(receipt_path.read_text(encoding="utf-8"))
        stored_hash = stored.pop("receipt_sha256", None)
        actual_hash = sha256_canonical_object(stored)
        sidecar_path = receipts_dir / (receipt_path.name + ".sha256")
        sidecar_hash = sidecar_path.read_text(encoding="ascii").split()[0]
        if stored_hash != actual_hash or sidecar_hash != actual_hash:
            raise RuntimeError(f"Persisted receipt/sidecar hash verification failed: {receipt_path.name}")
        persisted_hashes.append(actual_hash)
    if sha256_canonical_object(persisted_hashes) != all_receipt_digest:
        raise RuntimeError("Persisted receipt hash set differs from aggregate report")
    stored_report = json.loads(report_path.read_text(encoding="utf-8"))
    stored_report_hash = stored_report.pop("report_sha256", None)
    if stored_report_hash != sha256_canonical_object(stored_report) or report_sidecar.read_text(encoding="ascii").split()[0] != stored_report_hash:
        raise RuntimeError("Persisted aggregate report/sidecar hash verification failed")

    print(json.dumps({"status": report["status"], "run_id": report["run_id"], "receipt_count": report["receipt_count"], "receipt_hash_verification": "PASS_27_OF_27", "report_sha256": report["report_sha256"], "output_dir": str(output)}, ensure_ascii=False, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_prepare = sub.add_parser("prepare")
    p_prepare.add_argument("--project-root", type=Path, required=True)
    p_prepare.add_argument("--work-dir", type=Path, required=True)
    p_prepare.add_argument("--run-id", required=True)
    p_prepare.set_defaults(func=prepare)
    p_final = sub.add_parser("finalize")
    p_final.add_argument("--project-root", type=Path, required=True)
    p_final.add_argument("--work-dir", type=Path, required=True)
    p_final.add_argument("--output-dir", type=Path, required=True)
    p_final.add_argument("--godot-stdout", type=Path, required=True)
    p_final.add_argument("--godot-stderr", type=Path, required=True)
    p_final.add_argument("--python-prepare-stdout", type=Path, required=True)
    p_final.add_argument("--python-prepare-stderr", type=Path, required=True)
    p_final.add_argument("--python-prepare-exit-code", type=int, required=True)
    p_final.add_argument("--godot-exit-code", type=int, required=True)
    p_final.add_argument("--godot-version", required=True)
    p_final.set_defaults(func=finalize)
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(json.dumps({"status": "FAIL_R1P", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
