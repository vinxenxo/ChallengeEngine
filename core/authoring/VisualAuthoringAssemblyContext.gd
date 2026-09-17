class_name VisualAuthoringAssemblyContext
extends RefCounted

## C10-A — Infrastructure inputs intentionally kept outside product intent.
## Seed comes from the external seed manager; presentation/assets/audio/provenance
## are explicit contract inputs and are never silently invented by the adapter.

var seed: int
var rng_version: String
var content_id: String
var content_version: String
var engine_version: String
var presentation: Dictionary
var assets: Dictionary
var audio: Dictionary
var provenance: Dictionary

func _init(
    p_seed: int,
    p_rng_version: String,
    p_content_id: String,
    p_content_version: String,
    p_engine_version: String,
    p_presentation: Dictionary,
    p_assets: Dictionary,
    p_audio: Dictionary,
    p_provenance: Dictionary
) -> void:
    seed = p_seed
    rng_version = p_rng_version
    content_id = p_content_id
    content_version = p_content_version
    engine_version = p_engine_version
    presentation = p_presentation.duplicate(true)
    assets = p_assets.duplicate(true)
    audio = p_audio.duplicate(true)
    provenance = p_provenance.duplicate(true)
