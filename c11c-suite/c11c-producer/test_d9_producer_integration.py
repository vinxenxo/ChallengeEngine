from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

from c11d_gui_request import (  # noqa: E402
    build_production_request,
    evaluate_gui_request,
    resolve_delivery_profile_data,
)


def _request(challenge, profile_id, profile, mode, request_id, enabled=True, player_name="ANA"):
    content = challenge.get("content") or {}
    values = {
        "title": str(content.get("hook", "")),
        "subtitle": "OBSERVA CADA MOVIMIENTO",
        "call_to_action": str(content.get("cta", "")),
        "language": "es",
        "player_name": player_name,
        "challenge_label": str(challenge.get("mechanic", "UNKNOWN")).upper(),
    }
    return build_production_request(
        request_id=request_id,
        mode=mode,
        challenge_document=challenge,
        delivery_profile_id=profile_id,
        resolved_delivery_profile=profile,
        seed=12345,
        music_seed=840001,
        audio_enabled=True,
        variation_index=0,
        personalization_enabled=enabled,
        editorial_values=values,
    )


def run_checks() -> dict[str, int]:
    challenges = {}
    for path in sorted((PROJECT / "challenges").glob("CHALLENGE_*.json")):
        item = json.loads(path.read_text(encoding="utf-8-sig"))
        challenges[str(item["challenge_id"])] = item
    assert len(challenges) == 9, f"expected 9 challenges, got {len(challenges)}"

    delivery_config = json.loads(
        (PROJECT / "profiles" / "delivery" / "c11c_video_delivery_profiles.json").read_text(encoding="utf-8-sig")
    )
    profile_ids = [
        "MASTER_1080",
        "REVIEW_720",
        "MIN_540",
        "META_REELS_FINAL_V1",
        "LONGFORM_1080",
    ]
    assert set(profile_ids).issubset(set(delivery_config["profiles"]))

    count_core = 0
    for challenge_id, challenge in sorted(challenges.items()):
        for profile_id in profile_ids:
            _resolved_id, profile = resolve_delivery_profile_data(profile_id, delivery_config)
            for mode in ("REVIEW", "PRODUCTION"):
                request = _request(
                    challenge,
                    profile_id,
                    profile,
                    mode,
                    f"D951-CORE-{challenge_id}-{profile_id}-{mode}",
                )
                result = evaluate_gui_request(request, PROJECT)
                assert result["parity"]["status"] == "PASS"
                assert result["plan"]["mode"] == mode
                assert result["plan"]["delivery_profile_id"] == profile_id
                assert result["plan"]["runtime_authority"] == "NONE"
                assert result["plan"]["renderer_activation"] is False
                assert result["plan"]["orchestrator_execution"] is False
                assert result["execution"] is False and result["renderer"] is False
                assert result["release_authority"] == "NONE"
                count_core += 1

    count_personalization = 0
    selected_ids = sorted(challenges)[:3]
    for challenge_id in selected_ids:
        challenge = challenges[challenge_id]
        profile_id = "REVIEW_720"
        _resolved_id, profile = resolve_delivery_profile_data(profile_id, delivery_config)
        for mode in ("REVIEW", "PRODUCTION"):
            for enabled in (False, True):
                request = _request(
                    challenge,
                    profile_id,
                    profile,
                    mode,
                    f"D951-PERSONAL-{challenge_id}-{mode}-{int(enabled)}",
                    enabled=enabled,
                    player_name="ANA",
                )
                result = evaluate_gui_request(request, PROJECT)
                expected_profile = "editorial_text_v1" if enabled else "none_v1"
                assert result["resolved_personalization"]["profile_id"] == expected_profile
                assert result["parity"]["status"] == "PASS"
                count_personalization += 1

    baseline_challenge = challenges[selected_ids[0]]
    _resolved_id, review_profile = resolve_delivery_profile_data("REVIEW_720", delivery_config)
    baseline = _request(
        baseline_challenge, "REVIEW_720", review_profile, "REVIEW", "D951-TEXT-MUTATION", True, "ANA"
    )
    changed = copy.deepcopy(baseline)
    changed["personalization"]["values"]["player_name"] = "LUIS"
    changed["editorial"]["title"] = "TEXTO MODIFICADO"
    changed["provenance"]["request_origin"] = "GUI"
    result_a = evaluate_gui_request(baseline, PROJECT)
    result_b = evaluate_gui_request(changed, PROJECT)
    assert result_a["request"]["seed"] == result_b["request"]["seed"] == 12345
    assert result_a["request"]["music_seed"] == result_b["request"]["music_seed"] == 840001
    assert result_a["personalization_hash"] != result_b["personalization_hash"]
    assert result_a["plan_hash"] != result_b["plan_hash"]

    negative_count = 0
    missing_music = copy.deepcopy(baseline)
    missing_music.pop("music_seed")
    try:
        evaluate_gui_request(missing_music, PROJECT)
    except (ValueError, TypeError, KeyError):
        negative_count += 1
    else:
        raise AssertionError("D4.2 should reject a missing music_seed")

    forbidden_truth = copy.deepcopy(baseline)
    forbidden_truth["winning_frame"] = 99
    try:
        evaluate_gui_request(forbidden_truth, PROJECT)
    except (ValueError, TypeError, KeyError):
        negative_count += 1
    else:
        raise AssertionError("D4.2 should reject forbidden winning_frame input")

    forbidden_personalization = copy.deepcopy(baseline)
    forbidden_personalization["personalization"]["values"]["seed"] = "999"
    try:
        evaluate_gui_request(forbidden_personalization, PROJECT)
    except (ValueError, TypeError, KeyError):
        negative_count += 1
    else:
        raise AssertionError("D4.3 should reject unallowlisted seed personalization")

    cycle = {"profiles": {"A": {"alias_of": "B"}, "B": {"alias_of": "A"}}}
    try:
        resolve_delivery_profile_data("A", cycle)
    except ValueError:
        negative_count += 1
    else:
        raise AssertionError("delivery profile alias cycle must be rejected")

    assert count_core == 90, count_core
    assert count_personalization == 12, count_personalization
    assert negative_count == 4, negative_count
    return {
        "core_cases": count_core,
        "personalization_cases": count_personalization,
        "negative_cases": negative_count,
    }


if __name__ == "__main__":
    counts = run_checks()
    print(
        "C11-D D9.5.1 Producer GUI integration PASS | "
        f"core={counts['core_cases']}/90 | personalization={counts['personalization_cases']}/12 | "
        f"negative={counts['negative_cases']}/4 | renderer=OFF | release_authority=NONE"
    )
