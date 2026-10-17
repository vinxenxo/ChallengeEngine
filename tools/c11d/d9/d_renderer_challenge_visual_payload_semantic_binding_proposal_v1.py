"""Static source-derived semantic-binding proposal audit; it never materializes a payload."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parents[2]
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_SCHEMA_V1.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_REPORT_SCHEMA_V1.json")
CAPABILITY_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json")
CAPABILITY_SHA256 = "3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_ID = "C11-D-RENDERER-CHALLENGE-VISUAL-PAYLOAD-SEMANTIC-BINDING-PROPOSAL-CONTRACT-V1"
REPORT_ID = "C11-D-RENDERER-CHALLENGE-VISUAL-PAYLOAD-SEMANTIC-BINDING-PROPOSAL-REPORT-V1"
BASE_FIELDS = ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"]
EXPECTED_IDS = [f"CHALLENGE_{i:03d}" for i in range(1,10)]
EXPECTED_CUSTOM_FIELDS = {"CHALLENGE_003":"target_x","CHALLENGE_005":"target_position","CHALLENGE_006":"target_position","CHALLENGE_007":"target_position","CHALLENGE_008":"active_selection","CHALLENGE_009":"displayed_count"}
EXPECTED_STATIC_FIELDS = {"CHALLENGE_001":"presentation.static_target_position","CHALLENGE_002":"difficulty.parking.target_position","CHALLENGE_004":"difficulty.parking.target_position"}
class ProposalError(ValueError): pass

def sha256_bytes(value: bytes) -> str: return hashlib.sha256(value).hexdigest()
def sha256_file(path: Path) -> str: return sha256_bytes(path.read_bytes())
def read_json(path: Path) -> dict[str, Any]:
    try: value=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise ProposalError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value,dict): raise ProposalError(f"Expected JSON object: {path}")
    return value

def dotted(value: Mapping[str,Any], path: str) -> Any:
    current: Any=value
    for part in path.split('.'):
        if not isinstance(current,Mapping) or part not in current: raise ProposalError(f"Source pointer does not resolve: {path}")
        current=current[part]
    return current

def validate_binding_approval(cid: str, binding: Mapping[str,Any]) -> None:
    if binding.get("proposal_status") != "PROPOSAL_ONLY_NOT_APPROVED" or binding.get("binding_authorized") is not False or binding.get("renderer_projection_approved") is not False:
        raise ProposalError(f"Selector binding self-approved: {cid}")

def validate_custom_candidate(cid: str, field: str) -> None:
    if EXPECTED_CUSTOM_FIELDS.get(cid) != field:
        raise ProposalError(f"Unapproved/custom data field proposed for {cid}: {field}")

def validate_contract(root: Path) -> tuple[dict[str,Any],dict[str,Any],dict[str,Any]]:
    contract=read_json(root/CONTRACT_REL); schema=read_json(root/SCHEMA_REL); report_schema=read_json(root/REPORT_SCHEMA_REL)
    if contract.get('schema') != CONTRACT_ID or contract.get('schema_version') != '1.0': raise ProposalError('Contract identity/version mismatch')
    if contract.get('status') != 'PREPARATION_ONLY_PROPOSAL_NOT_APPROVED_NOT_RUNTIME_ACCEPTANCE': raise ProposalError('Proposal status must not self-approve')
    if schema.get('$id') != 'urn:c11d:challenge-visual-payload-semantic-binding-proposal:v1' or schema.get('additionalProperties') is not False: raise ProposalError('Contract schema identity/strictness mismatch')
    if report_schema.get('$id') != 'urn:c11d:challenge-visual-payload-semantic-binding-proposal-report:v1' or report_schema.get('additionalProperties') is not False: raise ProposalError('Report schema identity/strictness mismatch')
    src=contract.get('source_authority',{})
    if src.get('frozen_c11c_manifest_sha256') != FROZEN_MANIFEST_SHA256: raise ProposalError('Frozen C11-C pin mismatch')
    if src.get('capability_matrix_contract_sha256') != CAPABILITY_SHA256 or sha256_file(root/CAPABILITY_REL) != CAPABILITY_SHA256: raise ProposalError('Capability matrix source pin mismatch')
    locks=contract.get('governance_locks',{})
    expected={'renderer':'OFF','media_created':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed_adopted':False,'d4_8':'BLOCKED','d9_10':'PREPARE_ONLY','d9_17':'BLOCKED_NO_GO','d10':'BLOCKED_FOR_PROMOTION','release_authority':'NONE','source_mutation':False,'godot_invocations':0,'payload_materialized':False,'payload_files_written':False,'renderer_native_input_emitted':False,'renderer_dispatch_invoked':False,'media_output_created':False}
    if locks != expected: raise ProposalError('Governance lock mismatch')
    scope=contract.get('scope',{})
    if scope.get('approved_custom_data_bindings') != 0 or scope.get('approved_renderer_projection_bindings') != 0: raise ProposalError('Proposal cannot contain approved bindings')
    if scope.get('custom_data_policy') != 'NEVER_SERIALIZE_WHOLE_MAP; CANDIDATE_FIELDS_ARE_PROPOSAL_ONLY_AND_BINDING_AUTHORIZED_FALSE': raise ProposalError('custom_data policy changed')
    return contract,schema,report_schema

def validate_proposal(root: Path | None = None) -> dict[str,Any]:
    root=root or ROOT_DEFAULT
    contract, schema, report_schema=validate_contract(root)
    # Invoke the already accepted V2-A audit as the authority for the 43 source pins.
    sys.path.insert(0,str(root/'tools'/'c11d'/'d9'))
    try:
        from d_renderer_challenge_visual_payload_capability_matrix_v1 import validate_inventory, build_report as build_cap_report
        inventory=validate_inventory(root)
        cap_report=build_cap_report(root)
    except Exception as exc:
        raise ProposalError(f"Accepted V2-A source audit did not validate: {exc}") from exc
    if inventory.get('pins',{}).get('source_pins') != 43 or cap_report.get('summary',{}).get('selectors') != '9/9': raise ProposalError('V2-A source pins or selector matrix incomplete')
    cap=read_json(root/CAPABILITY_REL)
    rows=contract.get('selector_semantics')
    if not isinstance(rows,list) or [str(r.get('challenge_id')) for r in rows] != EXPECTED_IDS: raise ProposalError('Semantic proposal must declare selectors 001..009 in order')
    if contract.get('never_bind_by_default') != cap.get('custom_data_semantics',{}).get('never_bind_by_default'): raise ProposalError('Never-bind telemetry denylist drift')
    unique_assets=set(); asset_refs=0; static_count=0; custom_count=0
    for i,row in enumerate(rows):
        cid=EXPECTED_IDS[i]; selector=cap['selector_matrix'][i]
        if row.get('mechanic') != selector.get('mechanic') or row.get('challenge_source_sha256') != next(x['sha256'] for x in cap['pinned_sources'] if x['path']==f'challenges/{cid}.json'):
            raise ProposalError(f'Selector identity/source lineage mismatch: {cid}')
        if row.get('mechanic_source_path') != selector.get('mechanic_source_path') or row.get('mechanic_source_sha256') != selector.get('mechanic_source_sha256'):
            raise ProposalError(f'Mechanic lineage mismatch: {cid}')
        if row.get('asset_bindings') != selector.get('asset_bindings'): raise ProposalError(f'Asset role references drifted: {cid}')
        if row.get('base_track',{}).get('fields') != BASE_FIELDS: raise ProposalError(f'Base track fields mismatch: {cid}')
        if row.get('base_track',{}).get('coordinate_projection') != 'UNRESOLVED_NOT_APPLIED' or row.get('base_track',{}).get('delivery_resampling') != 'UNRESOLVED_NOT_APPLIED': raise ProposalError(f'Base track can not project/resample: {cid}')
        spec=row.get('secondary_binding_proposal',{})
        validate_binding_approval(cid, spec)
        if spec.get('candidate_custom_data_field'):
            field=str(spec['candidate_custom_data_field'])
            validate_custom_candidate(cid, field)
            if field not in selector.get('custom_data_keys_inventory_only',[]): raise ProposalError(f'Field not in source custom_data inventory for {cid}: {field}')
            src=(root/str(selector['mechanic_source_path'])).read_text(encoding='utf-8-sig')
            if re.search(r'"'+re.escape(field)+r'"\s*:',src) is None: raise ProposalError(f'Field not found in mechanic source: {cid}.{field}')
            custom_count+=1
        else:
            if cid in EXPECTED_CUSTOM_FIELDS: raise ProposalError(f'Required candidate field omitted: {cid}')
        if cid in EXPECTED_STATIC_FIELDS:
            if spec.get('source_pointer') != EXPECTED_STATIC_FIELDS[cid]: raise ProposalError(f'Static source pointer mismatch: {cid}')
            ch=read_json(root/f'challenges/{cid}.json')
            value=dotted(ch,EXPECTED_STATIC_FIELDS[cid])
            if not isinstance(value,list) or len(value)!=2 or not all(isinstance(x,(int,float)) for x in value): raise ProposalError(f'Static target source value is not a coordinate pair: {cid}')
            static_count+=1
        elif spec.get('source_pointer') != 'FrameSnapshot.custom_data.'+str(spec.get('candidate_custom_data_field','')):
            raise ProposalError(f'Custom source pointer mismatch: {cid}')
        if cid=='CHALLENGE_003':
            if row.get('coordinate_space')!='PILOT_0X100' or spec.get('coordinate_policy')!='PILOT_0X100_SCALAR_ONLY_NO_2D_POSITION_CONVERSION': raise ProposalError('Pilot target_x must remain scalar in source coordinate space')
        if cid in ('CHALLENGE_005','CHALLENGE_006','CHALLENGE_007') and spec.get('semantic_type')!='Vector2': raise ProposalError(f'Secondary target needs Vector2: {cid}')
        if cid=='CHALLENGE_008' and (spec.get('semantic_type')!='int' or row.get('runtime_preview_target_scope')!='WITHHOLD_FOR_TIMEBASE_DECISION'): raise ProposalError('Choose challenge must remain held behind timebase decision')
        if cid=='CHALLENGE_009' and (spec.get('semantic_type')!='int' or row.get('runtime_preview_target_scope')!='WITHHOLD_FOR_TIMEBASE_DECISION'): raise ProposalError('Count challenge must remain held behind timebase decision')
        if row.get('temporal_status')!=selector.get('temporal_status'): raise ProposalError(f'Temporal status drift: {cid}')
        for rel in row['asset_bindings'].values(): unique_assets.add(rel); asset_refs+=1
    if static_count != 3 or custom_count != 6 or asset_refs != 27 or len(unique_assets) != 15: raise ProposalError('Expected static/custom mapping or asset role counts changed')
    # Ensure only source-declared contradictory totals are quarantined.
    conflicts=[r['challenge_id'] for r in rows if r.get('temporal_status')=='DECLARED_TOTAL_CONFLICTS_WITH_PHASE_SUM']
    if conflicts != ['CHALLENGE_008','CHALLENGE_009']: raise ProposalError(f'Temporal conflict set changed: {conflicts}')
    summary={'selectors':'9/9','source_pins':'43/43','base_track_fields':'6/6','secondary_binding_proposals':'9/9','static_source_bindings':'3/3','custom_data_candidate_fields':'6/6','asset_reference_bindings':'27/27','unique_assets':'15/15','temporal_conflicts':'2/2','approved_bindings':0,'godot_invocations':0,'payload_materialized':False,'renderer':'OFF','release_authority':'NONE'}
    return {'schema':REPORT_ID,'schema_version':'1.0','status':'PASS_STATIC_PROPOSAL_ONLY_NO_BINDING_APPROVAL','contract_sha256':sha256_file(root/CONTRACT_REL),'capability_matrix_sha256':CAPABILITY_SHA256,'summary':summary,'selector_semantics':rows,'temporal_review':contract['temporal_review'],'governance_locks':contract['governance_locks']}

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--root',default='.') ; parser.add_argument('--full-report',action='store_true'); args=parser.parse_args(argv)
    root=Path(args.root).resolve()
    try:
        report=validate_proposal(root); s=report['summary']
        print('C11-D CHALLENGE VISUAL PAYLOAD SEMANTIC BINDING PROPOSAL V1 PASS | selectors=%s | source_pins=%s | base_track_fields=%s | secondary_binding_proposals=%s | static_source_bindings=%s | custom_data_candidate_fields=%s | asset_reference_bindings=%s | unique_assets=%s | temporal_conflicts=%s | approved_bindings=0 | godot_invocations=0 | payload_materialized=false | renderer=OFF | release_authority=NONE' % (s['selectors'],s['source_pins'],s['base_track_fields'],s['secondary_binding_proposals'],s['static_source_bindings'],s['custom_data_candidate_fields'],s['asset_reference_bindings'],s['unique_assets'],s['temporal_conflicts']))
        if args.full_report: print('C11D_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_REPORT='+json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(',',':')))
        return 0
    except Exception as exc:
        print('C11-D CHALLENGE VISUAL PAYLOAD SEMANTIC BINDING PROPOSAL V1 FAIL | '+str(exc),file=sys.stderr); return 1
if __name__ == '__main__': raise SystemExit(main())
