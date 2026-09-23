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
    def production(self):
        return self.artifacts / "production" / "audiovisual"

    @property
    def prototypes_artifacts(self):
        return self.artifacts / "prototypes"

    @property
    def review_assets(self):
        return self.prototypes_artifacts / "c11c_review_assets"

    @property
    def legacy(self): return self.artifacts / "legacy"

    @property
    def qa(self): return self.artifacts / "qa"

    @property
    def regression(self): return self.artifacts / "regression"

    @property
    def releases(self): return self.artifacts / "releases"

    @property
    def tests(self): return self.artifacts / "tests"

    @property
    def scratch(self): return self.artifacts / "scratch"

    def family_prototype_dir(self, folder):
        return self.prototypes / folder
