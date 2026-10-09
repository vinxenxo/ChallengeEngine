"""Focused contract/regression tests for the non-executable D renderer candidate preview."""
from __future__ import annotations

import ast
import copy
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_render_adapter import prepare_d_only_adapter_envelope
from d_renderer_candidate import (
    DRendererCandidateError,
    PREVIEW_SCHEMA,
    build_renderer_binding_preview,
    sha256_json,
    validate_renderer_binding_preview,
    _load_spec,
    SPEC_REL,
)
from editorial_render_bridge import build_bridge_planning_record
from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from test_editorial_render_bridge import _raw, _representative_selections


def _envelope(selection: dict, request_id: str, *, title: str = "Candidate preview", seed: int = 12345, music_seed: int = 840001, delivery_profile: str = "REVIEW_720", presentation_profile: str = "social_default_v1", audio_enabled: bool = True) -> dict:
    request = _raw(selection, request_id)
    request["seed"] = seed
    request["music_seed"] = music_seed
    request["delivery_profile_id"] = delivery_profile
    request["presentation_profile_id"] = presentation_profile
    request["audio_enabled"] = audio_enabled
    request["production_override"]["title"] = title
    result = evaluate_universal_request(request, ROOT)
    record = build_bridge_planning_record(result, ROOT)
    return prepare_d_only_adapter_envelope(result, record, ROOT)


def _reseal_adapter(envelope: dict) -> dict:
    envelope["envelope_hash"] = sha256_json({key: value for key, value in envelope.items() if key != "envelope_hash"})
    return envelope


def _reseal_preview(preview: dict) -> dict:
    preview["preview_sha256"] = sha256_json({key: value for key, value in preview.items() if key != "preview_sha256"})
    return preview


def _must_reject(label: str, action) -> None:
    try:
        action()
    except (DRendererCandidateError, ValueError, TypeError, KeyError):
        return
    raise AssertionError(f"Expected fail-closed rejection: {label}")


def run_checks() -> dict[str, int]:
    # Static guard: the candidate mapper must remain a pure JSON transformation.
    implementation_tree = ast.parse((HERE / "d_renderer_candidate.py").read_text(encoding="utf-8"))
    forbidden_modules = {"subprocess", "ffmpeg", "godot", "os"}
    for node in ast.walk(implementation_tree):
        if isinstance(node, ast.Import):
            assert not any(alias.name.split(".")[0] in forbidden_modules for alias in node.names), "Renderer/process modules must not be imported"
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] not in forbidden_modules, "Renderer/process modules must not be imported"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in {"write_text", "write_bytes", "Popen", "system", "startfile"}, "Candidate mapper may not write files or launch processes"

    representatives = _representative_selections()
    previews = {}
    positive = 0
    deterministic = 0
    for content_type in ("challenges", "visual_loops", "visual_drills"):
        envelope = _envelope(representatives[content_type], f"D-RENDER-CANDIDATE-{content_type.upper()}")
        preview = build_renderer_binding_preview(envelope, ROOT)
        repeated = build_renderer_binding_preview(copy.deepcopy(envelope), ROOT)
        assert preview == repeated, content_type
        assert preview["schema"] == PREVIEW_SCHEMA
        assert preview["status"] == "PREPARATION_ONLY_NOT_RENDERER_INPUT"
        assert preview["content_identity"]["content_type"] == content_type
        assert preview["source_identity"]["adapter_envelope_hash"] == envelope["envelope_hash"]
        assert preview["delivery_profile"]["resolved_profile_id"] == "REVIEW_720"
        assert preview["delivery_profile"]["profile"]["width"] == 720
        assert preview["delivery_profile"]["profile"]["height"] == 1280
        assert preview["source_contract_identities"]["adapter_contract_canonical_sha256"] == envelope["adapter_contract_identity"]["sha256"]
        assert preview["source_contract_identities"]["editorial_model_canonical_sha256"] == envelope["editorial_model_identity"]["sha256"]
        assert preview["seed_contract"]["gameplay_seed"] == 12345
        assert preview["seed_contract"]["music_seed"] == 840001
        assert preview["seed_contract"]["cross_domain_seed_sharing"] == "FORBIDDEN"
        assert preview["truth_and_telemetry"] == {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"}
        assert validate_renderer_binding_preview(preview, envelope, ROOT) is True
        boundary = preview["execution_boundary"]
        assert boundary == {
            "candidate_mode": "NON_EXECUTABLE_BINDING_REVIEW",
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "output_artifact_path": None,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": False,
        }
        field_names = {item["source_field"] for item in preview["editorial_binding_preview"]}
        assert field_names <= set(envelope["binding_preview"]["editorial_allowlist_fields"])
        assert all(item["mapping_state"] == "PROPOSED_NOT_APPROVED" for item in preview["editorial_binding_preview"])
        previews[content_type] = (envelope, preview)
        positive += 1
        deterministic += 1

    # A genuine editorial change must change the preview and its declared value hash,
    # while both seed domains remain fixed.
    loop_selection = representatives["visual_loops"]
    base_envelope = _envelope(loop_selection, "D-RENDER-EDITORIAL-DELTA", title="Base title")
    changed_envelope = _envelope(loop_selection, "D-RENDER-EDITORIAL-DELTA", title="Changed title")
    base_preview = build_renderer_binding_preview(base_envelope, ROOT)
    changed_preview = build_renderer_binding_preview(changed_envelope, ROOT)
    assert base_preview["preview_sha256"] != changed_preview["preview_sha256"]
    assert base_preview["seed_contract"] == changed_preview["seed_contract"]
    assert base_preview["editorial_binding_preview"] != changed_preview["editorial_binding_preview"]

    # Independent music-seed changes alter only the music-domain value, not the gameplay seed.
    music_changed = _envelope(loop_selection, "D-RENDER-MUSIC-SEED-DELTA", seed=12345, music_seed=840002)
    music_preview = build_renderer_binding_preview(music_changed, ROOT)
    assert music_preview["seed_contract"]["gameplay_seed"] == base_preview["seed_contract"]["gameplay_seed"]
    assert music_preview["seed_contract"]["music_seed"] == 840002

    negative = 0
    original = previews["visual_loops"][0]

    tampered_editorial = copy.deepcopy(original)
    tampered_editorial["binding_preview"]["editorial_bindings"]["title"] = "Tampered without canonical editorial hash"
    _reseal_adapter(tampered_editorial)
    _must_reject("tampered editorial binding disagrees with source identity", lambda: build_renderer_binding_preview(tampered_editorial, ROOT)); negative += 1

    renderer_claim = copy.deepcopy(original)
    renderer_claim["renderer_input_emitted"] = True
    _reseal_adapter(renderer_claim)
    _must_reject("adapter claims renderer input emitted", lambda: build_renderer_binding_preview(renderer_claim, ROOT)); negative += 1

    dispatch_claim = copy.deepcopy(original)
    dispatch_claim["renderer_dispatch_invoked"] = True
    _reseal_adapter(dispatch_claim)
    _must_reject("adapter claims dispatch", lambda: build_renderer_binding_preview(dispatch_claim, ROOT)); negative += 1

    same_seeds = copy.deepcopy(original)
    same_seeds["binding_preview"]["seed_contract"]["music_seed"] = same_seeds["binding_preview"]["seed_contract"]["gameplay_seed"]
    _reseal_adapter(same_seeds)
    _must_reject("gameplay/music seed collision", lambda: build_renderer_binding_preview(same_seeds, ROOT)); negative += 1

    unknown_delivery = copy.deepcopy(original)
    unknown_delivery["binding_preview"]["delivery_profile_id"] = "UNREGISTERED_PROFILE"
    _reseal_adapter(unknown_delivery)
    _must_reject("unknown delivery profile", lambda: build_renderer_binding_preview(unknown_delivery, ROOT)); negative += 1

    unknown_type = copy.deepcopy(original)
    unknown_type["content_identity"]["content_type"] = "longform"
    _reseal_adapter(unknown_type)
    _must_reject("Longform unsupported", lambda: build_renderer_binding_preview(unknown_type, ROOT)); negative += 1

    false_audio = copy.deepcopy(original)
    false_audio["binding_preview"]["audio_enabled"] = "yes"
    _reseal_adapter(false_audio)
    _must_reject("audio flag must be boolean", lambda: build_renderer_binding_preview(false_audio, ROOT)); negative += 1

    missing_presentation = copy.deepcopy(original)
    missing_presentation["binding_preview"]["presentation_profile_id"] = "UNKNOWN"
    _reseal_adapter(missing_presentation)
    _must_reject("unknown presentation profile", lambda: build_renderer_binding_preview(missing_presentation, ROOT)); negative += 1

    original_preview = previews["visual_loops"][1]
    tampered_preview = copy.deepcopy(original_preview)
    tampered_preview["editorial_binding_preview"][0]["value"] = "forged"
    _reseal_preview(tampered_preview)
    _must_reject("preview values must match source envelope", lambda: validate_renderer_binding_preview(tampered_preview, original, ROOT)); negative += 1

    released_preview = copy.deepcopy(original_preview)
    released_preview["execution_boundary"]["release_authority"] = "APPROVED"
    _reseal_preview(released_preview)
    _must_reject("release authority escalation", lambda: validate_renderer_binding_preview(released_preview, original, ROOT)); negative += 1

    active_preview = copy.deepcopy(original_preview)
    active_preview["execution_boundary"]["renderer_activation"] = True
    _reseal_preview(active_preview)
    _must_reject("renderer activation claim", lambda: validate_renderer_binding_preview(active_preview, original, ROOT)); negative += 1

    stale_preview = copy.deepcopy(original_preview)
    stale_preview["preview_sha256"] = "0" * 64
    _must_reject("preview hash tamper", lambda: validate_renderer_binding_preview(stale_preview, original, ROOT)); negative += 1

    with tempfile.TemporaryDirectory(prefix="c11d_renderer_spec_lock_") as temp_dir:
        temp_root = Path(temp_dir)
        spec_path = temp_root / SPEC_REL
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        spec_doc = json.loads((ROOT / SPEC_REL).read_text(encoding="utf-8"))
        spec_doc["approval_state"]["renderer_baseline_approved"] = True
        spec_path.write_text(json.dumps(spec_doc, ensure_ascii=False, indent=2), encoding="utf-8")
        _must_reject("candidate contract cannot self-approve renderer baseline", lambda: _load_spec(temp_root)); negative += 1

    assert positive == 3
    assert deterministic == 3
    assert negative == 13
    return {"content_types": positive, "determinism": deterministic, "negative": negative}


def main() -> int:
    counts = run_checks()
    print(
        "C11-D RENDERER CANDIDATE BINDING PREVIEW PASS | "
        f"content_types={counts['content_types']}/3 | deterministic={counts['determinism']}/3 | "
        f"negative={counts['negative']}/13 | renderer_input=NOT_EMITTED | renderer=OFF | "
        "media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
