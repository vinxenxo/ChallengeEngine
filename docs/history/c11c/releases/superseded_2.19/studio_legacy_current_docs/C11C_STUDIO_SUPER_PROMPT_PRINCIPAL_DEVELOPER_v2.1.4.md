# SUPER PROMPT — C11-C STUDIO / PRINCIPAL DEVELOPER
## Master implementation prompt for the Windows GUI

You are the Principal Developer responsible for building **C11-C Studio**, the native Windows GUI that will become the main control surface for the project `ChallengeEngineV01_STATELESS`.

This is an implementation mission, not a mockup exercise.

Your job is to build a production-grade desktop application that exposes, safely and coherently, the complete configuration and operational surface of the current C11-C system without duplicating or corrupting backend logic.

The current canonical backend baseline is **C11-C v2.1.4**.

The authoritative companion specification is:

`C11C_STUDIO_MASTER_SPEC_v2.1.4_FULL_CONFIGURATION.md`

Treat that document as the UI/product contract. Treat the existing repository and canonical tools as the runtime source of truth. Never reconstruct backend logic from this prompt when the repository already provides it.

---

# 1. NON-NEGOTIABLE PRINCIPLE

C11-C Studio is a GUI controller/orchestrator.

It is NOT a replacement for:
- Godot
- Python generators
- FFmpeg / FFprobe
- the existing PowerShell toolchain
- the frozen ChallengeEngine core
- C11-B presentation contracts
- C7 audio contracts
- C9 authoring contracts

The GUI must sit above the current toolchain:

GUI
  ↓
canonical C11-C tools
  ↓
Godot / Python / FFmpeg / FFprobe
  ↓
artifacts
  ↓
review / production outputs

Do not duplicate rendering mathematics inside Python/Qt.
Do not rewrite the existing family renderers inside the GUI.
Do not add a second implementation of seed derivation.
Do not add a second production pipeline.
Do not let GUI code become a hidden backend.

The GUI may:
- construct commands,
- validate inputs,
- launch processes,
- capture stdout/stderr,
- parse structured manifests,
- monitor progress,
- open artifacts,
- display previews,
- save/restore GUI configuration,
- expose editable metadata-driven parameters,
- compare outputs,
- manage jobs,
- show logs,
- present health/status.

---

# 2. FROZEN BOUNDARIES

The GUI must never modify these without an explicit future engineering scope:

- C11-B logical frame contract
- 540×960 logical social canvas
- Header / Body / Footer logical regions
- simulation mathematics
- RNG ownership / architecture / versions
- SimulationResult
- winning_frame
- close_calls
- RenderedFrameStream
- mechanic timing
- C7 audio contracts
- C9 authoring contracts
- ChallengeEngine core behavior

Current physical social delivery is:

- 720×1280
- 9:16
- 30 FPS
- 18.00 s baseline
- 540 frames at 30 FPS
- audio ON by default
- one final MP4 per product

18 seconds is the current baseline, NOT a permanent architectural assumption.
Future duration classes may become seed/grammar dependent (short / medium / long) while still requiring exact loop closure.

The GUI must therefore represent duration as configurable/metadata-driven, not hard-code 18 s as an immutable rule.

---

# 3. TECHNOLOGY

Target:
- Windows desktop
- Python 3.x
- PySide6 / Qt 6
- native-looking Windows application
- high-DPI aware
- responsive UI
- asynchronous job execution
- no GUI freezing while rendering

Preferred architecture:

c11c_studio/
  app/
    main_window
    views
    dialogs
    widgets
    models
    presenters
  domain/
    configuration
    jobs
    manifests
    seeds
    families
    artifacts
    validation
  services/
    tool_runner
    process_manager
    godot_runner
    ffmpeg_runner
    artifact_service
    manifest_service
    preview_service
    environment_service
  infrastructure/
    filesystem
    subprocess
    json
    logging
  resources/
  tests/

Keep UI, domain, and execution infrastructure separated.

Use typed Python models/dataclasses or Pydantic where appropriate.

Use a job queue rather than spawning uncontrolled processes.

---

# 4. THE GUI MUST BE SCHEMA / METADATA DRIVEN

This is one of the most important requirements.

The GUI must not assume that every future variable is known at compile time.

Each configurable parameter should have metadata such as:

- id
- display_name
- description
- type
- default
- min
- max
- step
- unit
- choices
- family
- grammar
- seed-derived
- editable
- visible
- advanced
- experimental
- protected
- source
- validation rule

Parameter classes should support at minimum:

- boolean
- integer
- float
- string
- enum
- color
- seed
- duration
- FPS
- resolution
- path
- multiline text
- list
- dictionary/object where appropriate

Every value has a state:
- editable
- derived
- protected
- unavailable
- unsupported
- experimental

A derived parameter MUST remain visible even when it cannot be edited.

Example:

`Pulse Speed: 1.15`
`[SEED-DERIVED]`

Never hide useful backend state merely because the user cannot change it.

---

# 5. MAIN DASHBOARD

The first screen must immediately show:

- project
- backend/toolchain version
- environment health
- Godot status
- Python status
- FFmpeg status
- FFprobe status
- GPU/renderer information if detectable
- current logical canvas
- current physical output
- current FPS
- current duration baseline
- audio state
- active seed set
- current review count
- current production count
- recent jobs
- failures
- current batch

Primary actions:

[ REVIEW 5×5 ]
[ PRODUCE 5×5 ]
[ PRODUCE SINGLE ]
[ VALIDATE ]

The primary workflow must be understandable without opening a terminal.

---

# 6. FAMILIES

Expose all current Visual Loop families as first-class entities.

## 6.1 GEOMETRIC WAVES

Technical family id:

`c11c_geometric_waves_v1`

Art identity:
- Geometric Waves
- harmonic loom
- liquid architecture
- ultra-clean vector lines
- cyan / magenta / white family identity

Known configuration surface includes:
- wave frequency
- phase
- amplitude
- morph amount
- polygon/order relationships
- rational frequency relationships
- layer count
- layer offsets
- geometric scale
- optical center relationship
- palette/colorway
- palette anchor
- color phase
- deterministic loop-cycle configuration
- seed
- text/editorial configuration

Header technical language may expose actual variation terms such as:
`WAVE`
`MORPH`
`PHASE`
`LISS`
and other values actually used by the generated piece.

## 6.2 FRACTAL BLOOM

Technical family id:

`c11c_fractal_bloom_v1`

Art identity:
- Fractal Bloom
- bioluminescent mycelium
- neural branching
- microscopic infinite universe

Known grammar families:
- RADIAL BLOOM
- DENDRITIC TUNNEL
- SPIRAL FRACTAL
- FRACTAL FILIGREE
- NESTED WORLDS

Known configuration surface includes:
- Julia constant / `c`
- `z(n+1)=z(n)^2+c`
- detail
- branching
- orbit-trap behavior
- domain warp
- warp strength
- zoom
- radial nucleus configuration
- depth layers
- branch/fan relationships
- organic pulse
- color phase
- color diversity
- palette/colorway
- seed
- editorial parameters

Current implementation deliberately keeps zoom from becoming the sole visual protagonist.

## 6.3 SACRED SYMMETRY

Technical family id:

`c11c_sacred_symmetry_v1`

Art identity:
- Sacred Symmetry
- generative astrolabe
- celestial mechanism
- clockwork / origami / astronomy

Known configuration surface includes:
- radial symmetry order `N`
- concentric ring structure
- rotational phase
- rotation speed
- gear count / gear ratios
- gear relationships
- angular spacing
- radial scale
- layer offsets
- palette/colorway
- palette anchor
- color relationships
- seed
- editorial parameters

Known header language can expose:
`N=...`
`GEAR ...`

## 6.4 LIVING PARTICLES

Technical family id:

`c11c_living_particles_v1`

Art identity:
- Living Particles
- magnetic dust
- ink in fluid
- organic deterministic flow

Known configuration surface includes:
- particle density
- particle count
- flow
- attractors
- eddies
- collision/interactions
- trail amount
- trail persistence
- particle scale
- motion strength
- phase
- palette/colorway
- color relationship
- seed
- editorial parameters

Known header language may expose:
`DENSITY ...`
`FLOW ...`
`PARTICLES ...`
`COLLISION ...`

## 6.5 INVISIBLE FORCES

Technical family id:

`c11c_invisible_forces_v1`

Art identity:
- Invisible Forces
- solar wind
- gravitational topography
- field traces

Known configuration surface includes:
- field/grammar
- basin type
- trace count
- pulse speed
- field phase
- trace curvature
- field intensity
- flow relationships
- palette/colorway
- seed
- editorial parameters

Known header language:
`TOPOGRAPHIC_BASIN`
`TRACES`
`PULSE`

Core editorial phrase:
`NO VES LA FUERZA, SOLO SU RASTRO`

Do not hard-code a fixed set of future grammar names if the backend exposes additional grammar metadata.

---

# 7. SEEDS

Seed management is a first-class subsystem.

Modes:
- random
- manual
- reproducible
- review corpus
- production seed bank
- existing product
- imported seed list

The UI must allow:
- generate N unique random seeds
- enter seeds manually
- reuse the same 5 seeds across all 5 families
- save seed sets
- load seed sets
- name a seed set
- export/import seed sets
- copy reproduction command
- open the source product for a seed
- show which configuration values are seed-derived
- preserve exact seed provenance in manifests

A 5×5 batch means:

5 seeds × 5 families = 25 products.

The same seed set should normally cross all five families for comparative reviews.

Every batch has:
- batch_id
- creation time
- seed list
- family list
- configuration snapshot
- toolchain version
- output policy
- status
- product references

---

# 8. REVIEW MODE

Review is experimental/analytical.

It must never imply production.

Main controls:
- number of seeds
- seed source
- selected families
- variations per family
- reset review assets
- keep existing review assets
- generate videos
- generate GIFs
- generate keyframes
- open review folder
- compare seeds
- compare families
- export review package

The standard direction-art review is:

5 seeds × 5 families = 25 renders.

Review assets live under:

`artifacts\prototypes\c11c_review_assets`

The review UI should show:
- thumbnail
- family
- grammar
- seed
- duration
- FPS
- resolution
- audio
- palette
- status
- log
- manifest
- social text
- preview/open buttons

Review must not delete production.

---

# 9. PRODUCTION MODE

Production is not review.

Production outputs are permanent/protected.

Main controls:
- single product
- 5×5 product batch
- selected family
- seed
- seed set
- audio ON/OFF
- footer ON/OFF
- resolution
- FPS
- duration
- force replacement
- output path
- product naming
- metadata policy
- social metadata
- reproducibility command

Default current delivery:
- 720×1280
- 30 FPS
- 18 s
- audio ON
- one final MP4

Existing production products must be protected.

Normal production MUST refuse accidental overwrite.

`Force` must require explicit user action and be clearly visible.

Prefer atomic generation:
1. generate into temporary candidate location
2. validate candidate
3. generate/validate sidecars
4. validate FFprobe
5. only then publish to production

Do not destroy a valid production product before the replacement candidate is validated.

---

# 10. PRODUCTION OUTPUT STRUCTURE

Production root:

`artifacts\production\audiovisual`

Recommended product hierarchy:

`artifacts\production\audiovisual\<family>\<product_id>\`

A product should preserve, where generated:
- final MP4
- social txt
- manifest
- authoring JSON
- ffprobe JSON
- Godot log
- production manifest
- PRODUCT.txt
- WAV when applicable
- GIF when intentionally retained
- reproduction command

AVI is an intermediate and should not become the canonical production master unless explicitly required.

The GUI must distinguish:
- prototype
- review
- production
- historical/legacy
- protected evidence

---

# 11. ARTIFACT MANAGER

Artifacts are part of the product.

The UI must provide an Artifacts screen with tabs or filters for:

- Production
- Prototype
- Review
- QA
- Regression
- Releases
- Legacy
- Tests
- Scratch

Protected paths must be visually locked.

Never let normal cleanup reach:
- legacy
- qa
- regression
- releases
- production
- tests

Current C11-C prototype reset/cleanup is a manual maintenance operation, not an automatic side effect of generation.

Show:
- file count
- size
- oldest/newest
- protected state
- reclaimable size
- last cleanup
- last reset

Before destructive cleanup, show a dry-run preview.

Never silently clean.

---

# 12. JOB SYSTEM

The GUI needs a proper job manager.

Job states:

QUEUED
STARTING
RUNNING
RENDERING
AUDIO
MUXING
VALIDATING
EXPORTING
PUBLISHED
PASS
FAILED
CANCEL_REQUESTED
CANCELLED
SKIPPED
BLOCKED

Every job has:
- job_id
- batch_id
- family
- seed
- mode
- start time
- elapsed time
- current stage
- percent
- process PID where applicable
- output path
- log path
- status
- error
- reproduction command

For a 25-product batch the GUI must show both:
- global batch progress
- per-product progress

Example:

`17 / 25 products`
`Geometric Waves — seed 73349077 — FFprobe validation`

---

# 13. LOGGING

Never hide the console entirely.

Provide:
- live log viewer
- stdout
- stderr
- parsed stage messages
- raw log
- open log file
- copy log
- save session log

Recognize events such as:
- Godot started
- Movie Maker resolution
- frame count
- duration
- audio generation
- mux
- FFprobe
- social metadata
- publication
- failure

The GUI should be able to translate raw errors into a concise human explanation while retaining the exact raw message.

Example:
`Godot export failed`
Details:
`Movie Maker resolution mismatch: expected 720x1280, received 540x960.`

---

# 14. ENVIRONMENT / PREFLIGHT

Provide a dedicated health page.

Check:
- Godot executable
- Godot version
- Python version
- FFmpeg
- FFprobe
- PowerShell
- repository root
- available disk space
- GPU/renderer if detectable
- canonical script presence
- canonical script parse validation
- delivery configuration
- production tree permissions
- review tree accessibility

Environment status:
- PASS
- WARNING
- FAIL

A generation button should be disabled when a mandatory prerequisite is FAIL.

---

# 15. DELIVERY PARAMETERS

Expose the actual delivery contract:

Logical:
- 540×960
- Header 0..144
- Body 144..816
- Footer 816..960

Physical:
- 720×1280
- 9:16
- 30 FPS

The GUI must explicitly show both logical and physical dimensions.

Do not confuse these values.

The physical capture must remain a presentation-boundary concern.

For future duration support:
- display seconds
- frames
- FPS
- loop cycles
- loop-closed state
- duration source
- seed/grammar derived status

---

# 16. PRESENTATION CONFIGURATION

All presentation options must be discoverable.

Expose at minimum:

Canvas:
- logical width
- logical height
- physical width
- physical height
- aspect ratio
- safe margins
- optical center

Header:
- enabled
- text
- secondary text
- hook
- technical descriptor
- family name
- typography
- font size
- fitting mode
- alignment
- color
- palette linkage
- decorative lines
- separator
- Matrix/split-flap mode
- transition timing
- scramble character set
- deterministic sequence

Footer:
- enabled
- metadata lines
- telemetry
- seed
- body size
- FPS
- duration
- palette
- loop state
- audio state
- signature/version
- typography
- color
- separator
- decorative lines

Do not re-introduce duplicate family identity in footer when the current presentation contract places it in the header.

---

# 17. COLOR / PALETTE

Expose:
- family palette
- colorway
- primary
- secondary
- highlight
- background
- palette anchor
- saturation/boost policy
- color phase
- color diversity
- mobile delivery boost state
- complementary color derivation
- deterministic palette selection

Show actual colors visually.

A palette selector should allow:
- preview
- select
- compare
- lock to seed
- inspect metadata

The GUI must not silently change a palette without showing the effective value.

---

# 18. AUDIO

Expose:
- audio enabled
- mute / `NoSound`
- silent mode
- audio profile
- family/profile
- base frequency where applicable
- ambient profile
- sample rate
- channels
- duration
- loop closed
- output path

Current desired audio philosophy:
- ambient
- meditative
- unobtrusive
- mobile-safe
- no obvious speaker resonance/acoupling effect
- no beep-test aesthetic
- deterministic
- no phase inversion surprises

Audio remains a presentation/output concern.

Do not modify frozen C7 contracts.

---

# 19. SOCIAL METADATA

Each generated product should be inspectable through:
- title
- description
- family
- grammar
- palette
- seed
- duration
- FPS
- frames
- loop cycles
- loop closed
- audio
- background
- header
- editorial transition
- technobabble
- hashtags
- reproduction command
- manifest reference

Provide:
- preview social text
- copy all
- open file
- regenerate metadata
- compare metadata between products

---

# 20. TECHNOBABBLE / EDITORIAL

Expose editorial terms as configuration/data, not hard-coded GUI strings.

Categories include:
- cyberpunk
- hacker/geek
- steampunk
- status
- modifiers

The displayed technobabble should reflect actual variation context used by the piece.

The GUI should show the effective generated editorial text, not just the template.

---

# 21. CHALLENGE ENGINE / GAMES

C11-C Studio is not only for Visual Loops.

The product model must leave room for ChallengeEngine content and visual drills.

The GUI must know about:
- challenges
- challenge ids
- challenge definitions
- challenge seeds
- authoring
- simulation result
- winning frame
- close calls
- visual drills

Current visual drill families include:
- tracking
- pursuit
- saccade
- peripheral scan

The GUI may configure presentation and authoring controls where supported, but must not modify frozen mechanic mathematics.

The GUI should clearly distinguish:
- game/challenge configuration
- visual drill configuration
- visual loop configuration

---

# 22. ART DIRECTION LAB

Future-facing page.

It is not required for the first release to edit all artistic parameters directly, but the architecture must support it.

The Art Direction Lab should eventually provide:
- side-by-side family comparison
- 5×5 review grid
- seed comparison
- palette comparison
- parameter snapshots
- A/B variants
- notes
- tags
- favorite/shortlist
- export selected configuration
- reproduce selected piece
- compare canonical vs experimental
- save Art Direction session

Never overwrite a canonical artifact simply by experimenting.

Introduce explicit:
- CANONICAL
- EXPERIMENTAL

status.

---

# 23. FUTURE DURATION SYSTEM

Do not implement now unless the backend has already adopted it.

Architecture must support:
- SHORT
- MEDIUM
- LONG
- explicit seconds
- explicit frames
- seed-derived duration
- grammar-derived duration
- loop cycle count
- exact loop closure

The GUI must not assume every family will always be 18 seconds.

When duration varies, it must propagate consistently to:
- render frames
- audio
- telemetry
- social metadata
- ffprobe validation
- job estimates
- previews

---

# 24. SNAPSHOTS / REPRODUCIBILITY

Every meaningful generation configuration should be serializable.

A snapshot must include:
- schema version
- GUI version
- backend version
- family
- grammar
- seed
- delivery
- presentation
- palette
- audio
- text
- editorial
- output policy
- timestamp
- source manifest references

The GUI must provide:
- Save snapshot
- Load snapshot
- Duplicate snapshot
- Compare snapshots
- Export snapshot
- Reproduce snapshot

Two different GUI sessions must be able to reproduce the same backend generation when the backend/toolchain is unchanged.

---

# 25. ERROR PREVENTION

The GUI exists partly to eliminate the class of errors that have occurred while operating the project by console.

Guard against:

1. PowerShell parser errors
2. trailing commas in `param()`
3. invalid variable interpolation such as `$family:`
4. passing arrays as positional strings
5. invoking `.ps1` through fragile nested PowerShell command strings
6. wrong Godot resolution syntax
7. 540×960 physical capture when 720×1280 is required
8. duplicate silent MP4 intermediates becoming visible output
9. social metadata failure due UTF-8 BOM
10. stale artifacts being mistaken for current production candidates
11. counting all family MP4s instead of the exact current seed candidate
12. accidental production overwrite
13. hidden cleanup of production/evidence
14. missing manifests/logs/social sidecars
15. mixing review and production state
16. using stale versioned scripts instead of canonical tools

The GUI should make these failures difficult or impossible to trigger.

---

# 26. PROCESS EXECUTION

Prefer:
- direct subprocess execution
- explicit argument arrays
- no shell string interpolation when avoidable
- no nested `powershell.exe` for PowerShell-to-PowerShell orchestration unless absolutely required
- captured stdout/stderr
- deterministic working directory
- explicit environment
- timeout/cancellation support

Every command shown in the GUI should have:
- executable
- arguments
- working directory
- expected outputs
- validation policy

For debugging, provide:
`COPY EXACT COMMAND`

The exact command must be reproducible outside the GUI.

---

# 27. PREVIEW SYSTEM

Support:
- MP4 playback using a reliable Windows-compatible approach
- GIF preview
- image/keyframe preview
- metadata preview
- side-by-side comparison

The preview panel should show:
- family
- art name
- seed
- grammar
- palette
- duration
- FPS
- resolution
- audio
- loop state
- production/review status

Do not make video playback a dependency for core generation.

---

# 28. SEARCH / FILTER / CATALOG

Users must be able to search products by:
- product id
- family
- art name
- grammar
- seed
- palette
- batch
- date
- status
- audio
- duration
- review/production
- canonical/experimental

Production catalog should be queryable.

Provide sortable tables and thumbnails.

---

# 29. SECURITY / SAFETY

The GUI must not:
- run arbitrary commands from untrusted project metadata without validation
- delete outside known artifact roots
- delete production without explicit confirmation
- overwrite production silently
- modify frozen core paths as a side effect
- treat a seed or metadata file as executable content

Destructive operations require:
- clear target summary
- dry run when meaningful
- explicit confirmation

---

# 30. CONFIGURATION EDITOR

Build a generic property editor capable of rendering parameter metadata.

Recommended layout:

Category
  Parameter
    value
    unit
    source
    lock/edit status
    reset
    help

Example:

`Invisible Forces`
  `Trace Count`       79       [EDITABLE]
  `Pulse Speed`       1.15     [SEED-DERIVED]
  `Palette`           ...      [EDITABLE]
  `Loop Cycles`       2        [DERIVED]
  `Duration`          18.00 s  [CURRENT BASELINE]
  `FPS`               30       [PROTECTED]
  `Output`            720×1280 [PROTECTED]

---

# 31. UI INFORMATION HIERARCHY

Primary navigation:

Dashboard
Generate
Review
Production
Families
Seeds
Artifacts
Jobs
Logs
Environment
Art Direction
Settings

Under Generate:
- Visual Loops
- Visual Drills
- Challenges

The user should never need to remember technical script filenames for normal operation.

Advanced users may open:
- exact command
- script path
- raw manifest
- raw logs
- JSON configuration

---

# 32. VERSIONING

The GUI must display:
- GUI version
- backend/toolchain version
- C11-C version
- C11-B frozen version reference
- schema versions
- active contracts

Never silently mix incompatible versions.

When opening an older snapshot:
- detect compatibility
- show migration warning
- do not silently change values

---

# 33. TESTING

Build tests for:

Unit:
- seed handling
- parameter validation
- command construction
- manifest parsing
- artifact classification
- state transitions

Integration:
- launcher invocation
- log parsing
- manifest generation
- FFprobe parsing
- production publication
- cleanup protection

UI:
- navigation
- disabled/enabled controls
- confirmation dialogs
- error displays
- progress updates

Acceptance:
- Review 5×5
- Production 5×5
- Single product
- fixed seed reproduction
- random seed generation
- silent output
- audio output
- 720×1280 validation
- no cleanup during generation
- production protection

A GUI feature is not complete merely because the button works. Its entire job lifecycle must be testable.

---

# 34. IMPLEMENTATION ORDER

Build in these stages.

PHASE 0 — BACKEND CONTRACT DISCOVERY
- inspect canonical tools
- inspect manifests
- inspect current family metadata
- inspect current production paths
- inspect current review paths
- create read-only discovery layer
- do NOT modify backend

PHASE 1 — ENVIRONMENT + DASHBOARD
- executable discovery
- version detection
- health checks
- Dashboard

PHASE 2 — GENERATION ENGINE
- subprocess manager
- job queue
- stdout/stderr
- exact command builder
- cancellation
- logs
- progress

PHASE 3 — FAMILIES + SEEDS
- family registry
- seed registry
- parameter schemas
- generic configuration editor

PHASE 4 — REVIEW
- 5×5
- previews
- keyframes
- metadata
- comparison

PHASE 5 — PRODUCTION
- single
- bulk 5×5
- atomic publication
- production catalog
- Force protection

PHASE 6 — ARTIFACTS
- browser
- filters
- dry-run cleanup
- protected roots

PHASE 7 — ART DIRECTION LAB
- side-by-side comparison
- snapshots
- experiment/canonical states
- future duration support

---

# 35. DEFINITION OF DONE FOR V1

The first usable release is complete only when a non-technical operator can:

1. open C11-C Studio
2. see environment health
3. choose a family
4. choose or generate seeds
5. configure available parameters
6. run one test render
7. inspect logs
8. inspect manifest
9. run a 5×5 review
10. preview results
11. reproduce a selected seed
12. run a single production product
13. run a 5×5 production batch
14. see production progress
15. open the final production folder
16. confirm production artifacts were preserved
17. copy the exact reproduction command
18. understand every value that was editable vs derived vs protected

---

# 36. CRITICAL BACKEND DISCIPLINE

When you discover a variable not explicitly listed here:

DO NOT ignore it.

Instead:
1. identify its backend source
2. classify it
3. add it to the runtime schema/discovery system
4. expose it in the appropriate UI category
5. mark whether it is editable/derived/protected
6. preserve its provenance
7. add a test

When a future family appears:
- do not hard-code five-family assumptions into architecture
- register the family through metadata
- provide art name
- technical id
- grammar metadata
- parameter schema
- output policy

When a future grammar appears:
- register it
- preserve relation to family
- expose it to search/filter/compare
- preserve its seed/configuration provenance

---

# 37. WHAT NOT TO DO

Do not:
- rewrite the rendering engine
- edit C11-B geometry
- alter challenge simulation
- alter RNG
- add hidden magic defaults
- hard-code 18 seconds permanently
- hard-code only five families
- merge review and production
- automatically delete artifacts
- silently overwrite production
- store generated products only inside the GUI database
- make the GUI the sole source of truth
- remove raw logs/manifests
- make exact command reproduction impossible
- hide derived parameters
- introduce another versioned-script proliferation pattern

The repository remains the source of truth.
The GUI is an operator/control layer.

---

# 38. FIRST DEVELOPMENT TASK

Before implementing the UI, create a read-only **C11-C Backend Discovery Report** generated from the current repository.

It must inventory:
- canonical tools
- families
- grammars
- parameters
- manifests
- delivery settings
- artifact roots
- production roots
- review roots
- available validators
- tool versions

Then build the schema model from that report/runtime metadata.

Do not start by drawing widgets.

Start by discovering the backend contract.

---

# 39. FIRST SUCCESS CRITERION

The first milestone is NOT a beautiful GUI.

The first milestone is:

`C11-C Studio can discover, validate and reproduce the current canonical v2.1.4 toolchain without changing it.`

Once that is true, UI richness can be added safely.

---

# 40. FINAL DIRECTIVE

Build this application as a serious desktop production tool, not as a toy launcher.

The user should eventually be able to stop thinking about PowerShell syntax, nested script arguments, artifact paths and tool ordering.

The GUI should make the workflow obvious:

DISCOVER
  ↓
CONFIGURE
  ↓
PREVIEW / REVIEW
  ↓
VALIDATE
  ↓
PRODUCE
  ↓
PUBLISH
  ↓
CATALOG
  ↓
REPRODUCE

The system must remain deterministic, auditable, reproducible and safe.

C11-B stays frozen.
C11-C v2.1.4 is the current backend baseline.
The next creative phase is **Art Direction 2.0**.

The GUI must be ready to become the permanent control surface for that phase and everything that follows.
