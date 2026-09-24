from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Product:
    product_id: str
    family: str
    seed: int | None
    root: Path
    status: str = "DISCOVERED"
    files: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    @property
    def mp4(self): return self.files.get("mp4")
    @property
    def manifest(self): return self.files.get("manifest")
