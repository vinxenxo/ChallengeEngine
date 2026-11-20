# E6 Loop source closure V1 — 2026-11-20

**Scope:** read-only provenance reconciliation for the six Loop Smoke18 candidate rows. No renderer input is emitted.

## Evidence links

- GEOAVR2 harmonic membrane pair (used instead of the earlier Q5 A/B output hashes because the old Q5 outputs differ from the operator-accepted pair): technical mux-only replacement report SHA `15712f3187237f118df05c0c013558c65b2a2f7d342a0e765da8307e7a7ff037`. Its A/B `video_source_sha256` equals the selected Q5_024454 source MP4 SHA `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`; source and final H.264 stream hashes are identical. The operator closeout links this exact GEO replacement report and MP4 hash.
- R1V five-family A/V report: `Q5_024454_45F195`; 10/10 completed A/V outputs, five repeat pairs.
- R1V operator closeout: 10/10 visual/layer/editorial and 10/10 audio listening accepted by operator.
- Loop22 report: `L22_191801_27ABF3`; 44/44 A/V outputs, 22/22 pairs. Operator closeout document is pinned separately.
- R1P recovery: 27/27 receipts and sidecars; six selected Loop receipt indices are linked by the audit.
- Smoke18 matrix remains DRAFT: 18 rows; 6 Loop rows; `e6_accepted=0`.

## Six source candidates

| Row | Selector | Provenance | R1P index |
|---|---|---|---:|
| E6-L-01 | `fractal_bloom/radial_bloom` | R1V | 06 |
| E6-L-02 | `geometric_waves/harmonic_membrane` | R1V | 01 |
| E6-L-03 | `invisible_forces/dipole_field` | R1V | 21 |
| E6-L-04 | `living_particles/swarm` | R1V | 16 |
| E6-L-05 | `sacred_symmetry/astrolabe` | R1V | 11 |
| E6-L-06 | `geometric_waves/interference_plane` | Loop22 | 02 |

## Technical boundary

Historical source stream is H.264 720x1280, 30 fps, `time_base=1/15360`, PTS step 512, encoded `yuvj420p` full-range (`pc`). Archived decode hashes identify `yuv420p` frames; frame images were not written to disk. This does **not** prove a packed RGB24 frame buffer. QImage expects RGB24, stride 2160, 2,764,800 bytes/frame. Historical decoded YUV420P is 1,382,400 bytes/frame, and manifests revalidate exact frame-count × byte-count totals. Source color primaries, transfer and matrix are not declared by these inventories; do not assume BT.709.

The audit must rehash active-checkout inventory, pixel manifest, sidecar FFprobe JSON, R1P launcher/prototype/scene pins and MP4 when present. Missing MP4 is reported as pending, not passed. No external executable is invoked.
