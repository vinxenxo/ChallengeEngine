import json
import os
from pathlib import Path


def config_path() -> Path:
    base = Path(os.environ.get("APPDATA") or Path.home())
    p = base / "C11CStudio" / "config.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


class AppConfig:
    def __init__(self, data=None):
        self.data = dict(data or {})
        self.path = config_path()

    @classmethod
    def load(cls):
        p = config_path()
        if not p.exists():
            return cls()
        try:
            return cls(json.loads(p.read_text(encoding="utf-8-sig")))
        except (OSError, ValueError):
            return cls()

    def save(self):
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
