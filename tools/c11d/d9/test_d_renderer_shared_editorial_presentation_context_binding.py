from __future__ import annotations
import copy, json, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from universal_editorial_model import build_catalog
from d_renderer_shared_editorial_presentation_context_binding import (
    SharedContextBindingError, build_context_binding, build_context_binding_from_result,
    validate_binding_record, validate_contract, audit,
)

def raw_request(selection: dict, request_id: str) -> dict:
    return {
        "schema": REQUEST_SCHEMA_ID, "schema_version":"1.0", "request_id":request_id, "mode":"REVIEW",
        "selection":selection, "seed":12345, "music_seed":840001, "delivery_profile_id":"REVIEW_720",
        "presentation_profile_id":"social_default_v1", "variation_index":0, "audio_enabled":True,
        "personalization_enabled":True, "editorial_profile":{},
        "production_override":{"title":"  TÍTULO EDITORIAL  ","subtitle":"Subtítulo compartido","call_to_action":"Continuar","language":" ES ",
          **({"player_name":"ANA","challenge_label":"RETO"} if selection.get("content_type")=="challenges" else {})},
        "provenance":{"source_revision":"D9_CONTEXT_BINDING_TEST","request_origin":"TEST"},
    }

def representatives() -> list[dict]:
    catalog=build_catalog(ROOT)
    ch=catalog["content_types"]["challenges"]["families"][0]
    loop_family=next(f for f in catalog["content_types"]["visual_loops"]["families"] if f["id"]=="c11c_geometric_waves_v1")
    drill_family=catalog["content_types"]["visual_drills"]["families"][0]
    ch_variant=ch["variants"][0]["id"]
    loop_subtype=next(s["id"] for s in loop_family["subtypes"] if s["id"]!="auto")
    drill_variant=drill_family["variants"][0]["id"]
    return [
      raw_request({"content_type":"challenges","family_id":ch["id"],"variant_id":ch_variant},"CTX-CHALLENGE-001"),
      raw_request({"content_type":"visual_loops","family_id":loop_family["id"],"subtype_id":loop_subtype},"CTX-LOOP-001"),
      raw_request({"content_type":"visual_drills","family_id":drill_family["id"],"variant_id":drill_variant},"CTX-DRILL-001"),
    ]

def run_checks() -> dict:
    state=validate_contract(ROOT)
    assert state["lineage_count"] >= 14
    counts=audit(ROOT)
    assert counts["registered_profiles"]==1 and counts["supported_content_types"]==3 and counts["shared_fields"]==4 and counts["reserved_fields"]==12
    cases=representatives()
    records=[]
    for req in cases:
        result=evaluate_universal_request(req,ROOT)
        record=build_context_binding_from_result(result,ROOT)
        assert validate_binding_record(record,result,ROOT)
        assert record["identity"]["request_sha256"]==result["request_hash"]
        assert record["identity"]["plan_sha256"]==result["plan_hash"]
        assert record["identity"]["editorial_sha256"]==result["editorial_hash"]
        assert record["presentation_binding"]["profile_id"]==req["presentation_profile_id"]=="social_default_v1"
        assert record["editorial_binding"]["shared_display_text_fields"]["title"]=="TÍTULO EDITORIAL"
        assert record["editorial_binding"]["shared_metadata_fields"]["language"]=="es"
        assert record["execution_boundary"]["renderer_native_input_emitted"] is False
        assert record["execution_boundary"]["report_persisted"] is False
        records.append(record)
    assert [r["identity"]["content_type"] for r in records]==["challenges","visual_loops","visual_drills"]
    assert len({r["presentation_binding"]["registry_entry_sha256"] for r in records})==1
    # Common fields are same semantics across content types; Challenge-only fields never leak.
    assert set(records[0]["editorial_binding"]["resolved_values"])=={"title","subtitle","call_to_action","language","player_name","challenge_label"}
    assert all(set(r["editorial_binding"]["resolved_values"])=={"title","subtitle","call_to_action","language"} for r in records[1:])
    # Each separate-process CLI result equals the in-process canonical binding for the same request.
    with tempfile.TemporaryDirectory(prefix="c11d_shared_context_binding_") as temp:
        temp=Path(temp)
        for idx,(req,record) in enumerate(zip(cases,records)):
            path=temp/f"request-{idx}.json"
            path.write_text(json.dumps(req,ensure_ascii=False),encoding="utf-8")
            proc=subprocess.run(
                [sys.executable,str(HERE/"d_renderer_shared_editorial_presentation_context_binding.py"),"--project-root",str(ROOT),"--request",str(path)],
                cwd=ROOT, capture_output=True, text=False, timeout=60,
            )
            stdout_bytes = proc.stdout or b""
            stderr_text = (proc.stderr or b"").decode("utf-8", errors="replace")
            stdout_preview = stdout_bytes.decode("ascii", errors="replace")
            assert proc.returncode == 0, (
                f"Separate-process CLI exited {proc.returncode}; stderr={stderr_text!r}; "
                f"stdout={stdout_preview[:500]!r}"
            )
            try:
                cli_text = stdout_bytes.decode("ascii")
            except UnicodeDecodeError as exc:
                raise AssertionError(
                    "Separate-process CLI JSON must be ASCII-safe across Windows code pages; "
                    f"invalid byte at offset {exc.start}"
                ) from exc
            try:
                cli = json.loads(cli_text)
            except json.JSONDecodeError as exc:
                raise AssertionError(
                    f"Separate-process CLI returned invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
                ) from exc
            assert cli == record
    # Editable text changes bind to the same selection/profile but make the context identity different; seeds stay fixed.
    base=cases[1]; a=build_context_binding(base,ROOT)
    changed=copy.deepcopy(base); changed["production_override"]["title"]="OTRO TÍTULO"
    b=build_context_binding(changed,ROOT)
    assert a["identity"]["editorial_sha256"]!=b["identity"]["editorial_sha256"]
    assert a["binding_context_sha256"]!=b["binding_context_sha256"]
    assert a["domain_binding"]==b["domain_binding"]
    assert a["presentation_binding"]==b["presentation_binding"]
    assert a["editorial_binding"]["shared_metadata_fields"]==b["editorial_binding"]["shared_metadata_fields"]
    # Same presentation reference is bound to all types; it is not geometry.
    assert all(r["presentation_binding"]["geometry_resolution"]=="NOT_PERFORMED" for r in records)
    assert all(r["presentation_binding"]["presentation_policy_approved"] is False for r in records)
    # Any profile outside the explicit registry rejects, even if D9.9 alone accepts the non-empty string.
    unknown=copy.deepcopy(cases[1]); unknown["presentation_profile_id"]="future_unregistered_profile"
    try: build_context_binding(unknown,ROOT)
    except SharedContextBindingError as exc: assert "Unregistered presentation_profile_id" in str(exc)
    else: raise AssertionError("Unregistered profile must fail closed")
    unknown_default=copy.deepcopy(cases[1]); unknown_default["presentation_profile_id"]="UNKNOWN"
    try: build_context_binding(unknown_default,ROOT)
    except SharedContextBindingError: pass
    else: raise AssertionError("UNKNOWN presentation profile must reject")
    # Tampering cannot be repaired by changing only record hashes; validation reconstructs from canonical result.
    result=evaluate_universal_request(cases[1],ROOT); record=build_context_binding_from_result(result,ROOT)
    tampered=copy.deepcopy(record); tampered["editorial_binding"]["resolved_values"]["title"]="FAKE"
    try: validate_binding_record(tampered,result,ROOT)
    except SharedContextBindingError: pass
    else: raise AssertionError("Tampered context record must reject")
    tampered=copy.deepcopy(record); tampered["presentation_binding"]["profile_id"]="fake"
    try: validate_binding_record(tampered,result,ROOT)
    except SharedContextBindingError: pass
    else: raise AssertionError("Tampered presentation identity must reject")
    # Strict source-drift negative is isolated in a temporary mirror, never mutating the active checkout.
    with tempfile.TemporaryDirectory(prefix="c11d_context_binding_drift_") as temp_root_name:
        temp_root=Path(temp_root_name)
        required={
            "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_CONTRACT_V1.json",
            "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_CONTRACT_SCHEMA_V1.json",
            "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_SCHEMA_V1.json",
            "definitions/c11d/production/D_RENDERER_SHARED_PRESENTATION_PROFILE_REFERENCE_REGISTRY_V1.json",
            "definitions/c11d/production/D_RENDERER_SHARED_PRESENTATION_PROFILE_REFERENCE_REGISTRY_SCHEMA_V1.json",
            "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
            "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_V1.json",
            "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_SCHEMA_V1.json",
            "definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json",
        }
        contract_doc=json.loads((ROOT/"definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_CONTRACT_V1.json").read_text(encoding="utf-8"))
        required.update(row["path"] for row in contract_doc["source_lineage"])
        for relative in required:
            src=ROOT/relative; dst=temp_root/relative
            dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        pin=temp_root/"core/presentation/PresentationProfile.gd"
        original=pin.read_bytes()
        pin.write_bytes(original+b"\n# TEMPORARY TEST MUTATION\n")
        try: validate_contract(temp_root)
        except SharedContextBindingError as exc: assert "Pinned source drift" in str(exc) or "Profile registry source drift" in str(exc)
        else: raise AssertionError("Pinned profile identity source drift must reject")
        pin.write_bytes(original)
        assert pin.read_bytes()==original
    # Reproducibility / record self-hashes.
    again=build_context_binding(cases[1],ROOT)
    assert again==a
    assert len({r["binding_context_sha256"] for r in records})==3
    return {"source_pins":counts["source_pins"],"profiles":counts["registered_profiles"],"content_types":len(records),"common_fields":counts["shared_fields"],"cli_parity":len(records),"negative":4,"text_mutation":1}

if __name__=="__main__":
    c=run_checks()
    print("C11-D SHARED EDITORIAL/PRESENTATION CONTEXT BINDING CONTRACT PASS | "
          f"source_pins={c['source_pins']}/{c['source_pins']} | profiles={c['profiles']}/{c['profiles']} | "
          f"content_types={c['content_types']}/3 | shared_fields={c['common_fields']}/4 | "
          f"separate_process_parity={c['cli_parity']}/3 | fail_closed_negatives={c['negative']}/4 | "
          f"editorial_mutation_seed_isolation={c['text_mutation']}/1 | renderer_input=NOT_EMITTED | "
          "renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
