# C11 Freeze — Stable Random Seed Policy

## Goal

Exercise many seeds without introducing flaky tests.

## Two seed classes

### Canonical seeds

The six C11-A.1 seeds are immutable compatibility fixtures.

### Stress seeds

Generated from one deterministic corpus seed. The generated list is stored as JSON and becomes an evidence artifact.

Default configuration:

- corpus seed: `0xC11F2026`
- count: 32
- domain: `1..2147483646`
- uniqueness: required

Changing the corpus seed or count creates a new corpus version; it never mutates the old one.

## Recommended matrix

### Headless stress

9 challenges × 32 stress seeds = 288 deterministic simulation runs.

### Physical smoke

9 challenges × 3 selected stress seeds = 27 videos.

### Full canonical compatibility

9 challenges × 6 canonical seeds = 54 runs, already certified by C11-A.1 and rerun during freeze validation.

## Reproducibility

Every report records:

- corpus version;
- corpus generator seed;
- seed list SHA-256;
- challenge definition SHA-256;
- Godot version;
- runner version.
