class_name ArtifactPaths
extends RefCounted

## C11 Freeze — canonical generated-artifact paths.
## Tests must use this resolver instead of embedding output/export/qa roots.

const ROOT := "res://artifacts"
const TESTS := ROOT + "/tests"
const QA := ROOT + "/qa"
const REGRESSION := ROOT + "/regression"
const PRODUCTION := ROOT + "/production"
const SCRATCH := ROOT + "/scratch"

static func absolute(relative_path: String) -> String:
	return ProjectSettings.globalize_path(ROOT + "/" + relative_path.trim_prefix("/"))

static func ensure(relative_dir: String) -> String:
	var path := ROOT + "/" + relative_dir.trim_prefix("/")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path))
	return ProjectSettings.globalize_path(path)
