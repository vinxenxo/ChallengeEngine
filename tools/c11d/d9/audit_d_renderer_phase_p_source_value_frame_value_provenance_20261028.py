#!/usr/bin/env python3
"""Phase P source-value/frame-value provenance audit; outputs evidence under TEMP only."""
from __future__ import annotations
import argparse, hashlib, importlib, json, os, subprocess, sys, time
from pathlib import Path
from typing import Any

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_SCHEMA_V1.json")
HARNESS_REL = Path("tools/c11d/d9/phase_p_source_value_frame_value_provenance_in_memory.gd")
HARNESS_MARKER = "C11D_PHASE_P_PROVENANCE_RECEIPT="
BLOCK_MARKER = "C11D_PHASE_P_PROVENANCE_BLOCKED="
FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_BYTES = 796318
EXPECTED_PHASE_P_CONTRACT_SHA256 = "4412fe2291e82e71dae14fe0b48862ba504c879c01882f9216f83d1d04deb041"
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EXPECTED_IDS = ["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007","CHALLENGE_008","CHALLENGE_009"]
EXPECTED_FIELDS = {"CHALLENGE_003":"target_x","CHALLENGE_005":"target_position","CHALLENGE_006":"target_position","CHALLENGE_007":"target_position","CHALLENGE_008":"active_selection","CHALLENGE_009":"displayed_count"}
EXPECTED_TYPES = {"CHALLENGE_003":"float","CHALLENGE_005":"Vector2","CHALLENGE_006":"Vector2","CHALLENGE_007":"Vector2","CHALLENGE_008":"int","CHALLENGE_009":"int"}
EXPECTED_RELATIONS = {"CHALLENGE_003":"PASS_SOURCE_FORMULA_PER_FRAME","CHALLENGE_005":"PASS_CONSTANT_RUNTIME_TARGET_PER_RUN_NO_DIRECT_CONFIG_EQUALITY","CHALLENGE_006":"PASS_PINNED_CATCH_SOURCE_TO_FRAME_TRACK_HASH_ONLY","CHALLENGE_007":"PASS_PINNED_FIND_SOURCE_TO_FRAME_TRACK_HASH_ONLY","CHALLENGE_008":"PASS_SOURCE_SELECTION_SCHEDULE_AND_OPTION_POSITION","CHALLENGE_009":"PASS_SOURCE_COUNT_SCHEDULE_AND_POSITION_ENCODING"}

class AuditError(RuntimeError): pass

def sha_bytes(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def sha_file(p: Path) -> str:
    if not p.is_file(): raise AuditError(f"required file missing: {p}")
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()
def read_json(p: Path) -> Any:
    try: return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e: raise AuditError(f"invalid JSON {p}: {e}") from e
def load_module(name: str, base: Path):
    if str(base) not in sys.path: sys.path.insert(0,str(base))
    return importlib.import_module(name)
def verify_pins(root: Path, pins: list[dict[str,Any]]) -> list[str]:
    bad=[]
    seen=set()
    for pin in pins:
        path=pin.get("path"); expected=pin.get("sha256"); size=pin.get("bytes")
        if not isinstance(path,str) or path in seen: bad.append(f"PIN_PATH_INVALID_OR_DUPLICATE:{path}"); continue
        seen.add(path); p=root/path
        try:
            data=p.read_bytes(); actual=sha_bytes(data)
            if actual != expected or len(data) != size: bad.append(f"PIN_MISMATCH:{path}:sha={actual}:bytes={len(data)}")
        except OSError: bad.append(f"PIN_MISSING:{path}")
    return bad
def validate_contract(c: Any, schema: Any) -> None:
    if not isinstance(c,dict) or c.get("schema")!="C11D-PHASE-P-SOURCE-VALUE-FRAME-VALUE-PROVENANCE-CONTRACT-V1": raise AuditError("Phase P contract identity invalid")
    if not isinstance(schema,dict) or schema.get("title")!="C11-D Phase P Source Value vs Frame Value Provenance Contract V1": raise AuditError("Phase P schema identity invalid")
    if c.get("expected_selector_count")!=6 or c.get("independent_processes_per_selector")!=2: raise AuditError("Phase P denominator/repeat count invalid")
    selectors=c.get("selectors")
    if not isinstance(selectors,list) or [s.get("challenge_id") for s in selectors]!=EXPECTED_IDS: raise AuditError("Phase P selector order or coverage invalid")
    if c.get("source_pin_count")!=len(c.get("source_pins",[])): raise AuditError("Phase P source-pin count invalid")
    if c.get("frozen_c11c",{}).get("manifest_sha256")!=FROZEN_SHA or c.get("frozen_c11c",{}).get("manifest_bytes")!=FROZEN_BYTES: raise AuditError("C11-C frozen identity changed")
    locks=c.get("governance_locks",{})
    for key,value in {"renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,"seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED","D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED","D9.16":"BLOCKED","D9.17":"BLOCKED_NO_GO","D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING","freeze_eligible":False,"release_authority":"NONE"}.items():
        if locks.get(key)!=value: raise AuditError(f"governance lock changed: {key}")
    if c.get("semantic_binding_policy",{}).get("approved_bindings")!=0 or c.get("semantic_binding_policy",{}).get("approved_custom_data_bindings")!=0 or c.get("semantic_binding_policy",{}).get("approved_renderer_projection_bindings")!=0: raise AuditError("binding approval was not zero")
    for s in selectors:
        cid=s.get("challenge_id")
        if s.get("candidate_field")!=EXPECTED_FIELDS[cid] or s.get("expected_frame_value_type")!=EXPECTED_TYPES[cid]: raise AuditError(f"candidate field/type drift: {cid}")
        if not s.get("source_input_paths") or not s.get("relation_policy"): raise AuditError(f"source relation incomplete: {cid}")
        if bool(s.get("timebase_issue_preserved")) != (cid in ("CHALLENGE_008","CHALLENGE_009")): raise AuditError(f"timebase status mismatch: {cid}")
def validate_receipt(r: Any, contract: dict[str,Any], selector: dict[str,Any], run_id: str, pid: int, request_hash: str, plan_hash: str) -> None:
    if not isinstance(r,dict) or r.get("schema")!="C11D-PHASE-P-SOURCE-VALUE-FRAME-VALUE-PROVENANCE-RECEIPT-V1" or r.get("status")!="SOURCE_VALUE_FRAME_VALUE_PROVENANCE_RECEIPT": raise AuditError("receipt schema/status invalid")
    if r.get("selector",{}).get("challenge_id")!=selector["challenge_id"]: raise AuditError("receipt selector mismatch")
    if r.get("process",{}).get("run_id")!=run_id or r.get("process",{}).get("process_id")!=pid or r.get("process",{}).get("exit_code")!=0: raise AuditError("receipt process identity mismatch")
    lin=r.get("lineage",{})
    if lin.get("contract_sha256")!=sha_file(contract_path_for(contract)) or lin.get("frozen_manifest_sha256")!=FROZEN_SHA: raise AuditError("receipt lineage mismatch")
    if lin.get("challenge_source_sha256")!=selector.get("source_sha256"): raise AuditError("receipt challenge source pin mismatch")
    route=r.get("route",{})
    if route.get("planner_request_hash")!=request_hash or route.get("planner_plan_hash")!=plan_hash or route.get("renderer")!="OFF" or route.get("release_authority")!="NONE": raise AuditError("canonical planner/governance route mismatch")
    fields=r.get("candidate_field_observations",{})
    candidate=fields.get(selector["candidate_field"])
    if not isinstance(candidate,dict) or candidate.get("status")!="PASS": raise AuditError("candidate provenance receipt missing or blocked")
    for k in ("source_input_value_sha256","frame_value_series_sha256","frame_unique_value_set_sha256"):
        v=candidate.get(k)
        if not isinstance(v,str) or len(v)!=64 or any(ch not in "0123456789abcdef" for ch in v): raise AuditError(f"candidate hash malformed: {k}")
    if candidate.get("expected_frame_value_type")!=EXPECTED_TYPES[selector["challenge_id"]] or candidate.get("field")!=EXPECTED_FIELDS[selector["challenge_id"]]: raise AuditError("candidate shape drift")
    if candidate.get("frame_count")!=r.get("source_frames",{}).get("count") or candidate.get("present_frames")!=candidate.get("frame_count"): raise AuditError("candidate cardinality mismatch")
    if candidate.get("actual_candidate_values_serialized") is not False or candidate.get("whole_custom_data_map_serialized") is not False or candidate.get("renderer_binding_approved") is not False: raise AuditError("unsafe provenance receipt flags")
    if candidate.get("source_relation_status")!=EXPECTED_RELATIONS[selector["challenge_id"]]: raise AuditError(f"source relation status incorrect for {selector['challenge_id']}: {candidate.get('source_relation_status')}")
    if candidate.get("relation_mismatch_count")!=0: raise AuditError("source-frame relation mismatches present")
    side=r.get("side_effects",{})
    for k in ("payload_file_written","media_created","renderer_native_input_emitted","render_nodes_created","rendering_server_called","viewport_captured","canonical_state_mutated","production_dispatched"):
        if side.get(k) is not False: raise AuditError(f"side effect not forbidden: {k}")
    state=r.get("semantic_binding_state",{})
    if state.get("approved_bindings")!=0 or state.get("approved_custom_data_bindings")!=0 or state.get("custom_data_values_serialized") is not False: raise AuditError("binding or value serialization lock changed")
    # Keep the 11s vs 12s contradiction visible; it is not adjudicated here.
    tb=r.get("source_timebase",{})
    conflict=selector["challenge_id"] in ("CHALLENGE_008","CHALLENGE_009")
    if bool(tb.get("known_conflict"))!=conflict or (conflict and tb.get("phase_timeline_acceptance") not in ("BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY","NOT_EVALUATED_SOURCE_FRAME_ONLY","BLOCKED_CONFLICT","BLOCKED_DECLARED_TOTAL_PHASE_SUM_CONFLICT","SOURCE_TIMEBASE_CONFLICT_NOT_ACCEPTED")):
        raise AuditError("temporal conflict was not preserved")
def contract_path_for(contract: dict[str,Any]) -> Path:
    # set by main before any receipt validation; actual path remains rooted in the active checkout.
    return _ACTIVE_CONTRACT_PATH
_ACTIVE_CONTRACT_PATH: Path

def run_one(exe: str, ver: str, root: Path, ev: Path, selector: dict[str,Any], plan: dict[str,Any], contract_sha: str, contract: dict[str,Any], n: int) -> dict[str,Any]:
    cid=selector["challenge_id"]; run_id=f"{cid}_P_R{n}"; prefix=ev/f"{cid}_R{n}"
    cmd=[exe,"--headless","--path",str(root),"--script",str(root/HARNESS_REL),"--",f"--challenge-id={cid}",f"--contract-sha256={contract_sha}",f"--run-id={run_id}",f"--godot-version={ver}",f"--planner-request-hash={plan['request_hash']}",f"--planner-plan-hash={plan['plan_hash']}"]
    pid=0; code=127; out=""; err=""; timed_out=False
    try:
        proc=subprocess.Popen(cmd,cwd=str(root),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",errors="replace"); pid=int(proc.pid or 0)
        try: out,err=proc.communicate(timeout=180); code=int(proc.returncode if proc.returncode is not None else 127)
        except subprocess.TimeoutExpired:
            timed_out=True; proc.kill(); out,err=proc.communicate(); code=int(proc.returncode if proc.returncode is not None else 124); err+="\nPHASE_P_TIMEOUT: Godot exceeded 180 seconds.\n"
    except OSError as e: err=f"PHASE_P_PROCESS_START_ERROR:{type(e).__name__}:{e}"
    ob=out.encode("utf-8"); eb=err.encode("utf-8"); (prefix.with_suffix('.out')).write_bytes(ob); (prefix.with_suffix('.err')).write_bytes(eb)
    hits=[line[len(HARNESS_MARKER):] for line in out.splitlines() if line.startswith(HARNESS_MARKER)]
    block_hits=[line[len(BLOCK_MARKER):] for line in out.splitlines() if line.startswith(BLOCK_MARKER)]
    receipt=None; fail=None
    if timed_out: fail="GODOT_PROCESS_TIMEOUT"
    elif code!=0: fail=f"GODOT_EXIT_NONZERO:{code}"
    elif len(hits)!=1: fail=f"GODOT_RECEIPT_MARKER_COUNT:{len(hits)}"
    elif block_hits: fail="GODOT_PROVENANCE_BLOCKED_MARKER_PRESENT"
    else:
        try:
            receipt=json.loads(hits[0]); validate_receipt(receipt,contract,selector,run_id,pid,plan["request_hash"],plan["plan_hash"])
        except Exception as e: receipt=None; fail=f"GODOT_RECEIPT_INVALID:{type(e).__name__}:{e}"
    run={"selector":cid,"run_id":run_id,"process_id":pid,"exit_code":code,"stdout_sha256":sha_bytes(ob),"stderr_sha256":sha_bytes(eb),"receipt_sha256":sha_bytes(json.dumps(receipt,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")) if receipt is not None else None,"receipt":receipt,"failure":fail}
    if fail: raise AuditError(f"{cid} {run_id} failed closed: {fail}; logs={prefix.with_suffix('.out')}|{prefix.with_suffix('.err')}")
    return run

def main() -> int:
    global _ACTIVE_CONTRACT_PATH
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--evidence-dir',required=True); ap.add_argument('--godot',default=None); a=ap.parse_args()
    root=Path(a.repo_root).resolve(); ev=Path(a.evidence_dir).resolve()
    if not root.is_dir() or not (root/'project.godot').is_file(): print('C11D_PHASE_P_STATUS=BLOCKED reason=INVALID_REPO_ROOT',file=sys.stderr); return 2
    temp_env=os.environ.get('TEMP') or os.environ.get('TMP')
    temp_root=Path(temp_env).resolve() if temp_env else Path.home()
    try: ev.relative_to(temp_root)
    except ValueError: print('C11D_PHASE_P_STATUS=BLOCKED reason=EVIDENCE_DIR_NOT_UNDER_TEMP',file=sys.stderr); return 2
    try: ev.relative_to(root); print('C11D_PHASE_P_STATUS=BLOCKED reason=EVIDENCE_DIR_INSIDE_REPO',file=sys.stderr); return 2
    except ValueError: pass
    if ev.exists() and any(ev.iterdir()): print('C11D_PHASE_P_STATUS=BLOCKED reason=EVIDENCE_DIR_NOT_EMPTY',file=sys.stderr); return 2
    ev.mkdir(parents=True,exist_ok=True)
    failures=[]; phase_p_pins=[]; base_pins=[]; selector_rows=[]; plans={}; runs=[]; base=None; version=''; vcode=-1; vout=EMPTY_SHA; verr=EMPTY_SHA; probes=0; planner_calls=0; runtime_calls=0; report_path=ev/'phase_p_provenance_report.json'
    try:
        py=(sys.version_info.major,sys.version_info.minor,sys.version_info.micro)
        if py[0:2]!=(3,13): raise AuditError(f"Python 3.13 required; found {py}")
        cpath=root/CONTRACT_REL; _ACTIVE_CONTRACT_PATH=cpath
        csha=sha_file(cpath);
        if csha != EXPECTED_PHASE_P_CONTRACT_SHA256: raise AuditError("PHASE_P_CONTRACT_SHA256_MISMATCH:"+csha)
        c=read_json(cpath); sch=read_json(root/CONTRACT_SCHEMA_REL); validate_contract(c,sch)
        pins=c.get('source_pins',[]); phase_p_pins=verify_pins(root,pins)
        if phase_p_pins: raise AuditError('PHASE_P_SOURCE_PIN_RECONCILIATION_FAILED:'+phase_p_pins[0])
        manifest=root/'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
        if manifest.stat().st_size!=FROZEN_BYTES or sha_file(manifest)!=FROZEN_SHA: raise AuditError('FROZEN_C11C_MANIFEST_SHA_OR_SIZE_MISMATCH')
        base=load_module('d_renderer_challenge_visual_payload_v2c_source_frame_runtime',root/'tools/c11d/d9')
        base_contract,base_sha=base.load_contract(root); base_pins=base.verify_pins(root,base_contract)
        if base_pins: raise AuditError('V2C_SOURCE_PIN_RECONCILIATION_FAILED:'+base_pins[0])
        exe=base.resolve_godot(a.godot)
        if not exe: raise AuditError('GODOT_4_7_1_MONO_EXECUTABLE_NOT_FOUND')
        version,vcode,vout,verr=base.version_probe(exe); probes=1
        if vcode!=0 or '4.7.1' not in version or 'mono' not in version.lower(): raise AuditError(f'GODOT_4_7_1_MONO_VERSION_PROBE_FAILED:{version}:{vcode}')
        base_by_id={s['challenge_id']:s for s in base_contract['selectors']}
        for s in c['selectors']:
            cid=s['challenge_id']; base_s=base_by_id.get(cid)
            if not base_s: raise AuditError(f'BASE_V2C_SELECTOR_MISSING:{cid}')
            # Keep the source record identical to the accepted V2-C contract, except for Phase-P-only fields.
            for k in ('source_path','source_sha256','mechanic_source','mechanic','family_id','custom_data_candidate_fields'):
                if s.get(k)!=base_s.get(k): raise AuditError(f'BASE_SELECTOR_IDENTITY_DRIFT:{cid}:{k}')
            plan=base.make_planner(root,base_s); planner_calls+=int(plan.get('invocations',0))
            if plan.get('status')!='PLANNED': raise AuditError(f'CANONICAL_PLANNER_BLOCKED:{cid}')
            plans[cid]=plan
            pair=[]
            for n in (1,2):
                runtime_calls+=1
                r=run_one(exe,version,root,ev,base_s,plan,csha,c,n)
                pair.append(r); runs.append(r)
            a1=pair[0]['receipt']['candidate_field_observations'][s['candidate_field']]
            a2=pair[1]['receipt']['candidate_field_observations'][s['candidate_field']]
            agreement=(a1.get('source_input_value_sha256')==a2.get('source_input_value_sha256') and a1.get('frame_value_series_sha256')==a2.get('frame_value_series_sha256') and a1.get('frame_unique_value_set_sha256')==a2.get('frame_unique_value_set_sha256') and a1.get('source_relation_status')==a2.get('source_relation_status'))
            if not agreement: raise AuditError(f'INDEPENDENT_PROCESS_PROVENANCE_HASH_MISMATCH:{cid}')
            selector_rows.append({'challenge_id':cid,'field':s['candidate_field'],'expected_type':s['expected_frame_value_type'],'planner_invocations':1,'runtime_processes':2,'process_ids': [x['process_id'] for x in pair],'run_ids':[x['run_id'] for x in pair],'repeat_hash_agreement':agreement,'source_input_value_sha256':a1['source_input_value_sha256'],'frame_value_series_sha256':a1['frame_value_series_sha256'],'frame_unique_value_set_sha256':a1['frame_unique_value_set_sha256'],'source_relation_status':a1['source_relation_status'],'relation_check_count':a1['relation_check_count'],'relation_mismatch_count':a1['relation_mismatch_count'],'temporal_conflict_preserved':cid in ('CHALLENGE_008','CHALLENGE_009'),'receipt_hashes':[x['receipt_sha256'] for x in pair],'stdout_hashes':[x['stdout_sha256'] for x in pair],'stderr_hashes':[x['stderr_sha256'] for x in pair]})
        if planner_calls!=6 or runtime_calls!=12 or len(selector_rows)!=6: raise AuditError('PHASE_P_DENOMINATOR_MISMATCH')
        final_phase=verify_pins(root,pins); final_base=base.verify_pins(root,base_contract)
        if final_phase: raise AuditError('FINAL_PHASE_P_SOURCE_PIN_RECONCILIATION_FAILED:'+final_phase[0])
        if final_base: raise AuditError('FINAL_V2C_SOURCE_PIN_RECONCILIATION_FAILED:'+final_base[0])
        if sha_file(manifest)!=FROZEN_SHA or manifest.stat().st_size!=FROZEN_BYTES: raise AuditError('FINAL_FROZEN_C11C_MANIFEST_DRIFT')
        report={'schema':'C11D-PHASE-P-SOURCE-VALUE-FRAME-VALUE-PROVENANCE-REPORT-V1','status':'PASS_SOURCE_FRAME_PROVENANCE_ONLY_NO_BINDING_APPROVAL','created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'repository_root':str(root),'contract_sha256':csha,'contract_pin_count':len(pins),'phase_p_source_pins_before_after':'PASS','phase_p_source_pin_count':len(pins),'v2c_parent_source_pins':'PASS','v2c_parent_source_pin_count':len(base_contract.get('source_pins',[])),'frozen_c11c_manifest_sha256':FROZEN_SHA,'frozen_c11c_manifest_bytes':FROZEN_BYTES,'python_version':'.'.join(map(str,sys.version_info[:3])),'godot_version':version,'godot_version_probe_count':probes,'godot_version_probe_stdout_sha256':vout,'godot_version_probe_stderr_sha256':verr,'canonical_planner_invocations':planner_calls,'godot_runtime_process_invocations':runtime_calls,'selector_count':len(selector_rows),'selectors':selector_rows,'process_evidence_files':len([p for p in ev.iterdir() if p.is_file() and p.name not in ('phase_p_provenance_report.json',)]),'actual_candidate_values_serialized':False,'whole_custom_data_map_serialized':False,'payload_materialized':False,'media_created':False,'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','timebase_conflicts':{'CHALLENGE_008':'PRESERVED_DECLARED_11_SECONDS_VS_PHASE_SUM_12_SECONDS','CHALLENGE_009':'PRESERVED_DECLARED_11_SECONDS_VS_PHASE_SUM_12_SECONDS'},'governance_locks':c['governance_locks'],'release_authority':'NONE'}
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        report_sha=sha_file(report_path)
        print('C11D_PHASE_P_SOURCE_VALUE_FRAME_VALUE_PROVENANCE_AUDIT=PASS_SOURCE_FRAME_PROVENANCE_ONLY_NO_BINDING_APPROVAL')
        print(f'PYTHON_CONTRACT_PINS={len(pins)}/{len(pins)}')
        print(f'V2C_PARENT_SOURCE_PINS={len(base_contract.get("source_pins",[]))}/{len(base_contract.get("source_pins",[]))}')
        print(f'CANONICAL_PLANNER_INVOCATIONS={planner_calls}/6')
        print(f'GODOT_RUNTIME_PROCESSES={runtime_calls}/12')
        print(f'SELECTORS={len(selector_rows)}/6')
        print('SOURCE_FRAME_REPEAT_HASHES=PASS')
        print('ACTUAL_CANDIDATE_VALUES_SERIALIZED=false')
        print('WHOLE_CUSTOM_DATA_MAP_SERIALIZED=false')
        print('RENDERER=OFF; MEDIA_CREATED=false; PAYLOAD_MATERIALIZED=false; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
        print(f'REPORT_PATH={report_path}')
        print(f'REPORT_SHA256={report_sha}')
        print(f'GODOT_VERSION_STDOUT_SHA256={vout}')
        print(f'GODOT_VERSION_STDERR_SHA256={verr}')
        return 0
    except Exception as exc:
        msg=f'{type(exc).__name__}:{exc}'
        print(f'C11D_PHASE_P_STATUS=BLOCKED reason={msg}',file=sys.stderr)
        # Preserve a failure report where possible; no success marker is emitted.
        if ev.exists():
            try: (ev/'phase_p_failure.txt').write_text(msg+'\n',encoding='utf-8')
            except OSError: pass
        return 2

if __name__=='__main__': raise SystemExit(main())
