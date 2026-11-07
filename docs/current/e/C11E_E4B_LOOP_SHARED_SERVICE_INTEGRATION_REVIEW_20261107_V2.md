# E4B Loop Shared Service Integration Review — V2

## Intended architecture

One E1 `c11e_production_service.py` boundary prepares the same Loop family-stage contract for Producer GUI and CLI. GUI rendering code consumes the service result; it must not own a separate business-rule implementation. Existing D9.9 canonical plan, D9.10 bridge and D-only adapter remain the named seam. No new Producer, sixth GUI surface, duplicated binder or new editorial request fields.

## Source postimages

V1 source postimages remain the V2 targets:

- service `08ab5a278de8ebb55795a57391c83a27207ce01920704c419b8e28be25ddcf65`
- GUI main `ad88ac99a4582a6a470b8885425144ab7265188c3771ed4c48d8857c43343c55`
- service tests `6fecc35f3f3d8dc0e138a70452b1eee9acadbcd8f95db05dc6518baad80ed285`
- D9.8 model JSON `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`
- D9.8 implementation `dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd`
- D9.8 tests `d36319e49fcc93c530a7fd2747d6db2536aa70f4fcd02825d1836d0795045e4c`

The V1 package's 25 service tests and D9.8 tests were rerun in a reconstructed V79 workspace with these postimages and passed. V1 Windows installation itself aborted before its add-only or source mutation stage. Do not treat that local test as Windows checkout acceptance.

## Install failure and V2 correction

The failed `System.IO.File.Copy` destination was 262 characters. The installer had already staged all 21 package files and had saved two exact backups. Its code backs up all sources before writing add-only destinations or replacing sources, so the error occurred before those writes. V2 uses six short `b/01.bak`…`b/06.bak` slots, validates containment, collision and length for every slot before the first backup copy, and records exact source-to-slot mappings.

## Required acceptance

1. PowerShell 5.1 AST and installer payload integrity PASS.
2. Exact V79 preimages and frozen C11-C manifest PASS; six backups verify exact source preimage SHA.
3. Fifteen add-only destinations installed; six postimage hashes verified.
4. V2 runner: 25/25 service tests, D9.8 test PASS, in-memory syntax compile PASS, 6/6 postimage pins.
5. Read-only D9.15/D-baseline results reported distinctly.

This integration prepares the shared boundary for 27 Loop grammars. It does not produce renderer payloads, consume pixels, connect the family adapter for rendering, invoke music, mux media or authorize D4.8. `family_adapter=NOT_CONNECTED_E1` remains the truthful runtime status until actual pixel consumption is implemented and proven.
