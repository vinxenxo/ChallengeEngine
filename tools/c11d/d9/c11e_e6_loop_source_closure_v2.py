#!/usr/bin/env python3
"""Read-only source closure audit for the six E6 Smoke18 Visual Loop candidates."""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys, uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "C11E-E6-LOOP-SOURCE-CLOSURE-RECEIPT-V2"
MATRIX_PATH = "definitions/c11e/test_only/C11E_E6_SMOKE18_SCENARIO_MATRIX_20261119_V1.json"
R1V_REPORT = "artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_024454_45F195/r1v_av_report.json"
R1V_HUMAN = "artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json"
LOOP22_REPORT = "artifacts/tests/c11e/e4b_loop22_av/L22_191801_27ABF3/loop22_av_report.json"
GEO_REPORT = "artifacts/tests/c11e/r1v_geometric_av_reuse_qualification/GEOAVR2_224356_841F9B/GEO_AV_REUSE_MUX_REPORT_V1.json"
R1P_ROOT = "artifacts/tests/c11e/e4b_r1p/E4B_R1P_20261107_032743_5F75045C"
R1P_RECOVERY = "artifacts/tests/c11e/e4b_r1p_recovery/E4B_R1P_20261107_032743_5F75045C/archive_recovery_report.json"
LOOP_POLICY = "artifacts/tests/c11e/e6_loop_policy_pin_reconciliation_v2/E6LOOPPOLICYV2_20261119T184655Z_9466C358/E6_LOOP_POLICY_PIN_RECONCILIATION_RECEIPT_V2.json"
QIMAGE_RECEIPT = "artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_7/E6OPTCQTV2_7_20261119T225516Z_6DCBCB1C/C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_7.json"
L1_RECEIPT = "artifacts/tests/c11e/e6_post_qimage_l1_reconciliation_v2/E6L1RECONV2_20261119T233934Z_11996B28/C11E_E6_POST_QIMAGE_L1_PHASE_RECONCILIATION_RECEIPT_V2.json"
DOCS_RECEIPT = "artifacts/tests/c11e/e6_l1_closeout_docs_v3_install/E6L1DOCV3_20261119T234358Z_AED40579/r.json"
EXPECTED = {
 "r1v_report": (R1V_REPORT,"6a2a315a426a4bb212e07fe22cc9d786ffbbe41ede882024f3049777daadeffb",214091),
 "r1v_process": ("artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_024454_45F195/r1v_av_process_receipt.json","310588bca7e82c9ab99c4d517dd479ccc157be375b3152ca83e02ca7719b76a5",3475),
 "r1v_human": (R1V_HUMAN,"a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a",10555),
 "geo_requal_report": (GEO_REPORT,"15712f3187237f118df05c0c013558c65b2a2f7d342a0e765da8307e7a7ff037",166456),
 "loop22_report": (LOOP22_REPORT,"d8f7050f952b7248b24763abde20ce52bf812c3934738f14670a0a3dc0c72068",992067),
 "loop22_process": ("artifacts/tests/c11e/e4b_loop22_av/L22_191801_27ABF3/loop22_av_process_receipt.json","37ee99f8ab30eb445c9ca462471152b6fadc850471b8a27f7c59f30714ec2f5d",3374),
 "loop22_human_doc": ("docs/history/c11e/C11E_E4B_LOOP22_OPERATOR_ACCEPTANCE_CLOSEOUT_20261109_V2.md","f9a09d34d04ea4bd92eb70cf3668b9da093542f8a94c0a391861805f841d1dd3",1042),
 "r1p_recovery": (R1P_RECOVERY,"6bd16983a01919c7c41f785b281988139ae2a569a23daa81db6a20694f21c640",22284),
 "r1p_parent_bindings": (R1P_ROOT+"/parent_bindings.json","460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a",628698),
 "loop_policy_v2": (LOOP_POLICY,"5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be",7430),
 "smoke18_matrix": (MATRIX_PATH,"98e391738c0409c5d9d94576195d48cabcd885957434858062a44a44fe77fb75",7147),
 "r1p_06": (R1P_ROOT+"/receipts/06_E4B_R1P_20261107_032743_5F75045C_06.json","ae2c4e61c8cac93af28872fe46037d178f15d6fb96c7e30ed2d90be9144c303c",11604),
 "r1p_01": (R1P_ROOT+"/receipts/01_E4B_R1P_20261107_032743_5F75045C_01.json","aee4ce82d046ea20c1caf4a46029f02d9562b161fb4398c2e91c78998d7cd444",11821),
 "r1p_21": (R1P_ROOT+"/receipts/21_E4B_R1P_20261107_032743_5F75045C_21.json","54d69c33bcbfcd8bee62c4c80b053319252d63bfdfa7b1d139ded3d71920aec8",11642),
 "r1p_16": (R1P_ROOT+"/receipts/16_E4B_R1P_20261107_032743_5F75045C_16.json","c6ad01b6cac403a8d08e1240dccdb664fb524caadab3ad208bf5f4d69008ae5a",11766),
 "r1p_11": (R1P_ROOT+"/receipts/11_E4B_R1P_20261107_032743_5F75045C_11.json","44d15e63ca6bfc976e8aa9326eb6add7f0f18381da3ecd706bb66974959c18f3",11465),
 "r1p_02": (R1P_ROOT+"/receipts/02_E4B_R1P_20261107_032743_5F75045C_02.json","b7f230e69e251798aa426a8c818dddcb5c278acdb5590f854e46f42b1caa0679",11724),
}
R1P_PINS = {
 6: ("ae2c4e61c8cac93af28872fe46037d178f15d6fb96c7e30ed2d90be9144c303c",11604),
 1: ("aee4ce82d046ea20c1caf4a46029f02d9562b161fb4398c2e91c78998d7cd444",11821),
 21: ("54d69c33bcbfcd8bee62c4c80b053319252d63bfdfa7b1d139ded3d71920aec8",11642),
 16: ("c6ad01b6cac403a8d08e1240dccdb664fb524caadab3ad208bf5f4d69008ae5a",11766),
 11: ("44d15e63ca6bfc976e8aa9326eb6add7f0f18381da3ecd706bb66974959c18f3",11465),
 2: ("b7f230e69e251798aa426a8c818dddcb5c278acdb5590f854e46f42b1caa0679",11724),
}
SELECTOR_EXPECTED = [
 {"scenario_id":"E6-L-01","selector":"fractal_bloom/radial_bloom","family_id":"c11c_fractal_bloom_v1","grammar_id":"radial_bloom","gameplay_seed":100006,"music_seed":500006,"fps":30,"duration_seconds":22,"r1p_index":6,"origin":"R1V"},
 {"scenario_id":"E6-L-02","selector":"geometric_waves/harmonic_membrane","family_id":"c11c_geometric_waves_v1","grammar_id":"harmonic_membrane","gameplay_seed":100001,"music_seed":500001,"fps":30,"duration_seconds":23,"r1p_index":1,"origin":"R1V"},
 {"scenario_id":"E6-L-03","selector":"invisible_forces/dipole_field","family_id":"c11c_invisible_forces_v1","grammar_id":"dipole_field","gameplay_seed":100021,"music_seed":500021,"fps":30,"duration_seconds":22,"r1p_index":21,"origin":"R1V"},
 {"scenario_id":"E6-L-04","selector":"living_particles/swarm","family_id":"c11c_living_particles_v1","grammar_id":"swarm","gameplay_seed":100016,"music_seed":500016,"fps":30,"duration_seconds":20,"r1p_index":16,"origin":"R1V"},
 {"scenario_id":"E6-L-05","selector":"sacred_symmetry/astrolabe","family_id":"c11c_sacred_symmetry_v1","grammar_id":"astrolabe","gameplay_seed":100011,"music_seed":500011,"fps":30,"duration_seconds":23,"r1p_index":11,"origin":"R1V"},
 {"scenario_id":"E6-L-06","selector":"geometric_waves/interference_plane","family_id":"c11c_geometric_waves_v1","grammar_id":"interference_plane","gameplay_seed":100002,"music_seed":500002,"fps":30,"duration_seconds":23,"r1p_index":2,"origin":"LOOP22"},
]
C11C_SHA="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D48_SHA="0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"

def safe_relative(value):
 value=str(value).replace("\\","/")
 parts=value.split("/")
 return bool(value) and not value.startswith("/") and not re.match(r"^[A-Za-z]:",value) and all(x not in ("",".","..") for x in parts)

def valid_pts(pts,frame_count,time_base):
 return time_base=="1/15360" and len(pts)==frame_count and all(int(v)==i*512 for i,v in enumerate(pts))

def colorimetry_declared(stream):
 return all(stream.get(k) not in (None,"") for k in ("color_space","color_primaries","color_transfer"))

def qimage_rgb24_contract(width=720,height=1280):
 return {"width":width,"height":height,"pixel_format":"RGB24","stride":width*3,"bytes_per_frame":width*height*3}

def yuv420p_frame_bytes(width=720,height=1280):
 return width*height*3//2

def pixel_manifest_contract(pixels,frame_count,width=720,height=1280):
 expected=frame_count*yuv420p_frame_bytes(width,height)
 return (pixels.get("width")==width and pixels.get("height")==height and
         pixels.get("source_pixel_format")=="yuvj420p" and
         pixels.get("decode_pixel_format")=="yuv420p" and
         pixels.get("frames_written_to_disk") is False and
         len(pixels.get("frame_hashes",[]))==frame_count and
         all(isinstance(h,str) and re.fullmatch(r"[0-9a-f]{64}",h) for h in pixels.get("frame_hashes",[])) and
         pixels.get("raw_bytes_decoded")==expected and
         isinstance(pixels.get("global_decoded_stream_sha256"),str) and
         re.fullmatch(r"[0-9a-f]{64}",pixels.get("global_decoded_stream_sha256","")) is not None)

def ab_source_pair_valid(rows):
 if len(rows)!=2 or {x.get("repeat") for x in rows}!={"A","B"}: return False
 a=next(x for x in rows if x.get("repeat")=="A"); b=next(x for x in rows if x.get("repeat")=="B")
 return (a.get("source_video_sha256")==b.get("source_video_sha256") and
         a.get("global_pixel_stream_sha256")==b.get("global_pixel_stream_sha256") and
         a.get("frame_count")==b.get("frame_count") and a.get("time_base")==b.get("time_base"))

def geo_video_source_matches(slots,expected_sha):
 if len(slots)!=2 or {x.get("slot") for x in slots}!={"A","B"}: return False
 return all(x.get("video_source_sha256")==expected_sha and
            x.get("source_h264_stream_sha256")==x.get("final_h264_stream_sha256") for x in slots)

class Audit:
 def __init__(self,root): self.root=root.resolve(); self.checks=[]; self.fail=[]; self.pending=[]
 def add(self,ident,status,detail=None):
  row={"id":ident,"status":status}
  if detail is not None: row["detail"]=detail
  self.checks.append(row)
  if status.startswith("BLOCKED"): self.fail.append(row)
  elif status.startswith("PENDING"): self.pending.append(row)
  return row
 def path(self,rel):
  p=(self.root/Path(rel.replace("\\","/"))).resolve()
  if not p.is_relative_to(self.root): raise ValueError("PATH_ESCAPE:"+rel)
  return p
 def file(self,ident,rel,expected_sha=None,expected_bytes=None,required=True):
  try: p=self.path(rel)
  except Exception as e: return self.add(ident,"BLOCKED_PATH",str(e))
  if not p.is_file(): return self.add(ident,"BLOCKED_MISSING" if required else "PENDING_MISSING",rel)
  b=p.read_bytes(); actual=hashlib.sha256(b).hexdigest(); ok=(expected_sha is None or actual==expected_sha) and (expected_bytes is None or len(b)==expected_bytes)
  return self.add(ident,"PASS" if ok else "BLOCKED_PIN_MISMATCH",{"path":rel,"bytes":len(b),"sha256":actual,"expected_sha256":expected_sha,"expected_bytes":expected_bytes})
 def sidecar(self,rel,receipt_sha):
  p=self.path(rel+".sha256")
  if not p.is_file(): return self.add("sidecar:"+rel,"BLOCKED_SIDECAR_MISSING")
  first=p.read_text(encoding="ascii",errors="strict").strip().split()[0].lower()
  return self.add("sidecar:"+rel,"PASS" if first==receipt_sha else "BLOCKED_SIDECAR_MISMATCH",{"declared":first,"expected":receipt_sha})
 def load(self,rel): return json.loads(self.path(rel).read_text(encoding="utf-8-sig"))
 def rel_from_win(self,value):
  s=str(value).replace("/","\\")
  marker="ChallengeEngineV01_STATELESS\\"
  if marker in s: s=s.split(marker,1)[1]
  s=s.lstrip("\\")
  if re.match(r"^[A-Za-z]:",s): raise ValueError("UNMAPPED_ABSOLUTE_SOURCE_PATH:"+s)
  rel=s.replace("\\","/")
  if not safe_relative(rel): raise ValueError("UNSAFE_SOURCE_PATH:"+rel)
  return rel
 def source_record(self,spec,matrix_row,r1p):
  origin=spec["origin"]
  report_rel=R1V_REPORT if origin=="R1V" else LOOP22_REPORT
  report=self.load(report_rel)
  family=spec["family_id"]; grammar=spec["grammar_id"]
  matches=[x for x in report["source_inventories"] if x.get("family_id")==family and x.get("grammar_id")==grammar and x.get("repeat")=="A"]
  if len(matches)!=1: raise ValueError(f"SOURCE_INVENTORY_CARDINALITY:{spec['scenario_id']}:{len(matches)}")
  inv=matches[0]
  source_pair=[x for x in report["source_inventories"] if x.get("family_id")==family and x.get("grammar_id")==grammar and x.get("repeat") in ("A","B")]
  if not ab_source_pair_valid(source_pair): raise ValueError("AB_SOURCE_PAIR_NOT_IDENTICAL:"+spec["scenario_id"])
  self.add(spec["scenario_id"]+":ab_source_pair","PASS_AB_SOURCE_AND_PIXEL_STREAM_IDENTICAL",{"source_video_sha256":inv["source_video_sha256"],"global_pixel_stream_sha256":inv["global_pixel_stream_sha256"]})
  for field in ["frame_count","source_video_bytes","source_video_sha256","inventory_path","inventory_sha256","pixel_manifest_path","pixel_manifest_sha256","pts","time_base","source_video_stream","launcher_sidecars_sha256"]:
   if field not in inv: raise ValueError("SOURCE_INVENTORY_FIELD_MISSING:"+field)
  invrel=self.rel_from_win(inv["inventory_path"]); pxrel=self.rel_from_win(inv["pixel_manifest_path"]); videorel=self.rel_from_win(inv["source_video_path"])
  self.file(spec["scenario_id"]+":frame_inventory",invrel,inv["inventory_sha256"])
  self.file(spec["scenario_id"]+":pixel_manifest",pxrel,inv["pixel_manifest_sha256"])
  video=self.path(videorel)
  media_status="PASS_REHASHED" if video.is_file() else "PENDING_MEDIA_NOT_PRESENT_IN_CHECKOUT"
  media_actual=None
  if video.is_file():
   bb=video.read_bytes(); media_actual=hashlib.sha256(bb).hexdigest()
   if len(bb)!=int(inv["source_video_bytes"]) or media_actual!=inv["source_video_sha256"]:
    self.add(spec["scenario_id"]+":source_mp4","BLOCKED_PIN_MISMATCH",{"path":videorel,"bytes":len(bb),"sha256":media_actual,"expected_bytes":inv["source_video_bytes"],"expected_sha256":inv["source_video_sha256"]})
   else: self.add(spec["scenario_id"]+":source_mp4","PASS_REHASHED",{"path":videorel,"bytes":len(bb),"sha256":media_actual})
  else: self.add(spec["scenario_id"]+":source_mp4",media_status,{"path":videorel,"expected_bytes":inv["source_video_bytes"],"expected_sha256":inv["source_video_sha256"]})
  inventory=self.load(invrel); pixels=self.load(pxrel)
  selector=inventory["selector"]; timing=inventory["timing"]; stream=inventory["metadata"]["streams"][0]
  expected_frames=int(spec["duration_seconds"]*spec["fps"])
  if selector.get("family_id")!=family or selector.get("grammar_id")!=grammar or selector.get("gameplay_seed")!=spec["gameplay_seed"] or selector.get("music_seed")!=spec["music_seed"] or selector.get("fps")!=30 or selector.get("duration_seconds")!=spec["duration_seconds"]:
   raise ValueError("INVENTORY_SELECTOR_OR_SEED_MISMATCH:"+spec["scenario_id"])
  if int(inv["frame_count"])!=expected_frames or int(timing["frame_count"])!=expected_frames or int(pixels["frame_count"])!=expected_frames:
   raise ValueError("FRAME_COUNT_MISMATCH:"+spec["scenario_id"])
  if inventory.get("repeat")!="A" or inventory.get("schema")!="C11E-R1V-ACTUAL-SOURCE-FRAME-INVENTORY-V1":
   raise ValueError("INVENTORY_SCHEMA_OR_REPEAT_MISMATCH:"+spec["scenario_id"])
  source_video=inventory.get("source_video",{})
  if source_video.get("sha256")!=inv["source_video_sha256"] or source_video.get("bytes")!=inv["source_video_bytes"] or source_video.get("immutable") is not True:
   raise ValueError("INVENTORY_SOURCE_VIDEO_LINK_MISMATCH:"+spec["scenario_id"])
  inner_pts=timing.get("pts",[])
  if timing.get("time_base")!=inv.get("time_base") or len(inner_pts)!=expected_frames or any(not isinstance(x,dict) or int(x.get("frame_index",-1))!=i or int(x.get("pts",-1))!=int(inv.get("pts",[])[i]) or x.get("time_base")!=inv.get("time_base") for i,x in enumerate(inner_pts)):
   raise ValueError("OUTER_INNER_TIMING_LINEAGE_MISMATCH:"+spec["scenario_id"])
  pts=inv.get("pts",[])
  if not valid_pts(pts,expected_frames,inv.get("time_base")):
   raise ValueError("PTS_OR_TIMEBASE_MISMATCH:"+spec["scenario_id"])
  if stream.get("codec_name")!="h264" or stream.get("width")!=720 or stream.get("height")!=1280 or stream.get("r_frame_rate")!="30/1" or stream.get("time_base")!="1/15360" or stream.get("pix_fmt")!="yuvj420p" or stream.get("color_range")!="pc":
   raise ValueError("SOURCE_STREAM_CONTRACT_MISMATCH:"+spec["scenario_id"])
  if not pixel_manifest_contract(pixels,expected_frames):
   raise ValueError("PIXEL_MANIFEST_CONTRACT_MISMATCH:"+spec["scenario_id"])
  if pixels.get("source_mp4_sha256")!=inv["source_video_sha256"] or pixels.get("global_decoded_stream_sha256")!=inv.get("global_pixel_stream_sha256") or inventory.get("pixel_identity",{}).get("global_decoded_stream_sha256")!=pixels.get("global_decoded_stream_sha256"):
   raise ValueError("PIXEL_STREAM_HASH_LINEAGE_MISMATCH:"+spec["scenario_id"])
  if inventory.get("decode",{}).get("raw_pixel_bytes")!=pixels.get("raw_bytes_decoded") or inventory.get("decode",{}).get("frames_written_to_disk") is not False:
   raise ValueError("INVENTORY_DECODE_SUMMARY_MISMATCH:"+spec["scenario_id"])
  color_fields={k:stream.get(k) for k in ("color_space","color_primaries","color_transfer","color_range")}
  color_declared=colorimetry_declared(stream)
  self.add(spec["scenario_id"]+":frame_contract","PASS",{"source_video_sha256":inv["source_video_sha256"],"source_video_bytes":inv["source_video_bytes"],"inventory_sha256":inv["inventory_sha256"],"pixel_manifest_sha256":inv["pixel_manifest_sha256"],"frames":expected_frames,"fps":30,"pts_first":pts[0] if pts else None,"pts_last":pts[-1] if pts else None,"pts_step":512,"time_base":"1/15360","source_encoded_pix_fmt":"yuvj420p","source_color_range":"pc","decoded_pix_fmt":"yuv420p","decoded_bytes_per_frame":1382400,"color_metadata":color_fields,"color_primaries_transfer_space_declared":color_declared,"frames_written_to_disk":pixels["frames_written_to_disk"]})
  # Hash the exact FFprobe JSON whose digest is already recorded in the inventory's launcher sidecars.
  ffprobe_name=Path(invrel).name.replace("_r1v_frame_inventory.json","_ffprobe.json")
  ffprobe_rel=str(Path(invrel).parent/ffprobe_name).replace("\\","/")
  expected_ff=inv["launcher_sidecars_sha256"]["launcher_ffprobe_sha256"]
  self.file(spec["scenario_id"]+":ffprobe_json",ffprobe_rel,expected_ff)
  # R1P source code pins: launcher, prototype and scene.
  lp=r1p["case_source_pins"]["launcher"]; pp=r1p["case_source_pins"]["prototype"]
  self.file(spec["scenario_id"]+":launcher_source",lp["path"],lp["sha256"])
  self.file(spec["scenario_id"]+":prototype_source",pp["path"],pp["prototype_sha256"])
  scene_path=selector.get("scene_path") or r1p.get("selection",{}).get("scene_path")
  scene_sha=selector.get("scene_sha256") or r1p.get("selection",{}).get("scene_sha256")
  if scene_path and scene_sha: self.file(spec["scenario_id"]+":scene_source",scene_path,scene_sha)
  else: self.add(spec["scenario_id"]+":scene_source","BLOCKED_SCENE_PIN_MISSING")
  # Verify R1V A/B delivery hashes have matching operator-closeout entries for the five R1V representatives.
  if origin=="R1V":
   human=self.load(R1V_HUMAN)
   if grammar=="harmonic_membrane":
    geo=self.load(GEO_REPORT)
    geoslots=[x for x in geo["slots"] if x.get("slot") in ("A","B")]
    if geo.get("run_id")!="GEOAVR2_224356_841F9B" or not geo_video_source_matches(geoslots,inv["source_video_sha256"]):
     raise ValueError("GEO_REPLACEMENT_SOURCE_IDENTITY_MISMATCH:"+spec["scenario_id"])
    av=[{"repeat":x["slot"],"final_av_sha256":x["final_av_sha256"]} for x in geoslots]
   else:
    av=[x for x in report["audiovisual_outputs"] if x.get("family_id")==family and x.get("grammar_id")==grammar and x.get("repeat") in ("A","B")]
   hs=[x for x in human["slots"] if x.get("family_id")==family and x.get("grammar_id")==grammar and x.get("slot") in ("A","B")]
   if len(av)!=2 or len(hs)!=2: raise ValueError("R1V_AB_HUMAN_PAIR_CARDINALITY:"+spec["scenario_id"])
   amap={x["repeat"]:x["final_av_sha256"] for x in av}; hmap={x["slot"]:x["mp4_sha256"] for x in hs}
   if amap!=hmap or any(x.get("operator_statement")!="pass" or x.get("visual_status") not in ("OPERATOR_CONFIRMED_PASS","OPERATOR_CONFIRMED_AV_PASS") or x.get("audio_status") not in ("OPERATOR_CONFIRMED_PASS","OPERATOR_CONFIRMED_AV_PASS") for x in hs):
    raise ValueError("R1V_HUMAN_REVIEW_LINEAGE_MISMATCH:"+spec["scenario_id"])
   self.add(spec["scenario_id"]+":operator_av_review","PASS_OPERATOR_CLOSEOUT_LINK_MATCHED",{"A_sha256":amap["A"],"B_sha256":amap["B"],"visual":"PASS","audio":"PASS"})
  else:
   av=[x for x in report["audiovisual_outputs"] if x.get("family_id")==family and x.get("grammar_id")==grammar and x.get("repeat") in ("A","B")]
   if len(av)!=2: raise ValueError("LOOP22_AB_PAIR_CARDINALITY")
   self.add(spec["scenario_id"]+":operator_av_review","PASS_LOOP22_PHASE_CLOSEOUT_REUSE_LINK",{"A_sha256":next(x["final_av_sha256"] for x in av if x["repeat"]=="A"),"B_sha256":next(x["final_av_sha256"] for x in av if x["repeat"]=="B"),"closeout_document":"C11E_E4B_LOOP22_OPERATOR_ACCEPTANCE_CLOSEOUT_20261109_V2.md"})
  r1p_path=f"{R1P_ROOT}/receipts/{spec['r1p_index']:02d}_E4B_R1P_20261107_032743_5F75045C_{spec['r1p_index']:02d}.json"
  self.add(spec["scenario_id"]+":r1p_receipt_link","PASS",{"path":r1p_path,"receipt_sha256":hashlib.sha256(self.path(r1p_path).read_bytes()).hexdigest(),"R1P_payload_sha256":r1p.get("payload_sha256"),"R1P_not_renderer_input":True})
  return {"scenario_id":spec["scenario_id"],"selector":spec["selector"],"origin":origin,"source_mp4_path":videorel,"source_mp4_sha256":inv["source_video_sha256"],"source_mp4_bytes":inv["source_video_bytes"],"source_mp4_rehashed":video.is_file() and media_actual==inv["source_video_sha256"],"frame_count":expected_frames,"pts_step":512,"time_base":"1/15360","encoded_pixel_format":"yuvj420p","decoded_pixel_format":"yuv420p","decoded_bytes_per_frame":yuv420p_frame_bytes(),"qimage_input_contract":{"pixel_format":"RGB24","stride":2160,"bytes_per_frame":2764800},"color_metadata":color_fields,"color_conversion_qualified":False,"L2_ready":False}

def qimage_receipt_semantics(obj):
 """Validate the actual V2.7 receipt schema; do not compare a nested object to an integer."""
 runtime=obj.get("runtime", {})
 tests=obj.get("qimage_tests", {})
 bench=obj.get("qimage_benchmark", {})
 governance=obj.get("governance", {})
 fixtures=obj.get("fixtures", [])
 source_checks=obj.get("source_checks", [])
 a3=obj.get("loop_policy_a3_adjudication", {})
 checks={
  "schema": obj.get("schema")=="C11E-E6-OPTION-C-NATIVE-QT-PROBE-RECEIPT-V2.7",
  "status": obj.get("status")=="PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END",
  "runtime": runtime.get("python_version")=="3.13.14" and runtime.get("pyside6")=="6.11.2",
  "tests": tests.get("run") is True and tests.get("tests")==37 and tests.get("failures")==0 and tests.get("errors")==0 and tests.get("status")=="PASS" and obj.get("qimage_test_import_error") is None and obj.get("qimage_test_execution_error") is None,
  "benchmark": bench.get("iterations")==7 and len(bench.get("samples_ms", []))==7 and isinstance(bench.get("p95_ms"),(int,float)) and float(bench.get("p95_ms"))<=1000.0/30.0 and bench.get("stage_30fps_budget")=="PASS" and bench.get("end_to_end_qualified") is False,
  "source_pins": len(source_checks)==23 and all(x.get("status")=="PASS" for x in source_checks),
  "a3": a3.get("status")=="PASS" and a3.get("error") is None,
  "fixtures": len(fixtures)==3 and all(x.get("source_immutable") is True for x in fixtures),
  "governance": governance.get("c11c_modified") is False and governance.get("d4_8_v2_modified") is False and governance.get("source_files_modified") is False and governance.get("godot_invoked") is False and governance.get("ffmpeg_invoked") is False and governance.get("ffprobe_invoked") is False and governance.get("audio_generated") is False and governance.get("mux_invoked") is False and governance.get("production_dispatch") is False and governance.get("production_media_created") is False and governance.get("renderer_native_input_emitted") is False and governance.get("batch_id_consumed") is False and governance.get("e6_accepted")==0 and governance.get("release_authority")=="NONE",
 }
 return all(checks.values()), checks, {"status":obj.get("status"),"qimage_tests":tests,"qimage_benchmark":{"iterations":bench.get("iterations"),"p95_ms":bench.get("p95_ms"),"stage_30fps_budget":bench.get("stage_30fps_budget"),"end_to_end_qualified":bench.get("end_to_end_qualified")},"runtime":runtime,"source_checks":len(source_checks),"a3_status":a3.get("status"),"fixture_count":len(fixtures),"checks":checks}


def l1_receipt_semantics(obj):
 """Read E6 acceptance from its actual phase_state/governance containers."""
 phase=obj.get("phase_state", {})
 governance=obj.get("governance", {})
 checks=obj.get("checks", [])
 all_checks_pass=(len(checks)==18 and all(x.get("status")=="PASS" for x in checks))
 result_checks={
  "schema": obj.get("schema")=="C11E-E6-POST-QIMAGE-L1-PHASE-RECONCILIATION-RECEIPT-V2",
  "status": obj.get("status")=="PASS_READ_ONLY_E6_PHASE_RECONCILIATION_V2_WITH_VISUAL_REVIEW_PENDING",
  "check_totals": obj.get("check_count")==18 and obj.get("passed_checks")==18 and obj.get("blocked_checks")==0 and obj.get("blocked_ids")==[],
  "all_18_checks_pass": all_checks_pass,
  "phase_e6_accepted_zero": phase.get("e6_accepted")==0,
  "governance_e6_accepted_zero": governance.get("e6_accepted")==0,
  "d4_8_immutable_blocked": governance.get("d4_8_v2")=="BLOCKED_IMMUTABLE",
  "release_authority_none": governance.get("release_authority")=="NONE",
  "no_execution_authority": obj.get("no_execution_authority_created") is True,
  "resampler_still_pending": phase.get("visual_resampler_review")=="PENDING_OPERATOR_VISUAL_REVIEW_NOT_INFERRED_FROM_HASHES",
 }
 return all(result_checks.values()),result_checks,{"status":obj.get("status"),"check_count":obj.get("check_count"),"passed_checks":obj.get("passed_checks"),"blocked_checks":obj.get("blocked_checks"),"blocked_ids":obj.get("blocked_ids"),"phase_state_e6_accepted":phase.get("e6_accepted"),"governance_e6_accepted":governance.get("e6_accepted"),"no_execution_authority_created":obj.get("no_execution_authority_created"),"checks":result_checks}

def run(root):
 a=Audit(root)
 # Immutable release pins, current gates, receipts and predecessor evidence.
 for key,(rel,digest,nbytes) in EXPECTED.items():
  a.file(key,rel,digest,nbytes)
  if key in ("geo_requal_report","loop_policy_v2"):
   a.sidecar(rel,digest)
 a.file("frozen_c11c_manifest","release/C11C_FREEZE_PACKAGE_MANIFEST.json",C11C_SHA,796318)
 a.file("d4_8_v2_immutable","definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json",D48_SHA,12996)
 # V3 documentation install receipt and the two successful L1 receipts are anchored to operator-provided current-checkout values.
 a.file("qimage_v2_7_receipt",QIMAGE_RECEIPT,"95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783")
 a.sidecar(QIMAGE_RECEIPT,"95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783")
 a.file("l1_reconciliation_v2_receipt",L1_RECEIPT,"24c2a4f09901a3d1c888d972aabf2a7016496f48e5011b512a1e261338d72474")
 a.sidecar(L1_RECEIPT,"24c2a4f09901a3d1c888d972aabf2a7016496f48e5011b512a1e261338d72474")
 a.file("docs_v3_install_receipt",DOCS_RECEIPT,"08321c5988aecca20cc668ab69b95e0ab854006b524dda0d4df205a79defeed6")
 a.sidecar(DOCS_RECEIPT,"08321c5988aecca20cc668ab69b95e0ab854006b524dda0d4df205a79defeed6")
 # Validate semantic envelopes, not just bytes.
 try:
  q=json.loads(a.path(QIMAGE_RECEIPT).read_text(encoding="utf-8-sig")); qok,qchecks,qdetail=qimage_receipt_semantics(q)
  a.add("qimage_l1_semantics","PASS" if qok else "BLOCKED_QIMAGE_RECEIPT_SEMANTICS",qdetail)
  l1=json.loads(a.path(L1_RECEIPT).read_text(encoding="utf-8-sig")); l1ok,l1checks,l1detail=l1_receipt_semantics(l1)
  a.add("l1_reconciliation_semantics","PASS" if l1ok else "BLOCKED_L1_RECEIPT_SEMANTICS",l1detail)
  h=json.loads(a.path(R1V_HUMAN).read_text(encoding="utf-8-sig")); hte=h.get("technical_evidence",{})
  hgeo=(hte.get("geo_replacement_report_sha256")==EXPECTED["geo_requal_report"][1] and hte.get("geo_replacement_run_id")=="GEOAVR2_224356_841F9B" and hte.get("geo_replacement_ab_mp4_sha256")=="a3c5d820fbed7be5392f1b5514b4bbc8437c0de50d2c0e22b63204ea4233a0ce")
  hok=(h.get("status")=="PASS_TEST_ONLY_OPERATOR_ACCEPTED" and h.get("phase_closed") is True and h.get("acceptance",{}).get("combined_slots")=="10/10_PASS" and hgeo)
  a.add("r1v_operator_review_semantics","PASS" if hok else "BLOCKED_R1V_HUMAN_REVIEW_SEMANTICS",{"status":h.get("status"),"phase_closed":h.get("phase_closed"),"combined_slots":h.get("acceptance",{}).get("combined_slots"),"GEO_replacement_link":hgeo})
  rp=json.loads(a.path(R1P_RECOVERY).read_text(encoding="utf-8-sig")); a.add("r1p_recovery_semantics","PASS" if rp.get("status")=="PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27" and rp.get("receipt_json_count")==27 and rp.get("receipt_sidecar_count")==27 else "BLOCKED_R1P_RECOVERY_SEMANTICS")
  lp=json.loads(a.path(LOOP_POLICY).read_text(encoding="utf-8-sig")); a.add("loop_policy_semantics","PASS" if lp.get("status")=="PASS_LOOP_POLICY_DECISIONS_RECONCILED_NOT_COMPOSITOR_ACCEPTANCE" and lp.get("check_count")==18 and lp.get("failed_checks")==0 else "BLOCKED_LOOP_POLICY_SEMANTICS")
  matrix=a.load(MATRIX_PATH); rows=[r for r in matrix.get("rows",[]) if r.get("family")=="visual_loops"]
  a.add("smoke18_draft_semantics","PASS" if matrix.get("status")=="DRAFT_CANDIDATE_MATRIX_NOT_FROZEN_NOT_E6_ACCEPTED" and len(rows)==6 and matrix.get("e6_accepted")==0 else "BLOCKED_MATRIX_STATE",{"loop_rows":len(rows),"matrix_status":matrix.get("status"),"e6_accepted":matrix.get("e6_accepted")})
  process1=a.load(EXPECTED["r1v_process"][0]); process2=a.load(EXPECTED["loop22_process"][0]); report1=a.load(R1V_REPORT); report2=a.load(LOOP22_REPORT)
  a.add("r1v_process_report_link","PASS" if process1.get("report_sha256")==EXPECTED["r1v_report"][1] and process1.get("status")==report1.get("status") and report1.get("completed_av_outputs")==10 else "BLOCKED_R1V_PROCESS_LINK")
  a.add("loop22_process_report_link","PASS" if process2.get("report_sha256")==EXPECTED["loop22_report"][1] and process2.get("status")==report2.get("status") and report2.get("completed_av_outputs")==44 else "BLOCKED_LOOP22_PROCESS_LINK")
  georeport=a.load(GEO_REPORT)
  a.add("geo_harmonic_requalification_semantics","PASS" if georeport.get("status")=="PASS_GEO_AV_REUSE_MUX_ONLY_TECHNICAL_REQUALIFICATION_NOT_FULL_R1V_ACCEPTANCE" and len(georeport.get("slots",[]))==2 and georeport.get("errors")==[] else "BLOCKED_GEO_REQUALIFICATION_SEMANTICS")
  loopdoc=a.path("docs/history/c11e/C11E_E4B_LOOP22_OPERATOR_ACCEPTANCE_CLOSEOUT_20261109_V2.md").read_text(encoding="utf-8")
  loopdoc_ok=("CLOSED_PASS_OPERATOR_ACCEPTED" in loopdoc and "44/44" in loopdoc and "22/22" in loopdoc and "L22_191801_27ABF3" in loopdoc and EXPECTED["loop22_report"][1] in loopdoc)
  a.add("loop22_operator_closeout_semantics","PASS" if loopdoc_ok else "BLOCKED_LOOP22_OPERATOR_CLOSEOUT_SEMANTICS")
  # Validate six R1P payload/selector receipts and source code pins.
  specs=[]
  for spec in SELECTOR_EXPECTED:
   specrow=next((x for x in rows if x.get("scenario_id")==spec["scenario_id"]),None)
   if specrow is None or any(specrow.get(k)!=spec.get(k) for k in ("selector","gameplay_seed","music_seed","fps","duration_seconds")):
    raise ValueError("SMOKE18_ROW_DOES_NOT_MATCH_LOCKED_SELECTOR:"+spec["scenario_id"])
   rpath=f"{R1P_ROOT}/receipts/{spec['r1p_index']:02d}_E4B_R1P_20261107_032743_5F75045C_{spec['r1p_index']:02d}.json"
   rr=a.load(rpath); exsha,exbytes=R1P_PINS[spec["r1p_index"]]
   if rr.get("selection",{}).get("family_id")!=spec["family_id"] or rr.get("selection",{}).get("grammar_id")!=spec["grammar_id"] or rr.get("timing",{}).get("duration_seconds")!=spec["duration_seconds"] or rr.get("timing",{}).get("fps")!=30 or rr.get("seed_domains",{}).get("gameplay_seed")!=spec["gameplay_seed"] or rr.get("seed_domains",{}).get("music_seed")!=spec["music_seed"]:
    raise ValueError("R1P_SELECTOR_SEED_TIMING_MISMATCH:"+spec["scenario_id"])
   m=rr.get("materialization",{})
   if rr.get("status")!="PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT" or m.get("frame_buffers_materialized") is not False or m.get("pixel_payload_materialized") is not False or m.get("renderer_native_input_emitted") is not False:
    raise ValueError("R1P_RENDERER_INPUT_BOUNDARY_CHANGED:"+spec["scenario_id"])
   a.file("r1p_"+spec["scenario_id"],rpath,exsha,exbytes); a.sidecar(rpath,rr.get("receipt_sha256"))
   specs.append(a.source_record(spec,specrow,rr))
  # Global QImage input contract: synthetic RGB24 benchmark does not materialize real selector buffers.
  rgb=qimage_rgb24_contract()
  a.add("qimage_rgb24_contract","PASS_CONTRACT_ONLY",{**rgb,"real_buffers_present":False})
  a.add("colorimetry_gate","PENDING_UNDECLARED_SOURCE_COLORIMETRY",{"source_color_primaries":None,"source_color_transfer":None,"source_color_space":None,"no_assumption":"BT.709 or other colorimetry must not be inferred","conversion_authorized":False})
  a.add("visual_resampler_gate","PENDING_OPERATOR_VISUAL_REVIEW",{"required_preview_pngs":["OPTION_C_QT_color_bars_registration.png","OPTION_C_QT_smooth_rgb_gradient.png","OPTION_C_QT_one_pixel_checkerboard.png"],"geometry_approved":True,"resampler_approved":False})
  blocked=len(a.fail); pending=len(a.pending)
  if blocked: status="BLOCKED_LOOP_SOURCE_CLOSURE"
  elif pending: status="PASS_LOOP_SOURCE_PROVENANCE_RECONCILED_WITH_COLORIMETRY_AND_VISUAL_REVIEW_PENDING"
  else: status="PASS_LOOP_SOURCE_PROVENANCE_RECONCILED_L2_STILL_BLOCKED_BY_RGB24_COLORIMETRY_AND_GOVERNANCE"
  runid="E6LOOPSRCV2_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"_"+uuid.uuid4().hex[:8].upper()
  outroot=a.path(f"artifacts/tests/c11e/e6_loop_source_closure_v2/{runid}"); outroot.mkdir(parents=True,exist_ok=False)
  rec={"schema":SCHEMA,"run_id":runid,"created_utc":datetime.now(timezone.utc).isoformat(),"status":status,"check_count":len(a.checks),"passed_checks":sum(x['status'].startswith('PASS') for x in a.checks),"pending_checks":pending,"failed_checks":blocked,"checks":a.checks,"selected_loop_sources":specs,"source_media_rehash_complete":all(x["source_mp4_rehashed"] for x in specs),"qimage_real_rgb24_buffers_present":False,"colorimetry_complete":False,"visual_resampler_review":"PENDING_OPERATOR_VISUAL_REVIEW","L2_ready":False,"governance":{"C11C_frozen_manifest_sha256":C11C_SHA,"D4_8_V2_sha256":D48_SHA,"D4_8":"BLOCKED_UNCHANGED","renderer":"OFF","media":"OFF","dispatch":"OFF","godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"audio_generated":False,"mux_invoked":False,"e6_accepted":0,"release_authority":"NONE","git_checks":"SKIPPED","commits":"OPERATOR_MANAGED"}}
  rp=outroot/"C11E_E6_LOOP_SOURCE_CLOSURE_RECEIPT_V2.json"; raw=(json.dumps(rec,indent=2,ensure_ascii=False)+"\n").encode();rp.write_bytes(raw); digest=hashlib.sha256(raw).hexdigest();(outroot/(rp.name+".sha256")).write_text(digest+"  "+rp.name+"\n",encoding="ascii")
  print("READ_ONLY_SOURCE_CHECKS=%d; PASS=%d; PENDING=%d; BLOCKED=%d"%(len(a.checks),rec['passed_checks'],pending,blocked))
  print("LOOP_SELECTOR_ROWS=%d/6"%len(specs));print("SOURCE_MEDIA_REHASH_COMPLETE=%s"%str(rec['source_media_rehash_complete']).upper())
  print("QIMAGE_REAL_RGB24_BUFFERS=NOT_PRESENT_IN_R1P_PIXEL_EVIDENCE")
  print("SOURCE_COLORIMETRY=UNDECLARED; NO_BT709_ASSUMPTION")
  print("VISUAL_RESAMPLER_REVIEW=PENDING_OPERATOR_VISUAL_REVIEW")
  print("PENDING_GATE_IDS="+",".join(x["id"] for x in a.pending))
  print("L2_READY=FALSE; REAL_RGB24_BUFFER_PRESENT=FALSE; COLOR_CONVERSION_AUTHORIZED=FALSE")
  print("D4_8_V2=BLOCKED/UNCHANGED; RENDERER=OFF; MEDIA=OFF; E6_ACCEPTED=0; RELEASE_AUTHORITY=NONE")
  print("SOURCE_CLOSURE_V2_STATUS="+status);print("RECEIPT="+str(rp));print("RECEIPT_SHA256="+digest);print("RECEIPT_SIDECAR="+str(rp)+".sha256")
  print("GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE; AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE")
  return 0 if not blocked else 2
 except Exception as e:
  print("SOURCE_CLOSURE_V2_AUDIT_EXCEPTION="+type(e).__name__+":"+str(e),file=sys.stderr)
  return 2

def main():
 p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);args=p.parse_args();root=Path(args.project_root)
 if not root.is_dir(): print("PROJECT_ROOT_MISSING",file=sys.stderr);return 2
 return run(root)
if __name__=="__main__": raise SystemExit(main())
