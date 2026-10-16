"""Read-only audit of the existing D9.9 -> request-scoped source-binding seam.

It calls the canonical producer, D9.10 bridge/adapter and existing source binder;
it does not implement a second binder, invoke Godot, persist requests/payloads, or render.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any, Mapping
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # contract dependency
    raise RuntimeError("jsonschema is required for D9.12 audit contract validation") from exc

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from editorial_render_bridge import build_bridge_planning_record
from d_render_adapter import prepare_d_only_adapter_envelope
from d_renderer_request_scoped_payload_binding import (
    build_request_scoped_payload_binding,
    validate_request_scoped_payload_binding,
)

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_REQUEST_CHAIN_GAP_AUDIT_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_REQUEST_CHAIN_GAP_AUDIT_SCHEMA_V1.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_REQUEST_CHAIN_GAP_AUDIT_REPORT_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
REPORT_PREFIX = "C11-D VISUAL LOOP GEOMETRIC REQUEST CHAIN GAP AUDIT="
BLOCKED_STATUS = "BLOCKED_BY_FIXED_V1_TIMING_REVIEW_SCOPE"
BOUND_STATUS = "SOURCE_BINDING_REVIEW_ONLY"

class RequestChainGapAuditError(RuntimeError):
    """Raised on source drift, canonical plan drift, or a gap outside the pinned expected boundary."""

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()
def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
def _sha_file(path: Path) -> str:
    try: return _sha_bytes(path.read_bytes())
    except OSError as exc: raise RequestChainGapAuditError(f"Cannot read pinned source {path}: {exc}") from exc
def _read_json(path: Path) -> Any:
    try: return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise RequestChainGapAuditError(f"Cannot read JSON {path}: {exc}") from exc
def _require(condition: bool, message: str) -> None:
    if not condition: raise RequestChainGapAuditError(message)
def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / CONTRACT_SCHEMA_REL)
    report_schema = _read_json(root / REPORT_SCHEMA_REL)
    _require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "Contract schema must use Draft 2020-12")
    _require(report_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "Report schema must use Draft 2020-12")
    Draft202012Validator.check_schema(schema); Draft202012Validator.check_schema(report_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(contract), key=lambda e: list(e.absolute_path))
    if errors:
        e=errors[0]; raise RequestChainGapAuditError(f"Contract schema rejected {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}")
    _require(contract.get("schema") == "C11-D-D9-VISUAL-LOOP-GEOMETRIC-REQUEST-CHAIN-GAP-AUDIT-V1", "Contract identity mismatch")
    _require(contract.get("status") == "PREPARATION_ONLY_CANONICAL_REQUEST_TO_BINDING_GAP_AUDIT_NOT_ADMISSION", "Contract status cannot self-promote")
    _require(contract.get("candidate_input_admissible") is False, "Candidate input must stay inadmissible")
    _require(contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") == EXPECTED_MANIFEST_SHA256, "Frozen C11-C contract pin mismatch")
    _require(_sha_file(root / MANIFEST_REL) == EXPECTED_MANIFEST_SHA256, "Frozen C11-C manifest drift")
    lineage = contract.get("source_lineage")
    _require(isinstance(lineage,list) and len(lineage)==13, "Exactly 13 pinned sources required")
    seen=set()
    for i,row in enumerate(lineage):
        _require(isinstance(row,dict) and set(row)=={"path","sha256"}, "Malformed source-lineage row")
        rel=row["path"]
        _require(isinstance(rel,str) and rel and not Path(rel).is_absolute() and ".." not in Path(rel).parts and "\\" not in rel, f"Unsafe source path: {rel!r}")
        _require(rel not in seen, f"Duplicate source pin: {rel}"); seen.add(rel)
        actual=_sha_file(root / rel)
        _require(actual==row["sha256"], f"Pinned source drift: {rel}")
        if i==0: _require(rel==MANIFEST_REL.as_posix() and actual==EXPECTED_MANIFEST_SHA256, "Frozen C11-C manifest must be first pin")
    _require(contract.get("execution_boundary",{}).get("renderer")=="OFF", "Renderer governance drift")
    _require(contract.get("approval_state",{}).get("timing_review_inheritance_approved") is False, "Timing/review inheritance cannot self-approve")
    return contract, schema, report_schema

def _raw_request(grammar_id: str, request_id: str) -> dict[str, Any]:
    return {
      "schema": REQUEST_SCHEMA_ID, "schema_version":"1.0", "request_id":request_id,
      "mode":"REVIEW",
      "selection":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":grammar_id,"variant_id":None},
      "seed":12345, "music_seed":840001, "delivery_profile_id":"REVIEW_720",
      "presentation_profile_id":"social_default_v1", "variation_index":0,
      "audio_enabled":True, "personalization_enabled":True, "editorial_profile":{},
      "production_override":{"title":"Prueba editorial · título","subtitle":"Subtítulo de revisión","call_to_action":"Continuar","language":"es"},
      "provenance":{"source_revision":"C11D-D9.9-DYNAMIC-REQUEST-V1","request_origin":"TEST"}
    }

def run_audit(project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root); contract,_,report_schema=load_contract(root)
    scope=contract["scope"]; matrix_path=root/scope["matrix_contract_path"]; matrix=_read_json(matrix_path)
    _require(matrix.get("source_of_truth",{}).get("frozen_c11c_manifest_sha256")==EXPECTED_MANIFEST_SHA256, "Grammar matrix frozen manifest mismatch")
    matrix_scope=matrix.get("scope",{})
    _require(matrix_scope.get("content_type")==scope["content_type"] and matrix_scope.get("family_id")==scope["family_id"], "Grammar matrix scope mismatch")
    rows=matrix_scope.get("grammar_matrix")
    _require(isinstance(rows,list) and [r.get("grammar_id") for r in rows]==scope["expected_grammar_ids"], "Matrix grammar identity/order mismatch")
    producer=_read_json(root/"c11c-suite/c11c-producer/producer_schema.json")
    family=producer.get("families",{}).get(scope["family_id"],{})
    registry_ids=[str(r[0]) for r in family.get("grammars",[]) if isinstance(r,list) and r and r[0]!="auto"]
    _require(registry_ids==scope["expected_grammar_ids"], "Producer grammar registry differs from pinned V2 matrix")
    cases=[]
    for row in rows:
        grammar_id=str(row["grammar_id"])
        raw=_raw_request(grammar_id,"D-GRAMMAR-CHAIN-GAP-"+grammar_id.upper())
        try:
            result=evaluate_universal_request(raw,root)
            _require(result.get("status")=="PLANNED", f"Canonical D9.9 did not plan {grammar_id}")
            selection=result.get("plan",{}).get("selection",{})
            canonical_selection={k:selection.get(k) for k in ("content_type","family_id","subtype_id","variant_id")}
            expected_selection={"content_type":"visual_loops","family_id":scope["family_id"],"subtype_id":grammar_id,"variant_id":None}
            _require(canonical_selection==expected_selection, f"Canonical selection identity drift for {grammar_id}")
            bridge=build_bridge_planning_record(result,root)
            envelope=prepare_d_only_adapter_envelope(result,bridge,root)
            try:
                binding=build_request_scoped_payload_binding(result,bridge,envelope,root)
                validate_request_scoped_payload_binding(binding,result,bridge,envelope,root)
                binding_status=BOUND_STATUS; binding_error=None
            except Exception as exc:
                message=str(exc)
                if grammar_id not in scope["current_blocked_grammar_ids"] or not message.startswith(scope["blocked_reason_prefix"]):
                    raise RequestChainGapAuditError(f"Unexpected source-binding failure for {grammar_id}: {message}") from exc
                expected_fragment=f"selection.subtype_id={grammar_id!r}"
                _require(expected_fragment in message, f"Blocked reason did not identify selected grammar {grammar_id}")
                binding_status=BLOCKED_STATUS; binding_error=message
            if grammar_id in scope["current_source_binding_grammar_ids"]:
                _require(binding_status==BOUND_STATUS, f"Pinned existing source-binding case unexpectedly blocked: {grammar_id}")
            else:
                _require(binding_status==BLOCKED_STATUS, f"Previously blocked grammar unexpectedly passed without contract version: {grammar_id}")
            cases.append({
                "grammar_id":grammar_id,"grammar_index":int(row["grammar_index"]),"shader_branch":str(row["shader_branch"]),
                "canonical_plan_status":"PLANNED","canonical_request_hash":str(result["request_hash"]),
                "canonical_selection":canonical_selection,"request_scoped_source_binding_status":binding_status,
                "request_scoped_source_binding_error":binding_error,"payload_instance_materialized":False
            })
        except RequestChainGapAuditError:
            raise
        except Exception as exc:
            raise RequestChainGapAuditError(f"Canonical request/binding inspection failed for {grammar_id}: {exc}") from exc
    report={
      "schema":"C11-D-D9-VISUAL-LOOP-GEOMETRIC-REQUEST-CHAIN-GAP-REPORT-V1","schema_version":"1.0",
      "status":"PREPARATION_ONLY_CANONICAL_REQUEST_CHAIN_GAP_AUDIT",
      "source_contract_sha256":_sha_file(root/CONTRACT_REL),
      "source_lineage":[dict(r) for r in contract["source_lineage"]],
      "cases":cases,
      "summary":{"canonical_plans":"5/5","source_binding_review_passes":"1/5","blocked_by_fixed_v1_scope":"4/4","candidate_input_admissible":False},
      "governance":{"godot_invoked":False,"request_persisted":False,"payload_instance_materialized":False,
        "renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"media_created":False,"c11c_source_mutation":False,
        "renderer":"OFF","D4.8":"BLOCKED","release_authority":"NONE"}
    }
    report["audit_sha256"]=_sha_json(report)
    errors=sorted(Draft202012Validator(report_schema).iter_errors(report),key=lambda e:list(e.absolute_path))
    if errors:
        e=errors[0]; raise RequestChainGapAuditError(f"Report schema rejected {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}")
    _require(report["audit_sha256"]==_sha_json({k:v for k,v in report.items() if k!="audit_sha256"}), "Report self-hash mismatch")
    return report

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",default=str(_root()),help="Repository root")
    parser.add_argument("--full-report",action="store_true",help="Print complete audit JSON to stdout; never persist a report")
    args=parser.parse_args(argv)
    try:
        report=run_audit(args.root)
        summary=("C11-D VISUAL LOOP GEOMETRIC REQUEST CHAIN GAP AUDIT PASS | canonical_plans=5/5 | "
                 "source_binding_review=1/5 | blocked_by_fixed_v1_scope=4/4 | candidate_input_admissible=false | "
                 "payload_instance_materialized=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        print(REPORT_PREFIX+json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")))
        print(summary)
        if args.full_report: print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))
        return 0
    except Exception as exc:
        print("C11-D VISUAL LOOP GEOMETRIC REQUEST CHAIN GAP AUDIT FAIL | %s | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"%str(exc))
        return 1
if __name__=="__main__": raise SystemExit(main())
