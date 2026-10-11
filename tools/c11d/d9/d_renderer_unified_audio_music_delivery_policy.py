"""Proposal-only audio delivery alignment across Loop, Drill and Challenge.

This module validates metadata and arithmetic only. It neither selects music, emits audio,
performs mixing/normalization, encodes media, nor authorizes renderer execution.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_SCHEMA_V1.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
REGISTRY_SHA256 = "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"
TIMEBASE_SHA256 = "1e190d5bc1541d04f93052ccc27afd8a3ed289d9c2271d364ebbae6548412921"
POLICY_ID = "C11D_UNIFIED_AUDIO_DELIVERY_ALIGNMENT_ALL_CONTENT_TYPES_V1"
CONTRACT_SCHEMA = "C11-D-D9-UNIFIED-AUDIO-MUSIC-DELIVERY-POLICY-PROPOSAL-V1"
OUTPUT_SCHEMA = "C11-D-D9-UNIFIED-AUDIO-MUSIC-DELIVERY-POLICY-PREVIEW-V1"
EXPECTED_LINEAGE = [
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", MANIFEST_SHA256),
    ("profiles/delivery/c11c_video_delivery_profiles.json", REGISTRY_SHA256),
    ("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json", TIMEBASE_SHA256),
]
EXPECTED_PROFILE = {
    "profile_id": "REVIEW_720", "audio_codec": "aac", "audio_profile": "aac_low",
    "audio_bitrate_kbps": 192, "audio_sample_rate_hz": 48000, "audio_channels": 2,
    "profile_fields_are_metadata_only": True, "resolved_alias_count": 0,
}
EXPECTED_MATRIX = [
    {"content_type": "visual_loops", "duration_seconds": 20.0, "delivery_fps": 30, "delivery_frame_count": 600,
     "audio_sample_rate_hz": 48000, "target_pcm_sample_count": 960000, "audio_codec": "aac", "audio_profile": "aac_low",
     "audio_bitrate_kbps": 192, "audio_channels": 2, "timeline_rule": "MATCH_VIDEO_DURATION_PRE_ENCODE",
     "source_audio_selected": False, "music_asset_selected": False, "audio_samples_emitted": False, "audio_delivery_materialized": False},
    {"content_type": "visual_drills", "duration_seconds": 21.0, "delivery_fps": 30, "delivery_frame_count": 630,
     "audio_sample_rate_hz": 48000, "target_pcm_sample_count": 1008000, "audio_codec": "aac", "audio_profile": "aac_low",
     "audio_bitrate_kbps": 192, "audio_channels": 2, "timeline_rule": "MATCH_VIDEO_DURATION_PRE_ENCODE",
     "source_audio_selected": False, "music_asset_selected": False, "audio_samples_emitted": False, "audio_delivery_materialized": False},
    {"content_type": "challenges", "duration_seconds": 15.0, "delivery_fps": 30, "delivery_frame_count": 450,
     "audio_sample_rate_hz": 48000, "target_pcm_sample_count": 720000, "audio_codec": "aac", "audio_profile": "aac_low",
     "audio_bitrate_kbps": 192, "audio_channels": 2, "timeline_rule": "MATCH_VIDEO_DURATION_PRE_ENCODE",
     "source_audio_selected": False, "music_asset_selected": False, "audio_samples_emitted": False, "audio_delivery_materialized": False},
]
EXPECTED_INVARIANTS = [
    "USE_EXPLICIT_REVIEW_720_AUDIO_FIELDS_FROM_PINNED_DELIVERY_REGISTRY",
    "PRE_ENCODE_PCM_TIMELINE_DURATION_EQUALS_VIDEO_DELIVERY_DURATION",
    "PCM_SAMPLE_COUNT_EQUALS_DURATION_SECONDS_TIMES_48000_EXACTLY",
    "DO_NOT_SELECT_OR_SYNTHESIZE_MUSIC_OR_SOUND_EFFECTS",
    "DO_NOT_INFER_SILENCE_AS_DEFAULT_WHEN_AUDIO_ASSET_IS_ABSENT",
    "DO_NOT_MIX_DUCK_FADE_LOOP_OR_CROSSFADE_AUDIO",
    "DO_NOT_APPLY_GAIN_OR_LOUDNESS_NORMALIZATION",
    "CODEC_PRIMING_AND_POST_ENCODE_DURATION_TOLERANCE_REMAIN_UNDEFINED",
    "NO_AUDIO_PAYLOAD_OR_MEDIA_IS_EMITTED_BY_THIS_REVIEW",
]
EXPECTED_APPROVAL = {
    "audio_delivery_profile_policy_approved": False, "music_selection_policy_approved": False,
    "mixing_policy_approved": False, "loudness_policy_approved": False, "audio_timeline_policy_approved": False,
    "unified_delivery_timebase_policy_approved": False, "renderer_baseline_approved": False, "renderer_baseline_frozen": False,
    "d4_8_authorized": False, "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
    "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED", "d9_17_closure": "BLOCKED_NO_GO",
    "d10": "BLOCKED", "release_authority": "NONE",
}
EXPECTED_EXECUTION = {
    "mode": "STATIC_AUDIO_DELIVERY_POLICY_REVIEW_ONLY", "audio_samples_emitted": False,
    "audio_payload_materialized": False, "music_asset_selected": False, "music_asset_emitted": False,
    "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False,
    "production_execution": False, "media_created": False, "c11c_source_mutation": False,
    "d4_8": "BLOCKED", "release_authority": "NONE", "video_render_ready": False,
}
EXPECTED_EXCLUSIONS = {
    "music_selection_and_licensing": "OUT_OF_SCOPE_NOT_DEFINED_NOT_SELECTED",
    "music_editorial_per_content_family": "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED",
    "sound_effects_and_synthetic_audio": "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED",
    "mixing_ducking_gains_fades_loops_crossfades": "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED",
    "loudness_target_measurement_and_normalization": "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED",
    "encoder_priming_and_post_encode_duration_tolerance": "OUT_OF_SCOPE_NOT_DEFINED_NOT_MEASURED",
    "audio_payload_materialization": "FORBIDDEN_IN_THIS_PROPOSAL",
}
EXPECTED_FORBIDDEN = [
    "select, fetch, synthesize or emit a music/audio asset", "assume silence when no audio source exists",
    "mix, duck, loop, fade, crossfade, gain-adjust or loudness-normalize audio",
    "materialize PCM samples or an audio payload", "encode media or invoke the renderer",
    "mutate frozen C11-C sources or manifest", "promote any policy to approved from validation output",
    "authorize D4.8, renderer baseline freeze, D9 closure, D10 or release authority",
]

class UnifiedAudioMusicDeliveryPolicyError(ValueError):
    """Unified audio/music delivery proposal mismatch or governance escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UnifiedAudioMusicDeliveryPolicyError(f"Cannot read required JSON: {path}") from exc
    if not isinstance(value, dict):
        raise UnifiedAudioMusicDeliveryPolicyError(f"JSON root must be object: {path}")
    return value

def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def validate_contract(project_root: Path | str | None = None, *, verify_sources: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    root = _root(project_root)
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / SCHEMA_REL)
    expected_lineage = [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE]
    authority = {
        "frozen_c11c_manifest_sha256": MANIFEST_SHA256,
        "delivery_profile_registry_sha256": REGISTRY_SHA256,
        "unified_delivery_timebase_policy_sha256": TIMEBASE_SHA256,
        "target_profile_id": "REVIEW_720",
    }
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise UnifiedAudioMusicDeliveryPolicyError("Audio delivery policy contract identity/version drift")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise UnifiedAudioMusicDeliveryPolicyError("Audio delivery policy cannot self-promote to renderer input")
    if contract.get("authority") != authority or contract.get("source_lineage") != expected_lineage:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio delivery source lineage/authority drift")
    if contract.get("target_audio_profile") != EXPECTED_PROFILE:
        raise UnifiedAudioMusicDeliveryPolicyError("Target audio profile is not the pinned REVIEW_720 profile")
    expected_policy = {
        "policy_id": POLICY_ID, "state": "PROPOSED_NOT_APPROVED",
        "scope": "TECHNICAL_DELIVERY_ENVELOPE_AND_PRE_ENCODE_TIMELINE_ONLY", "target_profile_id": "REVIEW_720",
        "profile_resolution": "EXPLICIT_REVIEW_720_PROFILE_FIELDS_FROM_PINNED_REGISTRY_METADATA_ONLY",
        "audio_timeline_rule": "MATCH_VIDEO_DELIVERY_DURATION_PRE_ENCODE",
        "sample_count_formula": "ROUND_EXACT_INTEGER(duration_seconds * audio_sample_rate_hz)",
        "audio_format_rule": "AAC_LOW_COMPLEXITY_192_KBPS_48000_HZ_STEREO_FROM_PINNED_REVIEW_720_PROFILE",
        "music_asset_policy": "OUT_OF_SCOPE_NOT_SELECTED_NOT_EMITTED",
        "mixing_policy": "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED",
        "loudness_policy": "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED",
        "missing_audio_policy": "UNRESOLVED_NO_AUTOMATIC_SILENCE_OR_SYNTHESIS",
        "encoder_delay_policy": "OUT_OF_SCOPE_NOT_DEFINED_NOT_MEASURED",
        "post_encode_duration_tolerance": "UNDEFINED_NOT_APPROVED",
        "shared_invariants": EXPECTED_INVARIANTS,
        "audio_payload_materialized": False, "audio_samples_emitted": False,
        "renderer_native_input_emitted": False, "media_creation": False,
    }
    if contract.get("policy") != expected_policy:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio delivery policy semantics/scope drift")
    if contract.get("content_matrix") != EXPECTED_MATRIX:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio timeline/sample-count matrix drift")
    for row in EXPECTED_MATRIX:
        if row["target_pcm_sample_count"] != int(row["duration_seconds"] * row["audio_sample_rate_hz"]):
            raise UnifiedAudioMusicDeliveryPolicyError("Pre-encode audio sample count is not exact")
    if contract.get("excluded_policy_domains") != EXPECTED_EXCLUSIONS:
        raise UnifiedAudioMusicDeliveryPolicyError("Out-of-scope audio/music domains drift")
    if contract.get("approval_state") != EXPECTED_APPROVAL:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio/music approval state must remain locked false/blocked")
    if contract.get("execution_boundary") != EXPECTED_EXECUTION:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio delivery proposal execution/governance boundary drift")
    if contract.get("forbidden_operations") != EXPECTED_FORBIDDEN:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio/music forbidden operations drift")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("additionalProperties") is not False:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio/music policy schema must be strict Draft 2020-12")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(schema).validate(contract)
        except jsonschema.ValidationError as exc:
            raise UnifiedAudioMusicDeliveryPolicyError(f"Audio/music policy schema validation failed: {exc.message}") from exc
    if verify_sources:
        for rel, digest in EXPECTED_LINEAGE:
            path = root / rel
            if not path.is_file():
                raise UnifiedAudioMusicDeliveryPolicyError(f"Pinned audio policy source missing: {rel}")
            actual = _sha(path.read_bytes())
            if actual != digest:
                raise UnifiedAudioMusicDeliveryPolicyError(f"Pinned audio policy source SHA-256 mismatch: {rel}")
    return contract, schema

def build_preview(project_root: Path | str | None = None, *, verify_sources: bool = True) -> dict[str, Any]:
    root = _root(project_root)
    contract, _ = validate_contract(root, verify_sources=verify_sources)
    return {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "policy_id": POLICY_ID,
        "policy_state": "PROPOSED_NOT_APPROVED",
        "proposal_contract_sha256": _sha((root / CONTRACT_REL).read_bytes()),
        "target_audio_profile": copy.deepcopy(contract["target_audio_profile"]),
        "content_matrix": copy.deepcopy(contract["content_matrix"]),
        "shared_invariants": copy.deepcopy(EXPECTED_INVARIANTS),
        "excluded_policy_domains": copy.deepcopy(EXPECTED_EXCLUSIONS),
        "audio_payload_materialized": False,
        "audio_samples_emitted": False,
        "music_asset_selected": False,
        "policy_approved": False,
        "approval_state": copy.deepcopy(contract["approval_state"]),
        "execution_boundary": copy.deepcopy(contract["execution_boundary"]),
    }

def validate_preview(preview: Mapping[str, Any], project_root: Path | str | None = None, *, verify_sources: bool = True) -> dict[str, Any]:
    expected = build_preview(project_root, verify_sources=verify_sources)
    if dict(preview) != expected:
        raise UnifiedAudioMusicDeliveryPolicyError("Audio/music delivery preview mismatch, policy promotion, or execution boundary drift")
    return copy.deepcopy(expected)
