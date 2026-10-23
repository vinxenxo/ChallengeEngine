# C11-D V2B — decisión de evidencia de composición de fuentes

Fecha: 2026-10-23
Estado: PASS_OPERATOR_RUNTIME_EVIDENCE_CAPTURED

## Resultado
- Validación estática: 132/132 PASS.
- Runtime Godot Mono 4.7.1: PASS, código de salida 0 según la consola del operador.
- Candidatos: 4/4.
- Fotogramas fuente: 1.680/1.680.
- Marcadores proyectados: 1.680/1.680.
- Marcador PASS del runtime: exactamente uno; marcador FAIL: ninguno.
- stdout SHA-256: b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb
- stderr SHA-256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

## Recibo
Ruta: definitions\c11d\production\D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_V1_20261023.json
SHA-256: a4684fdb7b3ea4b85f68b561d9aaa64981517f65530ba8a8787f820eb5e3960f

## Fuentes fijadas
- Runner: 5c69f08194213b7bcf48fe7f52bd17e8ec29a2d6e275c4c73787e7fa20b174ff
- Contrato V1: d3265f1ba91dc664e85bbb0dc87ea6b145f0fed34ffa4552412c8fa70c19b2ab
- Harness runtime: 74fe446ef69c92de0291aa739caf1b5c25dbcdaed7f9939eb1e63c9a4623cfe2
- Manifiesto congelado C11-C: e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953

## Decisión y límites
Se registra como superada la ejecución del harness de composición de fuentes en los cuatro candidatos cubiertos por esta prueba. El contrato V1 permanece sin cambios y sirve como especificación histórica de la ejecución.

No se autoriza la implementación productiva, la materialización de payloads, la creación de medios, las pruebas de render productivo ni la promoción de C11-D. renderer=OFF; production_calls=0; media_created=false; render_test_authorized=false. C11-C sigue siendo inmutable y autoritativo.