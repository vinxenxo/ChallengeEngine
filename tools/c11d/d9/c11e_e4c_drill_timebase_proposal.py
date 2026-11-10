"""Validate the unapproved E4C Drill phase-to-final-stream timebase proposal."""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
from typing import Any

PROPOSAL = Path("definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json")
SCHEMA = Path("definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_SCHEMA_V1.json")
EXPECTED_PROPOSAL_SHA = "44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8"
SOURCE_PINS = {'core/presentation/CountdownPresentationLogic.gd': 'b163ea114cc48af2dfd957ee92d00d524ea5b96b5966850f5ca8d6e5ec933379', 'core/presentation/VisualDrillPresentationPhaseLogic.gd': '6555d08ac3c0098b20a57e924b0c4ff2df006a23fa00a81b254fa5ebd5bb2494', 'core/presentation/rendering/VisualContentPlayer.gd': '58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145', 'core/presentation/VisualDrillPresentationBinder.gd': 'cb6acc408252b8b794177d8f5923a3b151646eebdfd1efe9a30fdd6221de82c0', 'core/presentation/C11CVisualEditorialLayer.gd': 'f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d', 'core/presentation/PresentationUI.gd': 'a55fea5a4525ea247144a4da88242f4ac602c3a014f7d02b50d032ce99224730', 'definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json': '609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc', 'definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json': '5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795', 'definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json': '41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85', 'docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json': '49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04', 'docs/current/e/C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json': 'aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac'}
class TimebaseProposalError(ValueError): pass

def _sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def _round_gdscript(value: float) -> int: return int(math.floor(value + 0.5))
def countdown_frames(fps: int) -> int: return _round_gdscript(3.0 * max(1, fps))
def end_cta_frames(fps: int) -> int: return _round_gdscript(3.0 * max(1, fps))

def map_player_frame_to_final(phase: str, player_frame_index: int, gameplay_frames: int, fps: int) -> dict[str, Any]:
    if isinstance(player_frame_index, bool) or not isinstance(player_frame_index, int):
        raise TimebaseProposalError("player_frame_index must be an integer")
    if isinstance(gameplay_frames, bool) or not isinstance(gameplay_frames, int) or gameplay_frames <= 0:
        raise TimebaseProposalError("gameplay_frames must be a positive integer")
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0:
        raise TimebaseProposalError("fps must be a positive integer")
    pre = countdown_frames(fps); end = end_cta_frames(fps); total = pre + gameplay_frames + end
    if phase == "PRE_ROLL":
        if not 0 <= player_frame_index < pre: raise TimebaseProposalError("PRE_ROLL frame index outside source phase")
        return {"final_presentation_frame_index":player_frame_index,"source_frame_index":0,"d_editorial_visible":False}
    if phase == "GAME":
        if not 0 <= player_frame_index < gameplay_frames: raise TimebaseProposalError("GAME frame index outside payload interval")
        return {"final_presentation_frame_index":pre+player_frame_index,"source_frame_index":player_frame_index,"d_editorial_visible":True}
    if phase == "END_CTA":
        if not pre+gameplay_frames <= player_frame_index < total: raise TimebaseProposalError("END_CTA player index outside final presentation interval")
        return {"final_presentation_frame_index":player_frame_index,"source_frame_index":gameplay_frames-1,"d_editorial_visible":False}
    if phase == "DONE": return {"final_presentation_frame_index":None,"source_frame_index":None,"d_editorial_visible":False}
    raise TimebaseProposalError("unknown Drill phase")

def validate(root: Path) -> dict[str, Any]:
    root=root.resolve(); p=root/PROPOSAL; s=root/SCHEMA
    if not p.is_file() or _sha(p)!=EXPECTED_PROPOSAL_SHA: raise TimebaseProposalError("timebase proposal SHA mismatch")
    if not s.is_file(): raise TimebaseProposalError("timebase proposal schema missing")
    for rel,digest in SOURCE_PINS.items():
        src=root/rel
        if not src.is_file() or _sha(src)!=digest: raise TimebaseProposalError("timebase source pin mismatch: "+rel)
    d=json.loads(p.read_text(encoding="utf-8")); schema=json.loads(s.read_text(encoding="utf-8"))
    try:
        import jsonschema
        jsonschema.Draft202012Validator(schema).validate(d)
    except Exception as exc: raise TimebaseProposalError("timebase proposal schema validation failed: "+str(exc)) from exc
    if d["authority"]["source_pins"] != SOURCE_PINS: raise TimebaseProposalError("proposal source pin set mismatch")
    if d["status"]!="PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT" or d["approval"]["timebase_mapping_approved"] is not False: raise TimebaseProposalError("timebase proposal was promoted")
    if d["candidate_mapping"]["formula"]!="final_presentation_frame_index = pre_roll_frames + game_payload_frame_index": raise TimebaseProposalError("candidate formula changed")
    if d["candidate_mapping"]["phase_visibility"]["END_CTA"].find("SUPPRESS_ALL_D_EDITORIAL_FIELDS")<0: raise TimebaseProposalError("D fields would compete with native END_CTA")
    if d["semantic_guards"]["d1_audio_asset_selection_or_generation_authorized"] is not False: raise TimebaseProposalError("D1 audio authorization broadened")
    if d["execution_boundary"]["renderer"]!="OFF" or d["execution_boundary"]["media_created"] is not False or d["execution_boundary"]["release_authority"]!="NONE": raise TimebaseProposalError("execution boundary broadened")
    return {"status":"PASS_PROPOSAL_ONLY","proposal_sha256":EXPECTED_PROPOSAL_SHA,"schema_sha256":_sha(s),"source_pins":len(SOURCE_PINS),"sample_30fps":map_player_frame_to_final("GAME",0,630,30),"game_interval":"[90,720)","renderer":"OFF","media_created":False,"release_authority":"NONE"}
