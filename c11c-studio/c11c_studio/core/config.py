import json
import os
from pathlib import Path


def _config_dir():
    base = os.environ.get("APPDATA") or str(Path.home())
    d = Path(base) / "C11CStudio"
    d.mkdir(parents=True, exist_ok=True)
    return d


class AppConfig:
    def __init__(self, data=None):
        self._data = data or {}
        self._path = _config_dir() / "config.json"

    @classmethod
    def load(cls):
        p = _config_dir() / "config.json"
        if p.exists():
            try:
                return cls(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                return cls({})
        return cls({})

    def save(self):
        self._path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8")

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
