# Production and Distribution — C11-C 2.19.12

C11-C production uses declarative delivery profiles and canonical production launchers. Review and production are separate workflows.

`c11c-suite` GUI operations delegate to the same scripts used from the command line. This parity rule is part of the D architecture and must remain visible while developing new asset, music and personalization layers.

The frozen source archive excludes generated `artifacts/` while carrying compact acceptance/review evidence under `release/evidence/`.
