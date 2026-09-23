from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Product:
    product_id: str
    family: str
    seed: int
    root: Path
    mp4: object = None
    wav: object = None
    social_txt: object = None
    manifest_json: object = None
    authoring_json: object = None
    ffprobe_json: object = None
    godot_log: object = None
    status: str = "CANDIDATE"
    metadata: dict = field(default_factory=dict)
