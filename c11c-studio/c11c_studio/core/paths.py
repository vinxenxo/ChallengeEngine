from pathlib import Path


class Paths:
    def __init__(self, root):
        self.root = Path(root).resolve()

    @property
    def tools(self): return self.root / "tools"
    @property
    def prototypes(self): return self.tools / "prototypes"
    @property
    def bulk_tools(self): return self.prototypes / "c11c_bulk"
    @property
    def common_tools(self): return self.prototypes / "c11c_common"
    @property
    def artifacts(self): return self.root / "artifacts"
    @property
    def production(self): return self.artifacts / "production" / "audiovisual"
    @property
    def prototype_artifacts(self): return self.artifacts / "prototypes"
    @property
    def review_assets(self): return self.prototype_artifacts / "c11c_review_assets"
    @property
    def qa(self): return self.artifacts / "qa"
    @property
    def regression(self): return self.artifacts / "regression"
    @property
    def releases(self): return self.artifacts / "releases"
    @property
    def legacy(self): return self.artifacts / "legacy"
    @property
    def tests(self): return self.artifacts / "tests"
    @property
    def scratch(self): return self.artifacts / "scratch"
    @property
    def gui_workspace(self): return self.scratch / "c11c_studio"
    @property
    def gui_logs(self): return self.gui_workspace / "logs"
    @property
    def gui_snapshots(self): return self.gui_workspace / "snapshots"
    @property
    def production_catalog(self): return self.production / "C11C_PRODUCTION_CATALOG.json"

    def family_dir(self, family):
        return self.prototypes / family
