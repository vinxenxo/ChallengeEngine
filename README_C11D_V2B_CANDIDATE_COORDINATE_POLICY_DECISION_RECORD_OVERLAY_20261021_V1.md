# C11-D V2-B Coordinate Policy Decision Record Overlay V1

This is an ADD_ONLY overlay for an operator decision record on the previously tested coordinate-policy proposal. It does not alter the proposal, source files, coordinate mapper, challenge JSON, renderer code, payload consumer, or C11-C.

Decision scope: **future consumer specification only**. Five coordinate policy choices are accepted within that scope; pixel rounding/crop raster semantics remain blocked. No runtime transform, binding, projection, consumer, render test or media is authorized.

Expected prior coordinate proposal evidence: 961/961, stdout `439e68e15c72975ccc3ac26d42e5e8e8dc5019bcc4e9f1f3051fd061701b07f3`, stderr empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, receipt `1518168dd6b50fc869dbd18b05dcdef13397ea8023ff6fa1f896f55dee5b9f96`. Prior field-region decision: 653/653, receipt `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`. Prior semantic decision: 146/146, receipt `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.

Frozen C11-C manifest pin: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `CHALLENGE_008` and `CHALLENGE_009` remain blocked. `renderer=OFF`, payload/media false, candidate input inadmissible and release authority NONE remain unchanged.

Apply only from the active checkout after verifying every manifest pin. Run the independent Python static regression suite and require the exact test denominator in the manifest, zero stderr and unchanged pins. These are static policy checks; they must not invoke Godot or create media.
