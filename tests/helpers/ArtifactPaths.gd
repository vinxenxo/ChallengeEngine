class_name ArtifactPaths
extends RefCounted

## Canonical generated-artifact resolver for tests and QA.
## Source fixtures belong under tests/fixtures; generated evidence belongs under artifacts/.

const ROOT := "res://artifacts"
const TESTS := ROOT + "/tests"
const QA := ROOT + "/qa"
const REGRESSION := ROOT + "/regression"
const PRODUCTION := ROOT + "/production"
const AUDIOVISUAL := PRODUCTION + "/audiovisual"
const CHALLENGES := PRODUCTION + "/challenges"
const SCRATCH := ROOT + "/scratch"

static func absolute(relative_path: String) -> String:
	return ProjectSettings.globalize_path(ROOT + "/" + relative_path.trim_prefix("/"))

static func ensure(relative_dir: String) -> String:
	var path := ROOT + "/" + relative_dir.trim_prefix("/")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path))
	return ProjectSettings.globalize_path(path)
