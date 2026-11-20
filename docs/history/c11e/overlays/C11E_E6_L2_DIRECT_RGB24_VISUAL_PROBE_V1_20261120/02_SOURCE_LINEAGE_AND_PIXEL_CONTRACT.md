# Source lineage and pixel contract

The direct viewport frame is a newly rendered sample from the pinned C11-C Loop scene; it is not the historical MP4 frame. Scene, script, renderer, shader, social-frame, editorial, palette, grammar, font and duration dependencies are SHA-pinned in `C11E_E6_L2_DIRECT_RGB24_SOURCE_PIN_MANIFEST_V1.json` and revalidated against the active checkout before and after execution.

The harness requires the viewport image to be exactly 720×1280 `RGBA8`. It fails closed if dimensions or pixel format differ, or if any alpha byte is not 255. The channel extraction is byte-exact: R, G, B are copied in order and alpha is discarded. It does not run a colour transform, use an ICC profile, infer primaries, infer transfer, infer a matrix, or assume BT.709.

The resulting source buffer must be exactly 2,764,800 bytes with a 2160-byte row stride. The existing QImage module then executes its established scale and black-band/gutter composition; its output must also be exactly 2,764,800 RGB24 bytes at 720×1280.

The historical YUV420P/`yuvj420p` pixel evidence remains a separate provenance record. This route does not convert that stream and makes no equality claim against it.
