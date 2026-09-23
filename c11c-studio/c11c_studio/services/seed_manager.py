import json
import uuid
from datetime import datetime
from pathlib import Path

from ..domain.seed import SeedRecord, generate_unique_seeds


class SeedManager:
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._current_batch_id = None
        self._records = []

    def new_batch_id(self):
        self._current_batch_id = (
            datetime.now().strftime("batch_%Y%m%d_%H%M%S_")
            + uuid.uuid4().hex[:6])
        return self._current_batch_id

    def random_batch(self, count, source="RANDOM"):
        bid = self.new_batch_id()
        seeds = generate_unique_seeds(count)
        recs = [SeedRecord(seed=s, source=source, batch_id=bid) for s in seeds]
        self._records.extend(recs)
        return recs

    def manual_batch(self, seeds):
        bid = self.new_batch_id()
        recs = [SeedRecord(seed=s, source="MANUAL", batch_id=bid) for s in seeds]
        self._records.extend(recs)
        return recs

    @property
    def records(self):
        return list(self._records)

    def save_batch(self, recs):
        bid = recs[0].batch_id or self.new_batch_id()
        path = self.workspace / (bid + ".json")
        path.write_text(json.dumps([r.__dict__ for r in recs], indent=2),
                        encoding="utf-8")
        return path
