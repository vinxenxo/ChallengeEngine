# C11-C Production Artifact Policy

Final products are stored only under `artifacts/production/audiovisual/`. Review and prototype cleanup scripts do not target this root.

Each product directory keeps the final MP4 and recovery sidecars: social TXT, Godot log, ffprobe JSON, authoring JSON, source manifest, PRODUCT.txt, production manifest, plus WAV/GIF when available. The intermediate AVI is not copied to production.

Product folders are immutable by default. Replacing an existing product requires `-Force`.
