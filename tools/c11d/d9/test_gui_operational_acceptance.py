from __future__ import annotations
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import gui_operational_acceptance as op

def expect(value: bool, message: str):
    if not value: raise AssertionError(message)

def main() -> int:
    record=op.build_operational_preflight(ROOT)
    expect(record['status']=='PREFLIGHT_PASS_OPERATOR_CONFIRMATION_REQUIRED',json.dumps(record.get('errors',[]),ensure_ascii=False))
    result=op.validate_operational_preflight(record,ROOT)
    expect(result['valid'] is True,'operational preflight receipt did not validate')
    expect(record['capability_count']==8 and record['surface_count']==5,'coverage count mismatch')
    expect(record['operator_acceptance']['confirmed'] is False and record['operator_acceptance']['evidence_ref'] is None,'static preflight cannot confirm GUI acceptance')
    expect(record['governance']['renderer_activation'] is False and record['governance']['production_execution'] is False and record['governance']['media_created'] is False and record['governance']['d4_8']=='BLOCKED' and record['governance']['release_authority']=='NONE','D9.15 governance drift')
    negative=0
    def reject(label,mutator,reseal=True):
        candidate=copy.deepcopy(record); mutator(candidate)
        if reseal: candidate=op._seal(candidate)
        try: op.validate_operational_preflight(candidate,ROOT)
        except op.OperationalAcceptanceError: pass
        else: raise AssertionError(f'D9.15 negative unexpectedly accepted: {label}')
    reject('claim operational closed',lambda x:x.update(operational_acceptance_closed=True)); negative+=1
    reject('claim operator confirmation',lambda x:x['operator_acceptance'].update(confirmed=True)); negative+=1
    reject('invent evidence ref',lambda x:x['operator_acceptance'].update(evidence_ref='artifacts/fake.png')); negative+=1
    reject('renderer activated',lambda x:x['side_effects'].update(renderer_activated=True)); negative+=1
    reject('production executed',lambda x:x['side_effects'].update(production_executed=True)); negative+=1
    reject('media created',lambda x:x['side_effects'].update(media_created=True)); negative+=1
    reject('release created',lambda x:x['side_effects'].update(release_created=True)); negative+=1
    reject('release authority granted',lambda x:x['governance'].update(release_authority='GRANTED')); negative+=1
    reject('D4.8 unlocked',lambda x:x['governance'].update(d4_8='AUTHORIZED')); negative+=1
    reject('master seed adopted',lambda x:x['governance'].update(master_seed='ADOPTED')); negative+=1
    reject('cross-domain seeds shared',lambda x:x['governance'].update(cross_domain_seed_sharing='ALLOWED')); negative+=1
    reject('drop capability',lambda x:x.update(capabilities=x['capabilities'][:-1],capability_count=7)); negative+=1
    reject('add sixth surface',lambda x:x.update(surfaces=x['surfaces']+[{'surface_id':'c11d-control'}],surface_count=6)); negative+=1
    reject('operator confirmed capability',lambda x:x['capabilities'][0].update(operator_confirmed=True,evidence_ref='evidence/gui.png')); negative+=1
    reject('freeze manifest mismatch',lambda x:x['references'].update(historical_c11c_manifest_sha256='0'*64)); negative+=1
    reject('status claim pass',lambda x:x.update(status='PASS',preflight_pass=True)); negative+=1
    reject('raw seal tamper',lambda x:x.update(status='BLOCKED'),reseal=False); negative+=1
    reject('longform enabled',lambda x:x['governance'].update(longform='ENABLED')); negative+=1
    reject('side-effect declaration omitted',lambda x:x.update(side_effects={})); negative+=1
    expect(negative==19,f'negative controls mismatch: {negative}/19')
    manifest=json.loads((ROOT/'c11c-suite/c11c-test/BUILD_MANIFEST.json').read_text(encoding='utf-8-sig'))
    expect(manifest.get('d9_15_operational_acceptance') is True,'Test manifest does not register D9.15')
    expect(manifest.get('renderer_activation') is False and manifest.get('media_creation') is False and manifest.get('release_authority')=='NONE','Test manifest governance drift')
    print(f"C11-D D9.15 GUI OPERATIONAL ACCEPTANCE PREFLIGHT PASS | capabilities=8/8 | surfaces=5/5 | negative={negative}/19 | operator_confirmation=REQUIRED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0

if __name__=='__main__': raise SystemExit(main())
