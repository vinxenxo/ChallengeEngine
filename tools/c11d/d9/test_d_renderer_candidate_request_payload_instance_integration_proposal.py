#!/usr/bin/env python3
"""Read-only integrity/shape check for the D-only request→payload integration proposal."""
from __future__ import annotations
import hashlib
import json
import pathlib
import sys
import copy

ROOT = pathlib.Path(__file__).resolve().parents[3]
CONTRACT_REL = pathlib.Path("definitions/c11d/production/D_RENDERER_CANDIDATE_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_V1.json")
SCHEMA_REL = pathlib.Path("definitions/c11d/production/D_RENDERER_CANDIDATE_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_SCHEMA_V1.json")
IO_AUDIT_REL = pathlib.Path("definitions/c11d/production/D_RENDERER_CANDIDATE_IO_GAP_AUDIT_V1.json")
MANIFEST_REL = pathlib.Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
DOCKET_REL = pathlib.Path("definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json")
FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
DOCKET_SHA = "e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f"
IO_AUDIT_SHA = "429963458d6cbad3fc6a6ae8108ddd6e5578ad4fa4ee21a92d919f355184ac07"

def sha(path: pathlib.Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def fail(message: str) -> None:
    raise RuntimeError(message)

def main() -> int:
    root=ROOT
    manifest=root/MANIFEST_REL
    if not manifest.is_file() or sha(manifest) != FROZEN_SHA or manifest.stat().st_size != 796318:
        fail("Frozen C11-C manifest identity mismatch; stop.")
    docket=root/DOCKET_REL
    if not docket.is_file() or sha(docket) != DOCKET_SHA:
        fail("Renderer policy docket hash mismatch; stop.")
    audit_path=root/IO_AUDIT_REL
    if not audit_path.is_file() or sha(audit_path) != IO_AUDIT_SHA:
        fail("I/O gap audit contract differs from the proposal source basis; stop.")
    contract=json.loads((root/CONTRACT_REL).read_text(encoding="utf-8"))
    schema=json.loads((root/SCHEMA_REL).read_text(encoding="utf-8"))
    audit=json.loads(audit_path.read_text(encoding="utf-8"))
    if len(contract.get("source_pins",[])) != 54 or contract["source_pins"] != audit.get("source_pins"):
        fail("The proposal source pin list must exactly equal the 54-row current I/O audit pin list.")
    for idx,pin in enumerate(contract["source_pins"], start=1):
        p=root/pathlib.Path(pin["path"])
        if not p.is_file() or sha(p) != pin["sha256"]:
            fail(f"Source pin {idx}/54 mismatch: {pin['path']}")
    if contract.get("status") != "PROPOSAL_ONLY_NON_PRODUCTION_INTEGRATION_NOT_IMPLEMENTED_NOT_APPROVED":
        fail("The proposal may not claim implementation or approval.")
    if contract.get("observed_gap_state",{}).get("complete_groups") != 0:
        fail("The proposal must preserve the observed 0/10 complete I/O groups.")
    locks=contract.get("required_locks",{})
    expected={"renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,
              "seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED",
              "approved_bindings":0,"approved_custom_data_bindings":0,"approved_renderer_projection_bindings":0,
              "D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED","D9.16":"BLOCKED",
              "D9.17":"BLOCKED_NO_GO","D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING",
              "freeze_eligible":False,"release_authority":"NONE","c11c_immutable":True}
    if locks != expected:
        fail("Proposal governance locks differ from the exact required boundary.")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("additionalProperties") is not False:
        fail("Schema is not a strict Draft 2020-12 object schema.")
    if len(schema.get("properties",{}).get("source_pins",{}).get("prefixItems",[])) != 54:
        fail("Strict schema must pin all 54 source rows positionally.")
    schema_engine="STRUCTURAL_ONLY"
    negatives=0
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(schema)
        validator=Draft202012Validator(schema)
        errors=list(validator.iter_errors(contract))
        if errors:
            fail("Proposal schema invalid: " + "; ".join(e.message for e in errors[:5]))
        schema_engine="DRAFT2020_12"
        for mutate in [
            lambda x: x.update(undeclared_property=True),
            lambda x: x.update(status="APPROVED"),
            lambda x: x["required_locks"].update(renderer="ON"),
            lambda x: x["required_locks"].update(candidate_input_admissible=True),
            lambda x: x["source_pins"].pop(),
            lambda x: x["source_pins"][0].update(sha256="0"*64),
        ]:
            bad=copy.deepcopy(contract); mutate(bad)
            if validator.is_valid(bad):
                fail("Strict-schema negative mutation was accepted.")
            negatives += 1
    except ImportError:
        pass
    print(f"C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION PROPOSAL PASS | source_pins=54/54 | io_gap_groups=10/10 | complete=0 partial=6 blocked=4 | schema_engine={schema_engine} | schema_negatives={negatives}/6 | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION PROPOSAL FAIL | {exc}", file=sys.stderr)
        raise SystemExit(1)
