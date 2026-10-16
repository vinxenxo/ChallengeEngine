#!/usr/bin/env python3
"""Read-only source-pinned audit of shared timing/review inheritance for five Loop grammars."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

CONTRACT_REL = "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_V1.json"
SCHEMA_REL = "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_SCHEMA_V1.json"
EXPECTED_GRAMMARS = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
EXPECTED_POLICY_IDS = [
    "LOOP_DRILL_EDITORIAL_FIELD_WINDOW_V1", "UNIFIED_DELIVERY_TIMEBASE_V1",
    "UNIFIED_PRESENTATION_REGION_V1", "UNIFIED_AUDIO_MUSIC_DELIVERY_V1",
    "SOURCE_BOUND_TEMPORAL_PREVIEW_V1", "EDITORIAL_REVIEW_MANIFEST_V1",
    "UNIFIED_CONTENT_REVIEW_V1", "NEUTRAL_FRAME_PROGRAM_V1", "CANDIDATE_LOGICAL_COMPOSITION_V1",
]
LOCKS = "renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"

class AuditError(Exception): pass

def require(cond, msg):
    if not cond: raise AuditError(msg)

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def read_json(root: Path, rel: str):
    p=root/rel
    require(p.is_file(), f"Missing source: {rel}")
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc: raise AuditError(f"Invalid JSON {rel}: {exc}") from exc

def get_dotted(obj, dotted):
    cur=obj
    for part in dotted.split("."):
        require(isinstance(cur, dict) and part in cur, f"Missing approval field {dotted}")
        cur=cur[part]
    return cur

def audit(root: Path):
    c=read_json(root, CONTRACT_REL)
    schema=read_json(root, SCHEMA_REL)
    require(c.get("schema")=="C11-D-D10-VISUAL-LOOP-GEOMETRIC-TIMING-REVIEW-INHERITANCE-PROPOSAL-V1", "Unexpected contract schema id")
    require(c.get("status")=="PREPARATION_ONLY_SHARED_POLICY_INHERITANCE_PROPOSAL_NOT_APPROVAL_NOT_BINDING", "Contract status weakened or changed")
    require(schema.get("$schema")=="https://json-schema.org/draft/2020-12/schema", "Wrong JSON Schema draft")
    require(c.get("authority",{}).get("frozen_c11c_manifest_sha256")=="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953", "Frozen C11-C pin changed")

    pin_rows=c.get("source_lineage")
    require(isinstance(pin_rows,list) and len(pin_rows)==17, "Expected exactly 17 direct source pins")
    seen=set()
    for row in pin_rows:
        rel=row.get("path"); expected=row.get("sha256")
        require(isinstance(rel,str) and rel not in seen, f"Duplicate/invalid source path: {rel}")
        seen.add(rel)
        path=root/rel
        require(path.is_file(), f"Missing pinned source: {rel}")
        actual=sha256(path)
        require(actual==expected, f"Pinned source drift: {rel}; expected={expected}; actual={actual}")

    matrix=read_json(root,"definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_V2.json")
    gap=read_json(root,"definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_REQUEST_CHAIN_GAP_AUDIT_V1.json")
    rows=c.get("scope",{}).get("selector_rows")
    require(isinstance(rows,list) and len(rows)==5, "Must contain exactly five selector rows")
    matrix_rows=matrix.get("scope",{}).get("grammar_matrix",[])
    require([r.get("grammar_id") for r in matrix_rows]==EXPECTED_GRAMMARS, "Grammar IDs differ from matrix V2")
    require([r.get("grammar_index") for r in matrix_rows]==list(range(5)), "Grammar indices differ from matrix V2")
    require([r.get("grammar_id") for r in rows]==EXPECTED_GRAMMARS, "Selector rows do not match matrix V2 order")
    require([r.get("grammar_index") for r in rows]==list(range(5)), "Selector indices are not exact 0..4")

    prefs=c.get("shared_policy_refs")
    require(isinstance(prefs,list) and len(prefs)==9, "Expected nine shared policy refs")
    require([p.get("id") for p in prefs]==EXPECTED_POLICY_IDS, "Policy ref identity/order mismatch")
    expected_ids=set(EXPECTED_POLICY_IDS)
    for row in rows:
        require(row.get("inheritance_mode")=="PROPOSED_SHARED_POLICY_DEFAULT", "Selector inheritance status changed")
        require(row.get("policy_refs")==EXPECTED_POLICY_IDS, f"Shared policy reference set differs for {row.get('grammar_id')}")
        require(row.get("family_exception")=="NONE_DECLARED", "Implicit family exception detected")
        require(row.get("binding_state")=="CANONICAL_BINDING_NOT_ADMITTED_BY_THIS_CONTRACT", "Binding boundary weakened")
    require(c.get("scope",{}).get("family_exceptions")==[], "Unexpected family exception list")

    checked_policy_sources=0
    approval_assertions=0
    for ref in prefs:
        src=read_json(root,ref["path"])
        require(src.get("status")==ref.get("expected_status"), f"Policy status drift: {ref['id']}")
        actual=sha256(root/ref["path"])
        require(actual==ref.get("sha256"), f"Policy source hash drift: {ref['id']}")
        checked_policy_sources+=1
        for dotted, expected in ref.get("approval_assertions",{}).items():
            actual_value=get_dotted(src,dotted)
            require(actual_value is expected, f"Policy approval/state changed: {ref['id']} {dotted}={actual_value!r}")
            require(expected is False, f"Only explicit false approval controls are allowed in this proposal: {dotted}")
            approval_assertions+=1
        for dotted, expected in ref.get("expected_review_policy",{}).items():
            actual_value=get_dotted(src,"review_policy."+dotted)
            require(actual_value==expected, f"Review state changed: {ref['id']} {dotted}")

    bb=c.get("binding_boundary",{})
    sc=gap.get("scope",{})
    bound=sc.get("current_source_binding_grammar_ids")
    blocked=sc.get("current_blocked_grammar_ids")
    require(bound==["harmonic_membrane"], "Canonical V1 bound scope changed unexpectedly")
    require(blocked==EXPECTED_GRAMMARS[1:], "The four V1 blocked grammars changed unexpectedly")
    require(bb.get("currently_bound_grammars")==bound, "Contract binding summary differs from current gap audit")
    require(bb.get("currently_blocked_grammars")==blocked, "Contract blocked summary differs from current gap audit")
    require(bb.get("candidate_input_admissible") is False, "Candidate input became admissible outside canonical gate")

    ai=c.get("approval_state",{})
    required_false=["timing_review_inheritance_approved","canonical_request_selector_matrix_approved","exact_selector_payload_approved","shared_policy_approved","renderer_baseline_approved","renderer_baseline_frozen","d4_8_authorized"]
    for k in required_false: require(ai.get(k) is False, f"Governance lock weakened: {k}")
    require(ai.get("d9_14_full_acceptance")=="BLOCKED_AS_REQUIRED", "D9.14 gate changed")
    require(ai.get("d9_16_full_acceptance")=="BLOCKED_AS_REQUIRED", "D9.16 gate changed")
    require(ai.get("d9_17_closure")=="BLOCKED_NO_GO", "D9.17 gate changed")
    require(ai.get("d10")=="BLOCKED" and ai.get("release_authority")=="NONE", "D10/release state changed")
    eb=c.get("execution_boundary",{})
    for k in ["godot_invoked","request_persisted","payload_materialized","renderer_native_input_emitted","renderer_dispatch_invoked","media_created","c11c_source_mutation"]:
        require(eb.get(k) is False, f"Execution boundary weakened: {k}")
    require(eb.get("renderer")=="OFF", "Renderer must remain OFF")
    return {"selectors":len(rows),"shared_policy_refs":len(prefs),"policy_sources":checked_policy_sources,"source_pins":len(pin_rows),"approval_assertions_checked":approval_assertions,"approvals_granted":0,"canonical_bound":len(bound),"blocked_by_fixed_v1_scope":len(blocked),"candidate_input_admissible":False,"timing_review_inheritance_approved":False}

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args=ap.parse_args(argv)
    try:
        s=audit(Path(args.root).resolve())
        print("C11-D VISUAL LOOP TIMING/REVIEW INHERITANCE AUDIT PASS | selectors={selectors}/5 | shared_policy_refs={shared_policy_refs}/9 | policy_sources={policy_sources}/9 | source_pins={source_pins}/17 | approval_assertions_checked={approval_assertions_checked} | approvals_granted=0 | canonical_bound={canonical_bound}/5 | blocked_by_fixed_v1_scope={blocked_by_fixed_v1_scope}/4 | candidate_input_admissible=false | timing_review_inheritance_approved=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE".format(**s))
        print("C11D_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_AUDIT="+json.dumps({"schema":"C11D-VISUAL-LOOP-TIMING-REVIEW-INHERITANCE-AUDIT-REPORT-V1","schema_version":"1.0","status":"PASS_PREPARATION_ONLY_SHARED_POLICY_INHERITANCE_VERIFIED_NOT_APPROVED_NOT_BINDING",**s,"renderer":"OFF","media_created":False,"d4_8":"BLOCKED","release_authority":"NONE"},sort_keys=True,separators=(",",":")))
        return 0
    except (AuditError, OSError, ValueError, KeyError) as exc:
        print(f"C11-D VISUAL LOOP TIMING/REVIEW INHERITANCE AUDIT FAIL | {exc} | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1
if __name__=="__main__": sys.exit(main())
