from datetime import datetime
import uuid
from pathlib import Path
from ..domain.seed import SeedSet, generate_unique_seeds, MIN_SEED, MAX_SEED, validate_seed


class SeedManager:
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.last = None

    @staticmethod
    def _batch_id() -> str:
        return "batch_%s_%s" % (datetime.now().strftime("%Y%m%d_%H%M%S"), uuid.uuid4().hex[:6])

    def random_set(self, count: int) -> SeedSet:
        s = SeedSet(self._batch_id(), generate_unique_seeds(count), "RANDOM")
        self.last = s
        s.save(self.workspace / (s.batch_id + ".json"))
        return s

    def manual_set(self, seeds) -> SeedSet:
        vals = [validate_seed(int(x)) for x in seeds]
        if not vals or len(vals) != len(set(vals)):
            raise ValueError("Seeds must be unique and non-empty.")
        if any(x < MIN_SEED or x > MAX_SEED for x in vals):
            raise ValueError(f"Seed range is {MIN_SEED}..{MAX_SEED}.")
        s = SeedSet(self._batch_id(), vals, "MANUAL")
        self.last = s
        s.save(self.workspace / (s.batch_id + ".json"))
        return s
