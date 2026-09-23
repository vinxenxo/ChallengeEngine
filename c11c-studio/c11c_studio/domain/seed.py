import random
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SeedRecord:
    seed: int
    source: str = "MANUAL"
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    batch_id: object = None
    used_in_families: list = field(default_factory=list)


def generate_unique_seeds(count, min_v=1, max_v=2147483647):
    if count <= 0:
        return []
    if count > (max_v - min_v + 1):
        raise ValueError("Too many unique seeds requested.")
    seen = set()
    out = []
    while len(out) < count:
        s = random.randint(min_v, max_v)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out
