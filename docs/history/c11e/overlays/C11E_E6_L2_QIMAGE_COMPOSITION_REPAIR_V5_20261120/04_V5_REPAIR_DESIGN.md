# V5 repair design

V5 is a QImage-only continuation from the immutable V4 RGB24 capture. It validates V4 receipt/sidecar, installation receipt/sidecar, import/capture log hashes, metadata, source PNG dimensions, source buffer length and source PNG-to-RGB24 pixel equality. It then loads the already pinned compositor using the corrected `sys.modules`-registered file loader and executes exactly one QImage composition.

No Godot process is started. Output files and a new V5 receipt/sidecar are written under a new unique V5 artifact root. V4 artifacts and receipts are never altered.
