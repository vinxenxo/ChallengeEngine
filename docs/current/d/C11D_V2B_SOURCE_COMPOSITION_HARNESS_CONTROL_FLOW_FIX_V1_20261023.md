# C11-D V2B — corrección de control de flujo del harness

Fecha: 2026-10-23
Estado: APLICADA_PENDIENTE_DE_TEST
Alcance: harness de pruebas de composición; sin cambios productivos.

## Causa observada
El harness imprimía el marcador PASS y llamaba a quit(0), pero continuaba dentro de _run(), alcanzando después la rama que imprime FAIL y llama a quit(1).

## Corrección aplicada
Se añade return inmediatamente después de quit(0), para impedir que el camino de éxito continúe hacia la rama de fallo.

## Integridad
Runtime SHA256 nuevo: 74FE446EF69C92DE0291AA739CAF1B5C25DBCDAED7F9939EB1E63C9A4623CFE2
Runner SHA256 conservado: 5C69F08194213B7BCF48FE7F52BD17E8EC29A2D6E275C4C73787E7FA20B174FF
Contrato SHA256 conservado: D3265F1BA91DC664E85BBB0DC87EA6B145F0FED34FFA4552412C8FA70C19B2AB
Manifiesto congelado C11-C SHA256: E405D08E4D166B1AD95953558F4A088E73EEA9527E6E89244BEB4096EAC4B953

## Límites
renderer=OFF
media_created=false
production_calls=0
render_test_authorized=false
C11-C permanece inmutable.
La aceptación del test queda pendiente de una ejecución real con código de salida 0.