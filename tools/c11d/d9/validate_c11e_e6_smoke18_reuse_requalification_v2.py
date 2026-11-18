#!/usr/bin/env python3
"""C11-E E6 Smoke18 reuse requalification: package checks + read-only checkout audit."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, uuid
from datetime import datetime, timezone
from pathlib import Path

LEDGER_REL = Path('definitions/c11d/production/C11E_E6_SMOKE18_EVIDENCE_REUSE_REQUALIFIED_DRAFT_V2.json')
EXPECTED_C11C = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
EXPECTED_D48 = '0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07'
EXPECTED_HYDRATION = '11f0eeba941f4740759132b3ba984eecf80c68a69aad27fe605a81a4ff8f5a77'
EXPECTED_CH004_V4 = 'ded460447cf69f9360d5761627b0ae6a191a6c687043d8ae2ba4eeeeb01a105a'
EXPECTED_CH004_RECEIPT = '102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0'
EXPECTED_LOOP22 = 'a2fdb135a201a5ce9f91c19b51c65be53ab0d0aaeced6829633958195d7f0131'
EXPECTED_D9_RESOLVER = 'dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd'
EXPECTED_E1_SERVICE = 'e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87'

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def safe_file(root: Path, rel: str) -> Path:
    p_rel = Path(rel)
    if p_rel.is_absolute() or any(part in ('..', '') for part in p_rel.parts):
        raise ValueError(f'UNSAFE_RELATIVE_PATH:{rel}')
    p = root / p_rel
    resolved_root = root.resolve()
    resolved = p.resolve(strict=False)
    if resolved_root != resolved and resolved_root not in resolved.parents:
        raise ValueError(f'PATH_ESCAPES_PROJECT_ROOT:{rel}')
    if p.is_symlink():
        raise ValueError(f'SYMLINK_NOT_ALLOWED:{rel}')
    if not p.is_file():
        raise FileNotFoundError(f'FILE_MISSING:{rel}')
    return p

def verify(root: Path, name: str, rel: str, expected: str, expected_bytes: int | None = None):
    p = safe_file(root, rel)
    actual = digest(p)
    size = p.stat().st_size
    ok = actual == expected and (expected_bytes is None or size == expected_bytes)
    return {'id':name,'path':rel,'expected_sha256':expected,'actual_sha256':actual,'bytes':size,
            'expected_bytes':expected_bytes,'status':'PASS' if ok else 'FAIL'}

def verify_sidecar(root: Path, name: str, rel: str, expected: str):
    p = safe_file(root, rel)
    content = p.read_text(encoding='utf-8').strip()
    expected_line = f"{expected}  {Path(rel[:-7]).name}" if rel.lower().endswith('.sha256') else None
    # Sidecars are GNU sha256sum format; derive target name from removing '.sha256'.
    ok = bool(expected_line) and content.lower() == expected_line.lower()
    return {'id':name,'path':rel,'actual_content':content,'expected_content':expected_line,
            'status':'PASS' if ok else 'FAIL'}

def load_ledger(path: Path):
    obj = json.loads(path.read_text(encoding='utf-8'))
    validate_ledger(obj)
    return obj

def validate_ledger(obj):
    if obj.get('schema') != 'C11E-E6-SMOKE18-EVIDENCE-REUSE-REQUALIFICATION-DRAFT-V2':
        raise ValueError('LEDGER_SCHEMA_MISMATCH')
    if obj.get('status') != 'REQUALIFICATION_CANDIDATE_LEDGER_PREPARED_NOT_FROZEN_NOT_E6_ACCEPTED':
        raise ValueError('LEDGER_STATUS_MUST_REMAIN_DRAFT_NOT_ACCEPTED')
    rows = obj.get('smoke18_scenarios', [])
    if len(rows) != 18:
        raise ValueError(f'SMOKE18_COUNT_MISMATCH:{len(rows)}')
    counts = {f: sum(1 for r in rows if r.get('family') == f) for f in ('challenge','visual_loop','visual_drill')}
    if counts != {'challenge':6,'visual_loop':6,'visual_drill':6}:
        raise ValueError(f'FAMILY_COUNTS_MISMATCH:{counts}')
    if obj['summary'].get('reuse_candidates_total') != 13:
        raise ValueError('REUSE_CANDIDATE_COUNT_MISMATCH')
    if obj['summary'].get('e6_accepted_scenarios') != 0:
        raise ValueError('E6_ACCEPTANCE_MUST_REMAIN_ZERO')
    if obj['governance'].get('e6_media_authorized') is not False:
        raise ValueError('E6_MEDIA_AUTHORIZATION_MUST_REMAIN_FALSE')
    if obj['governance'].get('d4_8') != 'BLOCKED_PINNED_R1V_ONLY':
        raise ValueError('D4_8_MUST_REMAIN_BLOCKED')
    if obj['governance'].get('release_authority') != 'NONE':
        raise ValueError('RELEASE_AUTHORITY_MUST_REMAIN_NONE')
    if any(r.get('e6_acceptance') == 'ACCEPTED' for r in rows):
        raise ValueError('CANDIDATE_ROW_MUST_NOT_BE_E6_ACCEPTED')
    lp06 = next(r for r in rows if r['scenario_id']=='E6-LP-06')
    if lp06.get('verified_media_outputs',{}).get('A',{}).get('sha256') != EXPECTED_LOOP22:
        raise ValueError('LOOP22_HASH_PIN_MISMATCH')
    if lp06.get('verified_media_outputs',{}).get('B',{}).get('sha256') != EXPECTED_LOOP22:
        raise ValueError('LOOP22_PAIR_HASH_MISMATCH')
    ch004 = next(r for r in rows if r['scenario_id']=='E6-CH-004')
    if ch004.get('ledger_reuse_disposition') != 'ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED':
        raise ValueError('CH004_DISPOSITION_MISMATCH')
    if ch004.get('reuse_evidence',{}).get('semantic_review_v4',{}).get('sha256') != EXPECTED_CH004_V4:
        raise ValueError('CH004_V4_EVIDENCE_PIN_MISMATCH')
    if len([r for r in rows if r['family']=='visual_loop']) != 6 or len([r for r in rows if r['family']=='visual_drill']) != 6:
        raise ValueError('LOOP_OR_DRILL_ROW_COUNT_MISMATCH')
    # All music-seed values in Challenge remain proposal-only.
    for row in rows:
        if row['family']=='challenge':
            for probe in row.get('execution_probes',[]):
                if probe.get('music_seed_status') != 'PROPOSAL_ONLY_NOT_AUTHORIZED':
                    raise ValueError(f'CHALLENGE_MUSIC_SEED_AUTHORITY_DRIFT:{row["scenario_id"]}')

def package_check(package_root: Path):
    ledger_path = package_root / 'payload' / LEDGER_REL
    obj = load_ledger(ledger_path)
    doc = package_root / 'payload/docs/current/e/C11E_E6_SMOKE18_EVIDENCE_REUSE_REQUALIFICATION_20261118_V2.md'
    if not doc.is_file():
        raise FileNotFoundError('PACKAGE_README_PAYLOAD_MISSING')
    print('LEDGER_SCHEMA=PASS')
    print('SMOKE18_ROWS=18/18')
    print('FAMILY_COUNTS=6/6/6')
    print('REUSE_CANDIDATES=13')
    print('E6_ACCEPTED=0')
    print('D4_8=BLOCKED')
    print('PACKAGE_STATIC_VALIDATION=PASS')
    return 0

def project_audit(root: Path):
    ledger_path = safe_file(root, str(LEDGER_REL).replace('\\','/'))
    ledger = load_ledger(ledger_path)
    checks=[]
    def add(name, rel, sha_value, size=None):
        try: checks.append(verify(root,name,rel,sha_value,size))
        except Exception as e: checks.append({'id':name,'path':rel,'status':'FAIL','error':str(e)})
    def side(name, rel, sha_value):
        try: checks.append(verify_sidecar(root,name,rel,sha_value))
        except Exception as e: checks.append({'id':name,'path':rel,'status':'FAIL','error':str(e)})
    add('frozen_c11c_manifest','release/C11C_FREEZE_PACKAGE_MANIFEST.json',EXPECTED_C11C,796318)
    add('d4_8_policy','definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json',EXPECTED_D48)
    add('d9_editorial_resolver_current','tools/c11d/d9/universal_editorial_model.py',EXPECTED_D9_RESOLVER)
    add('e1_production_service_current','c11c-suite/c11c-producer/c11e_production_service.py',EXPECTED_E1_SERVICE)
    hyd=ledger['evidence_lineage']['hydration_v2']
    add('hydration_v2_report',hyd['path'],hyd['sha256'],hyd['bytes'])
    side('hydration_v2_report_sidecar',hyd['sidecar_path'],hyd['sha256'])
    v4=ledger['evidence_lineage']['ch004_semantic_review_v4']
    add('ch004_semantic_review_v4_report',v4['path'],v4['sha256'])
    side('ch004_semantic_review_v4_sidecar',v4['sidecar_path'],v4['sha256'])
    ch004=next(r for r in ledger['smoke18_scenarios'] if r['scenario_id']=='E6-CH-004')
    ev=ch004['reuse_evidence']
    add('ch004_e4a7_receipt',ev['e4a7_receipt_path'],ev['e4a7_receipt_sha256'])
    e5=ledger['evidence_lineage']['e5_closeout']
    add('e5_operator_av_closeout',e5['path'],e5['sha256'])
    plan=ledger['evidence_lineage']['e6_plan_only']
    add('e6_d9_plan_manifest',plan['manifest_path'],plan['manifest_sha256'])
    add('e6_d9_plan_receipt',plan['receipt_path'],plan['receipt_sha256'])
    audit=ledger['evidence_lineage']['smoke18_readonly_audit']
    add('e6_smoke18_readonly_audit_receipt',audit['receipt_path'],audit['receipt_sha256'])
    # Six E4C Drill receipt hashes are checked directly; nested paths remain attributed to the exact pinned Hydration V2 audit.
    for row in ledger['smoke18_scenarios']:
        if row['family']=='visual_drill':
            add(row['scenario_id']+'_e4c_receipt',row['e4c_receipt_path'],row['e4c_receipt_sha256'])
    lp06=next(r for r in ledger['smoke18_scenarios'] if r['scenario_id']=='E6-LP-06')
    for variant in ('A','B'):
        item=lp06['verified_media_outputs'][variant]
        add('loop22_interference_plane_'+variant,item['path'],item['sha256'],item['bytes'])
    passed=sum(1 for c in checks if c['status']=='PASS')
    failed=len(checks)-passed
    run_id='E6SMK18REQUAL_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8].upper()
    report={
        'schema':'C11E-E6-SMOKE18-REUSE-REQUALIFICATION-RECEIPT-V1','run_id':run_id,
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE' if failed==0 else 'BLOCKED_E6_REUSE_REQUALIFICATION_EVIDENCE_MISMATCH',
        'checks':checks,'check_count':len(checks),'passed_checks':passed,'failed_checks':failed,
        'candidate_summary':{'smoke18_rows':18,'reconciled_reuse_candidates':13,'e6_accepted':0,'fresh_challenge_av_required':5},
        'hydration_v2_original_result_preserved':{'checks':1803,'passed':1801,'failed':2,'failure_categories':{'historical_source_pin_divergence':2,'other_failures':0},'report_sha256':EXPECTED_HYDRATION},
        'ch004_v4_semantic_review':{'sha256':EXPECTED_CH004_V4,'status':v4['status'],'disposition':'ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED'},
        'loop22_media_rehash':{'A_sha256':EXPECTED_LOOP22,'B_sha256':EXPECTED_LOOP22,'bytes_each':10500987,'status':'PASS' if all(c['status']=='PASS' for c in checks if c['id'].startswith('loop22_interference_plane_')) else 'FAIL'},
        'governance':{'e1':'PREPARE_ONLY','d4_8':'BLOCKED','d4_8_overridden':False,'renderer':'OFF','production_dispatch':False,'production_media':False,'godot_invoked':False,'ffmpeg_invoked':False,'ffprobe_invoked':False,'audio_generated':False,'mux_invoked':False,'batch_id_consumed':False,'release_authority':'NONE','source_files_modified':False,'git_checks':'SKIPPED','commits':'OPERATOR_MANAGED','source_file_pins':'ENFORCED'}
    }
    outdir=root/'artifacts/tests/c11e/e6_smoke18_reuse_requalification'/run_id
    outdir.mkdir(parents=True,exist_ok=False)
    out=outdir/'E6_SMOKE18_REUSE_REQUALIFICATION_RECEIPT_V1.json'
    raw=(json.dumps(report,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
    out.write_bytes(raw)
    h=hashlib.sha256(raw).hexdigest()
    sidecar=out.with_name(out.name+'.sha256')
    sidecar.write_text(f'{h}  {out.name}\n',encoding='ascii')
    print('E6_REUSE_REQUALIFICATION_STATUS='+report['status'])
    print(f'E6_REUSE_REQUALIFICATION_CHECKS={passed}/{len(checks)} PASS')
    print(f'E6_REUSE_REQUALIFICATION_FAILURES={failed}')
    print('E6_REUSE_CANDIDATES=13; E6_ACCEPTED=0; FRESH_CHALLENGE=5')
    print('D4_8=BLOCKED; MEDIA_TOOLS_INVOKED=FALSE; MEDIA_CREATED=FALSE; BATCH_ID_CONSUMED=FALSE; RELEASE_AUTHORITY=NONE')
    print('SOURCE_FILES_MODIFIED=FALSE; GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED')
    print('REPORT='+str(out))
    print('REPORT_SHA256='+h)
    print('REPORT_SIDECAR='+str(sidecar))
    return 0 if failed==0 else 2

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--package-root')
    ap.add_argument('--project-root')
    args=ap.parse_args()
    if bool(args.package_root)==bool(args.project_root):
        ap.error('specify exactly one of --package-root or --project-root')
    try:
        if args.package_root: return package_check(Path(args.package_root).resolve())
        return project_audit(Path(args.project_root).resolve())
    except Exception as e:
        print('E6_REUSE_REQUALIFICATION_FATAL='+str(e),file=sys.stderr)
        return 2
if __name__=='__main__': raise SystemExit(main())
