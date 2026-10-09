from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from editorial_render_bridge import (
    CONTRACT_REL,
    CONTRACT_SCHEMA,
    EditorialRenderBridgeError,
    RECORD_SCHEMA,
    build_bridge_planning_record,
    load_contract,
    sha256,
)
from d_render_adapter import (
    ADAPTER_SCHEMA,
    DRenderAdapterError,
    prepare_d_only_adapter_envelope,
    validate_d_only_adapter_envelope,
)


def _raw(selection: dict, request_id: str) -> dict:
    return {
        "schema": REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": selection,
        "seed": 12345,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {
            "title": "Bridge planning · título",
            "subtitle": "Subtítulo",
            "call_to_action": "Continuar",
            "language": "ES",
            **({"player_name": "ANA", "challenge_label": "RETO"} if selection.get("content_type") == "challenges" else {}),
        },
        "provenance": {"source_revision": "C11D-D9.9-PRODUCER-0.11.0", "request_origin": "TEST"},
    }


def _representative_selections() -> dict[str, dict]:
    schema = json.loads((ROOT / "c11c-suite/c11c-producer/producer_schema.json").read_text(encoding="utf-8"))
    challenges = sorted((ROOT / "challenges").glob("CHALLENGE_[0-9][0-9][0-9].json"))
    challenge_doc = json.loads(challenges[0].read_text(encoding="utf-8"))
    challenge_id = str(challenge_doc["challenge_id"])
    challenge_family = str(challenge_doc.get("mechanic", "key"))
    loop_family_id, loop_family = next(iter(schema["families"].items()))
    loop_grammar = next((row[0] for row in loop_family.get("grammars", []) if row[0] != "auto"), None)
    drill_type, drill = next(iter(schema["drills"].items()))
    tier = drill.get("difficulty_values", [1, 2, 3, 4, 5])[0]
    return {
        "challenges": {"content_type": "challenges", "family_id": challenge_family, "variant_id": challenge_id},
        "visual_loops": {"content_type": "visual_loops", "family_id": loop_family_id, "subtype_id": loop_grammar},
        "visual_drills": {"content_type": "visual_drills", "family_id": drill_type, "variant_id": f"tier-{tier}"},
    }


def run_checks() -> dict[str, int]:
    contract = load_contract(ROOT)
    assert contract["schema"] == CONTRACT_SCHEMA
    assert contract["output"]["schema"] == RECORD_SCHEMA
    assert contract["output"]["renderer_input_emitted"] is False
    assert contract["output"]["media_output_created"] is False
    adapter_envelopes = {}
    adapter_contract = json.loads((ROOT / "definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json").read_text(encoding="utf-8"))
    adapter_source = (HERE / "d_render_adapter.py").read_text(encoding="utf-8")
    for forbidden_import in ("import subprocess", "from subprocess", "import ffmpeg", "import godot"):
        assert forbidden_import not in adapter_source.lower(), f"D-only prepare adapter must not execute media tooling: {forbidden_import}"
    assert "C11C_FREEZE_PACKAGE_MANIFEST" not in adapter_source
    assert adapter_contract["policy"]["adapter_prepare_enabled"] is True
    assert adapter_contract["policy"]["renderer_dispatch_enabled"] is False
    assert adapter_contract["policy"]["renderer_activation"] is False
    assert contract["governance"]["d4_8"] == "BLOCKED"
    model = json.loads((ROOT / "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json").read_text(encoding="utf-8"))
    assert contract["governance"]["release_authority"] == "NONE"
    assert json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8"))["schema_version"] == "1.0"

    valid_results = {}
    records = {}
    cli_cases = 0
    with tempfile.TemporaryDirectory(prefix="c11d_d910_bridge_") as temp_dir:
        temp = Path(temp_dir)
        for content_type, selection in _representative_selections().items():
            request = _raw(selection, f"D910-{content_type.upper()}")
            result = evaluate_universal_request(request, ROOT)
            record = build_bridge_planning_record(result, ROOT)
            envelope = prepare_d_only_adapter_envelope(result, record, ROOT)
            assert validate_d_only_adapter_envelope(envelope, ROOT) is True
            assert envelope["schema"] == ADAPTER_SCHEMA
            assert envelope["status"] == "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED"
            assert envelope["source_identity"]["request_hash"] == result["request_hash"]
            assert envelope["source_identity"]["editorial_hash"] == result["editorial_hash"]
            assert envelope["source_identity"]["plan_hash"] == result["plan_hash"]
            assert envelope["source_identity"]["bridge_record_hash"] == record["record_hash"]
            assert envelope["binding_preview"]["editorial_bindings"] == result["plan"]["editorial"]
            assert envelope["binding_preview"]["seed_contract"]["gameplay_seed"] == request["seed"]
            assert envelope["binding_preview"]["seed_contract"]["music_seed"] == request["music_seed"]
            assert envelope["d_only_adapter_prepare_invoked"] is True
            assert envelope["renderer_dispatch_invoked"] is False
            assert envelope["renderer_input_emitted"] is False
            assert envelope["production_execution"] is False and envelope["media_output_created"] is False
            assert envelope["output_artifact_path"] is None
            assert envelope["d4_8"] == "BLOCKED" and envelope["release_authority"] == "NONE"
            assert envelope["envelope_hash"] == sha256({key: value for key, value in envelope.items() if key != "envelope_hash"})
            assert prepare_d_only_adapter_envelope(result, record, ROOT) == envelope
            assert record["content_type"] == content_type
            assert record["schema"] == RECORD_SCHEMA
            assert record["contract_schema"] == contract["schema"]
            assert record["contract_identity"] == {"schema": contract["schema"], "schema_version": contract["schema_version"], "sha256": sha256(contract)}
            assert record["editorial_model_identity"] == {"schema": model["schema"], "schema_version": model["schema_version"], "checkpoint": model["checkpoint"], "sha256": sha256(model)}
            assert record["status"] == "PLANNING_ONLY_NOT_RENDERABLE"
            assert record["renderer_input_emitted"] is False
            assert record["renderer_adapter_invoked"] is False
            assert record["renderer_activation"] is False
            assert record["production_execution"] is False
            assert record["media_output_created"] is False
            assert record["output_artifact_path"] is None
            assert record["release_authority"] == "NONE" and record["d4_8"] == "BLOCKED"
            assert record["record_hash"] == sha256({key: value for key, value in record.items() if key != "record_hash"})
            assert build_bridge_planning_record(result, ROOT) == record, "Bridge record must be deterministic"
            assert record["seed_contract"]["gameplay_seed"] == request["seed"]
            assert record["seed_contract"]["music_seed"] == request["music_seed"]
            assert record["seed_contract"]["cross_domain_seed_sharing"] == "FORBIDDEN"
            assert record["editorial"]["values_hash"] == result["editorial_hash"] or record["editorial"]["values_hash"] == sha256(result["plan"]["editorial"])
            valid_results[content_type] = result
            records[content_type] = record
            adapter_envelopes[content_type] = envelope

            # Confirm CLI process emits exactly the same bridge plan and D-only adapter envelope.
            request_path = temp / f"{content_type}.json"
            request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
            cli = subprocess.run(
                [sys.executable, str(HERE / "universal_producer_cli.py"), "--request", str(request_path), "--print-json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )
            assert cli.returncode == 0, cli.stdout + "\n" + cli.stderr
            cli_result = json.loads(cli.stdout)
            assert cli_result["bridge_planning_record"] == record, content_type
            assert cli_result["d_only_adapter_envelope"] == envelope, content_type
            cli_cases += 1

    assert records["challenges"]["route"]["route_id"] == "REUSE_CANONICAL_D4_CHALLENGE_SUBPLAN"
    assert records["visual_loops"]["route"]["route_id"] == "FUTURE_D_NATIVE_VISUAL_LOOP_ADAPTER_REQUIRED"
    assert records["visual_drills"]["route"]["route_id"] == "FUTURE_D_NATIVE_VISUAL_DRILL_ADAPTER_REQUIRED"

    # Editorial-only changes alter the bridge identity while preserving both seed domains.
    base_request = _raw(_representative_selections()["visual_loops"], "D910-EDITORIAL-IDENTITY")
    base_result = evaluate_universal_request(base_request, ROOT)
    changed_request = copy.deepcopy(base_request)
    changed_request["production_override"]["title"] = "Editorial changed"
    changed_result = evaluate_universal_request(changed_request, ROOT)
    base_record = build_bridge_planning_record(base_result, ROOT)
    changed_record = build_bridge_planning_record(changed_result, ROOT)
    base_envelope = prepare_d_only_adapter_envelope(base_result, base_record, ROOT)
    changed_envelope = prepare_d_only_adapter_envelope(changed_result, changed_record, ROOT)
    assert base_record["record_hash"] != changed_record["record_hash"]
    assert base_envelope["envelope_hash"] != changed_envelope["envelope_hash"]
    assert base_envelope["binding_preview"]["editorial_bindings"] != changed_envelope["binding_preview"]["editorial_bindings"]
    assert base_record["seed_contract"]["gameplay_seed"] == changed_record["seed_contract"]["gameplay_seed"]
    assert base_record["seed_contract"]["music_seed"] == changed_record["seed_contract"]["music_seed"]
    assert base_envelope["binding_preview"]["seed_contract"]["gameplay_seed"] == changed_envelope["binding_preview"]["seed_contract"]["gameplay_seed"]
    assert base_envelope["binding_preview"]["seed_contract"]["music_seed"] == changed_envelope["binding_preview"]["seed_contract"]["music_seed"]

    # Negative bridge-contract controls fail closed; no forged plan can gain renderer authority.
    negative_cases = []

    def rejects(name: str, mutate, *, rehash_plan: bool = False) -> None:
        sample = copy.deepcopy(valid_results["visual_loops"])
        mutate(sample)
        if rehash_plan:
            sample["plan_hash"] = sha256(sample["plan"])
            sample["editorial_hash"] = sha256({"selection": sample["plan"].get("selection"), "editorial": sample["plan"].get("editorial")})
        try:
            build_bridge_planning_record(sample, ROOT)
        except (EditorialRenderBridgeError, ValueError, TypeError, KeyError):
            negative_cases.append(name)
        else:
            raise AssertionError(f"Expected D9.10 bridge rejection: {name}")

    rejects("wrong_status", lambda r: r.update(status="FAILED"))
    rejects("request_hash_mismatch", lambda r: r.update(request_hash="0" * 64))
    rejects("plan_hash_mismatch", lambda r: r.update(plan_hash="0" * 64))
    rejects("editorial_hash_mismatch", lambda r: r.update(editorial_hash="0" * 64))
    rejects("renderer_result_enabled", lambda r: r.update(renderer=True))
    rejects("execution_result_enabled", lambda r: r.update(execution=True))
    rejects("plan_renderer_enabled", lambda r: r["plan"].update(renderer_activation=True), rehash_plan=True)
    rejects("plan_execution_enabled", lambda r: r["plan"].update(production_execution=True), rehash_plan=True)
    rejects("release_authority_escalated", lambda r: r.update(release_authority="AUTHORIZED"))
    rejects("d4_8_unblocked", lambda r: r["plan"].update(d4_8="AUTHORIZED"), rehash_plan=True)
    rejects("telemetry_as_editorial", lambda r: r["plan"]["editorial"].update(frame_count=300), rehash_plan=True)
    rejects("boolean_gameplay_seed", lambda r: r["plan"].update(seed=True), rehash_plan=True)
    rejects("gameplay_seed_crosswired", lambda r: r["plan"].update(seed=r["plan"]["music_seed"] + 1), rehash_plan=True)
    rejects("automatic_seed_generation", lambda r: r["plan"].update(automatic_seed_generation=True), rehash_plan=True)
    rejects("wrong_plan_schema", lambda r: r["plan"].update(schema="RENDERER-READY"), rehash_plan=True)
    assert len(negative_cases) == 15, negative_cases

    adapter_negative_cases = []
    def adapter_rejects(name: str, mutate, *, rehash: bool = False) -> None:
        sample = copy.deepcopy(adapter_envelopes["visual_loops"])
        mutate(sample)
        if rehash:
            sample["envelope_hash"] = sha256({key: value for key, value in sample.items() if key != "envelope_hash"})
        try:
            validate_d_only_adapter_envelope(sample, ROOT)
        except (DRenderAdapterError, ValueError, TypeError, KeyError):
            adapter_negative_cases.append(name)
        else:
            raise AssertionError(f"Expected D-only adapter rejection: {name}")

    adapter_rejects("envelope_hash_mismatch", lambda e: e.update(envelope_hash="0" * 64))
    adapter_rejects("renderer_dispatch_enabled", lambda e: e.update(renderer_dispatch_invoked=True))
    adapter_rejects("renderer_input_emitted", lambda e: e.update(renderer_input_emitted=True))
    adapter_rejects("production_execution_enabled", lambda e: e.update(production_execution=True))
    adapter_rejects("media_output_claimed", lambda e: e.update(media_output_created=True))
    adapter_rejects("release_authority_escalated", lambda e: e.update(release_authority="AUTHORIZED"))
    adapter_rejects("c11c_mutation_claimed", lambda e: e.update(c11c_source_mutation=True))
    adapter_rejects("editorial_allowlist_bypass", lambda e: e["binding_preview"]["editorial_bindings"].update(simulation_truth="forged"), rehash=True)
    adapter_rejects("gameplay_music_seed_crosswire", lambda e: e["binding_preview"]["seed_contract"].update(music_seed=e["binding_preview"]["seed_contract"]["gameplay_seed"]), rehash=True)
    assert len(adapter_negative_cases) == 9, adapter_negative_cases

    return {"content_types": len(records), "cli_cases": cli_cases, "negative_cases": len(negative_cases), "adapter_negative_cases": len(adapter_negative_cases), "routes": 3}


if __name__ == "__main__":
    counts = run_checks()
    print(
        "C11-D D9.10 EDITORIAL-RENDER BRIDGE PLANNING PASS | "
        f"content_types={counts['content_types']}/3 | CLI bridge parity={counts['cli_cases']}/3 | adapter parity={counts['cli_cases']}/3 | "
        f"negative={counts['negative_cases']}/15 | adapter_negative={counts['adapter_negative_cases']}/9 | "
        "adapter=PREPARE_ONLY | renderer_input=NOT_EMITTED | renderer=OFF | production=false | "
        "D4.8=BLOCKED | release_authority=NONE"
    )
