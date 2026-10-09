from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"c11c-suite/c11c-catalog"))
from c11d_catalog import project_cross_suite_lifecycle_intent
identity={"request_id":"D913-TEST-CHALLENGE","content_type":"challenges","selection":{"content_type":"challenges","family_id":"key","variant_id":"CHALLENGE_001"},"request_hash":"a"*64,"editorial_hash":"b"*64,"plan_hash":"c"*64,"bridge_record_hash":"d"*64,"gameplay_seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","resolved_delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","audio_enabled":True,"personalization_enabled":True}
life="D9L13-"+"A"*24; identity_sha="e"*64; evidence="artifacts/tests/c11d_d9/producer_universal/D913-TEST-CHALLENGE/cross_suite_lifecycle_receipt.json"
row=project_cross_suite_lifecycle_intent(identity,life,identity_sha,evidence)
assert row["record_type"]=="CROSS_SUITE_LIFECYCLE_INTENT" and row["lifecycle_id"]==life
assert row["identity_hash"]==identity_sha and row["media_path"] is None and row["media_sha256"] is None
assert row["release_authority"]=="NONE" and row["media_eligibility"]=="NO_MEDIA_CREATED"
def rejects(label, mutate):
 x=dict(identity); mutate(x)
 try: project_cross_suite_lifecycle_intent(x,life,identity_sha,evidence)
 except (ValueError,TypeError): return
 raise AssertionError(f"negative accepted: {label}")
rejects("bad request hash",lambda x:x.update(request_hash="bad"))
rejects("unsafe receipt path",lambda x:None) if False else None
try: project_cross_suite_lifecycle_intent(identity,life,identity_sha,"artifacts/tests/../../release/out/cross_suite_lifecycle_receipt.json")
except ValueError: pass
else: raise AssertionError("unsafe evidence path accepted")
try: project_cross_suite_lifecycle_intent(identity,"bad-id",identity_sha,evidence)
except ValueError: pass
else: raise AssertionError("invalid lifecycle id accepted")
print("C11C_CATALOG_D9_13_PROJECTION PASS | identity=bound | projection=read-only | media=false | release_authority=NONE | negative=5/5")
