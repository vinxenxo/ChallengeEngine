from __future__ import annotations
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import full_acceptance as fa

def expect(ok: bool, msg: str):
    if not ok: raise AssertionError(msg)

def main() -> int:
    record=fa.build_full_acceptance_preflight(ROOT)
    expect(record["status"]=="PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED",json.dumps(record.get("errors",[]),ensure_ascii=False))
    validation=fa.validate_full_acceptance_preflight(record,ROOT)
    expect(validation["valid"] is True and validation["full_acceptance_closed"] is False,"D9.16 validator result mismatch")
    expect(record["case_count"]==9 and record["check_count"]==5,"D9.16 count mismatch")
    expect(all(x["registered"] for x in record["cases"]),"one or more D9.8-D9.16 evidence routes are missing")
    expected_d915 = "PASS_CLOSED" if record["operator_evidence"]["status"] == "PASS_CLOSED" else "REQUIRED"
    expect(record["d9_14_gate_status"]=="BLOCKED" and record["d9_15_operator_status"]==expected_d915,"D9.14/D9.15 state did not match current validated checkpoints")
    expect(record["operator_evidence"]["five_surface_evidence_recorded"] is (expected_d915 == "PASS_CLOSED"), "D9.15 evidence was not bound to the accepted checkpoint")
    expect(record["governance"]["renderer_activation"] is False and record["governance"]["media_created"] is False and record["governance"]["d4_8"]=="BLOCKED" and record["governance"]["release_authority"]=="NONE","governance drift")
    negative=0
    def reject(label,mutate,reseal=True):
        nonlocal negative
        candidate=copy.deepcopy(record); mutate(candidate)
        if reseal: candidate=fa._seal(candidate)
        try: fa.validate_full_acceptance_preflight(candidate,ROOT)
        except fa.FullAcceptanceError: negative+=1
        else: raise AssertionError(f"D9.16 negative unexpectedly accepted: {label}")
    reject("claim full acceptance",lambda x:x.update(full_acceptance_status="PASS",full_acceptance_closed=True))
    reject("claim operator evidence",lambda x:x["operator_evidence"].update(five_surface_evidence_recorded=True,evidence_ref="artifacts/fake.png"))
    reject("unlock D9.14",lambda x:x.update(d9_14_gate_status="AUTHORIZED"))
    reject("forge D9.15 GUI evidence state",lambda x:x.update(d9_15_operator_status=("REQUIRED" if expected_d915 == "PASS_CLOSED" else "PASS_CLOSED")))
    reject("renderer activated",lambda x:x["governance"].update(renderer_activation=True))
    reject("renderer input emitted",lambda x:x["governance"].update(renderer_input_emitted=True))
    reject("production executed",lambda x:x["governance"].update(production_execution=True))
    reject("media created",lambda x:x["governance"].update(media_created=True))
    reject("D4.8 unblocked",lambda x:x["governance"].update(d4_8="AUTHORIZED"))
    reject("release authority granted",lambda x:x["governance"].update(release_authority="GRANTED"))
    reject("master seed adopted",lambda x:x["governance"].update(master_seed="ADOPTED"))
    reject("cross-domain sharing",lambda x:x["governance"].update(cross_domain_seed_sharing="ALLOWED"))
    reject("longform enabled",lambda x:x["governance"].update(longform="SUPPORTED"))
    reject("alter freeze manifest reference",lambda x:x["references"].update(historical_c11c_manifest_sha256="0"*64))
    reject("drop evidence case",lambda x:x.update(cases=x["cases"][:-1],case_count=8))
    reject("add sixth surface claim",lambda x:x["checks"][0].update(actual_surface_count=6))
    reject("write evidence side effect",lambda x:x["side_effects"].update(files_written=True))
    reject("create release side effect",lambda x:x["side_effects"].update(release_created=True))
    reject("missing blocker",lambda x:x.update(blockers=[]))
    reject("preflight status promoted",lambda x:x.update(status="PASS",static_preflight_pass=True))
    reject("raw seal tamper",lambda x:x.update(full_acceptance_closed=True),reseal=False)
    expect(negative==21,f"negative controls mismatch: {negative}/20")
    print(f"C11-D D9.16 FULL ACCEPTANCE PREFLIGHT PASS | static_checks=5/5 | evidence_routes=9/9 | negative={negative}/21 | full_acceptance=BLOCKED_AS_REQUIRED | D9.14=BLOCKED | D9.15_operator_evidence={record['d9_15_operator_status']} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0
if __name__=="__main__": raise SystemExit(main())
