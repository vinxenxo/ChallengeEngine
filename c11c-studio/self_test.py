from pathlib import Path
import tempfile

from c11c_studio.domain.seed import SeedRecord, SeedSet, MIN_SEED, MAX_SEED, generate_unique_seeds
from c11c_studio.services.seed_manager import SeedManager
from c11c_studio.services.command_builder import CommandBuilder, CommandSpec


def main() -> int:
    seeds = generate_unique_seeds(5)
    assert len(seeds) == 5 and len(set(seeds)) == 5
    assert all(MIN_SEED <= value <= MAX_SEED for value in seeds)
    seedset = SeedSet("batch_test", seeds, "TEST")
    assert len(seedset.records(["c11c_geometric_waves_v1"])) == 5
    assert isinstance(seedset.records()[0], SeedRecord)

    with tempfile.TemporaryDirectory() as tmp:
        manager = SeedManager(Path(tmp))
        manual = manager.manual_set([1, 2, 3, 4, 5])
        assert manual.seeds == [1, 2, 3, 4, 5]
        assert (Path(tmp) / (manual.batch_id + ".json")).exists()

    spec = CommandSpec("powershell.exe", ["-NoProfile", "-File", "demo.ps1", "-Seeds", "1", "2"])
    assert spec.arguments[-3:] == ["-Seeds", "1", "2"]

    print("C11-C Studio v0.3.0 self-test PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
