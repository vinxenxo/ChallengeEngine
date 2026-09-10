#!/usr/bin/env python3
"""C6-D4 phase-duration contract audit.

Validates the declarative fixture timelines against the production factory's
Python timeline builder without executing Godot. Runtime rendering remains
required for final E2E certification.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build_factory import build_timeline_from_definition  # noqa: E402

EXPECTED = {
    "CHALLENGE_001": (["GAME", "CTA"], 540),
    "CHALLENGE_002": (["HOOK", "GAME"], 600),
    "CHALLENGE_005": (["GAME"], 420),
    "CHALLENGE_006": (["GAME", "CTA"], 540),
    "CHALLENGE_007": (["HOOK", "GAME"], 600),
}


def effective_phases(video):
    phases = []
    for key, name in (("hook_duration", "HOOK"), ("game_duration", "GAME"), ("reveal_duration", "REVEAL"), ("cta_duration", "CTA")):
        if float(video.get(key, 0.0)) > 0:
            phases.append(name)
    return phases


def main():
    for challenge_id, (expected_sequence, expected_frames) in EXPECTED.items():
        cfg = json.loads((ROOT / "challenges" / f"{challenge_id}.json").read_text())
        timeline = build_timeline_from_definition(cfg["video"])
        phases = effective_phases(cfg["video"])
        if phases != expected_sequence:
            raise AssertionError(f"{challenge_id}: phases={phases}, expected={expected_sequence}")
        if timeline["total_frames"] != expected_frames:
            raise AssertionError(f"{challenge_id}: total_frames={timeline['total_frames']}, expected={expected_frames}")
        if timeline["game_frames"] <= 0:
            raise AssertionError(f"{challenge_id}: GAME must remain active")
        print(f"[C6_D4_PHASE_CONTRACT] {challenge_id} PASS -> {phases} -> {expected_frames} frames")
    print("[C6_D4_PHASE_CONTRACT_SUITE] PASS")


if __name__ == "__main__":
    main()
