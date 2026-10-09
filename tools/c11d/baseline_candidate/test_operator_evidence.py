from __future__ import annotations
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / 'tools/c11d/baseline_candidate/operator_evidence.py'
spec = importlib.util.spec_from_file_location('d915_operator_evidence_tested', MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

REQ = 'definitions/c11d/baseline/D_BASELINE_OPERATOR_EVIDENCE_REQUIREMENTS_V1.json'
D915 = 'definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json'
MANIFEST = 'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
GOVERNANCE_COPIES = [
    'tools/c11d/baseline_candidate/operator_evidence.py',
    'definitions/c11d/d9/D9_14_GUI_REAL_MEDIA_CERTIFICATION_GATE_V1.json',
    'definitions/c11d/d9/D9_16_FULL_ACCEPTANCE_V1.json',
    'definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json',
    'docs/current/d/D9.17_D9_CLOSURE_ADJUDICATION_CHECKPOINT.md',
]
ATTEST = module.ATTESTATION
FINAL_ATTEST = 'I_CONFIRM_ALL_D915_PAIRINGS_REVIEWED_NO_MEDIA'

def base_copy(tmp: Path) -> None:
    for rel in (REQ, D915, MANIFEST, *GOVERNANCE_COPIES):
        target=tmp/rel; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,target)

def expect_error(fn, label):
    try: fn()
    except module.EvidenceError: return
    raise AssertionError(f'negative unexpectedly accepted: {label}')

def main() -> int:
    negatives=0
    with tempfile.TemporaryDirectory(prefix='d915_operator_evidence_') as tmp_raw:
        tmp=Path(tmp_raw); base_copy(tmp)
        init=module.init_ledger(tmp)
        assert init['status']=='INITIALIZED_PENDING' and init['required_pairings']==13
        expect_error(lambda: module.init_ledger(tmp),'ledger reinitialize'); negatives+=1
        req=module._requirements(tmp)
        rows=req['required_evidence_pairings']
        assert len(rows)==13
        evidence_root=tmp/'artifacts/evidence/d9_15_operator'; evidence_root.mkdir(parents=True,exist_ok=True)
        status=module.inspect_ledger(tmp)
        assert status['status']=='D9.15_OPERATOR_EVIDENCE_REQUIRED' and status['pending_pairings']==13
        # A path outside the approved evidence root, an unsupported pairing and an attestation spoof are rejected.
        expect_error(lambda: module.record_event(tmp,surface='c11c-config',capability='configuration',action='Observed config GUI pass',evidence_file='../escape.txt',observed_status='PASS',operator='QA',operator_attestation=ATTEST),'path traversal'); negatives+=1
        expect_error(lambda: module.record_event(tmp,surface='c11c-catalog',capability='configuration',action='Observed config GUI pass',evidence_file='artifacts/evidence/d9_15_operator/e.txt',observed_status='PASS',operator='QA',operator_attestation=ATTEST),'invalid surface/capability pair'); negatives+=1
        expect_error(lambda: module.record_event(tmp,surface='c11c-config',capability='configuration',action='Observed config GUI pass',evidence_file='artifacts/evidence/d9_15_operator/missing.txt',observed_status='PASS',operator='QA',operator_attestation=ATTEST),'missing evidence'); negatives+=1
        (evidence_root/'tiny.txt').write_text('short',encoding='utf-8')
        expect_error(lambda: module.record_event(tmp,surface='c11c-config',capability='configuration',action='Observed config GUI pass',evidence_file='artifacts/evidence/d9_15_operator/tiny.txt',observed_status='PASS',operator='QA',operator_attestation=ATTEST),'short evidence'); negatives+=1
        (evidence_root/'good.txt').write_text('GUI visible status PASS, no media created, renderer disabled.\nEvidence record fixture.',encoding='utf-8')
        expect_error(lambda: module.record_event(tmp,surface='c11c-config',capability='configuration',action='Observed config GUI pass',evidence_file='artifacts/evidence/d9_15_operator/good.txt',observed_status='PASS',operator='QA',operator_attestation=''),'missing operator attestation'); negatives+=1
        expect_error(lambda: module.finalize_acceptance(tmp,operator_attestation=FINAL_ATTEST),'finalize incomplete ledger'); negatives+=1

        # Record one PASS screenshot/log excerpt for each pair derived from the approved D9.15 contract.
        recorded=[]
        for i,row in enumerate(rows,1):
            evidence_name=f'{i:02d}_{row["surface_id"]}_{row["capability_id"]}.txt'
            evidence_path=evidence_root/evidence_name
            evidence_path.write_text(
                f'Windows GUI evidence fixture {i}\nsurface={row["surface_id"]}\ncapability={row["capability_id"]}\n'
                'observed_status=PASS\nrenderer_activation=false\nmedia_created=false\nrelease_authority=NONE\n',encoding='utf-8')
            result=module.record_event(
                tmp,surface=row['surface_id'],capability=row['capability_id'],
                action=f'Observed {row["surface_id"]} {row["capability_id"]} GUI route in Windows and inspected visible result',
                evidence_file=f'artifacts/evidence/d9_15_operator/{evidence_name}',
                observed_status='PASS',operator='test-operator',operator_attestation=ATTEST)
            assert result['status']=='RECORDED' and result['required_pairings']==13
            recorded.append(result)
        audit=module.inspect_ledger(tmp)
        assert audit['status']=='D9.15_OPERATOR_EVIDENCE_COMPLETE_CHECKPOINT_REQUIRED'
        assert audit['recorded_pass_pairings']==13 and audit['pending_pairings']==0 and audit['blocked_pairings']==0
        expect_error(lambda: module.finalize_acceptance(tmp,operator_attestation='yes'),'invalid finalize attestation'); negatives+=1
        finalized=module.finalize_acceptance(tmp,operator_attestation=FINAL_ATTEST)
        assert finalized['status']=='D9.15_OPERATOR_EVIDENCE_PASS_CLOSED' and finalized['pairings']=='13/13'
        ok,why=module.validate_acceptance_checkpoint(tmp,raise_on_error=False)
        assert ok,why
        audited=module.inspect_ledger(tmp)
        assert audited['status']=='D9.15_OPERATOR_EVIDENCE_PASS_CLOSED' and audited['freeze_eligible'] is False
        checkpoint=json.loads((tmp/module.CHECKPOINT_REL).read_text(encoding='utf-8'))
        assert checkpoint['d4_8']=='BLOCKED' and checkpoint['renderer_activation'] is False and checkpoint['media_created'] is False
        assert checkpoint['release_authority']=='NONE' and checkpoint['baseline_freeze_authorized'] is False
        # The candidate adjudicator may clear only the D9.15 evidence blocker after it verifies the checkpoint;
        # all independent real-media, full-acceptance, closure and approval blockers must remain.
        candidate_path=ROOT/'tools/c11d/baseline_candidate/d_baseline_candidate.py'
        candidate_spec=importlib.util.spec_from_file_location('d_candidate_audit_for_evidence_test',candidate_path)
        assert candidate_spec and candidate_spec.loader
        candidate_module=importlib.util.module_from_spec(candidate_spec); candidate_spec.loader.exec_module(candidate_module)
        candidate_blockers,candidate_gov=candidate_module._governance_and_closure(
            tmp, {'reconciled':True}, candidate_source_sha256='a'*64,
            manifest_sha256=module.EXPECTED_MANIFEST_SHA256)
        assert 'D9_15_OPERATOR_EVIDENCE_MATRIX_REQUIRED' not in candidate_blockers
        for required_blocker in ('D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED','D9_16_FULL_ACCEPTANCE_NOT_CLOSED','D9_17_CLOSURE_NO_GO','D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED','D_BASELINE_APPROVAL_NOT_RECORDED'):
            assert required_blocker in candidate_blockers, (required_blocker,candidate_blockers)
        assert candidate_gov['d9_15_operator_evidence_pass_closed'] is True
        expect_error(lambda: module.finalize_acceptance(tmp,operator_attestation=FINAL_ATTEST),'checkpoint overwrite'); negatives+=1
        # Evidence tampering is caught after the sealed record and checkpoint were written.
        victim=evidence_root/'01_c11c-config_configuration.txt'
        original=victim.read_text(encoding='utf-8'); victim.write_text(original+'TAMPERED',encoding='utf-8')
        expect_error(lambda: module.inspect_ledger(tmp),'evidence bytes changed after recording'); negatives+=1
        assert negatives==10, negatives
    print(f'C11-D D9.15 OPERATOR EVIDENCE RECORDER PASS | pairings=13/13 | negative={negatives}/10 | append_only_hash_chain=PASS | evidence_hash_recheck=PASS | d9_15_scope_only=true | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE')
    return 0

if __name__=='__main__': raise SystemExit(main())
