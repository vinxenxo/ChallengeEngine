#!/usr/bin/env python3
"""C11-E E6 Smoke18 read-only source/evidence audit. Never launches media tools."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
POLICY_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"

SOURCE_PINS = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": FROZEN_SHA,
    "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json": POLICY_SHA,
    "definitions/c11d/production/C11E_E4B_LOOP22_SELECTOR_MATRIX_V1.json": "eb0ce2fab5ee97c298e232685ec3452779fc1e1f4a8dcd1c9c994bff1a45a1a1",
    "profiles/presentation/c11c_visual_music_profiles.json": "b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58",
    "challenges/CHALLENGE_001.json": "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea",
    "challenges/CHALLENGE_002.json": "db5d70a28c460e986e785c6787447529372ac5ea3b5a7ff0507667decbe2a160",
    "challenges/CHALLENGE_003.json": "38cb0166482c5ba4862deef8ab75dad4a6e1524590b6850312bab5238f078419",
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "challenges/CHALLENGE_005.json": "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30",
    "challenges/CHALLENGE_006.json": "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694",
    "challenges/CHALLENGE_007.json": "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61",
    "definitions/visual_loop_fractal_canonical.json": "80eb24280db77a6dc8e3b6477b84370ec574d6e8f1728e6c69c59707b9868d15",
    "definitions/visual_loop_geometric_canonical.json": "648eb36225dd4c090457b4da3c9e8eca218c26c8f995cf02a39914cf3f860dcc",
    "definitions/visual_loop_kaleidoscope_canonical.json": "a32152d4ee04bedf6308a718d3160ddf65c1808d13fa1e05087e5488cd81378f",
    "definitions/visual_loop_particle_flow_canonical.json": "2a5293512d83cb1b7783a21dcaeda809331a1f34647e8872c3849aa52effacfd",
    "definitions/visual_loop_vector_field_canonical.json": "bb8cbe569e62e8554479b2900fa9c8aebe5a30000b9abfcadcd13e65e56d3482",
    "definitions/visual_drill_tracking_canonical.json": "54d432c80f190f4ac5dcb8ef5b135e16f18c378da120f35723fd5be944719ec3",
    "definitions/visual_drill_pursuit_canonical.json": "dfe2bce9913df8ebe4f92d06eec5d22736338214e71b497dde3562a6927600bc",
    "definitions/visual_drill_saccade_canonical.json": "daba3fa558f6898a17107ab68894d15c58fa5b2127e8da7d7b11b203f4ddfaa1",
    "definitions/visual_drill_peripheral_scan_canonical.json": "aaf50f9223bad678df15589110dfcd6ff42dda89326a0a84bc5a5f51d133a904",
    "tools/c11d/d9/c11e_e4a_challenge_av_review.py": "a31083dcad457b2621610ae68d180a9797cdeb12537a300150e53ec880ee06de",
    "tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py": "9ea0219f681a912760de3bcdf2469f8a3812a7afe7fb3f5ac569664f354ac18e",
    "tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd": "eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203",
    "c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py": "46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d",
    "c11c-suite/c11c-producer/c11e_e3_audio_pilot.py": "06abd7a9f8c99382366f3720b93601e4e76b80861b4f54ce554acab11571209f",
    "tools/c11d/d9/c11e_e4b_loop22_av_qualification_v2.py": "9da24610922bb0c0a8694da743ae383386e86e3926d592b550b6ba6f5b1787c9",
    "tools/c11d/d9/c11e_e4b_loop22_av_support_v1.py": "4f79a33f063dc22e350fc707f82b572ed1007bb14d36b0c6d49b6fd511a0e6e1",
    "tools/c11d/d9/c11e_r1v_five_family_qualification.py": "9d1baba14ca8cf96e3f2f466cedc104ec4b9cf1b94ef4b11690abe7a6de9e019",
    "tools/c11d/d9/c11e_e4c_drill_execution.py": "b7cbf7bd97f76f4c2e339840fc694d3f5b0e50186ba2456e45ff00e585751abe",
    "tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py": "d5cd8e24c0cfdd83ec035b006c76468ed637d6babf5f0a9fcca8a93817ba1aa8",
    "docs/history/c11e/C11E_E4B_LOOP22_OPERATOR_ACCEPTANCE_CLOSEOUT_20261109_V2.md": "f9a09d34d04ea4bd92eb70cf3668b9da093542f8a94c0a391861805f841d1dd3",
    "docs/history/c11e/C11E_R1V_AV_QUALIFICATION_CLOSEOUT_20261109_V2.md": "e86525d3ddacb572c106e49191388cc3afb65549007b8d713613f370fdb6e65b",
    "artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json": "a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a",
    "artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_report.json": "85de2645621acd6f8183508e0da9b5466b8a00cf9d2cb340a170f7d2803285ba",
    "artifacts/tests/c11e/r1v_geometric_av_reuse_qualification/GEOAVR2_224356_841F9B/GEO_AV_REUSE_MUX_REPORT_V1.json": "15712f3187237f118df05c0c013558c65b2a2f7d342a0e765da8307e7a7ff037",
    "artifacts/tests/c11e/e4b_loop22_av/L22_191801_27ABF3/loop22_av_report.json": "d8f7050f952b7248b24763abde20ce52bf812c3934738f14670a0a3dc0c72068",
    "artifacts/tests/c11e/e4b_loop22_av/L22_191801_27ABF3/loop22_av_process_receipt.json": "37ee99f8ab30eb445c9ca462471152b6fadc850471b8a27f7c59f30714ec2f5d",
    "artifacts/tests/c11e/e4b_loop22_av/L22_191801_27ABF3/loop22_run_manifest.json": "170b869b604eae0fdecf770c395e379554ae4ee05bbe579a560180a725fe396f",
    "artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json": "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0",
    "artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_REPORT.json": "efb0f1a9245d3fce15bf48041c8972e90f6874d308fa99340afb5c731f94403a",
    "docs/current/e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_PLAN_20261106_V3.md": "cb498f260f8f1ab5a1165b29ae5c372bb975c4563abbde49b022d140d000a831",
    "docs/current/e/C11E_E4C_PURSUIT_FAMILY_CLOSEOUT_20261116_V1.md": "7f06694ea3980e34868027fb607fdf918c07f03b75e9ef82e8630a9d7814c534",
    "docs/current/e/C11E_E4C_SACCADE_FAMILY_CLOSEOUT_20261116_V5.md": "9a5ad358f0bf9afb6c24c8cebb076c51981bf15bf855373b0fa54637e937cb8c",
    "artifacts/production/c11e/E4C-TRK-T2-6239dd21/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json": "f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7",
    "artifacts/production/c11e/E4C-PRS-T1-b3abbe94/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json": "57206b4560b917c7a7fe5e738c5afd5d900d293e01c99fcd554f0926acc6eee7",
    "artifacts/production/c11e/E4C-SAC-T1-57fdf44b/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json": "930ba103153fbca0226a0b7abd1226b46dfd3c2e523204e83e6cb39f1282e606",
    "artifacts/production/c11e/E4C-PSC-T1-b342a227/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json": "eb290666163df0e89daac9c683a95a39c38d536c5da735def15cd3a19964083b",
    "artifacts/production/c11e/E4C-TRK-T5-6239dd21/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json": "6e55dc3fd4fc13745347cc641d29103fbfb7fa90dee932910f920703690c3c61",
    "artifacts/production/c11e/E4C-PSC-T5-b342a227/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json": "5644ffa386c2d1388e7dd657cb566c796a87de93b22c28db84197dbb8ad3a224",
    "docs/current/e/C11E_E4C_PERIPHERAL_SCAN_FAMILY_CLOSEOUT_20261116_V1.md": "88f0a7e2c34dc16d490ace9192766eb6801119649ccc1b05210de894436a3183",
}

E6_DOC_PINS = {
    "docs/current/e/C11E_CURRENT_AUTHORITY_20261116_V175.md": "2ec87d22d373275d97ef7f84d1917c42041b3deb9a9cbd73b10a55bf3b5dff8c",
    "docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261116_V170.md": "ec53cd188ac2453ed37698a258b1492606e9abebded0dcb590ccf26ecc691008",
    "docs/current/e/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261116_V116.md": "3e04ce6323c6260f2899153855b9238b1eca386ca4520cbb3cd72d810d25f3ba",
    "docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261116_V146.md": "32db857d4eb9ae63c4f070064b6431f2b484e6d797908727e34945fb60a93653",
    "docs/current/e/C11E_E5_FULL_PHASE_CLOSEOUT_20261116_V1.md": "c19b3b9994bd6d03ee5b00459b663262a9e1b4300ab70859e793e80577e3a9b1",
    "docs/current/e/C11E_E6_SMOKE18_SCOPE_PLAN_20261116_V1.md": "30651efa7a79f3b322db244129ddccd4ddbb46e800e62ae3743af8805fd47f8e",
    "docs/current/e/C11E_E6_SMOKE18_TEST_ONLY_AUTHORIZATION_PROPOSAL_20261116_V1.md": "fa198d8bd20fe72f99c6593f51a5d17bc7d29441fbb6c62ba4eeecf1c7fc12e8",
    "docs/master-prompts/C11E_MASTER_HANDOVER_20261116_V2.md": "39bf9fce35f2eaa5ad02907eb46b609d815383abaede3f0e4318c473b9734834",
    "prompts/C11E_CONTINUATION_MASTER_PROMPT_20261116_V177.md": "9398f3478c6813b84a2ca56723f999adfa6ebda78a72deca19a40cc799e30e45",
    "prompts/C11E_NEXT_WINDOW_START_PROMPT_20261116_V177.md": "ec179418847fec57ae5db572617c33a9b5cfd7baddc2346ca45b5bd2c4bd5d78",
    "prompts/C11E_FIRST_PROMPT_20261116_V101.md": "7c866181f979acfee6f5a652051c018e49eb9f5d7a1e3a5a0ea4ff8d7019dcc1",
}

DRILL_CANDIDATES = [
    {"family":"tracking","selector":"tier-2","path":"artifacts/production/c11e/E4C-TRK-T2-6239dd21/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json","sha256":"f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7"},
    {"family":"pursuit","selector":"tier-1","path":"artifacts/production/c11e/E4C-PRS-T1-b3abbe94/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json","sha256":"57206b4560b917c7a7fe5e738c5afd5d900d293e01c99fcd554f0926acc6eee7"},
    {"family":"saccade","selector":"tier-1","path":"artifacts/production/c11e/E4C-SAC-T1-57fdf44b/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json","sha256":"930ba103153fbca0226a0b7abd1226b46dfd3c2e523204e83e6cb39f1282e606"},
    {"family":"peripheral_scan","selector":"tier-1","path":"artifacts/production/c11e/E4C-PSC-T1-b342a227/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json","sha256":"eb290666163df0e89daac9c683a95a39c38d536c5da735def15cd3a19964083b"},
    {"family":"tracking","selector":"tier-5","path":"artifacts/production/c11e/E4C-TRK-T5-6239dd21/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json","sha256":"6e55dc3fd4fc13745347cc641d29103fbfb7fa90dee932910f920703690c3c61"},
    {"family":"peripheral_scan","selector":"tier-5","path":"artifacts/production/c11e/E4C-PSC-T5-b342a227/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json","sha256":"5644ffa386c2d1388e7dd657cb566c796a87de93b22c28db84197dbb8ad3a224"},
]

LOOP_CANDIDATES = [
    {"family_id":"c11c_fractal_bloom_v1","grammar_id":"radial_bloom","gameplay_seed":100006,"music_seed":500006,"fps":30,"duration_seconds":22.0,"evidence":"R1V accepted five-family A/B + human closeout"},
    {"family_id":"c11c_geometric_waves_v1","grammar_id":"harmonic_membrane","gameplay_seed":100001,"music_seed":500001,"fps":30,"duration_seconds":23.0,"evidence":"R1V corrected GEOAVR2 A/B + human closeout"},
    {"family_id":"c11c_invisible_forces_v1","grammar_id":"dipole_field","gameplay_seed":100021,"music_seed":500021,"fps":30,"duration_seconds":22.0,"evidence":"R1V accepted five-family A/B + human closeout"},
    {"family_id":"c11c_living_particles_v1","grammar_id":"swarm","gameplay_seed":100016,"music_seed":500016,"fps":30,"duration_seconds":20.0,"evidence":"R1V accepted five-family A/B + human closeout"},
    {"family_id":"c11c_sacred_symmetry_v1","grammar_id":"astrolabe","gameplay_seed":100011,"music_seed":500011,"fps":30,"duration_seconds":23.0,"evidence":"R1V accepted five-family A/B + human closeout"},
    {"family_id":"c11c_geometric_waves_v1","grammar_id":"interference_plane","gameplay_seed":100002,"music_seed":500002,"fps":30,"duration_seconds":23.0,"evidence":"E4B Loop22 44-output A/B + human closeout"},
]

CHALLENGE_PATHS = [f"challenges/CHALLENGE_{i:03d}.json" for i in range(1, 8)]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value

def check_pins(root: Path, pins: dict[str, str]) -> dict[str, Any]:
    rows=[]
    for rel, expected in pins.items():
        path=root / Path(rel)
        if not path.is_file():
            rows.append({"path":rel,"status":"MISSING","expected_sha256":expected,"actual_sha256":None})
            continue
        actual=sha256_file(path)
        rows.append({"path":rel,"status":"PASS" if actual==expected else "MISMATCH","expected_sha256":expected,"actual_sha256":actual,"bytes":path.stat().st_size})
    return {"expected":len(pins),"passed":sum(x["status"]=="PASS" for x in rows),"failed":sum(x["status"]!="PASS" for x in rows),"rows":rows}

def evaluate_policy(policy: dict[str, Any]) -> dict[str, Any]:
    forbidden=policy.get("forbidden",{})
    allowances=policy.get("allowances",{})
    valid=(policy.get("status")=="APPROVED_BOUNDED_R1V_QUALIFICATION_ONLY"
           and policy.get("execution",{}).get("launcher_invocations_exact")==10
           and policy.get("scope",{}).get("allowed_selector_count")==5
           and forbidden.get("smoke18_or_matrix99") is True
           and forbidden.get("d3_music_engine") is True
           and forbidden.get("pcm_audio_generation") is True
           and forbidden.get("ffmpeg_filter_or_mux") is True
           and allowances.get("audio_or_music_generation") is False
           and allowances.get("ffmpeg_mux") is False
           and policy.get("authority_boundary",{}).get("general_d4_8_production")=="BLOCKED")
    return {"status":"PINNED_R1V_ONLY_E6_PROHIBITED" if valid else "POLICY_CONTRACT_MISMATCH","valid":valid,"policy_id":policy.get("policy_id"),"launcher_invocations":policy.get("execution",{}).get("launcher_invocations_exact"),"selector_count":policy.get("scope",{}).get("allowed_selector_count"),"smoke18_forbidden":forbidden.get("smoke18_or_matrix99"),"d3_forbidden":forbidden.get("d3_music_engine"),"audio_forbidden":forbidden.get("pcm_audio_generation"),"ffmpeg_mux_forbidden":forbidden.get("ffmpeg_filter_or_mux")}

def evaluate_r1v(root: Path) -> dict[str, Any]:
    receipt=load_json(root/"artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json")
    report=load_json(root/"artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_report.json")
    geo=load_json(root/"artifacts/tests/c11e/r1v_geometric_av_reuse_qualification/GEOAVR2_224356_841F9B/GEO_AV_REUSE_MUX_REPORT_V1.json")
    slots=receipt.get("slots",[])
    visual=sum(s.get("visual_status") in ("OPERATOR_CONFIRMED_PASS","OPERATOR_CONFIRMED_AV_PASS") for s in slots)
    audio=sum(s.get("audio_status") in ("OPERATOR_CONFIRMED_PASS","OPERATOR_CONFIRMED_AV_PASS") for s in slots)
    closeout=(root/"docs/history/c11e/C11E_R1V_AV_QUALIFICATION_CLOSEOUT_20261109_V2.md").read_text(encoding="utf-8")
    output_rows=report.get("audiovisual_outputs",[])
    observed={(x.get("family_id"),x.get("grammar_id"),x.get("gameplay_seed"),x.get("music_seed")) for x in output_rows}
    required={(x["family_id"],x["grammar_id"],x["gameplay_seed"],x["music_seed"]) for x in LOOP_CANDIDATES[:5]}
    candidates_match=required.issubset(observed) and len(output_rows)==10
    geo_ok=(geo.get("status")=="PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE" and geo.get("family_id")=="c11c_geometric_waves_v1" and geo.get("grammar_id")=="harmonic_membrane" and len(geo.get("slots",[]))==2)
    receipt_lineage=(receipt.get("technical_evidence",{}).get("original_report_sha256")==sha256_file(root/"artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_report.json") and receipt.get("technical_evidence",{}).get("geo_replacement_report_sha256")==sha256_file(root/"artifacts/tests/c11e/r1v_geometric_av_reuse_qualification/GEOAVR2_224356_841F9B/GEO_AV_REUSE_MUX_REPORT_V1.json"))
    valid=(receipt.get("status")=="PASS_TEST_ONLY_OPERATOR_ACCEPTED" and len(slots)==10 and visual==10 and audio==10 and "CLOSED_PASS_TEST_ONLY_OPERATOR_ACCEPTED" in closeout and "GEOAVR2" in closeout and candidates_match and geo_ok and receipt_lineage)
    return {"status":"PASS_HUMAN_CLOSEOUT_10_OF_10" if valid else "CLOSEOUT_EVIDENCE_MISMATCH","valid":valid,"technical_slots":len(output_rows),"visual_pass":visual,"audio_pass":audio,"five_loop_candidate_pairs_present":candidates_match,"geometric_replacement_pass":geo_ok,"historical_original_report_status":report.get("status"),"historical_failure_preserved":True,"geometric_replacement_documented":"GEOAVR2" in closeout,"receipt_sha256":sha256_file(root/"artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json"),"technical_report_sha256":sha256_file(root/"artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_report.json"),"geometric_replacement_report_sha256":sha256_file(root/"artifacts/tests/c11e/r1v_geometric_av_reuse_qualification/GEOAVR2_224356_841F9B/GEO_AV_REUSE_MUX_REPORT_V1.json")}

def evaluate_loop22(root: Path) -> dict[str, Any]:
    base=root/"artifacts/tests/c11e/e4b_loop22_av/L22_191801_27ABF3"
    report=load_json(base/"loop22_av_report.json")
    receipt=load_json(base/"loop22_av_process_receipt.json")
    manifest=load_json(base/"loop22_run_manifest.json")
    matrix=load_json(root/"definitions/c11d/production/C11E_E4B_LOOP22_SELECTOR_MATRIX_V1.json")
    closeout=(root/"docs/history/c11e/C11E_E4B_LOOP22_OPERATOR_ACCEPTANCE_CLOSEOUT_20261109_V2.md").read_text(encoding="utf-8")
    outputs=report.get("audiovisual_outputs",[])
    jobs=manifest.get("jobs",[])
    matrix_rows=matrix.get("selectors",[])
    loop6=LOOP_CANDIDATES[5]
    matrix_match=any(x.get("family_id")==loop6["family_id"] and x.get("grammar_id")==loop6["grammar_id"] and x.get("gameplay_seed")==loop6["gameplay_seed"] and x.get("music_seed")==loop6["music_seed"] for x in matrix_rows)
    jobs_match=sum(1 for x in jobs if x.get("family_id")==loop6["family_id"] and x.get("grammar_id")==loop6["grammar_id"] and x.get("gameplay_seed")==loop6["gameplay_seed"] and x.get("music_seed")==loop6["music_seed"])==2
    report_sha=sha256_file(base/"loop22_av_report.json")
    valid=(report.get("status")=="PASS_E4B_LOOP22_AV_QUALIFICATION_44_OF_44_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW"
           and receipt.get("status")==report.get("status") and receipt.get("report_sha256")==report_sha
           and len(outputs)==44 and len(jobs)==44 and matrix_match and jobs_match
           and "CLOSED_PASS_OPERATOR_ACCEPTED" in closeout
           and "44 visual and audio outputs pass" in closeout and "22/22 A/B pairs" in closeout)
    return {"status":"PASS_HUMAN_CLOSEOUT_44_OF_44" if valid else "CLOSEOUT_EVIDENCE_MISMATCH","valid":valid,"technical_outputs":len(outputs),"launcher_jobs":len(jobs),"ab_pairs":22 if valid else None,"interference_plane_matrix_match":matrix_match,"interference_plane_A_B_jobs_match":jobs_match,"operator_human_acceptance":"PASS" if valid else "UNVERIFIED","report_sha256":report_sha,"process_receipt_sha256":sha256_file(base/"loop22_av_process_receipt.json"),"run_manifest_sha256":sha256_file(base/"loop22_run_manifest.json")}

def evaluate_challenge(root: Path) -> dict[str, Any]:
    selectors=[]
    for rel in CHALLENGE_PATHS:
        obj=load_json(root/rel)
        selectors.append({"challenge_id":obj.get("challenge_id"),"mechanic":obj.get("mechanic"),"gameplay_seed":obj.get("generation",{}).get("seed"),"fps":obj.get("video",{}).get("fps"),"declared_duration_seconds":sum(float(obj.get("video",{}).get(k,0) or 0) for k in ("hook_duration","game_duration","reveal_duration","cta_duration")),"source_path":rel})
    receipt=load_json(root/"artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json")
    plan=(root/"docs/current/e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_PLAN_20261106_V3.md").read_text(encoding="utf-8")
    e1=receipt.get("e1_intents",{})
    e1_ok=(len(e1)==3 and all(v.get("validation_status")=="PASS_E1_PREPARATION_ONLY" and v.get("request_origin")=="TEST" for v in e1.values()))
    one_selector=(receipt.get("status")=="PASS_ISOLATED_E4A7_D_COMPOSITED_CHALLENGE_AV_TEST_ONLY" and "ISOLATED_CHALLENGE_004" in receipt.get("scope","") and "CHALLENGE_004" in plan and e1_ok and receipt.get("production_dispatch") is False and receipt.get("release_authority")=="NONE")
    return {"candidate_pool_count":len(selectors),"candidate_pool":selectors,"accepted_av_selector":"CHALLENGE_004" if one_selector else None,"accepted_av_receipt_sha256":sha256_file(root/"artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json"),"six_selector_matrix_frozen":False,"music_seed_authority_for_other_candidates":"NOT_PRESENT_IN_E4A7_ACCEPTANCE_RECEIPT_OR_CHALLENGE_CANONICAL_DEFINITIONS","multi_selector_d_owned_av_executor":"NOT_PROVEN_BY_CURRENT_E4A7_SCOPE","status":"ONE_ACCEPTED_SELECTOR_ONLY_6_OF_7_POOL_UNRESOLVED" if one_selector else "CHALLENGE_EVIDENCE_MISMATCH"}

def evaluate_drill(root: Path) -> dict[str, Any]:
    rows=[]
    expected_profiles={"tracking":"FLOWING_VECTOR","pursuit":"ORGANIC_BLOOM","saccade":"CIRCUIT_PULSE","peripheral_scan":"ORBITAL_RITUAL"}
    for item in DRILL_CANDIDATES:
        path=root/item["path"]
        obj=load_json(path)
        actual=sha256_file(path)
        ok=(actual==item["sha256"] and obj.get("status")=="PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION" and obj.get("family")==item["family"] and obj.get("tier")==int(item["selector"].split("-")[1]) and obj.get("gameplay_seed")==12345 and obj.get("music_seed_a")==840001 and obj.get("music_seed_b")==840001 and obj.get("music_seed_c_changed")==840002 and obj.get("family_music_profile")==expected_profiles[item["family"]] and obj.get("delivery_profile")=="REVIEW_720" and obj.get("audio_generated") is True and obj.get("d_postcomposition") is True and obj.get("ffmpeg_decode_encode_mux") is True and obj.get("source_pin_count")==91 and obj.get("c11c_manifest_sha256")==FROZEN_SHA and obj.get("source_pins_pre_post_equal") is True and obj.get("production_dispatch") is False and obj.get("production_release") is False and obj.get("release_authority")=="NONE")
        rows.append({"family":item["family"],"selector":item["selector"],"path":item["path"],"sha256":actual,"status":"PASS" if ok else "MISMATCH","gameplay_seed":obj.get("gameplay_seed"),"music_seed_A_B":obj.get("music_seed_a"),"music_seed_C":obj.get("music_seed_c_changed"),"family_music_profile":obj.get("family_music_profile"),"audio_generated":obj.get("audio_generated"),"operator_closeout_reference":"E4C 20/20 family closeouts"})
    latest_family_closeout=(root/"docs/current/e/C11E_E4C_PERIPHERAL_SCAN_FAMILY_CLOSEOUT_20261116_V1.md").read_text(encoding="utf-8")
    global_20_of_20=("E4C is now 20/20 accepted and CLOSED" in latest_family_closeout)
    all_ok=len(rows)==6 and all(x["status"]=="PASS" for x in rows) and global_20_of_20
    return {"status":"PASS_PRIOR_E4C_EVIDENCE_6_OF_6" if all_ok else "DRILL_EVIDENCE_MISMATCH","valid":all_ok,"accepted_receipts":sum(x["status"]=="PASS" for x in rows),"global_e4c_closeout_20_of_20":global_20_of_20,"rows":rows,"reuse_requires_explicit_E6_contract":True}

def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+"."+uuid.uuid4().hex[:8]+".tmp")
    with temp.open("xb") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(temp,path)

def run_audit(root: Path) -> dict[str, Any]:
    root=root.resolve()
    if not root.is_dir(): raise FileNotFoundError(f"Project root not found: {root}")
    pins=check_pins(root,SOURCE_PINS)
    docs=check_pins(root,E6_DOC_PINS)
    frozen_ok=(pins["rows"][0]["status"]=="PASS")
    policy_path=root/"definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
    policy=evaluate_policy(load_json(policy_path)) if policy_path.is_file() else {"valid":False,"status":"MISSING"}
    r1v=evaluate_r1v(root)
    loop=evaluate_loop22(root)
    challenge=evaluate_challenge(root)
    drill=evaluate_drill(root)
    e6_output_root=root/"artifacts/tests/c11e/e6_smoke18"
    output_collision=e6_output_root.exists()
    blockers=[]
    if pins["failed"]: blockers.append("SOURCE_PIN_MISMATCH_OR_MISSING")
    if docs["failed"]: blockers.append("E5_E6_BASELINE_DOC_PIN_MISMATCH_OR_MISSING")
    if not frozen_ok: blockers.append("FROZEN_C11C_MANIFEST_MISMATCH")
    if not policy.get("valid"): blockers.append("D4_8_POLICY_PIN_OR_CONTRACT_MISMATCH")
    if not r1v.get("valid"): blockers.append("R1V_HUMAN_CLOSEOUT_NOT_VERIFIED")
    if not loop.get("valid"): blockers.append("LOOP22_HUMAN_CLOSEOUT_NOT_VERIFIED")
    if not drill.get("valid"): blockers.append("DRILL_PRIOR_EVIDENCE_NOT_VERIFIED")
    if challenge.get("accepted_av_selector")!="CHALLENGE_004": blockers.append("CHALLENGE_E4A_AV_EVIDENCE_MISMATCH")
    blockers.extend(["CHALLENGE_SIX_SELECTOR_SET_NOT_FROZEN_FROM_SEVEN_CANDIDATES","CHALLENGE_MUSIC_SEED_DOMAIN_NOT_AUTHORIZED_FOR_FIVE_ADDITIONAL_SELECTORS","CHALLENGE_MULTI_SELECTOR_D_OWNED_AV_EXECUTOR_NOT_PROVEN","SEPARATE_E6_TEST_ONLY_AUTHORIZATION_REQUIRED_D4_8_V2_PROHIBITS_SMOKE18_AUDIO_AND_MUX"])
    if output_collision: blockers.append("E6_OUTPUT_ROOT_ALREADY_EXISTS_REVIEW_DO_NOT_OVERWRITE")
    status="PASS_AUDIT_READ_ONLY_EVIDENCE_RECONCILED_EXECUTION_HELD" if not (pins["failed"] or docs["failed"] or not frozen_ok or not policy.get("valid") or not r1v.get("valid") or not loop.get("valid") or not drill.get("valid") or output_collision) else "FAIL_CLOSED_AUDIT_INPUT_OR_EVIDENCE_MISMATCH"
    now=datetime.now(timezone.utc)
    run_id="E6AUDIT_"+now.strftime("%Y%m%dT%H%M%SZ_")+uuid.uuid4().hex[:8].upper()
    report={"schema":"C11E-E6-SMOKE18-READONLY-AUDIT-RECEIPT-V1","status":status,"run_id":run_id,"created_utc":now.isoformat(),"project_root":str(root),"scope":"READ_ONLY_SELECTOR_SOURCE_EVIDENCE_AUDIT_NO_MEDIA_NO_RESERVATION","source_pins":pins,"baseline_document_pins":docs,"frozen_c11c_manifest_sha256":FROZEN_SHA,"d4_8_policy":policy,"prior_evidence":{"r1v":r1v,"loop22":loop,"challenge":challenge,"drill":drill},"candidate_reuse_summary":{"visual_loop_candidates":6,"visual_loop_prior_human_accepted":6,"visual_drill_candidates":6,"visual_drill_prior_technical_receipts":6,"challenge_candidate_pool":challenge["candidate_pool_count"],"challenge_prior_av_accepted":1,"loop_and_drill_prior_reuse":12,"challenge_CH004_additional_reuse_if_selected":1,"total_potential_reuse_if_CH004_is_selected":13,"challenge_additional_av_cases_required_if_CH004_is_selected":5},"e6_matrix":{"target_scenarios":18,"per_family":6,"challenge":"NOT_FROZEN","visual_loop":"PROPOSED_6_CANDIDATES_REUSE_SUBJECT_TO_E6_CONTRACT","visual_drill":"PROPOSED_6_CANDIDATES_REUSE_SUBJECT_TO_E6_CONTRACT","frozen":False},"execution":{"e6_test_only_authorized":False,"media_invoked":False,"renderer_invoked":False,"godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"audio_generated":False,"mux_invoked":False,"production_dispatch":False,"release_authority":"NONE","new_batch_id_consumed":False,"e6_output_root_preexisting":output_collision},"blockers":blockers,"next_required_work":["Resolve and pin the six Challenge selectors; CHALLENGE_008/009 remain excluded.","Define the Challenge request.music_seed values and duration/timebase mapping without changing gameplay seeds.","Prove a single family-owned Challenge D composition/A/V route for the selected six selectors; do not add a parallel renderer or alter C11-C.","Freeze an exact 18-row E6 manifest with reuse rules for accepted Loop/Drill evidence.","Publish separate E6 TEST_ONLY authorization and obtain explicit operator/governance approval before any media invocation."]}
    evidence=root/"artifacts/tests/c11e/e6_smoke18_audit"/run_id
    if evidence.exists(): raise FileExistsError(f"Evidence output already exists: {evidence}")
    payload=(json.dumps(report,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
    atomic_write(evidence/"E6_SMOKE18_READONLY_AUDIT_RECEIPT_V1.json",payload)
    digest=hashlib.sha256(payload).hexdigest()
    atomic_write(evidence/"E6_SMOKE18_READONLY_AUDIT_RECEIPT_V1.json.sha256",(digest+"  E6_SMOKE18_READONLY_AUDIT_RECEIPT_V1.json\n").encode("ascii"))
    report["receipt_path"]=str(evidence/"E6_SMOKE18_READONLY_AUDIT_RECEIPT_V1.json")
    report["receipt_sha256"]=digest
    return report

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-root",type=Path,required=True)
    args=parser.parse_args()
    try:
        result=run_audit(args.project_root)
        print("E6_READONLY_AUDIT_STATUS="+result["status"])
        print("E6_READONLY_AUDIT_RUN_ID="+result["run_id"])
        print(f"E6_SOURCE_PINS={result['source_pins']['passed']}/{result['source_pins']['expected']} PASS")
        print(f"E6_BASELINE_DOC_PINS={result['baseline_document_pins']['passed']}/{result['baseline_document_pins']['expected']} PASS")
        print("E6_R1V_HUMAN_CLOSEOUT="+result["prior_evidence"]["r1v"]["status"])
        print("E6_LOOP22_HUMAN_CLOSEOUT="+result["prior_evidence"]["loop22"]["status"])
        print("E6_DRILL_PRIOR_RECEIPTS="+result["prior_evidence"]["drill"]["status"])
        print("E6_CHALLENGE_AV="+result["prior_evidence"]["challenge"]["status"])
        print("E6_LOOP_DRILL_REUSE_CANDIDATES=12/18")
        print("E6_TOTAL_POTENTIAL_REUSE_IF_CH004_SELECTED=13/18")
        print("E6_MATRIX=NOT_FROZEN_CHALLENGE_EXECUTOR_AND_AUTHORIZATION_BLOCKED")
        print("E6_MEDIA_INVOKED=FALSE")
        print("E6_RECEIPT="+result["receipt_path"])
        print("E6_RECEIPT_SHA256="+result["receipt_sha256"])
        return 0 if result["status"].startswith("PASS_") else 3
    except Exception as exc:
        print(f"E6_READONLY_AUDIT=FAIL_CLOSED:{type(exc).__name__}:{exc}")
        return 3

if __name__=="__main__":
    raise SystemExit(main())
