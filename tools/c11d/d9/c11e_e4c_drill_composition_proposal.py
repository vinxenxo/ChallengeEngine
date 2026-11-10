"""Validate the unapproved E4C Drill outer-band proposal as a design-only artifact."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any
PROPOSAL=Path("definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_V1.json")
SCHEMA=Path("definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_SCHEMA_V1.json")
EXPECTED_SHA="b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09"
SCHEMA_SHA="3684316e98ab2054bd913df17c6e398d8040d047027de36332690cfd2be517bc"
SOURCE_PINS={
 "core/presentation/VisualDrillPresentationPhaseLogic.gd":"6555d08ac3c0098b20a57e924b0c4ff2df006a23fa00a81b254fa5ebd5bb2494",
 "core/presentation/VisualDrillPresentationBinder.gd":"cb6acc408252b8b794177d8f5923a3b151646eebdfd1efe9a30fdd6221de82c0",
 "core/presentation/rendering/VisualContentPlayer.gd":"58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145",
 "core/presentation/C11CVisualEditorialLayer.gd":"f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d",
 "core/presentation/PresentationUI.gd":"a55fea5a4525ea247144a4da88242f4ac602c3a014f7d02b50d032ce99224730",
 "core/presentation/SocialUIBinder.gd":"b15a062bf327d0c2bbc4ead0e877914f912528cc56e388df20dd84eb89863a3c",
 "core/presentation/UnifiedSocialFrame.gd":"d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba",
}
class ProposalError(ValueError): pass
def _sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(root:Path)->dict[str,Any]:
 root=root.resolve(); p=root/PROPOSAL; s=root/SCHEMA
 if not p.is_file() or _sha(p)!=EXPECTED_SHA: raise ProposalError("Drill composition proposal SHA mismatch")
 if not s.is_file() or _sha(s)!=SCHEMA_SHA: raise ProposalError("Drill composition schema SHA mismatch")
 for rel,digest in SOURCE_PINS.items():
  if not (root/rel).is_file() or _sha(root/rel)!=digest: raise ProposalError("protected C11-C source pin mismatch: "+rel)
 d=json.loads(p.read_text(encoding="utf-8")); schema=json.loads(s.read_text(encoding="utf-8"))
 try:
  import jsonschema
  jsonschema.Draft202012Validator(schema).validate(d)
 except Exception as exc: raise ProposalError("Drill proposal schema validation failed: "+str(exc)) from exc
 g=d["geometry"]; top=g["top_editorial_band"]; view=g["source_frame_viewport"]; bottom=g["bottom_editorial_band"]
 if (top["x"],top["y"],top["width"],top["height"])!=(0,0,720,192): raise ProposalError("top band geometry changed")
 if (view["x"],view["y"],view["width"],view["height"])!=(108,192,504,896): raise ProposalError("source viewport geometry changed")
 if (bottom["x"],bottom["y"],bottom["width"],bottom["height"])!=(0,1088,720,192): raise ProposalError("bottom band geometry changed")
 if top["y"]+top["height"]!=view["y"] or view["y"]+view["height"]!=bottom["y"] or bottom["y"]+bottom["height"]!=1280: raise ProposalError("bands must partition the full canvas without overlap or gaps")
 if d["phase_ownership"]["payload_to_final_presentation_offset"]!="UNRESOLVED_REQUIRES_EXPLICIT_D_OWNED_TIMEBASE_DECISION": raise ProposalError("phase offset was inferred without approval")
 if d["approval_gates"]["drill_composition_approved"] is not False or d["approval_gates"]["drill_timebase_mapping_approved"] is not False: raise ProposalError("unapproved Drill proposal was promoted")
 if d["execution_boundary"]["renderer"]!="OFF" or d["execution_boundary"]["media_created"] is not False: raise ProposalError("renderer/media boundary was weakened")
 if d["native_source_ownership"]["native_visual_drill_end_cta"]!="PRESERVED_INSIDE_SOURCE_FRAME_HEADER_DURING_END_CTA": raise ProposalError("native END_CTA ownership was changed")
 if d.get("editorial_visibility",{}).get("PRE_ROLL","").find("SUPPRESS_ALL_D_EDITORIAL_FIELDS") < 0 or d.get("editorial_visibility",{}).get("END_CTA","").find("SUPPRESS_ALL_D_EDITORIAL_FIELDS") < 0: raise ProposalError("D editorial must remain suppressed during PRE_ROLL and END_CTA")
 return {"status":"PASS_PROPOSAL_ONLY","proposal_sha256":EXPECTED_SHA,"schema_sha256":SCHEMA_SHA,"pinned_c11c_sources":len(SOURCE_PINS),"geometry":"720x1280 / 192px bands / 504x896 source viewport","phase_offset":"UNRESOLVED","renderer":"OFF","media_created":False,"release_authority":"NONE"}
