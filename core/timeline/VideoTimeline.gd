class_name VideoTimeline
extends ChallengeTimeline

## C6-F0.3.4 — Legacy Compatibility Shim.
## Safely aliases ChallengeTimeline to ensure F1/F2/F3 components (like ChallengeRuntimeBridge, ChallengeValidator, etc)
## remain unbroken without rewriting their specific imports.

func _init(video_cfg: Dictionary) -> void:
	super._init(video_cfg)