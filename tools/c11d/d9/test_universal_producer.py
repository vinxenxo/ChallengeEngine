from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

from universal_editorial_model import build_catalog  # noqa: E402
from universal_producer import (  # noqa: E402
    PLAN_SCHEMA_ID,
    REQUEST_SCHEMA_ID,
    UniversalProducerError,
    evaluate_universal_request,
    normalize_universal_request,
)


def _raw(selection: dict, request_id: str = "D99-TEST-001") -> dict:
    return {
        "schema": REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": selection,
        "seed": 12345,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {
            "title": "  TEXTO EDITORIAL  ",
            "subtitle": "Subtítulo",
            "call_to_action": "Continuar",
            "language": " ES ",
            **({"player_name": "ANA", "challenge_label": "RETO"} if selection.get("content_type") == "challenges" else {}),
        },
        "provenance": {"source_revision": "C11D-D9.9-PRODUCER-0.11.0", "request_origin": "GUI"},
    }


def _all_selections() -> tuple[list[dict], dict[str, int]]:
    catalog = build_catalog(ROOT)
    out: list[dict] = []
    challenges = 0
    loops = 0
    drills = 0
    for family in catalog["content_types"]["challenges"]["families"]:
        for variant in family["variants"]:
            out.append({"content_type": "challenges", "family_id": family["id"], "variant_id": variant["id"]})
            challenges += 1
    for family in catalog["content_types"]["visual_loops"]["families"]:
        for subtype in family["subtypes"]:
            out.append({"content_type": "visual_loops", "family_id": family["id"], "subtype_id": subtype["id"]})
            loops += 1
    for family in catalog["content_types"]["visual_drills"]["families"]:
        for variant in family["variants"]:
            out.append({"content_type": "visual_drills", "family_id": family["id"], "variant_id": variant["id"]})
            drills += 1
    return out, {"challenges": challenges, "loop_selector_variants_including_auto": loops, "drill_variants": drills}


def run_checks() -> dict[str, int]:
    selections, counts = _all_selections()
    assert counts == {"challenges": 9, "loop_selector_variants_including_auto": 32, "drill_variants": 20}, counts
    results = []
    cli_cases = 0
    with tempfile.TemporaryDirectory(prefix="c11d_d99_parity_") as temp:
        temp_path = Path(temp)
        for index, selection in enumerate(selections, start=1):
            request = _raw(selection, f"D99-MATRIX-{index:03d}")
            gui_result = evaluate_universal_request(request, ROOT)
            assert gui_result["status"] == "PLANNED"
            assert gui_result["plan"]["schema"] == PLAN_SCHEMA_ID
            assert gui_result["plan"]["seed"] == request["seed"]
            assert gui_result["plan"]["music_seed"] == request["music_seed"]
            assert gui_result["renderer"] is False and gui_result["execution"] is False
            assert gui_result["plan"]["renderer_activation"] is False
            assert gui_result["plan"]["production_execution"] is False
            assert gui_result["plan"]["release_authority"] == "NONE"
            assert gui_result["plan"]["simulation_truth_mutation"] is False
            if selection["content_type"] == "challenges":
                assert gui_result["d4_evidence"]["status"] == "PASS"
                assert gui_result["plan"]["plan_kind"] == "UNIVERSAL_PLAN_WITH_CANONICAL_D4_CHALLENGE_SUBPLAN"
            else:
                assert gui_result["d4_evidence"] is None
                assert gui_result["plan"]["plan_kind"] == "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY"
            results.append((selection, request, gui_result))

        # Run an actual separate CLI process for one valid selection of every supported type.
        # All 61 identities were already resolved above; the full GUI/CLI process parity is
        # then proven through the same serialized request boundary once per type.
        representatives = {}
        for selection, request, gui_result in results:
            content_type = selection["content_type"]
            if content_type not in representatives:
                if content_type == "visual_loops" and selection.get("subtype_id") == "auto":
                    continue
                representatives[content_type] = (request, gui_result)
        assert set(representatives) == {"challenges", "visual_loops", "visual_drills"}
        for index, (content_type, pair) in enumerate(sorted(representatives.items()), start=100):
            request, gui_result = pair
            request_path = temp_path / f"request-cli-{index}.json"
            request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
            cli = subprocess.run(
                [sys.executable, str(HERE / "universal_producer_cli.py"), "--request", str(request_path), "--print-json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )
            assert cli.returncode == 0, cli.stdout + "\n" + cli.stderr
            cli_result = json.loads(cli.stdout)
            assert cli_result["canonical_request"] == gui_result["canonical_request"], content_type
            assert cli_result["request_hash"] == gui_result["request_hash"], content_type
            assert cli_result["plan"] == gui_result["plan"], content_type
            assert cli_result["plan_hash"] == gui_result["plan_hash"], content_type
            cli_cases += 1

    # Text normalization and identity changes must not mutate either seed domain.
    base_request = _raw({"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"})
    base = evaluate_universal_request(base_request, ROOT)
    changed = copy.deepcopy(base_request)
    changed["production_override"]["title"] = "OTRO TÍTULO"
    result_changed = evaluate_universal_request(changed, ROOT)
    assert base["plan"]["seed"] == result_changed["plan"]["seed"] == 12345
    assert base["plan"]["music_seed"] == result_changed["plan"]["music_seed"] == 840001
    assert base["editorial_hash"] != result_changed["editorial_hash"]
    assert base["plan_hash"] != result_changed["plan_hash"]
    assert base["canonical_request"]["editorial"]["title"] == "TEXTO EDITORIAL"
    assert base["canonical_request"]["editorial"]["language"] == "es"

    # GUI-vs-CLI provenance is intentionally normalized out of semantic identity.
    gui_origin = copy.deepcopy(base_request)
    cli_origin = copy.deepcopy(base_request)
    gui_origin["provenance"]["request_origin"] = "GUI"
    cli_origin["provenance"]["request_origin"] = "CLI"
    a = evaluate_universal_request(gui_origin, ROOT)
    b = evaluate_universal_request(cli_origin, ROOT)
    assert a["canonical_request"] == b["canonical_request"]
    assert a["plan_hash"] == b["plan_hash"]

    # Strict negatives across selector identity, protected fields, missing seeds and unsupported Longform.
    negative_cases = []
    def rejects(name: str, mutate) -> None:
        item = copy.deepcopy(base_request)
        mutate(item)
        try:
            normalize_universal_request(item, ROOT)
        except (UniversalProducerError, ValueError, TypeError, KeyError):
            negative_cases.append(name)
        else:
            raise AssertionError(f"Expected D9.9 rejection: {name}")

    rejects("unknown_content_type", lambda r: r["selection"].update(content_type="unknown"))
    rejects("unknown_loop_family", lambda r: r["selection"].update(family_id="made_up_family"))
    rejects("unknown_loop_subtype", lambda r: r["selection"].update(subtype_id="made_up_grammar"))
    rejects("loop_native_variant_not_declared", lambda r: r["selection"].update(variant_id="variant-2"))
    rejects("longform_disabled", lambda r: r.update(selection={"content_type": "longform"}))
    rejects("missing_gameplay_seed", lambda r: r.pop("seed"))
    rejects("missing_music_seed", lambda r: r.pop("music_seed"))
    rejects("boolean_seed", lambda r: r.update(seed=True))
    rejects("non_editorial_seed", lambda r: r["production_override"].update(seed="123"))
    rejects("winning_frame_truth", lambda r: r["production_override"].update(winning_frame=42))
    rejects("telemetry_duration", lambda r: r["production_override"].update(duration_seconds="30"))
    rejects("unsupported_loop_player_name", lambda r: r["production_override"].update(player_name="ANA"))
    rejects("reserved_field", lambda r: r["production_override"].update(show_header=True))
    rejects("overlong_text", lambda r: r["production_override"].update(title="x" * 161))
    rejects("bad_audio_flag", lambda r: r.update(audio_enabled="yes"))
    rejects("unknown_top_level", lambda r: r.update(arbitrary=True))
    rejects("unknown_selection_key", lambda r: r["selection"].update(variant="x"))
    rejects("personalization_disabled_with_values", lambda r: r.update(personalization_enabled=False))
    rejects("unknown_provenance_field", lambda r: r["provenance"].update(secret="x"))
    rejects("bad_request_id", lambda r: r.update(request_id="D99 bad id"))
    assert len(negative_cases) == 20, negative_cases

    # Challenge path must preserve the original D4 canonical proof and independent seeds.
    challenge = _raw({"content_type": "challenges", "family_id": "key", "variant_id": "CHALLENGE_001"}, "D99-CHALLENGE-PARITY")
    challenge_a = evaluate_universal_request(challenge, ROOT)
    challenge_b_request = copy.deepcopy(challenge)
    challenge_b_request["production_override"]["title"] = "Challenge edit"
    challenge_b = evaluate_universal_request(challenge_b_request, ROOT)
    assert challenge_a["d4_evidence"]["status"] == "PASS"
    assert challenge_a["plan"]["seed"] == challenge_b["plan"]["seed"]
    assert challenge_a["plan"]["music_seed"] == challenge_b["plan"]["music_seed"]
    assert challenge_a["d4_evidence"]["plan_hash"] != challenge_b["d4_evidence"]["plan_hash"]

    return {
        "challenge_variants": counts["challenges"],
        "loop_family_grammar_selectors": counts["loop_selector_variants_including_auto"],
        "drill_variants": counts["drill_variants"],
        "gui_cli_matrix_cases": cli_cases,
        "negative_cases": len(negative_cases),
    }


if __name__ == "__main__":
    result = run_checks()
    print(
        "C11-D D9.9 UNIVERSAL PRODUCER PASS | "
        f"challenge={result['challenge_variants']}/9 | "
        f"loop_selectors={result['loop_family_grammar_selectors']} (27 concrete + 5 auto) | "
        f"drill_variants={result['drill_variants']}/20 | "
        f"GUI/CLI parity={result['gui_cli_matrix_cases']}/{result['gui_cli_matrix_cases']} | "
        f"negative={result['negative_cases']}/20 | renderer=OFF | release_authority=NONE"
    )
