class_name PresentationBindingResult
extends RefCounted

var success: bool = false
var error: String = ""

var presentation_profile: PresentationProfile = null
var presentation_render_model: Dictionary = {}

var audio_profile: Dictionary = {}

var asset_family_meta: Dictionary = {}
var physical_assets: Dictionary = {}

var timeline: VideoTimeline = null
var winning_frame: int = -1