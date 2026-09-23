from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArtifactRoot:
    key: str
    path: Path
    label: str
    protection: str
    exists: bool
    size_bytes: int = 0
    file_count: int = 0


PROTECTED_KEYS = {"production", "qa", "regression", "releases", "legacy", "tests"}


class ArtifactRegistry:
    def __init__(self, ctx):
        self.ctx = ctx

    def roots(self):
        p = self.ctx.paths
        specs = [
            ("production", p.production, "Production (audiovisual)", "protected"),
            ("review", p.review_assets, "Review assets", "regenerable"),
            ("prototypes", p.prototypes_artifacts, "Prototypes", "experimental"),
            ("qa", p.qa, "QA evidence", "protected"),
            ("regression", p.regression, "Regression evidence", "protected"),
            ("releases", p.releases, "Releases", "protected"),
            ("legacy", p.legacy, "Legacy", "protected"),
            ("tests", p.tests, "Tests", "protected"),
            ("scratch", p.scratch, "Scratch", "disposable"),
        ]
        out = []
        for key, path, label, protection in specs:
            exists = path.exists()
            size = 0
            files = 0
            if exists:
                for f in path.rglob("*"):
                    try:
                        if f.is_file():
                            files += 1
                            size += f.stat().st_size
                    except Exception:
                        pass
            out.append(ArtifactRoot(key, path, label, protection,
                                    exists, size, files))
        return out

    def is_protected(self, key):
        return key in PROTECTED_KEYS
