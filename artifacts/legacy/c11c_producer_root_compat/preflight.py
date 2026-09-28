from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent.parent / "c11c-suite" / "c11c-producer" / "preflight.py"), run_name="__main__")
