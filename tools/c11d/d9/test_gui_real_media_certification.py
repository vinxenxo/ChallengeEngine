from __future__ import annotations
import copy
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import gui_real_media_certification as gate_module


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    gate=gate_module.run_preflight(ROOT)
    expect(gate["status"]=="BLOCKED","D9.14 must remain blocked pending future D baseline + D4.8 authorization")
    expect(gate["case_count"]==10 and len(gate["cases"])==10,"D9.14 end-to-end case matrix must remain 10/10")
    expect(gate["operator_execution_authorized"] is False,"operator execution must not be authorized by a preflight")
    expect(gate["governance"]["renderer_activation"] is False and gate["governance"]["production_execution"] is False,"renderer/production must remain disabled")
    expect(gate["governance"]["media_output_created"] is False and gate["governance"]["output_artifact_path"] is None,"preflight must create no media/path")
    expect(gate["governance"]["d4_8"]=="BLOCKED" and gate["governance"]["release_authority"]=="NONE","D4.8/release authority must stay blocked")
    expect(gate["governance"]["gameplay_seed_source"]=="request.seed" and gate["governance"]["music_seed_source"]=="request.music_seed","seed sources must remain explicit and separate")
    expect(gate["unsupported_content_types"]["longform"]=="DISABLED_UNTIL_CANONICAL_D_REQUEST_SUPPORTS_LONGFORM","Longform must remain disabled")
    expect(len(gate["gate_sha256"])==64,"D9.14 gate must be sealed with SHA-256")
    validated=gate_module.validate_certification_gate(gate,ROOT)
    expect(validated["status"]=="PASS_GATE_BLOCKED_AS_REQUIRED","validator result mismatch")

    negative=0
    def reject(label, mutate, reseal=True):
        nonlocal negative
        candidate=copy.deepcopy(gate)
        mutate(candidate)
        if reseal:
            candidate=gate_module._seal(candidate)
        try:
            gate_module.validate_certification_gate(candidate,ROOT)
        except gate_module.CertificationGateError:
            negative+=1
        else:
            raise AssertionError(f"D9.14 negative unexpectedly accepted: {label}")
    reject("status unlock",lambda x:x.update(status="READY"))
    reject("gate result unlock",lambda x:x.update(gate_result="PASS_REAL_MEDIA_AUTHORIZED"))
    reject("operator authorization",lambda x:x.update(operator_execution_authorized=True))
    reject("renderer activation",lambda x:x["governance"].update(renderer_activation=True))
    reject("renderer adapter",lambda x:x["governance"].update(renderer_adapter_invoked=True))
    reject("renderer input",lambda x:x["governance"].update(renderer_input_emitted=True))
    reject("production execution",lambda x:x["governance"].update(production_execution=True))
    reject("media created",lambda x:x["governance"].update(media_output_created=True))
    reject("artifact path",lambda x:x["governance"].update(output_artifact_path="artifacts/fake.mp4"))
    reject("D4.8 override",lambda x:x["governance"].update(d4_8="AUTHORIZED"))
    reject("release authority",lambda x:x["governance"].update(release_authority="GRANTED"))
    reject("gameplay seed altered",lambda x:x["governance"].update(gameplay_seed_source="music_seed"))
    reject("seed sharing allowed",lambda x:x["governance"].update(cross_domain_seed_sharing="ALLOWED"))
    reject("case promoted",lambda x:x["cases"][0].update(status="PASS_REAL_MEDIA",executed=True))
    reject("case media claim",lambda x:x["cases"][1].update(media_created=True))
    reject("longform unsupported override",lambda x:x["unsupported_content_types"].update(longform="SUPPORTED"))
    reject("missing blocker",lambda x:x.update(blockers=["NONE"]))
    reject("case reorder",lambda x:x["cases"].reverse())
    reject("freeze manifest hash",lambda x:x["references"].update(historical_c11c_manifest_sha256="0"*64))
    # Raw unsealed tamper test proves integrity seal detection independently of semantic negatives.
    reject("raw gate hash tamper",lambda x:x.update(status="READY"),reseal=False)
    expect(negative==20,f"negative controls count mismatch: {negative}/20")

    # GUI and Test surfaces must expose the same gate, but no route may launch real production.
    producer=(ROOT/"c11c-suite/c11c-producer/main.py").read_text(encoding="utf-8")
    producer_contract=json.loads((ROOT/"c11c-suite/c11c-producer/BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    test_manifest=json.loads((ROOT/"c11c-suite/c11c-test/BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    config_manifest=json.loads((ROOT/"c11c-suite/c11c-config/BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    expect("D9.14 · REAL-MEDIA CERTIFICATION GATE (BLOCKED)" in producer,"Producer GUI gate view missing")
    expect("def _run_d914_certification_preflight(" in producer,"Producer preflight callback missing")
    expect(producer_contract.get("d9_14_real_media_execution") is False and producer_contract.get("d9_14_renderer_activation") is False,"Producer manifest must be non-executing")
    expect(any(row.get("name")=="D9.14 REAL GUI PRODUCTION CERTIFICATION GATE (BLOCKED)" for row in test_manifest.get("gui_routes",[])),"Test route missing")
    expect(config_manifest.get("d9_14_renderer_activation") is False and config_manifest.get("d9_14_production_execution") is False,"Config manifest must not grant D9.14 execution")
    print(f"C11-D D9.14 REAL GUI PRODUCTION CERTIFICATION GATE PASS | gate=BLOCKED_AS_REQUIRED | cases=10/10 | negative={negative}/20 | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
