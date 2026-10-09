from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import production_qualification_contract as contract


def expect(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def reject(label: str, action) -> None:
    try:
        action()
    except contract.QualificationContractError:
        return
    raise AssertionError(f"negative case accepted: {label}")


def main() -> int:
    token = "RUN_C11D_PRODUCTION_QUALIFICATION_NO_RELEASE"
    auth = contract.validate_authorization(ROOT, token)
    expect(auth["status"] == "AUTHORIZED_BOUNDED_QUALIFICATION_ONLY", "authorization status mismatch")
    expect(auth["governance"]["release_authority"] == "NONE", "qualification must not grant release authority")
    expect(auth["governance"]["renderer_activation_for_general_D_requests"] is False, "global D renderer must remain disabled")
    reject("wrong token", lambda: contract.validate_authorization(ROOT, "RUN_ANYTHING"))

    auth_path = ROOT / contract.AUTH_REL
    auth_data = json.loads(auth_path.read_text(encoding="utf-8"))
    for key in (
        "d4_8_global_activation", "general_d_renderer_activation", "unbounded_production_execution",
        "release_or_publishing", "D9_14_FULL_GUI_CERTIFICATION", "D9_15_ACCEPTANCE_CLOSURE",
        "D9_16_FULL_ACCEPTANCE_CLOSURE", "D9_17_CLOSURE", "final_D_BASELINE_FREEZE",
        "C11C_SOURCE_OR_MANIFEST_MUTATION",
    ):
        expect(auth_data["not_authorized"].get(key) is True, f"missing restriction: {key}")
    expect(auth_data["immutable_reference"]["manifest_sha256"] == contract.EXPECTED_C_MANIFEST_SHA256, "C11-C ref hash drift")

    runner = (ROOT / "tools/c11d/d9/run_d9_14_production_qualification.ps1").read_text(encoding="utf-8-sig")
    for marker in (
        "RUN_C11D_PRODUCTION_QUALIFICATION_NO_RELEASE",
        "ChallengeId='CHALLENGE_001'",
        "Grammar='harmonic_membrane'",
        "Family='tracking'",
        "same_seed_loop_video_replay='PASS'",
        "music_seed_changes_audio_identity='PASS'",
        "c11d_editorial_renderer_binding='NOT_CERTIFIED_BY_THIS_RUN'",
        "release_authority='NONE'",
        "sourceBefore -ne $sourceAfter",
    ):
        expect(marker in runner, f"runner lacks required control/qualification marker: {marker}")
    expect("-Force'" not in runner and "Remove-Item -Recurse" not in runner, "runner must not overwrite/delete qualification assets")

    bad_report = {
        "schema": contract.REPORT_SCHEMA,
        "status": "PASS",
        "d9_14_full_acceptance": "PASS",
    }
    reject("cannot relabel qualification as D9.14 closure", lambda: contract.validate_report_shape(bad_report, ROOT))
    bad_report["status"] = "BOUNDED_PRODUCTION_QUALIFICATION_PASS_NOT_D9_14_CLOSURE"
    bad_report["d9_14_full_acceptance"] = "NOT_CLOSED"
    bad_report["d9_15"] = "PASS"
    reject("cannot promote waived D9.15 to PASS", lambda: contract.validate_report_shape(bad_report, ROOT))

    print("C11-D D9.14 PRODUCTION QUALIFICATION CONTRACT PASS | authorization_scope=BOUNDED_ONLY | negative=3/3 | C11-C=IMMUTABLE | general_D_renderer=OFF | release_authority=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
