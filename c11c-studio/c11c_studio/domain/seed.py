import json
import secrets
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path


MIN_SEED = 1
MAX_SEED = 2147483646


@dataclass(frozen=True)
class SeedRecord:
    seed: int
    source: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    batch_id: str | None = None
    used_in_families: tuple[str, ...] = ()

    def serializable(self) -> dict:
        return asdict(self)


def validate_seed(value: int) -> int:
    value = int(value)
    if value < MIN_SEED or value > MAX_SEED:
        raise ValueError(f"Seed range is {MIN_SEED}..{MAX_SEED}.")
    return value


def generate_unique_seeds(count: int) -> list[int]:
    count = int(count)
    if count < 1 or count > 1000:
        raise ValueError("Seed count must be between 1 and 1000.")
    values: set[int] = set()
    while len(values) < count:
        values.add(secrets.randbelow(MAX_SEED - MIN_SEED + 1) + MIN_SEED)
    return list(values)


@dataclass
class SeedSet:
    batch_id: str
    seeds: list[int]
    source: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def __post_init__(self) -> None:
        self.seeds = [validate_seed(x) for x in self.seeds]
        if not self.seeds:
            raise ValueError("SeedSet must contain at least one seed.")
        if len(self.seeds) != len(set(self.seeds)):
            raise ValueError("SeedSet seeds must be unique.")

    def records(self, families: list[str] | None = None) -> list[SeedRecord]:
        used = tuple(families or ())
        return [SeedRecord(seed=s, source=self.source, created_at=self.created_at, batch_id=self.batch_id, used_in_families=used) for s in self.seeds]

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")
        return path
