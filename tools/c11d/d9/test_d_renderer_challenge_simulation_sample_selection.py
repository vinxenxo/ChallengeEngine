from __future__ import annotations
import ast, copy, json, sys, tempfile, shutil
from pathlib import Path
from typing import Any, Callable
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
from d_renderer_challenge_simulation_sample_selection import (
    build_sample_selection_preview, validate_sample_selection_preview,
    ChallengeSampleSelectionError, _nearest_delivery_tick_half_up,
)

def _reject(label: str, action: Callable[[], Any]) -> None:
    try: action()
    except (ChallengeSampleSelectionError, ValueError, TypeError, KeyError, AssertionError): return
    raise AssertionError(f"Expected fail-closed rejection: {label}")

def run_checks() -> dict[str, int]:
    source = (HERE / "d_renderer_challenge_simulation_sample_selection.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_modules = {"subprocess", "socket", "multiprocessing", "ffmpeg", "godot", "requests", "urllib"}
    forbidden_calls = {"write_text", "write_bytes", "Popen", "system", "startfile", "run", "call", "check_call", "check_output", "unlink", "mkdir", "makedirs", "replace", "rename"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): assert not any(alias.name.split(".")[0] in forbidden_modules for alias in node.names)
        elif isinstance(node, ast.ImportFrom): assert (node.module or "").split(".")[0] not in forbidden_modules
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute): assert node.func.attr not in forbidden_calls, f"Persistence/dispatch call forbidden: {node.func.attr}"
    contract = json.loads((ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json").read_text(encoding="utf-8-sig"))
    schema = json.loads((ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PREVIEW_SCHEMA_V1.json").read_text(encoding="utf-8-sig"))
    assert contract["sampling_policy"]["state"] == "PROPOSED_NOT_APPROVED"
    assert contract["sampling_policy"]["interpolation"] == "NONE"
    assert contract["approval_state"]["simulation_sample_selection_policy_approved"] is False
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema" and schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        Draft202012Validator = None
    if Draft202012Validator is not None: Draft202012Validator.check_schema(schema)
    candidate = build_sample_selection_preview(ROOT)
    assert candidate == build_sample_selection_preview(ROOT)
    assert validate_sample_selection_preview(candidate, ROOT) is True
    assert candidate["proposal_state"] == "PROPOSED_NOT_APPROVED"
    assert candidate["source_timebase"] == {"fps":60,"total_frames":900}
    assert candidate["delivery_timebase"] == {"fps":30,"total_frames":450}
    assert candidate["game_segment"] == {"source_start_frame":180,"source_end_frame_exclusive":600,"source_snapshot_count":420,"delivery_start_frame":90,"delivery_end_frame_exclusive":300,"delivery_snapshot_count":210,"duration_seconds":7}
    samples = candidate["samples"]
    assert len(samples) == 210
    assert samples[0] == {"delivery_game_frame_index":0,"delivery_absolute_frame_index":90,"source_game_snapshot_index":0,"source_absolute_frame_index":180}
    assert samples[-1] == {"delivery_game_frame_index":209,"delivery_absolute_frame_index":299,"source_game_snapshot_index":418,"source_absolute_frame_index":598}
    assert all(row["source_game_snapshot_index"] == row["delivery_game_frame_index"]*2 for row in samples)
    assert all(row["source_absolute_frame_index"] == row["delivery_absolute_frame_index"]*2 for row in samples)
    assert candidate["sample_assessment"]["source_index_sha256"]
    assert candidate["sample_assessment"]["interpolation_used"] is False
    assert candidate["anchor_mapping"] == {
        "winning_frame_local_game_index":394,
        "winning_frame_absolute_source_index":574,
        "winning_delivery_game_frame_index":197,
        "winning_absolute_delivery_frame_index":287,
        "anchor_mapping_status":"EXACT_SELECTED_SAMPLE_AND_DELIVERY_TICK",
        "winning_source_snapshot_selected":True,
        "source_frame_rounding_error_numerator":0,
        "source_frame_rounding_error_denominator":1,
        "close_calls_count":1,
        "close_calls_used_for_timing":False,
    }
    # Explicit half-up behavior for a hypothetical odd source anchor (not part of the pinned run).
    assert _nearest_delivery_tick_half_up(394,60,30) == 197
    assert _nearest_delivery_tick_half_up(395,60,30) == 198
    assert _nearest_delivery_tick_half_up(393,60,30) == 197  # exact half tie rounds later
    counts = {"deterministic":1,"frame_map":1,"anchor":1,"governance":1,"schema":1,"source_lineage":1}
    if Draft202012Validator is not None:
        Draft202012Validator(schema).validate(candidate); counts["jsonschema"] = 1
    else: counts["jsonschema"] = 0
    base = candidate
    mutations = [
        ("status escalation", lambda x:x.update(status="APPROVED_RENDERER_INPUT")),
        ("proposal approval escalation", lambda x:x.update(proposal_state="APPROVED")),
        ("policy state escalation", lambda x:x["sampling_policy"].update(state="APPROVED")),
        ("stride mutation", lambda x:x["sampling_policy"].update(source_snapshot_stride=1)),
        ("interpolation mutation", lambda x:x["sampling_policy"].update(interpolation="LINEAR")),
        ("sample count mutation", lambda x:x["samples"].pop()),
        ("duplicate output index", lambda x:x["samples"][1].update(delivery_game_frame_index=0)),
        ("source cadence mutation", lambda x:x["samples"][1].update(source_game_snapshot_index=3)),
        ("anchor mutation", lambda x:x["anchor_mapping"].update(winning_absolute_delivery_frame_index=288)),
        ("close_calls used as timing", lambda x:x["anchor_mapping"].update(close_calls_used_for_timing=True)),
        ("payload mutation escalation", lambda x:x["sampling_policy"].update(canonical_payload_mutation=True)),
        ("renderer dispatch escalation", lambda x:x["governance"].update(renderer_dispatch_invoked=True)),
        ("media escalation", lambda x:x["governance"].update(media_created=True)),
        ("D4.8 escalation", lambda x:x["governance"].update(d4_8="AUTHORIZED")),
        ("release authority escalation", lambda x:x["governance"].update(release_authority="GRANTED")),
        ("manifest identity mutation", lambda x:x.update(frozen_c11c_manifest_sha256="0"*64)),
        ("approval-state mutation", lambda x:x["approval_state"].update(simulation_sample_selection_policy_approved=True)),
        ("preview digest corruption", lambda x:x.update(preview_sha256="0"*64)),
    ]
    negatives=0
    for label, mutate in mutations:
        mutated=copy.deepcopy(base); mutate(mutated)
        # Recompute digest for all cases except the digest-corruption test to ensure semantic gates reject them.
        if label != "preview digest corruption":
            import hashlib
            obj={k:v for k,v in mutated.items() if k!="preview_sha256"}
            mutated["preview_sha256"]=hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")).hexdigest()
        _reject(label, lambda m=mutated:validate_sample_selection_preview(m,ROOT))
        negatives+=1
    _reject("unsupported sample cadence", lambda: _nearest_delivery_tick_half_up(-1,60,30)); negatives+=1
    _reject("zero source FPS", lambda: _nearest_delivery_tick_half_up(1,0,30)); negatives+=1
    _reject("zero delivery FPS", lambda: _nearest_delivery_tick_half_up(1,60,0)); negatives+=1
    _reject("bool index", lambda: _nearest_delivery_tick_half_up(True,60,30)); negatives+=1
    assert negatives == 22
    counts["negative"] = negatives
    return counts

def main() -> int:
    r=run_checks()
    print("C11-D RENDERER CHALLENGE SIMULATION SAMPLE-SELECTION PROPOSAL PASS"
      + f" | source_samples={420}@60FPS | delivery_samples={210}@30FPS"
      + f" | cadence=2:1_EVEN_SOURCE_INDICES | interpolation=NONE"
      + f" | winning_frame=574_TO_DELIVERY_287 | close_calls=COUNT_ONLY"
      + f" | deterministic={r['deterministic']}/1 | lineage={r['source_lineage']}/1 | schema={r['schema']}/1"
      + (f" | jsonschema={r['jsonschema']}/1" if r['jsonschema'] else " | jsonschema=NOT_INSTALLED (structural checks PASS)")
      + f" | negative={r['negative']}/22 | policy=PROPOSED_NOT_APPROVED"
      + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0
if __name__ == "__main__": raise SystemExit(main())
